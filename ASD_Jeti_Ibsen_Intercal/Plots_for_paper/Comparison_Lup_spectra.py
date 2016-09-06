'''
Created on 05.09.2016

@author: ried_st
'''
import numpy as np
import os
import matplotlib.pyplot as plt
from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate

'''
only L_up spectra are compared. Problem with Jeti: factor 10**5 too high, no idea where this comes from

'''
reader = Reader.File_Reader()
spectralon = spectralon_response.Interpolate_Spectralon()
ibsen_evaluate = Ibsen_evaluate.Ibsen_Evaluation()



# Jeti data reading section

jeti_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Andreas Jeti'
jeti_3 = reader.read_jeti(jeti_directory, 'Jeti_3.dat')['data']
jeti_4 = reader.read_jeti(jeti_directory, 'Jeti_4.dat')['data']
jeti_5 = reader.read_jeti(jeti_directory, 'Jeti_5.dat')['data']
jeti_6 = reader.read_jeti(jeti_directory, 'Jeti_6.dat')['data']
jeti_7 = reader.read_jeti(jeti_directory, 'Jeti_7.dat')['data']


wavelength_jeti = jeti_3[0]
spectralon_jeti = spectralon.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', wavelength_jeti)['resampled_spectralon']

# Ibsen data reading and processing section 

ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen_1 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target003', '.ibsenL1', 1.5, 1.5, 1.5)



# PLotting section

fig = plt.figure(figsize=(18, 10))
plt.plot(jeti_3[0], jeti_3[1]/100, marker='', color = 'b', linestyle='-', label = 'Jeti_3/10^5')
plt.plot(jeti_4[0], jeti_4[1]/100, marker='', color = 'b', linestyle='-', label = 'Jeti_4/10^5')
plt.plot(jeti_5[0], jeti_5[1]/100, marker='', color = 'b', linestyle='-', label = 'Jeti_5/10^5')
plt.plot(jeti_6[0], jeti_6[1]/100, marker='', color = 'b', linestyle='-', label = 'Jeti_6/10^5')
plt.plot(jeti_7[0], jeti_7[1]/100, marker='', color = 'b', linestyle='-', label = 'Jeti_7/10^5')


plt.plot(ibsen_1['wavelength'], ibsen_1['mean_good'], marker='', color = 'r', linestyle='-', label = 'target003')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Upwelling water radiance [mW/m^2.nm.sr]', fontsize = 18)
fig.suptitle('')
legend = plt.legend(ncol = 1, loc = 1)
plt.show()
#fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Paper_schreiben\Special Issue_Inland waters\Plots\Ibsen_response.png')
plt.close()

# ASD Section--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

