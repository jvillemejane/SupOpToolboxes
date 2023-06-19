# Libraries to import
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QAction
from CameraWidget import Camera_Widget
from ChartWidget import Chart_Widget

from SettingsWidget import Settings_Widget
from HistogramWidget import Histogram_Widget

#-------------------------------------------------------------------------------------------------------

class MainWidget(QWidget):
    """
    Main Widget of our Main Window.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    def __init__(self):
        """
        Initialisation of the main Widget.
        """
        super().__init__()


        # Chossing the optimate value for the measurement
        self.measurementInterval = 300

        # Tested values
        # 100  => 1.35s      |      325  => 1s
        # 250  => 1.25s      |      400  => 1.22s
        # 275  => 1.22s  ok  |      500  => 1.5s
        # 300  => 0.95s      |      1000 => 2s  

        # Create the several widgets
        self.cameraWidget = Camera_Widget()
        self.chartWidget = Chart_Widget(measurementInterval = self.measurementInterval)
        self.settingsWidget = Settings_Widget()
        self.cameraHistogramWidget = Histogram_Widget(histogramTitle = "Camera's histogram", FrameOrLists =  "frame", measurementInterval = self.measurementInterval)
        self.chartHistogramWidget = Histogram_Widget(histogramTitle = "Pixels' histogram", FrameOrLists ="lists", measurementInterval = self.measurementInterval)
        

        # Create and add the widgets into the layout
        layoutMain = QGridLayout()
        self.setLayout(layoutMain)

        layoutMain.addWidget(self.cameraWidget, 0, 0, 4, 4) # row = 0, column = 0, rowSpan = 4, columnSpan = 4
        layoutMain.addWidget(self.chartWidget, 0, 5, 2, 4) # row = 0, column = 5, rowSpan = 2, columnSpan = 4
        layoutMain.addWidget(self.cameraHistogramWidget, 2, 5, 2, 2) # row = 2, column = 5, rowSpan = 2, columnSpan = 2
        layoutMain.addWidget(self.chartHistogramWidget, 2, 7, 2, 2) # row = 2, column = 7, rowSpan = 2, columnSpan = 2

        
        self.cameraWidget.connectCamera()
        self.cameraWidget.launchVideo()

        self.initSettings()

        # lambda function used to prevent the Nonetype error
        self.cameraWidget.aoiButton.clicked.connect(lambda : self.cameraWidget.launchAOI(
                                                            self.settingsWidget.AOIXGetValue(),
                                                            self.settingsWidget.AOIYGetValue(),
                                                            self.settingsWidget.AOIWidthGetValue(),
                                                            self.settingsWidget.AOIHeightGetValue()
                                                            ))
                                                            
        self.settingsWidget.AOISettingX.slider.valueChanged.connect(lambda : self.cameraWidget.launchAOI(
                                                            self.settingsWidget.AOIXGetValue(),
                                                            self.settingsWidget.AOIYGetValue(),
                                                            self.settingsWidget.AOIWidthGetValue(),
                                                            self.settingsWidget.AOIHeightGetValue(),
                                                            type = "forced"))
        
        self.settingsWidget.AOISettingY.slider.valueChanged.connect(lambda : self.cameraWidget.launchAOI(
                                                            self.settingsWidget.AOIXGetValue(),
                                                            self.settingsWidget.AOIYGetValue(),
                                                            self.settingsWidget.AOIWidthGetValue(),
                                                            self.settingsWidget.AOIHeightGetValue(),
                                                            type = "forced"))
        
        self.settingsWidget.AOISettingWidth.slider.valueChanged.connect(lambda : self.cameraWidget.launchAOI(
                                                            self.settingsWidget.AOIXGetValue(),
                                                            self.settingsWidget.AOIYGetValue(),
                                                            self.settingsWidget.AOIWidthGetValue(),
                                                            self.settingsWidget.AOIHeightGetValue(),
                                                            type = "forced"))
        
        self.settingsWidget.AOISettingHeight.slider.valueChanged.connect(lambda : self.cameraWidget.launchAOI(
                                                            self.settingsWidget.AOIXGetValue(),
                                                            self.settingsWidget.AOIYGetValue(),
                                                            self.settingsWidget.AOIWidthGetValue(),
                                                            self.settingsWidget.AOIHeightGetValue(),
                                                            type = "forced"))

    def initSettings(self):
        """
        Method used to setup the settings.
        """
        self.settingsWidget.AOISettingX.slider.setMaximum(self.cameraWidget.max_width)
        self.settingsWidget.AOISettingX.slider.setValue(self.cameraWidget.max_width//4)

        self.settingsWidget.AOISettingY.slider.setMaximum(self.cameraWidget.max_height)
        self.settingsWidget.AOISettingY.slider.setValue(self.cameraWidget.max_height//4)

        self.settingsWidget.AOISettingWidth.slider.setMaximum(self.cameraWidget.max_width)
        self.settingsWidget.AOISettingWidth.slider.setValue(self.cameraWidget.max_width//2)

        self.settingsWidget.AOISettingHeight.slider.setMaximum(self.cameraWidget.max_height)
        self.settingsWidget.AOISettingHeight.slider.setValue(self.cameraWidget.max_height//2)

#-------------------------------------------------------------------------------------------------------

class MainWindow(QMainWindow):
    """
    Our main window.

    Args:
        QMainWindow (class): QMainWindow can contain several widgets.
    """
    def __init__(self):
        """
        Initialisation of the main Window.
        """
        super().__init__()

        # Variables
        self.oneOrFour = 4

        # Define Window title
        self.setWindowTitle("TP : Étude d'un capteur CMOS industriel")
        self.setGeometry(50, 50, 1200, 800)

        # Set the widget as the central widget of the window
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

        # Setting the toolbar's buttons and the toolbar itself
        quitButton = QPushButton("Quit")
        quitButton.clicked.connect(self.close)

        settingsButton = QPushButton("Settings")
        settingsButton.clicked.connect(self.mainWidget.settingsWidget.show)

        startButton = QPushButton("Start")
        startButton.clicked.connect(self.mainWidget.cameraHistogramWidget.startMethod)
        startButton.clicked.connect(self.mainWidget.chartHistogramWidget.startMethod)
        startButton.clicked.connect(self.mainWidget.chartWidget.startMethod)

        stopButton = QPushButton("Stop")
        stopButton.clicked.connect(self.mainWidget.cameraHistogramWidget.stopMethod)
        stopButton.clicked.connect(self.mainWidget.chartHistogramWidget.stopMethod)
        stopButton.clicked.connect(self.mainWidget.chartWidget.stopMethod)

        clearButton = QPushButton("Clear")
        clearButton.clicked.connect(self.mainWidget.chartWidget.clearMethod)

        oneOrFourButton = QPushButton("I / IV")
        oneOrFourButton.clicked.connect(self.changeOneOrFour)

        toolbarMainWindow = self.addToolBar("Toolbar")
        toolbarMainWindow.addWidget(quitButton)
        toolbarMainWindow.addWidget(settingsButton)

        # Add a separator between main's buttons and chart's button
        separator1 = QAction(self)
        separator1.setSeparator(True)
        toolbarMainWindow.addAction(separator1)

        toolbarMainWindow.addWidget(startButton)
        toolbarMainWindow.addWidget(stopButton)
        toolbarMainWindow.addWidget(clearButton)

        separator2 = QAction(self)
        separator2.setSeparator(True)
        toolbarMainWindow.addAction(separator2)
        toolbarMainWindow.addWidget(oneOrFourButton)

        # Launching the update methods
        self.mainWidget.cameraHistogramWidget.timerUpdate.timeout.connect(self.updateCameraHistogram)
        self.mainWidget.chartWidget.timerUpdate.timeout.connect(self.updateChart)
        self.mainWidget.chartHistogramWidget.timerUpdate.timeout.connect(self.updateChartHistogram)

    def updateCameraHistogram(self):
        """
        Update the camera's histogram with the new values.
        """
        # Get frame
        cameraFrame = self.mainWidget.cameraWidget.cameraFrame

        # Plot it
        self.mainWidget.cameraHistogramWidget.update(cameraFrame)

    def updateChartHistogram(self):
        """
        Update the chart's histogram with the new values.
        """
        # Get values
        ordinates = [self.mainWidget.chartWidget.ordinateAxis1,
                self.mainWidget.chartWidget.ordinateAxis2,
                self.mainWidget.chartWidget.ordinateAxis3,
                self.mainWidget.chartWidget.ordinateAxis4]
        
        # Plot it
        self.mainWidget.chartHistogramWidget.update(data = ordinates, numberOfPoints = self.oneOrFour)

    def updateChart(self):
        """
        Update the chart with the new values.
        """
        # Generate a data point
        newOrdinates = self.mainWidget.cameraWidget.getGraphValues()

        # Call the add_data_point method to add the new data point to the graph
        self.mainWidget.chartWidget.addOrdinatesPoints(ordinates = newOrdinates, numberOfPoints = self.oneOrFour)

    def changeOneOrFour(self):
        """
        Method used to change from the 4 points acquisition to the 1's one.
        """
        self.mainWidget.chartWidget.clearMethod()
        if self.oneOrFour == 4 :
            self.oneOrFour = 1

            # Print into the command prompt
            print(f"Acquisition : changed to {self.oneOrFour} point.")

        elif self.oneOrFour == 1:
            self.oneOrFour = 4

            # Print into the command prompt
            print(f"Acquisition : changed to {self.oneOrFour} points.")

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
