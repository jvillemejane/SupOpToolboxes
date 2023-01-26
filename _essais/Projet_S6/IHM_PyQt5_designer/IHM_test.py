# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 10:55:40 2023

@author: Villou
"""

from PyQt5.QtWidgets import (QWidget, QRadioButton, QHBoxLayout, QVBoxLayout,
                             QLabel, QApplication, QMainWindow)
from PyQt5.uic import loadUi
import sys

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("interface_graphique.ui", self)

def main():

    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()