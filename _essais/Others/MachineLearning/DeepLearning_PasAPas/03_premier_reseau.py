import os
os.environ["QT_API"] = "pyqt5"

# Perceptron Simple

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_circles
from sklearn.metrics import accuracy_score
import lib_neurones as nr
import lib_neurones_2couches as nr2c
aff = 0

# 2 Sets de variables X et Y de 100 échantillons de 2 grandeurs chacun
X, y = make_circles(n_samples=1000, noise=0.1, factor=0.3, random_state=10)
y = y.reshape(y.shape[0], 1)

# Avec 1 neurone
if aff == 1:
    # affichage des informations des vecteurs x et y
    print('dimensions de X:', X.shape)
    print('dimensions de y:', y.shape)
    # affichage des échantillons X
    plt.scatter(X[:,0], X[:, 1], c=y, cmap='summer')
    plt.show()

    # Premier essai
    W, b = nr.artificial_neuron(X, y, 0.3, 100)

    # affichage des échantillons X et de la nouvelle donnée
    plt.scatter(X[:,0], X[:, 1], c=y, cmap='summer')
    # affichage courbe de décision
    x1 = np.linspace(-2, 2, 100)
    x2 = ( - W[0] * x1 - b) / W[1]
    plt.plot(x1, x2, c='orange', lw=3)
    plt.show()

# AVEC NOUVEAU RESEAU
X = X.T
y = y.reshape(1, y.shape[0])
# affichage des échantillons X
plt.scatter(X[0,:], X[1,:], c=y, cmap='summer')
plt.show()

parametres = nr2c.reseau_2couches(X, y, n1 = 3, n_iter = 5000, learning_rate = 0.05)