# PIMS Vision Industrielle 2020/2021
# Samuel GERENTE, Victoire DE SALEON-TERRAS, Flora SILBERZAN, Martin COLLIGNON, Hugo LASSIETTE, Oscar BOUCHER
# Under the supervision of Thierry AVIGNON and Julien VILLEMEJANE
#
# Institut d'Optique Graduate School (https://www.institutoptique.fr/)
# LEnsE (http://lense.institutoptique.fr/)
#
# This application allows you to (non-exhaustive list):
#   - Connect to a uEye camera (through USB)
#   - Set the main parameters of the camera (frame rate, exposure time, colormode, AOI)
#   - Show the video from the camera
#   - Take screen shoot from the camera and save it into a file or into the clipboard
#   - Apply a lot of image processing functions
#   - Control the lights by connecting to the external interface (serial)
#
# This application was developed on Python 3.9.8 (require version >= 3.7 and <=3.11, use command "python --version" to
# check your version). The following items need to be installed on the computer:
#   - the driver of the uEye camera. The easier way to install them is to install the software suite
#   IDS Software Studio, see https://fr.ids-imaging.com/ (free account needed for download). It contains the software
#   uEyeCockpit which allow you to check if the camera is recognized;
#   - the PyQt5 library, can be installed with the command: pip install pyqt5 (https://pypi.org/project/PyQt5/)
#   - the Numpy library, can be installed with the command: pip install numpy (https://pypi.org/project/numpy/)
#   - the OpenCV library, can be installed with the command: pip install opencv-python
#   (https://pypi.org/project/opencv-python/)
#   - the PyuEye library, can be installed with the command: pip install pyueye (https://pypi.org/project/pyueye/)
#   - the PySerial library, can be installed with the command: pip install pyserial (https://pypi.org/project/pyserial/)
#
# Please refer to the documentation of more information (in creation...)


import sys
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc
from math import floor
import numpy as np
import cv2
import resources
import ctypes
from pyueye import ueye
from camera import uEyeCamera, get_cam_list
from AcquisitionTab import AcquisitionTab
from SimpleProcessingInPicutureTab import SimpleProcessingInPictureTab
from SimpleProcessingInVideoTab import SimpleProcessingInVideoTab
from FormDetectionInPictureTab import FormDetectionInPictureTab
from FormDetectionInVideoTab import FormDetectionInVideoTab
from MeasurementInVideoTab import MeasurementInVideoTab
from ColorDetectionInVideoTab import ColorDetectionInVideoTab
from AutoDarkRingTab import AutoDarkRingTab
from Utils import GetVideoThread
import serial

from Dictionary_EN import *


class MainApp(Qtw.QApplication):
    """The main application object"""

    def __init__(self, argv):
        super().__init__(argv)

        # Setting the icon of the application (top-left corner and taskbar)
        app_icon = Qtg.QIcon(":/screenshot_icon.png")
        self.setWindowIcon(app_icon)

        self.choose_camera_window = ChooseCameraWindow()
        self.choose_camera_window.camera_is_selected.connect(self.launch_app)
        self.choose_camera_window.show()

        self.main_window = None


    @Qtc.pyqtSlot(int)
    def launch_app(self, cam_id):
        self.choose_camera_window.close()
        self.main_window = MainWindow(cam_id)
        self.main_window.show()


class ChooseCameraWindow(Qtw.QWidget):
    """
    QWidget use when the app is launcher to ask for the camera to use
    """

    camera_is_selected = Qtc.pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.selected_cam = None

        # QLabel for displaying instruction
        top_text_qlabel = Qtw.QLabel()
        top_text_qlabel.setText(STR_SELECT_CAMERA_AND_CLICK)

        # QComboBox (drop-down list) which contain the cameras available
        self.camera_combo_box = Qtw.QComboBox()
        self.camera_combo_box.addItem(STR_SELECT_CAMERA)

        self.cam_list = get_cam_list()
        for c in self.cam_list:
            item = STR_ID + str(c[0]) + STR_SER_NO + c[1] + STR_MODEL + c[2]
            self.camera_combo_box.addItem(item)

        # QPushButton for validating the choice of camera
        select_button = Qtw.QPushButton(STR_SELECT)
        select_button.clicked.connect(self.select_camera)

        # Creation of the layout containing the above widgets
        layout = Qtw.QVBoxLayout()
        layout.addWidget(top_text_qlabel)
        layout.addWidget(self.camera_combo_box)
        layout.addWidget(select_button)
        self.setLayout(layout)

        self.setWindowTitle(STR_PIMS)

    @Qtc.pyqtSlot()
    def select_camera(self):
        index = self.camera_combo_box.currentIndex()-1
        if index >= 0:
            self.camera_is_selected.emit(self.cam_list[index][0])


