# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox, QWidget

)

from PyQt5.uic import loadUi



class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("interface_graphique.ui", self)
        
        self.cpt1 = 0;
        self.nbpiece1.setText("0")
        self.cpt2 = 0;
        self.nbpiece2.setText("0")
        self.cpt3 = 0;
        self.nbpiece3.setText("0")
   
        self.couleurchoix1 = 0
        self.formechoix1 = 0
        self.couleurchoix2 = 0
        self.formechoix2 = 0
        self.couleurchoix3 = 0
        self.formechoix3 = 0
        
        self.bleu1.toggled.connect(self.updateQT)
    

    def updateQT(self):
        self.nbpiece1.setText("OK")



if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()
    win.cpt1 = 0
    win.cpt2 = 0
    win.cpt3 = 0

    win.nbpiece1.setText(str(win.couleurchoix1))
    win.nbpiece2.setText(str(win.cpt1))
    win.nbpiece3.setText(str(win.cpt1))
    
    win.show()
    app.exec()
   # sys.exit(app.exec())
    
