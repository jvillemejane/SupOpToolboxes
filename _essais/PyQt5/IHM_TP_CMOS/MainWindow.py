# Libraries to import
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton
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

        # Create the several widgets
        self.cameraWidget = Camera_Widget()
        self.chartWidget = Chart_Widget(measurementInterval = 1000)
        self.settingsWidget = Settings_Widget()
        self.cameraHistogramWidget = Histogram_Widget(histogramTitle = "Camera's histogram", FrameOrLists =  "frame")
        self.chartHistogramWidget = Histogram_Widget(histogramTitle = "Pixels' histogram", FrameOrLists ="lists", measurementInterval = 1000)
        

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
        self.cameraWidget.aoiBt.clicked.connect(lambda : self.cameraWidget.launchAOI(
                                                            self.settingsWidget.AOIXGetValue(),
                                                            self.settingsWidget.AOIYGetValue(),
                                                            self.settingsWidget.AOIWidthGetValue(),
                                                            self.settingsWidget.AOIHeightGetValue()
                                                            ))
        self.settingsWidget.AOIRefreshButton.clicked.connect(lambda : self.cameraWidget.launchAOI(
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

        # Define Window title
        self.setWindowTitle("TP : Étude d'un capteur CMOS industriel")
        self.setGeometry(50, 50, 1600, 1000)

        # Set the widget as the central widget of the window
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

        # Setting the toolbar's buttons and the toolbar itself
        quitBt = QPushButton("Quit")
        quitBt.clicked.connect(self.close)

        settingsBt = QPushButton("Settings")
        settingsBt.clicked.connect(self.mainWidget.settingsWidget.show)

        startBt = QPushButton("Start")
        startBt.clicked.connect(self.mainWidget.cameraHistogramWidget.startFunction)
        startBt.clicked.connect(self.mainWidget.chartHistogramWidget.startFunction)
        startBt.clicked.connect(self.mainWidget.chartWidget.startFunction)

        stopBt = QPushButton("Stop")
        stopBt.clicked.connect(self.mainWidget.cameraHistogramWidget.stopFunction)
        stopBt.clicked.connect(self.mainWidget.chartHistogramWidget.stopFunction)
        stopBt.clicked.connect(self.mainWidget.chartWidget.stopFunction)

        toolbarMainWindow = self.addToolBar("Toolbar")
        toolbarMainWindow.addWidget(quitBt)
        toolbarMainWindow.addWidget(settingsBt)
        toolbarMainWindow.addWidget(startBt)
        toolbarMainWindow.addWidget(stopBt)

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
        self.mainWidget.chartHistogramWidget.update(ordinates)

    def updateChart(self):
        """
        Update the chart with the new values.
        """
        # Generate a data point
        newOrdinates = self.mainWidget.cameraWidget.getGraphValues()

        # Call the add_data_point method to add the new data point to the graph
        self.mainWidget.chartWidget.addOrdinatesPoints(newOrdinates)

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
