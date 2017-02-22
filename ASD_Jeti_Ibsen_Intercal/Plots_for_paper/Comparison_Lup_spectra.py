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
jeti_3 = reader.read_jeti(jeti_directory, 'Jeti_3', '.dat')['data']
jeti_4 = reader.read_jeti(jeti_directory, 'Jeti_4', '.dat')['data']
jeti_5 = reader.read_jeti(jeti_directory, 'Jeti_5', '.dat')['data']
jeti_6 = reader.read_jeti(jeti_directory, 'Jeti_6', '.dat')['data']
jeti_7 = reader.read_jeti(jeti_directory, 'Jeti_7', '.dat')['data']
jeti_average = (jeti_3[1] + jeti_4[1] + jeti_5[1] + jeti_6[1] + jeti_7[1])/500


wavelength_jeti = jeti_3[0]
spectralon_jeti = spectralon.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', wavelength_jeti)['resampled_spectralon']

# Ibsen data reading and processing section 

ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen_1 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target003', '.ibsenL1', 0.5, 4, 1.5)



# Plotting section

fig = plt.figure(figsize=(12, 7))
plt.plot(jeti_3[0], jeti_3[1]/100, marker='', color = 'b', linestyle='-', label = 'Jeti_3/10^5')
plt.plot(jeti_4[0], jeti_4[1]/100, marker='', color = 'b', linestyle='-', label = 'Jeti_4/10^5')
plt.plot(jeti_5[0], jeti_5[1]/100, marker='', color = 'b', linestyle='-', label = 'Jeti_5/10^5')
plt.plot(jeti_6[0], jeti_6[1]/100, marker='', color = 'b', linestyle='-', label = 'Jeti_6/10^5')
plt.plot(jeti_7[0], jeti_7[1]/100, marker='', color = 'b', linestyle='-', label = 'Jeti_7/10^5')
plt.plot(ibsen_1['wavelength'], ibsen_1['mean_good'], marker='', color = 'r', linestyle='-', label = 'target003')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('')
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
#fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Paper_schreiben\Special Issue_Inland waters\Plots\Ibsen_response.png')
plt.close()

fig = plt.figure(figsize=(12, 7))
plt.plot(jeti_3[0], jeti_average, marker='', color = 'b', linestyle='-', label = 'Jeti_3/10^5')
plt.plot(ibsen_1['wavelength'], ibsen_1['mean_good'], marker='', color = 'r', linestyle='-', label = 'target003')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('Ibsen vs Jeti')
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_Jeti_L_up_water_comparison.png')
plt.close()






# ASD Section single measurements---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ASD_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Andreas ASD\ASD_ASCII_data\with radiometric calibration'
dummy_asd = reader.read_asd_data(ASD_directory, 'spectralon_00007', '.dat')
wavelength_asd = dummy_asd['wavelength']

#11:32 Lup water
asd_10 = reader.read_asd_data(ASD_directory, 'wasser_00010', '.dat')['data'][2]*1000 # nirgendwo info gefunden, aber vermutlich spuckt ASD W/sqm.nm.sr aus, also x1000 fuer Konversion zu mW
asd_11 = reader.read_asd_data(ASD_directory, 'wasser_00011', '.dat')['data'][2]*1000
asd_12 = reader.read_asd_data(ASD_directory, 'wasser_00012', '.dat')['data'][2]*1000
asd_1_mean = (asd_10 + asd_11 + asd_12)/3
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser_Level1'
ibsen_2 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target004', '.ibsenL1', 0.5, 4, 1.5)

fig = plt.figure(figsize=(12, 7))
plt.plot(wavelength_asd, asd_10, marker='', color = 'b', linestyle='-', label = 'ASD 10, 11:32') 
plt.plot(wavelength_asd, asd_11, marker='', color = 'b', linestyle='-', label = 'ASD 11, 11:32')
plt.plot(wavelength_asd, asd_12, marker='', color = 'b', linestyle='-', label = 'ASD 12, 11:32')

