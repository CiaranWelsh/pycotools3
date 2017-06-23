# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 17:23:46 2017

@author: b3053674
"""

import PyCoTools
import os
import FilePaths

C=FilePaths.Celliere2011Example()

if os.path.isdir(C.local_PEData_dir):
    local_PEData_dir=C.local_PEData_dir
elif os.path.isdir(C.local_PEData_dir) !=True:
    if os.path.isfile(C.local_PEData_dir):
        local_PEData_dir=C.local_PEData_dir
else:
    raise PyCoTools.Errors.InputError('You need to run parameter estimations before trying to analyse them')

print local_PEData_dir
'''
Analysis of PEData produced in the secondary parameter estimations
are analyzed in the same way as the global data. 
'''
#PEData=PyCoTools.PEAnalysis.ParsePEData(local_PEData_dir)
### Print the best parameters from your parameter estimations to console
#print 'best estimated parameters:\n',PEData.data.iloc[0].sort_index()




#PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(local_PEData_dir,savefig='true',log10='true')

#PyCoTools.pycopi.InsertParameters(C.celliere2011_model,parameter_path=local_PEData_dir,index=0)
#
#PE=PyCoTools.pycopi.ParameterEstimation(C.celliere2011_model,C.noisy_timecourse_report,
#                                        method='CurrentSolutionStatistics',
#                                        plot='true',
#                                        savefig='true',
#                                        randomize_start_values='false')
#PE.set_up() ## setup
#PE.run()    ## and run the current solution statistics parameter estimation
#
#PyCoTools.PEAnalysis.EvaluateOptimizationPerformance(local_PEData_dir,savefig='true')
#
#PyCoTools.PEAnalysis.plotBoxplot(local_PEData_dir,savefig='true')
#
#PyCoTools.PEAnalysis.plotHistogram(local_PEData_dir,log10='true',
#                                   bins=10,savefig='true')
#PyCoTools.PEAnalysis.plotScatters(C.local_PEData_dir,log10='true',
#                                  savefig='true')


f=r"D:\MPhil\Python\My_Python_Modules\modelling_Tools\PyCoTools\PyCoTools\Examples\Celliere2011Example\Celliere2011_temp_TimeCourse.txt"
print PyCoTools.PEAnalysis.PlotPEData(C.celliere2011_model,C.noisy_timecourse_report,f)












