from pyedflib import highlevel
import numpy as np
import pandas as pd
import math
import csv
import os

# for making csv great again
#with open('/pythonwork/thefile_subset11.csv', 'w', newline='') as outfile:
#    writer = csv.writer(outfile)


# you can change file saving directory here 
current_dir_path = "C:/Users/LENOVO/Desktop/npydata/300/"

csvname = 'chb 300.csv'
# declaring things
fs = 256
duration = 300
df = pd.read_csv('FYP.csv')

# checking seizure is present or not is csv file
def checkseizure(n1):
    if math.isnan(n1):
        result = 'no'
    else:
        result = df['Starttime'][pfile]
    return result

# swap channels to make it same as chb1
def swapchannels(channels):
    channels[[8, 10]] = channels[[10, 8]]
    channels[[9, 11]] = channels[[11, 9]]
    channels[[10, 12]] = channels[[12, 10]]
    channels[[11, 13]] = channels[[13, 11]]
    channels[[12, 14]] = channels[[14, 12]]
    channels[[13, 15]] = channels[[15, 13]]
    channels[[14, 16]] = channels[[16, 14]]
    channels[[15, 17]] = channels[[17, 15]]
    return channels


# doing consistent channels
def consistentchannel(pattern, signals):
    channels = []

    if pattern == '1':
        consistent_data = signals

    if pattern == 'chb12-28':
        i = 0
        for x in signals:
            if i != 4 and i != 9 and i != 12 and i != 17 and i != 22:  # remove empty channels
                channels.append(x)
            i = i + 1
        channels = np.array(channels)
        consistent_data = swapchannels(channels)

    elif pattern == 'chb12-22':
        i = 0
        for x in signals:
            if i != 4 and i != 9 and i != 12 and i != 17:  # remove empty channels
                channels.append(x)
            i = i + 1
        channels = np.array(channels)
        consistent_data = swapchannels(channels)

    elif pattern == 'chb15':
        i = 0
        for x in signals:
            if i != 4 and i != 9 and i != 12 and i != 18 and i != 13 and i != 23:  # remove empty channels
                channels.append(x)
            i = i + 1
        channels = np.array(channels)
        consistent_data = swapchannels(channels)

    return consistent_data


# main duration selection and look ahead check code
def durationcode(signals, durations, seizuretime, pfile, syesorno):
    #intilizing things
    channels = []
    fs = 256
    i = 0
    inc = 0
    c = 0
    whole = 0
    chl = 1
    count = 1
    dstart = 0
    dend = durations
    lstart1 = dend
    lstart2 = dend
    lstart5 = dend
    lstart10 = dend
    lstart15 = dend
    lstart20 = dend
    lstart30 = dend
    lend1 = lstart1 + 60
    lend2 = lstart2 + 120
    lend5 = lstart5 + 300
    lend10 = lstart10 + 600
    lend15 = lstart15 + 900
    lend20 = lstart20 + 1200
    lend30 = lstart30 + 1800

    # checking seizure file or non seizure file and based on that change end time
    if syesorno == 'no':
        till = len(signals[0])
    else:
        seizurestime = int(seizuretime)
        till = fs * seizurestime

    # getting duration data till 18 channels till duration
    while count < till:
        for x in signals:
            channels.append(x)
            data = np.array(channels)[i][fs * dstart:fs * dend]

            # this is to check if non seizure file then save data
            if syesorno == 'no':
                    if inc == 0:
                        arr = np.array([data])
                    else:
                        arr = np.append(arr, [data], axis=0)

            # if seizure file then we have some checks then save data
            else:
                if fs * lstart1 <= fs * seizurestime <= fs * lend1:
                    if inc == 0:
                        arr = np.array([data])
                    else:
                        arr = np.append(arr, [data], axis=0)
                elif fs * lstart1 < fs * seizurestime and fs * lend1 < fs * seizurestime:
                    if inc == 0:
                        arr = np.array([data])
                    else:
                        arr = np.append(arr, [data], axis=0)

            # if channel is 18 then break
            if chl == 18:
                break
            inc = inc + 1
            i = i + 1
            chl = chl + 1

        # checking if there no seizure file then load till end and save file in npy
        if syesorno == 'no':
            name = df['Filename'][pfile] + '_' + str(whole)
            filename = os.path.join(current_dir_path, name)
            np.save(filename, np.asarray(arr))
            arr1 = np.load(filename + '.npy')
#            print arr1
#            print c
        # if seizure file then some so that program didnt save npy file over the seizure
        elif fs * lstart1 <= fs * seizurestime <= fs * lend1 or fs * lstart1 < fs * seizurestime and fs * lend1 < fs * seizurestime:
            name = df['Filename'][pfile] + '_' + str(whole)
            filename = os.path.join(current_dir_path, name)
            np.save(filename, np.asarray(arr))
            arr1 = np.load(filename + '.npy')
