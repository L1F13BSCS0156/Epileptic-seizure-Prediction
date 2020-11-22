import pyedflib as edf
import numpy as np
import matplotlib.pyplot as plt
import scipy
#file = edf.EdfReader("E:\\hard stuff\\ucp folders\\Project\\chb01_01.edf")
file = edf.EdfReader("E:\\hard stuff\\ucp folders\\Project\\Dataset\\chb-mit-scalp-eeg-database-1.0.0\\chb12\\chb12_08.edf")

'''''
print(file.getSampleFrequency(22)) #frequency of eef (256 for this file)
print(file.getSignalLabels()) #labels in the file, codes in this file
print(file.readSignal(0,0,None,False))  #returns the signal physical data
'''''

def swapchannels(channels):
    # swap channels to make it same as chb1
    channels[[8, 10]] = channels[[10, 8]]
    channels[[9, 11]] = channels[[11, 9]]
    channels[[10, 12]] = channels[[12, 10]]
    channels[[11, 13]] = channels[[13, 11]]
    channels[[12, 14]] = channels[[14, 12]]
    channels[[13, 15]] = channels[[15, 13]]
    channels[[14, 16]] = channels[[16, 14]]
    channels[[15, 17]] = channels[[17, 15]]
    return channels

channels = []
# this is for chb12 format with 28-1 = 27 channels
for i in range(0,27):
    c = file.readSignal(i,0,None,False)
    if i != 4 and i != 9 and i != 12 and i != 17 and i != 22: #remove empty channels
        channels.append(c)

channels = np.array(channels)
consistent_data = swapchannels(channels)

#checked. correct.


# for chb12 format with 22 channels till P8-02
chan = []
for i in range(0,22):
    c = file.readSignal(i,0,None,False)
    if i != 4 and i != 9 and i != 12 and i != 17: #remove empty channels
        chan.append(c)

chan = np.array(chan)
consistent_data = swapchannels(chan)



'''
# for chb15 format with 29-1 channels
chan = []
for i in range(0,28):
    c = file.readSignal(i,0,None,False)
    if i != 4 and i != 9 and i != 12 and i != 18 and i != 13 and i != 23: #remove empty channels
        chan.append(c)

chan = np.array(chan)
consistent_data = swapchannels(chan)
'''