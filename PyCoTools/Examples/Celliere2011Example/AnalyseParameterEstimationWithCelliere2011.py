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
available if you have run the runParameterEstimationWithKholodenko.py script
on your own machine.
'''

if os.path.isdir(C.PEData_dir):
    PEData_path=C.PEData_dir
elif os.path.isdir(C.PEData_dir) !=True:
    if os.path.isfile(C.PEData_file):
        PEData_path=C.PEData_file
else:
    raise PyCoTools.Errors.InputError('You need to run parameter estimations before trying to analyse them')

PEData=PyCoTools.PEAnalysis.ParsePEData(PEData_path,UsePickle='true',overwrite_pickle='false')

# Print the best parameters from your parameter estimations to console
print 'best estimated parameters:\n',PEData.data.iloc[0].sort_index()
#
#'''
#Visualize plot of likelihood Vs iteration
#'''
#PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(PEData_path,savefig='true')
#
'''
Insert the parameters and simulate a parameter estimation 
with current solution statistics as 'method' keyword, plotting the results
and saving to file (and remembering to turn off randomize_start_values)
'''
PyCoTools.pycopi.InsertParameters(C.celliere2011_model,parameter_path=PEData_path,index=0)
PE=PyCoTools.pycopi.ParameterEstimation(C.celliere2011_model,C.noisy_timecourse_report,
                                        method='CurrentSolutionStatistics',
                                        plot='true',
                                        savefig='true',
                                        randomize_start_values='false')
PE.set_up() ## setup
PE.run()    ## and run the current solution statistics parameter estimation
#
## plot box plots
PyCoTools.PEAnalysis.plotBoxplot(PEData_path,
                                 savefig='true')

## plot histograms
PyCoTools.PEAnalysis.plotHistogram(PEData_path,
                                   log10='true', ##plot on log10 scale
                                   truncate_model='percent',
                                   savefig='true')
## plot scatter graphs
PyCoTools.PEAnalysis.plotScatters(PEData_path,savefig='true',
                                  log10='true') 























