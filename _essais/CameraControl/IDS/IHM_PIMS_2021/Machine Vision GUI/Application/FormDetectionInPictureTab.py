import os.path

import numpy as np
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtCore as Qtc
from PyQt5 import Qt as Qt
from PyQt5 import QtGui as Qtg
import cv2

from Utils import h_line, v_line, convert_cv_to_qpixmap, convert_CV_64F_to_uint8, open_img
from PreProcessingFunction import func_find_draw_contours, func_contours_list
from FormDetectionFunction import *
from Dictionary_EN import *


class FormDetectionInPictureTab(Qtw.QTabWidget):
    def __init__(self):
        super().__init__()
        self.input_img_cv = None
        self.outlines_img = None
        self.outlines = None
        self.nb_shapes = None

        self.input_tab = InputTab()
        self.input_tab.open_btn.clicked.connect(self.load_img)

        self.train_tab = TrainTab()

        self.detection_tab = DetectionTab()

        self.addTab(self.input_tab, STR_INPUT)
        self.addTab(self.train_tab, STR_TRAIN)
        self.addTab(self.detection_tab, STR_DETECTION)

    def load_img(self):
        img = open_img(self)
        if img is not None:
            self.input_img_cv = img
            self.outlines = func_contours_list(img, 200)
            self.outlines_img = func_find_draw_contours(img, surface_min=200, contours_list=self.outlines)
            self.nb_shapes = len(self.outlines)
            self.input_tab.show_data(self.input_img_cv, self.outlines_img)
            self.train_tab.show_data(self.input_img_cv, self.outlines, self.nb_shapes)
            self.detection_tab.show_data(self.input_img_cv, self.outlines, self.nb_shapes)

    def resizeEvent(self, event):
        Qtw.QTabWidget.resizeEvent(self, event)
        current_widget = self.currentWidget()
        current_widget.update_size()


