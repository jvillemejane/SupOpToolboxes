import os
os.environ["QT_API"] = "pyqt5"

# Importation de fichier hdf5
import h5py
# Biblio neurones /
import lib_neurones_Ncouches as neur
# Autres bibliothèques
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_circles
from sklearn.metrics import accuracy_score
# barre de progression
from tqdm import tqdm

X, y = make_circles(n_samples=1000, noise=0.1, factor=0.4, random_state=10)
X = X.T
y = y.reshape((1, y.shape[0]))

print('dimensions de X:', X.shape)
print('dimensions de y:', y.shape)

plt.scatter(X[0, :], X[1, :], c=y, cmap='summer')
plt.show()

(parametres, training_history) = neur.deep_neural_network(X, y, hidden_layers = (32, 64, 16), learning_rate = 0.02, n_iter = 3000)


# Prediction sur de nouvelles données
X_valid, y_valid = make_circles(n_samples=5, factor=0.3, noise=0.05, random_state=0)
X_valid = X_valid.T
y_valid = y_valid.reshape(1, y_valid.shape[0])

# affichage des échantillons X et de la nouvelle donnée
plt.figure()
plt.scatter(X[0, :], X[1, :], c=y, cmap='summer')
plt.scatter(X_valid[0,:], X_valid[1,:], c='r')
# affichage courbe de décision
plt.show()

print("Predictions : " + str(neur.predict(X_valid, parametres)))
print("Vraies Vals : " + str(y_valid))