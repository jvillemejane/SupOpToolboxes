
import numpy as np
import os
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtCore as Qtc
from PyQt5 import Qt as Qt
from PyQt5 import QtGui as Qtg
import cv2
import time


from Utils import convert_cv_to_qpixmap, Timer, h_line, is_gray
from PreProcessingFunction import func_closing, func_opening, func_simple_thresholding, func_otsu_thresholding, \
    func_contours_list, func_gaus_blurring, gray_to_binary
from FormDetectionFunction import identify_shapes, SHAPES_NAME_LIST, get_img_shape_list, is_outside

from Dictionary_EN import *


class FormDetectionInVideoTab(Qtw.QMainWindow):
    def __init__(self, video_thread):
        super().__init__()

        self.raw_cv_img = None
        self.shown_cv_img = None
        self.calculating = False
        self.directory = os.path.join(os.getcwd(), 'test_shapes')

        self.get_video_thread = video_thread
        self.get_video_thread.new_cv_img_signal.connect(self.update_video_qlabel)
        self.get_video_thread.stopped_signal.connect(self.video_stopped)

        self.video_qlabel = Qtw.QLabel()
        self.setCentralWidget(self.video_qlabel)

        self.setting_dock = Qtw.QDockWidget('Setting', self)
        setting_widget = Qtw.QWidget()

        self.calculate_btn = Qtw.QPushButton(STR_START_CALCULATION)
        self.calculate_btn.clicked.connect(self.start_calculation)
        self.calculate_btn.setEnabled(False)

        self.fps_qlabel = Qtw.QLabel()

        self.show_binary_checkbox = Qtw.QCheckBox(STR_SHOW_BINARY_IMAGE)
        self.show_binary_checkbox.setChecked(False)

        self.opening_checkbox = Qtw.QCheckBox(STR_OPENING)
        self.opening_checkbox.setChecked(False)

        self.closing_checkbox = Qtw.QCheckBox(STR_CLOSING)
        self.closing_checkbox.setChecked(False)

        self.blur_checkbox = Qtw.QCheckBox(STR_GAUSSIAN_BLURRING)
        self.blur_checkbox.setChecked(False)

        self.threshold_spinbox = Qtw.QSpinBox()
        self.threshold_spinbox.setRange(-1, 255)  # -1 value is for auto threshold selection
        self.threshold_spinbox.setValue(-1)

        self.min_area_spinbox = Qtw.QSpinBox()
        self.min_area_spinbox.setRange(0, 1000000000)
        self.min_area_spinbox.setSingleStep(50)
        self.min_area_spinbox.setValue(1000)

        self.max_area_spinbox = Qtw.QSpinBox()
        self.max_area_spinbox.setRange(0, 1000000000)
        self.max_area_spinbox.setSingleStep(50)
        self.max_area_spinbox.setValue(90000)

        self.directory_qlabel = Qtw.QLabel()
        self.directory_qlabel.setText(self.directory)
        self.change_folder_btn = Qtw.QPushButton('Change directory')
        self.change_folder_btn.clicked.connect(self.change_directory)

        self.screenshot_btn = Qtw.QPushButton(STR_TAKE_SCREENSHOT)
        self.screenshot_btn.clicked.connect(self.save_screenshot)
        self.screenshot_btn.setEnabled(False)
        self.clipboard_btn = Qtw.QPushButton(STR_COPY_TO_CLIPBOARD)
        self.clipboard_btn.clicked.connect(self.clipboard_screenshot)
        self.clipboard_btn.setEnabled(False)

        setting_form_layout = Qtw.QFormLayout()
        setting_form_layout.addRow(self.calculate_btn)
        setting_form_layout.addRow(h_line())
        setting_form_layout.addRow(Qtw.QLabel(STR_FPS), self.fps_qlabel)
        setting_form_layout.addRow(h_line())
        setting_form_layout.addRow('Current directory:', self.directory_qlabel)
        setting_form_layout.addRow(self.directory_qlabel)
        setting_form_layout.addRow(self.change_folder_btn)
        setting_form_layout.addRow(h_line())
        setting_form_layout.addRow(self.show_binary_checkbox)
        setting_form_layout.addRow(self.opening_checkbox)
        setting_form_layout.addRow(self.closing_checkbox)
        setting_form_layout.addRow(self.blur_checkbox)
        setting_form_layout.addRow(STR_THRESHOLD, self.threshold_spinbox)
        setting_form_layout.addRow(STR_MIN_SURFACE, self.min_area_spinbox)
        setting_form_layout.addRow(STR_MAX_SURFACE, self.max_area_spinbox)
        setting_form_layout.addRow(h_line())
        setting_form_layout.addRow(self.screenshot_btn, self.clipboard_btn)

        setting_widget.setLayout(setting_form_layout)

        self.setting_dock.setWidget(setting_widget)

        self.addDockWidget(Qtc.Qt.LeftDockWidgetArea, self.setting_dock)

        self.timer = Timer()
        self.timer.start()

    @Qtc.pyqtSlot()
    def video_stopped(self):
        self.video_qlabel.setText(STR_PLS_LAUNCH_ACQUISITION)
        self.shown_cv_img = None
        self.fps_qlabel.setText('')
        self.calculating = False
        self.calculate_btn.setEnabled(False)
        self.calculate_btn.setText(STR_START_CALCULATION)
        self.screenshot_btn.setEnabled(False)
        self.clipboard_btn.setEnabled(False)

    @Qtc.pyqtSlot()
    def save_screenshot(self):
        """Slot connected to the clicked signal of save_screenshot_button (QPushButton). It open a window for choosing
        a path and a file name """

        filename = Qtw.QFileDialog.getSaveFileName(self, STR_SAVE_IMAGE, '', STR_IMAGE_FORMAT)
        if filename[0] != "":
            cv2.imwrite(filename[0], self.shown_cv_img)

    @Qtc.pyqtSlot()
    def clipboard_screenshot(self):
        Qtw.QApplication.clipboard().setPixmap(convert_cv_to_qpixmap(self.shown_cv_img, None))

    @Qtc.pyqtSlot()
    def change_directory(self):
        self.directory = Qtw.QFileDialog.getExistingDirectory(self, 'Open directory', '',
                                                              Qtw.QFileDialog.ShowDirsOnly |
                                                              Qtw.QFileDialog.DontResolveSymlinks)
        if self.directory != '':
            self.directory_qlabel.setText(self.directory)

    @Qtc.pyqtSlot()
    def start_calculation(self):
        if not self.calculating:
            self.calculate_btn.setText(STR_STOP_CALCULATION)
            self.calculating = True
        else:
            self.calculate_btn.setText(STR_START_CALCULATION)
            self.calculating = False
            self.fps_qlabel.setText('')

    @Qtc.pyqtSlot(np.ndarray)
    def update_video_qlabel(self, cv_img):
        """Slot connected to the new_cv_img_signal signal of GetVideoThread (QRadioBox). Updates the video_qlabel
        with a new opencv image from the camera """
        if is_gray(cv_img):
            self.calculate_btn.setEnabled(True)
            self.screenshot_btn.setEnabled(True)
            self.clipboard_btn.setEnabled(True)

            d_t = self.timer.reset()
            self.fps_qlabel.setText(str(int(1 / d_t)))

            if self.calculating:

                binary_img = gray_to_binary(cv_img, self.threshold_spinbox.value(), self.opening_checkbox.isChecked(),
                                            self.closing_checkbox.isChecked(), self.blur_checkbox.isChecked())

                contours_list = func_contours_list(binary_img, self.min_area_spinbox.value(), self.max_area_spinbox.value())

                if self.show_binary_checkbox.isChecked():
                    contours_img = cv2.merge([binary_img, binary_img, binary_img])
                else:
                    contours_img = cv2.merge([cv_img, cv_img, cv_img])

                good_contours_list = []

                for cnt in contours_list:
                    if not is_outside(cnt, cv_img.shape):
                        good_contours_list.append(cnt)

                nb_shapes = len(good_contours_list)
                img_shapes_list = get_img_shape_list(binary_img, good_contours_list)

                cv2.drawContours(contours_img, good_contours_list, -1, (0, 0, 255), 3)

                detected_shapes_index_list = identify_shapes(img_shapes_list, self.directory)

                for i in range(nb_shapes):
                    cnt = good_contours_list[i]

                    m = cv2.moments(cnt)
                    center_x = int(m["m10"] / m["m00"])
                    center_y = int(m["m01"] / m["m00"])

                    cv2.circle(contours_img, (center_x, center_y), 4, (0, 0, 255), -1)

                    shape_name = SHAPES_NAME_LIST[detected_shapes_index_list[i]]
                    cv2.putText(contours_img, shape_name, (center_x-55, center_y-10), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 0, 0), 2, cv2.LINE_AA)

                self.shown_cv_img = contours_img

            else:
                self.shown_cv_img = cv_img
            qt_img = convert_cv_to_qpixmap(self.shown_cv_img, self.video_qlabel.size())
            self.video_qlabel.setPixmap(qt_img)

        else:
            self.calculating = False
            self.calculate_btn.setEnabled(False)
            self.calculate_btn.setText(STR_START_CALCULATION)
            self.screenshot_btn.setEnabled(False)
            self.clipboard_btn.setEnabled(False)
            self.video_qlabel.setText(STR_COLOR_TO_GRAY)
            self.shown_cv_img = None
            self.fps_qlabel.setText('')


    def resizeEvent(self, event):
        """Overriding the resizeEvent methode for resize the Qlabels containing image each time the main window
         is resized """
        Qtw.QWidget.resizeEvent(self, event)  # Calling the basic resizeEvent of QWidget
        if self.shown_cv_img is not None:
            qt = convert_cv_to_qpixmap(self.shown_cv_img, self.video_qlabel.size())
            self.video_qlabel.setPixmap(qt)