class InputTab(Qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.img_cv = None
        self.outlines_img_cv = None

        self.open_btn = Qtw.QPushButton(STR_OPEN_IMAGE)
        self.open_btn.setIcon(Qtg.QIcon(":/open_icon.png"))
        self.take_from_processing_btn = Qtw.QPushButton(STR_TAKE_FROM_PROCESSING)

        tab_widget = Qtw.QTabWidget()

        self.img_qlabel = Qtw.QLabel()
        tab_widget.addTab(self.img_qlabel, STR_INPUT_IMAGE)
        self.outlines_qlabel = Qtw.QLabel()
        tab_widget.addTab(self.outlines_qlabel, STR_OUTLINES)

        layout = Qtw.QGridLayout()
        layout.addWidget(self.open_btn, 0, 0)
        layout.addWidget(self.take_from_processing_btn, 0, 1)
        layout.addWidget(tab_widget, 1, 0, 2, 2)

        self.setLayout(layout)

    def show_data(self, img, outlines_img):
        self.img_cv = img
        self.img_qlabel.setPixmap(convert_cv_to_qpixmap(img, self.img_qlabel.size()))

        self.outlines_img_cv = outlines_img
        self.outlines_qlabel.setPixmap(convert_cv_to_qpixmap(outlines_img, self.outlines_qlabel.size()))

    def update_size(self):
        if self.img_cv is not None:
            self.img_qlabel.setPixmap(convert_cv_to_qpixmap(self.img_cv, self.img_qlabel.size()))
            self.outlines_qlabel.setPixmap(convert_cv_to_qpixmap(self.outlines_img_cv, self.outlines_qlabel.size()))


class TrainTab(Qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.img_cv = None
        self.contours_list = None
        self.nb_shapes = None

        self.main_img_qlabel = Qtw.QLabel()

        self.nb_form_qlabel = Qtw.QLabel()

        calculate_btn = Qtw.QPushButton(STR_CALCULATE)
        calculate_btn.clicked.connect(self.calculate)

        right_layout = Qtw.QVBoxLayout()
        right_layout.addWidget(calculate_btn)
        right_layout.addWidget(h_line())

        layout = Qtw.QHBoxLayout()
        layout.addLayout(right_layout)
        layout.addWidget(v_line())
        layout.addWidget(self.main_img_qlabel)

        self.setLayout(layout)

        self.ask_shape_name_dialog = AskShapeName()

    def show_data(self, img, contours_list, nb_shapes):
        self.img_cv = img
        self.main_img_qlabel.setPixmap(convert_cv_to_qpixmap(img, self.main_img_qlabel.size()))

        self.contours_list = contours_list
        self.nb_shapes = nb_shapes

    def update_size(self):
        if self.img_cv is not None:
            self.main_img_qlabel.setPixmap(convert_cv_to_qpixmap(self.img_cv, self.main_img_qlabel.size()))

    @Qtc.pyqtSlot()
    def calculate(self):
        directory = Qtw.QFileDialog.getExistingDirectory(self, 'Open directory', '',
                                                         Qtw.QFileDialog.ShowDirsOnly |
                                                         Qtw.QFileDialog.DontResolveSymlinks)
        if directory != '':
            for cnt in self.contours_list:
                x_min, x_max, y_min, y_max = coordinates(cnt)

                shape_img = np.zeros(self.img_cv.shape, np.uint8)
                cv2.drawContours(shape_img, [cnt], 0, 255, -1)
                shape_img = crop_image_w_margin(shape_img, x_min, x_max, y_min, y_max)

                shape_img = convert_CV_64F_to_uint8(shape_img)

                self.ask_shape_name_dialog.show_shape(shape_img)

                current_shape_name = SHAPES_NAME_LIST[self.ask_shape_name_dialog.exec()]

                directory_shape_folder = os.path.join(directory, current_shape_name)
                os.makedirs(directory_shape_folder, exist_ok=True)  # leaves the directory unchanged if already created

                number_of_files = len([f for f in os.listdir(directory_shape_folder)
                                       if os.path.isfile(os.path.join(directory_shape_folder, f))])

                filename_csv = os.path.join(directory_shape_folder,
                                            current_shape_name + str(int(number_of_files)) + '.csv')
                filename_jpg = os.path.join(directory_shape_folder,
                                            current_shape_name + str(int(number_of_files)) + '.jpg')

                #write_csv_file(filename_csv, cnt)
                cv2.imwrite(filename_jpg, shape_img)


class AskShapeName(Qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(STR_NAME_THE_SHAPE)
        self.setModal(True)

        self.img_cv = None
        self.form_img_qlabel = Qtw.QLabel()

        square_btn = Qtw.QPushButton(STR_SQUARE)
        square_btn.clicked.connect(self.is_square)
        triangle_btn = Qtw.QPushButton(STR_TRIANGLE)
        triangle_btn.clicked.connect(self.is_triangle)
        circle_btn = Qtw.QPushButton(STR_CIRCLE)
        circle_btn.clicked.connect(self.is_circle)
        star_btn = Qtw.QPushButton(STR_STAR)
        star_btn.clicked.connect(self.is_star)
        pentagon_btn = Qtw.QPushButton(STR_PENTAGON)
        pentagon_btn.clicked.connect(self.is_pentagon)
        hexagon_btn = Qtw.QPushButton(STR_HEXAGON)
        hexagon_btn.clicked.connect(self.is_hexagon)
        nothing_btn = Qtw.QPushButton(STR_NOTHING)
        nothing_btn.clicked.connect(self.is_nothing)

        btn_layout = Qtw.QGridLayout()
        qlabel = Qtw.QLabel(STR_WHAT_IS_THIS_SHAPE)
        qlabel.setFont(Qtg.QFont("Times", 12))

        btn_layout.addWidget(qlabel, 0, 0, 1, 3)
        btn_layout.addWidget(square_btn, 1, 0)
        btn_layout.addWidget(circle_btn, 1, 1)
        btn_layout.addWidget(star_btn, 1, 2)
        btn_layout.addWidget(triangle_btn, 2, 0)
        btn_layout.addWidget(pentagon_btn, 2, 1)
        btn_layout.addWidget(hexagon_btn, 2, 2)
        btn_layout.addWidget(nothing_btn, 3, 0)

        layout = Qtw.QVBoxLayout()
        layout.addWidget(self.form_img_qlabel)
        layout.addWidget(h_line())
        layout.addWidget(qlabel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def show_shape(self, img):
        self.img_cv = img
        self.form_img_qlabel.setPixmap(convert_cv_to_qpixmap(img, self.form_img_qlabel.size()))

    def resizeEvent(self, event):
        Qtw.QDialog.resizeEvent(self, event)
        self.form_img_qlabel.setPixmap(convert_cv_to_qpixmap(self.img_cv, self.form_img_qlabel.size()))

    @Qtc.pyqtSlot()
    def is_square(self):
        self.done(0)

    @Qtc.pyqtSlot()
    def is_triangle(self):
        self.done(1)

    @Qtc.pyqtSlot()
    def is_star(self):
        self.done(2)

    @Qtc.pyqtSlot()
    def is_circle(self):
        self.done(3)

    @Qtc.pyqtSlot()
    def is_hexagon(self):
        self.done(4)

    @Qtc.pyqtSlot()
    def is_pentagon(self):
        self.done(5)

    @Qtc.pyqtSlot()
    def is_nothing(self):
        self.done(6)


class VerifShapeName(Qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(STR_VERIF_SHAPE_NAME)
        self.setModal(True)

        self.img_cv = None
        self.img_qlabel = Qtw.QLabel()

        yes_btn = Qtw.QPushButton(STR_YES)
        yes_btn.clicked.connect(self.yes)
        no_btn = Qtw.QPushButton(STR_NO)
        no_btn.clicked.connect(self.no)

        self.detected_shape_name_qlabel = Qtw.QLabel()

        layout = Qtw.QGridLayout()
        layout.addWidget(self.img_qlabel, 0, 0, 1, 2)
        layout.addWidget(h_line(), 1, 0, 1, 2)
        layout.addWidget(Qtw.QLabel(STR_DETECTED_SHAPE), 2, 0)
        layout.addWidget(self.detected_shape_name_qlabel, 2, 1)
        layout.addWidget(h_line(), 3, 0, 1, 2)
        layout.addWidget(Qtw.QLabel(STR_IS_IT_TRUE), 4, 0, 1, 2)
        layout.addWidget(yes_btn, 5, 0)
        layout.addWidget(no_btn, 5, 1)

        self.setLayout(layout)

    def show_shape(self, img, detected_shape_index):
        self.img_cv = img
        self.img_qlabel.setPixmap(convert_cv_to_qpixmap(img, self.img_qlabel.size()))

        shape_name = SHAPES_NAME_LIST[detected_shape_index]
        self.detected_shape_name_qlabel.setText(shape_name)

    def resizeEvent(self, event):
        Qtw.QDialog.resizeEvent(self, event)
        self.img_qlabel.setPixmap(convert_cv_to_qpixmap(self.img_cv, self.img_qlabel.size()))

    @Qtc.pyqtSlot()
    def yes(self):
        self.done(1)

    @Qtc.pyqtSlot()
    def no(self):
        self.done(0)


class DetectionTab(Qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.img_cv = None
        self.contours_list = None
        self.nb_shapes = None
        self.img_shapes_list = None
        self.detected_shapes_index_list = None

        self.count_detected_shapes = None
        self.correct_shapes_index_list = None

        self.main_img_qlabel = Qtw.QLabel()
        self.shape_img_qlabel = Qtw.QLabel()

        self.nb_shape_qlabel = Qtw.QLabel()
        self.nb_detected_square_qlabel = Qtw.QLabel()
        self.nb_detected_triangle_qlabel = Qtw.QLabel()
        self.nb_detected_star_qlabel = Qtw.QLabel()
        self.nb_detected_pentagon_qlabel = Qtw.QLabel()
        self.nb_detected_hexagon_qlabel = Qtw.QLabel()
        self.nb_detected_circle_qlabel = Qtw.QLabel()
        self.error_qlabel = Qtw.QLabel()

        self.nb_detected_qlabel_list = [self.nb_detected_square_qlabel, self.nb_detected_triangle_qlabel,
                                        self.nb_detected_star_qlabel, self.nb_detected_circle_qlabel,
                                        self.nb_detected_hexagon_qlabel, self.nb_detected_pentagon_qlabel]

        calculate_btn = Qtw.QPushButton(STR_CALCULATE)
        calculate_btn.clicked.connect(self.calculate)
        verif_shapes_btn = Qtw.QPushButton(STR_VERIF_ALL_SHAPES)
        verif_shapes_btn.clicked.connect(self.verif_shape)

        left_layout = Qtw.QVBoxLayout()
        left_layout.addWidget(calculate_btn)
        left_layout.addWidget(h_line())

        nb_shape_form = Qtw.QFormLayout()
        nb_shape_form.addRow(Qtw.QLabel(STR_NB_FORM), self.nb_shape_qlabel)

        for i in range(6):
            nb_shape_form.addRow(Qtw.QLabel(SHAPES_NAME_LIST[i]), self.nb_detected_qlabel_list[i])

        nb_shape_form.addRow(Qtw.QLabel(STR_ERROR), self.error_qlabel)

        left_layout.addLayout(nb_shape_form)

        left_layout.addWidget(h_line())
        left_layout.addWidget(verif_shapes_btn)

        layout = Qtw.QHBoxLayout()
        layout.addLayout(left_layout)
        layout.addWidget(v_line())
        layout.addWidget(self.main_img_qlabel)

        self.setLayout(layout)

        self.verif_shape_name_dialog = VerifShapeName()

    def show_data(self, img, contours_list, nb_shapes):
        self.main_img_qlabel.setPixmap(convert_cv_to_qpixmap(img, self.main_img_qlabel.size()))
        self.nb_shape_qlabel.setText(str(nb_shapes))

        self.img_cv = img
        self.contours_list = contours_list
        self.nb_shapes = nb_shapes

    def update_size(self):
        if self.img_cv is not None:
            self.main_img_qlabel.setPixmap(convert_cv_to_qpixmap(self.img_cv, self.main_img_qlabel.size()))

    @Qtc.pyqtSlot()
    def calculate(self):
        directory = Qtw.QFileDialog.getExistingDirectory(self, 'Open directory', '',
                                                         Qtw.QFileDialog.ShowDirsOnly |
                                                         Qtw.QFileDialog.DontResolveSymlinks)
        if directory != '':
            self.img_shapes_list = get_img_shape_list(self.img_cv, self.contours_list)

            self.detected_shapes_index_list = identify_shapes(self.img_shapes_list, directory)

            self.count_detected_shapes = sort_shapes(self.detected_shapes_index_list)

            for i in range(6):
                self.nb_detected_qlabel_list[i].setText(str(int(self.count_detected_shapes[i])))
            self.error_qlabel.setText('')

    def verif_shape(self):

        self.correct_shapes_index_list = []
        nb_error = 0
        for i in range(self.nb_shapes):
            shape_img = self.img_shapes_list[i]
            self.verif_shape_name_dialog.show_shape(convert_CV_64F_to_uint8(shape_img),
                                                    self.detected_shapes_index_list[i])
            is_correct = self.verif_shape_name_dialog.exec()
            if not is_correct:
                nb_error += 1

        self.error_qlabel.setText(str(nb_error))







