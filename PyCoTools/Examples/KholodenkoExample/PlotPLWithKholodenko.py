# -*- coding: utf-8 -*-

import PyCoTools
import os
import pandas
import numpy


import sys
if sys.platform=='win32':
    current_directory='D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Examples\KholodenkoExample'
else:
    current_directory=r'/sharedlustre/users/b3053674/2017/Jan'
copasi_file=r'Kholodenko.cps'
Kholodenko_model=os.path.join(current_directory,copasi_file)
report=os.path.join(current_directory,'TimeCourseOutput.txt')
noisy_report=os.path.join(current_directory,'NoisyTimeCourseOutput.txt')

PEData_report=os.path.join(current_directory,'LocalPEData.txt')


PyCoTools.pydentify2.Plot(Kholodenko_model, #full path to the model
                           ParameterPath=PEData_report, #full path to the PEData
                           Index=-1,
                           RSS=108.083)
#                           Mode='one',
#                           PlotIndex=0,
#                           PlotParameter='(transcription of PER).KI')#, #index of PE set for plotting. (best is 0)
                           






































