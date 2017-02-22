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

# level 1 processing Interkalibrationskampagne
# Mittwoch
level1  = Ibsen_level1_processor.Ibsen_Level1_Processor()
input_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser'
output_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser_Level1'

level1.ibsen_level1_processor('darkcurrent000', 'reference000', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'target000', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'target001', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'target002', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'target003', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'reference001', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'target004', '', input_directory_1, output_directory_1)

evaluate.plot_all(output_directory_1, '.ibsenL1', '')


input_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2'
output_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Flachwasser 2_Level1'

level1.ibsen_level1_processor('darkcurrent000', 'reference000', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'reference001', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'reference002', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'reference003', 'y', input_directory_1, output_directory_1)

level1.ibsen_level1_processor('darkcurrent000', 'target000', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'target001', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'target002', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'target003', '', input_directory_1, output_directory_1)

evaluate.plot_all(output_directory_1, '.ibsenL1', '')


input_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje'
output_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Mittwoch\Stechlinsee\Tiefwasser Boje_Level1'

level1.ibsen_level1_processor('darkcurrent000', 'reference000', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'reference001', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'reference002', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'reference003', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'reference004', 'y', input_directory_1, output_directory_1)

level1.ibsen_level1_processor('darkcurrent000', 'target000', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'target001', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'target002', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'target003', '', input_directory_1, output_directory_1)

evaluate.plot_all(output_directory_1, '.ibsenL1', '')

# Dienstag
input_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\ST01'
output_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\ST01_Level1'

level1.ibsen_level1_processor('darkcurrent001', 'reference000', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'reference001', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'reference002', 'y', input_directory_1, output_directory_1)

level1.ibsen_level1_processor('darkcurrent002', 'target000', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent002', 'target001', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent002', 'target002', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent002', 'target003', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent002', 'target004', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent002', 'target005', '', input_directory_1, output_directory_1)

evaluate.plot_all(output_directory_1, '.ibsenL1', '')


input_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\ST04'
output_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\ST04_Level1'

level1.ibsen_level1_processor('darkcurrent000', 'reference000', 'y', input_directory_1, output_directory_1)

level1.ibsen_level1_processor('darkcurrent000', 'target000', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'target001', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'target002', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'target003', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent000', 'target004', '', input_directory_1, output_directory_1)

evaluate.plot_all(output_directory_1, '.ibsenL1', '')



input_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\Alle zusammen'
output_directory_1 = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Ibsen Daten\Messworkshop 2016_Stechlinsee Dienstag\Boje Tiefste Stelle\Alle zusammen_Level1'

level1.ibsen_level1_processor('darkcurrent000', 'reference000', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent001', 'reference001', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent002', 'reference002', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent003', 'reference003', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent004', 'reference004', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent005', 'reference005', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent006', 'reference006', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent007', 'reference007', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent008', 'reference008', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent009', 'reference009', 'y', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent010', 'reference010', 'y', input_directory_1, output_directory_1)

level1.ibsen_level1_processor('darkcurrent001', 'target000', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent002', 'target001', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent003', 'target002', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent004', 'target003', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent005', 'target004', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent006', 'target005', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent008', 'target006', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent008', 'target007', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent009', 'target008', '', input_directory_1, output_directory_1)
level1.ibsen_level1_processor('darkcurrent010', 'target009', '', input_directory_1, output_directory_1)

evaluate.plot_all(output_directory_1, '.ibsenL1', '')