plt.plot(ibsen_2['wavelength'], ibsen_2['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 2, 11:34')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 11:32', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_ASD_L_up_water_comparison_11_32.png')
plt.close()


#12:04 Lup water
asd_16 = reader.read_asd_data(ASD_directory, 'wasser_00016', '.dat')['data'][2]*1000 # nirgendwo info gefunden, aber vermutlich spuckt ASD W/sqm.nm.sr aus, also x1000 fuer Konversion zu mW
asd_17 = reader.read_asd_data(ASD_directory, 'wasser_00017', '.dat')['data'][2]*1000
asd_18 = reader.read_asd_data(ASD_directory, 'wasser_00018', '.dat')['data'][2]*1000
asd_19 = reader.read_asd_data(ASD_directory, 'wasser_00019', '.dat')['data'][2]*1000
asd_2_mean = (asd_16 + asd_17 + asd_18 + asd_19)/4
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen_3 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target000', '.ibsenL1', 0.5, 4, 1.5)

fig = plt.figure(figsize=(12, 7))
plt.plot(wavelength_asd, asd_16, marker='', color = 'b', linestyle='-', label = 'ASD 16, 12:04') 
plt.plot(wavelength_asd, asd_17, marker='', color = 'b', linestyle='-', label = 'ASD 17, 12:04')
plt.plot(wavelength_asd, asd_18, marker='', color = 'b', linestyle='-', label = 'ASD 18, 12:04')
plt.plot(wavelength_asd, asd_19, marker='', color = 'b', linestyle='-', label = 'ASD 19, 12:04')
plt.plot(ibsen_3['wavelength'], ibsen_3['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 3, 12:04')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 12:04', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_ASD_L_up_water_comparison_12_04.png')
plt.close()


#12:06 Lup water
asd_24 = reader.read_asd_data(ASD_directory, 'wasser_00024', '.dat')['data'][2]*1000 # nirgendwo info gefunden, aber vermutlich spuckt ASD W/sqm.nm.sr aus, also x1000 fuer Konversion zu mW
asd_25 = reader.read_asd_data(ASD_directory, 'wasser_00025', '.dat')['data'][2]*1000
asd_3_mean = (asd_24 + asd_25)/2
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen_4 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target001', '.ibsenL1', 0.5, 4, 1.5)

fig = plt.figure(figsize=(12, 7))
plt.plot(wavelength_asd, asd_24, marker='', color = 'b', linestyle='-', label = 'ASD 24, 12:06') 
plt.plot(wavelength_asd, asd_25, marker='', color = 'b', linestyle='-', label = 'ASD 25, 12:06')
plt.plot(ibsen_4['wavelength'], ibsen_4['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 4, 12:07')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 12:06', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_ASD_L_up_water_comparison_12_06.png')
plt.close()


#13:17 Lup water
asd_28 = reader.read_asd_data(ASD_directory, 'wasser_00028', '.dat')['data'][2]*1000 # nirgendwo info gefunden, aber vermutlich spuckt ASD W/sqm.nm.sr aus, also x1000 fuer Konversion zu mW
asd_29 = reader.read_asd_data(ASD_directory, 'wasser_00029', '.dat')['data'][2]*1000
asd_30 = reader.read_asd_data(ASD_directory, 'wasser_00030', '.dat')['data'][2]*1000
asd_31 = reader.read_asd_data(ASD_directory, 'wasser_00031', '.dat')['data'][2]*1000
asd_32 = reader.read_asd_data(ASD_directory, 'wasser_00032', '.dat')['data'][2]*1000

asd_4_mean = (asd_28 + asd_29 + asd_30 + asd_31 + asd_32)/5
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2_Level1'
ibsen_5 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target000', '.ibsenL1', 0.5, 4, 1.5)

