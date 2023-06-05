## MIDI2DMX Application / byVillou.fr & LEnsE
#       Developed by Julien VILLEMEJANE
#       Creation date : 01/oct/2022
#
#       FILENAME :        main.py
#
#       DESCRIPTION :
#           Main File.
#
#       NOTES :
#           These functions are a part of the MIDI2DMX application
#######################################################################
#       Hardware :
#           + Add SRAM (128k * 8 bits) with SPI ? ( for presets ? for anything else ? )
#           + Add TEMPO mode from 60 to 140 BPM
#           + Add Transition ( from a preset to another ) in a specific time ( or tempo )
#######################################################################
#       TO DO :
#           - Modify DataBase Visualization (Existing and New Spots) with M2DGraphElements
#           + DMX Address Setup ( 000 directories and *.adr files )
#               - create a new setup / with name
#               - add spot at a specific address (with group)
#               - save setup to *.adr file
#               - open / update existing *.adr file
#           + Controller Setup ( *.ctr file )
#               - create a new setup for a main controller ( if 2 controllers ? )
#               - add specific control (see *.ctr file)
#               - save controller setup to *.ctr file
#               - open / update existing *.ctr file
#           + Keyboard Mode ( *.not file )
#               - create a new MIDI notes setup ( *.not file )
#               - save MIDI notes setup to *.not file
#               - open / update existing *.not file
#               -
#           + Preset Setup for groups
#           + Direct USB Control
#               - group control with DMX Address Setup ( from *.adr file )
#           + Save data to M2D SD card ( with or without USB connexion to M2D Hardware )


from M2DAppGUI.MIDI2DMXMainWindow import *


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = MIDI2DMXMainWindow()
    window.show()

    app.exec()
