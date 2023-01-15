# -*- coding: utf-8 -*-
"""
Projet Diagramme Automatisé Rayonnement source LED

TO DO
- IHM pour affichage graphique
- Interface avec Nucleo pour pilotage ServoMoteur et Acquisition


FIRST TEST 
- pyserial pour récupérer et discuter avec une carte Nucleo
- connection à une carte nucleo
- protocole simple : 
    - envoie d'un 'a' avec le PC
    - renvoie 2 caractères 'ab' (a étant le caractere envoye initialement)

Created on Thu Dec 15 13:40:39 2022

@author: julien.villemejane
"""

import serial
import serial.tools.list_ports

# List all the available COM ports
serial_port = serial.tools.list_ports.comports()

# Print the list of avalaible COM ports
for k in serial_port:
    print(f"{k}")
    
# serial_com = input("Quel port voulez-vous utiliser ? (uniquement le nombre) ")


serial_com = 6
print(f"Utilisation du port COM{serial_com} --> ")
serial_com_name = 'COM'+str(serial_com)

# Open the setup serial port
ser = serial.Serial(serial_com_name, baudrate=115200)  # open serial port @ 115200 bauds
print(ser.name)         # check which port was really used
# Sending a char to Nucleo Board
print('Sending char \'a\' to Nucleo Board')
ser.write(b'a')     # write a string

# Waiting for data sending by Nucleo board
print(ser.in_waiting)
while(ser.in_waiting == 0):
    print("Wait !")

rec_data_nucleo = ser.readline(2)
print(f'Rec = {rec_data_nucleo}')

ser.close()  