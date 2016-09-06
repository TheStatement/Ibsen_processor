'''
Created on 05.09.2016

@author: ried_st
'''
import numpy as np
import os
import matplotlib.pyplot as plt
from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate

'''
only Ed spectra are compared. Problem with Jeti: factor 10**5 too high, no idea where this comes from

'''
reader = Reader.File_Reader()
spectralon = spectralon_response.Interpolate_Spectralon()
ibsen_evaluate = Ibsen_evaluate.Ibsen_Evaluation()



# Jeti data reading section

jeti_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Andreas Jeti'
jeti_1 = reader.read_jeti(jeti_directory, 'Jeti_1.dat')['data']
jeti_2 = reader.read_jeti(jeti_directory, 'Jeti_2.dat')['data']

jeti_8 = reader.read_jeti(jeti_directory, 'Jeti_8.dat')['data']
jeti_9 = reader.read_jeti(jeti_directory, 'Jeti_9.dat')['data']
jeti_10 = reader.read_jeti(jeti_directory, 'Jeti_10.dat')['data']
jeti_11 = reader.read_jeti(jeti_directory, 'Jeti_11.dat')['data']

wavelength_jeti = jeti_1[0]
spectralon_jeti = spectralon.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', wavelength_jeti)['resampled_spectralon']

# Ibsen data reading and processing section 

ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen_1 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference003', '.ibsenL1', 1.5, 1.5, 1.5)
ibsen_2 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference004', '.ibsenL1', 1.5, 1.5, 1.5)


# PLotting section

fig = plt.figure(figsize=(18, 10))
plt.plot(jeti_1[0], jeti_1[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_1/10^5')
plt.plot(jeti_2[0], jeti_2[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_2/10^5')
plt.plot(jeti_8[0], jeti_8[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_8/10^5')
plt.plot(jeti_9[0], jeti_9[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_9/10^5')
plt.plot(jeti_10[0], jeti_10[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_10/10^5')
plt.plot(jeti_11[0], jeti_11[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_11/10^5')

plt.plot(ibsen_1['wavelength'], ibsen_1['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 1')
plt.plot(ibsen_2['wavelength'], ibsen_2['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 2')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Downwelling irradiance [mW/m^2.nm.sr]', fontsize = 18)
fig.suptitle('')
legend = plt.legend(ncol = 1, loc = 1)
plt.show()
#fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Paper_schreiben\Special Issue_Inland waters\Plots\Ibsen_response.png')
plt.close()

# ASD Section--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ASD_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Andreas ASD\ASD_ASCII_data\with radiometric calibration'
dummy = reader.read_asd_data(ASD_directory, 'spectralon_00007')
wavelength = dummy['wavelength']
spectralon_asd = spectralon.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', wavelength)['resampled_spectralon']

#11:32
asd_7 = reader.read_asd_data(ASD_directory, 'spectralon_00007')['data'][2]/spectralon_asd
asd_8 = reader.read_asd_data(ASD_directory, 'spectralon_00008')['data'][2]/spectralon_asd
asd_9 = reader.read_asd_data(ASD_directory, 'spectralon_00009')['data'][2]/spectralon_asd
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser_Level1'
ibsen_1 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference001', '.ibsenL1', 1.5, 1.5, 1.5)

#12:03
asd_13 = reader.read_asd_data(ASD_directory, 'spectralon_00013')['data'][2]/spectralon_asd
asd_14 = reader.read_asd_data(ASD_directory, 'spectralon_00014')['data'][2]/spectralon_asd
asd_15 = reader.read_asd_data(ASD_directory, 'spectralon_00015')['data'][2]/spectralon_asd
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen_2 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference000', '.ibsenL1', 1.5, 1.5, 1.5)

#13:19
asd_33 = reader.read_asd_data(ASD_directory, 'spectralon_00033')['data'][2]/spectralon_asd
asd_34 = reader.read_asd_data(ASD_directory, 'spectralon_00034')['data'][2]/spectralon_asd
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2_Level1'
ibsen_1 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference000', '.ibsenL1', 1.5, 1.5, 1.5)

muss nur noch geplottet werden
