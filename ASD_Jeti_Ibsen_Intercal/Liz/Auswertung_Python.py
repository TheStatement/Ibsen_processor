# -*- coding: cp1252 -*-
import numpy as np
import struct
import pylab as plt
import os
import scipy as sp


from scipy.interpolate import splprep, splev


from matplotlib.pyplot import *
from matplotlib import rc

directory = r'C:\Users\ried_st\OneDrive\Austausch\Kampagnen\Interkalibrationskampagne\Atwood_Stechlinsee_31_05_2015'

def readbytes(pos, bytes, data_type,f):
    f.seek(pos)
    d=f.read(bytes)
    res=struct.unpack(data_type,d)[0]
    return(res)


def convertrawasd (filename): 
    filename = os.path.join(directory, filename)
    f = open(filename,"rb")
    dt = readbytes(186,1,"b",f)
    start_wavelength = readbytes(191,4,"f",f)
    wavelength_step = readbytes(195,4,"f",f)
    channels=readbytes(204,2,"h",f)
    it = readbytes(390,4,"L",f)
    drange = readbytes(418,2,"H",f)
    swir1gain = readbytes(436,2,"H",f)
    swir2gain = readbytes(438,2,"H",f)
    swir1offset = readbytes(440,2,"H",f)
    swir2offset = readbytes(442,2,"H",f)
    splice1 = readbytes(444,4,"f",f),
    splice2 = readbytes(448,4,"f",f)
    data = np.zeros(channels)
    matrix=np.zeros(shape=(channels,2))
    
    for i in range(channels):
        matrix[i,1] = float(readbytes(484+i*4,4,"f",f))
        matrix[i,0]= i+350
        
    return (matrix)




def readfolder(pfad,endung):
    Ausgabeliste=[]
    liste=os.listdir(pfad)              # liste mit filenamen aus Ordner "Pfad" einlesen
    for n in range(0,len(liste)):       # einträge mit passender Endung suchen
        if liste[n].count(endung) !=0:
            Ausgabeliste.append(liste[n])
    
    return(Ausgabeliste)


def MessdatenPlotten(Array,titel,YLabel,filename):

    #plt.figure()
    fig = plt.figure(figsize=(18, 10))
    Array = np.transpose(Array)
    plt.plot(Array[0],Array[1],label=filename)
    plt.title(titel)
    plt.xlabel("wavelength [nm]")    
    plt.ylabel(YLabel)
    plt.xlim([350,2500])
    plt.legend()                 #loc=4
    plt.grid()
    #fig.savefig(os.path.join(directory, filename + '.png'))
    plt.show()
    plt.close()



Array = convertrawasd('probe1_00000.asd')
print(Array)
np.savetxt(os.path.join(directory, '0001.dat'), Array, delimiter = ',')
MessdatenPlotten(Array,'probe1_00000','DN','probe1_00000')
#      
# for file in os.listdir(directory):
#     if file.endswith('.asd'):
#         filename, file_extension = os.path.splitext(file)
#         Array = convertrawasd(filename + '.asd')
#         MessdatenPlotten(Array,filename,'DN',filename)


# convertrawasd spuckt seltsame Daten aus. Auf jeden Fall keine Rohdaten, keine Ahnung was es sein soll, nicht zu gebrauchen.
