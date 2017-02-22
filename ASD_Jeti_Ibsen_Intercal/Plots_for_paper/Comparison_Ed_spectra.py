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
jeti_1 = reader.read_jeti(jeti_directory, 'Jeti_1.dat')['data'][1]
jeti_2 = reader.read_jeti(jeti_directory, 'Jeti_2.dat')['data'][1]

jeti_8 = reader.read_jeti(jeti_directory, 'Jeti_8.dat')['data'][1]
jeti_9 = reader.read_jeti(jeti_directory, 'Jeti_9.dat')['data'][1]
jeti_10 = reader.read_jeti(jeti_directory, 'Jeti_10.dat')['data'][1]
jeti_11 = reader.read_jeti(jeti_directory, 'Jeti_11.dat')['data'][1]

wavelength_jeti = jeti_1 = reader.read_jeti(jeti_directory, 'Jeti_1.dat')['data'][0]
spectralon_jeti = spectralon.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', wavelength_jeti)['resampled_spectralon']
jeti_average = (jeti_1 + jeti_2 + jeti_8 + jeti_9 + jeti_10 + jeti_11)*np.pi/spectralon_jeti/600

# Ibsen data reading and processing section 

ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen_1 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference003', '.ibsenL1', 1.5, 1.5, 1.5)
ibsen_2 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference004', '.ibsenL1', 1.5, 1.5, 1.5)
ibsen_avergae = (ibsen_1['mean_good'] + ibsen_2['mean_good'])/2


# PLotting section

fig = plt.figure(figsize=(18, 10))
# plt.plot(jeti_1[0], jeti_1[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_1/10^5')
# plt.plot(jeti_2[0], jeti_2[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_2/10^5')
# plt.plot(jeti_8[0], jeti_8[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_8/10^5')
# plt.plot(jeti_9[0], jeti_9[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_9/10^5')
# plt.plot(jeti_10[0], jeti_10[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_10/10^5')
# plt.plot(jeti_11[0], jeti_11[1]/spectralon_jeti/100, marker='', color = 'b', linestyle='-', label = 'Jeti_11/10^5')
# 
# plt.plot(ibsen_1['wavelength'], ibsen_1['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 1, 12:22')
# plt.plot(ibsen_2['wavelength'], ibsen_2['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 2, 12:24'

plt.plot(wavelength_jeti, jeti_average, marker='', color = 'b', linestyle='-', label = 'Jeti average')
plt.plot(ibsen_2['wavelength'], ibsen_avergae, marker='', color = 'r', linestyle='-', label = 'Ibsen average')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Downwelling irradiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('Jeti and Ibsen comparison, Wed. 1.6., 12:22, deep water', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\E_d_comparison\Ibsen_Jeti_E_d_comparison_12_22.png')
plt.close()




# ASD Section--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ASD_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Andreas ASD\ASD_ASCII_data\with radiometric calibration'
dummy_asd = reader.read_asd_data(ASD_directory, 'spectralon_00007')
wavelength_asd = dummy_asd['wavelength']
spectralon_asd = spectralon.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', wavelength_asd)['resampled_spectralon']

#11:32
asd_7 = reader.read_asd_data(ASD_directory, 'spectralon_00007')['data'][2]/spectralon_asd*1000*np.pi # nirgendwo info gefunden, aber vermutlich spuckt ASD W/sqm.nm.sr aus, also x1000 fuer Konversion zu mW
asd_8 = reader.read_asd_data(ASD_directory, 'spectralon_00008')['data'][2]/spectralon_asd*1000*np.pi
asd_9 = reader.read_asd_data(ASD_directory, 'spectralon_00009')['data'][2]/spectralon_asd*1000*np.pi
asd_1_mean = (asd_7 + asd_8 + asd_9)/3
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser_Level1'
ibsen_3 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference001', '.ibsenL1', 1.5, 1.5, 1.5)

fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength_asd, asd_7, marker='', color = 'b', linestyle='-', label = 'ASD 7, 11:32') 
plt.plot(wavelength_asd, asd_8, marker='', color = 'b', linestyle='-', label = 'ASD 8, 11:32')
plt.plot(wavelength_asd, asd_9, marker='', color = 'b', linestyle='-', label = 'ASD 9, 11:32')
plt.plot(ibsen_3['wavelength'], ibsen_3['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 3, 11:33')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Downwelling irradiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 11:32', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\E_d_comparison\Ibsen_ASD_E_d_comparison_11_32.png')
plt.close()


