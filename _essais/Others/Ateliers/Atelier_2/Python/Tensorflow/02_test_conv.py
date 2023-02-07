import os
os.environ["QT_API"] = "pyqt5"

# Autre tutoriel pour Tensorflow - with CNN
# Tutoriel : https://www.youtube.com/watch?v=hQ6pmoNZzU8
# A convolutional neural network, or CNN, is a deep learning neural network sketched for processing structured arrays of data such as portrayals.

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import pandas as pd
import sys

## Loading datas
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

print(train_images.shape[0])


## On ne prend qu'une partie des données
NN = input("Combien d'images pour l'entrainement ?")
while int(NN) > train_images.shape[0]:
    print("Valeur non possible")
    NN = input("Combien d'images pour l'entrainement ?")
train_images = train_images[:int(NN)]
train_labels = train_labels[:int(NN)]
## On normalise les données
max_img = train_images.max()
train_images = train_images / max_img
test_images = test_images / max_img

train_images.shape
test_images.max()

## Modele
model = keras.Sequential()
model.add(tf.keras.layers.Conv2D(64, (3,3), activation=tf.nn.relu, input_shape=(28,28,1)))
model.add(tf.keras.layers.MaxPooling2D((2,2)))
model.add(tf.keras.layers.Conv2D(128, (3,3), activation=tf.nn.relu, input_shape=(28,28,1)))
model.add(tf.keras.layers.MaxPooling2D((2,2)))
model.add(tf.keras.layers.Conv2D(32, (3,3), activation=tf.nn.relu, input_shape=(28,28,1)))
model.add(tf.keras.layers.MaxPooling2D((2,2)))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(1024, activation='selu'))
model.add(keras.layers.Dense(512, activation='selu'))
model.add(keras.layers.Dense(256, activation='selu'))
model.add(keras.layers.Dense(128, activation='selu'))
model.add(keras.layers.Dense(10, activation=tf.nn.softmax))    # taille de sortie

## Compilation du modele
model.compile(optimizer=tf.keras.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

k = input('Waiting...')

## Training
history = model.fit(train_images, train_labels, epochs=20, steps_per_epoch=20, validation_data=(test_images, test_labels))
# avec verication sur données test
# steps per epochs : permet de mettre un pas de calcul de la validation
model.save('model.h5')

## Affichage des couts au cours des epochs
def plot_learning_curves(history):
    pd.DataFrame(history.history).plot(figsize=(8,5))
    plt.grid(True)
    plt.gca().set_ylim(0,1)
    plt.show()
# plot_learning_curves(history)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(acc))

plt.figure()
plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and Validation Accuracy')
plt.legend(loc=0)

plt.figure()
plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and Validation Accuracy')
plt.legend(loc=0)
plt.show()

## Evaluation du modele
print(model.evaluate(test_images, test_labels))

## Prediction
y_proba = model.predict(test_images)
y_pred = y_proba.argmax(axis=1)   # pour obtenir l'indice de la case max
print("Prediction : ",y_pred)
print("Valeur Réelle : ",train_labels)