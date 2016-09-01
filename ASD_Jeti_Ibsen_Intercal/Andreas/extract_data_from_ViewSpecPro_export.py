'''
Created on 21.07.2016

@author: ried_st
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Andreas ASD\ASCII_data\with radiometric calibration'
filename = 'rawdata_radiometric cal.dat'



with open(os.path.join(directory, filename), 'r') as asddata:
    searchlines = asddata.readlines()

for i in range(0,56):
    tmp = []
    name = (searchlines[i*2151].split()[0]).split('.')[0] + '.dat'
    print(name)
    for n in range(0,2151):
        tmp.append(searchlines[i*2151+n].strip('\n').replace(',','.'))
    target = open(os.path.join(directory, name), 'w')
    target.writelines(["%s\n" % item  for item in tmp])
print(tmp)

    