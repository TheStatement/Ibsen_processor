'''
Created on 08.08.2016

@author: ried_st
'''

import os
import numpy as np
from scipy import interpolate
from scipy import ndimage
import matplotlib.pyplot as plt
from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate
from sympy.physics.units import length
from scipy.signal.signaltools import wiener
from signal import signal


reader = Reader.File_Reader()
spectralon = spectralon_response.Interpolate_Spectralon()
ibsen_evaluate = Ibsen_evaluate.Ibsen_Evaluation()


ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\test'
ref00 = reader.read_ibsen_data(ibsen_directory, 'reference000')
dark = reader.read_ibsen_data(ibsen_directory, 'darkcurrent000')
wavelength =  ref00[0][0]


data = np.empty((0,len(wavelength)), int)
int_times = []
for file in os.listdir(ibsen_directory):
    if file.endswith('.asc') and 'reference' in file:
        filename, file_extension = os.path.splitext(file)
        ref = reader.read_ibsen_data(ibsen_directory, filename)
        dark = reader.read_ibsen_data(ibsen_directory, 'darkcurrent' + filename.strip('reference'))
        int_times.append(ref[3])
        
        result = (ref[0][1] - dark[0][1])
        data = np.vstack([data, result])
        
        
data = np.transpose(data)[31:953]


fig = plt.figure(figsize=(18, 10))
# liste = np.append([data[0]], [1050])
# liste = np.sort(liste)
# ergebnis = np.interp(1050, data[0], int_times)
# print(int_times)
# print(ergebnis)
all_values = []
all_nonlin = []
for i in range(0,922): #921 or 922
    DN_values = np.append([data[i]], [1050]) # 1050 is appended to int-time series of channel i
    DN_values = np.sort(DN_values) # values are sorted for size to enable interpolation
    interpol = np.interp(1050, data[i], int_times) # interpolates a fake int time
    tmp_int_time = np.sort(np.append([int_times], [interpol]))
    result = np.divide(DN_values, tmp_int_time)*interpol/1050
    result2 = [result, DN_values]
    
    plt.plot(DN_values, result, marker='x', linestyle='')
    all_values = np.append(all_values, DN_values)
    all_nonlin = np.append(all_nonlin, result)
    

plt.xlabel('Raw DN', fontsize = 18)
plt.ylabel('Expected DN normalized to 1050 DN', fontsize = 18)
#legend = plt.legend(ncol = 2)


all_array = [all_values, all_nonlin]
all_array = np.transpose(all_array)
all_tuple = tuple(all_array)
all_sorted = sorted(all_tuple, key=lambda tup: tup[0])
all_sorted = np.transpose(list(all_sorted))

x = all_sorted[0]
y = all_sorted[1]

def kernel(x, shift, sigma):
    return np.exp(-((x-shift)**2/(2*sigma**2))) 

sigma = 1000
res = []
xnew = np.arange(min(x), max(x), 500)
for i in xnew:
    res.append(np.sum(kernel(x, i, sigma)*y)/ np.sum(kernel(x, i, sigma)))
res = np.array(res)


plt.plot(xnew, res, marker='o', linestyle='-')

plt.show()
plt.close()

array_write = np.transpose([xnew, res])
#np.savetxt(fname = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\results\nonlinearity_high.dat', X = array_write, fmt = '%10.5f', delimiter = ' ')
