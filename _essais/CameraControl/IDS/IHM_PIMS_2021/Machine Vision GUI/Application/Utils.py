
from PyQt5 import QtCore as Qtc
from PyQt5 import QtGui as Qtg
from PyQt5 import QtWidgets as Qtw
import numpy as np
from math import sqrt
from pyueye import ueye
import cv2
import time

from Dictionary_EN import *


def v_line():
    """Return a QFrame representing a vertical line"""
    line = Qtw.QFrame()
    line.setFrameShape(Qtw.QFrame.VLine)
    line.setLineWidth(2)
    return line


def h_line():
    """Return a QFrame representing a horizontal line"""
    line = Qtw.QFrame()
    line.setFrameShape(Qtw.QFrame.HLine)
    line.setLineWidth(2)
    return line


def open_img(parent):
    filename = Qtw.QFileDialog.getOpenFileName(parent, STR_OPEN_IMAGE, '', STR_IMAGE_FORMAT)

    if filename[0] != "":
        img = cv2.imread(filename[0], cv2.IMREAD_COLOR)

        if np.array_equal(img[:, :, 2], img[:, :, 1]) \
                and np.array_equal(img[:, :, 2], img[:, :, 1]) \
                and np.array_equal(img[:, :, 2], img[:, :, 1]):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return img
    else:
        return None


def save_img(parent, img):
    filename = Qtw.QFileDialog.getSaveFileName(parent, STR_SAVE_IMAGE, '', STR_IMAGE_FORMAT)
    if filename[0] != "":
        cv2.imwrite(filename[0], img)


def convert_cv_to_qpixmap(cv_img, qsize=None, bgr2rgb=True):
    """Convert from an opencv image to QPixmap of size qsize (given in argument)"""

    shape = cv_img.shape
    if len(shape) == 3:  # if image is RGB
        h, w, ch = shape
        bytes_per_line = ch * w
        if bgr2rgb:
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        converted_to_qimage = Qtg.QImage(cv_img.data, w, h, bytes_per_line, Qtg.QImage.Format_RGB888)

    else:  # else it's grayscale
        h, w = shape
        ch = 1
        bytes_per_line = ch * w
        converted_to_qimage = Qtg.QImage(cv_img.data, w, h, bytes_per_line, Qtg.QImage.Format_Grayscale8)

    if qsize is None:  # If no scale indicated then full scale
        qsize = Qtc.QSize(w, h)

    p = converted_to_qimage.scaled(qsize, Qtc.Qt.KeepAspectRatio)
    return Qtg.QPixmap.fromImage(p)


def convert_CV_64F_to_uint8(img):
    img = img - img.min()
    img = img / img.max() * 255

    return np.uint8(img)


def is_gray(img):
    if len(img.shape) <= 2:
        return True
    return False


def is_color(img):
    if len(img.shape) >= 3:
        return True
    return False


class QLabelRect(Qtw.QLabel):
    """Overriding the Qtw.QLabel class for getting position of mousePressEvent and drawing rectangle with mouse"""

    mouse_released_signal = Qtc.pyqtSignal(Qtc.QPoint, Qtc.QPoint)

    def __init__(self):
        super().__init__()
        self.x0 = 0
        self.y0 = 0
        self.qpos0 = Qtc.QPoint()
        self.x1 = 0
        self.y1 = 0
        self.qpos1 = Qtc.QPoint()
        self.flag = False
        self.setting_aoi = False

    def mousePressEvent(self, event):
        if event.button() == Qtc.Qt.LeftButton and self.setting_aoi:

            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()
            self.qpos0 = event.pos()
            self.x1 = self.x0
            self.y1 = self.y0
            self.qpos1 = self.qpos0

            Qtw.QLabel.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qtc.Qt.LeftButton:
            self.flag = False
            self.mouse_released_signal.emit(self.qpos0, self.qpos1)

            Qtw.QLabel.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.flag and self.setting_aoi:
            self.x1 = event.x()
            self.y1 = event.y()
            self.qpos1 = event.pos()
            self.update()

            Qtw.QLabel.mouseMoveEvent(self, event)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.flag:
            rect = Qtc.QRect(min(self.x0, self.x1), min(self.y0, self.y1),
                             abs(self.x1 - self.x0), abs(self.y1 - self.y0))
            painter = Qtg.QPainter(self)
            painter.setPen(Qtg.QPen(Qtc.Qt.red, 2, Qtc.Qt.SolidLine))
            painter.drawRect(rect)


