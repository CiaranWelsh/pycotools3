# -*- coding: utf-8 -*-
'''
 This file is part of PyCoTools.

 PyCoTools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 PyCoTools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with PyCoTools.  If not, see <http://www.gnu.org/licenses/>.


Author: 
    Ciaran Welsh
Date:
    12/03/2017 
'''
import PyCoTools
import os
import pandas
import numpy

import FilePaths

K=FilePaths.KholodenkoExample()

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

if os.path.isdir(K.PEData_dir):
    PEData_path=K.PEData_dir
elif os.path.isdir(K.PEData_dir) !=True:
    if os.path.isfile(K.PEData_file):
        PEData_path=K.PEData_file
else:
    raise PyCoTools.Errors.InputError('You need to run parameter estimations before trying to analyse them')

#PEData=PyCoTools.PEAnalysis.ParsePEData(PEData_path)
#
### Print the best parameters from your parameter estimations to console
#print 'best estimated parameters:\n',PEData.data.iloc[0].sort_index()
#
#'''
#Visualize plot of likelihood Vs iteration
#'''
#PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(PEData_path,savefig='true')
##
#'''
#Insert the parameters and simulate a parameter estimation 
#with current solution statistics as 'method' keyword, plotting the results
#and saving to file (and remembering to turn off randomize_start_values)
#'''
#PyCoTools.pycopi.InsertParameters(K.kholodenko_model,parameter_path=PEData_path,index=0)
#PE=PyCoTools.pycopi.ParameterEstimation(K.kholodenko_model,K.noisy_timecourse_report,
#                                        method='CurrentSolutionStatistics',
#                                        plot='true',
#                                        savefig='true',
#                                        randomize_start_values='false')
#PE.set_up() ## setup
#PE.run()    ## and run the current solution statistics parameter estimation
#
### plot box plots
#PyCoTools.PEAnalysis.plotBoxplot(PEData_path,
#                                 savefig='true')
#
### plot histograms
#PyCoTools.PEAnalysis.plotHistogram(PEData_path,
#                                   log10='true', ##plot on log10 scale
#                                   truncate_model='percent',
#                                   savefig='true')
# plot scatter graphs
PyCoTools.PEAnalysis.plotScatters(PEData_path,savefig='true',
                                  log10='true') 























