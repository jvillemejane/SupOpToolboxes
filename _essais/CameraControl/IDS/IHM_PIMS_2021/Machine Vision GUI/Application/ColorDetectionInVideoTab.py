
import numpy as np
import os
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtCore as Qtc
from PyQt5 import Qt as Qt
from PyQt5 import QtGui as Qtg
import cv2
import time
import colorsys

from Utils import convert_cv_to_qpixmap, Timer, h_line, QLabelLin, midpoint, distance, is_color
from PreProcessingFunction import func_contours_list, gray_to_binary
from FormDetectionFunction import is_outside

from Dictionary_EN import *


class ColorDetectionInVideoTab(Qtw.QMainWindow):
    def __init__(self, video_thread):
        super().__init__()

        self.shown_cv_img = None
        self.calculating = False

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
        setting_form_layout.addRow(self.show_binary_checkbox)
        setting_form_layout.addRow(self.opening_checkbox)
        setting_form_layout.addRow(self.closing_checkbox)
        setting_form_layout.addRow(self.blur_checkbox)
        setting_form_layout.addRow(STR_THRESHOLD, self.threshold_spinbox)
        setting_form_layout.addRow(STR_MIN_SURFACE, self.min_area_spinbox)
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

        if is_color(cv_img):
            self.calculate_btn.setEnabled(True)
            self.screenshot_btn.setEnabled(True)
            self.clipboard_btn.setEnabled(True)

            d_t = self.timer.reset()
            self.fps_qlabel.setText(str(int(1 / d_t)))

            if self.calculating:

                gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

                #cv2.imshow("Image", mask_img);
                #cv2.waitKey(0);



                self.shown_cv_img = display_name(gray_img, cv_img)

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
            self.video_qlabel.setText(STR_GRAY_TO_COLOR)
            self.shown_cv_img = None
            self.fps_qlabel.setText('')

    def resizeEvent(self, event):
        """Overriding the resizeEvent methode for resize the Qlabels containing image each time the main window
         is resized """
        Qtw.QWidget.resizeEvent(self, event)  # Calling the basic resizeEvent of QWidget
        if self.shown_cv_img is not None:
            qt = convert_cv_to_qpixmap(self.shown_cv_img, self.video_qlabel.size())
            self.video_qlabel.setPixmap(qt)







def color_clusters(img,nclusters):
    # les samples pour cv2.kmean doivent être sous dorme d'une unique colonne
    pixels = np.float32(img.reshape(-1, 3))
    # définition du critère de terminaision pour l'algo itératif cv2.kmean
    # dès que la precision eps est atteinte ou des que le nombre max d'iteraitions est atteinte
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.)
    # pour ruptures de lignes :
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centers = cv2.kmeans(pixels, nclusters, None, criteria, 10, flags)
    return labels, centers


def color_diagram_data(img,labels):
    # counts : nombre de fois que chaque couleur apparaît :
    _, counts = np.unique(labels, return_counts=True)
    # indices (0: couleur dominante, nclusters-1 : couleur minoritaire)
    indices = np.argsort(counts)[::-1]
    # fréquences cumulées d'apparition des couleurs (dominantes d'abord, minoritaires après):
    freqs = np.cumsum(np.hstack([[0], counts[indices] / counts.sum()]))
    # nombre de lignes corresppndant pour chaque couleur
    rows = np.int_(img.shape[0] * freqs)
    return rows, indices


# quantification des couleurs : réduction du nombre de couleurs de l'image
def average_dominant(img,nclusters):
    labels, centers = color_clusters(img,nclusters)
    rows, indices = color_diagram_data(img,labels)
    liste_legende=[]
    for i in range(len(rows) - 1):
        dominant = centers[indices[i]]
        [B, G, R] = dominant
        dominant = [int(R), int(G), int(B)]
        liste_legende.append(dominant)
    return liste_legende


def hls2rgb(h,l,s):
    return tuple((i*255) for i in colorsys.hls_to_rgb(h,l,s))


def rgb2hls(r,g,b):
    return tuple((i*255) for i in colorsys.rgb_to_hls(r,g,b))


# position sur le diagramme des couleurs
def dominant_position(r, g, b):
    print(r,g,b)
    imgHL = np.zeros((255,255,3))
    [h,l,s]=rgb2hls(r/255,g/255,b/255)
    h,l,s=h/255,l/255,s/255
    min=10
    imin=0
    jmin=0
    for i in range(255):
        for j in range(255):
            H=i/255
            S=250/255
            L=j/255
            [R,G,B]=hls2rgb(H,L,S)
            imgHL[i, j, 0] = R/255
            imgHL[i, j, 1] = G/255
            imgHL[i, j, 2] = B/255
            similarity = ((H-h)**2 +(S-s)**2 +(L-l)**2)/3
            if similarity<min:
                min=similarity
                imin=i
                jmin=j
    return imin


def dominant_color(i):
    if i<=15:
        char = 'red'
    if i>15 and i<=35:
        char = 'orange'
    if i>35 and i<=45:
        char = 'yellow'
    if i>45 and i<=110:
        char = 'green'
    if i>110 and i<=120:
        char = 'blue-green'
    if i>120 and i<=135:
        char = 'cyan'
    if i>135 and i<=180:
        char = 'blue'
    if i>180 and i<=205:
        char = 'purple'
    if i>205 and i<=245:
        char = 'pink'
    if i>245:
        char = 'red'
    return char


def what_is_this_color(triplet):
    [r,g,b] = triplet
    i = dominant_position(r, g, b)
    char = dominant_color(i)
    return char


def display_name(mask,img):
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE);
    print(len(contours))
    for c in contours:
        mask[:] = 0;
        mask = cv2.drawContours(mask, [c], -1, 255, -1);
        one_color = img.copy()
        one_color[mask != 255] = (0, 0, 0);
        dominant_list = average_dominant(one_color, 2)
        char = what_is_this_color(dominant_list[1])
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.drawContours(img, [c], -1, (0, 255, 0), 3)
        cv2.putText(img, char, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return img
    #cv2.imshow("Image", img);
    #cv2.waitKey(0);