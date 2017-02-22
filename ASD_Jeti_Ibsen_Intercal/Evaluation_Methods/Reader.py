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
    
    
    def read_ibsen_data(self, directory, lower_wavelength, filename, file_extension):
        '''
        Input: input directory, input filename (eg: 'target001') and file extension (eg. '.asc')
        Output:
        ['data'] (before: [0][1])
        ['data_raw']: only raw data without wavelength, mean and std before
        ['mean']: mean of all data
        ['std']: standard deviation of all data
        ['wavelength'] (before: [0][0])
        ['number_columns']
        ['comment']
        ['int_time'] (before: [3])
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
                comment = searchlines[i][8:] # gets the line which contains the comment in the usual format
            if 'Time' in line:
                if '[IntTime]' not in line:
                    time = searchlines[i][5:13]
                else:
                    time = 'early measurement, time not yet in file'
                
        for i, line in enumerate(searchlines):
            if (i>beginning_data + WL_shift): # only reads the relevant range (942 is lower limit, below plotting not sensible because of detector noise)
                row2 = np.array([float(w) for w in line.split()])
                data_matrix.append(row2)
        
        np_data = np.array(data_matrix)
        np_data = np.transpose(np_data) #columns contain the formatted data
        
        lower_wl = min(np_data[0], key=lambda x:abs(x-float(lower_wavelength))) #find closest WL to lower reading border
        lower_wl_position = int(np.where(np_data[0]==lower_wl)[0]) # returns integer with position of lower_wl
        np_data = np_data[:, lower_wl_position:] # cuts data to desired shape (lower_wl to max WL)
        
        return({'data': np_data, 'data_raw': np_data[3:number_columns], 'wavelength': np_data[0], 'mean': np_data[1], 'std': np_data[2], 'number_columns': number_columns, 'comment': comment, 'int_time': int_time, 'header': header, 'time': time})

    
    
    def read_jeti(self, directory, filename, file_extension):
        data_matrix = []
        filename = filename + file_extension
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
        data = np_data[1]
        return{'data': data, 'time': time, 'int_time': int_time, 'wavelength': wavelength}

    
    
    def read_asd_data(self, directory, filename, file_extension, wavelength_cutoff):
        if wavelength_cutoff != '':
            wavelength_cutoff = int(wavelength_cutoff) - 350
        input_filename = filename + file_extension
        asd_directory = os.path.join(directory, input_filename)
        #asddata_directory_noextension = os.path.join(input_directory, filename)
        
        
        data_matrix = []
        if file_extension == '.dat' or file_extension == '.asc':
            with open(asd_directory, 'r') as asddata:
                searchlines = asddata.readlines()
                    
            for i, line in enumerate(searchlines):
                if wavelength_cutoff != '': # should work like: if empty read all wavelengths
                    if i<wavelength_cutoff:
                        row2 = np.array([float(w) for w in line.split()[1:4]])
                        data_matrix.append(row2)
                else:
                    row2 = np.array([float(w) for w in line.split()[1:4]])
                    data_matrix.append(row2)
            np_data = np.array(data_matrix)
            np_data = np.transpose(np_data) #columns contain the formatted data
            wavelength = np_data[1] # test if this is true
            np_data = np_data[2]
        if file_extension == '.ASDrrs':
            with open(asd_directory, 'r') as asddata:
                searchlines = asddata.readlines()
            for i, line in enumerate(searchlines):
                if '[Data_reflectance]' in line:
                    beginning_data = i
            for i, line in enumerate(searchlines):
                if i>beginning_data:
                    row = np.array([float(w) for w in line.split()])
                    data_matrix.append(row)                    
            tmp = np.array(data_matrix)
            tmp = np.transpose(tmp) #columns contain the formatted data
            wavelength = tmp[0]
            np_data = tmp[1]

        return({'data': np_data, 'wavelength': wavelength})