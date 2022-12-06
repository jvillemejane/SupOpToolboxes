# -*- coding: utf-8 -*-
"""
Symbolic Calculation - First Test

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-04
"""

import sympy as sp
from IPython.display import *

sp.init_printing(use_latex=True)

P0,PL,rho,mu,R,L,r= sp.symbols('P0,PL,rho,mu,R,L,r')

vz=(P0-PL)*R**2/(4*mu*L)*(1-(r/R)**2)
V=2*sp.pi*sp.integrate(vz*r,(r,0,R))/(2*sp.pi*sp.integrate(r,(r,0,R)))
Q=V*sp.pi*R**2
W=Q*rho

display(sp.simplify(W))