#12:03
asd_13 = reader.read_asd_data(ASD_directory, 'spectralon_00013')['data'][2]/spectralon_asd*1000*np.pi # nirgendwo info gefunden, aber vermutlich spuckt ASD W/sqm.nm.sr aus, also x1000 fuer Konversion zu mW
asd_14 = reader.read_asd_data(ASD_directory, 'spectralon_00014')['data'][2]/spectralon_asd*1000*np.pi
asd_15 = reader.read_asd_data(ASD_directory, 'spectralon_00015')['data'][2]/spectralon_asd*1000*np.pi
asd_2_mean = (asd_13 + asd_14 + asd_15)/3
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen_4 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference000', '.ibsenL1', 1.5, 1.5, 1.5)

fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength_asd, asd_13, marker='', color = 'b', linestyle='-', label = 'ASD 13, 12:03')
plt.plot(wavelength_asd, asd_14, marker='', color = 'b', linestyle='-', label = 'ASD 14, 12:03')
plt.plot(wavelength_asd, asd_15, marker='', color = 'b', linestyle='-', label = 'ASD 15, 12:03')
plt.plot(ibsen_4['wavelength'], ibsen_4['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 4, 12:03')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Downwelling irradiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 12:03', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\E_d_comparison\Ibsen_ASD_E_d_comparison_12_03.png')
plt.close()


#13:19
asd_33 = reader.read_asd_data(ASD_directory, 'spectralon_00033')['data'][2]/spectralon_asd*1000*np.pi # nirgendwo info gefunden, aber vermutlich spuckt ASD W/sqm.nm.sr aus, also x1000 fuer Konversion zu mW
asd_34 = reader.read_asd_data(ASD_directory, 'spectralon_00034')['data'][2]/spectralon_asd*1000*np.pi
asd_3_mean = (asd_33 + asd_34)/2
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2_Level1'
ibsen_5 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference000', '.ibsenL1', 1.5, 1.5, 1.5)


fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength_asd, asd_33, marker='', color = 'b', linestyle='-', label = 'ASD 33, 13:19')
plt.plot(wavelength_asd, asd_34, marker='', color = 'b', linestyle='-', label = 'ASD 34, 13:19')
plt.plot(ibsen_5['wavelength'], ibsen_5['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 5, 13:18')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Downwelling irradiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 13:19', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\E_d_comparison\Ibsen_ASD_E_d_comparison_13_19.png')
plt.close()


# ASD average vs Ibsen---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength_asd, asd_1_mean, marker='', color = '#00BFFF', linestyle='-', label = 'ASD mean, 11:32') #blue
plt.plot(wavelength_asd, asd_2_mean, marker='', color = '#00FF7F', linestyle='-', label = 'ASD mean, 12:03') #green
plt.plot(wavelength_asd, asd_3_mean, marker='', color = 'r', linestyle='-', label = 'ASD mean, 13:19') #red
plt.plot(ibsen_3['wavelength'], ibsen_3['mean_good'], marker='', color = '#4169E1', linestyle='-', label = 'Ibsen 3, 11:33')
plt.plot(ibsen_4['wavelength'], ibsen_4['mean_good'], marker='', color = '#32CD32', linestyle='-', label = 'Ibsen 4, 12:03')
plt.plot(ibsen_5['wavelength'], ibsen_5['mean_good'], marker='', color = '#8B0000', linestyle='-', label = 'Ibsen 5, 13:18')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Downwelling irradiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD and Ibsen comparison, Wed. 1.6.', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\E_d_comparison\Ibsen_ASD_E_d_comparison_13_19.png')
plt.close()

# average normalized
fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength_asd, asd_1_mean/max(asd_1_mean)+0.31, marker='', color = '#00BFFF', linestyle='-', label = 'ASD mean, 11:32')
plt.plot(wavelength_asd, asd_2_mean/max(asd_2_mean)+0.62, marker='', color = '#00FF7F', linestyle='-', label = 'ASD mean, 12:03')
plt.plot(wavelength_asd, asd_3_mean/max(asd_3_mean), marker='', color = 'r', linestyle='-', label = 'ASD mean, 13:19')
plt.plot(ibsen_3['wavelength'], ibsen_3['mean_good']/max(ibsen_3['mean_good'])+0.31, marker='', color = '#4169E1', linestyle='-', label = 'Ibsen 3, 11:33')
plt.plot(ibsen_4['wavelength'], ibsen_4['mean_good']/max(ibsen_4['mean_good'])+0.62, marker='', color = '#32CD32', linestyle='-', label = 'Ibsen 4, 12:03')
plt.plot(ibsen_5['wavelength'], ibsen_5['mean_good']/max(ibsen_5['mean_good']), marker='', color = '#8B0000', linestyle='-', label = 'Ibsen 5, 13:18')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Downwelling irradiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD and Ibsen comparison, Wed. 1.6., normalized', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 2)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\E_d_comparison\Ibsen_ASD_E_d_comparison_13_19_normalized.png')
plt.close()
