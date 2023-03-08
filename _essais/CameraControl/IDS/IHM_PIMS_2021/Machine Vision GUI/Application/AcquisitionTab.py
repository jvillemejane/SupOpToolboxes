from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc
from math import floor
from pyueye import ueye
import numpy as np
import cv2
import serial
import serial.tools.list_ports
import threading


from Utils import QLabelRect, v_line, h_line, convert_cv_to_qpixmap, WarningWidget
from camera import uEyeCamera
from Dictionary_EN import *


class AcquisitionTab(Qtw.QWidget):
    """The acquisition tab widget is build here"""

    send_screenshot_signal = Qtc.pyqtSignal(np.ndarray)

    def __init__(self, cam, video_thread, ser):
        super().__init__()

        self.displayed_cv_img = np.array([])
        self.displayed_qt_img = np.array([])
        self.displayed_cv_screenshot = np.array([])
        self.displayed_qt_screenshot = np.array([])
        self.ser = ser


        self.cam = cam
        self.max_width_AOI = self.cam.width_max.value
        self.max_height_AOI = self.cam.height_max.value
        self.cam.set_colormode(ueye.IS_CM_MONO8)
        self.cam.set_aoi(0, 0, self.max_width_AOI, self.max_height_AOI)
        self.cam.alloc()
        self.cam.capture_video()

        # Creating and connecting the QThread for read the video from the camera
        self.get_video_thread = video_thread
        self.get_video_thread.new_cv_img_signal.connect(self.update_video_qlabel)

        # Creating icons for acquisition_button QPushButton
        self.start_icon = Qtg.QIcon(":/start_icon.png")
        self.stop_icon = Qtg.QIcon(":/stop_icon.png")

        # QLabel for showing pixmap of the live video  from the camera
        self.video_qlabel = QLabelRect()  # QLabel from a overriding class (see below)
        self.video_qlabel.setAlignment(Qtc.Qt.AlignLeft)
        self.video_qlabel.setAlignment(Qtc.Qt.AlignTop)
        self.video_qlabel.setSizePolicy(Qtw.QSizePolicy.MinimumExpanding, Qtw.QSizePolicy.MinimumExpanding)

        # QLabel for showing pixmap of the screenshot taken from live video
        self.screenshot_qlabel = Qtw.QLabel()
        self.screenshot_qlabel.setAlignment(Qtc.Qt.AlignLeft)
        self.screenshot_qlabel.setAlignment(Qtc.Qt.AlignTop)

        # QPushButton for taking a screenshot from live video
        self.take_screenshot_button = Qtw.QPushButton(STR_TAKE_SCREENSHOT)
        screenshot_icon = Qtg.QIcon(":/screenshot_icon.png")
        self.take_screenshot_button.setIcon(screenshot_icon)
        self.take_screenshot_button.setEnabled(False)
        self.take_screenshot_button.clicked.connect(self.take_screenshot)

        # QPushButton for saving the screenshot into a file
        self.save_screenshot_button = Qtw.QPushButton(STR_SAVE_SCREENSHOT)
        save_icon = Qtg.QIcon(":/save_icon.png")
        self.save_screenshot_button.setIcon(save_icon)
        self.save_screenshot_button.setEnabled(False)
        self.save_screenshot_button.clicked.connect(self.save_screenshot)
        self.save_screenshot_shortcut = Qtw.QShortcut(Qtg.QKeySequence('Ctrl+S'), self)

        # QPushButton for copying the screenshot into the clipboard
        self.clipboard_screenshot_button = Qtw.QPushButton(STR_COPY_TO_CLIPBOARD)
        self.clipboard_screenshot_button.setIcon(Qtg.QIcon(":/clipboard_icon.png"))
        self.clipboard_screenshot_button.setEnabled(False)
        self.clipboard_screenshot_button.clicked.connect(self.clipboard_screenshot)
        self.clipboard_screenshot_shortcut = Qtw.QShortcut(Qtg.QKeySequence('Ctrl+C'), self)

        # QPushButton for launching and stop live acquisition
        self.acquisition_button = Qtw.QPushButton()
        self.state_acquisition_button = False
        self.acquisition_button.clicked.connect(self.clicked_acquisition_button)

        # # All QObject for the lighting setting
        # self.belt_on_off = Qtw.QCheckBox(STR_CONVEYOR)
        # self.belt_speed_slider = Qtw.QSlider(Qtc.Qt.Horizontal)
        # self.belt_speed_slider.setMinimum(1)
        # self.belt_speed_slider.setMaximum(100)
        # self.led_bar_1_on_off = Qtw.QCheckBox(STR_LED_BAR + ' 1')
        # self.led_bar_2_on_off = Qtw.QCheckBox(STR_LED_BAR + ' 2')
        # self.dome_light_on_off = Qtw.QCheckBox(STR_DOME_LIGHT)
        # self.dark_field_ring_on_off = Qtw.QCheckBox(STR_DF_RING)
        # self.red_ring_on_off = Qtw.QCheckBox(STR_RED)
        # self.green_ring_on_off = Qtw.QCheckBox(STR_GREEN)
        # self.blue_ring_on_off = Qtw.QCheckBox(STR_BLUE)
        #
        # # A QObjet for camera info
        # self.cam_id_qlabel = Qtw.QLabel()
        # self.cam_name_qlabel = Qtw.QLabel()
        # self.cam_ser_no_qlabel = Qtw.QLabel()
        # self.cam_sensor_width_qlabel = Qtw.QLabel()
        # self.cam_sensor_height_qlabel = Qtw.QLabel()
        # self.cam_pixel_size_qlabel = Qtw.QLabel()
        # self.cam_aoi_width = Qtw.QLabel()
        # self.cam_aoi_height = Qtw.QLabel()

        # All QObject for the camera setting
        self.pixelclock_qlabel = Qtw.QLabel("Pixel clock [MHz]")
        self.value_pixelclock_qlabel = Qtw.QLabel()

        self.framerate_qlabel = Qtw.QLabel("Framerate [fps]")
        self.max_value_framerate_qlabel = Qtw.QLabel()
        self.min_value_framerate_qlabel = Qtw.QLabel()
        self.framerate_spinbox = Qtw.QSpinBox()
        self.framerate_spinbox.setValue(10)
        self.framerate_spinbox.valueChanged.connect(self.update_framerate)

        self.exposure_qlabel = Qtw.QLabel("Exposure time [ms]")
        self.max_value_exposure_qlabel = Qtw.QLabel()
        self.min_value_exposure_qlabel = Qtw.QLabel()
        self.exposure_spinbox = Qtw.QSpinBox()
        self.exposure_spinbox.setValue(10)
        self.exposure_spinbox.valueChanged.connect(self.update_exposure)

        self.aoi_button = Qtw.QPushButton(STR_NEW_AOI)
        self.aoi_button.clicked.connect(self.new_aoi)

        self.gray_radio = Qtw.QRadioButton(STR_GRAYSACLE)
        self.gray_radio.setChecked(True)
        self.gray_radio.toggled.connect(self.update_colormode)
        self.rgb_radio = Qtw.QRadioButton(STR_RGB)

        self.acquisition_set_enable(False)

        self.light_setting_and_camera_info_widget = LightSettingAndCamInfo(self.ser)

        self.light_setting_and_camera_info_widget.update_cam_info(self.cam.get_cam_info(),
                                                             self.cam.get_sensor_info(),
                                                             self.cam.get_aoi())

        # Building layout
        main_grid_layout = Qtw.QGridLayout()  # the grid layout will have 3(row)*3(column) cases
        main_grid_layout.addWidget(self.video_qlabel, 1, 0)
        main_grid_layout.addWidget(self.screenshot_qlabel, 1, 2)
        main_grid_layout.addWidget(self.acquisition_button, 2, 0)
        main_grid_layout.addLayout(self.screenshot_buttons_layout(), 2, 2)
        #main_grid_layout.addLayout(LightSettingAndCamInfo(), 0, 2)
        main_grid_layout.addWidget(self.light_setting_and_camera_info_widget, 0, 2)
        main_grid_layout.addLayout(self.camera_setting_layout(), 0, 0)
        main_grid_layout.addWidget(v_line(), 0, 1, 2, 1)

        h_l = Qtw.QHBoxLayout()
        h_l.addStretch(1)
        main_grid_layout.addLayout(h_l, 0, 2)

        self.setLayout(main_grid_layout)

        self.update_pixel_clock()
        self.update_framerate()
        self.update_exposure()

        self.update_min_max_exposure()
        self.update_min_max_framerate()


    @Qtc.pyqtSlot()
    def clicked_acquisition_button(self):
        """Slot connected to the clicked signal of acquisition_button. Turn on or off the acquisition"""
        if not self.state_acquisition_button:
            # If acquisition is off then is turn on. Also enabling screenshot and camera setting buttons
            self.acquisition_set_enable(True)
        else:
            # Else acquisition is on then is turn off. ALso disabling screenshot and camera setting buttons
            self.acquisition_set_enable(False)

    @Qtc.pyqtSlot(bool)
    def update_colormode(self, gray_checked):
        """Slot connected to the toggled signal of gray_radio (QRadioBox)"""
        if gray_checked:  # if gray_radio is checked
            colormode = ueye.IS_CM_MONO8
        else:  # else rgb_radio is checked
            colormode = ueye.IS_CM_BGR8_PACKED

        self.get_video_thread.stop()
        self.cam.stop_video()
        self.cam.un_alloc()
        self.cam.set_colormode(colormode)
        self.cam.alloc()
        self.update_min_max_framerate()
        self.update_framerate()
        self.update_min_max_exposure()
        self.update_exposure()
        self.cam.capture_video()
        self.get_video_thread.start()

    @Qtc.pyqtSlot(np.ndarray)
    def update_video_qlabel(self, cv_img):
        """Slot connected to the new_cv_img_signal signal of GetVideoThread (QRadioBox). Updates the video_qlabel
        with a new opencv image from the camera """
        #qt_img = convert_cv_to_qpixmap(cv_img[self.aoi[0]:self.aoi[2], self.aoi[1]:self.aoi[3]],
        #                               self.video_qlabel.size())

        qt_img = convert_cv_to_qpixmap(cv_img, self.video_qlabel.size())
        self.displayed_cv_img = cv_img
        self.displayed_qt_img = qt_img
        self.video_qlabel.setPixmap(qt_img)

    @Qtc.pyqtSlot()
    def take_screenshot(self):
        """Slot connected to the clicked signal of take_screenshot_button (QPushButton). Take a scrrenshot by showing
        the current image of live  video (on video_qlabel) on screenshot_qlabel."""

        # Save and Clipboard buttons are enabled the first time a screenshot is taken
        if self.displayed_cv_screenshot.size == 0:
            self.save_screenshot_button.setEnabled(True)
            self.save_screenshot_shortcut.activated.connect(self.save_screenshot)
            self.clipboard_screenshot_button.setEnabled(True)
            self.clipboard_screenshot_shortcut.activated.connect(self.clipboard_screenshot)

        self.displayed_cv_screenshot = self.displayed_cv_img
        self.displayed_qt_screenshot = self.displayed_qt_img

        self.screenshot_qlabel.setPixmap(self.displayed_qt_screenshot)

    @Qtc.pyqtSlot()
    def save_screenshot(self):
        """Slot connected to the clicked signal of save_screenshot_button (QPushButton). It open a window for choosing
        a path and a file name """

        filename = Qtw.QFileDialog.getSaveFileName(self, STR_SAVE_IMAGE, '', STR_IMAGE_FORMAT)
        if filename[0] != "":
            cv2.imwrite(filename[0], self.displayed_cv_screenshot)

    @Qtc.pyqtSlot()
    def clipboard_screenshot(self):
        Qtw.QApplication.clipboard().setPixmap(convert_cv_to_qpixmap(self.displayed_cv_screenshot, None))

    @Qtc.pyqtSlot(Qtc.QPoint, Qtc.QPoint)
    def get_release_pos(self, qpos0, qpos1):

        # Retrieving the total width and height of the displayed picture
        xt = self.video_qlabel.pixmap().width()
        yt = self.video_qlabel.pixmap().height()

        # Calculating the coordinates in the original image and in the displayed one (with is scaled)
        x0 = floor(qpos0.x()/xt*self.max_width_AOI)
        y0 = floor(qpos0.y()/yt*self.max_height_AOI)
        x1 = floor(qpos1.x()/xt*self.max_width_AOI)
        y1 = floor(qpos1.y()/yt*self.max_height_AOI)

        # Setting the new AOI, first mouse click can any corner of the rectangle AOI
        self.get_video_thread.stop()
        self.cam.stop_video()
        self.cam.un_alloc()
        self.cam.set_aoi(min(x0, x1), min(y0, y1), max(x0, x1)-min(x0, x1), max(y0, y1)-min(y0, y1))

        # print(min(x0, x1), min(y0, y1), max(x0, x1)-min(x0, x1), max(y0, y1)-min(y0, y1))
        self.cam.alloc()
        self.update_min_max_framerate()
        self.update_framerate()
        self.update_min_max_exposure()
        self.update_exposure()
        self.cam.capture_video()
        self.get_video_thread.start()

        self.light_setting_and_camera_info_widget.update_aoi(self.cam.get_aoi())

        # Enabling all the buttons once AOI is set.
        self.acquisition_button.setEnabled(True)
        self.aoi_button.setEnabled(True)
        self.take_screenshot_button.setEnabled(True)
        if self.displayed_cv_screenshot.size != 0:
            self.save_screenshot_button.setEnabled(True)
            self.clipboard_screenshot_button.setEnabled(True)
        self.framerate_spinbox.setEnabled(True)
        self.exposure_spinbox.setEnabled(True)
        self.gray_radio.setEnabled(True)
        self.rgb_radio.setEnabled(True)

        # Disconnecting the signal
        self.video_qlabel.mouse_released_signal.disconnect(self.get_release_pos)
        self.video_qlabel.setting_aoi = False

    @Qtc.pyqtSlot()
    def new_aoi(self):
        # Setting the AOI to maximum (displaying the all picture) in order to choose the new AOI
        self.get_video_thread.stop()
        self.cam.stop_video()
        self.cam.un_alloc()
        self.cam.set_aoi(0, 0, self.max_width_AOI, self.max_height_AOI)
        self.cam.alloc()
        self.update_min_max_framerate()
        self.update_framerate()
        self.update_min_max_exposure()
        self.update_exposure()
        self.cam.capture_video()
        self.get_video_thread.start()

        # Disabling all the buttons while in AOI setting mode.
        self.acquisition_button.setEnabled(False)
        self.aoi_button.setEnabled(False)
        self.take_screenshot_button.setEnabled(False)
        self.save_screenshot_button.setEnabled(False)
        self.clipboard_screenshot_button.setEnabled(False)
        self.framerate_spinbox.setEnabled(False)
        self.exposure_spinbox.setEnabled(False)
        self.gray_radio.setEnabled(False)
        self.rgb_radio.setEnabled(False)

        # Connecting the signal
        self.video_qlabel.mouse_released_signal.connect(self.get_release_pos)
        self.video_qlabel.setting_aoi = True

    @Qtc.pyqtSlot()
    def send_screenshot(self):
        self.send_screenshot_signal.emit(self.displayed_cv_screenshot)

    def update_exposure(self):
        exposure = self.exposure_spinbox.value()
        self.cam.set_exposure(exposure)

    def update_min_max_exposure(self):
        mini, maxi = self.cam.get_exposure_range()
        self.min_value_exposure_qlabel.setText(str(mini))
        self.max_value_exposure_qlabel.setText(str(maxi))
        self.exposure_spinbox.setRange(mini, maxi)

    def update_framerate(self):
        framerate = self.framerate_spinbox.value()
        self.cam.set_framerate(framerate)
        self.update_min_max_exposure()

    def update_min_max_framerate(self):
        a = self.cam.get_frame_time_range()
        mini = floor(1/a[1])
        maxi = floor(1/a[0])
        self.min_value_framerate_qlabel.setText(str(mini))
        self.max_value_framerate_qlabel.setText(str(maxi))
        self.framerate_spinbox.setRange(mini, maxi)

    def update_pixel_clock(self):
        pixel_clock = self.cam.get_pixel_clock()
        self.value_pixelclock_qlabel.setText(str(pixel_clock))

    def acquisition_set_enable(self, state):
        """Function that change the acquisition_button state"""

        self.framerate_spinbox.setEnabled(state)
        self.exposure_spinbox.setEnabled(state)
        self.gray_radio.setEnabled(state)
        self.rgb_radio.setEnabled(state)
        self.aoi_button.setEnabled(state)
        self.state_acquisition_button = state
        self.take_screenshot_button.setEnabled(state)
        if state:
            self.acquisition_button.setText(STR_STOP_VIDEO)
            self.acquisition_button.setIcon(self.stop_icon)
            self.get_video_thread.start()
        else:
            self.acquisition_button.setText(STR_START_VIDEO)
            self.acquisition_button.setIcon(self.start_icon)
            self.get_video_thread.stop()

    def camera_setting_layout(self):
        """Return de constructed layout for the camera setting interface"""
        framerate_h_layout = Qtw.QHBoxLayout()
        framerate_h_layout.addWidget(self.framerate_spinbox)
        framerate_h_layout.addWidget(Qtw.QLabel("max"))
        framerate_h_layout.addWidget(self.max_value_framerate_qlabel)
        framerate_h_layout.addWidget(Qtw.QLabel("min"))
        framerate_h_layout.addWidget(self.min_value_framerate_qlabel)

        exposure_h_layout = Qtw.QHBoxLayout()
        exposure_h_layout.addWidget(self.exposure_spinbox)
        exposure_h_layout.addWidget(Qtw.QLabel(STR_MAX))
        exposure_h_layout.addWidget(self.max_value_exposure_qlabel)
        exposure_h_layout.addWidget(Qtw.QLabel(STR_MIN))
        exposure_h_layout.addWidget(self.min_value_exposure_qlabel)

        camera_setting_formlayout = Qtw.QFormLayout()
        camera_setting_formlayout.addRow(self.pixelclock_qlabel, self.value_pixelclock_qlabel)
        camera_setting_formlayout.addRow(self.framerate_qlabel, framerate_h_layout)
        camera_setting_formlayout.addRow(self.exposure_qlabel, exposure_h_layout)

        right_v_layout = Qtw.QVBoxLayout()
        right_v_layout.addWidget(self.aoi_button)
        right_v_layout.addWidget(self.gray_radio)
        right_v_layout.addWidget(self.rgb_radio)

        # horizontal layout which will go in cell (0,0) of main_h_layout (camera setting)
        final_h_layout = Qtw.QHBoxLayout()
        final_h_layout.addLayout(camera_setting_formlayout)
        final_h_layout.addWidget(v_line())
        final_h_layout.addLayout(right_v_layout)
        final_h_layout.addStretch(1)

        return final_h_layout

    def screenshot_buttons_layout(self):
        """Return de constructed layout for the screenshot buttons"""
        h_layout = Qtw.QGridLayout()
        h_layout.addWidget(self.take_screenshot_button, 0, 0, 1, 2)
        h_layout.addWidget(self.save_screenshot_button, 1, 0)
        h_layout.addWidget(self.clipboard_screenshot_button, 1, 1)

        return h_layout

    def resizeEvent(self, event):
        """Overriding the resizeEvent methode for resize the Qlabels containing the live video and the screenshot
        each time the main window is resized """
        # print("Window has been resized")

        # Resizing the QLabel containing the video pixmap (video_qlabel)
        cv_img = self.displayed_cv_img
        if cv_img.size != 0 and not self.state_acquisition_button:
            # Check if a pixmap is shown and if the video is not live because if it's the case, the resizing event is
            # handle in update_video_qlabel
            qt_img = convert_cv_to_qpixmap(cv_img, self.video_qlabel.size())
            self.displayed_qt_img = qt_img
            self.video_qlabel.setPixmap(qt_img)

        # Resizing the QLabel containing the screenshot pixmap (screenshot_qlabel)
        cv_img = self.displayed_cv_screenshot
        if cv_img.size != 0:  # Check if a pixmap is shown
            qt_img = convert_cv_to_qpixmap(cv_img, self.screenshot_qlabel.size())
            self.displayed_qt_screenshot = qt_img
            self.screenshot_qlabel.setPixmap(qt_img)

        Qtw.QWidget.resizeEvent(self, event)  # Calling the basic resizeEvent of QWidget


