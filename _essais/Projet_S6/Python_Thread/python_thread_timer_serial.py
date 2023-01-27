# -*- coding: utf-8 -*-
"""
First application with Threads 
    

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Tue Jan 26 20:34:05 2023

@author: julien.villemejane
@see https://stackoverflow.com/questions/12435211/threading-timer-repeat-function-every-n-seconds
"""

from threading import Timer, Thread, Event
from datetime import datetime
from serial import Serial
import serial.tools.list_ports


class PerpetualTimer():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()
        
    def setTime(self, t):
        self.t = t
        

class SerialCom(Serial):
    
    def __init__(self, port, baud):
        super().__init__(port, baud)
        self.port = port
        
    def serialIsReady():
        if(self.ser.inWaiting() != 0):
            print("Data OK")
            dataRcvCnt = ser.inWaiting()
              
    def close(self):
        super().close()
        
    def __str__(self):
        return f"Name: {super().port}"
        

if __name__ == "__main__":
    ports = serial.tools.list_ports.comports()

    for port, desc, hwid in sorted(ports):
        print("{}: {}".format(port, desc))
        
    selectPort = input("Select a COM port : ")    
    print(f"Port Selected : COM{selectPort}")
    serNuc = SerialCom('COM'+str(selectPort), 115200)
    # tik = PerpetualTimer(1, serNuc.serialIsReady)
    # tik.start()
    
    while serNuc.inWaiting() < 5:
        pass
    data_rec = serNuc.read(5)  # bytes
    print(type(data_rec))
    print(str(data_rec))
    
    
    serNuc.close()
    