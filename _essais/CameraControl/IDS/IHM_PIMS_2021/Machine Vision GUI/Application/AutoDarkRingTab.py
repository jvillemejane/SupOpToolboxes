"""--------------------------------------------------------------------------------

Vision Industrielle
-----------------------------------------------------------------------------------
Par l'équipe PIMS (Samuel Gerente, Hugo Lassiette, Flora Silberzan, Martin Collignon, Oscar Boucher, Victoire de Saléon
et par l'équipe ProTIS (Tong Zhu, Albane Lapras, Martin Collignon, Victoire de Saléon)
-----------------------------------------------------------------------------------
La classe AutoDarkRingTab est appelée dans le main.py à la ligne 208 (dans la classe MainWindow) par :
    @Qtc.pyqtSlot()
    def add_auto_dark_ring(self):
        self.main_tab_widget.addTab(AutoDarkRingTab(self.video_thread, self.ser), STR_AUTO_DARK_RING)
cette fonction permet de rajouter un menu dans la fenêtre principale
------------------------------------------------------------------------------------
ce menu permet de :
    - visualiser l'aquisition vidéo si la caméra est allumée (les images de la vidéo sont dans self.shown_cv_img)
    - effectuer des traitements simple de l'image (ouverture fermeture flou gaussien, pour une binarisation optimale)
    - définir les paramètres de détection de contours des objets (aire minimale et maximale des objets d'interêts)
    - enregistrer une image de l'aquisition manuellement (soit dans le clipboard soit dans un dossier)
ET SURTOUT de :
    - détecter les contours des objets
    - déterminer leur centre et sa distance avec le centre de l'anneau
    - si l'objet est au centre de l'anneau, baisser l'anneau et prendre une photo enregistrée automatiquement dans un dossier, puis relever l'anneau

--------------------------------------------------------------------------------"""

import numpy as np

#permet de créer des interfaces en python :
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtCore as Qtc

#fonctions de bases du traitement de l'image et de manipulation d'images :
import cv2

#fonctions programmées pendant les semaines PIMS
from Utils import convert_cv_to_qpixmap, Timer, h_line, is_gray
from PreProcessingFunction import func_contours_list, gray_to_binary
from FormDetectionFunction import is_outside

#dictionnaire de chaines de caractères fait pendant les semaines PIMS
from Dictionary_EN import *


