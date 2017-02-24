# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:40:20 2017

@author: b3053674
"""
from shutil import copy
import PyCoTools
import os
import argparse
##==============================================================================
des=''' Setup n parameter estimations on a single file using 
ParameterEstimation and Scan tasks then copy the file m times and 
process each model through CopasiSE simultaneously'''
parser=argparse.ArgumentParser(description=des)
parser.add_argument('Model',help='model to perform parameter estimation on')
parser.add_argument('ConfigFile',help='Pre-configured PyCoTools parameter estimation configuration file')
parser.add_argument('Data',nargs='+',help='data to use in parameter estimation. Accepts multiple file paths')
parser.add_argument('--Method',help='Method of parameter estimation',default='GeneticAlgorithm')
parser.add_argument('--RandomizeStartValues',help='Start parameter estimation from random initial values',default='true')
parser.add_argument('-n',help='Number of parameter estimations for model copy to perform',default=3,type=int)
parser.add_argument('-m',help='Number of times to copy the model. >6 will probably cause problems.',default=4,type=int)

## arguments to control optimization specific parameterswith defaults
parser.add_argument('--NumberOfGenerations',help='Method specific parameter',default=200,type=int)
parser.add_argument('--PopulationSize',help='Method specific parameter',default=50,type=int)
parser.add_argument('--RandomNumberGenerator',help='Method specific parameter',default=1,type=int)
parser.add_argument('--Seed',help='Method specific parameter',default=0,type=int)
parser.add_argument('--Pf',help='Method specific parameter',default=0.475,type=float)
parser.add_argument('--IterationLimit',help='Method specific parameter',default=50,type=int)
parser.add_argument('--Tolerance',help='Method specific parameter',default=0.00001,type=float)
parser.add_argument('--Rho',help='Method specific parameter',default=0.2,type=float)
parser.add_argument('--Scale',help='Method specific parameter',default=10,type=int)
parser.add_argument('--SwarmSize',help='Method specific parameter',default=50,type=int)
parser.add_argument('--StdDeviation',help='Method specific parameter',default=0.000001,type=float)
parser.add_argument('--NumberOfIterations',help='Method specific parameter',default=100000,type=int)
parser.add_argument('--StartTemperature',help='Method specific parameter',default=1,type=int)
parser.add_argument('--CoolingFactor',help='Method specific parameter',default=0.85,type=float)
args=parser.parse_args()
##==============================================================================


                      
                      

def copy_copasi(copasi_file,m):
    '''
    run a copasi file m times on the same computer 
    '''
    sub_copasi_files_dct={}
    copasi_path,copasi_filename=os.path.split(copasi_file)
    for i in range(m):
        new_cps=os.path.join(copasi_path,copasi_filename[:-4]+'{}.cps'.format(str(i)))
        copy(copasi_file,new_cps)
        sub_copasi_files_dct[i]= new_cps
    return sub_copasi_files_dct

def enumerate_PE_output(output_filename,m):
    '''
    make some more filenames for our analysis
    '''
    dct={}
    dire,fle=os.path.split(output_filename)
    output_dir=os.path.join(dire,'MultiplePEResults')
    if os.path.isdir(output_dir)!=True:
        os.mkdir(output_dir)
    for i in range(m):
        new_file=os.path.join(output_dir,fle[:-4]+'{}.txt'.format(str(i)))
        dct[i]=new_file
    return dct

if __name__=='__main__':
    copasi_files=copy_copasi(args.Model,args.m)
    result_files=enumerate_PE_output(args.Model,args.m)

    # general call to ParameterEstimation
    PE= PyCoTools.pycopi.ParameterEstimation(args.Model,
                                               args.Data, 
                                               Method=args.Method, #change to genetic algorithm (why not?)
                                               Plot='false', #don't want to plot this time
                                               SaveFig='false',
                                               RandomizeStartValues=args.RandomizeStartValues,
                                               
                                               ConfigFilename=args.ConfigFile,
                                               NumberOfGenerations=args.NumberOfGenerations,
                                               PopulationSize=args.PopulationSize,
                                               RandomNumberGenerator=args.RandomNumberGenerator,
                                               Seed=args.Seed,
                                               Pf=args.Pf,
                                               IterationLimit=args.IterationLimit,
                                               Tolerance=args.Tolerance,
                                               Rho=args.Rho,
                                               Scale=args.Scale,
                                               SwarmSize=args.SwarmSize,
                                               StdDeviation=args.StdDeviation,
                                               NumberOfIterations=args.NumberOfIterations,
                                               StartTemperature=args.StartTemperature,
                                               CoolingFactor=args.CoolingFactor,
                                               )
    PE.set_up()
    for i in range(args.m):
        '''
        Set up n repeat items with NumberOfSteps repeats of parameter estimation
        Set run to false as we want to use the multiprocess mode of the Run class
        to process all m files at once in CopasiSE
        '''
        PyCoTools.pycopi.Scan(copasi_files[i],
                              ScanType='repeat', #set up repeat item under scan. 
                              NumberOfSteps=args.n, #Run the parameter estimation task 3 times
                              SubTask='parameter_estimation', #this is the default, but included here for demonstration anyway
                              ReportType='parameter_estimation', ## report automatically set up within copasi. 
                              ReportName=result_files[i],
                              Run='false') #run the scan task automatically in the background
    for i in copasi_files.values():
        PyCoTools.pycopi.Run(i,Mode='multiprocess',Task='scan')
    
                                    

    
    
    
    
    
    
    
    
    
    
    
