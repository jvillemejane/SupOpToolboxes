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

def printer():
    tempo = datetime.today()
    h,m,s = tempo.hour, tempo.minute, tempo.second
    print(f"{h}:{m}:{s}")


if __name__ == "__main__":
    tik = PerpetualTimer(0.1, printer)
    tik.start()