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
    if 'RSS' in parameters.keys():
        del parameters['RSS']
    for i in parameters:
        print i,':\t',parameters[i]
    PyCoTools.pycopi.InsertParameters(copasi_file,ParameterDict=parameters)
    
    PE=PyCoTools.pycopi.ParameterEstimation(copasi_file,K.noisy_timecourse_report,
                                         Method='HookeJeeves',
                                         IterationLimit=1000,
                                         Tolerance=1e-6,
                                         RandomizeStartValues='false',
                                         Plot='true',
                                         SaveFig='true',
                                         UseTemplateStartValues='false',
                                         )

        
    PE.set_up()
    ## Run via scan task because this gives only best values in function
    ## evaluations, rather than the periodic function evaluations as well
    PyCoTools.pycopi.Scan(copasi_file,ScanType='repeat',Run='true',
                          NumberOfSteps=1,
                          ReportName=report,
                          ReportType='parameter_estimation')


for i in range(int(data.shape[0]*0.1)):
    print 'running index {} with starting RSS of {}'.format(i,data.iloc[i]['RSS'])
    if os.path.isdir(K.local_PEData_dir)!=True:
        os.mkdir(K.local_PEData_dir)
    report=os.path.join(K.local_PEData_dir,'{}.txt'.format(i))
    print runHJ(K.kholodenko_model,data.iloc[i].to_dict(),report)
































