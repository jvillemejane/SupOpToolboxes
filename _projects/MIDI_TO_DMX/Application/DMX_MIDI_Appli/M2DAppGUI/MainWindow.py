## MIDI2DMX Application / byVillou.fr & LEnsE
#       Developed by Julien VILLEMEJANE
#       Creation date : 01/oct/2022
#
#       FILENAME :        AppGUI/MainWindow.py
#
#       DESCRIPTION :
#           Main graphical interface class.
#
#       NOTES :
#           These functions are a part of the MIDI2DMX application
#######################################################################

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")

        # Set the central widget of the Window.
        self.setCentralWidget(button)