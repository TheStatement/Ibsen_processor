'''
Created on 12.07.2016

@author: ried_st
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate

reader = Reader.File_Reader()
spectralon = spectralon_response.Interpolate_Spectralon()
ibsen_evaluate = Ibsen_evaluate.Ibsen_Evaluation()

ASD_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Andreas ASD\ASCII_data\no radiometric calibration'

jeti_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Andreas Jeti'


# def plot_asd_all():
#     for file in os.listdir(directory):
#         if file.endswith('.dat'):
#             filename, file_extension = os.path.splitext(file)
#             asd_data = reader.read_asd_data(ASD_directory, filename)
#             fig = plt.figure(figsize=(18, 10))
#             plt.plot(asd_data[1], asd_data[2])
#             plt.xlabel('Wavelength [nm]', fontsize = 18)
#             plt.ylabel('DN', fontsize = 18)
#             fig.suptitle(filename)
#             fig.savefig(os.path.join(directory, filename + '.png'))
#             plt.close()


# plot_asd_all()


#1_________________________________________________________________________________________________________________________________________________________________________________________           
# nur exemplarische Daten verwendet, Vergleich ergaenzen um die restlichen Daten
asd_16 = reader.read_asd_data(ASD_directory, 'wasser_00016')
asd_17 = reader.read_asd_data(ASD_directory, 'wasser_00017')
asd_18 = reader.read_asd_data(ASD_directory, 'wasser_00018')
asd_19 = reader.read_asd_data(ASD_directory, 'wasser_00019')
asd_13 = reader.read_asd_data(ASD_directory, 'spectralon_00013')
asd_14 = reader.read_asd_data(ASD_directory, 'spectralon_00014')
asd_15 = reader.read_asd_data(ASD_directory, 'spectralon_00015')
asd_24 = reader.read_asd_data(ASD_directory, 'wasser_00024')
asd_25 = reader.read_asd_data(ASD_directory, 'wasser_00025')
asd_20 = reader.read_asd_data(ASD_directory, 'spectralon_00020')
asd_21 = reader.read_asd_data(ASD_directory, 'spectralon_00021')
asd_22 = reader.read_asd_data(ASD_directory, 'spectralon_00022')

wavelength = asd_16[1]
spectralon_asd = spectralon.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', wavelength)[0]
refl_asd = asd_16[2]/asd_20[2]/spectralon_asd
refl_asd1 = asd_17[2]/asd_20[2]/spectralon_asd
refl_asd2 = asd_18[2]/asd_20[2]/spectralon_asd
refl_asd3 = asd_19[2]/asd_20[2]/spectralon_asd
refl_asd4 = asd_24[2]/asd_20[2]/spectralon_asd
refl_asd5 = asd_25[2]/asd_20[2]/spectralon_asd
      
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference000', 'target000', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
ibsen2 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference001', 'target001', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
ibsen3 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference002', 'target002', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
    
      
fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength, refl_asd, label = 'ASD 16')
plt.plot(wavelength, refl_asd1, label = 'ASD 17')
plt.plot(wavelength, refl_asd2, label = 'ASD 18')
plt.plot(wavelength, refl_asd3, label = 'ASD 19')
plt.plot(wavelength, refl_asd4, label = 'ASD 24')
plt.plot(wavelength, refl_asd5, label = 'ASD 25')
plt.plot(ibsen[0], ibsen[1], label = 'Ibsen 12:04')
plt.plot(ibsen2[0], ibsen2[1], label = 'Ibsen 12:07')
plt.plot(ibsen3[0], ibsen3[1], label = 'Ibsen 12:08')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('Tiefwasser Boje, Ibsen vs ASD_unfertig', fontsize = 18)
legend = plt.legend(ncol = 1)
plt.show()
fig.savefig(os.path.join(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Plots', '1_reflectance_ASD_Ibsen_different_target.png'))
plt.close()
   

#1_2_________________________________________________________________________________________________________________________________________________________________________________________           
# nur exemplarische Daten verwendet, Vergleich ergaenzen um die restlichen Daten
asd_16 = reader.read_asd_data(ASD_directory, 'wasser_00016')
asd_17 = reader.read_asd_data(ASD_directory, 'wasser_00017')
asd_18 = reader.read_asd_data(ASD_directory, 'wasser_00018')
asd_19 = reader.read_asd_data(ASD_directory, 'wasser_00019')
asd_13 = reader.read_asd_data(ASD_directory, 'spectralon_00013')
asd_14 = reader.read_asd_data(ASD_directory, 'spectralon_00014')
asd_15 = reader.read_asd_data(ASD_directory, 'spectralon_00015')
asd_24 = reader.read_asd_data(ASD_directory, 'wasser_00024')
asd_25 = reader.read_asd_data(ASD_directory, 'wasser_00025')
asd_20 = reader.read_asd_data(ASD_directory, 'spectralon_00020')
asd_21 = reader.read_asd_data(ASD_directory, 'spectralon_00021')
asd_22 = reader.read_asd_data(ASD_directory, 'spectralon_00022')

wavelength = asd_16[1]
refl_asd = asd_16[2]/asd_13[2]/spectralon_asd
refl_asd1 = asd_16[2]/asd_14[2]/spectralon_asd
refl_asd2 = asd_16[2]/asd_15[2]/spectralon_asd
refl_asd3 = asd_16[2]/asd_20[2]/spectralon_asd
refl_asd4 = asd_16[2]/asd_21[2]/spectralon_asd
refl_asd5 = asd_16[2]/asd_22[2]/spectralon_asd
      
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference000', 'target000', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
ibsen2 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference001', 'target001', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
ibsen3 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference002', 'target002', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
      
      
fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength, refl_asd, label = 'ASD 16/13')
plt.plot(wavelength, refl_asd1, label = 'ASD 16/14')
plt.plot(wavelength, refl_asd2, label = 'ASD 16/15')
plt.plot(wavelength, refl_asd3, label = 'ASD 16/20')
plt.plot(wavelength, refl_asd4, label = 'ASD 16/21')
plt.plot(wavelength, refl_asd5, label = 'ASD 16/22')
plt.plot(ibsen[0], ibsen[1], label = 'Ibsen 12:04')
plt.plot(ibsen2[0], ibsen2[1], label = 'Ibsen 12:07')
plt.plot(ibsen3[0], ibsen3[1], label = 'Ibsen 12:08')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('Tiefwasser Boje, Ibsen vs ASD_unfertig', fontsize = 18)
legend = plt.legend(ncol = 1)
plt.show()
fig.savefig(os.path.join(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Plots', '1_2_reflectance_ASD_Ibsen_different_E_d.png'))
plt.close()


#2_________________________________________________________________________________________________________________________________________________________________________________________           
asd_2 = reader.read_asd_data(ASD_directory, 'wasser_00002')
asd_3 = reader.read_asd_data(ASD_directory, 'wasser_00003')
asd_4 = reader.read_asd_data(ASD_directory, 'wasser_00004')
asd_5 = reader.read_asd_data(ASD_directory, 'wasser_00005')
asd_6 = reader.read_asd_data(ASD_directory, 'wasser_00006')
asd_0 = reader.read_asd_data(ASD_directory, 'spectralon_00000')
asd_1 = reader.read_asd_data(ASD_directory, 'spectralon_00001')
asd_7 = reader.read_asd_data(ASD_directory, 'spectralon_00007')
asd_8 = reader.read_asd_data(ASD_directory, 'spectralon_00008')
asd_9 = reader.read_asd_data(ASD_directory, 'spectralon_00009')
    
wavelength = asd_2[1]
# refl_asd = asd_2[2]/asd_8[2]*spectralon_asd
# refl_asd1 = asd_3[2]/asd_8[2]*spectralon_asd
# refl_asd2 = asd_4[2]/asd_8[2]*spectralon_asd
# refl_asd3 = asd_5[2]/asd_8[2]*spectralon_asd
# refl_asd4 = asd_6[2]/asd_8[2]*spectralon_asd

refl_asd = asd_2[2]/asd_0[2]/spectralon_asd
refl_asd1 = asd_2[2]/asd_1[2]/spectralon_asd
refl_asd2 = asd_2[2]/asd_7[2]/spectralon_asd
refl_asd3 = asd_2[2]/asd_8[2]/spectralon_asd
refl_asd4 = asd_2[2]/asd_9[2]/spectralon_asd
    
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser_Level1'
#ibsen = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference001', 'target002', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
ibsen2 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference001', 'target003', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
ibsen3 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference001', 'target004', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')

fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength, refl_asd, label = 'ASD 11:31')
plt.plot(wavelength, refl_asd1, label = 'ASD 11:31_2')
plt.plot(wavelength, refl_asd2, label = 'ASD 11:31_3')
plt.plot(wavelength, refl_asd3, label = 'ASD 11:31_5')
plt.plot(wavelength, refl_asd4, label = 'ASD 11:31_6')
#plt.plot(ibsen[0], ibsen[1], label = 'Ibsen 11:29_Bodenprobe')
#plt.plot(ibsen2[0], ibsen2[1], label = 'Ibsen 11:29_2')
plt.plot(ibsen3[0], ibsen3[1], label = 'Ibsen 11:34')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('Flachwasser 1, L_up water', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 2)
plt.show()
fig.savefig(os.path.join(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Plots', '2_reflectance_ASD_Ibsen_verschiedene_target.png'))
plt.close()


#3_________________________________________________________________________________________________________________________________________________________________________________________           
jeti_1 = reader.read_jeti(jeti_directory, 'Jeti_1.dat')[0]
jeti_2 = reader.read_jeti(jeti_directory, 'Jeti_2.dat')[0]
jeti_3 = reader.read_jeti(jeti_directory, 'Jeti_3.dat')[0] #wasser
jeti_4 = reader.read_jeti(jeti_directory, 'Jeti_4.dat')[0] #wasser
jeti_5 = reader.read_jeti(jeti_directory, 'Jeti_5.dat')[0] #wasser
jeti_6 = reader.read_jeti(jeti_directory, 'Jeti_6.dat')[0] #wasser
jeti_7 = reader.read_jeti(jeti_directory, 'Jeti_7.dat')[0] #wasser
jeti_8 = reader.read_jeti(jeti_directory, 'Jeti_8.dat')[0]
jeti_9 = reader.read_jeti(jeti_directory, 'Jeti_9.dat')[0]
jeti_10 = reader.read_jeti(jeti_directory, 'Jeti_10.dat')[0]
jeti_11 = reader.read_jeti(jeti_directory, 'Jeti_11.dat')[0]

wavelength_jeti = jeti_1[0]
spectralon_jeti = spectralon.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', wavelength_jeti)[0]
refl_jeti1 = jeti_3[1]/jeti_1[1]/spectralon_jeti
refl_ges = (jeti_3[1] + jeti_4[1] + jeti_5[1] + jeti_6[1] + jeti_7[1])/(jeti_1[1] + jeti_2[1] + jeti_8[1] + jeti_9[1] + jeti_10[1] + jeti_11[1])*6/5/spectralon_jeti
# hat sich herausgestellt, dass die Unterschiede in den Spektren so gering sind, dass es sich nicht lohnt sie allein einzeln zu plotten.

 
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'
ibsen = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference003', 'target003', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
# ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2'
# ibsen2 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference000', 'target000', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
# ibsen3 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference002', 'target002', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
#  
fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength_jeti, refl_jeti1, label = 'Jeti single measurement')
plt.plot(wavelength_jeti, refl_ges, label = 'Jeti average over all measurements')
plt.plot(ibsen[0], ibsen[1], label = 'Ibsen 12:22')
#plt.plot(ibsen2[0], ibsen2[1], label = 'Ibsen 13:19') # Flachwasser Vergleich
#plt.plot(ibsen3[0], ibsen3[1], label = 'Ibsen 13:25') # Flachwasser Vergleich
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('Tiefwasser Boje, keine passenden ASD Daten dazu', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 2)
plt.show()
fig.savefig(os.path.join(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Plots', '3_reflectance_ASD_Ibsen_Jeti.png'))
plt.close()


#4_________________________________________________________________________________________________________________________________________________________________________________________           
asd_28 = reader.read_asd_data(ASD_directory, 'wasser_00028')
asd_29 = reader.read_asd_data(ASD_directory, 'wasser_00029')
asd_30 = reader.read_asd_data(ASD_directory, 'wasser_00030')
asd_31 = reader.read_asd_data(ASD_directory, 'wasser_00031')
asd_32 = reader.read_asd_data(ASD_directory, 'wasser_00032')
asd_40 = reader.read_asd_data(ASD_directory, 'wasser_00040')
asd_41 = reader.read_asd_data(ASD_directory, 'wasser_00041')
asd_42 = reader.read_asd_data(ASD_directory, 'wasser_00042')
asd_43 = reader.read_asd_data(ASD_directory, 'wasser_00043')
asd_44 = reader.read_asd_data(ASD_directory, 'wasser_00044')
asd_45 = reader.read_asd_data(ASD_directory, 'wasser_00045')
asd_26 = reader.read_asd_data(ASD_directory, 'spectralon_00026')
asd_27 = reader.read_asd_data(ASD_directory, 'spectralon_00027')
asd_33 = reader.read_asd_data(ASD_directory, 'spectralon_00033')
asd_34 = reader.read_asd_data(ASD_directory, 'spectralon_00034') #ist komsich
asd_46 = reader.read_asd_data(ASD_directory, 'spectralon_00046')
asd_47 = reader.read_asd_data(ASD_directory, 'spectralon_00047')
 
wavelength = asd_28[1]
refl_asd = (asd_28[2] + asd_29[2] + asd_30[2] + asd_31[2] + asd_32[2])/(asd_26[2] + asd_27[2] + asd_33[2])*3/5/spectralon_asd
refl_asd1 = (asd_40[2] + asd_41[2] + asd_42[2] + asd_43[2] + asd_44[2] + asd_45[2])/(asd_46[2] + asd_47[2])/3/spectralon_asd
 
ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2_Level1'
ibsen1 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference000', 'target000', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
ibsen2 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference002', 'target002', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')

fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength, refl_asd, label = 'ASD 13:17')
plt.plot(wavelength, refl_asd1, label = 'ASD 13:22')
plt.plot(ibsen1[0], ibsen1[1], label = 'Ibsen 13:19')
plt.plot(ibsen2[0], ibsen2[1], label = 'Ibsen 13:25')
 
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('Flachwasser 2, L_up water', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 2)
plt.show()
fig.savefig(os.path.join(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Plots', '4_reflectance_ASD_Ibsen_Flachwasser_water.png'))
plt.close()


#5_________________________________________________________________________________________________________________________________________________________________________________________           
asd_35 = reader.read_asd_data(ASD_directory, 'bodenprobe1_00035')
asd_36 = reader.read_asd_data(ASD_directory, 'bodenprobe1_00036')
asd_37 = reader.read_asd_data(ASD_directory, 'bodenprobe1_00037')
asd_38 = reader.read_asd_data(ASD_directory, 'bodenprobe1_00038')
asd_39 = reader.read_asd_data(ASD_directory, 'bodenprobe1_00039')

asd_48 = reader.read_asd_data(ASD_directory, 'bodenprobe2_00048')
asd_49 = reader.read_asd_data(ASD_directory, 'bodenprobe2_00049')
asd_50 = reader.read_asd_data(ASD_directory, 'bodenprobe2_00050')
asd_51 = reader.read_asd_data(ASD_directory, 'bodenprobe2_00051')
asd_52 = reader.read_asd_data(ASD_directory, 'bodenprobe2_00052')

asd_33 = reader.read_asd_data(ASD_directory, 'spectralon_00033')
asd_34 = reader.read_asd_data(ASD_directory, 'spectralon_00034') #ist komsich
asd_46 = reader.read_asd_data(ASD_directory, 'spectralon_00046')
asd_47 = reader.read_asd_data(ASD_directory, 'spectralon_00047')
asd_53 = reader.read_asd_data(ASD_directory, 'spectralon_00053')
asd_54 = reader.read_asd_data(ASD_directory, 'spectralon_00054')

wavelength = asd_35[1]
refl_asd = (asd_35[2] + asd_36[2] + asd_37[2] + asd_38[2] + asd_39[2])/(asd_33[2] + asd_46[2] + asd_47[2])*3/5/spectralon_asd
refl_asd1 = (asd_48[2] + asd_49[2] + asd_50[2] + asd_51[2] + asd_52[2])/(asd_53[2] + asd_54[2])*2/5/spectralon_asd

ibsen_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2_Level1'
ibsen = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference001', 'target001', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')
ibsen2 = ibsen_evaluate.reflectance_winnowed_l1(ibsen_directory, '.ibsenL1', 'reference003', 'target003', std_ref = 2, std_ref_r2 = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')

fig = plt.figure(figsize=(18, 10))
plt.plot(wavelength, refl_asd, label = 'ASD 13:20')
plt.plot(wavelength, refl_asd1, label = 'ASD 13:28')
plt.plot(ibsen1[0], ibsen1[1], label = 'Ibsen 13:23')
plt.plot(ibsen2[0], ibsen2[1], label = 'Ibsen 13:30')

plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('Flachwasser 2, Bodenprobe 2', fontsize = 18)
legend = plt.legend(ncol = 1, loc = 2)
plt.show()
fig.savefig(os.path.join(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Plots', '5_reflectance_ASD_Ibsen_Flachwasser_bodenprobe.png'))
plt.close()