class LightSettingAndCamInfo(Qtw.QTabWidget):
    def __init__(self, ser):
        super().__init__()

        self.ser = ser

        self.setSizePolicy(Qtw.QSizePolicy.Fixed, Qtw.QSizePolicy.Fixed)

        # All QObject for the lighting setting
        self.connect_btn = Qtw.QPushButton(STR_CONNECT)
        self.connect_btn.clicked.connect(self.connection)
        self.belt_on_off = Qtw.QCheckBox(STR_CONVEYOR)
        self.belt_on_off.stateChanged.connect(self.belt)
        self.belt_direction_btn = Qtw.QPushButton(STR_DIRECTION)
        self.belt_direction_btn.clicked.connect(self.belt_direction)
        self.belt_speed_slider = Qtw.QSlider(Qtc.Qt.Horizontal)
        self.belt_speed_slider.setMinimum(0)
        self.belt_speed_slider.setMaximum(50)
        self.belt_speed_slider.sliderReleased.connect(self.belt_speed)

        self.led_bar_1_on_off = Qtw.QCheckBox(STR_LED_BAR + ' 1')
        self.led_bar_1_on_off.stateChanged.connect(self.led_bar_1)

        self.led_bar_2_on_off = Qtw.QCheckBox(STR_LED_BAR + ' 2')
        self.led_bar_2_on_off.stateChanged.connect(self.led_bar_2)

        self.dome_light_on_off = Qtw.QCheckBox(STR_DOME_LIGHT)
        self.dome_light_on_off.stateChanged.connect(self.dome_light)

        self.dark_field_ring_on_off = Qtw.QCheckBox(STR_DF_RING)
        self.dark_field_ring_on_off.stateChanged.connect(self.dark_field_ring)

        self.red_ring_on_off = Qtw.QCheckBox(STR_RED)
        self.red_ring_on_off.stateChanged.connect(self.red_ring)

        self.green_ring_on_off = Qtw.QCheckBox(STR_GREEN)
        self.green_ring_on_off.stateChanged.connect(self.green_ring)

        self.uv_on_off = Qtw.QCheckBox(STR_UV)
        self.uv_on_off.stateChanged.connect(self.uv)

        self.blue_ring_on_off = Qtw.QCheckBox(STR_BLUE)
        self.blue_ring_on_off.stateChanged.connect(self.blue_ring)

        self.arm_expand_retract_btn = Qtw.QPushButton(STR_EXPAND)
        self.arm_expand_retract_btn.clicked.connect(self.arm_expand_retract)
        self.arm_state = 0

        self.arm_height_slider = Qtw.QSlider(Qtc.Qt.Vertical)
        self.arm_height_slider.setMinimum(60)
        self.arm_height_slider.setMaximum(100)
        self.arm_height_slider.setValue(100)
        self.arm_height_slider.sliderReleased.connect(self.arm_height)

        # A QObjet for camera info
        self.cam_id_qlabel = Qtw.QLabel()
        self.cam_name_qlabel = Qtw.QLabel()
        self.cam_ser_no_qlabel = Qtw.QLabel()
        self.cam_sensor_width_qlabel = Qtw.QLabel()
        self.cam_sensor_height_qlabel = Qtw.QLabel()
        self.cam_pixel_size_qlabel = Qtw.QLabel()
        self.cam_aoi_width = Qtw.QLabel()
        self.cam_aoi_height = Qtw.QLabel()

        light_setting_widget = Qtw.QWidget()
        light_setting_widget.setLayout(self.light_setting_layout())
        self.addTab(light_setting_widget, STR_LIGHT_SETTING)

        cam_info_widget = Qtw.QWidget()
        cam_info_widget.setLayout(self.cam_info_layout())
        self.addTab(cam_info_widget, STR_CAM_INFO)

        self.ask_serial_connect = SerialConnect()
        self.serial_open = False

        self.enable_btns(False)

        self.warning_connection_failed = WarningWidget(STR_CONNECTION_FAILED, cancel=False)
        self.warning_no_port_available = WarningWidget(STR_NO_PORT_AVAILABLE, cancel=False)


    def light_setting_layout(self):
        """Return de constructed layout for the light setting interface"""

        top_layout = Qtw.QHBoxLayout()
        top_layout.addWidget(self.connect_btn)
        top_layout.addWidget(v_line())
        top_layout.addWidget(self.belt_on_off)
        top_layout.addWidget(v_line())
        top_layout.addWidget(self.belt_direction_btn)
        top_layout.addWidget(v_line())
        top_layout.addWidget(Qtw.QLabel(STR_SPEED))
        top_layout.addWidget(self.belt_speed_slider)

        light_layout = Qtw.QGridLayout()
        light_layout.addWidget(self.led_bar_1_on_off, 0, 0)
        light_layout.addWidget(self.led_bar_2_on_off, 1, 0)
        light_layout.addWidget(self.dome_light_on_off, 0, 1)
        light_layout.addWidget(self.uv_on_off, 1, 1)
        light_layout.addWidget(v_line(), 0, 2, 2, 1)
        light_layout.addWidget(Qtw.QLabel(STR_RGB_RING), 0, 3, 1, 3)
        light_layout.addWidget(self.red_ring_on_off, 1, 3)
        light_layout.addWidget(self.green_ring_on_off, 1, 4)
        light_layout.addWidget(self.blue_ring_on_off, 1, 5)

        right_layout = Qtw.QGridLayout()
        right_layout.addWidget(self.arm_expand_retract_btn, 0, 0)
        right_layout.addWidget(self.dark_field_ring_on_off, 1, 0)
        right_layout.addWidget(v_line(), 0, 1, 3, 1)
        right_layout.addWidget(Qtw.QLabel(STR_ARM_HEIGHT), 0, 2)
        right_layout.addWidget(self.arm_height_slider, 1, 2, 1, 3)

        final_layout = Qtw.QGridLayout()
        final_layout.addLayout(top_layout, 0, 0)
        final_layout.addWidget(h_line(), 1, 0)
        final_layout.addLayout(light_layout, 2, 0)
        final_layout.addWidget(v_line(), 0, 1, 3, 1)
        final_layout.addLayout(right_layout, 0, 2, 3, 1)

        return final_layout

    def cam_info_layout(self):
        layout = Qtw.QHBoxLayout()

        left_form_layout = Qtw.QFormLayout()
        left_form_layout.addRow(Qtw.QLabel(STR_NAME), self.cam_name_qlabel)
        left_form_layout.addRow(Qtw.QLabel(STR_ID), self.cam_id_qlabel)
        left_form_layout.addRow(Qtw.QLabel(STR_SER_NO_BIS), self.cam_ser_no_qlabel)
        left_form_layout.addRow(Qtw.QLabel(STR_PIXEL_SIZE), self.cam_pixel_size_qlabel)

        right_form_layout = Qtw.QFormLayout()
        right_form_layout.addRow(Qtw.QLabel(STR_SENSOR_WIDTH), self.cam_sensor_width_qlabel)
        right_form_layout.addRow(Qtw.QLabel(STR_SENSOR_HEIGHT), self.cam_sensor_height_qlabel)
        right_form_layout.addRow(Qtw.QLabel(STR_AOI_WIDTH), self.cam_aoi_width)
        right_form_layout.addRow(Qtw.QLabel(STR_AOI_HEIGHT), self.cam_aoi_height)

        layout.addLayout(left_form_layout)
        layout.addLayout(right_form_layout)

        return layout

    def update_cam_info(self, cam_info, sensor_info, aoi):

        self.cam_ser_no_qlabel.setText(str(cam_info[0]))
        self.cam_id_qlabel.setText(str(cam_info[1]))
        self.cam_sensor_width_qlabel.setText(str(sensor_info[0].value))
        self.cam_sensor_height_qlabel.setText(str(sensor_info[1].value))
        self.cam_name_qlabel.setText(str(sensor_info[2]))
        self.cam_pixel_size_qlabel.setText(str(sensor_info[3]/100.0))
        self.cam_aoi_width.setText(str(aoi[2]))
        self.cam_aoi_height.setText(str(aoi[3]))

    def update_aoi(self, aoi):
        self.cam_aoi_width.setText(str(aoi[2]))
        self.cam_aoi_height.setText(str(aoi[3]))

    @Qtc.pyqtSlot()
    def connection(self):
        if not self.serial_open:  # If no serial connection is already open, we open one
            ports = serial.tools.list_ports.comports()
            nb_ports = len(ports)

            if nb_ports == 1:  # If the only serial port is available, it is opened
                i = 0
            elif nb_ports > 1:  # if more than one serial port is available, the user is asked which one he want to open
                self.ask_serial_connect.show_ports(ports)
                i = self.ask_serial_connect.exec()
            else:   # Else, no port available
                i = -1

            if i >= 0:  # If a serial port have been chosen
                self.ser.port = ports[i][0]
                self.ser.open()

                if self.ser.is_open:
                    self.connect_btn.setText('Disconnect')
                    self.serial_open = True
                    self.enable_btns(True)
                    self.reset_btns()
                    self.ser.write(chr(112).encode('utf-8'))
                    self.open_serial_ticker()
                else:
                    self.serial_open = False
                    self.enable_btns(False)
                    self.reset_btns()
                    self.warning_connection_failed.show()
                    self.warning_connection_failed.exec()
            else:
                self.warning_no_port_available.show()
                self.warning_no_port_available.exec()
                self.serial_open = False
                self.enable_btns(False)
                self.reset_btns()

        else:  # Else, the existing serial port is closed
            self.serial_open = False
            self.enable_btns(False)
            self.reset_btns()
            self.ser.write(chr(113).encode('utf-8'))
            self.ser.close()
            self.connect_btn.setText('Connect')

    def enable_btns(self, enable):
        self.belt_on_off.setEnabled(enable)
        self.belt_direction_btn.setEnabled(enable)
        self.belt_speed_slider.setEnabled(enable)
        self.led_bar_1_on_off.setEnabled(enable)
        self.led_bar_2_on_off.setEnabled(enable)
        self.dome_light_on_off.setEnabled(enable)
        self.dark_field_ring_on_off.setEnabled(enable)
        self.red_ring_on_off.setEnabled(enable)
        self.green_ring_on_off.setEnabled(enable)
        self.blue_ring_on_off.setEnabled(enable)
        self.uv_on_off.setEnabled(enable)
        self.arm_expand_retract_btn.setEnabled(enable)
        self.arm_height_slider.setEnabled(enable)

    def reset_btns(self):
        self.belt_on_off.setCheckState(False)
        #self.belt_direction_btn.setCheckState(False)
        #self.belt_speed_slider.setCheckState(False)
        self.led_bar_1_on_off.setCheckState(False)
        self.led_bar_2_on_off.setCheckState(False)
        self.dome_light_on_off.setCheckState(False)
        self.dark_field_ring_on_off.setCheckState(False)
        self.red_ring_on_off.setCheckState(False)
        self.green_ring_on_off.setCheckState(False)
        self.blue_ring_on_off.setCheckState(False)

    @Qtc.pyqtSlot()
    def led_bar_1(self):

        if self.ser.is_open and self.serial_open:
            self.ser.write(chr(108).encode('utf-8'))

    @Qtc.pyqtSlot()
    def led_bar_2(self):
        if self.ser.is_open and self.serial_open:
            self.ser.write(chr(109).encode('utf-8'))

    @Qtc.pyqtSlot()
    def dome_light(self):
        if self.ser.is_open and self.serial_open:
            self.ser.write(chr(106).encode('utf-8'))

    @Qtc.pyqtSlot()
    def dark_field_ring(self):
        if self.ser.is_open and self.serial_open:
            self.ser.write(chr(107).encode('utf-8'))

    @Qtc.pyqtSlot()
    def red_ring(self):
        if self.ser.is_open and self.serial_open:
            self.ser.write(chr(103).encode('utf-8'))

    @Qtc.pyqtSlot()
    def green_ring(self):
        if self.ser.is_open and self.serial_open:
            self.ser.write(chr(104).encode('utf-8'))

    @Qtc.pyqtSlot()
    def blue_ring(self):
        if self.ser.is_open and self.serial_open:
            self.ser.write(chr(105).encode('utf-8'))

    @Qtc.pyqtSlot()
    def uv(self):
        if self.ser.is_open and self.serial_open:
            # self.ser.write(chr(?????).encode('utf-8'))
            pass

    @Qtc.pyqtSlot()
    def belt(self):
        if self.ser.is_open and self.serial_open:
            self.ser.write(chr(111).encode('utf-8'))

    @Qtc.pyqtSlot()
    def belt_direction(self):
        if self.ser.is_open and self.serial_open:
            self.ser.write(chr(110).encode('utf-8'))

    @Qtc.pyqtSlot()
    def belt_speed(self):
        if self.ser.is_open and self.serial_open:
            value = self.belt_speed_slider.value()
            self.ser.write(chr(value).encode('utf-8'))
            #print(value)

    @Qtc.pyqtSlot()
    def arm_height(self):
        if self.ser.is_open and self.serial_open:
            value = self.arm_height_slider.value()
            self.ser.write(chr(value).encode('utf-8'))
            print(value)

    @Qtc.pyqtSlot()
    def arm_expand_retract(self):
        if self.ser.is_open and self.serial_open:

            if self.arm_state:
                self.arm_state = 0
                self.arm_expand_retract_btn.setText(STR_EXPAND)
                self.arm_height_slider.setEnabled(False)
                self.arm_height_slider.setValue(100)
                self.dark_field_ring_on_off.setEnabled(False)

            else:
                self.arm_state = 1
                self.arm_expand_retract_btn.setText(STR_RETRACT)
                self.arm_height_slider.setEnabled(True)
                self.dark_field_ring_on_off.setEnabled(True)

            self.ser.write(chr(117).encode('utf-8'))

    def open_serial_ticker(self):
        if self.serial_open and self.ser.is_open:
            self.ser.write(chr(114).encode('utf-8'))
            threading.Timer(1, self.open_serial_ticker).start()

        else:
            self.serial_open = False
            self.connect_btn.setText('Connect')


class SerialConnect(Qtw.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(STR_SERIAL_CONNECTION)

        self.port_list = Qtw.QComboBox()

        connect_btn = Qtw.QPushButton(STR_CONNECT)
        connect_btn.clicked.connect(self.connect)
        cancel_btn = Qtw.QPushButton(STR_CANCEL)
        cancel_btn.clicked.connect(self.cancel)

        layout = Qtw.QGridLayout()
        layout.addWidget(Qtw.QLabel(STR_SELECT_PORT_LIST), 0, 0, 1, 2)
        layout.addWidget(self.port_list, 1, 0, 1, 2)
        layout.addWidget(connect_btn, 2, 0)
        layout.addWidget(cancel_btn, 2,1)

        self.setLayout(layout)

    def show_ports(self, ports):
        self.port_list.clear()

        nb_port = len(ports)

        self.port_list.addItem(STR_PORTS_AVAILABLE + str(nb_port))

        for port in ports:
            self.port_list.addItem(port[0])

    @Qtc.pyqtSlot()
    def connect(self):
        self.done(self.port_list.currentIndex()-1)

    @Qtc.pyqtSlot()
    def cancel(self):
        self.done(-1)













