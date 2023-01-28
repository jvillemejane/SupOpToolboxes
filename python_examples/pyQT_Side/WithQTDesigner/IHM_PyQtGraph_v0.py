# -*- coding: utf-8 -*-
"""
First application with pyQtGraph / Spyder 

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Sat Jan 14 20:34:05 2023

@author: julien.villemejane
"""

import numpy as np

import pyqtgraph as pg

data = np.random.normal(size=1000)
pg.plot(data, title="Simplest possible plotting example")

#data = np.random.normal(size=(500,500))
#pg.image(data, title="Simplest possible image example")

if __name__ == '__main__':
    pg.exec()