'''
Created on 12.07.2016

@author: ried_st
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate

reader = Reader.File_Reader()
spectralon = spectralon_response.Interpolate_Spectralon()
ibsen_evaluate = Ibsen_evaluate.Ibsen_Evaluation()


ASD_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Atwood_Stechlinsee_31_05_2015\ASCII_Data\with radiometric calibration'
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\Alle zusammen'
dummy_asd = reader.read_asd_data(ASD_directory, 'GR_00019', '.dat')
wavelength_asd = dummy_asd['wavelength']
spectralon_asd = spectralon.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', wavelength_asd)['resampled_spectralon']



#1_________________________________________________________________________________________________________________________________________________________________________________________           
asd_16 = reader.read_asd_data(ASD_directory, 'water_00016', '.dat')['data'][2]*1000
asd_17 = reader.read_asd_data(ASD_directory, 'sky_00017', '.dat')['data'][2]*1000
asd_19 = reader.read_asd_data(ASD_directory, 'GR_00019', '.dat')['data'][2]/spectralon_asd*1000*np.pi
refl_asd_1 = (asd_16-0.024*asd_17)/asd_19*100


asd_21 = reader.read_asd_data(ASD_directory, 'water_00021', '.dat')['data'][2]*1000
asd_22 = reader.read_asd_data(ASD_directory, 'sky_00022', '.dat')['data'][2]*1000
asd_23 = reader.read_asd_data(ASD_directory, 'GR_00023', '.dat')['data'][2]/spectralon_asd*1000*np.pi
refl_asd_2 = (asd_21-0.024*asd_22)/asd_23*100

ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\Alle zusammen_Level1'
ibsen_1 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference006', '.ibsenL1', 1.5, 1.5, 1.5)
ibsen_2 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target005', '.ibsenL1', 0.5, 4, 1.5)
wavelength_ibsen = ibsen_1['wavelength']
ibsen_refl_1 = ibsen_2['mean_good'] / ibsen_1['mean_good']*100

ibsen_water_mean = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target006', '.ibsenL1', 0.5, 2, 1.5)['mean_good']
ibsen_water_std = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target006', '.ibsenL1', 0.5, 2, 1.5)['std_good']
ibsen_Ed_mean = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference008', '.ibsenL1', 1.5, 1.5, 1.5)['mean_good']
ibsen_Ed_std = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference008', '.ibsenL1', 1.5, 1.5, 1.5)['std_good']

ibsen_rss_mean = ibsen_water_mean/ibsen_Ed_mean*100
ibsen_rss_plus = (ibsen_water_mean + ibsen_water_std)/(ibsen_Ed_mean - ibsen_Ed_std)*100
ibsen_rss_minus = (ibsen_water_mean - ibsen_water_std)/(ibsen_Ed_mean + ibsen_Ed_std)*100

fig = plt.figure(figsize=(12, 7))
#plt.plot(wavelength_asd, refl_asd_1, label = 'ASD 14:04 GR')
plt.plot(wavelength_asd, refl_asd_2, label = 'ASD 14:07 GR')
#plt.plot(wavelength_ibsen, ibsen_refl_1, label = 'Ibsen 14:01')
plt.plot(wavelength_ibsen, ibsen_rss_mean, color = '#8B0000', label = 'Ibsen RSS mean 14:06')
plt.plot(wavelength_ibsen, ibsen_rss_plus, color = 'r')
plt.plot(wavelength_ibsen, ibsen_rss_minus, color = 'r')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Remote sensing reflectance $[\frac {1}{sr}]$', fontsize = 18)
fig.suptitle('ASD: Mobley geometry, sky radiance subtracted \nIbsen nadir measurement, no sky radiance subtracted', fontsize = 18)
legend = plt.legend(ncol = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\Mobley_nadir\Ibsen_ASD_reflectance_uncertainties.png')
plt.close()


#2_________________________________________________________________________________________________________________________________________________________________________________________
asd_28 = reader.read_asd_data(ASD_directory, 'water_00028', '.dat')['data'][2]*1000
asd_29 = reader.read_asd_data(ASD_directory, 'sky_00029', '.dat')['data'][2]*1000
asd_30 = reader.read_asd_data(ASD_directory, 'GR_00030', '.dat')['data'][2]/spectralon_asd*1000*np.pi
refl_asd_3 = (asd_28-0.024*asd_29)/asd_30*100


asd_34 = reader.read_asd_data(ASD_directory, 'water_00034', '.dat')['data'][2]*1000
asd_35 = reader.read_asd_data(ASD_directory, 'sky_00035', '.dat')['data'][2]*1000
asd_36 = reader.read_asd_data(ASD_directory, 'GR_00036', '.dat')['data'][2]/spectralon_asd*1000*np.pi
refl_asd_4 = (asd_34-0.024*asd_35)/asd_36*100
refl_asd_4_45 = (asd_34-0.0275*asd_35)/asd_36*100
refl_asd_4_50 = (asd_34-0.0332*asd_35)/asd_36*100
refl_asd_4_60 = (asd_34-0.0591*asd_35)/asd_36*100

ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\Alle zusammen_Level1'
ibsen_3 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference010', '.ibsenL1', 1.5, 1.5, 1.5)
ibsen_4 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target008', '.ibsenL1', 0.5, 4, 1.5)
ibsen_refl_4 = ibsen_4['mean_good'] / ibsen_3['mean_good']*100



ibsen_water_mean = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target009', '.ibsenL1', 0.5, 2, 1.5)['mean_good']
ibsen_water_std = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target009', '.ibsenL1', 0.5, 2, 1.5)['std_good']
ibsen_Ed_mean = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference010', '.ibsenL1', 1.5, 1.5, 1.5)['mean_good']
ibsen_Ed_std = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference010', '.ibsenL1', 1.5, 1.5, 1.5)['std_good']

ibsen_rss_mean = ibsen_water_mean/ibsen_Ed_mean*100
ibsen_rss_plus = (ibsen_water_mean + ibsen_water_std)/(ibsen_Ed_mean - ibsen_Ed_std)*100
ibsen_rss_minus = (ibsen_water_mean - ibsen_water_std)/(ibsen_Ed_mean + ibsen_Ed_std)*100

fig = plt.figure(figsize=(12, 7))
#plt.plot(wavelength_asd, refl_asd_3, label = 'ASD 14:12 GR')
plt.plot(wavelength_asd, refl_asd_4, label = 'ASD 14:16, 40 deg correction')
plt.plot(wavelength_asd, refl_asd_4_45, label = 'ASD 14:16, 45 deg correction')
plt.plot(wavelength_asd, refl_asd_4_50, label = 'ASD 14:16, 50 deg correction')
plt.plot(wavelength_asd, refl_asd_4_60, label = 'ASD 14:16, 60 deg correction')
#plt.plot(wavelength_ibsen, ibsen_refl_4, label = 'Ibsen 14:15')
plt.plot(wavelength_ibsen, ibsen_rss_mean, color = '#8B0000', label = 'Ibsen RSS 14:16')
plt.plot(wavelength_ibsen, ibsen_rss_plus, color = 'r')
plt.plot(wavelength_ibsen, ibsen_rss_minus, color = 'r')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Remote sensing reflectance $[\frac {1}{sr}]$', fontsize = 18)
fig.suptitle('ASD remote sensing reflectance of deep water with skyglint correction \nIbsen without skyglint correction', fontsize = 18)
legend = plt.legend(ncol = 1)
#plt.show()
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\Mobley_nadir\Ibsen_ASD_reflectance_uncertainties_2.png')
plt.close()


#compare all mobley WR___________________________________________________________________________________________________________________________________________________________________________
asd_4 = reader.read_asd_data(ASD_directory, 'water_00004', '.dat')['data'][2]*1000
asd_5 = reader.read_asd_data(ASD_directory, 'sky_00005', '.dat')['data'][2]*1000
asd_3 = reader.read_asd_data(ASD_directory, 'WR_00003', '.dat')['data'][2]*1000*np.pi
asd_6 = reader.read_asd_data(ASD_directory, 'WR_00006', '.dat')['data'][2]*1000*np.pi
refl_asd_WR_1 = (asd_4-0.024*asd_5)/(asd_3 + asd_6)*100*2

asd_8 = reader.read_asd_data(ASD_directory, 'water_00008', '.dat')['data'][2]*1000
asd_9 = reader.read_asd_data(ASD_directory, 'sky_00009', '.dat')['data'][2]*1000
asd_7 = reader.read_asd_data(ASD_directory, 'WR_00007', '.dat')['data'][2]*1000*np.pi
asd_10 = reader.read_asd_data(ASD_directory, 'WR_00010', '.dat')['data'][2]*1000*np.pi
refl_asd_WR_2 = (asd_8-0.024*asd_9)/(asd_7 + asd_10)*100*2

asd_12 = reader.read_asd_data(ASD_directory, 'water_00012', '.dat')['data'][2]*1000
asd_13 = reader.read_asd_data(ASD_directory, 'sky_00013', '.dat')['data'][2]*1000
asd_11 = reader.read_asd_data(ASD_directory, 'WR_00011', '.dat')['data'][2]*1000*np.pi
asd_14 = reader.read_asd_data(ASD_directory, 'WR_00014', '.dat')['data'][2]*1000*np.pi
refl_asd_WR_3 = (asd_12-0.024*asd_13)/(asd_11 + asd_14)*100*2

asd_201 = reader.read_asd_data(ASD_directory, 'water_200001', '.dat')['data'][2]*1000
asd_202 = reader.read_asd_data(ASD_directory, 'sky_200002', '.dat')['data'][2]*1000
asd_200 = reader.read_asd_data(ASD_directory, 'WR_200000', '.dat')['data'][2]*1000*np.pi
asd_204 = reader.read_asd_data(ASD_directory, 'WR_200004', '.dat')['data'][2]*1000*np.pi
refl_asd_WR_4 = (asd_201-0.024*asd_202)/(asd_200 + asd_204)*100*2

asd_206 = reader.read_asd_data(ASD_directory, 'water_200006', '.dat')['data'][2]*1000
asd_207 = reader.read_asd_data(ASD_directory, 'sky_200007', '.dat')['data'][2]*1000
asd_205 = reader.read_asd_data(ASD_directory, 'WR_200005', '.dat')['data'][2]*1000*np.pi
asd_208 = reader.read_asd_data(ASD_directory, 'WR_200008', '.dat')['data'][2]*1000*np.pi
refl_asd_WR_5 = (asd_206-0.024*asd_207)/(asd_205 + asd_208)*100*2

ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\Alle zusammen_Level1'
ibsen_1 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference004', '.ibsenL1', 1.5, 1.5, 1.5)
ibsen_2 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target003', '.ibsenL1', 0.5, 4, 1.5)
ibsen_refl_1 = ibsen_2['mean_good'] / ibsen_1['mean_good']*100

ibsen_2 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference005', '.ibsenL1', 1.5, 1.5, 1.5)
ibsen_3 = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target004', '.ibsenL1', 0.5, 4, 1.5)
ibsen_refl_2 = ibsen_3['mean_good'] / ibsen_2['mean_good']*100

asd_rss_mean = np.mean([refl_asd_WR_1, refl_asd_WR_2, refl_asd_WR_3, refl_asd_WR_4, refl_asd_WR_5], axis = 0)
asd_rss_std = np.std([refl_asd_WR_1, refl_asd_WR_2, refl_asd_WR_3, refl_asd_WR_4, refl_asd_WR_5], axis = 0, ddof = 1)
asd_rss_plus = asd_rss_mean + asd_rss_std
asd_rss_minus = asd_rss_mean - asd_rss_std

ibsen_water_mean = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target004', '.ibsenL1', 0.5, 2, 1.5)['mean_good']
ibsen_water_std = ibsen_evaluate.winnow_spectra(ibsen_directory, 'target004', '.ibsenL1', 0.5, 2, 1.5)['std_good']
ibsen_Ed_mean = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference005', '.ibsenL1', 1.5, 1.5, 1.5)['mean_good']
ibsen_Ed_std = ibsen_evaluate.winnow_spectra(ibsen_directory, 'reference005', '.ibsenL1', 1.5, 1.5, 1.5)['std_good']

ibsen_rss_mean = ibsen_water_mean/ibsen_Ed_mean*100
ibsen_rss_plus = (ibsen_water_mean + ibsen_water_std)/(ibsen_Ed_mean - ibsen_Ed_std)*100
ibsen_rss_minus = (ibsen_water_mean - ibsen_water_std)/(ibsen_Ed_mean + ibsen_Ed_std)*100

fig = plt.figure(figsize=(12, 7))
# plt.plot(wavelength_asd, refl_asd_WR_1, label = 'ASD 13:52 WR')
# plt.plot(wavelength_asd, refl_asd_WR_2, label = 'ASD 13:55 WR')
# plt.plot(wavelength_asd, refl_asd_WR_3, label = 'ASD 13:58 WR')
# plt.plot(wavelength_asd, refl_asd_WR_4, label = 'ASD 14:36 WR')
# plt.plot(wavelength_asd, refl_asd_WR_5, label = 'ASD 14:41 WR')
plt.plot(wavelength_asd, asd_rss_mean, color = '#4169E1', label = 'ASD RSS mean, 13:52-14:41 (incl. 13:58)')
plt.plot(wavelength_asd, asd_rss_plus, color = '#00BFFF')
plt.plot(wavelength_asd, asd_rss_minus, color = '#00BFFF')
#plt.plot(wavelength_ibsen, ibsen_refl_1, label = 'Ibsen 13:53')
#plt.plot(wavelength_ibsen, ibsen_refl_2, label = 'Ibsen 13:58')
plt.plot(wavelength_ibsen, ibsen_rss_mean, color = '#8B0000', label = 'Ibsen RSS mean 13:58')
plt.plot(wavelength_ibsen, ibsen_rss_plus, color = 'r')
plt.plot(wavelength_ibsen, ibsen_rss_minus, color = 'r')
plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
plt.ylabel(r'Remote sensing reflectance $[\frac {1}{sr}]$', fontsize = 18)
fig.suptitle('ASD white spectralon Mobley \nIbsen nadir', fontsize = 18)
legend = plt.legend(ncol = 1)
fig.savefig(r'C:\Users\ried_st\OneDrive\Austausch\Plots\Interkalibrationskampagne\Mobley_nadir\Ibsen_ASD_reflectance_WR.png')
plt.close()


asd_water_mean = asd_rss_mean = np.mean([asd_4, ], axis = 0)
# 
# #3_________________________________________________________________________________________________________________________________________________________________________________________
# asd_tar3 = '00034'
# asd_ref3 = '00036'
# asd_sky3 = '00035'
# asd_34 = read_asd_data(asd_tar3)
# asd_36 = read_asd_data(asd_ref3)
# asd_35 = read_asd_data(asd_sky3)
# refl_asd3 = (asd_34[2]-0.024*asd_35[2])/asd_36[2]*10
# 
# asd_ref3_1 = '00032'
# asd_32 = read_asd_data(asd_ref3_1)
# refl_asd3_1 = (asd_34[2]-0.024*asd_35[2])/asd_32[2]*100
# 
# ibsen3 = plot_reflectance_winnowed('darkcurrent010', 'reference010', 'target009', std_dark = 2, std_ref = 2, std_tar_plus = 0.5, std_tar_minus = 2, std_tar_r2 = 1.5, plot_reflec = 'y')
# 
# 
# fig = plt.figure(figsize=(18, 10))
# plt.plot(asd_34[1], refl_asd3, label = 'ASD GR')
# plt.plot(asd_34[1], refl_asd3_1, label = 'ASD WR')
# plt.plot(ibsen3[0], ibsen3[1], label = 'Ibsen')
# plt.xlabel('Wavelength [nm]', fontsize = 18)
# plt.ylabel('Reflectance [%]', fontsize = 18)
# fig.suptitle('asd: 00034-00035/00036 (GR) and 00033 (WR), 31.5. 14:17 \n ibsen: darkcurrent010, reference010, target009, 31.5. 14:17', fontsize = 18)
# legend = plt.legend(ncol = 1)
# plt.show()
# fig.savefig(os.path.join(directory, 'reflectance' + asd_tar3 + '_' + asd_ref3 + '_ibsen.png'))
# plt.close()
# 
# 
# #4 and 5______________________________________________________________________________________________________________________________________________________________________________________
# asd_tar4 = '00012'
# asd_ref4 = '00011'
# asd_sky4 = '00013'
# asd_12 = read_asd_data(asd_tar4)
# asd_11 = read_asd_data(asd_ref4)
# asd_13 = read_asd_data(asd_sky4)
# refl_asd4 = (asd_12[2]-0.024*asd_13[2])/asd_11[2]*100
# 
# asd_ref4_1 = '00014'
# asd_14 = read_asd_data(asd_ref4_1)
# refl_asd4_1 = (asd_12[2]-0.024*asd_13[2])/asd_14[2]*100
# 
# asd_tar5 = '00008'
# asd_ref5 = '00007'
# asd_sky5 = '00009'
# asd_8 = read_asd_data(asd_tar5)
# asd_7 = read_asd_data(asd_ref5)
# asd_9 = read_asd_data(asd_sky5)
# refl_asd5 = (asd_8[2]-0.024*asd_9[2])/asd_7[2]*100
# 
# asd_ref5_1 = '00010'
# asd_10 = read_asd_data(asd_ref5_1)
# refl_asd5_1 = (asd_8[2]-0.024*asd_9[2])/asd_10[2]*100
# 
# ibsen4 = plot_reflectance_winnowed('darkcurrent005', 'reference005', 'target004', std_dark = 2, std_ref = 2, std_tar_plus = 0.5, std_tar_minus = 2, std_tar_r2 = 1.5, plot_reflec = 'y')
# 
# 
# fig = plt.figure(figsize=(18, 10))
# plt.plot(asd_12[1], refl_asd4, label = 'ASD WR 13:58')
# plt.plot(asd_12[1], refl_asd4_1, label = 'ASD WR 13:59')
# plt.plot(ibsen4[0], ibsen4[1], label = 'Ibsen')
# plt.plot(asd_8[1], refl_asd5, label = 'ASD WR 13:55')
# plt.plot(asd_8[1], refl_asd5_1, label = 'ASD WR 13:56')
# plt.xlabel('Wavelength [nm]', fontsize = 18)
# plt.ylabel('Reflectance [%]', fontsize = 18)
# fig.suptitle('asd: 00012-00013/00011 (WR) 31.5. 13:58 and 00014 (WR), 13:59 \n asd: 00008-00009/00007 (WR) 31.5. 13:55 and 00010 (WR), 13:56 \n ibsen: darkcurrent005, reference005, target004, 31.5. 13:58', fontsize = 18)
# legend = plt.legend(ncol = 1)
# plt.show()
# fig.savefig(os.path.join(directory, 'reflectance' + asd_tar4 + '_' + asd_ref4 + '_ibsen.png'))
# plt.close()
# 
# 
#             
# #6_________________________________________________________________________________________________________________________________________________________________________________________
# asd_tar6 = '00004'
# asd_ref6 = '00003'
# asd_sky6 = '00005'
# asd_4 = read_asd_data(asd_tar6)
# asd_3 = read_asd_data(asd_ref6)
# asd_5 = read_asd_data(asd_sky6)
# refl_asd6 = (asd_4[2]-0.024*asd_5[2])/asd_3[2]*100
# 
# asd_ref6_1 = '00006'
# asd_6 = read_asd_data(asd_ref6_1)
# refl_asd6_1 = (asd_4[2]-0.024*asd_5[2])/asd_6[2]*100
# 
# ibsen6 = plot_reflectance_winnowed('darkcurrent005', 'reference005', 'target003', std_dark = 2, std_ref = 2, std_tar_plus = 0.5, std_tar_minus = 2, std_tar_r2 = 1.5, plot_reflec = 'y')
# 
# 
# fig = plt.figure(figsize=(18, 10))
# plt.plot(asd_4[1], refl_asd6, label = 'ASD WR 13:53')
# plt.plot(asd_4[1], refl_asd6_1, label = 'ASD WR 13:54')
# plt.plot(ibsen6[0], ibsen6[1], label = 'Ibsen')
# plt.xlabel('Wavelength [nm]', fontsize = 18)
# plt.ylabel('Reflectance [%]', fontsize = 18)
# fig.suptitle('asd: 00004-00005/00003 (WR) 31.5. 13:58 and 00006 (WR), 13:59 \n ibsen: darkcurrent005, reference005, target003, 31.5. 13:53', fontsize = 18)
# legend = plt.legend(ncol = 1)
# plt.show()
# fig.savefig(os.path.join(directory, 'reflectance' + asd_tar6 + '_' + asd_ref6 + '_ibsen.png'))
# plt.close()


