# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 16:29:25 2020

@author: LENOVO
"""

import tensorflow.keras as k
# from sklearn.metrics import confusion_matrix
from datagenerator import DataGenerator
import pandas as pd
import numpy as np

model = k.models.load_model("E:\\hard stuff\\ucp folders\\Project\\Code\\Parallel\\classesmodeloriginal\\modelclassesFunctionalFIVEnormalized")

csvfile = pd.read_csv("E:\\hard stuff\\ucp folders\\Project\\Dataset\\DATAGENERATION\\300\\chb 300.csv")    

#separate names and labels from pandas datagram
names = csvfile.Filename
labels = csvfile.Five       #dataset col
names = np.array(names)
labels = np.array(labels)

path = 'E:\\hard stuff\\ucp folders\\Project\\Dataset\DATAGENERATION\\300\\1-3\\'

#separate names and labels from pandas datagram
names = csvfile.Filename
labels = csvfile.Five       #dataset col ///////////////////////////////////////////////////////////////////////
names = np.array(names)
labels = np.array(labels)

#training data variables for training generator
train_names = names[:int(np.ceil(0.8 * len(csvfile.Filename)))]
y_train = labels[:int(np.ceil(0.8 * len(csvfile.Filename)))]

#testing data variables for testing generator
test_names = names[int(np.ceil(0.8 * len(csvfile.Filename))):int(np.ceil(0.8 * len(csvfile.Filename)))+50]
y_test = labels[int(np.ceil(0.8 * len(csvfile.Filename))):int(np.ceil(0.8 * len(csvfile.Filename)))+50]




# Generators
training_generator = DataGenerator(train_names, y_train, path, shuffle=True ,batch_size=20, dim=(18,76800))
validation_generator = DataGenerator(test_names, y_test, path, shuffle=False, batch_size=20, dim=(18,76800))


#class weights
clas_weights= {0:0.5,
                1:84}

# Train model on dataset
out = model.fit(training_generator,
      validation_data=validation_generator, 
      class_weight=(clas_weights),
      epochs=1, workers=4)

model.save("modelclassesFunctionalFIVEnormalized")


'''
predict
length data= 2028
shape data= (2028,)
data generator class init function
length result= 2048
shape result= (2048, 1)
'''
#print("length result=",len(result))
#print("shape result=",np.shape(result))
