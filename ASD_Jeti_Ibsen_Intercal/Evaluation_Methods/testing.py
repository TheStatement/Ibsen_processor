'''
Created on 12.08.2016

@author: ried_st
'''
from Evaluation_Methods import Ibsen_evaluate, Reader, Ibsen_level1_processor
import matplotlib.pyplot as plt

evaluate = Ibsen_evaluate.Ibsen_Evaluation()
#test = evaluate.winnow_spectra(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kalibration\Ibsen\Radiometric Calibration\RASTA\test3', 'target000', '.asc', std_plus = 1, std_minus = 1, std_r2 = 1)
#print(test[0], test[1])

Reader = Reader.File_Reader()

# directory = r'C:\Users\ried_st\OneDrive\Austausch\Software\IControl 1.2\results\160823_Essling\StegKiosk\000'
# filename = 'reference000'
# file_extension = '.asc'
# test = Reader.read_ibsen_data(directory, filename, file_extension)
# 
# directory2 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\CoastMap 2016\T4\ST04'
# filename2 = 'reference000'
# test2 = Reader.read_ibsen_data(directory2, filename2, file_extension)
# 
# fig = plt.figure(figsize=(18, 10))
# plt.plot(test[0][0], test[0][1]/max(test[0][1]), label = 'heute')
# plt.plot(test2[0][0], test2[0][1]/max(test2[0][1]), label = 'Ostsee')
# legend = plt.legend(ncol = 1)
# plt.show()
# 
# plt.close()

# level 1 processing

level1  = Ibsen_level1_processor.Ibsen_Level1_Processor()
input_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje'
output_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level 1'


level1.ibsen_level1_processor('darkcurrent000', 'reference000', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'reference000', '', input_directory_1, output_directory_1)
#level1.ibsen_level1_processor('darkcurrent000', 'target000', '', input_directory_1, output_directory_1)

# data_normal = Reader.read_ibsen_data(directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\Alle zusammen_Level1', filename = 'target000_1', file_extension = '.ibsenL1')
# data_winnowed = Reader.read_ibsen_data(directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\Alle zusammen_Level1', filename = 'target000', file_extension = '.ibsenL1')

# 
# fig = plt.figure(figsize=(18, 10))
# plt.plot(data_normal[0][0], data_normal[0][1], label = 'normal')
# plt.plot(data_winnowed[0][0], data_winnowed[0][1], label = 'winnowed')
# legend = plt.legend(ncol = 1)
# plt.show()
#  
# plt.close()

# evaluate.plot_all(r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Ibsen\20160825_Data for aerosol retieval\Dach_DLR_Level1', '.ibsenL1')