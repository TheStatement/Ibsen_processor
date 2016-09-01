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


ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\test'


fig = plt.figure(figsize=(18, 10))
for file in os.listdir(ibsen_directory):
    if file.endswith('.asc') and 'reference' in file:
        filename, file_extension = os.path.splitext(file)
        ref = reader.read_ibsen_data(ibsen_directory, filename)
        dark = reader.read_ibsen_data(ibsen_directory, 'darkcurrent' + filename.strip('reference'))
        print(ref[3])
        
        result = (ref[0][1] - dark[0][1])/ref[3]
        wavelength = ref[0][0]
        

        plt.plot(wavelength, result, label = ref[3])
        
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('DN', fontsize = 18)
legend = plt.legend(ncol = 2)
plt.show()
plt.close()


#extract nonlinearity
result_sum_all = []
int_times = []
max_DN = []
max_DN_normalized = []
for file in os.listdir(ibsen_directory):
    if file.endswith('.asc') and 'reference' in file:
        filename, file_extension = os.path.splitext(file)
        ref = reader.read_ibsen_data(ibsen_directory, filename)
        dark = reader.read_ibsen_data(ibsen_directory, 'darkcurrent' + filename.strip('reference'))
        
        ref_dark = ref[0][1] - dark[0][1]
        max_DN.append(np.amax(ref_dark))
        max_DN_normalized.append(np.amax(ref_dark/ref[3]))
        result = ref_dark/ref[3]
        result_sum = np.sum(result)
        result_sum_all.append(result_sum)
        int_times.append(ref[3])
        
        


result_sum_all = result_sum_all/np.mean(result_sum_all)

print(result_sum_all)
print(int_times)
print(np.transpose([int_times, result_sum_all]))

fig = plt.figure(figsize=(18, 10))
plt.plot(int_times, result_sum_all, marker='o', linestyle='-')
plt.xlabel('Integration time [ms]', fontsize = 18)
plt.ylabel('DN/(average*integration time)', fontsize = 18)
fig.suptitle('Integration time Ibsen nonlinearity', fontsize = 20)
plt.show()
plt.close()

#np.savetxt(os.path.join(input_directory, 'Ibsen_nonlinearity_factors.dat'), np.transpose([int_times, result_sum_all]), delimiter = ',')
max_DN_normalized = max_DN_normalized/np.mean(max_DN_normalized)

fig = plt.figure(figsize=(18, 10))
plt.plot(max_DN, result_sum_all, marker='o', linestyle='-', label = 'Integral over whole spectrum')
plt.plot(max_DN, max_DN_normalized, marker='o', linestyle='-', label = 'Max DN value')
plt.xlabel('Ibsen signal (max DN value)', fontsize = 18)
plt.ylabel('DN/(average*integration time)', fontsize = 18)
fig.suptitle('DN Ibsen nonlinearity', fontsize = 20)
legend = plt.legend(ncol = 2)
plt.show()
plt.close()
