'''
Created on 11.08.2016

@author: ried_st
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate



spectralon_function = spectralon_response.Interpolate_Spectralon()
reader = Reader.File_Reader()
evaluate = Ibsen_evaluate.Ibsen_Evaluation()

class Ibsen_Level1_Processor(object):
    def __init__(self):
        pass

    def ibsen_level1_processor(self, dark_current, target, spectralon, input_directory, output_directory):
        '''
        implement use of winnowed darkcurrent
        return same values as read_ibsen or write to file (fileending .ibsenL1)

        '''
            
        nonlinearity = np.genfromtxt(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\results\nonlinearity_gesamt.dat', delimiter = '    ')
        nonlinearity = np.transpose(nonlinearity) #nonlinearity[0] = DN values; nonlinearity[1] = correction factors
        
        ibsen_response = np.genfromtxt(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\results\ibsen_response.dat')
        ibsen_response = np.transpose(ibsen_response)
        
        tar = reader.read_ibsen_data(input_directory, target, '.asc') # read the target file
        if dark_current != '':
            dark = reader.read_ibsen_data(input_directory, dark_current, '.asc') # read the darkcurrent file
            dark_winnowed = evaluate.winnow_spectra(input_directory, dark_current, '.asc', std_plus = 2, std_minus = 2, std_r2 = 1.5)
            for i in range(2, tar[1]):
                #tar[0][i] = tar[0][i]-dark[0][1] #subtracts the darkcurrent average from each individual target measurement
                tar[0][i] = tar[0][i]-dark_winnowed[2] #subtracts the darkcurrent average from each individual target measurement


        for i in range(2, tar[1]): #tar[1] contains number of rows of the target file
            for j in range(0, len(tar[0][i])): #tar[0][i] contains one spectrum of the (usually 30) measurements in one file
                tar[0][i][j] = tar[0][i][j]/np.interp(tar[0][i][j], nonlinearity[0], nonlinearity[1]) #nonlinearity correction for each element, tar[0][i][j] contains a single number (corresponding to a wavelength of the spectrum)
            if spectralon == 'y':
                spectralon_resampled = spectralon_function.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', tar[0][i])
                tar[0][i] = np.divide(tar[0][i], spectralon_resampled[0])
            tar[0][i] = tar[0][i]/tar[3] # tar[3] contains the integration time, this step normalizes to 1ms
            tar[0][i] = np.multiply(tar[0][i], np.interp(tar[0][0], ibsen_response[0], ibsen_response[1])*10**-6) # mutiplies with the inverse ibsen response, converts units from W/m^3.sr to mW/m^2.nm.srM correction factor is 10**-6

        tar_transpose = np.transpose(tar[0])
        for i in range(0, len(tar[0][0])):
            tar[0][1][i] = np.mean(tar_transpose[i][3:tar[1]]) # new mean
            tar[0][2][i] = np.std(tar_transpose[i][3:tar[1]]) # new std
            
        #process header, change lines in header according to raw -> level 1
        tar[4][0] = '[Data calibrated] \nProcessed with: Ibsen_level1_processor Version 1.0 by Sebastian Riedel \nUsed dark current: ' + dark_current + ' with integration time ' + str(dark[3]) + '\n \n'
        tar[4][17] = '[DataCalibrated] [mW/m^2.nm.sr] [columns: wavelength [nm], mean, standard deviation, ' + str(tar[1]-3) + 'x data] \n'
        
        if os.path.isdir(output_directory) == False: # check if output directory exists
            os.makedirs(output_directory) # and create if not
            
        array_write = np.transpose(tar[0])
        file = open(os.path.join(output_directory, target + '.ibsenL1'), 'w')
        file.writelines(["%s" % item  for item in tar[4]])
        for row in array_write:
            row.tofile(file, sep='\t',format="%.4f")
            file.write('\n')



        
        
        
# level1 = Ibsen_Level1_Processor()
# result = level1.ibsen_level1_processor('darkcurrent001', 'target001', r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\test3', r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\test3')

# short validation of processor

# before = reader.read_ibsen_data(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\test3', 'target001', '.asc')
# dark = reader.read_ibsen_data(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\test3', 'darkcurrent001', '.asc')
# after = reader.read_ibsen_data(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\test3', 'target001', '.ibsenL1')
# tar_before = before[0][1] - dark[0][1]
#  
# ibsen_response = np.genfromtxt(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\results\ibsen_response.dat')
# ibsen_response = np.transpose(ibsen_response)
# check = np.multiply(tar_before, np.interp(before[0][0], ibsen_response[0], ibsen_response[1]))
#  
# fig = plt.figure(figsize=(18, 10))
# plt.plot(before[0][0], tar_before/max(tar_before), marker='', linestyle='-', label = 'before')
# plt.plot(after[0][0], after[0][1]/max(after[0][1]), marker='', linestyle='-', label = 'after')
# plt.plot(before[0][0], check/max(check), marker='', linestyle='-', label = 'check')
# legend = plt.legend(ncol = 1, loc = 2)
# plt.show()
# plt.close()