## MIDI2DMX Application / byVillou.fr & LEnsE
#       Developed by Julien VILLEMEJANE
#       Creation date : 08/oct/2022
#
#       FILENAME :        M2DGraphElements.py
#
#       DESCRIPTION :
#           Graphic Elements (Widget) to include in QTabWidget or QMainWindow
#           visualization.
#
#       NOTES :
#           These functions are a part of the MIDI2DMX application
#######################################################################


from PySide6.QtWidgets import *
from PySide6.QtGui import *

class QAskCombo():
    def __init__(self, label, layout, line, col=1):
        self.labelAskCombo = QLabel(label)
        self.labelAskCombo.setFixedHeight(30)
        self.labelAskCombo.setStyleSheet("background-color: darkgray; padding:5px; color:white;")
        self.comboAsk = QComboBox()
        self.layout = layout
        self.layout.addWidget(self.labelAskCombo, line, col)
        self.layout.addWidget(self.comboAsk, line, col+1)

    def getCombo(self):
        return self.labelAskCombo

    def setComboItems(self, items):
        self.comboAsk.addItems(items)

    def clearCombo(self):
        self.comboAsk.clear()

    def getComboText(self):
        return self.comboAsk.currentText()


class QAskLine():
    def __init__(self, label, layout, line, col=1):
        self.labelAskLine = QLabel(label)
        self.labelAskLine.setFixedHeight(30)
        self.lineAsk = QLineEdit()
        self.layout = layout
        self.layout.addWidget(self.labelAskLine, line, col)
        self.layout.addWidget(self.lineAsk, line, col+1)

    def getLineText(self):
        return self.lineAsk.text()


class QInfoLine():
    def __init__(self, label, layout, line, col=1):
        self.labelInfoLine = QLabel(label)
        self.labelInfoLine.setFixedHeight(30)
        self.labelInfoLine.setStyleSheet("background-color: darkgray;padding:5px;color:white")
        self.lineInfo = QLineEdit("0")
        self.lineInfo.setEnabled(False)
        self.lineInfo.setStyleSheet("background-color: white;color:black")
        self.layout = layout
        self.layout.addWidget(self.labelInfoLine, line, col)
        self.layout.addWidget(self.lineInfo, line, col+1)

    def getLineText(self):
        return self.lineInfo.text()

    def setLineText(self, text):
        self.lineInfo.setText(text)


class QTitle():
    def __init__(self, label, layout, line):
        self.titleLabel = QLabel(label)
        self.titleLabel.setFixedHeight(30)
        self.titleLabel.setStyleSheet("background-color: darkgray; padding:5px; font-weight:bold;")
        self.layout = layout
        self.layout.addWidget(self.titleLabel, line, 1, 1, 4)


class QLongSlider():
    def __init__(self, label, layout, line, fctChanged, min=0, max=255):
        self.sliderLabel = QLabel(label)
        self.sliderLabel.setFixedHeight(30)
        self.sliderLabel.setStyleSheet("background-color: darkgray; padding:5px; color:white;")
        self.layout = layout
        self.layout.addWidget(self.sliderLabel, line, 1)
        self.longSlider = QSlider(Qt.Horizontal)
        self.longSlider.setFixedHeight(30)
        self.longSlider.valueChanged.connect(fctChanged)
        self.longSlider.setTickInterval(5)
        self.longSlider.setTickPosition(QSlider.TicksBelow)
        self.longSlider.setMinimum(min)
        self.longSlider.setMaximum(max)
        self.layout = layout
        self.layout.addWidget(self.longSlider, line, 2, 1, 3)

    def getSliderValue(self):
        return self.longSlider.value()


class QSmallSlider():
    def __init__(self, label, layout, line, fctChanged, min=0, max=255):
        self.sliderLabel = QLabel(label)
        self.sliderLabel.setFixedHeight(30)
        self.sliderLabel.setStyleSheet("background-color: darkgray; padding:5px; color:white;")
        self.sliderValue = QLabel("0")
        self.sliderValue.setStyleSheet("background-color: white; color:black;")
        self.layout = layout
        self.layout.addWidget(self.sliderLabel, line, 1)
        self.layout.addWidget(self.sliderValue, line, 2)
        self.smallSlider = QSlider(Qt.Horizontal)
        self.smallSlider.setFixedHeight(30)
        self.smallSlider.valueChanged.connect(fctChanged)
        self.smallSlider.setTickInterval(5)
        self.smallSlider.setTickPosition(QSlider.TicksBelow)
        self.smallSlider.setMinimum(min)
        self.smallSlider.setMaximum(max)
        self.layout.addWidget(self.smallSlider, line, 3, 1, 2)

    def setLineText(self, text):
        self.sliderValue.setText(text)

    def getSliderValue(self):
        return self.smallSlider.value()
