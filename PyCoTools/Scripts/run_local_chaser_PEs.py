# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 15:19:52 2017

@author: b3053674
"""

import PyCoTools
import os
import argparse


##==============================================================================
parser=argparse.ArgumentParser(description='Run  local (HookJeeves) PE starting at output from global')
parser.add_argument('model',help='model to chase')
parser.add_argument('experimental_data',help='data to fit')
parser.add_argument('data_dir',help='path to parameter estimation data file')
parser.add_argument('-o', help='output data directory name',default=None)
parser.add_argument('-p',help='float between 0 and 1. Proportion of runs to chase with local',default=0.1,type=float)
args=parser.parse_args()
##==============================================================================



def runHJ(copasi_file,experimental_data,parameters,report_name):
    '''
    copasi_file:
        file to run hook and jeeves from 
    parameters:
        dictionary of parameters. Keys must match model names, values are input parameters
    report_name:
        name of the report to output PE data.
    
    Take parameters from global parameter estimation and perform local parameter
    estimation around these parameters.
    
    Need to instantiate ParameterEstimation class before inserting parameters
    '''
    if 'RSS' in parameters.keys():
        del parameters['RSS']
    for i in parameters:
        print i,':\t',parameters[i]
    PyCoTools.pycopi.InsertParameters(copasi_file,ParameterDict=parameters)
    
    PE=PyCoTools.pycopi.ParameterEstimation(copasi_file,experimental_data,
                                         Method='HookeJeeves',
                                         IterationLimit=20000,
                                         Tolerance=1e-30,
                                         RandomizeStartValues='false',
                                         Plot='true',
                                         SaveFig='true',
                                         UseTemplateStartValues='false',
                                         )

        
    PE.set_up()
    ## Run via scan task because this gives only best values in function
    ## evaluations, rather than the periodic function evaluations as well
    print '\n\n'
    print report_name
    print '\n'
    PyCoTools.pycopi.Scan(copasi_file,ScanType='repeat',
                          NumberOfSteps=1,
                          ReportName=report,
                          ReportType='parameter_estimation',Run='true')

#data.shape[0]*0.01)
if __name__=='__main__':
    os.chdir(os.path.dirname(args.model))
    
    if args.o==None:
        args.o=os.path.join(os.path.dirname(args.model),'ChaserParameterEstimations')
    
    data= PyCoTools.PEAnalysis.ParsePEData(args.data_dir).data
    '''
    Run hook and jeeves from the top 1 percent
    best estimated parameter from the genetic algorithm
    Run on windows machine
    '''
    if args.p>1 or args.p<0:
        raise Exception('args.p should be between 0 and 1')
    for i in range(int(data.shape[0]*args.p)):
        print 'running index {} with starting RSS of {}'.format(i,data.iloc[i]['RSS'])
        if os.path.isdir(args.o)!=True:
            os.mkdir(args.o)
        report=os.path.join(args.o,'{}.txt'.format(i))
        print runHJ(args.model,args.experimental_data,data.iloc[i].to_dict(),report)
        











