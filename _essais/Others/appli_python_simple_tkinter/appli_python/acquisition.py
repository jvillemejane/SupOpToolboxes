from tkinter import *
from tkinter.ttk	import *
import SerialUSB_Nucleo as sUSB

class Acquisition:
    "Application de communication avec une carte Nucleo - version simple - LEnsE / VILLEMEJANE (c) 2021"

    def __init__(self):
        # Serial communication variables
        self.serialUSB = sUSB.SerialUSB_Nucleo()                    # creation d'un objet liaison serie (bibliotheque)
        self.ports = self.serialUSB.serial_ports()                  # stockage de la liste des ports de communication possibles
        # Main window
        self.mainWindow = Tk()                                      # fenetre principal de TkInter
        self.mainWindow.title("Interface TkInter - Nucleo / LEnsE / VILLEMEJANE")
        self.mainWindow.geometry("300x200")
        self.mainWindow.bind("<Key>", self.clavier)                 # keyboard events attachement
        self.serialList()                                           # Creation de la liste des ports
        # Menu zone
        self.labelPorts = Label(self.mainWindow, text = "Port")     # Label pour afficher "Port"
        self.labelPorts.grid(row=0, column = 0)                     # positionnement de ce Label
        self.varInformations = StringVar()                          # variable pour afficher des informations sur le Label suivant
        self.labelInformation = Label(self.mainWindow, textvariable = self.varInformations)     # Label d'affichage des informations
        self.labelInformation.grid(row=2, column = 0, columnspan=3)               # positionnement de ce Label
        self.bFindSerial = Button(self.mainWindow, text ='FIND SERIAL', command =self.actionFind)
                                                                    # bouton Find serial
        self.bConnect = Button(self.mainWindow, text ='CONNECT', command =self.actionConnect)
                                                                    # bouton Connect
        self.bOn = Button(self.mainWindow, text ='LED ON', command =self.actionOn, state=DISABLED)  # bouton ON
        self.bOff = Button(self.mainWindow, text='LED OFF', command=self.actionOff, state=DISABLED) # bouton OFF
        # positionnement des boutons
        self.bFindSerial.grid(row = 1, column = 0, columnspan = 3)
        self.bConnect.grid(row = 3, column = 1)
        self.bOn.grid(row = 4, column = 1)
        self.bOff.grid(row = 5, column = 1)

    def clavier(self, event):
        touche = event.keysym
        if touche == 'q' or touche == 'Q' :
            self.varInformations.set('Touche Q')
        elif touche == 'a' or touche == 'A' :
            self.varInformations.set('Touche A')
            self.serialUSB.sendA()
        elif touche == 'e' or touche == 'E':
            self.varInformations.set('Touche E')
            self.serialUSB.sendE()
        self.step()

    def step(self):
        self.mainWindow.after(100,self.step)
    
    def actionFind(self):
        self.serialList()
        if self.ports == 0:
            self.bOn['state'] = DISABLED
            self.bOff['state'] = DISABLED
            self.bConnect['state'] = DISABLED
        else:
            self.bConnect['state'] = NORMAL
            self.bOn['state'] = DISABLED
            self.bOff['state'] = DISABLED
        
    def actionOn(self):
        errk = self.serialUSB.sendA()
        if(errk == 1):
            self.varInformations.set("LED ON")
        elif(errk == -1):
            self.varInformations.set("ERREUR")

    def actionOff(self):
        errk = self.serialUSB.sendE()
        if (errk == 1):
            self.varInformations.set("LED OFF")
        elif (errk == -1):
            self.varInformations.set("ERREUR")

    def actionConnect(self):
        if(self.listPorts != 0):
            self.ports_value = self.listPorts.get()
            # Sur windows (attention sous unix different !!)
            self.serialUSB.serialPortSelected = self.ports_value[3:5]
            print(self.serialUSB.serialPortSelected)
            self.labelInformation.grid(row=2, column = 2)
            errk = self.serialUSB.connect()
            if(errk == 1):
                self.varInformations.set("Conn. COM"+self.serialUSB.serialPortSelected)
                self.bOn['state'] = NORMAL
                self.bOff['state'] = NORMAL
            elif(errk == -1):
                self.varInformations.set("NO COMM")
                self.bOn['state'] = DISABLED
                self.bOff['state'] = DISABLED

    def serialList(self): 
        self.ports_value = StringVar(self.mainWindow)
        self.ports = self.serialUSB.serial_ports()    
        self.listPorts = Combobox(self.mainWindow)
        self.ports_name = []
        self.ports_number = []
        # Serial communication zone
        if(self.ports != 0):
            for i in range(0, len(self.ports)):
                self.listPorts.insert(i, self.ports[i])
        else:
            self.listPorts.insert(-1, 'No Serial')
        self.listPorts.grid(row = 0, column = 1, columnspan = 2)

    def run(self):
        # MAIN PROGRAM

        self.mainWindow.mainloop()