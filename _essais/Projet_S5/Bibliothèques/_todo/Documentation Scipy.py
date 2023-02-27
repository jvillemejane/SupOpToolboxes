#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 11:23:49 2023

@author: abouhydroxyde
"""

# Bibliothèque Scipy
# SciPy est une bibliothèque Python a usage scientifique notamment mathématiques très utilisée en ingénierie.
#L'algèbre linéaire traite des équations linéaires et de leurs représentations à l'aide d'espaces vectoriels et de matrices. SciPy est construite sur les bibliothèques ATLAS LAPACK et BLAS et est extrêmement rapide pour résoudre les problèmes liés à l'algèbre linéaire.


# 1) L'algèbre linéaire sur Scipy
#       1.a) Mathématiquement, l'inverse d'une matrice A est la matrice B telle que AB = I où I est la matrice d'identité. L'inverse est noté B = A^-1. Dans SciPy, cet inverse peut être obtenu en utilisant la méthode inv() exemple :
import numpy as np
from scipy import linalg
A = np.array([[2,0], [1,5]])
B = linalg.inv(A)
print(B) 

        #1.b) Pour calculer le déterminant d'une matrice carrée, on utilis la fonction det() comme l'exemple suivant :
import numpy as np
from scipy import linalg
A = np.array([[3,5], [2,4]])
d = linalg.det(A)
print(d) # affiche: 2.0000000000000018

        #1.c) Fonctions de matrices 
linalg.expm() #est la commande donnant l'exponentielle d'une matrice
linalg.logm() #est la commande donnant le logarithme d'une matrice 
linalg.sinm, linalg.cosm, linalg.tanm #fonctions trigonométriques de matrices 
sqrtm(A[, disp, taille]) # renvoie la racinne carrée de la matrice 

        #1.d) Solveurs 
solve_sylvester(a, b, q) #résouds l'équation (AX+BX)=Q



# 2) La bibliothèque scipy.fft (fast fourier transform) permet de manipuler les trasnformées de fourier 
from scipy.fft import fft, ifft
import numpy as np
x = np.array([1.0, 2.0, 1.0, -1.0, 1.5])
y = fft(x)
# en appelant y on affiche la transformée de fourier des nombres dans le tableau x comme suit :
    y
array([ 4.5       +0.j        ,  2.08155948-1.65109876j,
       -1.83155948+1.60822041j, -1.83155948-1.60822041j,
        2.08155948+1.65109876j])
>>> yinv = ifft(y)
>>> yinv
array([ 1.0+0.j,  2.0+0.j,  1.0+0.j, -1.0+0.j,  1.5+0.j])
# ifft(y) est la commande permettant de faire la transformée de fourier inverse 

    #2.2) visualisation des parties réelles et imaginaires de la transformée de Fourier
import numpy as np
import matplotlib.pyplot as plt

n = 20

# definition de a
a = np.zeros(n)
a[1] = 1

# visualisation de a
# on ajoute a droite la valeur de gauche pour la periodicite
plt.subplot(311)
plt.plot( np.append(a, a[0]) )

# calcul de A
A = np.fft.fft(a)

# visualisation de A
# on ajoute a droite la valeur de gauche pour la periodicite
B = np.append(A, A[0])
plt.subplot(312)
plt.plot(np.real(B))
plt.ylabel("partie reelle")

plt.subplot(313)
plt.plot(np.imag(B))
plt.ylabel("partie imaginaire")

plt.show()
# On peut également afficher la transformée de Fourier accompagnée d'une échelle colorée
#On rappelle que sur MATLAB, cette opération se fait en un seul clic une fois la transformée affichée.
# Affichage de la grille colorée
import numpy as np
import matplotlib.pyplot as plt

n = 20

# definition de a
a = np.zeros(n)
a[1] = 1

# visualisation de a
# on ajoute a droite la valeur de gauche pour la periodicite
plt.subplot(211)
plt.plot( np.append(a, a[0]) )

# calcul de k
k = np.arange(n)

# calcul de A
A = np.fft.fft(a)

# visualisation de A - Attention au changement de variable
# on ajoute a droite la valeur de gauche pour la periodicite
plt.subplot(212)
x = np.append(k, k[-1]+k[1]-k[0]) # calcul d'une valeur supplementaire
z = np.append(A, A[0])
X = np.array([x,x])

y0 = np.zeros(len(x))
y = np.abs(z)
Y = np.array([y0,y])

Z = np.array([z,z])
C = np.angle(Z)

plt.plot(x,y,'k')

plt.pcolormesh(X, Y, C, shading="gouraud", cmap=plt.cm.hsv, vmin=-np.pi, vmax=np.pi)
plt.colorbar()

plt.show()
# En voici un exemple cette fois avec un cosinus :
import numpy as np
import matplotlib.pyplot as plt

n = 20

# definition de a
m = np.arange(n)
a = np.cos(m * 2*np.pi/n)

# visualisation de a
# on ajoute a droite la valeur de gauche pour la periodicite
plt.subplot(311)
plt.plot( np.append(a, a[0]) )

# calcul de A
A = np.fft.fft(a)

# visualisation de A
# on ajoute a droite la valeur de gauche pour la periodicite
B = np.append(A, A[0])
plt.subplot(312)
plt.plot(np.real(B))
plt.ylabel("partie reelle")

plt.subplot(313)
plt.plot(np.imag(B))
plt.ylabel("partie imaginaire")

plt.show()
# 3) Transformées de Fourier discrètes : Fonction FFTFREQ
#numpy.fft.fftfreq renvoie les fréquences du signal calculé dans la transformée de Fourier discrète 
import numpy as np
import matplotlib.pyplot as plt

# definition du signal
dt = 0.1
T1 = 2
T2 = 5
t = np.arange(0, T1*T2, dt)
signal = 2*np.cos(2*np.pi/T1*t) + np.sin(2*np.pi/T2*t)

# affichage du signal
plt.subplot(211)
plt.plot(t,signal)

# calcul de la transformee de Fourier et des frequences
fourier = np.fft.fft(signal)
n = signal.size
freq = np.fft.fftfreq(n, d=dt)

# affichage de la transformee de Fourier
plt.subplot(212)
plt.plot(freq, fourier.real, label="real")
plt.plot(freq, fourier.imag, label="imag")
plt.legend()

plt.show()
















