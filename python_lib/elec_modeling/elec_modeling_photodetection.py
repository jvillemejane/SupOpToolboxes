# -*- coding: utf-8 -*-
"""
Numerical Methods for Maths and Physics

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01

Adapted from Francois Marquier / ENS Paris-Saclay
"""

from scipy import fftpack
import numpy as np


def bisection(F,a,b,tol):
    """ bisection calculates the approximative value of a root of the function
    by bisection method
    (dichotomie in French)
    
    :F: mathematical function 
    :a: start value
    :b: stop value
    :tol: calculation tolerance
    :return: approximative value of the root, iteration number
    """
    if F(a)*F(b) >0:
        return print("erreur : il faut agrandir l'intervalle")
    else:
        i = 0
        x = a
        while(abs(F(x))>tol and i < 100): # maximum iteration = 100
            x = (a+b)/2
            if F(x)*F(b)<0:
                a = x
            else:
                b = x
            i+=1
    return x, i


def newton_find_root(F, dF, x0, tol):
    """ newton_find_root calculates the approximative value of a root of the 
    function by the Newton method
    
    :F: mathematical function 
    :dF: derivate of the function F
    :x0: initial value
    :tol: calculation tolerance
    :return: approximative value of the root, iteration number
    """  
    i = 0
    x = x0
    while(abs(F(x))>tol and i < 100): # maximum iteration = 100
        y, dy = F(x),dF(x)
        dx = -y/dy
        x = x + dx
        i+=1
    return x, i