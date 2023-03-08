import numpy as np
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtCore as Qtc
from PyQt5 import Qt as Qt
from PyQt5 import QtGui as Qtg
import cv2

from PreProcessingFunction import *
from Utils import h_line, convert_cv_to_qpixmap, convert_CV_64F_to_uint8, open_img, save_img, WarningWidget
from Dictionary_EN import *


class SimpleProcessingInVideoTab(Qtw.QMainWindow):
    """The image processing tab widget is build here"""

    request_screenshot_signal = Qtc.pyqtSignal()

    def __init__(self, video_thread):
        super().__init__()

        self.get_video_thread = video_thread
        self.get_video_thread.new_cv_img_signal.connect(self.update_video_qlabel)
        #self.get_video_thread.stopped_signal.connect(self.video_stopped)

        # Attributes for stocking the imported (see after) input image
        self.shown_cv_img = None

        self.calculating = False

        # Those lists will store all the output image and histo (after each process, at index 0 after the process 1
        # and so on)
        self.output_img_list = []

        # Dockable widget used for the process and algo choices
        self.process_dock = Qtw.QDockWidget(STR_SELECTION, self)
        self.process_widget = Qtw.QWidget()

        # QTreeWidget that will contain the added process
        self.process_tree = ProcessTreeWidget()

        # Buttons for adding deleteing and moving an item (process) in the list
        add_btn = Qtw.QPushButton(STR_ADD)
        add_btn.setIcon(Qtg.QIcon(":/add_icon.png"))
        add_btn.clicked.connect(self.add_item)
        del_btn = Qtw.QPushButton(STR_DELETE)
        del_btn.setIcon(Qtg.QIcon(":/del_icon.png"))
        del_btn.clicked.connect(self.del_item)
        del_all_btn = Qtw.QPushButton(STR_DELETE_ALL)
        del_all_btn.clicked.connect(self.ask_del_all_item)
        down_btn = Qtw.QPushButton(STR_DOWN)
        down_btn.setIcon(Qtg.QIcon(":/down_arrow_icon.png"))
        down_btn.clicked.connect(self.down_item)
        up_btn = Qtw.QPushButton(STR_UP)
        up_btn.setIcon(Qtg.QIcon(":/up_arrow_icon.png"))
        up_btn.clicked.connect(self.up_item)

        # Button for launching the image processing according the selected process
        calculate_btn = Qtw.QPushButton(STR_CALCULATE)
        calculate_btn.setIcon(Qtg.QIcon(":/setting_icon.png"))
        calculate_btn.clicked.connect(self.calculate)

        # Drop-down list containing all the process
        self.process_list = Qtw.QComboBox()
        self.items = [STR_EROSION, STR_DILATATION, STR_OPENING, STR_CLOSING, STR_GAUSSIAN_BLURRING, STR_MEDIAN_BLUR,
                      STR_BILATERAL_FILTER, STR_EQUALIZATION, STR_SIMPLE_THRESHOLD, STR_ADAPTIVE_THRESHOLD,
                      STR_OTSUS_THRESHOLD, STR_FT, STR_OUTLINE_DETECTION]
        self.process_list.addItems(self.items)
        self.process_list.setFont(Qtg.QFont("Times", 12))  # Change font and font size

        # Creation of the layout containing the above widgets
        selection_layout = Qtw.QGridLayout()
        selection_layout.addWidget(self.process_list, 2, 0)
        selection_layout.addWidget(add_btn, 2, 1)
        selection_layout.addWidget(del_btn, 3, 0)
        selection_layout.addWidget(del_all_btn, 3, 1)
        selection_layout.addWidget(down_btn, 4, 0)
        selection_layout.addWidget(up_btn, 4, 1)

        layout = Qtw.QVBoxLayout()
        layout.addLayout(selection_layout)
        layout.addWidget(self.process_tree)
        layout.addWidget(calculate_btn)

        self.process_widget.setLayout(layout)
        self.process_dock.setWidget(self.process_widget)

        # The dockable widget is add the the main window
        self.addDockWidget(Qtc.Qt.LeftDockWidgetArea, self.process_dock)


        self.save_screenshot_btn = Qtw.QPushButton(STR_SAVE_SCREENSHOT)
        self.save_screenshot_btn.clicked.connect(self.save_screenshot)

        self.copy_screenshot_btn = Qtw.QPushButton(STR_COPY_TO_CLIPBOARD)
        self.copy_screenshot_btn.clicked.connect(self.copy_screenshot)

        self.video_qlabel = Qtw.QLabel()

        central_layout = Qtw.QGridLayout()
        central_layout.addWidget(self.video_qlabel, 0, 0, 1, 2)
        central_layout.addWidget(self.save_screenshot_btn, 2, 0)
        central_layout.addWidget(self.copy_screenshot_btn, 2, 1)
        central_widget = Qtw.QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        self.del_all_warning_window = WarningWidget(STR_WARNING_DEL_ALL_ITEM, cancel=True)
        #self.del_all_warning_window.ok_btn.clicked.connect(self.del_all_item)

    @Qtc.pyqtSlot()
    def save_screenshot(self):
        """Slot connected to the clicked signal of save_screenshot_button (QPushButton). It open a window for choosing
        a path and a file name """

        filename = Qtw.QFileDialog.getSaveFileName(self, STR_SAVE_IMAGE, '', STR_IMAGE_FORMAT)
        if filename[0] != "":
            cv2.imwrite(filename[0], self.shown_cv_img)

    @Qtc.pyqtSlot()
    def copy_screenshot(self):
        Qtw.QApplication.clipboard().setPixmap(convert_cv_to_qpixmap(self.shown_cv_img, None))

    @Qtc.pyqtSlot(np.ndarray)
    def update_video_qlabel(self, cv_img):
        """Slot connected to the new_cv_img_signal signal of GetVideoThread (QRadioBox). Updates the video_qlabel
        with a new opencv image from the camera """

        if self.calculating:
            self.output_img_list.clear()
            self.output_img_list.append(cv_img)

            iterator = Qtw.QTreeWidgetItemIterator(self.process_tree)

            while iterator.value():
                item = iterator.value()
                if not item.parent():
                    process = item.text(0)
                    self.sort_by_process(process, 'calculate', item)
                iterator += 1

            self.shown_cv_img = self.output_img_list[-1]


        else:
            self.shown_cv_img = cv_img

        qt_img = convert_cv_to_qpixmap(self.shown_cv_img, self.video_qlabel.size())
        self.video_qlabel.setPixmap(qt_img)

    @Qtc.pyqtSlot()
    def del_item(self):
        """
        Slot connected to del_btn

        Delete the currently selected item in the process TreeWidget (process_tree)

        :return: Nothing
        """
        index = self.process_tree.currentIndex()
        self.process_tree.takeTopLevelItem(index.row())

    @Qtc.pyqtSlot()
    def ask_del_all_item(self):
        """
        Slot conected to del_all_btn

        Delete all the items in the process TreeWidget (process_tree)

        :return: Nothing
        """
        top_item_count = self.process_tree.count_top_items()
        if top_item_count > 0:
            self.del_all_warning_window.show()
            is_ok = self.del_all_warning_window.exec()
            if is_ok:
                for i in range(top_item_count - 1, -1, -1):
                    self.process_tree.takeTopLevelItem(i)

    @Qtc.pyqtSlot()
    def del_all_item(self):
        """

        :return:
        """
        self.del_all_warning_window.close()
        top_item_count = self.process_tree.count_top_items()
        for i in range(top_item_count - 1, -1, -1):
            self.process_tree.takeTopLevelItem(i)

    @Qtc.pyqtSlot()
    def add_item(self):
        """
        Slot connected to add_btn

        Add in process_tree the process currently selected in process_list

        :return: Nothing
        """
        process = self.process_list.currentText()  # Name of the process
        self.sort_by_process(process, 'add')  # This will add the correct process and parameters in process_tree

    @Qtc.pyqtSlot()
    def up_item(self):
        """
        Slot connected to up_btn

        Move up the currently selected item in the process TreeWidget (process_tree)

        :return: Nothing
         """
        self.move_top_item(-1)

    @Qtc.pyqtSlot()
    def down_item(self):
        """
        Slot connect to down_btn
        Move down the currently selected item in the process TreeWidget (process_tree)

        :return: Nothing
        """
        self.move_top_item(1)

    @Qtc.pyqtSlot()
    def calculate(self):
        """
        Slot connect the calculate_btn

        :return: Nothing
        """

        self.calculating = not self.calculating




    def move_top_item(self, step):
        index = self.process_tree.currentIndex()
        item = self.process_tree.currentItem()
        top_items_count = self.process_tree.count_top_items()
        if index.isValid() and item.parent() is None and 0 <= index.row() + step < top_items_count:
            process = item.text(0)
            self.sort_by_process(process, 'move', item, index, step)
            self.process_tree.setCurrentItem(self.process_tree.topLevelItem(index.row()+step))

    def sort_by_process(self, process, mode, item=None, index=None, step=None):
        if process == STR_EROSION:
            if mode == 'move':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.erosion_item(index.row() + step, kernel_size, expanded)

            elif mode == 'add':
                self.process_tree.erosion_item(-1)

            elif mode == 'calculate':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()
                self.output_img_list.append(func_erosion(self.output_img_list[-1], kernel_size))

        elif process == STR_DILATATION:
            if mode == 'move':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.dilatation_item(index.row() + step, kernel_size, expanded)

            elif mode == 'add':
                self.process_tree.dilatation_item(-1)

            elif mode == 'calculate':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()
                self.output_img_list.append(func_dilatation(self.output_img_list[-1], kernel_size))

        elif process == STR_OPENING:
            if mode == 'move':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.opening_item(index.row() + step, kernel_size, expanded)

            elif mode == 'add':
                self.process_tree.opening_item(-1)

            elif mode == 'calculate':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()
                self.output_img_list.append(func_opening(self.output_img_list[-1], kernel_size))

        elif process == STR_CLOSING:
            if mode == 'move':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.closing_item(index.row() + step, kernel_size, expanded)

            elif mode == 'add':
                self.process_tree.closing_item(-1)

            elif mode == 'calculate':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()
                self.output_img_list.append(func_closing(self.output_img_list[-1], kernel_size))

        elif process == STR_GAUSSIAN_BLURRING:
            if mode == 'move':
                value1 = self.process_tree.itemWidget(item.child(0), 0).value()
                value2 = self.process_tree.itemWidget(item.child(1), 0).value()
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.gaus_blurring_item(index.row() + step, value1, value2, expanded)

            elif mode == 'add':
                self.process_tree.gaus_blurring_item(-1)

            elif mode == 'calculate':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()
                sigma = self.process_tree.itemWidget(item.child(1), 0).value()
                self.output_img_list.append(func_gaus_blurring(self.output_img_list[-1], kernel_size, sigma))

        elif process == STR_EQUALIZATION:
            if mode == 'move':
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.equalization_item(index.row() + step, expanded)

            elif mode == 'add':
                self.process_tree.equalization_item(-1)

            elif mode == 'calculate':
                self.output_img_list.append(func_equalization(self.output_img_list[-1]))

        elif process == STR_SIMPLE_THRESHOLD:
            if mode == 'move':
                value1 = self.process_tree.itemWidget(item.child(0), 0).value()
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.simple_thresholding_item(index.row() + step, value1, expanded)

            elif mode == 'add':
                self.process_tree.simple_thresholding_item(-1)

            elif mode == 'calculate':
                threshold = self.process_tree.itemWidget(item.child(0), 0).value()
                self.output_img_list.append(func_simple_thresholding(self.output_img_list[-1], threshold))


        elif process == STR_ADAPTIVE_THRESHOLD:
            if mode == 'move':
                value1 = self.process_tree.itemWidget(item.child(0), 0).currentIndex()
                value2 = self.process_tree.itemWidget(item.child(1), 0).value()
                value3 = self.process_tree.itemWidget(item.child(2), 0).value()
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.adaptive_thresholding_item(index.row() + step, value1, value2, value3, expanded)

            elif mode == 'add':
                self.process_tree.adaptive_thresholding_item(-1)

            elif mode == 'calculate':
                method = self.process_tree.itemWidget(item.child(0), 0).currentIndex()
                block_size = self.process_tree.itemWidget(item.child(1), 0).value()
                c = self.process_tree.itemWidget(item.child(2), 0).value()
                self.output_img_list.append(func_adaptive_thresholding(self.output_img_list[-1], method, block_size, c))

        elif process == STR_OTSUS_THRESHOLD:
            if mode == 'move':
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.otsu_thresholding_item(index.row() + step, expanded)

            elif mode == 'add':
                self.process_tree.otsu_thresholding_item(-1)

            elif mode == 'calculate':
                self.output_img_list.append(func_otsu_thresholding(self.output_img_list[-1]))

        elif process == STR_MEDIAN_BLUR:
            if mode == 'move':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()

                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.median_blurring_item(index.row() + step, kernel_size, expanded)

            elif mode == 'add':
                self.process_tree.median_blurring_item(-1)

            elif mode == 'calculate':
                kernel_size = self.process_tree.itemWidget(item.child(0), 0).value()
                self.output_img_list.append(func_median_blur(self.output_img_list[-1], kernel_size))

        elif process == STR_BILATERAL_FILTER:
            if mode == 'move':
                size = self.process_tree.itemWidget(item.child(0), 0).value()
                sigma = self.process_tree.itemWidget(item.child(1), 0).value()
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.bilateral_filtering_item(index.row() + step, size, sigma, expanded)

            elif mode == 'add':
                self.process_tree.bilateral_filtering_item(-1)

            elif mode == 'calculate':
                size = self.process_tree.itemWidget(item.child(0), 0).value()
                sigma = self.process_tree.itemWidget(item.child(1), 0).value()
                self.output_img_list.append(func_bilateral_filter(self.output_img_list[-1], size, sigma))

        elif process == STR_FT:
            if mode == 'move':
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.ft_item(index.row() + step, expanded)

            elif mode == 'add':
                self.process_tree.ft_item(-1)

            elif mode == 'calculate':
                self.output_img_list.append(func_ft(self.output_img_list[-1]))

        elif process == STR_OUTLINE_DETECTION:
            if mode == 'move':
                min_surface = self.process_tree.itemWidget(item.child(0), 0).value()
                expanded = item.isExpanded()

                self.process_tree.takeTopLevelItem(index.row())
                self.process_tree.outline_detection_item(index.row() + step, min_surface, expanded)

            elif mode == 'add':
                self.process_tree.outline_detection_item(-1)

            elif mode == 'calculate':
                min_surface = self.process_tree.itemWidget(item.child(0), 0).value()

                img = func_find_draw_contours(self.output_img_list[-1], min_surface)
                self.output_img_list.append(img)


    def resizeEvent(self, event):
        """Overriding the resizeEvent methode for resize the Qlabels containing image each time the main window
         is resized """
        Qtw.QMainWindow.resizeEvent(self, event)
        if self.shown_cv_img is not None:
            qt = convert_cv_to_qpixmap(self.shown_cv_img, self.video_qlabel.size())
            self.video_qlabel.setPixmap(qt)


