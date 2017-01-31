# -*- coding: utf-8 -*-

import PyCoTools
import os
import pandas
import numpy
import sys

import sys
if sys.platform=='win32':
    current_directory='D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Examples\KholodenkoExample'
    run_mode='slow'
else:
    current_directory=r'/sharedlustre/users/b3053674/2017/Jan/2'
    run_mode='SGE'
copasi_file=r'Kholodenko.cps'
kholodenko_model=os.path.join(current_directory,copasi_file)
report=os.path.join(current_directory,'TimeCourseOutput.txt')
noisy_report=os.path.join(current_directory,'NoisyTimeCourseOutput.txt')
PEData_dir=os.path.join(current_directory,'PEResults')
local_PEData=os.path.join(current_directory,'LocalPEData.txt')


'''
Global parameter estimation algorithms tend to locate good neighbourhoods
but fail when honing in on exact minima. Local methods however, if started 
in a good location are good at finding the minima. Therefore
before conducting profile likelihoods its a good idea to run a 
local optimizer on a parameter set to see if it will hone in on 
some parameter set. This procedure is conducted here using 
HookJeeves before running the profile likelihoods. 


'''
PyCoTools.pycopi.InsertParameters(kholodenko_model,ParameterPath=PEData_dir,Index=0)
PE=PyCoTools.pycopi.ParameterEstimation(kholodenko_model,noisy_report,Method='HookeJeeves',
                                        IterationLimit=500,Tolerance=1e-10, #stringent HookJeeves parameters
                                        ReportName=local_PEData, #write new PEData 
                                        RandomizeStartValues='false',
                                        )
PE.set_up()
PE.run()

PyCoTools.pydentify2.ProfileLikelihood(kholodenko_model, #full path to the model
                                       ParameterPath=local_PEData, #full path to the PEData
                                       Index=0, #index of PE set for profiling. (best is 0)
                                       NumberOfSteps=5, #resolution of profile likelihood 
                                       Run=run_mode,#Run method, 
                                       
                                       ##specify multipliers for scan boundaries\
                                       ##i.e. if estimated parameter was 0.1, \
                                       ##Boundaries with the present settings would be \
                                       ##between 0.1/1000 and 0.1*1000 = 0.0001 and 100\
                                       UpperBoundMultiplier=1000, 
                                       LowerBoundMultiplier=1000)  
#





