class AutoDarkRingTab(Qtw.QMainWindow):
    def __init__(self, video_thread, ser):
        super().__init__()
        self.nb=0 # numérotation des photos
        self.ser = ser # pour la conection usb

        self.raw_cv_img = None
        self.shown_cv_img = None
        self.calculating = False # Bouton de calcul en mode off

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

        """Pre-processing Buttons"""

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
        self.threshold_spinbox.setValue(80) #valeur du seuil fixée à 80

        self.min_area_spinbox = Qtw.QSpinBox()
        self.min_area_spinbox.setRange(0, 1000000000)
        self.min_area_spinbox.setSingleStep(50)
        self.min_area_spinbox.setValue(1000)

        self.max_area_spinbox = Qtw.QSpinBox()
        self.max_area_spinbox.setRange(0, 1000000000)
        self.max_area_spinbox.setSingleStep(50)
        self.max_area_spinbox.setValue(90000)

        """Screenshot Buttons"""

        self.screenshot_btn = Qtw.QPushButton(STR_TAKE_SCREENSHOT)
        self.screenshot_btn.clicked.connect(self.save_screenshot)
        self.screenshot_btn.setEnabled(False)
        self.clipboard_btn = Qtw.QPushButton(STR_COPY_TO_CLIPBOARD)
        self.clipboard_btn.clicked.connect(self.clipboard_screenshot)
        self.clipboard_btn.setEnabled(False)

        """Layout"""
        #on ajoute tous les éléments au layout

        setting_form_layout = Qtw.QFormLayout()
        setting_form_layout.addRow(self.calculate_btn) # ajout du bouton pour le calcul de la position des objets
        setting_form_layout.addRow(h_line()) # petite ligne horizontale pour que ca soit joli
        setting_form_layout.addRow(Qtw.QLabel(STR_FPS), self.fps_qlabel) #chaîne de caractères pour indiquer le nombre d'images par secondes
        setting_form_layout.addRow(h_line()) # petite ligne horizontale pour que ca soit joli
        setting_form_layout.addRow(self.show_binary_checkbox) # petite checkbox pour montrer l'image binaire
        setting_form_layout.addRow(self.opening_checkbox) # petite checkbox pour effectuer une ouverture
        setting_form_layout.addRow(self.closing_checkbox) # petite checkbox pour effectuer une fermeture
        setting_form_layout.addRow(self.blur_checkbox) # petite checkbox pour effectuer une fermeture
        setting_form_layout.addRow(STR_THRESHOLD, self.threshold_spinbox) # petite spinbox pour choisir la valeur du seuil pour le seuillage
        setting_form_layout.addRow(STR_MIN_SURFACE, self.min_area_spinbox) # petite spinsbox pour choisir la taille minimale d'un objet
        setting_form_layout.addRow(STR_MAX_SURFACE, self.max_area_spinbox)
        setting_form_layout.addRow(h_line())
        setting_form_layout.addRow(self.screenshot_btn, self.clipboard_btn)

        setting_widget.setLayout(setting_form_layout)

        self.setting_dock.setWidget(setting_widget)
        self.addDockWidget(Qtc.Qt.LeftDockWidgetArea, self.setting_dock)
        self.timer = Timer()
        self.timer.start()

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
    def save_screenshot(self): # permet d'ouvrir une fenêtre pour enregistrer le screenshot
        filename = Qtw.QFileDialog.getSaveFileName(self, STR_SAVE_IMAGE, '', STR_IMAGE_FORMAT)
        print(filename[0])
        if filename[0] != "":
            cv2.imwrite(filename[0], self.shown_cv_img)

    @Qtc.pyqtSlot()
    def clipboard_screenshot(self): # permet de copier l'image dans le clipboard
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
    def update_video_qlabel(self, cv_img): # met à jour l'image avec la nouvelle image de la caméra
        if is_gray(cv_img):
            self.calculate_btn.setEnabled(True)
            self.screenshot_btn.setEnabled(True)
            self.clipboard_btn.setEnabled(True)
            d_t = self.timer.reset()
            self.fps_qlabel.setText(str(int(1 / d_t)))

            if self.calculating:
                binary_img = gray_to_binary(cv_img, self.threshold_spinbox.value(), self.opening_checkbox.isChecked(),self.closing_checkbox.isChecked(), self.blur_checkbox.isChecked())
                [l,c]=np.shape(binary_img)

                #paramètres pour déteriner la position de l'image par rapport au centre
                center_l = round(l/2) # coordonnée du centre
                center_c = round(c/2) # coordonnée du centre
                AOI = 400 #tous les objets dont le centre est à plus de 400 pix du centre de la zone d'intérêt ne sont pas pris en compte
                contours_list = func_contours_list(binary_img, self.min_area_spinbox.value(), self.max_area_spinbox.value()) #liste des contours des formes sur l'image

                if self.show_binary_checkbox.isChecked():
                    contours_img = cv2.merge([binary_img, binary_img, binary_img])
                else:
                    contours_img = cv2.merge([cv_img, cv_img, cv_img])

                # sélection des formes de la liste qui sont au centre de l'image
                for cnt in contours_list:
                    # on calcule le centre de la forme à l'aide des moments de Hu
                    m = cv2.moments(cnt)
                    center_x = int(m["m10"] / m["m00"])
                    center_y = int(m["m01"] / m["m00"])
                    R = np.sqrt((center_x-center_l)**2 +(center_y-center_c)**2)
                    if not is_outside(cnt, cv_img.shape):
                        if R<AOI:
                            if R<250: #si l'objet est proche du centre on baisse l'anneau et on prend la photo
                                self.ser.write(chr(65).encode('utf-8'))
                                self.nb+=1 #mise a jour du numéro de la photo
                                cv2.imwrite("C:/Users/victo/PycharmProjects/PIMSProTis/Picture/piece/piece"+str(self.nb)+".png", contours_img) #enregistrement de l'image
                            if R>250: #si l'objet est loin du centre on relève l'anneau
                                self.ser.write(chr(100).encode('utf-8'))
                            #on dessine sur l'image les contours des formes
                            cv2.drawContours(contours_img, cnt, -1, (0, 0, 255), 3)

                            #on affiche le centre de la forme
                            cv2.circle(contours_img, (center_x, center_y), 4, (0, 0, 255), -1)
                            cv2.putText(contours_img, str(center_x) + "," + str(center_y), (center_x - 55, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)


                #on trace sur l'image la région d'interêt
                cv2.circle(contours_img, (center_l, center_c), AOI, (0, 0, 255), 4)
                cv2.circle(contours_img, (center_l,center_c),4,(0,0,255),-1)
                cv2.putText(contours_img, "center", (center_l,center_c),cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 2, cv2.LINE_AA)

                #on affiche l'image
                self.shown_cv_img = contours_img

            else: #si le bouton de calcul n'a pas été cliqué
                self.shown_cv_img = cv_img

            #l'image à afficher (avec ou sans les calculs réalisés) est convertie puis ajoutée à l'interface
            qt_img = convert_cv_to_qpixmap(self.shown_cv_img, self.video_qlabel.size())
            self.video_qlabel.setPixmap(qt_img)

        else: # si l'aquisition d'image en noir est blanc n'est pas lancée
            self.calculating = False
            self.calculate_btn.setEnabled(False) # on ne peut pas appuyer sur le bouton
            self.calculate_btn.setText(STR_START_CALCULATION)
            self.screenshot_btn.setEnabled(False) # on ne peut pas faire de screenshot
            self.clipboard_btn.setEnabled(False) # on ne peut pas enregistrer dans le clipboard
            self.video_qlabel.setText(STR_COLOR_TO_GRAY)
            self.shown_cv_img = None # il n'y a aucune image affichée
            self.fps_qlabel.setText('')

    def resizeEvent(self, event):
        Qtw.QWidget.resizeEvent(self, event)  # Calling the basic resizeEvent of QWidget
        if self.shown_cv_img is not None:
            qt = convert_cv_to_qpixmap(self.shown_cv_img, self.video_qlabel.size())
            self.video_qlabel.setPixmap(qt)












