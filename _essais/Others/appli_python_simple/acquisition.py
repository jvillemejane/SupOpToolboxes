import time
import serial
from serial import tools
from serial.tools import list_ports


def serial_ports():
    nb_port = 0
    ports = list(serial.tools.list_ports.comports())
    list_port = []
    for port in ports:
        print(port)

def sendA():
    # Opening selected communication port
    serialSelected = serial.Serial('COM'+ serialPortSelected, 115200, timeout=1)
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

def sendE():
    # Opening selected communication port
    serialSelected = serial.Serial('COM'+ serialPortSelected, 115200, timeout=1)
    if(serialSelected.isOpen() == False):
        serialSelected.open()
    # Sending char 'e' at the beginning and wait for char 'b'
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

# Affichage des ports de communication
serial_ports()
# Saisie du port a connecter
serialPortSelected = input('Entrer le port Nucleo : ')
if(serialPortSelected != 0):
    # Envoi du caractere a - allumage de la LED 1
    k = sendA()
    if k == 1:
        print('A OK')
    else:
        print('A NOK')
    time.sleep(1)
    # Envoi du caractere e - extinction de la LED 1
    k = sendE()
    if k == 1:
        print('E OK')
    else:
        print('E NOK')
else:
    print('No data to send')