fig = plt.figure(figsize=(12, 7))
plt.plot(wavelength_asd, asd_28, marker='', color = 'b', linestyle='-', label = 'ASD 28, 13:17') 
plt.plot(wavelength_asd, asd_29, marker='', color = 'b', linestyle='-', label = 'ASD 29, 13:17')
plt.plot(wavelength_asd, asd_30, marker='', color = 'b', linestyle='-', label = 'ASD 30, 13:17') 
plt.plot(wavelength_asd, asd_31, marker='', color = 'b', linestyle='-', label = 'ASD 31, 13:17') 
plt.plot(wavelength_asd, asd_32, marker='', color = 'b', linestyle='-', label = 'ASD 32, 13:17') 

plt.plot(ibsen_5['wavelength'], ibsen_5['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 5, 13:19')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 13:17-13:20', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_ASD_L_up_water_comparison_13_20.png')
plt.close()



#13:22 Lup water
asd_40 = reader.read_asd_data(ASD_directory, 'wasser_00040', '.dat')['data'][2]*1000 # nirgendwo info gefunden, aber vermutlich spuckt ASD W/sqm.nm.sr aus, also x1000 fuer Konversion zu mW
asd_41 = reader.read_asd_data(ASD_directory, 'wasser_00041', '.dat')['data'][2]*1000
asd_42 = reader.read_asd_data(ASD_directory, 'wasser_00042', '.dat')['data'][2]*1000
asd_43 = reader.read_asd_data(ASD_directory, 'wasser_00043', '.dat')['data'][2]*1000
asd_44 = reader.read_asd_data(ASD_directory, 'wasser_00044', '.dat')['data'][2]*1000
asd_45 = reader.read_asd_data(ASD_directory, 'wasser_00045', '.dat')['data'][2]*1000

asd_5_mean = (asd_40 + asd_41 + asd_42 + asd_43 + asd_44 + asd_45)/6
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2_Level1'
ibsen_6 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target002', '.ibsenL1', 0.5, 4, 1.5)

fig = plt.figure(figsize=(12, 7))
plt.plot(wavelength_asd, asd_40, marker='', color = 'b', linestyle='-', label = 'ASD 40, 13:22') 
plt.plot(wavelength_asd, asd_41, marker='', color = 'b', linestyle='-', label = 'ASD 41, 13:22')
plt.plot(wavelength_asd, asd_42, marker='', color = 'b', linestyle='-', label = 'ASD 42, 13:22') 
plt.plot(wavelength_asd, asd_43, marker='', color = 'b', linestyle='-', label = 'ASD 43, 13:22')
plt.plot(wavelength_asd, asd_44, marker='', color = 'b', linestyle='-', label = 'ASD 44, 13:22') 
plt.plot(wavelength_asd, asd_45, marker='', color = 'b', linestyle='-', label = 'ASD 45, 13:22')
plt.plot(ibsen_6['wavelength'], ibsen_6['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 4, 13:25')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 13:22', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_ASD_L_up_water_comparison_13_22.png')
plt.close()



# 13:20 bodenprobe
asd_35 = reader.read_asd_data(ASD_directory, 'bodenprobe1_00035', '.dat')['data'][2]*1000
asd_36 = reader.read_asd_data(ASD_directory, 'bodenprobe1_00036', '.dat')['data'][2]*1000
asd_37 = reader.read_asd_data(ASD_directory, 'bodenprobe1_00037', '.dat')['data'][2]*1000
asd_38 = reader.read_asd_data(ASD_directory, 'bodenprobe1_00038', '.dat')['data'][2]*1000
asd_39 = reader.read_asd_data(ASD_directory, 'bodenprobe1_00039', '.dat')['data'][2]*1000

asd_6_mean = (asd_35 + asd_36 + asd_37 + asd_38 + asd_39)/5
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2_Level1'
ibsen_7 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target001', '.ibsenL1', 0.5, 4, 1.5)

