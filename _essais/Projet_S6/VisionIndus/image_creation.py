# -*- coding: utf-8 -*-

from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import img_to_array, array_to_img, load_img

import os
from os import listdir, rename
import tqdm

datagen = ImageDataGenerator(       # initialisation de la classe qui va permettre de créer de nouvelles images
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest')

type_image = 'b' # TYPE IMAGE


img = load_img('r1_resize.png')  # chargement d'une image PIL
x = img_to_array(img)  # Array Numpy de dimensions (1080, 1080, 3)
x = x.reshape((1,) + x.shape)  # Array Numpy de dimensions (1, 1080, 1080, 3)

# la methode .flow() crée des images transformées (translatées, tournées, etc...) et les sauvegarde
i = 0
nb_images = 200
folder_dir = './resized'
for batch in datagen.flow(x, batch_size=32,seed=None,save_to_dir=folder_dir,save_prefix=type_image, save_format='ppm'):
    i += 1
    if i%20 == 0:
        ratio = i/nb_images*100
        print("Progression à :" + str(ratio) + "%")
    if i >= nb_images:
        break # stop quand on ne veut plus d'images

# Renommage de toutes les images
j = 1
for images in os.listdir(folder_dir):
    name_test = int(float(images[4:-4]))
    if name_test != j and name_test > j: # conditions pour avoir un bon ordre des noms des images
        new_name = type_image+"_"+str(j)+".ppm"
        try:
            os.rename(os.path.join(folder_dir, images), os.path.join(folder_dir, new_name))
        except FileExistsError:
            new_name = type_image+"_"+str(j+1)+".ppm"
            os.rename(os.path.join(folder_dir, images), os.path.join(folder_dir, new_name))
        j += 1
    else:
        continue
    
# Resize des images
from PIL import Image

for images in os.listdir(folder_dir):
    Image1 = Image.open('./resized/'+images)  # My image is a 200x374 jpeg that is 102kb large
    Image1 = Image1.resize((128,128),Image.LANCZOS)
    Image1.save('./resized_c/'+images, quality=95)  # The saved downsized image size is 24.8kb
