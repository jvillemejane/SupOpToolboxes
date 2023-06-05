## MIDI2DMX Application / byVillou.fr & LEnsE
#       Developed by Julien VILLEMEJANE
#       Creation date : 01/oct/2022
#
#       FILENAME :        VisualisationDatabaseWidget.py
#
#       DESCRIPTION :
#           Graphic Interface (Widget) containing Spots Database
#           visualization.
#
#       NOTES :
#           These functions are a part of the MIDI2DMX application
#######################################################################


from PySide6.QtWidgets import *
from PySide6.QtGui import *
from M2DFiles.M2DFilesDatabase import *

class VisualisationDatabaseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.createDBTree()
        self.createDBMenu()
        self.createDBRightScreen()
        self.createMainLayout()

    def createDBTree(self):
        # Data Tree
        self.tree = QTreeWidget()
        self.tree = self.updateDataDB()
        self.confLayoutPrinc = QVBoxLayout()
        self.confLayoutPrinc.addWidget(self.tree)
        self.selmodel = self.tree.selectionModel()
        self.selmodel.selectionChanged.connect(self.handleSelection)

    def createDBRightScreen(self):
        # Right screen with data
        self.rightLayout = QGridLayout()
        # Projector BrandName
        self.brandNameLabel = QLabel("Brand Name")
        self.brandName = QLineEdit()
        self.brandName.setEnabled(False)
        self.rightLayout.addWidget(self.brandNameLabel, 0, 1)
        self.rightLayout.addWidget(self.brandName, 0, 2)
        # Projector Name
        self.projNameLabel = QLabel("Projector Name")
        self.projName = QLineEdit()
        self.projName.setEnabled(False)
        self.rightLayout.addWidget(self.projNameLabel, 0, 3)
        self.rightLayout.addWidget(self.projName, 0, 4)
        # Projector Type
        self.projTypeLabel = QLabel("Projector Type")
        self.projType= QLineEdit()
        self.projType.setEnabled(False)
        self.rightLayout.addWidget(self.projTypeLabel, 1, 1)
        self.rightLayout.addWidget(self.projType, 1, 2)
        # Projector Channels Number
        self.projChLabel = QLabel("Number of Channels")
        self.projCh = QLineEdit()
        self.projCh.setEnabled(False)
        self.rightLayout.addWidget(self.projChLabel, 1, 3)
        self.rightLayout.addWidget(self.projCh, 1, 4)
        # Label Mode
        self.modeLabel = QLabel("MODE / NO FUNCTION")
        self.modeLabel.setFixedHeight(30)
        self.modeLabel.setStyleSheet("background-color: darkgray;padding:5px;")
        self.rightLayout.addWidget(self.modeLabel, 2, 1, 1, 4)
        # Projector Mode Channel
        self.projModeLabel = QLabel("Mode Channel")
        self.projMode = QLineEdit()
        self.projMode.setEnabled(False)
        self.rightLayout.addWidget(self.projModeLabel, 3, 1)
        self.rightLayout.addWidget(self.projMode, 3, 2)
        # Projector No Function Value
        self.projNoFuncLabel = QLabel("Default Value (No Function)")
        self.projNoFunc = QLineEdit()
        self.projNoFunc.setEnabled(False)
        self.rightLayout.addWidget(self.projNoFuncLabel, 3, 3)
        self.rightLayout.addWidget(self.projNoFunc, 3, 4)
        # Label Dimmer
        self.modeLabel = QLabel("DIMMER")
        self.modeLabel.setStyleSheet("background-color: darkgray")
        self.rightLayout.addWidget(self.modeLabel, 4, 1, 1, 4)
        # Projector Dim Channel
        self.projDimLabel = QLabel("Dimmer Channel")
        self.projDim = QLineEdit()
        self.projDim.setEnabled(False)
        self.rightLayout.addWidget(self.projDimLabel, 5, 1)
        self.rightLayout.addWidget(self.projDim, 5, 2)
        # Projector Dim Min Value
        self.projDimMinLabel = QLabel("Minimum Value")
        self.projDimMin = QLineEdit()
        self.projDimMin.setEnabled(False)
        self.rightLayout.addWidget(self.projDimMinLabel, 5, 3)
        self.rightLayout.addWidget(self.projDimMin, 5, 4)
        # Projector Dim Max Value
        self.projDimMaxLabel = QLabel("Maximum Value")
        self.projDimMax = QLineEdit()
        self.projDimMax.setEnabled(False)
        self.rightLayout.addWidget(self.projDimMaxLabel, 6, 3)
        self.rightLayout.addWidget(self.projDimMax, 6, 4)
        # Label RGB
        self.RGBLabel = QLabel("COLORS CHANNELS")
        self.RGBLabel.setStyleSheet("background-color: darkgray")
        self.rightLayout.addWidget(self.RGBLabel, 7, 1, 1, 4)
        # Projector Red Channel
        self.projRedLabel = QLabel("Red")
        self.projRed = QLineEdit()
        self.projRed.setEnabled(False)
        self.rightLayout.addWidget(self.projRedLabel, 8, 1)
        self.rightLayout.addWidget(self.projRed, 8, 2)
        # Projector Green Channel
        self.projGreenLabel = QLabel("Green")
        self.projGreen = QLineEdit()
        self.projGreen.setEnabled(False)
        self.rightLayout.addWidget(self.projGreenLabel, 8, 3)
        self.rightLayout.addWidget(self.projGreen, 8, 4)
        # Projector Blue Channel
        self.projBlueLabel = QLabel("Blue")
        self.projBlue = QLineEdit()
        self.projBlue.setEnabled(False)
        self.rightLayout.addWidget(self.projBlueLabel, 9, 1)
        self.rightLayout.addWidget(self.projBlue, 9, 2)
        # Projector White Channel
        self.projWhiteLabel = QLabel("Green")
        self.projWhite = QLineEdit()
        self.projWhite.setEnabled(False)
        self.rightLayout.addWidget(self.projWhiteLabel, 9, 3)
        self.rightLayout.addWidget(self.projWhite, 9, 4)
        # Projector Amber Channel
        self.projAmberLabel = QLabel("Amber")
        self.projAmber = QLineEdit()
        self.projAmber.setEnabled(False)
        self.rightLayout.addWidget(self.projAmberLabel, 10, 1)
        self.rightLayout.addWidget(self.projAmber, 10, 2)
        # Projector UV Channel
        self.projUVLabel = QLabel("UV")
        self.projUV = QLineEdit()
        self.projUV.setEnabled(False)
        self.rightLayout.addWidget(self.projUVLabel, 10, 3)
        self.rightLayout.addWidget(self.projUV, 10, 4)

    def createDBMenu(self):
        # Top menu
        self.menuLayout = QHBoxLayout()
        self.menuUpdateDB = QPushButton("Read Database")
        self.menuUpdateDB.clicked.connect(self.updateDBVisu)
        self.menuLayout.addWidget(self.menuUpdateDB)
        self.menuUpdateProj = QPushButton("Update Projector Data")
        self.menuUpdateProj.clicked.connect(self.readDBVisu)
        self.menuLayout.addWidget(self.menuUpdateProj)


    def createMainLayout(self):
        # Global Layout
        self.globalLayout = QGridLayout()
        self.middleLayout = QHBoxLayout()
        self.middleLayout.addLayout(self.confLayoutPrinc, 0)
        self.middleLayout.addLayout(self.rightLayout, 0)
        self.globalLayout.addLayout(self.menuLayout, 1, 0)
        self.globalLayout.addLayout(self.middleLayout, 0, 0)
        self.setLayout(self.globalLayout)

    def updateDataDB(self):
        # Reading DataBase
        data = readDB()
        tree = QTreeWidget()
        tree.setColumnCount(2)
        tree.setHeaderLabels(["Name", "Projector", "Type", "#Channels"])
        # Tree database visualization
        items = []
        if(len(data) > -1):
            for brand, values in data.items():
                item = QTreeWidgetItem([brand])
                for value in values:
                    child = QTreeWidgetItem([value['BrandName'], value['ProjName'], value['ProjType'], value['TotalNbCh']])
                    item.addChild(child)
                items.append(item)
            tree.insertTopLevelItems(0, items)
        return tree

    def updateDBVisu(self, event):
        print("update")
        self.tree.clear()
        self.confLayoutPrinc.removeWidget(self.tree)
        self.tree = self.updateDataDB()
        self.confLayoutPrinc.addWidget(self.tree)
        self.selmodel = self.tree.selectionModel()
        self.selmodel.selectionChanged.connect(self.handleSelection)

    def handleSelection(self, selected):
        self.readDBVisu(selected)

    def readDBVisu(self, event):
        print("visu")
        proj = self.tree.selectedItems()
        if(proj):
            brand = proj[0].text(0)
            projName = proj[0].text(1)
            fileName = brand+"/"+projName+".adr"
            data = openDBFile(fileName)
            if(data):
                self.brandName.setText(data['BrandName'])
                self.projName.setText(data['ProjName'])
                self.projType.setText(data['ProjType'])
                self.projCh.setText(data['TotalNbCh'])
                if(data['DimmerCh'] == '0'):
                    self.projDim.setText("NONE")
                else:
                    self.projDim.setText(data['DimmerCh'])
                if(data['RedCh'] == '0'):
                    self.projRed.setText("NONE")
                else:
                    self.projRed.setText(data['RedCh'])
                if(data['GreenCh'] == '0'):
                    self.projGreen.setText("NONE")
                else:
                    self.projGreen.setText(data['GreenCh'])
                if(data['BlueCh'] == '0'):
                    self.projBlue.setText("NONE")
                else:
                    self.projBlue.setText(data['BlueCh'])
                if(data['WhiteCh'] == '0'):
                    self.projWhite.setText("NONE")
                else:
                    self.projWhite.setText(data['WhiteCh'])
                if(data['AmberCh'] == '0'):
                    self.projAmber.setText("NONE")
                else:
                    self.projAmber.setText(data['AmberCh'])
                if (data['UVCh'] == '0'):
                    self.projUV.setText("NONE")
                else:
                    self.projUV.setText(data['UVCh'])
