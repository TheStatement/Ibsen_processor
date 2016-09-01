'''
Created on 27.07.2016

@author: ried_st
'''
import numpy as np
import os
import matplotlib.pyplot as plt


class Interpolate_Spectralon(object):
    def __init__(self):
        pass

    def interpolate_spectralon(self, directory, filename, file):
        '''
        input:
        directory = location of the spectralon data
        filename = name of the spectralon response file
        file = array, which contains the wavelengths, to which the spectralon response is supposed to be resampled
        
        output:
        spectralon = the spectralon response resampled to the desired wavelemghts
        np_data = the wavelengths (np_data[0]) and response (np_data[2]) of the original calibration file
        '''
        data_matrix = []
        with open(os.path.join(directory, filename), 'r') as spectralondata:
            searchlines = spectralondata.readlines()
        
        
        for i, line in enumerate(searchlines):
            if i>9:
                row2 = np.array([float(w) for w in line.split()])
                data_matrix.append(row2)
        
        np_data = np.array(data_matrix)
        np_data = np.transpose(np_data) #columns contain the formatted data
        
        spectralon = np.interp(file, np_data[0], np_data[1])
        
        return([spectralon, np_data])