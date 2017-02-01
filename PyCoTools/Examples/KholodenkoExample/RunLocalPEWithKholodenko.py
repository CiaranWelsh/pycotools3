# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 15:19:52 2017

@author: b3053674
"""

import PyCoTools
import os
import FilePaths

K=FilePaths.KholodenkoExample()

if os.path.isdir(K.PEData_dir):
    PEData_path=K.PEData_dir
elif os.path.isdir(K.PEData_dir) !=True:
    if os.path.isfile(K.PEData_file):
        PEData_path=K.PEData_file
        
        
data= PyCoTools.PEAnalysis.ParsePEData(PEData_path).data








def runHJ(copasi_file,parameters,report_name):
    '''
    Take parameters from global parameter estimation and perform local parameter
    estimation around these parameters.
    
    Need to instantiate ParameterEstimation class before inserting parameters
    '''
    PE=PyCoTools.pycopi.ParameterEstimation(copasi_file,K.noisy_timecourse_report,
                                         ReportName=report_name,
                                         Method='HookeJeeves',
                                         IterationLimit=1000,
                                         Tolerance=1e-10,
                                         RandomizeStartValues='false',
                                         Plot='true',
                                         SaveFig='true',
                                         )
    if 'RSS' in parameters.keys():
        del parameters['RSS']
    PyCoTools.pycopi.InsertParameters(copasi_file,ParameterDict=parameters)
    for i in parameters:
        print i,':\t',parameters[i]
        
    PE.set_up()
#    PE.run()
    
report=K.local_PEData[:-4]+'0.txt'
    
print runHJ(K.kholodenko_model,data.iloc[0].to_dict(),report)

































