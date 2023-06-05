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

from M2DAppGUI.VisualisationDatabaseWidget import *
from M2DAppGUI.AddingToDatabaseWidget import *
from M2DAppGUI.DirectUSBUniqueSpotWidget import *
import serial


class MIDI2DMXMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # menu
        self.create_menu()

        self.nucleoConnected = False
        self.serialNucleo = serial.Serial()
        self.serialNucleo.baudrate = 115200
        self.nucleoPort = ""
        # Main Tab Widget
        self.mainTabWidget = QTabWidget()
        # DataBase Tabulations
        self.DBTabWidget = QTabWidget()
        self.DBTabWidget.addTab(VisualisationDatabaseWidget(), "Existing Spots")
        self.DBTabWidget.addTab(AddingToDatabaseWidget(), "New Spot")

        # DMX Setup
        self.DMXTabWidget = QTabWidget()
        self.DMXTabWidget.addTab(QWidget(), "Setup Addressing") # TO DO

        # Controller Setup
        self.ControllerSetupTabWidget = QTabWidget()

        # Direct USB
        self.DirectUSBTabWidget = QTabWidget()
        self.DirectUSBTabWidget.addTab(DirectUSBUniqueSpotWidget(self, self.mainTabWidget), "Unique Spot")
        self.DirectUSBTabWidget.addTab(QWidget(), "Group Spot")

        # Save to SD
        self.SaveToSDWidget = QTabWidget()

        # MAIN Tabulations
        self.mainTabWidget.addTab(self.DBTabWidget, "Spots Database")
        self.mainTabWidget.addTab(self.DMXTabWidget, "DMX Address")
        self.mainTabWidget.addTab(self.ControllerSetupTabWidget, "Controller Setup")
        self.mainTabWidget.addTab(self.DirectUSBTabWidget, "Direct USB Control")
        self.mainTabWidget.addTab(self.SaveToSDWidget, "Save Setup to SD Card")

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.mainTabWidget, 0, 0)
        # central widget
        self.centralWindow = QWidget()
        self.centralWindow.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWindow)
        self.setWindowTitle("MIDI2DMX / Application / byVillou.fr & LEnsE")
        self.resize(1200, 800)


    def getSerialNucleo(self):
        return self.serialNucleo

    def getNucleoPort(self):
        return self.nucleoPort

    def connectSerialNucleo(self):
        if(self.nucleoPort != ""):
            self.serialNucleo.port = self.nucleoPort
            self.serialNucleo.open()
            while(self.serialNucleo.isOpen() == False):
                pass
            self.serialNucleo.write(b'!Y:1;')
            self.nucleoConnected = True
        else:
            print("Erreur Connection Nucleo - Empty Port")

    def sendSerialData(self, data):
        if(self.serialNucleo.isOpen()):
            self.serialNucleo.write(data)

    def disconnectSerialNucleo(self):
        if(self.nucleoConnected == True):
            self.serialNucleo.write(b'!Y:0;')
            self.serialNucleo.close()
            self.nucleoConnected = False
        else:
            print("Erreur DisConnection Nucleo - Nucleo Not Connected")

    def isNucleoConnected(self):
        return self.nucleoConnected

    def setNucleoConnected(self, value):
        self.nucleoConnected = value

    def setNucleoPort(self, port):
        if(self.nucleoConnected == False):
            self.nucleoPort = port
        else:
            print("Erreur Changing Port - Nucleo Connected")

    def create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")

        newAction = QAction(QIcon("images/new.png"), "New Project", self)
        newAction.setShortcut("Ctlr+N")
        fileMenu.addAction(newAction)
        openAction = QAction(QIcon("images/open.png"), "Open Project", self)
        openAction.setShortcut("Ctlr+O")
        fileMenu.addAction(openAction)
        saveAction = QAction(QIcon("images/save.png"), "Save Project", self)
        saveAction.setShortcut("Ctlr+S")
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        exitAction = QAction(QIcon("images/exit.png"), "Exit", self)
        exitAction.setShortcut("Ctlr+Q")
        exitAction.triggered.connect(self.close_window)
        fileMenu.addAction(exitAction)

    def close_window(self):
        self.close()


