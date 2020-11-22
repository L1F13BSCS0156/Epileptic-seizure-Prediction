# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 15:29:23 2020

@author: sohaib
"""

import pandas as pd
import numpy as np

#read csv
csvfile = pd.read_csv("E:\\hard stuff\\ucp folders\\Project\\Dataset\\DATAGENERATION\\300\\chb 300.csv")

csvfile = csvfile.sample(frac=1).reset_index(drop=True)

csvfile.to_csv("E:\\hard stuff\\ucp folders\\Project\\Dataset\\DATAGENERATION\\300\\300shuffled.csv")