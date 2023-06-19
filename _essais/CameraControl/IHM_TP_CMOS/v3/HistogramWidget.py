# Libraries
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5.QtCore import QTimer
import sys
import pyqtgraph as pg
import numpy

class Histogram_Widget(QWidget):
    """
    Widget used to show histograms of array or list of lists.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """

    def __init__(self, histogramTitle, FrameOrLists, measurementInterval = 100):
        """
        Initialisation of our histogram.

        Args:
            histogramTitle (str): Title given to the histogram.
            FrameOrLists (str): "frame" or "lists", given to adapt the update method to the frame one 
                                    or to the lists of list one.
            measurementInterval (int, optional): Interval between two measures. Defaults to 100.
        """
        super().__init__()

        # Setting title
        self.setWindowTitle("PyQtGraph")

        # Setting important values as attributs
        self.measurementInterval = measurementInterval
        self.histogramTitle = histogramTitle
        self.FrameOrLists = FrameOrLists


        self.colors = ['red', 'blue', 'green', 'orange']

        # Calling sub-initialisation's method
        self.UiComponents()

        # Creating a timer
        self.timerUpdate = QTimer() #ms
        self.timerUpdate.setInterval(self.measurementInterval)

        # showing all the widgets
        self.show()

    def UiComponents(self):
        """
        Sub-initialisation's method.
        """
        # Creating a plot window
        self.plotChart = pg.plot()
        self.plotChart.setBackground("w")
        self.plotChart.setTitle(self.histogramTitle, color = "black", size = "12pt")
        self.plotChart.addLegend()

        # Create horizontal list i.e x-axis
        self.abscissas = range(257)

        # Creating a grid layout
        layoutMain = QGridLayout()

        # Setting this layout to the widget
        self.setLayout(layoutMain)

        # Plot window goes on right side, spanning 3 rows
        layoutMain.addWidget(self.plotChart, 0, 0, 1, 1) #row = 0, column = 0, rowSpan = 1, columnSpan = 1

    def calculateHistogram(self, values):
        """
        Method used to calculate an histogram from 0 to 256 (include) from a list.

        Args:
            values (list): list coonverted inot a histogram.

        Returns:
            list: histogram converted from the list.
        """
        histogram = [0] * 257  # Index 0 to 256

        for value in values:
            if 0 <= value <= 256:
                histogram[value] += 1

        return histogram

    def update(self, data, numberOfPoints = None):
        """
        Update method for the histogram.

        Args:
            data ("np.darray" or "list of lists"): frame or lists that will be ploted into a histogram.
        """
        # Erase the last histogram
        self.plotChart.clear()

        # Plot method for the frame
        if self.FrameOrLists == "frame":
            data = data.flatten()
            data = self.calculateHistogram(data)
            firstIndex, lastIndex = self.findFirstLastIndex(data)
            barGraph = pg.BarGraphItem(x = self.abscissas[firstIndex:lastIndex], height = data[firstIndex:lastIndex], width = 1, brush ='blue')
            self.plotChart.addItem(barGraph)

        # Plot method for the list of lists
        elif self.FrameOrLists == "lists":
            if numberOfPoints == 1:
                color = self.colors[0]
                histogram = self.calculateHistogram(data[0])
                firstIndex, lastIndex = self.findFirstLastIndex(histogram)
                barGraph = pg.BarGraphItem(x = self.abscissas[firstIndex:lastIndex], height = histogram[firstIndex:lastIndex], width = 0.6, brush = color, name = "Pixel n°" + str(1))
                self.plotChart.addItem(barGraph)

            else:
                for i, datum in enumerate(data):
                    color = self.colors[i]
                    histogram = self.calculateHistogram(datum)
                    firstIndex, lastIndex = self.findFirstLastIndex(histogram)
                    barGraph = pg.BarGraphItem(x = self.abscissas[firstIndex:lastIndex], height = histogram[firstIndex:lastIndex], width = 0.6, brush = color, name = "Pixel n°" + str(i + 1))
                    self.plotChart.addItem(barGraph)

    def findFirstLastIndex(self, list):
        """
        Method used to find the first and the last index between or the intersting values are <=> values != 0.

        Args:
            list (list): list studied.

        Returns:
            int: first and last interesting index.
        """
        first_index = None
        last_index = None
        
        for i in range(len(list)):
            if list[i] != 0:
                if first_index is None:
                    first_index = i
                last_index = i

        # I add +1 here to prevent the +1 everywhere else, since it is a list index ...
        return first_index, last_index + 1

    def startMethod(self):
        """
        Method used to launch the update method.
        """
        if not self.timerUpdate.isActive():
            self.timerUpdate.start()

    def stopMethod(self):
        """
        Method used to stop the update method.
        """
        if self.timerUpdate.isActive():
            self.timerUpdate.stop()

# Launching as main for tests
if __name__ == "__main__":
    App = QApplication(sys.argv)

    window = Histogram_Widget("Histogram Test", "lists")
    window.update([[0,0,0,0,1,1,1,2,2,3,4], [0,23,4,5,5,5,5,4,6,5,23]])

    sys.exit(App.exec())
