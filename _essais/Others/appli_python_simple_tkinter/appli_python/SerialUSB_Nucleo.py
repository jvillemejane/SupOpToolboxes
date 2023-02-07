import time
import serial
from serial import tools
from serial.tools import list_ports

class SerialUSB_Nucleo:
    def __init__(self):
        self.nb_port = 0
        self.list_port = []
        self.serialPortSelected = 0

    def serial_ports(self):
        self.nb_port = 0
        ports = list(serial.tools.list_ports.comports())
        self.list_port = []
        for port in ports:
            if 'STM' in str(port) or 'USB' in str(port):
                self.nb_port += 1
                self.list_port.append(str(port))
        if(self.nb_port != 0):
            return self.list_port
        else:
            return 0

    def connect(self):
        # Opening selected communication port
        serialSelected = serial.Serial('COM'+ self.serialPortSelected, 115200, timeout=1)
        if(serialSelected.isOpen() == False):
            serialSelected.open()
        # Sending char 'a' at the beginning and wait for char 'o'
        serialSelected.write(bytes('z','utf-8'))
        dataRecOk = 0
        timeoutRec = 0
        while (dataRecOk == 0) or (timeoutRec < 10):
            timeoutRec += 1
            if(timeoutRec > 10): # timeout = 10 x 1ms
                return -1
            if serialSelected.inWaiting() > 0:
                dataReceived = serialSelected.read(1)
                if(dataReceived == bytes('k','utf-8')):
                    dataRecOk = 1
                    return 1
            time.sleep(0.001)

    def sendA(self):
        # Opening selected communication port
        serialSelected = serial.Serial('COM'+ self.serialPortSelected, 115200, timeout=1)
        if(serialSelected.isOpen() == False):
            serialSelected.open()
        # Sending char 'a' at the beginning and wait for char 'o'
        serialSelected.write(bytes('a','utf-8'))
        dataRecOk = 0
        timeoutRec = 0
        while (dataRecOk == 0) or (timeoutRec < 10):
            timeoutRec += 1
            if(timeoutRec > 10): # timeout = 10 x 1ms
                return -1
            if serialSelected.inWaiting() > 0:
                dataReceived = serialSelected.read(1)
                if(dataReceived == bytes('o','utf-8')):
                    dataRecOk = 1
                    return 1
            time.sleep(0.001)
    
    def sendE(self):
        # Opening selected communication port
        serialSelected = serial.Serial('COM'+ self.serialPortSelected, 115200, timeout=1)
        if(serialSelected.isOpen() == False):
            serialSelected.open()
        # Sending char 'a' at the beginning and wait for char 'o'
        serialSelected.write(bytes('e','utf-8'))
        dataRecOk = 0
        timeoutRec = 0
        while (dataRecOk == 0) or (timeoutRec < 10):
            timeoutRec += 1
            if(timeoutRec > 10): # timeout = 10 x 1ms
                return -1
            if serialSelected.inWaiting() > 0:
                dataReceived = serialSelected.read(1)
                if(dataReceived == bytes('b','utf-8')):
                    dataRecOk = 1
                    return 1
            time.sleep(0.001)
