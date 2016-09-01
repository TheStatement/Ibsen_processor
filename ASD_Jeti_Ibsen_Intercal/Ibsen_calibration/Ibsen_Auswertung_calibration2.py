'''
Created on 14.04.2016

@author: ried_st
'''

import os
import numpy as np
import matplotlib.pyplot as plt
from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate

reader = Reader.File_Reader()
spectralon = spectralon_response.Interpolate_Spectralon()
ibsen_evaluate = Ibsen_evaluate.Ibsen_Evaluation()

# passende Spektren auswaehlen
# nonlinearity Korrektur drueber laufen lassen
# in ein File schreiben
# Gauss filter drueber
# mit PTB Kurve verwursten
# abspeichern


ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\test2'
results_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\results'

nonlinearity = np.genfromtxt(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\results\nonlinearity_gesamt.dat', delimiter = '    ')
nonlinearity = np.transpose(nonlinearity) #nonlinearity[0] = DN values; nonlinearity[1] = correction factors

rasta_ptb = np.genfromtxt(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\results\2016-01_RASTA_1m_rawdata.dat')
rasta_ptb = np.transpose(rasta_ptb)

x = []
y = []
fig = plt.figure(figsize=(18, 10))
for file in os.listdir(ibsen_directory): # files from directory are parsed
    if file.endswith('.asc') and 'reference' in file:
        filename, file_extension = os.path.splitext(file)
        ref = reader.read_ibsen_data(ibsen_directory, filename, '.asc')
        dark = reader.read_ibsen_data(ibsen_directory, 'darkcurrent' + filename.strip('reference'), '.asc')
#         print(ref[0][1][0])
#         print(np.interp(ref[0][1][0], nonlinearity[0], nonlinearity[1]))
        for i in range(0, len(ref[0][1])):
            ref[0][1][i] = ref[0][1][i]/np.interp(ref[0][1][i], nonlinearity[0], nonlinearity[1]) #corrects for nonlinearity
            
        
        result = (ref[0][1] - dark[0][1])/ref[3]
        wavelength = ref[0][0]
        x = np.append(x, wavelength)
        y = np.append(y, result)
        plt.plot(wavelength, result, label = ref[3])
        
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('DN', fontsize = 18)
legend = plt.legend(ncol = 2)
#plt.show()
plt.close()


def kernel(x, shift, sigma):
    return np.exp(-((x-shift)**2/(2*sigma**2))) 

sigma = 1
res = []
xnew = np.arange(min(x), max(x), 6.02)
for i in xnew:
    res.append(np.sum(kernel(x, i, sigma)*y)/ np.sum(kernel(x, i, sigma)))
res = np.array(res)

fig = plt.figure(figsize=(18, 10))
plt.plot(x, y, marker='x', linestyle='')
plt.plot(xnew, res, marker='o', linestyle='-')
plt.show()
plt.close()

rasta_ptb_resample = np.interp(xnew, rasta_ptb[0], rasta_ptb[1])
ibsen_response = np.divide(rasta_ptb_resample, res)

fig = plt.figure(figsize=(18, 10))
plt.plot(xnew, ibsen_response/max(ibsen_response), marker='o', linestyle='-')
plt.plot(xnew, res/max(res), marker='o', linestyle='-')
plt.plot(rasta_ptb[0], rasta_ptb[1]/max(rasta_ptb[1]), marker='o', linestyle='-')
plt.show()
plt.close()

array_write = np.transpose([xnew, ibsen_response])
#np.savetxt(fname = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\results\ibsen_response.dat', X = array_write, fmt = '%10.5f', delimiter = ' ')
