# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 20:05:24 2023

@author: Villou
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PyQt5.QtGui import QColor

class ResizableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resizable Interface")
        self.resize(800, 600)

        # Create the main layout
        self.grid_layout = QGridLayout()

        # Set the central column size policy
        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 2)
        self.grid_layout.setColumnStretch(2, 1)

        # Set the row stretch for each column
        for i in range(2):
            self.grid_layout.setRowStretch(i, 1)
        for i in range(2, 7):
            self.grid_layout.setRowStretch(i, 1)
            self.grid_layout.setRowStretch(i + 5, 1)

        # Create widgets for each cell
        cells = [
            (0, 0, QColor("lightblue")),   # Left column, row 1
            (1, 0, QColor("lightgreen")),  # Left column, row 2
            (0, 1, QColor("lightyellow")), # Central column, row 1
            (1, 1, QColor("lightgray")),   # Central column, row 2
            (0, 2, QColor("lightpink")),   # Right column, row 1
            (1, 2, QColor("lightcyan"))    # Right column, row 2
        ]

        for row, col, color in cells:
            widget = QWidget()
            widget.setStyleSheet(f"background-color: {color.name()};")
            self.grid_layout.addWidget(widget, row, col)

        for i in range(2, 7):
            left_widget = QWidget()
            left_widget.setStyleSheet("background-color: lightblue;")
            self.grid_layout.addWidget(left_widget, i, 0)  # Left column, rows 3-7

            right_widget = QWidget()
            right_widget.setStyleSheet("background-color: lightpink;")
            self.grid_layout.addWidget(right_widget, i, 2)  # Right column, rows 3-7

        # Create the central widget and set the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.grid_layout)

        # Set the central widget for the main window
        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ResizableWindow()
    window.show()
    sys.exit(app.exec_())