# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 10:39:46 2020

@author: sohaib
"""

import tensorflow.keras as k
#import tensorflow.keras.layers as kc
import numpy as np

class DataGenerator(k.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, labels, dir_path, batch_size=25, dim=(18,76800), n_channels=1, n_classes=2, shuffle=True):
        'Initialization'
        print("data generator class init function")
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()
        self.path = dir_path

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.ceil(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
   
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        # Generate data
        X, y = self.__data_generation(list_IDs_temp,self.path)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp, path):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, *self.dim))#, self.n_channels))
        y = np.empty((self.batch_size), dtype=int)

        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            X[i,] = np.load(path + ID + '.npy')

            # Store class
            y[i] = self.labels[i] #[ID]
                        
#        X = np.array(X)
#        y = np.array(y)
        X = np.expand_dims(X, -1)            
        return X, y   # k.utils.to_categorical(y, num_classes=self.n_classes)
