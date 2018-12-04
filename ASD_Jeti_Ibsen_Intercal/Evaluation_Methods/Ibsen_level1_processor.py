'''
Created on 11.08.2016

@author: ried_st
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate



spectralon_function = spectralon_response.Interpolate_Spectralon()
reader = Reader.File_Reader()
evaluate = Ibsen_evaluate.Ibsen_Evaluation()


class Evaluation_Calibration(object):
    def __init__(self):
        pass
    
    def ibsen_nonlinearity_evaluation(self, input_directory, number_files, lower_wl, output_directory, output_filename, sigma_fine, step_size_fine, sigma_coarse, step_size_coarse, DN_transition_fine_coarse, plot, two_step):
        '''
        two_step = 'y': data, which is used for nonlinearity calculation for low and high DN
        '''
        wavelength = reader.read_ibsen_data(input_directory, lower_wl, 'darkcurrent000', '.asc')['wavelength']
        
        # first, we plot all spectra normalized to integration time, to see if there are saturation problems somewhere
        fig = plt.figure(figsize=(18, 10))
        for i in range(0, number_files):
            ref = reader.read_ibsen_data(input_directory, lower_wl, 'reference' + evaluate.adjust_length(str(i), 3, '0'), '.asc')
            dark = reader.read_ibsen_data(input_directory, lower_wl, 'darkcurrent' + evaluate.adjust_length(str(i), 3, '0'), '.asc')
            spectrum = (ref['mean']-dark['mean'])/ref['int_time']
            plt.plot(wavelength, spectrum, label = ref['int_time'])
        plt.xlabel(r'Wavelength $[nm]$', fontsize = 18)
        plt.ylabel(r'DN', fontsize = 18)
        fig.suptitle('All used spectra normalized to integration time', fontsize = 18)
        legend = plt.legend(ncol = 1, loc = 1)
        if plot == 'y':
            plt.show()
        plt.close()

   
        
        max_lowest_int_time = max(reader.read_ibsen_data(input_directory, lower_wl, 'reference000', '.asc')['mean']-reader.read_ibsen_data(input_directory, lower_wl, 'darkcurrent000', '.asc')['mean'])
        ref_max = 'reference' + evaluate.adjust_length(str(number_files-1), 3, '0') # number_files - 1 because lowest file starts at 0 (0....16 = 17 files)
        dark_max = 'darkcurrent' + evaluate.adjust_length(str(number_files-1), 3, '0')
        min_highest_int_time = min(reader.read_ibsen_data(input_directory, lower_wl, ref_max, '.asc')['mean']-reader.read_ibsen_data(input_directory, lower_wl, dark_max, '.asc')['mean'])
        # Needs to be slightly above the hightest value of the lowest integration time (information at low DN is important, because highest nonlinearity there.
        # it needs to be above because the numpy interpolate method does not extrapolate, so for earch wavelength the reference value needs to be within the interval
        print('Maximum value of the lowest integration time measurement is:', max_lowest_int_time)
        print('Minimum value of the highest integration time measurement is:', min_highest_int_time)
        
        data = np.empty((0,len(wavelength)), int) # preallocation of matrix for all measurements (corrected for dark current)
        int_times = [] # list of integration times
        
        for i in range(0, number_files): # prepares a matrix with all files, which are used for nonlinearity
            ref = reader.read_ibsen_data(input_directory, lower_wl, 'reference' + evaluate.adjust_length(str(i), 3, '0'), '.asc') # reads the reference data
            dark = reader.read_ibsen_data(input_directory, lower_wl, 'darkcurrent' + evaluate.adjust_length(str(i), 3, '0'), '.asc') # reads the darkcurrent
            result = ref['mean']-dark['mean']
            int_times.append(ref['int_time'])
            data = np.vstack([data, result]) # adds data to the preallocated matrix
            
        data = np.transpose(data)
        print('For nonlinearity used integration times are:', int_times)
        
        
        data_fine = np.empty((0,len(data[0])), int) # preallocation
        data_coarse = np.empty((0,len(data[0])), int)
        if two_step == 'y':
            # get data for fine mode (for low DN)
            for line in data:
                if min(line) < min_highest_int_time:
                    data_fine = np.vstack([data_fine, line])
                    
            for line in data:
                if max(line) > max_lowest_int_time:
                    data_coarse = np.vstack([data_coarse, line])
                    
        else:
            for line in data:
                data_fine = np.vstack([data_fine, line])
            
       
# old stuff, replaced by fresh code. Remails here in case new stuff is bullshit
#         values = np.array([max(x) for x in data])
#         index = np.where(values > max_lowest_int_time)[0] 
#         
#         data = data[index[0]:max(index)]
        

        
        fig = plt.figure(figsize=(18, 10)) # prepare plot
        plt.xlabel('Raw DN', fontsize = 18)
        plt.ylabel('Expected DN normalized to 1050 DN', fontsize = 18)
        
        
        # first the find mode######################################################################################################################
        all_values_fine = []
        all_nonlin_fine = []
        for line in data_fine:
            DN_values_fine = np.append(line, [min_highest_int_time]) # max_lowest_int_time is appended to int-time series of channel i
            DN_values_fine = np.sort(DN_values_fine) # values are sorted for size to enable interpolation
            interpol = np.interp(min_highest_int_time, line, int_times) # interpolates a fake int time
            tmp_int_time = np.sort(np.append([int_times], [interpol]))
            result_fine = np.divide(DN_values_fine, tmp_int_time)*interpol/min_highest_int_time # value by value division of DN/int_time and normalization to min_highest_int_time
             
#             plt.plot(DN_values_fine, result_fine, marker='x', linestyle='')
            all_values_fine = np.append(all_values_fine, DN_values_fine)
            all_nonlin_fine = np.append(all_nonlin_fine, result_fine)
         
         
        all_array = [all_values_fine, all_nonlin_fine] # schreibt die Gaudi in ein array
        all_array = np.transpose(all_array)
        all_tuple = tuple(all_array) # wird in tuple arrangiert, damit die zusammengehoerigen Werte zusammen bleiben
        all_sorted = sorted(all_tuple, key=lambda tup: tup[0]) # wird sortiert nach values (= tup[0])
        all_sorted = np.transpose(list(all_sorted)) # nach der Sortierung wird wieder in array geschrieben
        
        x = all_sorted[0]
        y = all_sorted[1]
        plt.plot(x, y, marker='x', linestyle='', color = 'b')
        
        def kernel(x, shift, sigma):
            return np.exp(-((x-shift)**2/(2*sigma**2))) 
        
        res_fine = [] # first iteration for fine mode
        xnew_fine = np.arange(min(x), max(x), step_size_fine)
        for i in xnew_fine:
            res_fine.append(np.sum(kernel(x, i, sigma_fine)*y)/ np.sum(kernel(x, i, sigma_fine)))
            
        # x = xnew_fine, y = res_fine
        # Korrektur faktor von max_lowest_int_time zu min_highest_int_time berechnen, um Normalisierung auf gleichen DN Wert sicherzustellen
        correction_factor = np.interp(max_lowest_int_time, xnew_fine, res_fine)
        
        if two_step == 'y':
            # now the coarse mode ###################################################
            all_values_coarse = []
            all_nonlin_coarse = []
            for line in data_coarse:
                DN_values_coarse = np.append(line, [max_lowest_int_time]) # max_lowest_int_time is appended to int-time series of channel i
                DN_values_coarse = np.sort(DN_values_coarse) # values are sorted for size to enable interpolation
                interpol = np.interp(max_lowest_int_time, line, int_times) # interpolates a fake int time
                tmp_int_time = np.sort(np.append([int_times], [interpol]))
                result_coarse = np.divide(DN_values_coarse, tmp_int_time)*interpol/max_lowest_int_time*correction_factor #check if works correctly: nonlinearity curve should lead through max_lowest_int_time
                
    #             plt.plot(DN_values_coarse, result_coarse, marker='x', linestyle='')
                all_values_coarse = np.append(all_values_coarse, DN_values_coarse)
                all_nonlin_coarse = np.append(all_nonlin_coarse, result_coarse)
            
            
            all_array_2 = [all_values_coarse, all_nonlin_coarse] # schreibt die Gaudi in ein array
            all_array_2 = np.transpose(all_array_2)
            all_tuple_2 = tuple(all_array_2) # wird in tuple arrangiert, damit die zusammengehoerigen Werte zusammen bleiben
            all_sorted_2 = sorted(all_tuple_2, key=lambda tup: tup[0]) # wird sortiert nach values (= tup[0])
            all_sorted_2 = np.transpose(list(all_sorted_2)) # nach der Sortierung wird wieder in array geschrieben
            
            print(all_sorted.shape)
            print(all_sorted_2.shape)
            
            x = all_sorted_2[0]
            y = all_sorted_2[1]
            plt.plot(x, y, marker='x', linestyle='', color = 'r')
            
            
            res_coarse = [] # second iteration for coarse mode
            xnew_coarse = np.arange(min(x), max(x), step_size_coarse)
            for i in xnew_coarse:
                res_coarse.append(np.sum(kernel(x, i, sigma_coarse)*y)/ np.sum(kernel(x, i, sigma_coarse)))


        ################################################################################################################################################
        
         
        # normalization_value = np.mean(res_coarse) # was not really a good idea. Does no real harm, but does not improve either
        
        
        res_total = []
        xnew_total = []
        if two_step == 'y':
            for i in range(0, len(xnew_fine)):
                if xnew_fine[i] < DN_transition_fine_coarse:
                    xnew_total.append(xnew_fine[i])
                    res_total.append(res_fine[i])
                    
            for i in range(0, len(xnew_coarse)):
                if xnew_coarse[i] > DN_transition_fine_coarse:
                    xnew_total.append(xnew_coarse[i])
                    res_total.append(res_coarse[i])
        else:
            res_total = res_fine # if nonlinearity calculation is not done in 2 steps, the fine mode contains the whole thing
            xnew_total = xnew_fine
                
        # res_total = res_total/normalization_value # replaces normalization to max_lowest_int_time by normalization to mean of res_coarse.
        # this can be done, because the normalization is random and has no effect, if response is calculated with the applied nonlinearity

        
        plt.plot(xnew_total, res_total, marker='o', linestyle='-')
        
        if plot == 'y':
            plt.show()
        plt.close()
        
        array_write = np.transpose([xnew_total, res_total])
        np.savetxt(fname = (os.path.join(output_directory, output_filename)), X = array_write, fmt = '%.5e', delimiter = '\t')
        ################################################################################################################################################################
        
        
        
    def get_response(self, input_directory, output_directory, output_filename, nonlinearity_directory, nonlinearity_directory_2, transition_wl, rasta_directory, sigma, step_size, min_int_time, plot):
        '''
        Important: unly use spectra with high integration time and low noise!
        Make sure no spectra with saturation issues are in the input folder
        
        if nonlinearity_directory_2 != '' then both nonlinearity files are used, otherwise all channels are processed with the first nonlinearity file
        '''
        
        
        nonlinearity = np.genfromtxt(nonlinearity_directory, delimiter = '\t')
        nonlinearity = np.transpose(nonlinearity) #nonlinearity[0] = DN values; nonlinearity[1] = correction factors
        
        if nonlinearity_directory_2 != '': 
            nonlinearity_2 = np.genfromtxt(nonlinearity_directory_2, delimiter = '\t')
            nonlinearity_2 = np.transpose(nonlinearity_2) #nonlinearity[0] = DN values; nonlinearity[1] = correction factors
        
        if plot == 'y': # plot the nonlinearity raw data ###########
            fig = plt.figure(figsize=(18, 10))    
            plt.plot(nonlinearity[0], nonlinearity[1], label = 'Nonlinearity 1')
            if nonlinearity_directory_2 != '':
                plt.plot(nonlinearity_2[0], nonlinearity_2[1], label = 'Nonlinearity 2')
            plt.xlabel('DN', fontsize = 18)
            plt.ylabel('Nonlinearity correction factor', fontsize = 18)
            legend = plt.legend(ncol = 1, loc = 0)
            fig.suptitle('Nonlinearity raw data', fontsize = 18)
            plt.show()
            
        
        rasta_ptb = np.genfromtxt(rasta_directory)
        rasta_ptb = np.transpose(rasta_ptb)
        
        x = []
        y = []
        y_2 = []
        int_times = [] # future list of integration times, which are used for the response file
        fig = plt.figure(figsize=(18, 10)) # needs to be here, sets image size for upcoming plot
        for file in os.listdir(input_directory): # files from directory are parsed
            if file.endswith('.asc') and 'reference' in file:
                filename, file_extension = os.path.splitext(file)
                ref = reader.read_ibsen_data(input_directory, 0, filename, file_extension)
                ref_2 = reader.read_ibsen_data(input_directory, 0, filename, file_extension)
                if ref['int_time'] >= min_int_time:
                    int_times.append(ref['int_time'])
                    dark = reader.read_ibsen_data(input_directory, 0, 'darkcurrent' + filename.strip('reference'), file_extension)
            
                    for i in range(0, len(ref['data'][1])):
                        ref['mean'][i] = ref['mean'][i]/np.interp(ref['mean'][i], nonlinearity[0], nonlinearity[1]) #corrects for nonlinearity
                        if nonlinearity_directory_2 != '':
                            ref_2['mean'][i] = ref_2['mean'][i]/np.interp(ref_2['mean'][i], nonlinearity_2[0], nonlinearity_2[1]) #corrects for nonlinearity with second nonlinearity
                    
                    result = (ref['mean'] - dark['mean'])/ref['int_time'] # normalization to integration time
                    if nonlinearity_directory_2 != '':
                        result_2 = (ref_2['mean'] - dark['mean'])/ref['int_time'] # second nonlinearity
                    wavelength = ref['wavelength']
                    x = np.append(x, wavelength) # contains x-times the ibsen wavelengths. x = number of used integration times\files
                    y = np.append(y, result) # contains all used ibsen measurements normalized to integration time
                    if nonlinearity_directory_2 != '':
                        y_2 = np.append(y_2, result_2) # second nonlinearity
                    plt.plot(wavelength, result, label = ref['comment']) # all normalized ibsen measurements are plotted to one graph
                    if nonlinearity_directory_2 != '':
                        plt.plot(wavelength, result_2, label = ref['comment']) # second nonlinearity
                    
                    
        print('For response used integration times:', int_times)
        plt.xlabel('Wavelength [nm]', fontsize = 18)
        plt.ylabel('DN normalized to integration time', fontsize = 18)
        #legend = plt.legend(ncol = 2)
        if plot == 'y':
            plt.show()
        plt.close()
        
        
        def kernel(x, shift, sigma): # Definition Gauss Filter: x = zu glaettende Daten, shift = Filterintervall, sigma = Filterbreite
            return np.exp(-((x-shift)**2/(2*sigma**2)))
        

        res = []
        res_2 = []
        xnew = np.arange(min(x), max(x), step_size)
        for i in xnew:
            res.append(np.sum(kernel(x, i, sigma)*y)/ np.sum(kernel(x, i, sigma))) # dont fully understand why it works but it does
            if nonlinearity_directory_2 != '':
                res_2.append(np.sum(kernel(x, i, sigma)*y_2)/ np.sum(kernel(x, i, sigma)))
        res = np.array(res)
        if nonlinearity_directory_2 != '':
            res_2 = np.array(res_2)
            
            fig = plt.figure(figsize=(18, 10))
            plt.plot(xnew, res/res_2) # name plot
            plt.xlabel('DN', fontsize = 18)
            plt.ylabel('Nonlinearity 1/Nonlinearity 2', fontsize = 18)
            fig.suptitle('Ratio of the two used nonlinearities', fontsize = 18)
            plt.show()
        
        # plot the nonlinearity corrected rawdata and the smoothed response curve #########################################################################################
        fig = plt.figure(figsize=(18, 10))
        plt.plot(x, y, marker='x', linestyle='')
        if nonlinearity_directory_2 != '':
            plt.plot(x, y_2, marker='x', linestyle='')
        plt.plot(xnew, res, marker='.', linestyle='-') # xnew = new 'wavelengths' after smoothing, res = smoothed result
        if nonlinearity_directory_2 != '':
            plt.plot(xnew, res_2, marker='.', linestyle='-')
        plt.xlabel('Wavelength [nm]', fontsize = 18)
        plt.ylabel('DN normalized to integration time', fontsize = 18)
        if plot == 'y':
            plt.show()
        plt.close()
        # plot end ########################################################################################
        
        print(res)
        # now the 2 results from 2 nonlinearities need to be fused #########################################################################################
        if nonlinearity_directory_2 != '':
            lower_wl = min(xnew, key=lambda x:abs(x-float(transition_wl))) #find closest WL to lower reading border
            lower_wl_position = int(np.where(xnew==lower_wl)[0]) # returns integer with position of lower_wl
            res_cut = res[:lower_wl_position] # cuts data to desired shape (lower_wl to max WL) test!
            res_2_cut = res_2[lower_wl_position:]
            res_total = np.append(res_cut, res_2_cut, axis = 0)# stack together test!
        else:
            res_total = res
            
        print(res_total)
        rasta_ptb_resample = np.interp(xnew, rasta_ptb[0], rasta_ptb[1])*10**-6 # RASTA PTB measurement is resampled to Ibsen wavelengths, xnew contains new "wavelengths" after gauss filtering the measurements
        # factor 10**-6 converts RASTA response from W/m^3.sr to mW/m^2.nm.sr, 10**-9 m->nm, 10**3 W->mW
        ibsen_response = np.divide(rasta_ptb_resample, res_total)
        
        
        fig = plt.figure(figsize=(18, 10))
        plt.xlabel('Wavelength [nm]', fontsize = 18)
        plt.ylabel(r'All normalized to 1', fontsize = 18)
        plt.plot(xnew, ibsen_response/max(ibsen_response), marker='', linestyle='-', label = 'Ibsen inverse response')
        plt.plot(xnew, res_total/max(res_total), marker='', linestyle='-', label = 'Smoothed ibsen measurement result')
#         plt.plot(rasta_ptb[0], rasta_ptb[1]/max(rasta_ptb[1]), marker='o', linestyle='-', label = 'RASTA PTB measurement')
        legend = plt.legend(ncol = 2)
        if plot == 'y':
            plt.show()
        plt.close()
        
        array_write = np.transpose([xnew, ibsen_response])
        np.savetxt(fname = (os.path.join(output_directory, output_filename)), X = array_write, fmt = '%.5e', delimiter = '\t')
        ####################################################################################################################################################################



class Ibsen_Level1_Processor(object):
    def __init__(self):
        pass

    def ibsen_level1_processor(self, nonlinearity, response, dark_current, target, spectralon, input_directory, output_directory):
        '''
        implement use of winnowed darkcurrent
        return same values as read_ibsen or write to file (fileending .ibsenL1)
        
        nonlinearity_2 is for longer wavelengths
        '''
        lower_wl = 0 # gets passed straight on to the reader. Currently I see no need to limit the read wavelength in the level 1 processor.
        
        nonlinearity = np.genfromtxt(nonlinearity, delimiter = '\t')    
        nonlinearity = np.transpose(nonlinearity) #nonlinearity[0] = DN values; nonlinearity[1] = correction factors
        
        ibsen_response = np.genfromtxt(response)
        ibsen_response = np.transpose(ibsen_response)
        
        tar = reader.read_ibsen_data(input_directory, 0, target, '.asc') # read the target file
        
        number_columns = tar['number_columns']

        if dark_current != '':
            dark = reader.read_ibsen_data(input_directory, 0, dark_current, '.asc') # read the darkcurrent file
            dark_winnowed = evaluate.winnow_spectra(input_directory, dark_current, '.asc', lower_wl, std_plus = 2, std_minus = 2, std_r2 = 1.5)
            for i in range(2, number_columns):
                tar['data'][i] = tar['data'][i]-dark_winnowed['mean_good'] #subtracts the darkcurrent average from each individual target measurement
        else:
            print('No darkcurrent is subtracted!')
        for i in range(2, number_columns): #tar[1] contains number of columns of the target file

            for j in range(0, len(tar['data'][i])): #tar[0][i] contains one spectrum of the (usually 30) measurements in one file
                tar['data'][i][j] = tar['data'][i][j]/np.interp(tar['data'][i][j], nonlinearity[0], nonlinearity[1]) #nonlinearity correction for each element, tar[0][i][j] contains a single number (corresponding to a wavelength of the spectrum)
            if spectralon == 'y':
                spectralon_resampled = spectralon_function.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_40447-1-1.dat', tar['data'][i])
                tar['data'][i] = np.divide(tar['data'][i]*np.pi, spectralon_resampled['resampled_spectralon']) # multiplication with pi forgotten.... changed 13.09.2016
            tar['data'][i] = tar['data'][i]/tar['int_time'] # tar['int_time'] contains the integration time, this step normalizes to 1ms
            tar['data'][i] = np.multiply(tar['data'][i], np.interp(tar['data'][0], ibsen_response[0], ibsen_response[1])) # mutiplies with the inverse ibsen response, converts units from W/m^3.sr to mW/m^2.nm.sr correction factor is 10**-6 NOT

        tar_transpose = np.transpose(tar['data'])
        for i in range(0, len(tar['data'][0])):
            tar['data'][1][i] = np.mean(tar_transpose[i][3:number_columns]) # new mean
            tar['data'][2][i] = np.std(tar_transpose[i][3:number_columns]) # new std
            
        #process header, change lines in header according to raw -> level 1
        tar['header'][0] = '[Data calibrated] \nProcessed with: Ibsen_level1_processor Version 1.0 by Sebastian Riedel \nUsed dark current: ' + dark_current + ' with integration time ' + str(dark['comment']) + '\n \n'
        if spectralon == 'y':
            tar['header'][17] = '[DataCalibrated] [E_d] [mW/m^2.nm] [columns: wavelength [nm], mean, standard deviation, ' + str(number_columns-3) + 'x data] \n'
        else:        
            tar['header'][17] = '[DataCalibrated] [L_u] [mW/m^2.nm.sr] [columns: wavelength [nm], mean, standard deviation, ' + str(number_columns-3) + 'x data] \n'
        
        if os.path.isdir(output_directory) == False: # check if output directory exists
            os.makedirs(output_directory) # and create if not
            
        array_write = np.transpose(tar['data'])
        file = open(os.path.join(output_directory, target + '.ibsenL1'), 'w')
        file.writelines(["%s" % item  for item in tar['header']])
        for row in array_write:
            row.tofile(file, sep='\t',format="%.4f")
            file.write('\n')
            
            
        
    def ibsen_level1_processor_2step(self, nonlinearity, nonlinearity_2, transition_wl, response, dark_current, target, spectralon, input_directory, output_directory):
        '''
        implement use of winnowed darkcurrent
        return same values as read_ibsen or write to file (fileending .ibsenL1)
        
        nonlinearity_2 is for longer wavelengths
        '''
        lower_wl = 0 # gets passed straight on to the reader. Currently I see no need to limit the read wavelength in the level 1 processor.
        
        nonlinearity = np.genfromtxt(nonlinearity, delimiter = '\t')    
        nonlinearity = np.transpose(nonlinearity) #nonlinearity[0] = DN values; nonlinearity[1] = correction factors
        
        if nonlinearity_2 != '':
            nonlinearity_2 = np.genfromtxt(nonlinearity_2, delimiter = '\t')    
            nonlinearity = np.transpose(nonlinearity) #nonlinearity[0] = DN values; nonlinearity[1] = correction factors
        
        ibsen_response = np.genfromtxt(response)
        ibsen_response = np.transpose(ibsen_response)
        
        tar = reader.read_ibsen_data(input_directory, 0, target, '.asc') # read the target file
        
        transition_wl_real = min(tar['wavelength'], key=lambda x:abs(x-float(transition_wl))) #find closest WL to transition wavelength
        transition_wl_real_position = int(np.where(tar['wavelength']==transition_wl_real)[0]) # returns integer with position of transition wavelength
        number_columns = tar['number_columns']

        if dark_current != '':
            dark = reader.read_ibsen_data(input_directory, 0, dark_current, '.asc') # read the darkcurrent file
            dark_winnowed = evaluate.winnow_spectra(input_directory, dark_current, '.asc', lower_wl, std_plus = 2, std_minus = 2, std_r2 = 1.5)
            for i in range(2, number_columns):
                tar['data'][i] = tar['data'][i]-dark_winnowed['mean_good'] #subtracts the darkcurrent average from each individual target measurement
        else:
            print('No darkcurrent is subtracted!')
        for i in range(2, number_columns): #tar[1] contains number of columns of the target file
            tar_1 = []
            tar_2 = []
            for j in range(0, len(tar['data'][i])): #tar[0][i] contains one spectrum of the (usually 30) measurements in one file
                tar_1.append(tar['data'][i][j]/np.interp(tar['data'][i][j], nonlinearity[0], nonlinearity[1])) #nonlinearity correction for each element, tar[0][i][j] contains a single number (corresponding to a wavelength of the spectrum)
                if nonlinearity_2 != '':
                    tar_2.append(tar['data'][i][j]/np.interp(tar['data'][i][j], nonlinearity_2[0], nonlinearity_2[1]))
            if nonlinearity_2 != '':
#                 plt.plot(tar['wavelength'], tar_1)
#                 plt.plot(tar['wavelength'], tar_2)
                tar['data'][i] = tar_1[:transition_wl_real_position] + tar_2[transition_wl_real_position:] # combines the 2 target datasets processed with 2 different nonlinearity files
                plt.plot(tar['wavelength'], tar['data'][i])
                plt.show()
            else:
                tar['data'][i] = tar_1 # if there is only one nonlinearity...
            if spectralon == 'y':
                spectralon_resampled = spectralon_function.interpolate_spectralon(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Spectralon Charakterisierung', 'S1005_40447-1-1.dat', tar['data'][i])
                tar['data'][i] = np.divide(tar['data'][i]*np.pi, spectralon_resampled['resampled_spectralon']) # multiplication with pi forgotten.... changed 13.09.2016
            tar['data'][i] = tar['data'][i]/tar['int_time'] # tar['int_time'] contains the integration time, this step normalizes to 1ms
            tar['data'][i] = np.multiply(tar['data'][i], np.interp(tar['data'][0], ibsen_response[0], ibsen_response[1])) # mutiplies with the inverse ibsen response, converts units from W/m^3.sr to mW/m^2.nm.sr correction factor is 10**-6 NOT

        tar_transpose = np.transpose(tar['data'])
        for i in range(0, len(tar['data'][0])):
            tar['data'][1][i] = np.mean(tar_transpose[i][3:number_columns]) # new mean
            tar['data'][2][i] = np.std(tar_transpose[i][3:number_columns]) # new std
            
        #process header, change lines in header according to raw -> level 1
        tar['header'][0] = '[Data calibrated] \nProcessed with: Ibsen_level1_processor Version 1.0 by Sebastian Riedel \nUsed dark current: ' + dark_current + ' with integration time ' + str(dark['comment']) + '\n \n'
        if spectralon == 'y':
            tar['header'][17] = '[DataCalibrated] [E_d] [mW/m^2.nm] [columns: wavelength [nm], mean, standard deviation, ' + str(number_columns-3) + 'x data] \n'
        else:        
            tar['header'][17] = '[DataCalibrated] [L_u] [mW/m^2.nm.sr] [columns: wavelength [nm], mean, standard deviation, ' + str(number_columns-3) + 'x data] \n'
        
        if os.path.isdir(output_directory) == False: # check if output directory exists
            os.makedirs(output_directory) # and create if not
            
        array_write = np.transpose(tar['data'])
        file = open(os.path.join(output_directory, target + '.ibsenL1'), 'w')
        file.writelines(["%s" % item  for item in tar['header']])
        for row in array_write:
            row.tofile(file, sep='\t',format="%.4f")
            file.write('\n')



    