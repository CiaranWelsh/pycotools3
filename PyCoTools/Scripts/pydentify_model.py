# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 20:23:21 2017

@author: b3053674
"""

import PyCoTools as P
import os
import argparse
import time
import pickle
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



## Set to true if you want to pass model fie path from the command line
COMMAND_LINE=True

if COMMAND_LINE:


    #==============================================================================
    parser=argparse.ArgumentParser()
    parser.add_argument('model',help='copasi file for running through the pydentify workflow' )
    args=parser.parse_args()
    #==============================================================================





## Plot and save everything that we can
plot='true'
savefig='true'

if COMMAND_LINE:
    model=args.model
else:
    ## Set model variable to a path to COPASI file if not using COMMAND_LINE option
    model=r"D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PydentifyingBiomodelFoldersFromPyCoTools\PydentifyingBiomodels\BIOMD0000000016\Goldbeter1995_CircClock.cps"

print model
## get working directory and file
directory,fle=os.path.split(model)

profile_likelihood_computation_time_pickle=os.path.join(directory,'profile_likelihood_computation_time_pickle.pickle')

#%% Name time course reort and run time course, saving data to file and plotting 
## with matplotlib
TCReportName=os.path.join(directory,'timecourse_report.txt')
TC=P.pycopi.TimeCourse(model,End=1000,StepSize=20,Intervals=50,Plot=plot,SaveFig=savefig,
                       ReportName=TCReportName)
                       
print 'running time course {}'.format(TCReportName)
#%% Add Noise to timecourse for more interesting fits. 
noisy_data= P.Misc.add_noise(TCReportName)
noisy_datafile=os.path.join(directory,'noisy_data.txt')
noisy_data.to_csv(noisy_datafile,sep='\t')
print 'adding noise {}'.format(noisy_datafile)
#%% Run Parameter estimation. Do not randomize initial values as we
##  want to start the parameter estimation in a good place.
##  Run parameter estimation through the scan task to get only the best parameter
##  values rather than progression of optimization problem as function evalutions
##  Only run one parameter estimation save to file

PEResults_file=os.path.join(directory,'PEResults.txt')
print 'running parameter estimation for  {}'.format(PEResults_file)
PE=P.pycopi.ParameterEstimation(model,noisy_datafile,Method='GeneticAlgorithm',
                                RandomizeStartValues='false')
PE.write_item_template() #estimate all paraemter variables, therefore doesn't need editing 
PE.set_up()

S=P.pycopi.Scan(model,ScanType='repeat',NumberOfSteps=1,
                ReportName=PEResults_file,ReportType='parameter_estimation',Run='true')
                
                
#%% Insert estimated parameters into model
P.pycopi.InsertParameters(model,ParameterPath=PEResults_file)

#%% Run a 'current solution statistics' parameter estimation
##  to get a plot of simulated vs experimental data 
PE=P.pycopi.ParameterEstimation(model,noisy_datafile,Method='CurrentSolutionStatistics',
                                RandomizeStartValues='false',SaveFig=savefig,Plot=plot)
PE.set_up()
PE.run()

#%% Run profile likelihoods

start=time.time()
print 'running profile likelihoods for {}'.format(model)
P.pydentify2.ProfileLikelihood(model,ParameterPath=PEResults_file,
                               NumberOfSteps=10,UpperBoundMultiplier=1000,
                               LowerBoundMultiplier=100,Run='slow',Index=0)

computation_time=time.time()-start
with open(profile_likelihood_computation_time_pickle,'w') as f:
    pickle.dump(computation_time,f)
#%% Visualize profile likelihoods
P.pydentify2.Plot(model,ParameterPath=PEResults_file,Index=0,SaveFig=savefig)



