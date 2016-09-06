'''
Created on 23.07.2016

@author: ried_st
'''

import numpy as np
import os
import matplotlib.pyplot as plt
from Evaluation_Methods import Reader, spectralon_response, Ibsen_evaluate

reader = Reader.File_Reader()
jeti_directory = r'C:\Users\ried_st\OneDrive\Austausch\Messdaten\Kampagnen\Interkalibrationskampagne\Andreas Jeti'


for file in os.listdir(jeti_directory):
    if file.endswith('.dat'):
        filename, file_extension = os.path.splitext(file)
        jeti_data = reader.read_jeti(jeti_directory, filename + '.dat')
        fig = plt.figure(figsize=(18, 10))
        plt.plot(jeti_data['data'][0], jeti_data['data'][1])
        plt.xlabel('Wavelength [nm]', fontsize = 18)
        plt.ylabel('DN', fontsize = 18)
        fig.suptitle(filename)
        fig.savefig(os.path.join(jeti_directory, filename + '.png'))
        plt.close()