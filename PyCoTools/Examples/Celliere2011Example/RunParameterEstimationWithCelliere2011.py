# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 21:59:01 2017

@author: b3053674
"""
import PyCoTools
import os
import pandas
import numpy

import FilePaths

## Instantiate class contianing file paths for Celliere2011` example
C=FilePaths.Celliere2011Example()

## Set up a parameter estimation 
'''
First instantiate ParameterEstimation class
with chosen keyword arguments. define the method variables within the PE class using the key word arguments
'''

PE= PyCoTools.pycopi.ParameterEstimation(C.celliere2011_model, #model
                                           C.noisy_timecourse_report, #experimental data
                                           Method='GeneticAlgorithm',#use a quick global algorithm 
                                           NumberOfGenerations=300, #set Generation Number and population size
                                           PopulationSize=150)
#                                           Plot='true',SaveFig='true') ## Optionally use to get experimental Vs simualted graphs
'''
Then write a template file. This contains all your model variables. 
Delete the rows containing variables that you do not want to estimate, modify
the estimation boundaries as you see fit, save and close. The last three columns
are for PyCoTools to set and map your variables and do not need to be touched. 

In this example I've removed the initial concentration varibles from the estimation

Comment and uncomment the below lines of code as you need
'''
#PE.write_item_template()


'''
Perform the setting up of the parameter estimation
Variable names in the experimental data header need to exactly match the 
corresponding variables in the model to be mapped correctly. 
'''
PE.set_up()

'''
The run method enables you to run the parameter estimation from Python. 
If the Plot keyword was set to 'true' in the instantiation of the ParameterEstimation
class, plots are generated of the experimental vs simulated data. 
In this tutorial however we want to run the parameter estimation via the repeat
scan task so we'll not use the run method.
'''
#PE.run() 
#

'''
Run the parameter estimation via the scan task to run 'NumberOfSteps' of them

Other options include copying the model to 'n' other file locations. 
Then you could run the same code in a loop and have n copasi's running parameter
estimations on one machine. Alternatively the 'submit_copasi_multijob.py' 
script under the 'Scripts' folder in PyCoTools main directory will submit 
a copasi file 'n' times to a SunGrinEngine based cluster. Support for 
other job schedulers is not currently supported but modular nature of PyCoTools
allows for extension code to support other systems. 

#'''
PyCoTools.pycopi.Scan(C.celliere2011_model,ScanType='repeat',
                      ReportName=C.PEData_file, 
                      ReportType='parameter_estimation',
                      NumberOfSteps=1,
                      Run='false') ## Change run to true to run on this computer


'''
Run is currently set to false because the copasi file was run on a cluster
'''



























