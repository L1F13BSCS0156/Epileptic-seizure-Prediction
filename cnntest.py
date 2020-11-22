# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 15:58:32 2020

@author: sohaib
"""
import tensorflow.keras as k
from datagenerator import DataGenerator

import tensorflow.keras.layers as kc
import numpy as np
import pandas as pd

#from sklearn.metrics import confusion_matrix
#import sklearn.metrics as skm
#import matplotlib.pyplot as plt

def getModel():
    m = k.Sequential()
    m.add(kc.Conv2D(18, (3,3), padding='same', activation='relu', input_shape=(18,76800,1)))
    m.add(kc.Conv2D(18,kernel_size=3, activation='relu'))
    
    m.add(kc.Flatten())
    m.add(kc.Dense(1, activation='relu'))
    m.summary()
    return m


#read csv
csvfile = pd.read_csv("E:\\hard stuff\\ucp folders\\Project\\Dataset\\DATAGENERATION\\300\\chb 300.csv")    

#randomize records
csvfile = csvfile.sample(frac=1).reset_index(drop=True)

#separate names and labels from pandas datagram
names = csvfile.Filename
labels = csvfile.Thirty       #dataset col
names = np.array(names)
labels = np.array(labels)



#training data variables for training generator
train_names = names[:int(np.ceil(0.8 * len(csvfile.Filename)))]
y_train = labels[:int(np.ceil(0.8 * len(csvfile.Filename)))]

#testing data variables for testing generator
test_names = names[int(np.ceil(0.8 * len(csvfile.Filename))):(int(np.ceil(0.8 * len(csvfile.Filename)))+50)]
y_test = labels[int(np.ceil(0.8 * len(csvfile.Filename))):(int(np.ceil(0.8 * len(csvfile.Filename)))+50)]

'''
#prediction variables
pred_names = names[(int(np.ceil(0.8 * len(csvfile.Filename)))+50):]
y_pred = labels[(int(np.ceil(0.8 * len(csvfile.Filename)))+50):]
'''

path = 'E:\\hard stuff\\ucp folders\\Project\\Dataset\DATAGENERATION\\300\\1-3\\'

#batch_size = 20

# Generators
training_generator = DataGenerator(train_names, y_train, path, shuffle=True ,batch_size=20, dim=(18,76800))
validation_generator = DataGenerator(test_names, y_test, path, shuffle=False, batch_size=20, dim=(18,76800))
#pred_generator = DataGenerator(pred_names, y_pred, path, shuffle=False, batch_size=32, dim=(18,76800))
#print(training_generator.__getitem__(5))

#model get
m = getModel()
m.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])#, k.metrics.TruePositives(),
#                                                                 k.metrics.TrueNegatives(),
#                                                                 k.metrics.FalsePositives(),
#                                                                 k.metrics.FalseNegatives()])

#m.fit(x = X_train, y=y_train,batch_size=10,epochs=3 )

# Train model on dataset
out = m.fit_generator( training_generator,
      validation_data=validation_generator,
      epochs=1, workers=4)

m.save("modelcnnsoftTHIRTY")
'''
result = m.predict_classes(pred_generator)
cm = confusion_matrix(y_pred,result)
plot_labels = ['seizure','no seizure']
skm.plot_confusion_matrix(cm,plot_labels)
'''
'''
#Confution Matrix and Classification Report
Y_pred = m.predict_generator(pred_generator, num_of_test_samples // batch_size+1)
#y_pred = np.argmax(Y_pred, axis=1)
print('Confusion Matrix')
print(confusion_matrix(validation_generator.classes, y_pred))
print('Classification Report')
target_names = ['Cats', 'Dogs', 'Horse']
print(classification_report(validation_generator.classes, y_pred, target_names=target_names))
'''

