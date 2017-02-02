# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 17:23:46 2017

@author: b3053674
"""

import PyCoTools
import os
import FilePaths

K=FilePaths.KholodenkoExample()

if os.path.isdir(K.local_PEData_dir):
    local_PEData_dir=K.local_PEData_dir
elif os.path.isdir(K.local_PEData_dir) !=True:
    if os.path.isfile(K.local_PEData_dir):
        local_PEData_dir=K.local_PEData_dir
else:
    raise PyCoTools.Errors.InputError('You need to run parameter estimations before trying to analyse them')


'''
Analysis of PEData produced in the secondary parameter estimations
are analyzed in the same way as the global data. 
'''
PEData=PyCoTools.PEAnalysis.ParsePEData(local_PEData_dir)
## Print the best parameters from your parameter estimations to console
print 'best estimated parameters:\n',PEData.data.iloc[0].sort_index()

PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(local_PEData_dir,SaveFig='true',Log10='true')

#PyCoTools.pycopi.InsertParameters(K.kholodenko_model,ParameterPath=local_PEData_dir,Index=0)
#
#PE=PyCoTools.pycopi.ParameterEstimation(K.kholodenko_model,K.noisy_timecourse_report,
#                                        Method='CurrentSolutionStatistics',
#                                        Plot='true',
#                                        SaveFig='true',
#                                        RandomizeStartValues='false')
#PE.set_up() ## setup
#PE.run()    ## and run the current solution statistics parameter estimation
#
#PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(local_PEData_dir,SaveFig='true')
#
#PyCoTools.PEAnalysis.PlotBoxplot(local_PEData_dir,SaveFig='true')
#
#PyCoTools.PEAnalysis.PlotHistogram(local_PEData_dir,Log10='true',
#                                   Bins=10,SaveFig='true')
#PyCoTools.PEAnalysis.PlotScatters(K.local_PEData_dir,Log10='true',
#                                  SaveFig='true')
#















