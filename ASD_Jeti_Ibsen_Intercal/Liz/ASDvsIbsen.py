'''
Created on 12.07.2016

@author: ried_st
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

directory = r'C:\Users\ried_st\OneDrive\Austausch\Kampagnen\Interkalibrationskampagne\Atwood_Stechlinsee_31_05_2015\ASCII_Data'

def read_asd_data(filename):
    
    
    input_filename = filename + '.dat'
    asd_directory = os.path.join(directory, input_filename)
    #asddata_directory_noextension = os.path.join(input_directory, filename)
    
    
    data_matrix = []
    
    with open(asd_directory, 'r') as asddata:
        searchlines = asddata.readlines()
        
#     for i, line in enumerate(searchlines):
#         if '[DataRaw]' in line: # metadata is collected
#             beginning_data = i
#             tmp = searchlines[i+1].split()
#             number_columns = len(tmp) # gets the number of columns, eg 33 for 30 measurements
#             comment = searchlines[i-10] # gets the line which contains the comment in the usual format
            
    for i, line in enumerate(searchlines):
        if i<500:
            row2 = np.array([float(w) for w in line.split()[1:4]])
            data_matrix.append(row2)
    
    np_data = np.array(data_matrix)
    np_data = np.transpose(np_data) #columns contain the formatted data
    return(np_data)



input_directory = r'C:\Users\ried_st\OneDrive\Austausch\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\Alle zusammen'

def read_data(filename):
    '''
    takes the input directory from line 22 and a filename as input
    output: writes a figure of the input file into the same directory
    '''
    
    
    input_filename = filename + '.asc'
    ibsendata_directory = os.path.join(input_directory, input_filename)
    #ibsendata_directory_noextension = os.path.join(input_directory, filename)
    
    
    data_matrix = []
    
    with open(ibsendata_directory, 'r') as ibsendata:
        searchlines = ibsendata.readlines()
        
    for i, line in enumerate(searchlines):
        if '[DataRaw]' in line: # metadata is collected
            beginning_data = i
            tmp = searchlines[i+1].split()
            number_columns = len(tmp) # gets the number of columns, eg 33 for 30 measurements
            comment = searchlines[i-10] # gets the line which contains the comment in the usual format
            
    for i, line in enumerate(searchlines):
        if (i>beginning_data+100): # only reads the relevant range (942 is lower limit, below plotting not sensible because of detector noise)
            row2 = np.array([float(w) for w in line.split()])
            data_matrix.append(row2)
    
    np_data = np.array(data_matrix)
    np_data = np.transpose(np_data) #columns contain the formatted data
    return([np_data, number_columns, comment])

def plot_reflectance_winnowed(dark_current, reference, target, std_dark, std_ref, std_tar_plus, std_tar_minus, std_tar_r2, plot_reflec):
    '''
    takes the filenames of input files and calculates reflectance, outliers are thrown out
    also uses input_directory specified in line 22
    std_dark = multiple of the standard deviation calculated from integrals over dark current spectra. Spectra above or below std_dark*standard deviation are ignored
        (larger value means more spectra are included)
    std_ref = same as std_dark for the reference spectrum
    std_tar_plus = boundary value for brighter spectra, larger value means more spectra are included
    str_tar_minus = boundary value for darker spectra, larger value means more spectra are included
    std_tar_r2 = boundary value for R^2 coefficient. Values with lower R^2 score than mean-standard deviation are excluded. Larger value means more spectra are included
    plot_reflec = if 'y', reflectance will be plotted, else the mean target spectrum without division by E_d will be plotted
    plot_avg_all = if 'y', the mean value over all spectra will be plotted into the same plot for comparison. Works independent of the rest:
    if switched on the standard reflectance will still be plotted
    
    
    '''
    
    ibsendata_directory_noextension = os.path.join(input_directory, str(target))
    wavelength = read_data(target)[0][0] #contains the wavelengths for plotting
    
    '''
    reminder:
    read_data returns: return([np_data, number_rows, comment])
    '''
    
    dark = read_data(dark_current)
    #dark_current_avg = dark_current_avg[100:]
    ref = read_data(reference)
    #reference_avg = reference_avg[100:]
    tar = read_data(target)
    #target_avg = target_avg[100:]

    
    # dark current section______________________________________________________________________________________________________________________________________________________________
    dark_sum = np.sum(dark[0][3:dark[1]], axis=1) # integrates over the whole spectrum (for identification of outliers), adds the sum over each dark current spectrum to dark_sum
    dark_sum_mean = np.mean(dark_sum) #gets the mean of all sum values
    dark_sum_std = np.std(dark_sum) #gets standard deviation
    
    dark_use = []
    for i in range(0,dark[1]-3): #throws all dark currents out which are too high or low
        if abs(dark_sum[i] - dark_sum_mean) < std_dark*dark_sum_std: #1.5 times standard deviation is used
            dark_use.append(i)
    
    #dark_use_spectra = np.zeros(924) #preallocation
    dark_use_spectra = []
    for n in dark_use: # get all spectra which have not been sorted out from dark_use
        dark_use_spectra.append(dark[0][n+3]) # n+3 because first 3 rows contain wl, mean and std of all spectra

    dark_use_spectra = np.array(dark_use_spectra) #creates a numpy array from normal python array
    dark_mean = np.mean(dark_use_spectra, axis=0) #gets mean over all curves for further use
    #dark_std = np.std(dark_use_spectra, axis=0)
        
        
    # reference spectrum section________________________________________________________________________________________________________________________________________________________ 
    ref[0][3:ref[1]] -= dark_mean # subtracts dark current from reference
    ref_sum = np.sum(ref[0][3:ref[1]], axis=1) # adds the sum over each reference spectrum to ref_sum
    ref_sum_mean = np.mean(ref_sum) #gets the mean of all sum values
    ref_sum_std = np.std(ref_sum) #gets standard deviation
    
    ref_use = []
    for i in range(0,ref[1]-3): #throws all reference spectra out which are too bright or dark
        if abs(ref_sum[i] - ref_sum_mean) < std_ref*ref_sum_std: #1.5 times standard deviation is used
            ref_use.append(i)
            
    ref_use_spectra = []
    for n in ref_use: # get all spectra which have not been sorted out from ref_use
        ref_use_spectra.append(ref[0][n+3]) # n+3 because first 3 rows contain wl, mean and std of all spectra
        
    ref_use_spectra = np.array(ref_use_spectra) #creates a numpy array from normal python array
    ref_mean = np.mean(ref_use_spectra, axis=0) #gets mean over all curves for further use
    ref_std = np.std(ref_use_spectra, axis=0)
    ref_mean_plus = np.add(ref_mean, ref_std)
    ref_mean_minus = np.subtract(ref_mean, ref_std)
    
    
    # target spectrum section________________________________________________________________________________________________________________________________________________________
    tar[0][3:tar[1]] -= dark_mean # subtracts dark current from target
    tar_sum = np.sum(tar[0][3:tar[1]], axis=1) # adds the sum over each target spectrum to tar_sum
    tar_sum_mean = np.mean(tar_sum) #gets the mean of all sum values
    tar_sum_std = np.std(tar_sum) #gets standard deviation
    
    tar_use = []
    for i in range(0,tar[1]-3): #throws all target spectra out which are too bright or dark
        if ((tar_sum[i] - tar_sum_mean) < std_tar_plus*tar_sum_std) and ((tar_sum[i] - tar_sum_mean) > -std_tar_minus*tar_sum_std): #contains conditions for including or excluding spectra.
                                                                                                                                    #Separate values are used for upper and lower limit
            tar_use.append(i)
            
    tar_use_spectra = []
    for n in tar_use: # get all spectra which have not been sorted out from tar_use
        tar_use_spectra.append(tar[0][n+3]) # n+3 because first 3 rows contain wl, mean and std of all spectra
        
    tar_use_spectra = np.array(tar_use_spectra) #creates a numpy array from normal python array
    tar_mean = np.mean(tar_use_spectra, axis=0) #gets mean over all curves for further use
    tar_std = np.std(tar_use_spectra, axis=0, ddof=1)
    tar_mean_plus = np.add(tar_mean, tar_std)
    tar_mean_minus = np.subtract(tar_mean, tar_std)
    
    tar_use_r2 = []
    for spectrum in tar_use_spectra:
        R2 = r2_score(tar_mean, spectrum) # get R^2 value for each spectrum
        tar_use_r2.append(R2)
        
    tar_use_r2_mean = np.mean(tar_use_r2) #gets the mean of all R^2 values
    tar_use_r2_std = np.std(tar_use_r2) #gets standard deviation of R^2 values
    
    tar_use_r2_spectra = []
    for value in tar_use_r2:
        if value - tar_use_r2_mean > -std_tar_r2*tar_use_r2_std: # condition to throw out spectra with low r^2, higher value means less spectra
            tar_use_r2_spectra.append(tar_use_spectra[tar_use_r2.index(value)]) # appends good spectra to the list
    
    # plot reflectance or target mean_______________________________________________________________________________________________________________________________________________
    
    if plot_reflec == 'y':
        reflectance = tar_mean*0.1/ref_mean*100 #grey spectralon (*0.1), percent (*100)
        reflectance_plus = tar_mean_plus*0.1/ref_mean*100
        reflectance_minus = tar_mean_minus*0.1/ref_mean*100
    else:
        reflectance = tar_mean
        reflectance_plus = tar_mean_plus
        reflectance_minus = tar_mean_minus
    
    print('number of spectra used: dark current:', len(dark_use),' reference:', len(ref_use), ' target:', len(tar_use_r2_spectra))   
    
    # average over all section______________________________________________________________________________________________________________________________________________________
    reference_all = ref[0][1] - dark_mean
    target_all = tar[0][1] - dark_mean
    reflectance_all = target_all/reference_all
    
    return([wavelength, reflectance])
#     # plotting section______________________________________________________________________________________________________________________________________________________________
#     
#     
#     fig = plt.figure(figsize=(18, 10))
#     plt.plot(wavelength, reflectance)
#     plt.plot(wavelength, reflectance_plus, 'r')
#     plt.plot(wavelength, reflectance_minus, 'r')
#     
#     if plot_avg_all == 'y':
#         plt.plot(wavelength, reflectance_all, 'g')
#         
#     plt.xlabel('Wavelength [nm]', fontsize = 18)
#     plt.ylabel('Reflectance', fontsize = 18)
#     fig.suptitle(str(target) + '.asc: ' + '\n' + read_data(target)[2])
#     
#     if plot_reflec == 'y':
#         fig.savefig(os.path.join(input_directory, 'reflectance_' + str(target) + '_' + str(reference) + '_' + str(dark_current) + '_winnowed.png'))
#     else:
#         plt.ylabel('Radiance (uncalibrated) [W/m^2 nm]', fontsize = 18)
#         fig.savefig(os.path.join(input_directory, 'average_' + str(target) + '_' + str(dark_current) + '_winnowed.png'))
#         
#     plt.show()
#     plt.close()
#     
#     if plot_single_measurements == 'y':
#         directory_single = os.path.join(input_directory, str(target) + '_' + str(reference))
#         if not os.path.exists(directory_single):
#             os.makedirs(directory_single)
#         for i in range(3,tar[1]):
#             ref_single = tar[0][i]/ref_mean
#             fig = plt.figure(figsize=(18, 10))
#             plt.plot(wavelength, ref_single)
#             
#             if plot_avg_all == 'y':
#                 plt.plot(wavelength, reflectance_all, 'g')
#                 
#             plt.xlabel('Wavelength [nm]', fontsize = 18)
#             plt.ylabel('Reflectance', fontsize = 18)
#             fig.suptitle(str(target) + '.asc: ' + '\n' + read_data(target)[2])
#             
#             fig.savefig(os.path.join(directory_single, 'reflectance_' + str(target) + '_' + str(i) + '_' + str(reference) + '_' + str(dark_current) + '.png'))
#             plt.close()

def plot_asd_all():
    for file in os.listdir(directory):
        if file.endswith('.dat'):
            filename, file_extension = os.path.splitext(file)
            asd_data = read_asd_data(filename)
            fig = plt.figure(figsize=(18, 10))
            plt.plot(asd_data[1], asd_data[2])
            plt.xlabel('Wavelength [nm]', fontsize = 18)
            plt.ylabel('DN', fontsize = 18)
            fig.suptitle(filename)
            fig.savefig(os.path.join(directory, filename + '.png'))
            plt.close()


#1_________________________________________________________________________________________________________________________________________________________________________________________           
asd_tar1 = '00016'
asd_ref1 = '00019'
asd_sky1 = '00017'
asd_16 = read_asd_data(asd_tar1)
asd_19 = read_asd_data(asd_ref1)
asd_17 = read_asd_data(asd_sky1)
refl_asd = (asd_16[2]-0.024*asd_17[2])/asd_19[2]*10

asd_tar11 = '00021'
asd_ref11 = '00023'
asd_sky11 = '00022'
asd_21 = read_asd_data(asd_tar11)
asd_23 = read_asd_data(asd_ref11)
asd_22 = read_asd_data(asd_sky11)
refl_asd1 = (asd_21[2]-0.024*asd_22[2])/asd_23[2]*10
ibsen = plot_reflectance_winnowed('darkcurrent008', 'reference008', 'target006', std_dark = 2, std_ref = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')


fig = plt.figure(figsize=(18, 10))
plt.plot(asd_16[1], refl_asd, label = 'ASD 14:04 GR')
plt.plot(asd_21[1], refl_asd1, label = 'ASD 14:07 GR')
plt.plot(ibsen[0], ibsen[1], label = 'Ibsen')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('asd: 00016-00017/00019, 31.5. 14:04 \n asd: _00021-00022/00023, 31.5. 14:07 \n ibsen: darkcurrent008, reference008, target006, 31.5. 14:06', fontsize = 18)
legend = plt.legend(ncol = 1)
plt.show()
fig.savefig(os.path.join(directory, 'reflectance' + asd_tar1 + '_' + asd_ref1 + asd_tar11 + '_' + asd_ref11 + '_ibsen.png'))
plt.close()


#2_________________________________________________________________________________________________________________________________________________________________________________________
asd_tar2 = '00028'
asd_ref2 = '00030'
asd_sky2 = '00029'
asd_28 = read_asd_data(asd_tar2)
asd_30 = read_asd_data(asd_ref2)
asd_29 = read_asd_data(asd_sky2)
refl_asd2 = (asd_28[2]-0.024*asd_29[2])/asd_30[2]*10

asd_ref2_1 = '00027'
asd_27 = read_asd_data(asd_ref2_1)
refl_asd2_1 = (asd_28[2]-0.024*asd_29[2])/asd_27[2]*100

ibsen2 = plot_reflectance_winnowed('darkcurrent009', 'reference009', 'target008', std_dark = 2, std_ref = 2, std_tar_plus = 1.5, std_tar_minus = 1.5, std_tar_r2 = 1.5, plot_reflec = 'y')


fig = plt.figure(figsize=(18, 10))
plt.plot(asd_28[1], refl_asd2, label = 'ASD GR')
plt.plot(asd_28[1], refl_asd2_1, label = 'ASD WR')
plt.plot(ibsen2[0], ibsen2[1], label = 'Ibsen')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('asd: 00028-00029/00030 (GR) and 00027 (WR), 31.5. 14:14 \n ibsen: darkcurrent009, reference009, target008, 31.5. 14:15', fontsize = 18)
legend = plt.legend(ncol = 1)
plt.show()
fig.savefig(os.path.join(directory, 'reflectance' + asd_tar2 + '_' + asd_ref2 + '_ibsen.png'))
plt.close()


#3_________________________________________________________________________________________________________________________________________________________________________________________
asd_tar3 = '00034'
asd_ref3 = '00036'
asd_sky3 = '00035'
asd_34 = read_asd_data(asd_tar3)
asd_36 = read_asd_data(asd_ref3)
asd_35 = read_asd_data(asd_sky3)
refl_asd3 = (asd_34[2]-0.024*asd_35[2])/asd_36[2]*10

asd_ref3_1 = '00032'
asd_32 = read_asd_data(asd_ref3_1)
refl_asd3_1 = (asd_34[2]-0.024*asd_35[2])/asd_32[2]*100

ibsen3 = plot_reflectance_winnowed('darkcurrent010', 'reference010', 'target009', std_dark = 2, std_ref = 2, std_tar_plus = 0.5, std_tar_minus = 2, std_tar_r2 = 1.5, plot_reflec = 'y')


fig = plt.figure(figsize=(18, 10))
plt.plot(asd_34[1], refl_asd3, label = 'ASD GR')
plt.plot(asd_34[1], refl_asd3_1, label = 'ASD WR')
plt.plot(ibsen3[0], ibsen3[1], label = 'Ibsen')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('asd: 00034-00035/00036 (GR) and 00033 (WR), 31.5. 14:17 \n ibsen: darkcurrent010, reference010, target009, 31.5. 14:17', fontsize = 18)
legend = plt.legend(ncol = 1)
plt.show()
fig.savefig(os.path.join(directory, 'reflectance' + asd_tar3 + '_' + asd_ref3 + '_ibsen.png'))
plt.close()


#4 and 5______________________________________________________________________________________________________________________________________________________________________________________
asd_tar4 = '00012'
asd_ref4 = '00011'
asd_sky4 = '00013'
asd_12 = read_asd_data(asd_tar4)
asd_11 = read_asd_data(asd_ref4)
asd_13 = read_asd_data(asd_sky4)
refl_asd4 = (asd_12[2]-0.024*asd_13[2])/asd_11[2]*100

asd_ref4_1 = '00014'
asd_14 = read_asd_data(asd_ref4_1)
refl_asd4_1 = (asd_12[2]-0.024*asd_13[2])/asd_14[2]*100

asd_tar5 = '00008'
asd_ref5 = '00007'
asd_sky5 = '00009'
asd_8 = read_asd_data(asd_tar5)
asd_7 = read_asd_data(asd_ref5)
asd_9 = read_asd_data(asd_sky5)
refl_asd5 = (asd_8[2]-0.024*asd_9[2])/asd_7[2]*100

asd_ref5_1 = '00010'
asd_10 = read_asd_data(asd_ref5_1)
refl_asd5_1 = (asd_8[2]-0.024*asd_9[2])/asd_10[2]*100

ibsen4 = plot_reflectance_winnowed('darkcurrent005', 'reference005', 'target004', std_dark = 2, std_ref = 2, std_tar_plus = 0.5, std_tar_minus = 2, std_tar_r2 = 1.5, plot_reflec = 'y')


fig = plt.figure(figsize=(18, 10))
plt.plot(asd_12[1], refl_asd4, label = 'ASD WR 13:58')
plt.plot(asd_12[1], refl_asd4_1, label = 'ASD WR 13:59')
plt.plot(ibsen4[0], ibsen4[1], label = 'Ibsen')
plt.plot(asd_8[1], refl_asd5, label = 'ASD WR 13:55')
plt.plot(asd_8[1], refl_asd5_1, label = 'ASD WR 13:56')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('asd: 00012-00013/00011 (WR) 31.5. 13:58 and 00014 (WR), 13:59 \n asd: 00008-00009/00007 (WR) 31.5. 13:55 and 00010 (WR), 13:56 \n ibsen: darkcurrent005, reference005, target004, 31.5. 13:58', fontsize = 18)
legend = plt.legend(ncol = 1)
plt.show()
fig.savefig(os.path.join(directory, 'reflectance' + asd_tar4 + '_' + asd_ref4 + '_ibsen.png'))
plt.close()


            
#6_________________________________________________________________________________________________________________________________________________________________________________________
asd_tar6 = '00004'
asd_ref6 = '00003'
asd_sky6 = '00005'
asd_4 = read_asd_data(asd_tar6)
asd_3 = read_asd_data(asd_ref6)
asd_5 = read_asd_data(asd_sky6)
refl_asd6 = (asd_4[2]-0.024*asd_5[2])/asd_3[2]*100

asd_ref6_1 = '00006'
asd_6 = read_asd_data(asd_ref6_1)
refl_asd6_1 = (asd_4[2]-0.024*asd_5[2])/asd_6[2]*100

ibsen6 = plot_reflectance_winnowed('darkcurrent005', 'reference005', 'target003', std_dark = 2, std_ref = 2, std_tar_plus = 0.5, std_tar_minus = 2, std_tar_r2 = 1.5, plot_reflec = 'y')


fig = plt.figure(figsize=(18, 10))
plt.plot(asd_4[1], refl_asd6, label = 'ASD WR 13:53')
plt.plot(asd_4[1], refl_asd6_1, label = 'ASD WR 13:54')
plt.plot(ibsen6[0], ibsen6[1], label = 'Ibsen')
plt.xlabel('Wavelength [nm]', fontsize = 18)
plt.ylabel('Reflectance [%]', fontsize = 18)
fig.suptitle('asd: 00004-00005/00003 (WR) 31.5. 13:58 and 00006 (WR), 13:59 \n ibsen: darkcurrent005, reference005, target003, 31.5. 13:53', fontsize = 18)
legend = plt.legend(ncol = 1)
plt.show()
fig.savefig(os.path.join(directory, 'reflectance' + asd_tar6 + '_' + asd_ref6 + '_ibsen.png'))
plt.close()


