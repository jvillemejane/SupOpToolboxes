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
from M2DGraphElements.M2DGraphElements import *
import serial
import serial.tools.list_ports



class DirectUSBUniqueSpotWidget(QWidget):
    def __init__(self, parent, mainTabWidget):
        """
        Direct USB Unique Spot control widget
        :param parent: mainWindow of the application
        :param mainTabWidget: tab widget containing the Direct USB Unique Spot Widget
        """
        super().__init__()
        self.parent = parent
        self.mainTabWidget = mainTabWidget
        self.ports_com = []
        self.createDBTree()
        self.createDBMenu()
        self.createDBRightScreen()
        self.createMainLayout()
        self.mainTabWidget.currentChanged.connect(self.directUSBChangedTab)
        self.projSelected = False
        self.projData = dict()

    def isProjSelected(self):
        return self.projSelected

    def directUSBChangedTab(self, i):
        """
        Call when Direct USB Control tab opened
        :param i: tab number
        :return:
        """
        if(self.mainTabWidget.tabText(i) == "Direct USB Control"):
            self.createPortList()

    def createDBTree(self):
        """
        Create the data tree of spots based on files in the database directory
        :return:
        """
        # Data Tree
        self.tree = QTreeWidget()
        self.tree = self.updateDataDB()
        self.confLayoutPrinc = QVBoxLayout()
        self.confLayoutPrinc.addWidget(self.tree)
        self.selmodel = self.tree.selectionModel()
        self.selmodel.selectionChanged.connect(self.handleSelection)

    def connectionAction(self):
        """
        Connect the Nucleo board via USB Serial Port
        Update the graphical element linked to the connection process (Connection button and Send Data button)
        :return:
        """
        if(self.parent.isNucleoConnected() == False):
            self.parent.setNucleoPort(self.serialLabel.getComboText())
            if(True):   # self.parent.getNucleoPort() != ""):
                self.parent.connectSerialNucleo()
                self.nucleoConnectionButton.setText("Disconnect")
                self.parent.setNucleoConnected(True)
                self.menuUpdateProj.setEnabled(True)
            else:
                print("Error Connection - No Port Selected")
        else:
            self.nucleoConnectionButton.setText("Connexion to Nucleo")
            self.parent.disconnectSerialNucleo()
            self.parent.setNucleoConnected(False)
            self.menuUpdateProj.setEnabled(False)

    def changeSlider(self, event):
        """
        Call when a slider value changed and update all the labels on the graphical interface
        :param event:
        :return:
        """
        value = self.dimmerSlider.getSliderValue()
        self.dimmerGlobal.setLineText(str(value))
        value = self.redSlider.getSliderValue()
        self.redSlider.setLineText(str(value))
        value = self.greenSlider.getSliderValue()
        self.greenSlider.setLineText(str(value))

    def createPortList(self):
        """
        Create Serial Port List of STM devices

        :return:
        void function
        fill items of Combobox for Serial Port Selection
        """
        # Serial Port list and connection
        self.ports = serial.tools.list_ports.comports()
        self.nb_ports = len(self.ports)

        for port in self.ports:
            if(port[1].startswith("STM")):  # TO TEST
                self.ports_com.append(port[0])

        self.serialLabel.clearCombo()
        self.serialLabel.setComboItems(self.ports_com)

    def createDBRightScreen(self):
        """
        Right part of the Direct USB Unique Spot Widget
        :return:
        """
        # Right screen with data
        self.rightLayout = QGridLayout()

        # USB SERIAL SELECTION
        self.nucleoTitle = QTitle("USB Nucleo Connection", self.rightLayout, 0)
        # Serial Label
        self.serialLabel = QAskCombo("Serial Port", self.rightLayout, 1)
        self.serialLabel.setComboItems(self.ports_com)
        # Connection Button
        self.nucleoConnectionButton = QPushButton("Connexion to Nucleo")
        self.nucleoConnectionButton.clicked.connect(self.connectionAction)
        self.rightLayout.addWidget(self.nucleoConnectionButton, 1, 3, 1, 2)

        # PROJECTOR INFORMATIONS
        self.selectedProj = QTitle("Selected Projector", self.rightLayout, 2)
        # Projector BrandName
        self.brandName = QInfoLine("Brand Name", self.rightLayout, 3)
        # Projector Name
        self.projName = QInfoLine("Projector Name", self.rightLayout, 3, 3)
        # Projector Type
        self.projType = QInfoLine("Projector Type", self.rightLayout, 4)
        # Projector Channels Number
        self.projCh = QInfoLine("Number of Channels", self.rightLayout, 4, 3)

        # Label Address
        self.addressDMX = QTitle("DMX ADDRESS", self.rightLayout, 5)

        self.addDMXAsk = QAskLine("DMX Address", self.rightLayout, 6)

        # Label Mode
        self.modeDMX = QTitle("MODE", self.rightLayout, 7)
        # Mode Selection - NoFunc, Sound, Strobe
        self.modeSelectionItems = ['No Function', 'Strobe', 'Sound']
        self.modeSelection = QAskCombo("Mode", self.rightLayout, 8)
        self.modeSelection.setComboItems(self.modeSelectionItems)

        # Label Dimmer
        self.dimmer = QTitle("GLOBAL DIMMER", self.rightLayout, 9)

        self.dimmerGlobal = QInfoLine("Dimmer Value", self.rightLayout, 10)

        self.dimmerSlider = QLongSlider("Dimmer Global", self.rightLayout, 11, self.changeSlider)

        # Label Colors Selection
        self.colorsSelection = QTitle("COLORS SELECTION", self.rightLayout, 12)
        # RGBWAUV Sliders
        self.redSlider = QSmallSlider("Red Value", self.rightLayout, 13, self.changeSlider)
        self.greenSlider = QSmallSlider("Green Value", self.rightLayout, 14, self.changeSlider)
        self.blueSlider = QSmallSlider("Blue Value", self.rightLayout, 15, self.changeSlider)
        self.whiteSlider = QSmallSlider("White Value", self.rightLayout, 16, self.changeSlider)
        self.amberSlider = QSmallSlider("Amber Value", self.rightLayout, 17, self.changeSlider)
        self.UVSlider = QSmallSlider("UV Value", self.rightLayout, 18, self.changeSlider)


        self.rightLayout.addWidget(QLabel(""), 20, 1, 1, 4)

    def updateDBRightScreen(self):
        if(self.projData != False):
            self.brandName.setLineText(self.projData['BrandName'])
            self.projName.setLineText(self.projData['ProjName'])
            self.projType.setLineText(self.projData['ProjType'])
            self.projCh.setLineText(self.projData['TotalNbCh'])

    def createDBMenu(self):
        # Top menu
        self.menuLayout = QHBoxLayout()
        self.menuUpdateDB = QPushButton("Read Database")
        self.menuUpdateDB.clicked.connect(self.updateDBVisu)
        self.menuLayout.addWidget(self.menuUpdateDB)
        self.menuUpdateProj = QPushButton("Send Data To USB")
        if(self.parent.isNucleoConnected() == False):
            self.menuUpdateProj.setEnabled(False)
        self.menuUpdateProj.clicked.connect(self.sendDataToUSB)
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
        self.projSelected = True

        self.projData = self.readDBVisu(selected)
        self.updateDBRightScreen()

    def sendDataToUSB(self):
        # !X:adr:channels:MODE_ch:MODE_nofunct_val:
        #      DIM_ch:DIM_min:DIM_max:DIM_val:R_ch:G_ch:B_ch:
        #      R_val:G_val:B_val:W_ch:W_val:A_ch:A_val:UV_ch:UV_val:
        self.dataToSend = '!X:'
        if(self.parent.isNucleoConnected()):
            if(self.projSelected):                      # Is a projector selected ?
                if(self.addDMXAsk.getLineText() != ""):     # Is a DMX address setup ?
                    self.dataToSend += str(self.addDMXAsk.getLineText())+':'
                    self.dataToSend += str(self.projCh.getLineText())+':'
                    self.dataToSend += str(self.projData['ModeCh'])+':'
                    self.dataToSend += str(self.projData['NoFunctionValue'])+':'
                    self.dataToSend += str(self.projData['DimmerCh'])+':'
                    self.dataToSend += str(self.projData['DimmerMin'])+':'
                    self.dataToSend += str(self.projData['DimmerMax'])+':'
                    self.dataToSend += str(self.dimmerSlider.getSliderValue())+':'
                    self.dataToSend += str(self.projData['RedCh'])+':'
                    self.dataToSend += str(self.projData['GreenCh'])+':'
                    self.dataToSend += str(self.projData['BlueCh'])+':'
                    self.dataToSend += str(self.redSlider.getSliderValue())+':'
                    self.dataToSend += str(self.greenSlider.getSliderValue())+':'
                    self.dataToSend += str(self.blueSlider.getSliderValue())+':'
                    self.dataToSend += str(self.projData['WhiteCh'])+':'
                    self.dataToSend += str(self.whiteSlider.getSliderValue())+':'
                    self.dataToSend += str(self.projData['AmberCh'])+':'
                    self.dataToSend += str(self.amberSlider.getSliderValue())+':'
                    self.dataToSend += str(self.projData['UVCh'])+':'
                    self.dataToSend += str(self.UVSlider.getSliderValue())+';'
                    print("Sending Data")
                    print(self.dataToSend)
                    self.dataToSendBytes = self.dataToSend.encode()
                    self.parent.sendSerialData(self.dataToSendBytes)
                else:
                    print("No DMX Address")
            else:
                print("No Projector Selected")
        else:
            print("No USB")

    def readDBVisu(self, event):
        print("visu")
        proj = self.tree.selectedItems()
        if(proj):
            brand = proj[0].text(0)
            projName = proj[0].text(1)
            fileName = brand+"/"+projName+".adr"
            data = openDBFile(fileName)
        return data
