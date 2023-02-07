import os
os.environ["QT_API"] = "pyqt5"

# Perceptron Simple

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_circles
from sklearn.metrics import accuracy_score
import lib_neurones as nr
import lib_neurones_2couches as nr2c

# 2 Sets de variables X et Y de 100 échantillons de 2 grandeurs chacun
X, y = make_circles(n_samples=1000, noise=0.1, factor=0.3, random_state=10)
y = y.reshape(y.shape[0], 1)


# AVEC NOUVEAU RESEAU
X = X.T
y = y.reshape(1, y.shape[0])
# affichage des échantillons X
plt.scatter(X[0,:], X[1,:], c=y, cmap='summer')
plt.show()

parametres = nr2c.reseau_2couches(X, y, n1 = 3, n_iter = 5000, learning_rate = 0.1)

# Prediction sur de nouvelles données
x_data, y_data = make_circles(n_samples=5, factor=0.3, noise=0.05, random_state=0)

# affichage des échantillons X et de la nouvelle donnée
plt.figure()
plt.scatter(X[0,:], X[1,:], c=y, cmap='copper')
plt.scatter(x_data[:,0], x_data[:,1], c='r')
plt.show()

# Prediction sur nouvel échantillon
print(nr2c.predict(x_data.T, parametres))
print(y_data)
