import os
os.environ["QT_API"] = "pyqt5"

# Perceptron Simple - Application à la détection de chat et de chien
# Modèle pas assez complexe car 1 seul neurone...


# Importation de fichier hdf5
import h5py
# Biblio neurones /
import lib_neurones as nr
# Autres bibliothèques
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.metrics import accuracy_score
# barre de progression
from tqdm import tqdm




def load_data(dirName):
    train_dataset = h5py.File(dirName+'/trainset.hdf5', "r")
    X_train = np.array(train_dataset["X_train"][:]) # your train set features
    y_train = np.array(train_dataset["Y_train"][:]) # your train set labels

    test_dataset = h5py.File(dirName+'/testset.hdf5', "r")
    X_test = np.array(test_dataset["X_test"][:]) # your train set features
    y_test = np.array(test_dataset["Y_test"][:]) # your train set labels

    return X_train, y_train, X_test, y_test

# Data set - lecture des fichiers HDF5
X_train, y_train, X_test, y_test = load_data('chat_chien')

# affichage des informations des vecteurs x et y
print('dimensions de X:', X_train.shape)
print('dimensions de y:', y_train.shape)
print(len(X_train))

# Affichage des premières images
plt.figure(figsize=(16, 8))
for i in range(1, 11):
    plt.subplot(2, 5, i)
    plt.imshow(X_train[i], cmap='gray')
    if y_train[i] == 1:
        plt.title('Chien')
    else:
        plt.title('Chat')
plt.show()

# Préparation des données
# 1 - normalisation (0-255 --> 0 - 1)
# Utilisation Normalisation MinMax - pour chaque pixel
# p = p - pmin / (pmax - pmin)
max_train = X_train.max()
X_train = X_train / max_train
X_test = X_test / max_train     # Attention l'entrainement est fait avec le max de X_train
# 2 - passage de 64x64 à 4096*1
X_train_reshape = X_train.reshape(X_train.shape[0], X_train.shape[1] * X_train.shape[2])
X_test_reshape = X_test.reshape(X_test.shape[0], X_test.shape[1] * X_test.shape[2])

print(X_train_reshape.max())

# Attention ! Si réseau faisant des pas d'apprentissage, possibilité d'oscillation dans la fonction de cout...
# Réduire le taux d'apprentissage...

# Premier entrainement
WB, bB = nr.artificial_neuron_test(X_train_reshape, y_train, X_test_reshape, y_test, 0.05, 1000, 10)





