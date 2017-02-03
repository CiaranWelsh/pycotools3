# -*- coding: utf-8 -*-

import PyCoTools
import os
import pandas
import numpy

import FilePaths

C=FilePaths.Celliere2011Example()

'''
Frist parse the PE data so you can print out the values 
of the best estimate. 

If this was run on a cluster than the data should be placed 
within a folder defined within the FilePaths.KholodenkoExample.PEData_dir 
attribute. This is used when available but if not will fall back 
on the data contained in FilePaths.KholodenkoExample.PEData_file which should be 
available if you have run the RunParameterEstimationWithKholodenko.py script
on your own machine.
'''

if os.path.isdir(C.PEData_dir):
    PEData_path=C.PEData_dir
elif os.path.isdir(C.PEData_dir) !=True:
    if os.path.isfile(C.PEData_file):
        PEData_path=C.PEData_file
else:
    raise PyCoTools.Errors.InputError('You need to run parameter estimations before trying to analyse them')

PEData=PyCoTools.PEAnalysis.ParsePEData(PEData_path,UsePickle='true',OverwritePickle='false')

# Print the best parameters from your parameter estimations to console
print 'best estimated parameters:\n',PEData.data.iloc[0].sort_index()
#
#'''
#Visualize plot of likelihood Vs iteration
#'''
#PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(PEData_path,SaveFig='true')
#
'''
Insert the parameters and simulate a parameter estimation 
with current solution statistics as 'Method' keyword, plotting the results
and saving to file (and remembering to turn off RandomizeStartValues)
'''
PyCoTools.pycopi.InsertParameters(C.celliere2011_model,ParameterPath=PEData_path,Index=0)
PE=PyCoTools.pycopi.ParameterEstimation(C.celliere2011_model,C.noisy_timecourse_report,
                                        Method='CurrentSolutionStatistics',
                                        Plot='true',
                                        SaveFig='true',
                                        RandomizeStartValues='false')
PE.set_up() ## setup
PE.run()    ## and run the current solution statistics parameter estimation
#
## Plot box plots
PyCoTools.PEAnalysis.PlotBoxplot(PEData_path,
                                 SaveFig='true')

## Plot histograms
PyCoTools.PEAnalysis.PlotHistogram(PEData_path,
                                   Log10='true', ##plot on log10 scale
                                   TruncateMode='percent',
                                   SaveFig='true')
## Plot scatter graphs
PyCoTools.PEAnalysis.PlotScatters(PEData_path,SaveFig='true',
                                  Log10='true') 