class QLabelLin(Qtw.QLabel):
    """Overriding the Qtw.QLabel class for getting position of mousePressEvent and drawing rectangle with mouse"""

    mouse_released_signal = Qtc.pyqtSignal(Qtc.QPoint, Qtc.QPoint)

    def __init__(self):
        super().__init__()
        self.x0 = 0
        self.y0 = 0
        self.qpos0 = Qtc.QPoint()
        self.x1 = 0
        self.y1 = 0
        self.qpos1 = Qtc.QPoint()
        self.flag = False
        self.setting_scale = False

    def mousePressEvent(self, event):
        if event.button() == Qtc.Qt.LeftButton and self.setting_scale:

            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()
            self.qpos0 = event.pos()
            self.x1 = self.x0
            self.y1 = self.y0
            self.qpos1 = self.qpos0

            Qtw.QLabel.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qtc.Qt.LeftButton:
            self.flag = False
            self.mouse_released_signal.emit(self.qpos0, self.qpos1)

            Qtw.QLabel.mouseReleaseEvent(self, event)
            self.setting_scale = False

    def mouseMoveEvent(self, event):
        if self.flag and self.setting_scale:
            self.x1 = event.x()
            self.y1 = event.y()
            self.qpos1 = event.pos()
            self.update()

            Qtw.QLabel.mouseMoveEvent(self, event)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.flag:
            line = Qtc.QLine(self.x0, self.y0, self.x1, self.y1)
            painter = Qtg.QPainter(self)
            painter.setPen(Qtg.QPen(Qtc.Qt.red, 2, Qtc.Qt.SolidLine))
            painter.drawLine(line)


class GetVideoThread(Qtc.QThread):

    new_cv_img_signal = Qtc.pyqtSignal(np.ndarray)
    stopped_signal = Qtc.pyqtSignal()

    def __init__(self, cam):
        super().__init__()
        self.run_flag = True
        self.cam = cam

    def run(self):

        self.run_flag = True
        while self.run_flag:
            array = self.cam.get_image()
            frame = np.reshape(array, (self.cam.height.value, self.cam.width.value, int(self.cam.nBitsPerPixel / 8)))
            frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
            # frame = cv2.flip(frame, 1)
            self.new_cv_img_signal.emit(frame)

            time.sleep(1/15)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.run_flag = False
        self.stopped_signal.emit()


class Timer:
    def __init__(self):
        self._start_time = None
        self.last_elapsed_time = None

    def start(self):
        """Start a new timer"""
        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            return 0

        self.last_elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        return self.last_elapsed_time

    def reset(self):
        """reset the timer, and report the elapsed time"""
        if self._start_time is None:
            return 0

        t = time.perf_counter()
        self.last_elapsed_time = t - self._start_time
        self._start_time = t
        return self.last_elapsed_time


def midpoint(a, b):
    return (a[0]+b[0])/2, (a[1]+b[1])/2


def distance(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


class WarningWidget(Qtw.QDialog):
    def __init__(self, text, cancel):
        super().__init__()

        self.setWindowTitle(STR_WARNING)

        text_qlabel = Qtw.QLabel(text)
        text_qlabel.setFont(Qtg.QFont("Times", 12))

        self.ok_btn = Qtw.QPushButton(STR_OK)
        self.ok_btn.clicked.connect(self.ok)
        if cancel:
            self.cancel_btn = Qtw.QPushButton(STR_CANCEL)
            self.cancel_btn.clicked.connect(self.cancel)
        layout = Qtw.QGridLayout()
        layout.addWidget(text_qlabel, 0, 0, 1, 2)
        if cancel:
            layout.addWidget(self.ok_btn, 1, 0)
            layout.addWidget(self.cancel_btn, 1, 1)
        else:
            layout.addWidget(self.ok_btn, 1, 0, 1, 2)

        self.setLayout(layout)

        self.setWindowIcon(Qtg.QIcon(":/warning_icon.png"))

    @Qtc.pyqtSlot()
    def ok(self):
        self.done(1)

    @Qtc.pyqtSlot()
    def cancel(self):
        self.done(0)


