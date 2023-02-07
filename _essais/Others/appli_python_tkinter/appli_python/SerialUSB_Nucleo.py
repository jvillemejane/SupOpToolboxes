import time
import os
import sys
import glob
import matplotlib.pyplot as plt
import serial
from serial import tools
from serial.tools import list_ports

class SerialUSB_Nucleo:
    def __init__(self):
        self.nucleo_connected = 0
        self.serial_connected = 0
        self.nb_port = 0
        self.list_port = []
        self.serialPortSelected = 0
        self.param_fe = 0
        self.param_nbPoints = 0
        self.param_sync = 0
        self.param_updated = 0
        self.data_acq = []

    def change_port(self, portSelected):
        self.serialPortSelected = portSelected

    def serial_ports(self):
        self.nb_port = 0
        ports = list(serial.tools.list_ports.comports())
        self.list_port = []
        for port in ports:
            if 'STM' in str(port):
                self.nb_port += 1
                #print(port)
                self.list_port.append(str(port))
        if(self.nb_port != 0):
            return self.list_port
        else:
            return 0

    def test_nucleo(self):
        if(self.nucleo_connected != 0):
            return 2
        # Opening selected communication port
        serialSelected = serial.Serial('COM'+ str(self.serialPortSelected), 115200, timeout=1)
        if(serialSelected.isOpen() == False):
            serialSelected.open()
            self.serial_connected = 1
        else:
            self.serial_connected = 1
        # Sending char 'a' at the beginning and wait for char 'o'
        serialSelected.write(bytes('a','utf-8'))
        dataRecOk = 0
        timeoutRec = 0
        while (dataRecOk == 0) or (timeoutRec < 10):
            timeoutRec += 1
            if(timeoutRec > 10):
                return -1
            if serialSelected.inWaiting() > 0:
                dataReceived = serialSelected.read(1)
                if(dataReceived == bytes('o','utf-8')):
                    dataRecOk = 1
                    self.nucleo_connected = 1
                    return 1
            time.sleep(0.001)

    def update_parameters(self, number_points, frequency, sync):
        if(self.nucleo_connected != 1):
            return -1
        self.param_nbPoints = number_points
        self.param_fe = frequency
        self.param_sync = sync
        # Opening selected communication port
        serialSelected = serial.Serial('COM'+ self.serialPortSelected, 115200, timeout=1)
        if(serialSelected.isOpen() == False):
            serialSelected.open()
            self.serial_connected = 1
        else:
            self.serial_connected = 1
        print('Sending data')
        # Sending data
        serialSelected.write(bytes('U','utf-8'))
        dataRecOk = 0
        timeoutRec = 0
        while (dataRecOk == 0) or (timeoutRec < 10):
            timeoutRec += 1
            if(timeoutRec > 10):
                return -1
            if serialSelected.inWaiting() > 0:
                dataReceived = serialSelected.read(1)
                print('Rec = ' + str(dataReceived))
                if(dataReceived == bytes('u','utf-8')):
                    dataRecOk = 1
            time.sleep(0.001)
        # Sending parameter number of points
        print('Sending n')
        serialSelected.write(bytes('n','utf-8'))
        dataRecOk = 0
        timeoutRec = 0
        while (dataRecOk == 0) or (timeoutRec < 10):
            timeoutRec += 1
            if(timeoutRec > 10):
                return -1
            if serialSelected.inWaiting() > 0:
                dataReceived = serialSelected.read(1)
                if(dataReceived == bytes('n','utf-8')):
                    dataRecOk = 1
            time.sleep(0.001)
        serialSelected.write(bytes(str(number_points),'utf-8'))
        # Sending parameter frequency
        print('Sending f')
        serialSelected.write(bytes('f','utf-8'))
        dataRecOk = 0
        timeoutRec = 0
        while (dataRecOk == 0) or (timeoutRec < 10):
            timeoutRec += 1
            if(timeoutRec > 10):
                return -1
            if serialSelected.inWaiting() > 0:
                dataReceived = serialSelected.read(1)
                if(dataReceived == bytes('f','utf-8')):
                    dataRecOk = 1
            time.sleep(0.001)
        serialSelected.write(bytes(str(frequency),'utf-8'))
        # Sending parameter sync
        print('Sending s')
        serialSelected.write(bytes('s','utf-8'))
        dataRecOk = 0
        timeoutRec = 0
        while (dataRecOk == 0) or (timeoutRec < 10):
            timeoutRec += 1
            if(timeoutRec > 10):
                return -1
            if serialSelected.inWaiting() > 0:
                dataReceived = serialSelected.read(1)
                if(dataReceived == bytes('s','utf-8')):
                    dataRecOk = 1
            time.sleep(0.001)
        serialSelected.write(bytes(str(sync),'utf-8'))
        serialSelected.close()
        self.serial_connected = 0
        self.param_updated = 1
        return 1

    def collect_data(self):
        if(self.param_updated != 1):
            return -1
        # Opening selected communication port
        serialSelected = serial.Serial('COM'+ self.serialPortSelected, 115200, timeout=100)
        if(serialSelected.isOpen() == False):
            serialSelected.open()
            self.serial_connected = 1
        print('Collecting data')
        serialSelected.write(bytes('G','utf-8')) # GO
        dataRecOk = 0
        # Waiting for the end of acquisition
        while dataRecOk == 0 :
            if (serialSelected.inWaiting() > 0):
                dataReceived = serialSelected.read(1)
                if(dataReceived == bytes('d','utf-8')):
                    dataRecOk = 1
                    print('ok d')
        # Collecting all the data
        nb_data = 0
        i_rec = 0
        num_rec = 0
        pdix = 1
        tab_data = [0] * 5

        while nb_data <= self.param_nbPoints :
            if (serialSelected.inWaiting() > 0):
                dataReceived = serialSelected.read(1)
                if(dataReceived == bytes('[','utf-8')):
                    i_rec = 0
                    nb_data += 1
                    tab_data = [0] * 5
                    pdix = 1
                    num_rec = 0
                elif(dataReceived == bytes(';','utf-8')):
                    for i_verif in range(i_rec):
                        num_rec += tab_data[i_rec - i_verif - 1] * pdix
                        pdix = pdix * 10
                    i_rec = 0
                    num_rec = 0
                    pdix = 1
                elif(dataReceived == bytes(']','utf-8')):
                    for i_verif in range(i_rec):
                        num_rec += tab_data[i_rec - i_verif - 1] * pdix
                        pdix = pdix * 10
                    i_rec = 0
                    self.data_acq.append(int(num_rec))
                    if nb_data == self.param_nbPoints:
                        nb_data += 1
                else:
                    tab_data[i_rec] = int(dataReceived)
                    i_rec += 1
        serialSelected.close()
        self.serial_connected = 0
        return 1