class MainWindow(Qtw.QMainWindow):
    """The main application window"""

    def __init__(self, cam_id):
        super().__init__()
        self.cam = uEyeCamera(cam_id)
        self.cam.set_display_mode(ueye.IS_SET_DM_DIB)
        self.video_thread = GetVideoThread(self.cam)

        self.ser = serial.Serial()
        self.ser.baudrate = 115200

        # Setting the minimum size of the main window
        self.setMinimumSize(1280, 720)
        self.showMaximized()

        # Setting the title of MainWindow
        self.setWindowTitle(STR_PIMS)

        self.main_tab_widget = MainTabWindow(self.cam, self.video_thread, self.ser)
        self.setCentralWidget(self.main_tab_widget)

        form_detection_in_picture_action = Qtw.QAction("Shape detection in picture", self)
        form_detection_in_picture_action.triggered.connect(self.add_form_detection_in_picture_tab)

        form_detection_in_video_action = Qtw.QAction("Shape detection in video", self)
        form_detection_in_video_action.triggered.connect(self.add_form_detection_in_video_tab)

        measurement_in_video_action = Qtw.QAction(STR_MEASUREMENT_IN_VIDEO, self)
        measurement_in_video_action.triggered.connect(self.add_measurement_in_video_tab)

        simple_processing_in_picture_action = Qtw.QAction(STR_SIMPLE_PROCESSING_IN_PICTURE, self)
        simple_processing_in_picture_action.triggered.connect(self.add_simple_processing_in_picture_tab)

        simple_processing_in_video_action = Qtw.QAction(STR_SIMPLE_PROCESSING_ON_VIDEO, self)
        simple_processing_in_video_action.triggered.connect(self.add_simple_processing_in_video_tab)

        color_detection_in_video_action = Qtw.QAction(STR_COLOR_DETECTION_IN_VIDEO, self)
        color_detection_in_video_action.triggered.connect(self.add_color_detection_in_video)

        auto_dark_ring_action = Qtw.QAction(STR_AUTO_DARK_RING, self)
        auto_dark_ring_action.triggered.connect(self.add_auto_dark_ring)

        menu = self.menuBar()

        add_processing_menu = menu.addMenu("&Add processing")
        add_processing_menu.addAction(simple_processing_in_picture_action)
        add_processing_menu.addAction(simple_processing_in_video_action)
        add_processing_menu.addAction(form_detection_in_picture_action)
        add_processing_menu.addAction(form_detection_in_video_action)
        add_processing_menu.addAction(measurement_in_video_action)
        add_processing_menu.addAction(auto_dark_ring_action)
        #add_processing_menu.addAction(color_detection_in_video_action)


    @Qtc.pyqtSlot()
    def add_simple_processing_in_video_tab(self):
        self.main_tab_widget.addTab(SimpleProcessingInVideoTab(self.video_thread), STR_SIMPLE_PROCESSING_ON_VIDEO)

    @Qtc.pyqtSlot()
    def add_simple_processing_in_picture_tab(self):
        simple_processing_tab = SimpleProcessingInPictureTab()
        simple_processing_tab.request_screenshot_signal.connect(self.main_tab_widget.acquisition_tab.send_screenshot)
        self.main_tab_widget.acquisition_tab.send_screenshot_signal.connect(simple_processing_tab.receive_screenshot)
        self.main_tab_widget.addTab(simple_processing_tab, STR_SIMPLE_PROCESSING_IN_PICTURE)

    @Qtc.pyqtSlot()
    def add_form_detection_in_picture_tab(self):
        self.main_tab_widget.addTab(FormDetectionInPictureTab(), STR_FORM_DETECTION)

    @Qtc.pyqtSlot()
    def add_form_detection_in_video_tab(self):
        self.main_tab_widget.addTab(FormDetectionInVideoTab(self.video_thread), 'Shape detection in video')

    @Qtc.pyqtSlot()
    def add_measurement_in_video_tab(self):
        self.main_tab_widget.addTab(MeasurementInVideoTab(self.video_thread), STR_MEASUREMENT_IN_VIDEO)

    @Qtc.pyqtSlot()
    def add_color_detection_in_video(self):
        self.main_tab_widget.addTab(ColorDetectionInVideoTab(self.video_thread), STR_COLOR_DETECTION_IN_VIDEO)

    @Qtc.pyqtSlot()
    def add_auto_dark_ring(self):
        self.main_tab_widget.addTab(AutoDarkRingTab(self.video_thread, self.ser), STR_AUTO_DARK_RING)


class MainTabWindow(Qtw.QTabWidget):
    def __init__(self, cam, video_thread, ser):
        super().__init__()

        # Initializing tabs
        self.acquisition_tab = AcquisitionTab(cam, video_thread, ser)

        # Adding the two tabs to the TabWidget
        self.addTab(self.acquisition_tab, STR_ACQUISITION)

        self.setTabsClosable(True)
        self.tabBar().tabButton(0, Qtw.QTabBar.RightSide).deleteLater()
        self.tabBar().setTabButton(0, Qtw.QTabBar.RightSide, None)
        self.tabBar().tabCloseRequested.connect(self.delete_tab)



    @Qtc.pyqtSlot(int)
    def delete_tab(self, index):
        tab = self.widget(index)
        self.removeTab(index)
        tab.deleteLater()


if __name__ == '__main__':

    # Those two lines are doing complicated things in order to tell Windows to set the right taskbar icon (need to
    # import ctypes)
    # See: https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7
    my_app_id = u'mycompany.myproduct.subproduct.version'  # arbitrary string
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    app = MainApp(sys.argv)
    sys.exit(app.exec())
