'''
Created on 14.04.2016

@author: ried_st
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append(r'/local/home/ried_st/git/Ibsen_processor/ASD_Jeti_Ibsen_Intercal')


from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate, Ibsen_level1_processor

reader = Reader.File_Reader()
spectralon = spectralon_response.Interpolate_Spectralon()
ibsen_evaluate = Ibsen_evaluate.Ibsen_Evaluation()
ibsen_nonlinerity = Ibsen_level1_processor.Evaluation_Calibration()
ibsen_response = Ibsen_level1_processor.Evaluation_Calibration()

# passende Spektren auswaehlen
# nonlinearity Korrektur drueber laufen lassen
# in ein File schreiben
# Gauss filter drueber
# mit PTB Kurve verwursten
# abspeichern





# input values and parameters
input_directory = r'/local/home/ried_st/OneDrive/Austausch/Messdaten/Kalibration/20160525_Radiometric Calibration_Ibsen/RASTA/test'
output_directory = r'/local/home/ried_st/OneDrive/Austausch/Messdaten/Kalibration/20160525_Radiometric Calibration_Ibsen/RASTA/results'
output_filename = 'ibsen_nonlinerity_total.asc'
number_files = 22
sigma_fine = 15 # of Gaussian filter
step_size_fine = 2 # of Gaussian filter
sigma_coarse = 1000
step_size_coarse = 500
DN_transition_fine_coarse = 300
lower_wl = 0
plot = 'y'
two_step = 'y'
# End input

ibsen_nonlinerity.ibsen_nonlinearity_evaluation(input_directory, number_files, lower_wl, output_directory, output_filename, sigma_fine, step_size_fine, sigma_coarse, step_size_coarse, DN_transition_fine_coarse, plot, two_step)



# input values and parameters for response
input_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\20160525_Radiometric Calibration_Ibsen\RASTA\test2'
output_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\20160525_Radiometric Calibration_Ibsen\RASTA\results'
output_filename = 'ibsen_response.asc'
nonlinearity_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\20160525_Radiometric Calibration_Ibsen\RASTA\results\ibsen_nonlinerity_total.asc'
rasta_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\PTB_Kalibrierkampagne_2016\2016-01_RASTA_1m_rawdata.dat'
sigma = 0.3
step_size = 0.2
min_int_time = 50
plot = ''
# End input

# ibsen_response.get_response(input_directory, output_directory, output_filename, nonlinearity_directory, rasta_directory, sigma, step_size, min_int_time, plot)

