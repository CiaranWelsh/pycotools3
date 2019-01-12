# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 20:23:21 2017

@author: b3053674
"""

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




 Object:
 
This file takesa copasi file and performs a series of copasi tasks using the model. 
This series of tasks include:
    1) time course. 
    2) add noise to time course
    3) use time course to estimate all model parameters
    4) visualize parameter estimates
    5) use parameter estimates in profile likelihood calculation
    6) visualize profile likelihoods


Author: Ciaran Welsh
Date: 12/03/2017
 
 """

import PyCoTools as P
import os
import argparse
import time
import pickle
import logging
'''
Download models from Biomodels in another Script. 

Import models into copasi in another

iterate over workflow for each model

Workflow:

    1) run a time course
    2) add noise to time course data
    3) run global parameter estimation with noisy data
    4) run local chaser parameter estimation
    5) run profile likelihood
    6) plot profile likelihood
    
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








## plot and save everything that we can
plot='true'
savefig='true'

if COMMAND_LINE:
    model=args.model
else:
    ## Set model variable to a path to COPASI file if not using COMMAND_LINE option
    model=r"D:\MPhil\Python\My_Python_Modules\modelling_Tools\PydentifyingBiomodelFoldersFromPyCoTools\PydentifyingBiomodels\BIOMD0000000016\Goldbeter1995_CircClock.cps"

print(model)
## get working directory and file
directory,fle=os.path.split(model)
log_filename=os.path.join(directory,fle[:-4]+'log.log')
P.Misc.setup_logger(__name__,log_filename,level=logging.DEBUG)
LOG=logging.getlog10ger(__name__)

profile_likelihood_computation_time_pickle=os.path.join(directory,'profile_likelihood_computation_time_pickle.pickle')

#%% Name time course reort and run time course, saving data to file and plotting 
## with matplotlib

TCreport_name=os.path.join(directory,'timecourse_report.txt')
LOG.debug('running TimeCourse')
TC=P.pycopi.TimeCourse(model,End=1000,StepSize=20,Intervals=50,plot=plot,savefig=savefig,
                       report_name=TCreport_name)
LOG.debug('TimeCourse finished')
#%% Add Noise to timecourse for more interesting fits. 
LOG.debug('adding noise to {}'.format(TCreport_name))
noisy_data= P.Misc.add_noise(TCreport_name)
noisy_datafile=os.path.join(directory,'noisy_data.txt')
noisy_data.to_csv(noisy_datafile,sep='\t')
LOG.debug('noise added to {}'.format(TCreport_name))
#%% run Parameter estimation. Do not randomize initial values as we
##  want to start the parameter estimation in a good place.
##  run parameter estimation through the scan task to get only the best parameter
##  values rather than progression of optimization problem as function evalutions
##  Only run one parameter estimation save to file

LOG.debug('running parameter estimation')
PEResults_file=os.path.join(directory,'PEResults.txt')
print('running parameter estimation for  {}'.format(PEResults_file))
PE=P.pycopi.ParameterEstimation(model,noisy_datafile,method='GeneticAlgorithm',
                                randomize_start_values='false')
PE.write_item_template() #estimate all paraemter variables, therefore doesn't need editing 
PE.set_up()
LOG.debug('running parameter estimation from scan task')
S=P.pycopi.Scan(model,scan_type='repeat',number_of_steps=1,
                report_name=PEResults_file,report_type='parameter_estimation',run='true')
LOG.debug('parameter estimation finished')
                
#%% Insert estimated parameters into model
LOG.debug('inserting parameters into model to plot experimental versus simulated')
P.pycopi.InsertParameters(model,parameter_path=PEResults_file)
LOG.debug('parameters inserted')

#%% run a 'current solution statistics' parameter estimation
##  to get a plot of simulated vs experimental data 
LOG.debug('running current solution parameter esitmation')
PE=P.pycopi.ParameterEstimation(model,noisy_datafile,method='CurrentSolutionStatistics',
                                randomize_start_values='false',savefig=savefig,plot=plot)
PE.set_up()
PE.run()
LOG.debug('current solution parameter estimation finished')

#%% run profile likelihoods

start=time.time()
LOG.debug('setting up and running profile likelihoods')
P.pydentify2.ProfileLikelihood(model,parameter_path=PEResults_file,
                               number_of_steps=10,upper_boundMultiplier=1000,
                               lower_boundMultiplier=100,run='slow',index=0)

computation_time=time.time()-start
LOG.debug('profile likelihoods calculated for model {}'.format(model))
LOG.debug('computation time for computation of profile likelihoods was: {} seconds'.format(computation_time))


with open(profile_likelihood_computation_time_pickle,'w') as f:
    pickle.dump(computation_time,f)

#%% Visualize profile likelihoods
LOG.debug('plotting profile likelihoods')
P.pydentify2.plot(model,parameter_path=PEResults_file,index=0,savefig=savefig)
LOG.debug('profiles plotted')


