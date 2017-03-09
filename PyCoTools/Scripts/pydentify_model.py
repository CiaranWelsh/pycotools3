# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 20:23:21 2017

@author: b3053674
"""

import PyCoTools as P
import os
import argparse

#==============================================================================
parser=argparse.ArgumentParser()
parser.add_argument('model',help='copasi file for running through the pydentify workflow' )
args=parser.parse_args()
#==============================================================================

'''
Download models from BioModels in another Script. 

Import Models into copasi in another

iterate over workflow for each model

Workflow:

    1) Run a time course
    2) add noise to time course data
    3) Run global parameter estimation with noisy data
    4) Run local chaser parameter estimation
    5) Run profile likelihood
    6) Plot profile likelihood
    
Collect counts to search for errors. 
'''





plot='true'
savefig='true'
model=r"D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PydentifyingBiomodelFoldersFromPyCoTools\PydentifyingBiomodels\BIOMD0000000001\Edelstein1996 - EPSP ACh event.cps"
directory,fle=os.path.split(model)
TCReportName=os.path.join(directory,'timecourse_report.txt')
TC=P.pycopi.TimeCourse(model,End=1000,StepSize=20,Intervals=50,Plot=plot,SaveFig=savefig,
                       ReportName=TCReportName)
#%%
noisy_data= P.Misc.add_noise(TCReportName)
noisy_datafile=os.path.join(directory,'noisy_data.txt')
noisy_data.to_csv(noisy_datafile,sep='\t')
#%%
PEResults_file=os.path.join(directory,'PEResults.txt')
## use hook and jeeves and do not randomize start parameters. That way
## we shold get nice fits with little effort
PE=P.pycopi.ParameterEstimation(model,noisy_datafile,Method='HookeJeeves',
                                RandomizeStartValues='false')
PE.write_item_template()
PE.set_up()
#%%
S=P.pycopi.Scan(model,ScanType='repeat',NumberOfSteps=1,
                ReportName=PEResults_file,ReportType='parameter_estimation',Run='true')
                
                
#%%
P.pycopi.InsertParameters(model,ParameterPath=PEResults_file)

#%%
PE=P.pycopi.ParameterEstimation(model,noisy_datafile,Method='CurrentSolutionStatistics',
                                RandomizeStartValues='false',SaveFig=savefig,Plot=plot)
PE.set_up()
PE.run()

#%%
P.pydentify2.ProfileLikelihood(model,ParameterPath=PEResults_file,
                               NumberOfSteps=10,UpperBoundMultiplier=1000,
                               LowerBoundMultiplier=100,Run='slow',Index=0)


#%%
P.pydentify2.Plot(model,ParameterPath=PEResults_file,Index=0,SaveFig=savefig)



