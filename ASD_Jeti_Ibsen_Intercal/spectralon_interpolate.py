'''
Created on 27.07.2016

@author: ried_st
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from Evaluation_Methods import Reader, Ibsen_evaluate

reader = Reader.File_Reader()
ibsen_evaluate = Ibsen_evaluate.Ibsen_Evaluation()

spectralon_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung'

def interpolate_spectralon(filename, file):
    data_matrix = []
    with open(os.path.join(spectralon_directory, filename), 'r') as spectralondata:
        searchlines = spectralondata.readlines()
    
    
    for i, line in enumerate(searchlines):
        if i>9:
            row2 = np.array([float(w) for w in line.split()])
            data_matrix.append(row2)
    
    np_data = np.array(data_matrix)
    np_data = np.transpose(np_data) #columns contain the formatted data
    
    spectralon = np.interp(file, np_data[0], np_data[1])
    
    return([spectralon, np_data])


directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje'


ibsen_data = reader.read_ibsen_data(directory, 'target000')[0][0]
spectr = interpolate_spectralon('S1005_22590-41.dat', ibsen_data)
#print(spectr[0])

fig = plt.figure(figsize=(18, 10))
plt.plot(spectr[1][0], spectr[1][1], label = 'unresampled')
plt.plot(ibsen_data, spectr[0], label = 'resampled')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('Tiefwasser Boje, Ibsen vs ASD_unfertig', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 2)
plt.show()
#fig.savefig(os.path.join(r'C:\Users\ried_st\OneDrive\Austausch\Kampagnen\Interkalibrationskampagne\Andreas ASD\Auswertung\Plots', '1_reflectance_ASD_Ibsen_different_target.png'))
plt.close()


ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje'
ibsen = ibsen_evaluate.reflectance_winnowed(ibsen_directory, 'darkcurrent000', 'reference000', 'target000', std_dark = 2, std_ref = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')

fig = plt.figure(figsize=(18, 10))
plt.plot(ibsen[0], ibsen[2], label = 'resampled')
plt.plot(ibsen[0], ibsen[3]*10, label = 'unresampled*10')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('DN', fontsize = 18)
fig.suptitle('Random E_d spectrum with and without measured spectralon response', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 2)
plt.show()
#fig.savefig(os.path.join(r'C:\Users\ried_st\OneDrive\Austausch\Kampagnen\Interkalibrationskampagne\Andreas ASD\Auswertung\Plots', '1_reflectance_ASD_Ibsen_different_target.png'))
plt.close()
