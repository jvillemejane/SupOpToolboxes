## MIDI2DMX Application / byVillou.fr & LEnsE
#       Developed by Julien VILLEMEJANE
#       Creation date : 01/oct/2022
#
#       FILENAME :        AddingToDatabaseWidget.py
#
#       DESCRIPTION :
#           Graphic Interface (Widget) containing Spots Database
#           adding functions, to complete the existing database.
#
#       NOTES :
#           These functions are a part of the MIDI2DMX application
#######################################################################

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from M2DFiles.M2DFilesDatabase import *


class AddingToDatabaseWidget(QWidget):
    def __init__(self, parent=None):
        super(AddingToDatabaseWidget, self).__init__(parent)
        self.confGridLayout = QGridLayout()
        # Projector BrandName
        self.brandNameLabel = QLabel("Brand Name *")
        self.brandName = QLineEdit()
        self.confGridLayout.addWidget(self.brandNameLabel, 0, 1)
        self.confGridLayout.addWidget(self.brandName, 0, 2)
        # Projector Name
        self.projNameLabel = QLabel("Projector Name *")
        self.projName = QLineEdit()
        self.confGridLayout.addWidget(self.projNameLabel, 0, 3)
        self.confGridLayout.addWidget(self.projName, 0, 4)
        # Projector Type
        self.projTypeLabel = QLabel("Projector Type *")
        self.projType = QComboBox()
        options = ["Lyre", "Scanner", "Par", "RGBAW-UV","Stroboscope"]
        for option in options:
            self.projType.addItem(option)
        self.confGridLayout.addWidget(self.projTypeLabel, 1, 1)
        self.confGridLayout.addWidget(self.projType, 1, 2)
        # Projector Channels Number
        self.projChLabel = QLabel("Number of Channels *")
        self.projCh = QLineEdit()
        self.confGridLayout.addWidget(self.projChLabel, 1, 3)
        self.confGridLayout.addWidget(self.projCh, 1, 4)
        # Label Mode
        self.modeLabel = QLabel("MODE / NO FUNCTION")
        self.modeLabel.setStyleSheet("background-color: darkgray")
        self.confGridLayout.addWidget(self.modeLabel, 2, 1, 1, 4)
        # Projector Mode Channel
        self.projModeLabel = QLabel("Mode Channel")
        self.projMode = QLineEdit()
        self.confGridLayout.addWidget(self.projModeLabel, 3, 1)
        self.confGridLayout.addWidget(self.projMode, 3, 2)
        # Projector No Function Value
        self.projNoFuncLabel = QLabel("Default Value (No Function)")
        self.projNoFunc = QLineEdit()
        self.confGridLayout.addWidget(self.projNoFuncLabel, 3, 3)
        self.confGridLayout.addWidget(self.projNoFunc, 3, 4)
        # Label Dimmer
        self.modeLabel = QLabel("DIMMER")
        self.modeLabel.setStyleSheet("background-color: darkgray")
        self.confGridLayout.addWidget(self.modeLabel, 4, 1, 1, 4)
        # Projector Dim Channel
        self.projDimLabel = QLabel("Dimmer Channel")
        self.projDim = QLineEdit()
        self.confGridLayout.addWidget(self.projDimLabel, 5, 1)
        self.confGridLayout.addWidget(self.projDim, 5, 2)
        # Projector Dim Min Value
        self.projDimMinLabel = QLabel("Minimum Value")
        self.projDimMin = QLineEdit()
        self.confGridLayout.addWidget(self.projDimMinLabel, 5, 3)
        self.confGridLayout.addWidget(self.projDimMin, 5, 4)
        # Projector Dim Max Value
        self.projDimMaxLabel = QLabel("Maximum Value")
        self.projDimMax = QLineEdit()
        self.confGridLayout.addWidget(self.projDimMaxLabel, 6, 3)
        self.confGridLayout.addWidget(self.projDimMax, 6, 4)
        # Label RGB
        self.RGBLabel = QLabel("COLORS CHANNELS")
        self.RGBLabel.setStyleSheet("background-color: darkgray")
        self.confGridLayout.addWidget(self.RGBLabel, 7, 1, 1, 4)
        # Projector Red Channel
        self.projRedLabel = QLabel("Red")
        self.projRed = QLineEdit()
        self.confGridLayout.addWidget(self.projRedLabel, 8, 1)
        self.confGridLayout.addWidget(self.projRed, 8,2)
        # Projector Green Channel
        self.projGreenLabel = QLabel("Green")
        self.projGreen = QLineEdit()
        self.confGridLayout.addWidget(self.projGreenLabel, 8, 3)
        self.confGridLayout.addWidget(self.projGreen, 8,4)
        # Projector Blue Channel
        self.projBlueLabel = QLabel("Blue")
        self.projBlue = QLineEdit()
        self.confGridLayout.addWidget(self.projBlueLabel, 9, 1)
        self.confGridLayout.addWidget(self.projBlue, 9, 2)
        # Projector White Channel
        self.projWhite = QLineEdit()
        self.projWhiteLabel = QLabel("White")
        self.projWhite = QLineEdit()
        self.confGridLayout.addWidget(self.projWhiteLabel, 9, 3)
        self.confGridLayout.addWidget(self.projWhite, 9, 4)
        # Projector Amber Channel
        self.projAmber = QLineEdit()
        self.projAmberLabel = QLabel("Amber")
        self.confGridLayout.addWidget(self.projAmberLabel, 10, 1)
        self.confGridLayout.addWidget(self.projAmber, 10, 2)
        # Projector UV Channel
        self.projUVLabel = QLabel("UV")
        self.projUV = QLineEdit()
        self.confGridLayout.addWidget(self.projUVLabel, 10, 3)
        self.confGridLayout.addWidget(self.projUV, 10, 4)

        self.buttonRun = QPushButton("Save to DB")
        self.buttonRun.clicked.connect(self.addToDB)

        self.confLayoutPrinc = QVBoxLayout()
        # self.confLayoutPrinc.addLayout(self.confLayout)
        self.confLayoutPrinc.addLayout(self.confGridLayout)
        self.confLayoutPrinc.addWidget(self.buttonRun)

        self.setLayout(self.confLayoutPrinc)

    def testBeforeDB(self, text, dataIn, error):
        if(text != ""):
            dataIn.append(text)
        else:
            error+=1
        return error


    def addToDB(self):
        fileName = self.brandName.text()+"/"+self.projName.text()
        dataIn = []
        errorDB = 0
        errorDB = self.testBeforeDB(self.brandName.text(), dataIn, errorDB)
        errorDB = self.testBeforeDB(self.projName.text(), dataIn, errorDB)
        errorDB = self.testBeforeDB(self.projType.currentText(), dataIn, errorDB)
        errorDB = self.testBeforeDB(self.projCh.text(), dataIn, errorDB)
        dataIn.append(self.projMode.text())
        dataIn.append(self.projNoFunc.text())
        dataIn.append(self.projDim.text())
        dataIn.append(self.projDimMin.text())
        dataIn.append(self.projDimMax.text())
        dataIn.append(self.projRed.text())
        dataIn.append(self.projGreen.text())
        dataIn.append(self.projBlue.text())
        dataIn.append(self.projWhite.text())
        dataIn.append(self.projAmber.text())
        dataIn.append(self.projUV.text())
        if(errorDB == 0):
            print("DB Ok")
            writeDBFile(fileName, dataIn)
        else:
            print("All the required value must be filled !")

