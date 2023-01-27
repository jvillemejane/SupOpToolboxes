# -*- coding: utf-8 -*-
"""
First application with Threads 
    

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Tue Jan 26 20:34:05 2023

@author: julien.villemejane
@see https://realpython.com/intro-to-python-threading/
"""

import logging
import threading
import time


def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    th_x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    th_x.start()       # Start thread
    logging.info("Main    : wait for the thread to finish")
    th_x.join()        # Wait until thread is ended / Blocking function
    logging.info("Main    : all done")
