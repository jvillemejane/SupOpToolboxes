
import numpy as np
import os
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtCore as Qtc
from PyQt5 import Qt as Qt
from PyQt5 import QtGui as Qtg
import cv2
import time

from Utils import convert_cv_to_qpixmap, Timer, h_line, QLabelLin, midpoint, distance, is_gray
from PreProcessingFunction import func_contours_list, gray_to_binary
from FormDetectionFunction import is_outside

from Dictionary_EN import *


class MeasurementInVideoTab(Qtw.QMainWindow):
    def __init__(self, video_thread):
        super().__init__()

        self.shown_cv_img = None
        self.calculating = False
        self.distance_pix = None
        self.scale = 1

        self.get_video_thread = video_thread
        self.get_video_thread.new_cv_img_signal.connect(self.update_video_qlabel)
        self.get_video_thread.stopped_signal.connect(self.video_stopped)

        self.video_qlabel = QLabelLin()
        self.video_qlabel.setText(STR_PLS_LAUNCH_ACQUISITION)
        self.setCentralWidget(self.video_qlabel)

        self.setting_dock = Qtw.QDockWidget('Setting', self)
        setting_widget = Qtw.QWidget()

        self.calculate_btn = Qtw.QPushButton(STR_START_CALCULATION)
        self.calculate_btn.clicked.connect(self.start_calculation)
        self.calculate_btn.setEnabled(False)

        self.fps_qlabel = Qtw.QLabel()

        self.nb_pixels_qlabel = Qtw.QLabel()
        self.scale_qlabel = Qtw.QLabel()

        self.distance_spinbox = Qtw.QSpinBox()
        self.distance_spinbox.setRange(1, 1000000)
        self.distance_spinbox.setSingleStep(100)
        self.distance_spinbox.setValue(10000)
        self.distance_spinbox.valueChanged.connect(self.update_scale)

        self.set_scale_btn = Qtw.QPushButton(STR_NEW_SCALE)
        self.set_scale_btn.clicked.connect(self.set_scale)
        self.set_scale_btn.setEnabled(False)

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

        self.screenshot_btn = Qtw.QPushButton(STR_TAKE_SCREENSHOT)
        self.screenshot_btn.clicked.connect(self.save_screenshot)
        self.screenshot_btn.setEnabled(False)
        self.clipboard_btn = Qtw.QPushButton(STR_COPY_TO_CLIPBOARD)
        self.clipboard_btn.clicked.connect(self.clipboard_screenshot)
        self.clipboard_btn.setEnabled(False)

        setting_form_layout = Qtw.QFormLayout()
        setting_form_layout.addRow(self.calculate_btn)
        setting_form_layout.addRow(h_line())
        setting_form_layout.addRow(STR_FPS, self.fps_qlabel)
        setting_form_layout.addRow(h_line())
        setting_form_layout.addRow(self.set_scale_btn)
        setting_form_layout.addRow(STR_NB_PIXELS, self.nb_pixels_qlabel)
        setting_form_layout.addRow(STR_DISTANCE, self.distance_spinbox)
        setting_form_layout.addRow(STR_SCALE, self.scale_qlabel)
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

    @Qtc.pyqtSlot(int)
    def update_scale(self, value):
        if self.distance_pix is not None:
            self.scale = value / (self.distance_pix * 1000)  # mm/pix
            self.scale_qlabel.setText("{:.3f}".format(self.scale))

    @Qtc.pyqtSlot()
    def set_scale(self):
        self.video_qlabel.mouse_released_signal.connect(self.new_scale)
        self.video_qlabel.setting_scale = True

    @Qtc.pyqtSlot(Qtc.QPoint, Qtc.QPoint)
    def new_scale(self, qpos0, qpos1):
        y_qt = self.video_qlabel.pixmap().height()
        y_cv = self.shown_cv_img.shape[0]

        self.distance_pix = distance((qpos0.x(), qpos0.y()), (qpos1.x(), qpos1.y())) * y_cv/y_qt
        self.nb_pixels_qlabel.setText("{:.3f}".format(self.distance_pix))

        self.update_scale(self.distance_spinbox.value())

        self.video_qlabel.mouse_released_signal.disconnect(self.new_scale)
        self.video_qlabel.setting_scale = False

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
            self.set_scale_btn.setEnabled(True)
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

                for cnt in good_contours_list:
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(contours_img, [box], 0, (0, 0, 255), 2)

                    (tl, tr, br, bl) = box  # tl = top left, tr = top right, br = bottom right, bl = bottom left
                    (tl_tr_X, tl_tr_Y) = midpoint(tl, tr)
                    (bl_br_X, bl_br_Y) = midpoint(bl, br)

                    (tl_bl_X, tl_bl_Y) = midpoint(tl, bl)
                    (tr_br_X, tr_br_Y) = midpoint(tr, br)

                    cv2.circle(contours_img, (int(tl_tr_X), int(tl_tr_Y)), 5, (255, 0, 0), -1)
                    cv2.circle(contours_img, (int(bl_br_X), int(bl_br_Y)), 5, (255, 0, 0), -1)
                    cv2.circle(contours_img, (int(tl_bl_X), int(tl_bl_Y)), 5, (255, 0, 0), -1)
                    cv2.circle(contours_img, (int(tr_br_X), int(tr_br_Y)), 5, (255, 0, 0), -1)

                    cv2.line(contours_img, (int(tl_tr_X), int(tl_tr_Y)), (int(bl_br_X), int(bl_br_Y)), (255, 0, 255), 2)
                    cv2.line(contours_img, (int(tl_bl_X), int(tl_bl_Y)), (int(tr_br_X), int(tr_br_Y)), (255, 0, 255), 2)

                    dA = distance((tl_tr_X, tl_tr_Y), (bl_br_X, bl_br_Y))
                    dB = distance((tl_bl_X, tl_bl_Y), (tr_br_X, tr_br_Y))

                    if self.distance_pix is None:
                        unit = 'pix'
                    else:
                        unit = 'mm'
                    cv2.putText(contours_img, "{:.1f}".format(dA*self.scale)+unit,
                                (int(tl_tr_X - 15), int(tl_tr_Y - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, (0, 0, 255), 2)
                    cv2.putText(contours_img, "{:.1f}".format(dB*self.scale)+unit,
                                (int(tr_br_X + 10), int(tr_br_Y)), cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, (0, 0, 255), 2)

                self.shown_cv_img = contours_img

            else:
                self.shown_cv_img = cv_img

            qt_img = convert_cv_to_qpixmap(self.shown_cv_img, self.video_qlabel.size())
            self.video_qlabel.setPixmap(qt_img)
        else:
            self.calculating = False
            self.calculate_btn.setEnabled(False)
            self.calculate_btn.setText(STR_START_CALCULATION)
            self.set_scale_btn.setEnabled(False)
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