fig = plt.figure(figsize=(12, 7))
plt.plot(wavelength_asd, asd_35, marker='', color = 'g', linestyle='-', label = 'ASD 35, 13:20') 
plt.plot(wavelength_asd, asd_36, marker='', color = 'g', linestyle='-', label = 'ASD 36, 13:20') 
plt.plot(wavelength_asd, asd_37, marker='', color = 'g', linestyle='-', label = 'ASD 37, 13:20') 
plt.plot(wavelength_asd, asd_38, marker='', color = 'g', linestyle='-', label = 'ASD 38, 13:20') 
plt.plot(wavelength_asd, asd_39, marker='', color = 'g', linestyle='-', label = 'ASD 39, 13:20') 
plt.plot(ibsen_7['wavelength'], ibsen_7['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 7, 13:23')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 13:20, sea ground sample', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 2)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_ASD_L_up_groundsample_comparison_11_32.png')
plt.close()



# 13:28 bodenprobe
asd_48 = reader.read_asd_data(ASD_directory, 'bodenprobe2_00048', '.dat')['data'][2]*1000
asd_49 = reader.read_asd_data(ASD_directory, 'bodenprobe2_00049', '.dat')['data'][2]*1000
asd_50 = reader.read_asd_data(ASD_directory, 'bodenprobe2_00050', '.dat')['data'][2]*1000
asd_51 = reader.read_asd_data(ASD_directory, 'bodenprobe2_00051', '.dat')['data'][2]*1000
asd_52 = reader.read_asd_data(ASD_directory, 'bodenprobe2_00052', '.dat')['data'][2]*1000


asd_7_mean = (asd_48 + asd_49 + asd_50 + asd_51 + asd_52)/5
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2_Level1'
ibsen_8 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target003', '.ibsenL1', 0.5, 4, 1.5)

fig = plt.figure(figsize=(12, 7))
plt.plot(wavelength_asd, asd_48, marker='', color = 'g', linestyle='-', label = 'ASD 48, 13:28') 
plt.plot(wavelength_asd, asd_49, marker='', color = 'g', linestyle='-', label = 'ASD 49, 13:28') 
plt.plot(wavelength_asd, asd_50, marker='', color = 'g', linestyle='-', label = 'ASD 50, 13:28') 
plt.plot(wavelength_asd, asd_51, marker='', color = 'g', linestyle='-', label = 'ASD 51, 13:28') 
plt.plot(wavelength_asd, asd_52, marker='', color = 'g', linestyle='-', label = 'ASD 52, 13:28') 
plt.plot(ibsen_8['wavelength'], ibsen_8['mean_good'], marker='', color = 'r', linestyle='-', label = 'Ibsen 8, 13:30')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 13:28, sea ground sample', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 2)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_ASD_L_up_groundsample_comparison_13_28.png')
plt.close()



# ASD Section measurement average---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# water
fig = plt.figure(figsize=(12, 7))
plt.plot(wavelength_asd, asd_1_mean, marker='', color = '#00FF7F', linestyle='-', label = 'ASD, 11:32, shallow water') #green
plt.plot(ibsen_2['wavelength'], ibsen_2['mean_good'], marker='', color = '#32CD32', linestyle='-', label = 'Ibsen, 11:34, shallow water')
# plt.plot(wavelength_asd, asd_2_mean, marker='', color = '#00BFFF', linestyle='-', label = 'ASD_2_average, 12:04') #blue
# plt.plot(ibsen_3['wavelength'], ibsen_3['mean_good'], marker='', color = '#4169E1', linestyle='-', label = 'Ibsen 3, 12:04')
plt.plot(wavelength_asd, asd_3_mean, marker='', color = 'r', linestyle='-', label = 'ASD, 12:06, deep water') #red
plt.plot(ibsen_4['wavelength'], ibsen_4['mean_good'], marker='', color = '#8B0000', linestyle='-', label = 'Ibsen, 12:07, deep water')
# plt.plot(wavelength_asd, asd_4_mean, marker='', color = '#00FFFF', linestyle='-', label = 'ASD_4_average, 13:17')
# plt.plot(ibsen_5['wavelength'], ibsen_5['mean_good'], marker='', color = '#20B2AA', linestyle='-', label = 'Ibsen 5, 13:19')
plt.plot(wavelength_asd, asd_5_mean, marker='', color = '#8A2BE2', linestyle='-', label = 'ASD, 13:22, shallow water')
plt.plot(ibsen_6['wavelength'], ibsen_6['mean_good'], marker='', color = '#8B008B', linestyle='-', label = 'Ibsen, 13:25, shallow water')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD and Ibsen comparison, upwelling water radiance 1.6.2016', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_ASD_L_up_water_comparison_average.png')
plt.close()


