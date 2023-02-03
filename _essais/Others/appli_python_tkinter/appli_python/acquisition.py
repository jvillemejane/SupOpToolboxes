from tkinter import *
from tkinter.ttk	import *
import time
import os
import sys
import glob      
import matplotlib.pyplot as plt
import SerialUSB_Nucleo as sUSB

class Acquisition:
    "Application d'acquisition de donnees - LEnsE / VILLEMEJANE (c) 2019"

    def __init__(self):
        self.go = 0
        # Serial communication variables
        self.serialUSB = sUSB.SerialUSB_Nucleo()
        self.ports = self.serialUSB.serial_ports()        
        self.ports_name = []
        self.ports_number = []
        self.ports_value = 0
        self.data = []
        self.dataAcquired = 0
        # Main window
        self.mainWindow = Tk()
        self.mainWindow.title("Acquisition / LEnsE / VILLEMEJANE")
        self.mainWindow.bind("<Key>", self.clavier)     # keyboard events attachement
        self.serialList()
        
        # Main zone
        self.can1 = Canvas(self.mainWindow, width = 500, height = 200, bg ='white')
        self.can1.grid(row=0, column = 0, columnspan = 3)
        
        # Menu zone
        self.labelPorts = Label(self.mainWindow, text = "Port")
        self.labelPorts.grid(row=1, column = 0)
        self.varPortConnected = StringVar()
        self.labelPortConnected = Label(self.mainWindow, textvariable = self.varPortConnected)
        self.labelPortConnected.grid(row=2, column = 2)
        self.bFindSerial = Button(self.mainWindow, text ='FIND SERIAL', command =self.actionFind)
        self.bConnect = Button(self.mainWindow, text ='CONNECT', command =self.actionConnect)
        self.bUpdate = Button(self.mainWindow, text ='UPDATE', command =self.actionUpdate, state=DISABLED)
        self.bGo = Button(self.mainWindow, text ='START ACQ', command =self.actionGo, state=DISABLED)
        self.bFindSerial.grid(row=2, column = 0, columnspan = 3)
        self.bConnect.grid(row=1, column = 2)
        self.bUpdate.grid(row=3, column = 2, rowspan = 3)
        self.bGo.grid(row=6, column = 1)
        # Parameters zone
        self.labelNumberPoints = Label(self.mainWindow, text = "Nombre points")
        self.labelFrequency = Label(self.mainWindow, text = "Frequence")
        self.labelSync = Label(self.mainWindow, text = "Synchro")
        self.labelNumberPoints.grid(row=3, column =0)
        self.labelFrequency.grid(row=4, column = 0)
        self.labelSync.grid(row=5, column = 0)
        # Data storage zone
        self.labelDataOk = Label(self.mainWindow, text = "No Data")
        self.labelDataOk.grid(row=7, column=0)
        self.bDataDisplay = Button(self.mainWindow, text ='DISPLAY', command =self.actionDisplay, state=DISABLED)
        self.bDataDisplay.grid(row=7, column=1)
        self.bDataExport = Button(self.mainWindow, text ='EXPORT CSV', command =self.actionExport, state=DISABLED)
        self.bDataExport.grid(row=7, column=2)
        self.go = 1
        
    def redessiner(self):
        self.can1.grid(row=0, column = 0, columnspan = 3)

    def clavier(self, event):
        touche = event.keysym
        if touche == 'q' or touche == 'Q' :
            self.go = -1
        self.step()

    def step(self):
        if self.go == 1 :
            #appel a run toute les 100ms
            self.redessiner()
            self.mainWindow.after(100,self.step)
        elif self.go == -1 :
            self.mainWindow.destroy()
    
    def actionFind(self):
        self.serialList()
        
    def actionGo(self):
        errk = self.serialUSB.collect_data()
        if(errk == 1):
            self.varPortConnected.set("Collected COM" + self.serialUSB.serialPortSelected)
            self.bDataDisplay['state'] = NORMAL
            self.bDataExport['state'] = NORMAL
            self.bGo['state'] = DISABLED
            self.dataAcquired = 1
        elif(errk == -1):
            self.varPortConnected.set("No Collect")
        
    def actionUpdate(self):
        # reste a chercher les parametres dans fenetres
        errk = self.serialUSB.update_parameters(10, 1000, 0)
        if(errk == 1):
            self.varPortConnected.set("Updated COM" + self.serialUSB.serialPortSelected)
            self.bGo['state'] = NORMAL
        elif(errk == -1):
            self.varPortConnected.set("No Update")
        
    def actionConnect(self):
        if(self.listPorts != 0):
            self.ports_value = self.listPorts.get()
            # Sur windows (attention sous unix different !!)
            self.serialUSB.serialPortSelected = self.ports_value[3:5]
            self.labelPortConnected.grid(row=2, column = 2)
            errk = self.serialUSB.test_nucleo()
            if(errk == 1):
                self.varPortConnected.set("Connected COM"+self.serialUSB.serialPortSelected)
                self.bUpdate['state'] = NORMAL
            elif(errk == 2):
                self.varPortConnected.set("No comm")
            elif(errk == -1):
                self.varPortConnected.set("Not Connected")
            print('CONNECT !!!' + str(self.ports_value))

    def actionDisplay(self):
        if(self.dataAcquired != 0):
            print(self.serialUSB.data_acq)
            print('ok')
            plt.plot(self.serialUSB.data_acq)
            # plt.ylabel('B12')
            # plt.title('Affichage des données (N = ' + str(self.labelNumberPoints) + ' @ Fe = ' + str(fe) + ')')
            plt.show()
        print("DISPLAY !!!")    
    
    def actionExport(self):
        if(self.dataAcquired != 0):
            print('ok')
        print("EXPORT !!!")
    
    def serialList(self): 
        self.ports_value = StringVar(self.mainWindow)
        self.ports = self.serialUSB.serial_ports()    
        self.listPorts = Combobox(self.mainWindow)
        self.ports_name = []
        self.ports_number = []
        # Serial communication zone
        if(self.ports != 0):
            for i in range(0, len(self.ports)):
                print(self.ports[i])
                self.ports_name.append(self.ports[i])
                self.ports_number.append(i)
                self.listPorts.insert(self.ports_number[i], self.ports_name[i])
                # self.listPorts.current(-1)
        else:
            self.ports_name.append('No Serial / Click on Find Serial')
            self.ports_number.append(-1)
            print(self.ports_number)
            self.ports_value.set(self.ports_number[0])
            self.listPorts.insert(self.ports_number[0], self.ports_name[0])
            print('No SERIAL')
        self.listPorts.grid(row=1, column = 1)

    def run(self):
        # MAIN PROGRAM

        self.mainWindow.mainloop()