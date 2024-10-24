# -*- coding: utf-8 -*-
"""Untitled21.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OuuQEB5TqA3WhyV3WKxPYKKa7c--DSJB
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

_URL="https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip"
zip_dir=tf.keras.utils.get_file("cats_and_dogs_filtered.zip", origin=_URL, extract=True)

base_dir= os.path.join(os.path.dirname(zip_dir),'cats_and_dogs_filtered')

#printing contents of base_dir
print(os.listdir(base_dir))

#spiliting data
train=os.path.join(base_dir,"train")
validation=os.path.join(base_dir,"validation")

print(os.listdir(train))

train_cats=os.path.join(train,"cats")
train_dogs=os.path.join(train,"dogs")

val_cats=os.path.join(validation,"cats")
val_dogs=os.path.join(validation,"dogs")

# len(os.listdir(train_cats))
# we have 1000 images in each training dir. and 500 inage in each validation directory

# augmentation of trainning data and normalizing validation data

train_data = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)
val_data = ImageDataGenerator(rescale=1./255)

#creating a DIRECTORY-ITERATOR object --which generates batches of augmented and preprocessed data during model training.
#This data generator will automatically read images from the specified train_dir, apply the data augmentation

train_generator = train_data.flow_from_directory(
        train,
        target_size=(150, 150),
        batch_size=20,
        class_mode='binary')
val_generator = train_data.flow_from_directory(
        validation,
        target_size=(150, 150),
        batch_size=20,
        class_mode='binary')

#is used to retrieve the next batch of images and their corresponding labels from the train_generator.
images_batch, labels_batch = train_generator.next()

#show images
aug_list=[]
for i in range(4):
  aug_list.append(train_generator[0][0][0])
  plt.imshow(aug_list[i])
  plt.show()



# NN architecture


from tensorflow.keras import layers
from tensorflow.keras import Model

from keras.layers import Conv2D,MaxPooling2D,\
     Dropout,Flatten,Dense,Activation,\
     BatchNormalization

model=tf.keras.Sequential()

model.add(Conv2D(32,kernel_size=(3,3),activation='relu',input_shape=(150,150,3)))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(64,kernel_size=(3,3),activation='relu'))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(128,kernel_size=(3,3),activation='relu'))
model.add(MaxPooling2D((2,2)))

model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1,activation='sigmoid'))

model.summary()

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=["accuracy"])

Epochs=100

history = model.fit_generator(
      train_generator,
      steps_per_epoch=100,
      epochs=Epochs,
      validation_data=val_generator,
      validation_steps=50,
      verbose=2
      )



#Epoch 100/100 - 23s - loss: 0.3556 - accuracy: 0.8475 - val_loss: 0.4775 - val_accuracy: 0.7710 - 23s/epoch - 230ms/step