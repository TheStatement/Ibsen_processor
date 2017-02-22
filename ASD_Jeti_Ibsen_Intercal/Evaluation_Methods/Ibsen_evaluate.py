'''
Created on 28.07.2016

@author: ried_st
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from Evaluation_Methods import Reader, spectralon_response
from scipy.optimize import curve_fit


spectralon = spectralon_response.Interpolate_Spectralon()
reader = Reader.File_Reader()

class Ibsen_Evaluation(object):
    def __init__(self):
        pass
    
    def reflectance_winnowed_l1(self, directory, file_extension, reference, target, std_ref, std_ref_r2, std_tar_plus, std_tar_minus, std_tar_r2, plot_reflec):
        # is old and needs to be reworked
        
        wavelength = reader.read_ibsen_data(directory, target, file_extension)['wavelength'] #contains the wavelengths for plotting
        
        '''
        reminder:
        read_data returns: ({'data': np_data, 'wavelength': np_data[0], 'number_columns': number_columns, 'comment': comment, 'int_time': int_time, 'header': header})
        '''
        ref = Ibsen_Evaluation.winnow_spectra(self, directory, reference, file_extension, std_ref, std_ref, std_ref_r2)
        tar = Ibsen_Evaluation.winnow_spectra(self, directory, target, file_extension, std_tar_plus, std_tar_minus, std_tar_r2)

        reflectance = tar[2]/ref[2]*100

        if plot_reflec == 'y': # reflectance is returned
            return([wavelength, reflectance])
        else: # only the mean of the winnowed target spectrum is returned
            return([wavelength, tar[2]])
    

    def winnow_spectra(self, input_directory, filename, file_extension, lower_wl, std_plus, std_minus, std_r2):
        '''
        Output: [data_good_spectra_2, data_bad_spectra, data_mean_2, data_std, data_mean_plus, data_mean_minus]
        ['good_spectra'] = data_good_spectra_2; all good spectra
        ['bad_spectra'] = data_bad_spectra; all bad spectra
        ['wavelength'] = wavelength array of the input file
        ['mean_good'] = data_mean_2; mean of all good spectra
        ['std_good'] = data_std; standard deviation of all good spectra
        ['mean_plus'] = data_mean_plus; mean of all good spectra + standard deviation
        ['mean_minus'] = data_mean_minus; mean of all good spectra - standard deviation
        Write all to file?
        
        needs unit test
        '''
        
        data = reader.read_ibsen_data(input_directory, lower_wl, filename, file_extension)
        number_columns = data['number_columns'] # contains the number of data columns.
        wavelength = data['wavelength']
        
        data['data'] = data['data'][3:number_columns] # throws out the first 3 rows with wavelength average and standard deviation
        number_data_columns = number_columns - 3 # for better readability of code
        data_sum = np.sum(data['data'][0:number_columns], axis=1) # adds the sum over each data spectrum to data_sum
        data_sum_mean = np.mean(data_sum) #gets the mean of all sum values
        data_sum_std = np.std(data_sum) #gets standard deviation
        
        
        data_use = []
        for i in range(0,number_data_columns): #throws all spectra out which are too bright or dark
            if ((data_sum[i] - data_sum_mean) < std_plus*data_sum_std) and ((data_sum[i] - data_sum_mean) > -std_minus*data_sum_std): #contains conditions for including or excluding spectra.
                                                                                                                                        #Separate values are used for upper and lower limit
                data_use.append(i)
                
        data_good_spectra = []
        data_bad_spectra = []
        for j in range(0,number_data_columns):
            if j in data_use: # get all spectra which have not been sorted out from data_use
                data_good_spectra.append(data['data'][j]) # n+3 because first 3 rows contain wl, mean and std of all spectra
            else:
                data_bad_spectra.append(data['data'][j])
            
        data_good_spectra = np.array(data_good_spectra) #creates a numpy array from normal python array # kill
        data_mean = np.mean(data_good_spectra, axis=0) #gets mean over all good spectra, is needed for calculation of R2 values
        
        data_use_r2 = [] # contains a R2 value for each spectrum in data_good_spectra
        for spectrum in data_good_spectra: # only works because this parses in an ordered way
            R2 = r2_score(data_mean, spectrum) # get R^2 value for each spectrum
            data_use_r2.append(R2)
            
        data_use_r2_mean = np.mean(data_use_r2) #gets the mean of all R^2 values
        data_use_r2_std = np.std(data_use_r2) #gets standard deviation of R^2 values
        
        data_good_spectra_2 = []
        for value in data_use_r2: # contains all R2 values
            if value - data_use_r2_mean > -std_r2*data_use_r2_std: # condition to throw out spectra with low r^2, higher value means less spectra
                data_good_spectra_2.append(data_good_spectra[data_use_r2.index(value)]) # appends good spectra to the list
            else:
                data_bad_spectra.append(data_good_spectra[data_use_r2.index(value)]) # appends bad spectra to the list
                
        # gets mean and std for the good_spectra_2 for eg plotting
        data_good_spectra_2 = np.array(data_good_spectra_2) #creates a numpy array from normal python array # kill
        data_mean_2 = np.mean(data_good_spectra_2, axis=0) #gets mean over all good spectra
        data_std = np.std(data_good_spectra_2, axis=0, ddof=1) # gets standard deviation of all good spectra
        data_mean_plus = np.add(data_mean_2, data_std) # mean + std for plotting
        data_mean_minus = np.subtract(data_mean_2, data_std) # mean - std for plotting
        
        print('Number good spectra: ' + str(len(data_good_spectra_2)) + '; number bad spectra: ' + str(len(data_bad_spectra))) # prints a message about the ratio of good and bad spectra
        #return([data_good_spectra_2, data_bad_spectra, data_mean_2, data_std, data_mean_plus, data_mean_minus])
        return{'good_spectra': data_good_spectra_2, 'bad_spectra': data_bad_spectra, 'wavelength': wavelength, 'mean_good': data_mean_2, 'std_good': data_std, 'mean_plus': data_mean_plus, 'mean_minus': data_mean_minus}


    def plot_all(self, input_directory, file_extension, lower_wl, instrument):
        for file in os.listdir(input_directory):
            if file.endswith(file_extension):
                filename, file_extension = os.path.splitext(file)
                fig = plt.figure(figsize=(18, 10))
                if instrument == 'asd':
                    data = reader.read_asd_data(input_directory, filename, file_extension)
                    plt.plot(data['wavelength'], data['data'][2])

                else:
                    data = reader.read_ibsen_data(input_directory, lower_wl, filename, file_extension)
                    for i in range(3, data['number_columns']):
                        plt.plot(data['wavelength'], data['data'][i]) # was i+3, is not correct any more. Change if error arises
    
            fig.savefig(os.path.join(input_directory, str(filename) + '_rawdata.png'))
            plt.close()
            
            
    def get_peak_wl(self, input_directory, filename_data, lower_wl, filename_darkcurrent, guess, plot, plot_title, curve_type, spectrometer_type, image_output_directory):
        
        if spectrometer_type == 'ibsen':
            wavelength = reader.read_ibsen_data(input_directory, lower_wl, filename_data[0], '.asc')['wavelength']
            darkcurrent = reader.read_ibsen_data(input_directory, lower_wl, filename_darkcurrent, '.asc')['mean'] # reads reference data
            
            data = np.zeros_like(wavelength)
            for file in filename_data:
                tmp = reader.read_ibsen_data(input_directory, lower_wl, file, '.asc')['mean'] # reads reference data
                tmp = tmp - darkcurrent
                data += tmp
                
        if spectrometer_type == 'jeti':
            jeti_data = np.genfromtxt(input_directory, delimiter = '\t')
            jeti_data = np.transpose(jeti_data)
            wavelength = jeti_data[0]
            
            data = np.zeros_like(wavelength)
            for file in filename_data:
                tmp = jeti_data[file]
                data += tmp
                
        if spectrometer_type == 'asd':
            wavelength_cutoff = 3000 # value larger than highest ASD wavelength
            wavelength = reader.read_asd_data(input_directory, filename_data[0], '.asc', wavelength_cutoff)['wavelength']
            
            data = np.zeros_like(wavelength)
            for file in filename_data:
                tmp = reader.read_asd_data(input_directory, file, '.asc', wavelength_cutoff)['data']
                data += tmp
            
#         ibsen_hg = reader.read_ibsen_data(input_directory, filename_data, '.asc') # reads reference data
#         darkcurrent_hg = reader.read_ibsen_data(input_directory, filename_darkcurrent, '.asc') # reads reference data
        
        
        x = wavelength
        y = data
        
        
        plt.plot(x,y)
        if plot == 'y':
            plt.show()
        
        def func(x, *params): #To use curve_fit, we need a model function, call it func, that takes x and our (guessed) parameters as arguments and returns the corresponding values for y. As our model, we use a sum of gaussians:
            y = np.zeros_like(x)
            for i in range(0, len(params), 3):
                ctr = params[i]
                amp = params[i+1]
                wid = params[i+2]
                if curve_type == 'gauss':
                    y = y + amp * np.exp( -((x - ctr)/wid)**2) # Gaussian
                if curve_type == 'lorentz':
                    y = y + amp * wid**2 / ((x - ctr)**2 + wid**2) # Lorentzian
            return y
        
        popt, pcov = curve_fit(func, x, y, p0 = guess) # performs the actual fit
        fitcurve = func(x, *popt) # for plotting
        
        central_wl = []
        peak_height = []
        peak_width = []
        for i in range(0, int(len(popt)/3)):
            central_wl.append(popt[3*i])
            peak_height.append(popt[3*i+1])
            peak_width.append(popt[3*i+2])
        
        fig = plt.figure(figsize=(12, 7))
        plt.plot(x, y)
        plt.plot(x, fitcurve, 'r-')

        plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
        plt.ylabel('DN', fontsize = 18)
        fig.suptitle(plot_title)
        # legend = plt.legend(ncol = 1, loc = 1)
        if plot == 'y':
            plt.show()
            
        if image_output_directory != '':
            filename = os.path.join(image_output_directory, plot_title) + '.png'
            fig.savefig(filename)
        # plt.close()
        
        return({'central_wl': central_wl, 'peak_height': peak_height, 'peak_width': peak_width, 'covariance': pcov})
    
    def adjust_length(self, parameter, length, character):
        '''adjust_length adds characters to the left of the string to adjust, till the given length is reached
        It takes a string as 'parameter' and a integer as 'length' '''
        if type(parameter) != type('') or type(length) != type(1):
            print ('Type of adjust_length input parameters is not correct')
        if len(parameter) > length:
            print('parameter <' + parameter + '> is too long!')
        else:
            while len(parameter) < length:
                parameter = character + parameter
        return (parameter)
    
     
    def reflectance_winnowed(self, directory, dark_current, reference, target, std_dark, std_ref, std_tar_plus, std_tar_minus, std_tar_r2, plot_reflec):
        '''
        Old program which should not be used anymore, since it is not suitable to work with ibsen Level 1 data
        
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
        
        The reference spectrum (and only the reference) is multipied with the spectralon response. Be careful when handling E_ds spectra (which might be labeled as target).
        '''
        
        ibsendata_directory_noextension = os.path.join(directory, str(target))
        wavelength = reader.read_ibsen_data(directory, target)[0][0] #contains the wavelengths for plotting
        
        '''
        reminder:
        read_data returns: return([np_data, number_columns, comment, int_time, header])
        '''
        
        dark = reader.read_ibsen_data(directory, dark_current)
        #dark_current_avg = dark_current_avg[100:]
        ref = reader.read_ibsen_data(directory, reference)
        #reference_avg = reference_avg[100:]
        tar = reader.read_ibsen_data(directory, target)
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
        ref_mean2 = ref_mean # for testing of functionality
        ref_mean = ref_mean/100/(spectralon.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_22590-41.dat', ref[0][0])[0])
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
            reflectance = tar_mean/ref_mean
            reflectance_plus = tar_mean_plus/ref_mean
            reflectance_minus = tar_mean_minus/ref_mean
        else:
            reflectance = tar_mean
            reflectance_plus = tar_mean_plus
            reflectance_minus = tar_mean_minus
        
        print('number of spectra used: dark current:', len(dark_use),' reference:', len(ref_use), ' target:', len(tar_use_r2_spectra))   
        
        # average over all section______________________________________________________________________________________________________________________________________________________
        reference_all = ref[0][1] - dark_mean
        target_all = tar[0][1] - dark_mean
        reflectance_all = target_all/reference_all

        
        return([wavelength, reflectance, ref_mean, ref_mean2])        # for testing of functionality
        #return([wavelength, reflectance])
        
