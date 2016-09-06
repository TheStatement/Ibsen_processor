'''
Created on 05.09.2016

@author: ried_st
'''
import numpy as np
import os
import matplotlib.pyplot as plt
from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate




ibsen_response = np.genfromtxt(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\results\ibsen_response.dat')
ibsen_response = np.transpose(ibsen_response)


fig = plt.figure(figsize=(9, 6))
plt.plot(ibsen_response[0],ibsen_response[1]*10**6, marker='o', linestyle='-', label = 'Ibsen Spectrometer Response')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('DN/(mW/m^2.nm.sr)', fontsize = 18)
fig.suptitle('')
legend = plt.legend(ncol = 1, loc = 1)
plt.show()
#fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Paper_schreiben\Special Issue_Inland waters\Plots\Ibsen_response.png')
plt.close()