class ParamSpinBox(Qtw.QSpinBox):
    def __init__(self, name, value, unit=STR_PX, mini=2, maxi=10, step=1):
        super().__init__()

        self.setAutoFillBackground(True)
        self.setMinimum(mini)
        self.setMaximum(maxi)
        self.setSingleStep(step)
        self.setPrefix(name)
        self.setSuffix(unit)
        self.setValue(value)


class ProcessTreeWidget(Qtw.QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setColumnWidth(0, 300)

    def erosion_item(self, index, value=5, expanded=False):
        erosion = Qtw.QTreeWidgetItem([STR_EROSION])

        erosion_kernel_size = Qtw.QTreeWidgetItem()
        erosion.addChild(erosion_kernel_size)

        if index == -1:
            self.addTopLevelItem(erosion)
        else:
            self.insertTopLevelItem(index, erosion)

        erosion.setExpanded(expanded)
        self.setItemWidget(erosion_kernel_size, 0, ParamSpinBox(STR_KERNEL_SIZE, value))

    def dilatation_item(self, index, value=5, expanded=False):
        dilatation = Qtw.QTreeWidgetItem([STR_DILATATION])

        dilatation_kernel_size = Qtw.QTreeWidgetItem()
        dilatation.addChild(dilatation_kernel_size)

        if index == -1:
            self.addTopLevelItem(dilatation)
        else:
            self.insertTopLevelItem(index, dilatation)

        dilatation.setExpanded(expanded)
        self.setItemWidget(dilatation_kernel_size, 0, ParamSpinBox(STR_KERNEL_SIZE, value))

    def opening_item(self, index, value=5, expanded=False):
        opening = Qtw.QTreeWidgetItem([STR_OPENING])

        opening_kernel_size = Qtw.QTreeWidgetItem()
        opening.addChild(opening_kernel_size)

        if index == -1:
            self.addTopLevelItem(opening)
        else:
            self.insertTopLevelItem(index, opening)

        opening.setExpanded(expanded)
        self.setItemWidget(opening_kernel_size, 0, ParamSpinBox(STR_KERNEL_SIZE, value))

    def closing_item(self, index, value=5, expanded=False):
        closing = Qtw.QTreeWidgetItem([STR_CLOSING])

        closing_kernel_size = Qtw.QTreeWidgetItem()
        closing.addChild(closing_kernel_size)

        if index == -1:
            self.addTopLevelItem(closing)
        else:
            self.insertTopLevelItem(index, closing)

        closing.setExpanded(expanded)
        self.setItemWidget(closing_kernel_size, 0, ParamSpinBox(STR_KERNEL_SIZE, value))

    def gaus_blurring_item(self, index, value1=5, value2=0, expanded=False):
        gaus_blurring = Qtw.QTreeWidgetItem([STR_GAUSSIAN_BLURRING])

        gaus_blurring_kernel_size = Qtw.QTreeWidgetItem()
        gaus_blurring.addChild(gaus_blurring_kernel_size)

        gaus_blurring_sigma = Qtw.QTreeWidgetItem()
        gaus_blurring.addChild(gaus_blurring_sigma)

        if index == -1:
            self.addTopLevelItem(gaus_blurring)
        else:
            self.insertTopLevelItem(index, gaus_blurring)

        gaus_blurring.setExpanded(expanded)
        self.setItemWidget(gaus_blurring_kernel_size, 0, ParamSpinBox(STR_KERNEL_SIZE, value1, mini=1, maxi=21, step=2))
        self.setItemWidget(gaus_blurring_sigma, 0, ParamSpinBox(STR_SIGMA, value2))

    def median_blurring_item(self, index, kernel_size=5, expanded=False):
        median_blurring = Qtw.QTreeWidgetItem([STR_MEDIAN_BLUR])

        median_blurring_kernel_size = Qtw.QTreeWidgetItem()
        median_blurring.addChild(median_blurring_kernel_size)

        if index == -1:
            self.addTopLevelItem(median_blurring)
        else:
            self.insertTopLevelItem(index, median_blurring)

        median_blurring.setExpanded(expanded)
        self.setItemWidget(median_blurring_kernel_size, 0, ParamSpinBox(STR_KERNEL_SIZE, kernel_size, mini=1,
                                                                        maxi=21, step=2))

    def bilateral_filtering_item(self, index, size=5, sigma=80, expanded=False):
        bilateral_filtering = Qtw.QTreeWidgetItem([STR_BILATERAL_FILTER])

        bilateral_filtering_size = Qtw.QTreeWidgetItem()
        bilateral_filtering.addChild(bilateral_filtering_size)

        bilateral_filtering_sigma = Qtw.QTreeWidgetItem()
        bilateral_filtering.addChild(bilateral_filtering_sigma)

        if index == -1:
            self.addTopLevelItem(bilateral_filtering)
        else:
            self.insertTopLevelItem(index, bilateral_filtering)

        bilateral_filtering.setExpanded(expanded)
        self.setItemWidget(bilateral_filtering_size, 0, ParamSpinBox(STR_FILTER_SIZE, size, mini=2, maxi=9))
        self.setItemWidget(bilateral_filtering_sigma, 0, ParamSpinBox(STR_SIGMA, sigma, mini=10, maxi=200, step=10))

    def equalization_item(self, index, expanded=False):
        equalization = Qtw.QTreeWidgetItem([STR_EQUALIZATION])

        if index == -1:
            self.addTopLevelItem(equalization)
        else:
            self.insertTopLevelItem(index, equalization)

        equalization.setExpanded(expanded)

    def simple_thresholding_item(self, index, value=127, expanded=False):
        simple_thresholding = Qtw.QTreeWidgetItem([STR_SIMPLE_THRESHOLD])

        simple_thresholding_threshold = Qtw.QTreeWidgetItem()
        simple_thresholding.addChild(simple_thresholding_threshold)

        if index == -1:
            self.addTopLevelItem(simple_thresholding)
        else:
            self.insertTopLevelItem(index, simple_thresholding)

        simple_thresholding.setExpanded(expanded)
        self.setItemWidget(simple_thresholding_threshold, 0, ParamSpinBox(STR_THRESHOLD, value,
                                                                          unit='', mini=0, maxi=255))

    def adaptive_thresholding_item(self, index, value1=0, value2=11, value3=2, expanded=False):
        adaptive_thresholding = Qtw.QTreeWidgetItem([STR_ADAPTIVE_THRESHOLD])

        adaptive_thresholding_method = Qtw.QTreeWidgetItem()
        adaptive_thresholding.addChild(adaptive_thresholding_method)

        adaptive_thresholding_method_list = Qtw.QComboBox()
        adaptive_thresholding_method_list.setAutoFillBackground(True)
        adaptive_thresholding_method_list.addItems([STR_MEAN, STR_GAUSSIAN])
        adaptive_thresholding_method_list.setCurrentIndex(value1)

        adaptive_thresholding_block_size = Qtw.QTreeWidgetItem()
        adaptive_thresholding.addChild(adaptive_thresholding_block_size)

        adaptive_thresholding_c = Qtw.QTreeWidgetItem()
        adaptive_thresholding.addChild(adaptive_thresholding_c)

        if index == -1:
            self.addTopLevelItem(adaptive_thresholding)
        else:
            self.insertTopLevelItem(index, adaptive_thresholding)

        adaptive_thresholding.setExpanded(expanded)
        self.setItemWidget(adaptive_thresholding_method, 0, adaptive_thresholding_method_list)
        self.setItemWidget(adaptive_thresholding_block_size, 0, ParamSpinBox(STR_BLOCK_SIZE, value2,
                                                                             mini=1, maxi=21, step=2))
        self.setItemWidget(adaptive_thresholding_c, 0, ParamSpinBox(STR_C, value3, mini=0, maxi=10))

    def otsu_thresholding_item(self, index, expanded=False):
        otsu_thresholding = Qtw.QTreeWidgetItem([STR_OTSUS_THRESHOLD])

        if index == -1:
            self.addTopLevelItem(otsu_thresholding)
        else:
            self.insertTopLevelItem(index, otsu_thresholding)

        otsu_thresholding.setExpanded(expanded)

    def ft_item(self, index, expanded=False):
        ft = Qtw.QTreeWidgetItem([STR_FT])

        if index == -1:
            self.addTopLevelItem(ft)
        else:
            self.insertTopLevelItem(index, ft)

        ft.setExpanded(expanded)

    def outline_detection_item(self, index, value=150, expanded=False):
        outline_detection = Qtw.QTreeWidgetItem([STR_OUTLINE_DETECTION])

        outline_detection_surface_min = Qtw.QTreeWidgetItem()
        outline_detection.addChild(outline_detection_surface_min)

        if index == -1:
            self.addTopLevelItem(outline_detection)
        else:
            self.insertTopLevelItem(index, outline_detection)

        outline_detection.setExpanded(expanded)
        self.setItemWidget(outline_detection_surface_min, 0, ParamSpinBox(STR_MIN_SURFACE, value,
                                                                          unit=STR_PIX2, mini=0, maxi=10000, step=50))

    def count_top_items(self):
        count = 0
        iterator = Qtw.QTreeWidgetItemIterator(self)  # pass your treewidget as arg
        while iterator.value():
            item = iterator.value()

            if item.parent():
                # if item.parent().isExpanded():
                #    count += 1
                pass
            else:
                # root item
                count += 1
            iterator += 1

        return count




