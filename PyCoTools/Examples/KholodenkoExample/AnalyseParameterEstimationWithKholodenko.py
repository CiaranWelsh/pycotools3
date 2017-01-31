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
goldbetter_model=os.path.join(current_directory,copasi_file)
report=os.path.join(current_directory,'TimeCourseOutput.txt')
noisy_report=os.path.join(current_directory,'NoisyTimeCourseOutput.txt')
#PEData_report=os.path.join(current_directory,'PEData.txt')
PEData_report='D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Examples\KholodenkoExample\PEResults'

'''
Frist parse the PE data so you can print out the values 
of the best estimate
'''
PEData=PyCoTools.PEAnalysis.ParsePEData(PEData_report)

print 'best estimated parameters:\n',PEData.data.iloc[0].sort_index()

'''
Visualize plot of likelihood Vs iteration
'''
PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(PEData_report,SaveFig='true')

'''
Insert the parameters and simulate a parameter estimation 
with current solution statistics as method, plotting the results
and saving to file (and remembering to turn off RandomizeStartValues)
'''
PyCoTools.pycopi.InsertParameters(goldbetter_model,ParameterPath=PEData_report,Index=0)

PE=PyCoTools.pycopi.ParameterEstimation(goldbetter_model,noisy_report,
                                        Method='CurrentSolutionStatistics',
                                        Plot='true',
                                        SaveFig='true',
                                        RandomizeStartValues='false')
PE.set_up() #setup
PE.run()    #and run the current solution statistics parameter estimation

PyCoTools.PEAnalysis.PlotBoxplot(PEData_report,
                                 NumPerPlot=8,#number of boxes per figure canvas
                                 SaveFig='true')

PyCoTools.PEAnalysis.PlotHistogram(PEData_report,
                                   Log10='true', ##plot on log10 scale
                                   TruncateMode='percent',
                                   SaveFig='true')
##
PyCoTools.PEAnalysis.PlotScatters(PEData_report,SaveFig='true',
                                  Log10='true') 























