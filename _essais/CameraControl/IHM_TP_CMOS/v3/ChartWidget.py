# -*- coding: utf-8 -*-

# Libraries to import
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import time
import sys
import numpy

#-------------------------------------------------------------------------------------------------------

class Chart_Widget(QWidget):
    """
    Widget used to show the chart of 4 pixels' intensity over time.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """

    def __init__(self, measurementInterval = 100):
        """
        Initialisation of our chart widget.

        Args:
            measurementInterval (int, optional): Interval between two measures. Defaults to 100.
        """
        super().__init__()

        # Setting useful variables
        self.measurementIntervalActive = measurementInterval
        self.totalStopTime = 0
        self.beginningStopTime = 0
        self.endStopTime = 0
        self.startTime = 0

        # Initialisate lists
        self.ordinateAxis1 = []
        self.ordinateAxis2 = []
        self.ordinateAxis3 = []
        self.ordinateAxis4 = []
        self.abscissaAxis = []

        # Setting the timer
        self.timerUpdate = QTimer() #ms
        self.timerUpdate.setInterval(self.measurementIntervalActive)

        # Create the main layout
        layoutMain = QGridLayout()
        self.setLayout(layoutMain)

        # Create a PlotWidget from pyqtgraph to display the chart and add it to the main layout
        self.graph_widget = pg.PlotWidget(self, viewBox=pg.ViewBox(border=pg.mkPen(width=1, color='k')), enableMenu=False)

        # Create buttons for save and add it to the layout
        self.saveBt = QPushButton('Save', self)
        self.saveBt.clicked.connect(self.saveMethod)

        # Add the graph_widget and saveBt to the main layout
        layoutMain.addWidget(self.graph_widget, 0, 0, 9, 10)  # row = 0, column = 0, rowSpan = 10, columnSpan = 9
        layoutMain.addWidget(self.saveBt, 10, 3, 1, 4)  # row = 10, column = 3, rowSpan = 1, columnSpan = 4


        # Set up the initial chart
        self.graph_widget.setBackground('w')  # Set the background color
        self.graph_widget.setLabel('left', 'Intensity', color = "black")  # Set Y-axis label
        self.graph_widget.setLabel('bottom', 'Time (s)', color = "black")  # Set X-axis label
        self.graph_widget.setTitle("Pixels' chart", color = "black", size = "16pt") # Set the title
        self.graph_widget.showGrid(x = True, y = True)
        self.graph_widget.setYRange(0, 260)
        self.graph_widget.setXRange(0, 10)

    def addOrdinatesPoints(self, ordinates, numberOfPoints):
        print(f"Time used : {self.time()}")
        """
        Method used to add points to our chart.

        Args:
            ordinates (list): List of ordinates that will be plot witht the time.
        """
        # Call the class' time method to set the new abscissa
        newAbscissa = self.time()

        # Add the new abscissa and ordinates
        self.abscissaAxis.append(newAbscissa)

        if numberOfPoints == 1:
            self.ordinateAxis1.append(ordinates[0])
        else:
            self.ordinateAxis1.append(ordinates[0])
            self.ordinateAxis2.append(ordinates[1])
            self.ordinateAxis3.append(ordinates[2])
            self.ordinateAxis4.append(ordinates[3])
            

        # Set ranges, following on the abscissa, zooming on the ordinates
        if int(newAbscissa) >= 10 : 
            self.graph_widget.setXRange(newAbscissa - 10, newAbscissa, padding = 1)
        self.graph_widget.setYRange(self.minimumOrdinates(), self.maximumOrdinates())

        # Plot the data
        self.graph_widget.plot(self.abscissaAxis, self.ordinateAxis1, pen = pg.mkPen(width=2, color = 'red'))  # Plot the data
        self.graph_widget.plot(self.abscissaAxis, self.ordinateAxis2, pen = pg.mkPen(width=2, color = 'green'))  # Plot the data
        self.graph_widget.plot(self.abscissaAxis, self.ordinateAxis3, pen = pg.mkPen(width=2, color = 'blue'))  # Plot the data
        self.graph_widget.plot(self.abscissaAxis, self.ordinateAxis4, pen = pg.mkPen(width=2, color = 'black'))  # Plot the data

    def minimumOrdinates(self):
        """
        Method used to find the minimum of the ordinates. To zoom in after.

        Returns:
            float: minimum value of the ordinates, minus 0.5 if possible (for more visibility).
        """
        if self.ordinateAxis2 == []:
            minimum = min(self.ordinateAxis1[-20:])
        else:
            minimum = min(min(list[-20:]) for list in [self.ordinateAxis1, self.ordinateAxis2, self.ordinateAxis3, self.ordinateAxis4])
        if minimum >= 0.5:
            return minimum - 0.5
        return minimum
    
    def maximumOrdinates(self):
        """
        Method used to find the maximum of the ordinates. To zoom in after.

        Returns:
            float: maximum value of the ordinates, plus 0.5 if possible (for more visibility).
        """
        if self.ordinateAxis2 == []:
            maximum = max(self.ordinateAxis1[-20:])
        else:
            maximum = max(max(list[-20:]) for list in [self.ordinateAxis1, self.ordinateAxis2, self.ordinateAxis3, self.ordinateAxis4])
        if maximum <=259.5:
            return maximum + 0.5
        return maximum

    def time(self):
        """
        Method used to set the time compared to the beginning of the measures.

        Returns:
            float: time compared to the beginning of the measures.
        """
        return time.time() - self.startTime - self.totalStopTime

    def startMethod(self):
        """
        Method used to launch the update method.
        """
        if self.startTime == 0 :
            self.startTime = time.time()
            
            # Print into the command prompt
            print("Acquisition : started.")

        if not self.timerUpdate.isActive():
            self.timerUpdate.start()
            if self.beginningStopTime != 0:
                self.endStopTime = time.time()

                # Print into the command prompt
                print("Acquisition : re-started.")
            self.totalStopTime += self.endStopTime - self.beginningStopTime
        
    def stopMethod(self):
        """
        Method used to stop the update method.
        """
        self.timerUpdate.stop()
        self.beginningStopTime = time.time()

        # Print into the command prompt
        print("Acquisition : stopped.")

    def saveMethod(self):
        """
        Method used to save our ordinates and abscissas in a file called "IntensitiesOverTime.txt" under the following form :
            Time(s) pixel_1_intensity   pixel_2_intensity   pixel_3_intensity   pixel_4_intensity

        """
        # Combine the data lists into a single list for easier handling
        abcissas = self.abscissaAxis
        ordinates = [self.ordinateAxis1, self.ordinateAxis2, self.ordinateAxis3, self.ordinateAxis4]
        if self.ordinateAxis2 != []:
            abcissasOrdinates = [abcissas] + ordinates

            # Transpose the combined data to align the columns properly
            transposedAbcissasOrdinates = list(zip(*abcissasOrdinates))

            # Convert the transposed data to tab-separated strings
            formattedAbscissasOrdinates = ['\t'.join(map(str, row)) for row in transposedAbcissasOrdinates]

            # Write the formatted data to the .txt file
            with open("IntensitiesOverTimeFourPoints.txt", 'w') as file:
                header = "Time(s)\tpixel_1_intensity\tpixel_2_intensity\tpixel_3_intensity\tpixel_4_intensity"
                file.write(header + '\n')
                file.writelines('\n'.join(formattedAbscissasOrdinates))
            
            # Print into the command prompt
            print("Acquisiton : saved.")

        else:
            abcissasOrdinates = [abcissas] + [self.ordinateAxis1]

            # Transpose the combined data to align the columns properly
            transposedAbcissasOrdinates = list(zip(*abcissasOrdinates))

            # Convert the transposed data to tab-separated strings
            formattedAbscissasOrdinates = ['\t'.join(map(str, row)) for row in transposedAbcissasOrdinates]

            # Write the formatted data to the .txt file
            with open("IntensitiesOverTimeOnePoint.txt", 'w') as file:
                header = "Time(s)\tpixel_1_intensity"
                file.write(header + '\n')
                file.writelines('\n'.join(formattedAbscissasOrdinates))
            
            # Print into the command prompt
            print("Acquisiton : saved.")


    def clearMethod(self):
        """
        Method used to clear to do another acquisition
        """
        # Re-initialisation of main variables
        self.totalStopTime = 0
        self.beginningStopTime = 0
        self.endStopTime = 0
        self.startTime = 0

        if self.timerUpdate.isActive():
            self.startTime = time.time()

        # Re-initialisation of the lists
        self.ordinateAxis1 = []
        self.ordinateAxis2 = []
        self.ordinateAxis3 = []
        self.ordinateAxis4 = []
        self.abscissaAxis = []

        # Clear the chart and re-initialisate it
        self.graph_widget.clear()
        self.graph_widget.setYRange(0, 260)
        self.graph_widget.setXRange(0, 10)

        # Print into the command prompt
        print("Acquisition : cleared.")
        print("Acquisition : started.")

#-------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    App = QApplication(sys.argv)

    window = Chart_Widget()
    window.show()

    sys.exit(App.exec())
    