#            print arr1
#            print c

        # checking it seizure file or simple if simple straight away put no
        if syesorno == 'no':
            with open(csvname, 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([name, dstart, dend, 'no', 'no', 'no', 'no', 'no', 'no', 'no'])

        # if seizure file then we have to look for lookahead 60,120,300,600,900,1200,1800 to predict seizure
        else:
            if fs * lstart1 <= fs * seizurestime <= fs * lend1:
                l1='yes'
            if fs * lstart1 < fs * seizurestime and fs * lend1 < fs * seizurestime:
                l1='no'
            if fs * lstart2 <= fs * seizurestime <= fs * lend2:
                l2='yes'
            if fs * lstart2 < fs * seizurestime and fs * lend2 < fs * seizurestime:
                l2='no'
            if fs * lstart5 <= fs * seizurestime <= fs * lend5:
                l5='yes'
            if fs * lstart5 < fs * seizurestime and fs * lend5 < fs * seizurestime:
                l5='no'
            if fs * lstart10 <= fs * seizurestime <= fs * lend10:
                l10='yes'
            if fs * lstart10 < fs * seizurestime and fs * lend10 < fs * seizurestime:
                l10='no'
            if fs * lstart15 <= fs * seizurestime <= fs * lend15:
                l15='yes'
            if fs * lstart15 < fs * seizurestime and fs * lend15 < fs * seizurestime:
                l15='no'
            if fs * lstart20 <= fs * seizurestime <= fs * lend20:
                l20='yes'
            if fs * lstart20 < fs * seizurestime and fs * lend20 < fs * seizurestime:
                l20='no'
            if fs * lstart30 <= fs * seizurestime <= fs * lend30:
                l30='yes'
            if fs * lstart30 < fs * seizurestime and fs * lend30 < fs * seizurestime:
                l30='no'
            # checking if there no seizure file then load till end and save in csv file
            if syesorno == 'no':
                with open(csvname, 'a') as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',',
                                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([name, dstart, dend, l1, l2, l5, l10, l15, l20, l30])

            # if seizure file then some checks so that program didnt save csv after seizure data
            elif fs * lstart1 <= fs * seizurestime <= fs * lend1 or fs * lstart1 < fs * seizurestime and fs * lend1 < fs * seizurestime:
                with open(csvname, 'a') as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',',
                                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow([name, dstart, dend, l1, l2, l5, l10, l15, l20, l30])

        # some iterations of intilizing data
        whole = whole + 1
        inc = 0
        arr = []
        chl = 1
        c = c + 1
        i = 0
        channels = []
        count = fs * dend
        dstart = dstart + 60
        dend = dend + 60
        lstart1 = dend
        lstart2 = dend
        lstart5 = dend
        lstart10 = dend
        lstart15 = dend
        lstart20 = dend
        lstart30 = dend
        lend1 = lstart1 + 60
        lend2 = lstart2 + 120
        lend5 = lstart5 + 300
        lend10 = lstart10 + 600
        lend15 = lstart15 + 900
        lend20 = lstart20 + 1200
        lend30 = lend30 + 1800
#        print "--------------------------------------------------------"


# main
# if you stuck anywhere just change these below three variable
# for pfile look at # 0-41 first patient files,42-76 second patiient files and so on
# if you stuck in patient 4 just change patirnt to 4 and change pfile variable so
# that when program start again it doesnt start from patient 1
patientsfile = [41, 76, 114, 156, 195, 213, 232, 252, 271, 296, 331, 352, 385, 411, 451, 470, 491, 527, 557, 586, 619,
                650, 659, 671]



#patientsfile = [41, 76, 114, 156, 195, 213, 232, 252, 271, 296, 331, 354, 387, 413, 453, 472, 493, 529, 559, 588, 621,
#                652, 661, 673]  # 24 patients file size

pfile = 115    # starting  #157
patient = 4
patientfilecount = 3   #end point #4

while patient <= 4:
    while pfile <= patientsfile[patientfilecount]:
        signals, signal_headers, header = highlevel.read_edf("E:\\hard stuff\\ucp folders\\Project\\Dataset\\chb-mit-scalp-eeg-database-1.0.0\\"+'patient ' + str(patient) + "\\"+df['Filename'][pfile]+".edf")
        seizuretime = df['Starttime'][pfile]
        pattern = df['Pattern'][pfile]
        signals = consistentchannel(pattern, signals)
        syesorno = checkseizure(seizuretime)
        durationcode(signals, duration, seizuretime, pfile, syesorno)
        pfile = pfile + 1
#        print "-------------------------------------------------------------------------------"
    patient = patient + 1
    patientfilecount = patientfilecount + 1
