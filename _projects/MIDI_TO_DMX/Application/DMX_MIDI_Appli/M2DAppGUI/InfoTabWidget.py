## MIDI2DMX Application / byVillou.fr & LEnsE
#       Developed by Julien VILLEMEJANE
#       Creation date : 01/oct/2022
#
#       FILENAME :        InfoTabWidget.py
#
#       DESCRIPTION :
#           Main Information TabWidget
#
#       NOTES :
#           These functions are a part of the MIDI2DMX application
#######################################################################


from PySide6.QtWidgets import *
import M2DFiles
from M2DGraphElements import *
from PySide6.QtGui import *
import serial


class InfoTabWidget(QTabWidget):
    def __init__(self, parent):
        """
        IntoTabWidget Class
        """
        super().__init__()
        self.parent = parent
        self.checkedHardware = False

        # Right Layout - Global information about database
        # #########################################################################
        self.rightLayout = QGridLayout()
        # Title
        self.titleLabel = QLabel("MIDI 2 DMX Application")
        self.titleLabel.setFixedHeight(60)
        self.titleLabel.setStyleSheet("background-color: darkgray; padding:5px; color:white; font-size:30px; font-weight:bold;")
        self.rightLayout.addWidget(self.titleLabel, 0, 1, 1, 4)
        # Existing Projects
        self.numberProject = M2DGraphElements.QInfoLine("Existing Projects", self.rightLayout, 1)
        self.totalNumberProjects = M2DFiles.M2DFilesDatabase.getNumberOfProjects()
        self.numberProject.setLineText(str(self.totalNumberProjects))
        self.existingProjectSelection = M2DGraphElements.QAskCombo("Selection ?", self.rightLayout, 1, col=3, minWidth=400)
        self.existingProjectItems = M2DFiles.listExistingProjects()
        self.existingProjectSelection.setComboItems(self.existingProjectItems)
        # Existing Spots
        self.numberSpots = M2DGraphElements.QInfoLine("Existing Spots", self.rightLayout, 2)
        self.totalNumberProjectors = M2DFiles.getNumberOfProjectors()
        self.numberSpots.setLineText(str(self.totalNumberProjectors))

        # Left Layout - Information about hardwar
        # #########################################################################
        self.leftLayout = QGridLayout()
        # Hardware connection
        self.hardWare = M2DGraphElements.QTitle("Hardware detection", self.leftLayout, 0)
        self.hardWareCheck = QPushButton("Check Hardware Connexion")
        self.hardWareCheck.clicked.connect(self.createPortList)
        self.leftLayout.addWidget(self.hardWareCheck, 1, 1, 1, 4)
        self.hardSerialLabel = M2DGraphElements.QAskCombo("Serial Selection", self.leftLayout, 2)
        self.hardSerialLabel.setComboItems([])
        self.hardSerialConnectButton = QPushButton("Connect to HardWare")
        self.hardSerialConnectButton.clicked.connect(self.connectionAction)
        self.hardSerialConnectButton.setEnabled(False)
        self.leftLayout.addWidget(self.hardSerialConnectButton, 2, 3, 1, 2)

        # Main Layout
        # #########################################################################
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.rightLayout)
        self.mainLayout.addLayout(self.leftLayout)
        self.setLayout(self.mainLayout)

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
        self.ports_com = []

        for port in self.ports:
            if(port[1].startswith("STM")):  # TO TEST
                self.ports_com.append(port[0])

        self.hardSerialLabel.clearCombo()
        self.hardSerialLabel.setComboItems(self.ports_com)

        if(len(self.ports_com) == 0):
            self.ports_com = ["NO HARDWARE DETECTED"]
            self.hardSerialLabel.setComboItems(self.ports_com)
        else:
            self.checkedHardware = True
            self.hardSerialConnectButton.setEnabled(True)


    def connectionAction(self):
        """
        Connect the Nucleo board via USB Serial Port
        Update the graphical element linked to the connection process (Connection button and Send Data button)
        :return:
        """
        if(self.parent.isNucleoConnected() == False):
            if(self.hardSerialLabel.getComboText() != ""):
                self.parent.setNucleoPort(self.hardSerialLabel.getComboText())
                if(self.parent.getNucleoPort() != ""):
                    # self.parent.connectSerialNucleo()
                    self.hardSerialConnectButton.setText("Disconnect")
                    self.parent.setNucleoConnected(True)
                    self.parent.setDirectUSBTabWidgetEnabled(True)
                    self.parent.setSaveToSDWidgetEnabled(True)
                    self.menuUpdateProj.setEnabled(True)
                else:
                    print("Error Connection - No Port Selected")
            else:
                print("Error - Empty Port")
        else:
            self.nucleoConnectionButton.setText("Connexion to Nucleo")
            self.parent.disconnectSerialNucleo()
            self.parent.setNucleoConnected(False)
            self.menuUpdateProj.setEnabled(False)
            self.parent.setDirectUSBTabWidgetEnabled(False)
            self.parent.setSaveToSDWidgetEnabled(False)