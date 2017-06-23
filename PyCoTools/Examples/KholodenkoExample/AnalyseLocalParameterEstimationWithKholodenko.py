# -*- coding: utf-8 -*-
"""
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

PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(local_PEData_dir,
                                                     savefig='true',
                                                     log10='true')
#                                                     truncate_model='below_x',x=2.062)

PyCoTools.pycopi.InsertParameters(K.kholodenko_model,parameter_path=local_PEData_dir,index=0)

PE=PyCoTools.pycopi.ParameterEstimation(K.kholodenko_model,K.noisy_timecourse_report,
                                        method='CurrentSolutionStatistics',
                                        plot='true',
                                        savefig='true',
                                        randomize_start_values='false')
PE.set_up() ## setup
PE.run()    ## and run the current solution statistics parameter estimation

PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(local_PEData_dir,savefig='true')

PyCoTools.PEAnalysis.plotBoxplot(local_PEData_dir,savefig='true')

PyCoTools.PEAnalysis.plotHistogram(local_PEData_dir,log10='true',
                                   bins=10,savefig='true')
PyCoTools.PEAnalysis.plotScatters(K.local_PEData_dir,log10='true',
                                  savefig='true')
















