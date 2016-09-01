'''
Created on 23.07.2016

@author: ried_st
'''

import numpy as np
import os
import matplotlib.pyplot as plt



jeti_directory = r'C:\Users\ried_st\OneDrive\Austausch\Kampagnen\Interkalibrationskampagne\Andreas Jeti'

def read_jeti(filename):
    data_matrix = []
    with open(os.path.join(jeti_directory, filename), 'r') as jetidata:
        searchlines = jetidata.readlines()
    
    time = searchlines[1].split()[2]
    int_time = searchlines[2].split()[2]
    
    for i, line in enumerate(searchlines):
        if i>3:
            row2 = np.array([float(w) for w in line.split()])
            data_matrix.append(row2)
    
    np_data = np.array(data_matrix)
    np_data = np.transpose(np_data) #columns contain the formatted data
    return(np_data, time, int_time)

test = read_jeti('Jeti_1.dat')



for file in os.listdir(jeti_directory):
    if file.endswith('.dat'):
        filename, file_extension = os.path.splitext(file)
        jeti_data = read_jeti(filename + '.dat')
        fig = plt.figure(figsize=(18, 10))
        plt.plot(jeti_data[0][0], jeti_data[0][1])
        plt.xlabel('Wavelength [nm]', fontsize = 18)
        plt.ylabel('DN', fontsize = 18)
        fig.suptitle(filename)
        fig.savefig(os.path.join(jeti_directory, filename + '.png'))
        plt.close()