# water normalized
fig = plt.figure(figsize=(12, 7))
plt.plot(wavelength_asd, asd_1_mean/max(asd_1_mean)+0.31, marker='', color = '#00FF7F', linestyle='-', label = 'ASD, 11:32, shallow water') #green
plt.plot(ibsen_2['wavelength'], ibsen_2['mean_good']/max(ibsen_2['mean_good'])+0.31, marker='', color = '#32CD32', linestyle='-', label = 'Ibsen, 11:34, shallow water')
plt.plot(wavelength_asd, asd_2_mean/max(asd_2_mean)+0.93, marker='', color = '#00BFFF', linestyle='-', label = 'ASD_2_average, 12:04') #blue
plt.plot(ibsen_3['wavelength'], ibsen_3['mean_good']/max(ibsen_3['mean_good'])+0.93, marker='', color = '#4169E1', linestyle='-', label = 'Ibsen 3, 12:04')
plt.plot(wavelength_asd, asd_3_mean/max(asd_3_mean)+0.62, marker='', color = 'r', linestyle='-', label = 'ASD, 12:06, deep water') #red
plt.plot(ibsen_4['wavelength'], ibsen_4['mean_good']/max(ibsen_4['mean_good'])+0.62, marker='', color = '#8B0000', linestyle='-', label = 'Ibsen, 12:07, deep water')
plt.plot(wavelength_asd, asd_4_mean/max(asd_4_mean)+1.24, marker='', color = '#00FFFF', linestyle='-', label = 'ASD_4_average, 13:17')
plt.plot(ibsen_5['wavelength'], ibsen_5['mean_good']/max(ibsen_5['mean_good'])+1.24, marker='', color = '#20B2AA', linestyle='-', label = 'Ibsen 5, 13:19')
plt.plot(wavelength_asd, asd_5_mean/max(asd_5_mean), marker='', color = '#8A2BE2', linestyle='-', label = 'ASD, 13:22, shallow water')
plt.plot(ibsen_6['wavelength'], ibsen_6['mean_good']/max(ibsen_6['mean_good']), marker='', color = '#8B008B', linestyle='-', label = 'Ibsen, 13:25, shallow water')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD and Ibsen comparison, upwelling water radiance 1.6.2016', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_ASD_L_up_water_comparison_average_normalized.png')
plt.close()



# bodenprobe
fig = plt.figure(figsize=(12, 7))
plt.plot(wavelength_asd, asd_6_mean, marker='', color = '#00BFFF', linestyle='-', label = 'ASD_6_average, 13:20')
plt.plot(ibsen_7['wavelength'], ibsen_7['mean_good'], marker='', color = '#4169E1', linestyle='-', label = 'Ibsen 7, 13:23')
plt.plot(wavelength_asd, asd_7_mean, marker='', color = 'r', linestyle='-', label = 'ASD_7_average, 13:28')
plt.plot(ibsen_8['wavelength'], ibsen_8['mean_good'], marker='', color = '#8B0000', linestyle='-', label = 'Ibsen 8, 13:30')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Upwelling water radiance $[\frac {mW}{m^2 \cdot nm}]$', fontsize = 18)
fig.suptitle('ASD vs Ibsen, Wed. 1.6., 13:28, sea ground sample', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 2)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\L_up_comparison\Ibsen_ASD_L_up_groundsample_comparison_average.png')
plt.close()


# mna sieht leider wenig in den plots. Normierne wie bei Ed und irgendwie besser herausarbeiten.
# Dann reflectance auswertung nochmal anfassen
# plots in Ordner speichern
