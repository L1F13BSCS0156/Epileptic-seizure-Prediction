# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 16:29:25 2020

@author: LENOVO
"""

import tensorflow.keras as k
import sklearn.metrics as skm
from sklearn.metrics import confusion_matrix
from datagenerator import DataGenerator
import pandas as pd
import numpy as np

model = k.models.load_model("E:\\hard stuff\\ucp folders\\Project\\Code\\generator\\modelfifteen")



csvfile = pd.read_csv("E:\\hard stuff\\ucp folders\\Project\\Dataset\\DATAGENERATION\\300\\chb 300.csv")    


#separate names and labels from pandas datagram
names = csvfile.Filename
labels = csvfile.Fifteen       #dataset col
names = np.array(names)
labels = np.array(labels)

#prediction variables
pred_names = names[(int(np.ceil(0.8 * len(csvfile.Filename)))+50):]
y_pred = labels[(int(np.ceil(0.8 * len(csvfile.Filename)))+50):]


path = 'E:\\hard stuff\\ucp folders\\Project\\Dataset\DATAGENERATION\\300\\1-3\\'
print("length data=",len(y_pred))
print("shape data=",np.shape(y_pred))
pred_generator = DataGenerator(pred_names, y_pred, path, shuffle=False, batch_size=32, dim=(18,76800))
#
#
#result = model.predict_generator(pred_generator)
result = model.predict(pred_generator)

print("length result=",len(result))
print("shape result=",np.shape(result))
#print("results=",result[:30])
#cm = confusion_matrix(y_pred,result)
#plot_labels = ['seizure','no seizure']
#skm.plot_confusion_matrix(cm,plot_labels)