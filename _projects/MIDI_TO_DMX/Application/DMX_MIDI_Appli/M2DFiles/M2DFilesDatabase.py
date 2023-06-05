import os
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *

def typeProj(type):
    return {
        "Lyre": "L",
        "Scanner":"S",
        "Par":"P",
        "RGBAW-UV":"R",
        "Stroboscope": "B"
    }[type]
def typeProjInv(type):
    return {
        "L": "Lyre",
        "S": "Scanner",
        "P": "Par",
        "R": "RGBAW-UV",
        "B": "Stroboscope"
    }[type]


def writeNoValueDBFile(param, fileDB):
    if (param != ""):
        fileDB.write(param + ":")
    else:
        fileDB.write("0:")


def writeDBFile(fileName_in, data_in):  # A MODIFIER !!!!
    pathName = "database/"+data_in[0]+"/"
    if not os.path.exists(pathName):
        print("No Path")
        os.makedirs(pathName)
    fileName = "database/"+fileName_in+".adr"
    choice = 'y'
    if(os.path.exists(fileName)):
        print("File already exists...")
        choice = input('Do you want to write again ? (y)es or (n)o :')

    if(choice == 'y'):
        filetemp = open(fileName, "w")
        filetemp.write(data_in[0]+":"+data_in[1]+":"+typeProj(data_in[2])+":\n")
        filetemp.write("S[01]001:")
        filetemp.write(data_in[3]+":01:")  # CH - Number of channels
        writeNoValueDBFile(data_in[4], filetemp)    # Mode Channel
        writeNoValueDBFile(data_in[5], filetemp)    # No function value
        writeNoValueDBFile(data_in[6], filetemp)    # DIM Channel
        writeNoValueDBFile(data_in[7], filetemp)    # DIM Min Value
        writeNoValueDBFile(data_in[8], filetemp)    # DIM Max Value
        writeNoValueDBFile(data_in[9], filetemp)    # R Channel
        writeNoValueDBFile(data_in[10], filetemp)   # G Channel
        writeNoValueDBFile(data_in[11], filetemp)   # B Channel
        writeNoValueDBFile(data_in[12], filetemp)   # W Channel
        writeNoValueDBFile(data_in[13], filetemp)   # A Channel
        writeNoValueDBFile(data_in[14], filetemp)   # UV Channely
        filetemp.close()
    else:
        print("Nothing was done...")

def popup_button(self, i):
    print(i.text())

def openDBFile(fileName_in):
    fileName = "database/"+fileName_in
    data = dict()
    if(os.path.exists(fileName)):
        filetemp = open(fileName, "r")
        lines = filetemp.readlines()
        # Global Parameter / Brandname, Projector Name, Type
        globalParam = lines[0].split(":")
        data['BrandName'] = (globalParam[0])
        data['ProjName'] = (globalParam[1])
        data['ProjType'] = (typeProjInv(globalParam[2]))
        channels = lines[1].split(":")
        # channels: DIM:R: G:B: W:A: UV:PAN: TILT:SPD: STB
        #   S[nn]adr:nbr:gpe:mode:nofunc:dim:dim_min:dim_max:r:g:b:w:a:uv:
        data['TotalNbCh'] = channels[1]     # total number of channels
        data['DimmerCh'] = channels[5]      # dimmer channel
        data['DimmerMin'] = channels[6]     # dimmer minimum value
        data['DimmerMax'] = channels[7]     # dimmer maximum value
        data['RedCh'] = channels[8]         # red channel
        data['GreenCh'] = channels[9]       # green channel
        data['BlueCh'] = channels[10]       # blue channel
        data['WhiteCh'] = channels[11]      # white channel
        data['AmberCh'] = channels[12]      # amber channel
        data['UVCh'] = channels[13]         # UV channel
        # Standard Modes / No Function
        data['ModeCh'] = channels[3]        # mode channel
        data['NoFunctionValue'] = channels[4]   # No function value

        # Other modes / Pan / Tilt / Sound / Strobe

        # Close file
        filetemp.close()
    return data

def readDB():
    data = {}
    pathName = "database/"
    print("Open DB")
    for file in os.listdir(pathName):
        if(os.path.isdir(pathName+"/"+file)):
            dataDir = []
            for file2 in os.listdir(pathName+"/"+file):
                data_new = openDBFile(file+"/"+file2)
                dataDir.append(data_new)
            data[file] = dataDir
    return data