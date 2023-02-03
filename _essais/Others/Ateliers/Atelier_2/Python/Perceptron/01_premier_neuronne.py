import os
os.environ["QT_API"] = "pyqt5"

# Perceptron Simple
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_circles
from sklearn.metrics import accuracy_score
import lib_neurones as nr

# Data set
# 2 Sets de variables X et Y de 100 échantillons de 2 grandeurs chacun
X, y = make_blobs(n_samples=1000, n_features=2, centers=2, random_state=23)
y = y.reshape((y.shape[0], 1))

X_test, y_test = make_blobs(n_samples=100, n_features=2, centers=2, random_state=23)
y_test = y_test.reshape((y_test.shape[0], 1))

# affichage des informations des vecteurs x et y
print('dimensions de X:', X.shape)
print('dimensions de y:', y.shape)
# affichage des échantillons X
plt.figure()
plt.scatter(X[:,0], X[:, 1], c=y/10, cmap='copper')
plt.show()

# Premier essai
W, b, Wfinal = nr.artificial_neuron_test(X, y, X_test, y_test, learning_rate = 0.002, n_iter = 1000, pas_iter = 1)

# Prediction sur de nouvelles données
x_data, y_data = make_blobs(n_samples=5, n_features=2, centers=2, random_state=23)

# affichage des échantillons X et de la nouvelle donnée
plt.figure()
plt.scatter(X[:,0], X[:, 1], c=y, cmap='copper')
plt.scatter(x_data[:,0], x_data[:,1], c='r')
# affichage courbe de décision
x1 = np.linspace(0, 10, 100)
x2 = ( - W[0] * x1 - b) / W[1]
plt.plot(x1, x2, c='orange', lw=3)
plt.show()

# Prediction sur nouvel échantillon
print(nr.predict(x_data, W, b))
print(y_data)

plt.figure()
plt.plot(Wfinal)
plt.title('Evolution du premier parametre W')
plt.show()


