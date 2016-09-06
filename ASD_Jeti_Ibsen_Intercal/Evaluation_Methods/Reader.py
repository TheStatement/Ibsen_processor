'''
Created on 27.07.2016

@author: ried_st
'''


import numpy as np
import os
import matplotlib.pyplot as plt



class File_Reader(object):
    def __init__(self):
        pass
    
    
    def read_ibsen_data(self, directory, filename, file_extension):
        '''
        Input: input directory, input filename (eg: 'target001') and file extension (eg. '.asc')
        Output:
        ['data']
        ['number_columns']
        ['comment']
        ['int_time']
        ['header']
        '''

        input_filename = filename + file_extension
        ibsendata_directory = os.path.join(directory, input_filename)
        #ibsendata_directory_noextension = os.path.join(input_directory, filename)
        
        if file_extension == '.asc':
            WL_shift = 70
        else:
            WL_shift = 1
        
        data_matrix = []
        
        with open(ibsendata_directory, 'r') as ibsendata:
            searchlines = ibsendata.readlines()
            
        for i, line in enumerate(searchlines):
            if '[DataRaw]' in line: # metadata is collected
                beginning_data = i
                tmp = searchlines[i+1].split()
                number_columns = len(tmp) # gets the number of columns, eg 33 for 30 measurements
                header = searchlines[0:i+1]
            if '[DataCalibrated]' in line: # metadata is collected
                beginning_data = i
                tmp = searchlines[i+1].split()
                number_columns = len(tmp) # gets the number of columns, eg 33 for 30 measurements
                header = searchlines[0:i+1]
            if '[IntTime]' in line:
                int_time = int(searchlines[i+1].split()[0])
            if 'Comment' in line:
                comment = searchlines[i] # gets the line which contains the comment in the usual format
                
        for i, line in enumerate(searchlines):
            if (i>beginning_data + WL_shift): # only reads the relevant range (942 is lower limit, below plotting not sensible because of detector noise)
                row2 = np.array([float(w) for w in line.split()])
                data_matrix.append(row2)
        
        np_data = np.array(data_matrix)
        np_data = np.transpose(np_data) #columns contain the formatted data
        return({'data': np_data, 'wavelength': np_data[0], 'number_columns': number_columns, 'comment': comment, 'int_time': int_time, 'header': header})

    
    
    def read_jeti(self, directory, filename):
        data_matrix = []
        with open(os.path.join(directory, filename), 'r') as jetidata:
            searchlines = jetidata.readlines()
        
        time = searchlines[1].split()[2]
        int_time = searchlines[2].split()[2]
        
        for i, line in enumerate(searchlines):
            if i>65:
                row2 = np.array([float(w) for w in line.split()])
                data_matrix.append(row2)
        
        np_data = np.array(data_matrix)
        np_data = np.transpose(np_data) #columns contain the formatted data
        wavelength = np_data[0]
        return{'data': np_data, 'time': time, 'int_time': int_time, 'wavelength': wavelength}

    
    
    def read_asd_data(self, directory, filename):
        input_filename = filename + '.dat'
        asd_directory = os.path.join(directory, input_filename)
        #asddata_directory_noextension = os.path.join(input_directory, filename)
        
        
        data_matrix = []
        
        with open(asd_directory, 'r') as asddata:
            searchlines = asddata.readlines()
                
        for i, line in enumerate(searchlines):
            if i<500:
                row2 = np.array([float(w) for w in line.split()[1:4]])
                data_matrix.append(row2)
        
        np_data = np.array(data_matrix)
        np_data = np.transpose(np_data) #columns contain the formatted data
        wavelength = np_data[1] # test if this is true
        return({'data': np_data, 'wavelength': wavelength})