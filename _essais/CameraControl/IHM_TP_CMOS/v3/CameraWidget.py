# -*- coding: utf-8 -*-

#   Libraries to import
# Camera
from pyueye import ueye
import camera

# Graphical interface
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout, QComboBox, QSlider, QLineEdit
    )
from PyQt5.QtGui import QPixmap, QImage
from SettingsWidget import Setting_Widget_Int

# Standard
import numpy as np
import cv2
import sys
import math

from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget, QGroupBox
from PyQt5.QtCore import QTimer, Qt

#-----------------------------------------------------------------------------------------------

class Camera_Widget(QWidget):
    """
    Widget used to show our camera.
    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """

    def __init__(self, colormode = "MONO8"):
        """
        Initialisation of our camera widget.
        """
        super().__init__(parent=None)

        # Camera
        self.camera = None
        self.max_width = 0
        self.max_height = 0
        self.colormode = colormode


        # Graphical interface
        self.cameraInfo = QLabel("Camera Info")
        self.cameraListCombo = QComboBox()
        self.initListCamera()

        self.refreshBt = QPushButton("Launch Video")
        self.refreshBt.clicked.connect(self.launchVideo)

        self.connectBt = QPushButton("Connect")
        self.connectBt.clicked.connect(self.connectCamera)

        self.cameraDisplay = QLabel()
        self.cameraDisplay.setAlignment(Qt.AlignCenter)

        self.aoiTrueFalse = False
        self.aoiButton = QPushButton("AOI")

        # Create a self.layout and add widgets
        self.layout = QGridLayout()

        self.layout.addWidget(self.aoiButton, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1
        self.layout.addWidget(self.cameraDisplay, 1, 0, 4, 4) # row = 1, column = 0, rowSpan = 4, columnSpan = 4
        self.layout.addWidget(self.refreshBt, 5, 2, 1, 2) # row = 5, column = 2, rowSpan = 1, columnSpan = 2
        self.layout.addWidget(self.connectBt, 5, 0, 1, 2) # row = 5, column = 0, rowSpan = 1, columnSpan = 2

        self.setLayout(self.layout)

        # Other variables
        self.timerUpdate = QTimer()
        self.frameWidth = self.cameraDisplay.width()
        self.frameHeight = self.cameraDisplay.height()

    def launchVideo(self):
        """
        Method used to launch the video.
        """
        self.timerUpdate.setInterval(int(self.camera.get_frame_rate()))
        self.timerUpdate.timeout.connect(self.refreshGraph)
        self.timerUpdate.start()    

    def refreshGraph(self):
        """
        Method used to refresh the graph for the image display.
        """
        self.cameraArray = self.camera.get_image()

        AOIX, AOIY, AOIWidth, AOIHeight = self.camera.get_aoi()
        self.cameraFrame = np.reshape(self.cameraArray, (AOIHeight, AOIWidth, -1))
        self.cameraFrame = cv2.resize(self.cameraFrame, dsize = (self.frameWidth, self.frameHeight), interpolation = cv2.INTER_CUBIC)

        # Convert the frame into an image
        image = QImage(self.cameraFrame, self.cameraFrame.shape[1], self.cameraFrame.shape[0], self.cameraFrame.shape[1], QImage.Format_Indexed8)
        pmap = QPixmap(image)

        # Resize the Qpixmap at the great size
        widgetWidth, widgetHeight = self.widgetGeometry()
        pmap = pmap.scaled(widgetWidth, int(widgetHeight*5/9), Qt.KeepAspectRatio)
        
        # "plot" it in the cameraDisplay
        self.cameraDisplay.setPixmap(pmap)

    def initListCamera(self):
        """
        Method used to initialize the different cameras linked to the computer.
        """
        self.nb_cam = camera.get_nb_of_cam()
        self.cameraInfo.setText('Cam Nb = '+str(self.nb_cam))
        if(self.nb_cam > 0):
            self.cameraList = camera.get_cam_list() 
            self.cameraListCombo.clear()
            for i in range(self.nb_cam):
                cam = self.cameraList[i]
                self.cameraListCombo.addItem(f'{cam[2]} (SN : {cam[1]})')

    def widgetGeometry(self):
        """
        Method use to get the width and the height of the widget.

        Returns:
            int: widget's width and height.
        """
        geometry = self.geometry()
        widgetWidth = geometry.width()
        widgetHeight = geometry.height()
        #print(f"height = {height}; width = {width}")
        return widgetWidth, widgetHeight

    def connectCamera(self):
        """
        Method used to connect the camera.
        """
        self.connectBt.setEnabled(False)
        self.refreshBt.setEnabled(True)
        self.connectBt.setText('Connected')
        
        self.selectedCamera = self.cameraListCombo.currentIndex()
        self.camera = camera.uEyeCamera(self.selectedCamera)
        
        self.max_width = int(self.camera.get_sensor_max_width())
        self.max_height = int(self.camera.get_sensor_max_height())

        self.camera.set_exposure(15)
        
        if self.colormode == "MONO8":
            self.camera.set_colormode(ueye.IS_CM_MONO8)
        else : 
            try : self.camera.set_colormode(ueye.IS_CM_SENSOR_RAW10)
            except camera.uEye_ERROR: 
                print("ueye.IS_CM_SENSOR_RAW10 unavailable")
                try : self.camera.set_colormode(ueye.IS_CM_SENSOR_RAW12)
                except camera.uEye_ERROR: 
                    print("ueye.IS_CM_SENSOR_RAW12 unavailable")
                    try : self.camera.set_colormode(ueye.IS_CM_MONO8)
                    except camera.uEye_ERROR: print("ueye.IS_CM_MONO8 unavailable.")

        print(f"Nombre de bits par pixels : {self.camera.nBitsPerPixel}")
        
        self.camera.set_aoi(0, 0, self.max_width-1, self.max_height-1)

        self.camera.alloc()
        self.camera.capture_video()

        # There is a way to set the initial minimumValue of the exposure as near as possible from the original minimumValue of the
        # camera, for any camera

        # Setting exposure setting
        self.exposureSetting = Setting_Widget_Float(" Exposure ", self.generateExpositionRangeList(10000))
        self.exposureSetting.value = self.camera.get_exposure()
        self.exposureSetting.setValue(self.exposureSetting.value)

        # Use lambda function to avoid the Nonetype error when it's not define yet
        self.exposureSetting.slider.valueChanged.connect(lambda : self.camera.set_exposure(self.exposureSetting.value))

        # Setting blacklevel setting
        self.blacklevel = int(self.camera.get_black_level())
        self.blacklevelSetting = Setting_Widget_Int(" Blacklevel ", minimumValue = 0, maximumValue = 256, initialisationValue = self.blacklevel)
        
        # Same for lambda function
        self.blacklevelSetting.slider.valueChanged.connect(lambda : self.camera.set_black_level(self.blacklevelSetting.getValue()))

        self.layout.addWidget(self.exposureSetting, 6, 0, 3, 4) # row = 6, column = 0, rowSpan = 3, columnSpan = 4
        self.layout.addWidget(self.blacklevelSetting, 9, 0, 3, 4) # row = 9, column = 0, rowSpan = 3, columnSpan = 4
        self.setLayout(self.layout)
        self.refreshGraph()

    def generateExpositionRangeList(self, pointsNumber):
        """
        Method used to create a list of pointsNumber points in the range of the camera's exposition.

        Args:
            nombrePoints (int): number of points possible in the range.

        Returns:
            list: list of points in the range of the camera's exposure.
        """
        (expositionRangeMinimum, expositionRangeMaximum) = self.camera.get_exposure_range()
        return np.linspace(expositionRangeMinimum+0.01, expositionRangeMaximum, pointsNumber) 

    def closeApp(self):
        """
        Method used to close the App.
        """
        self.close()
        self.closeEvent(None)

    def closeEvent(self, event):
        """
        Method used to close an event.

        Args:
            event (_???_): ???
        """
        if(self.camera != None):
            self.camera.stop_camera()
        QApplication.quit()

    def getGraphValues(self):
        """
        Method used to return the value of 4 points near the center of the frame.

        Returns:
            list: list of the value of the four points.
        """
        value1 = self.cameraFrame[self.frameWidth // 2 + 10][self.frameHeight // 2]
        value2 = self.cameraFrame[self.frameWidth // 2 - 10][self.frameHeight // 2]
        value3 = self.cameraFrame[self.frameWidth // 2][self.frameHeight // 2 + 10]
        value4 = self.cameraFrame[self.frameWidth // 2][self.frameHeight // 2 - 10]
        if self.camera.nBitsPerPixel == 8 :
            return [value1, value2, value3, value4]
        if self.camera.nBitsPerPixel == 16 :
            return [value1[0], value2[0], value3[0], value4[0]]
        if self.camera.nBitsPerPixel == 24 :
            return[sum(value1) // 3, sum(value2) // 3, sum(value3) // 3, sum(value4) // 3]

    def launchAOI(self, AOIX, AOIY, AOIWidth, AOIHeight, type = None):
        """
        Method used to launch the AOI.
        I know it is not optimised, but that avoid a bug where the image is in black when students are changing the setting
        values without being in AOI mode.
        """
        if not self.aoiTrueFalse and type == "forced":
            pass
        else:
            # Do Forced / Do Unforced / Undo AOI Mode

            # "Pause" refresh
            self.timerUpdate.stop()

            # Stop video and un_alloc memory # Merci M Villemejane
            self.camera.stop_video()
            self.camera.un_alloc()

            if self.aoiTrueFalse and type == "forced":

                # Setting the AOI
                self.camera.set_aoi(AOIX, AOIY, AOIWidth, AOIHeight)

            elif not self.aoiTrueFalse and type == None:

                # Setting the AOI
                self.camera.set_aoi(AOIX, AOIY, AOIWidth, AOIHeight)
                self.aoiTrueFalse = True 
                print("--- AOI Active ---") 

            elif self.aoiTrueFalse and type == None:

                # Stop AOI
                self.camera.set_aoi(0, 0, self.max_width, self.max_height)
                self.aoiTrueFalse = False 
                print("--- Whole Camera ---")
                
            # Re-alloc memory and re-run video
            self.camera.alloc()
            self.camera.capture_video()

            # Restart the refresh
            self.timerUpdate.setInterval(int(self.camera.get_frame_rate()))
            self.timerUpdate.start()

#-----------------------------------------------------------------------------------------------

class Setting_Widget_Float(QWidget):
    """
    Widget designed to select a value in a list.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self, selectionLabel, floatListToSelect):
        """
        Initialiszation of the widget.

        Args:
            selectionLabel (str): name given to the box and to the unit.
            floatListToSelect (list): list that will be described by the slider.
        """
        super().__init__()
        self.floatListToSelect = floatListToSelect
        self.selectionLabel = selectionLabel
        self.value = 0.01
        self.initUI()

    def initUI(self):
        """
        Sub-initialization method
        """
        group_box = QGroupBox(self.selectionLabel)
        layout = QGridLayout()

        # Create a layout
        line_label_layout = QGridLayout()

        # Create a line widget and place it into the grid layout
        self.line = QLineEdit(self)
        line_label_layout.addWidget(self.line, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 1
        self.line.textChanged.connect(self.linetextValueChanged)

        # Create a label widget and place it into the grid layout
        self.labelValue = QLabel()
        line_label_layout.addWidget(self.labelValue, 0, 1, 1, 1) # row = 0, column = 1, rowSpan = 1, columnSpan = 1

        # Create a slider widget and place it into the grid layout
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, len(self.floatListToSelect) - 1)
        self.slider.valueChanged.connect(self.sliderValueChanged)

        layout.addWidget(self.slider, 0, 0, 1, 4) # row = 0, column = 0, rowSpan = 1, columnSpan = 4
        layout.addLayout(line_label_layout, 1, 0, 1, 4) # row = 1, column = 0, rowSpan = 1, columnSpan = 4

        group_box.setLayout(layout)

        main_layout = QGridLayout()
        main_layout.addWidget(group_box, 0, 0, 1, 1) # row = 0, column = 0, rowSpan = 1, columnSpan = 0 <=> QHBoxLayout or V
        self.setLayout(main_layout)

    def sliderValueChanged(self, value):
        """
        Method used to set the self.value and and the labelValue text each time the slider is triggered.

        Args:
            value (float): useful value of the slider.
        """
        self.value = self.floatListToSelect[value]
        self.labelValue.setText(self.selectionLabel + "= "+ str(math.floor(self.value * 100) / 100))

    def linetextValueChanged(self, text):
        """
        Method used to set the self.value, self and the labelValue text each time the line is triggered.

        Args:
            text (str): string that'll be converted in float to changed the important values.
        """
        self.value = float(text)
        self.labelValue.setText(self.selectionLabel + str(math.floor(float(text) * 100) / 100))
        self.setValue(float(text))
    
    def setValue(self, value):
        """
        Method used to set the value of the slider without using a long line each time.
        It sets the nearest value present in the list from the real value to the slider.

        Args:
            value (float): near value that will be put.
        """
        self.slider.setValue(np.argmin(np.abs(self.floatListToSelect - value)))

#-----------------------------------------------------------------------------------------------

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Window")
        self.setGeometry(100, 100, 400, 300)

        widget = Camera_Widget()
        self.setCentralWidget(widget)

#-----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec_())
