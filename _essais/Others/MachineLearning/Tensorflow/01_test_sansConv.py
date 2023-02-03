import os
os.environ["QT_API"] = "pyqt5"

# Autre tutoriel pour Tensorflow
# Tutoriel : https://www.youtube.com/watch?v=hQ6pmoNZzU8

import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import pandas as pd

## Loading datas
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

print('Shape of train images')
print(train_images.shape[0])
print(train_images.shape)
print('Shape of train labels')
print(train_labels.shape)


## On ne prend qu'une partie des données
NN = input("Combien d'images pour l'entrainement ?")
while int(NN) > train_images.shape[0]:
    print("Valeur non possible")
    NN = input("Combien d'images pour l'entrainement ?")
train_images = train_images[:int(NN)]
train_labels = train_labels[:int(NN)]

print('After RESHAPE !!')
print('Shape of train images')
print(train_images.shape)
print('Shape of train labels')
print(train_labels.shape)

k = input('Waiting...')

## On normalise les données
max_img = train_images.max()
train_images = train_images / max_img
test_images = test_images / max_img

## Modele
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)), # images size - 28x28 -> 784x1
    keras.layers.Dense(512, activation=tf.nn.relu),      # couche intermédiaire
    keras.layers.Dense(256, activation=tf.nn.relu),      # couche intermédiaire
    keras.layers.Dense(128, activation=tf.nn.relu),      # couche intermédiaire
    keras.layers.Dense(64, activation=tf.nn.relu),      # couche intermédiaire
    keras.layers.Dense(10, activation=tf.nn.softmax)    # taille de sortie
])

## Compilation du modele
model.compile(optimizer=tf.keras.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

k = input('Waiting...')

## Training
history = model.fit(train_images, train_labels, epochs=10, validation_data=(test_images, test_labels))
# avec verication sur données test

## Affichage des couts au cours des epochs
def plot_learning_curves(history):
    pd.DataFrame(history.history).plot(figsize=(8,5))
    plt.grid(True)
    plt.gca().set_ylim(0,1)
    plt.show()
plot_learning_curves(history)

## Evaluation du modele
model.evaluate(test_images, test_labels)

## Prediction
y_proba = model.predict(test_images)
y_pred = y_proba.argmax(axis=1)   # pour obtenir l'indice de la case max
y_pred