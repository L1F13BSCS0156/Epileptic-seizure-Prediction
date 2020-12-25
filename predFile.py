# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:00:54 2020

@author: LENOVO
"""

import tensorflow.keras as k
# from sklearn.metrics import confusion_matrix
from datagenerator import DataGenerator
import pandas as pd
import numpy as np

model = k.models.load_model("E:\\hard stuff\\ucp folders\\Project\\Code\\Parallel\\classesmodeloriginal\\modelclassesFunctionalFIVE - Copy1epoc")

csvfile = pd.read_csv("E:\\hard stuff\\ucp folders\\Project\\Dataset\\DATAGENERATION\\300\\chb 300.csv")    

#separate names and labels from pandas datagram
names = csvfile.Filename
labels = csvfile.Five       #dataset col
names = np.array(names)
labels = np.array(labels)

path = 'E:\\hard stuff\\ucp folders\\Project\\Dataset\DATAGENERATION\\300\\1-3\\'

#prediction variables
pred_names = names[(int(np.ceil(0.8 * len(csvfile.Filename)))+50):(int(np.ceil(0.8 * len(csvfile.Filename)))+50+1200)]
y_pred = labels[(int(np.ceil(0.8 * len(csvfile.Filename)))+50):(int(np.ceil(0.8 * len(csvfile.Filename)))+50+1200)]

pred_generator = DataGenerator(pred_names, y_pred, path, shuffle=False, batch_size=20, dim=(18,76800))

result = model.predict(pred_generator)
print('length of y_pred=',len(y_pred))
print('length of result=',len(result))
for i in range(0,1200):
    print('y=',y_pred[i],'res=',result[i][0])
    
    
    