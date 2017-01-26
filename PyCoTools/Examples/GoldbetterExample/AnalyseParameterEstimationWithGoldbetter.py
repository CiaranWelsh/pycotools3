# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 21:59:01 2017

@author: b3053674
"""
import PyCoTools
import os
import pandas
import numpy


current_directory='D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Examples\GoldbetterExample'
copasi_file=r'Goldbeter1995_CircClock.cps'
goldbetter_model=os.path.join(current_directory,copasi_file)
report=os.path.join(current_directory,'TimeCourseOutput.txt')
noisy_report=os.path.join(current_directory,'NoisyTimeCourseOutput.txt')

PEData_report=os.path.join(current_directory,'PEData.txt')

#PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(PEData_report)


P= PyCoTools.PEAnalysis.ParsePEData(PEData_report)
data=P.read_data()
data=P.rename_RSS(data)
data=P.sort_data(data)
data=P.filter_constants(data)
#print data
#k=[]
#for i in data.keys():
#    print i
#    k.append(PyCoTools.Misc.RemoveNonAscii(i).filter)
#print k
#print P.prune_headers()
#print data
























