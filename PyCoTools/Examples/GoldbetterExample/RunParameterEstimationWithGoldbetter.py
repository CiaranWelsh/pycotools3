# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 21:59:01 2017

@author: b3053674
"""
import PyCoTools
import os
import pandas
import numpy

current_directory='D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Examples\GoldbetterExample'
copasi_file=r'Goldbeter1995_CircClock.cps'
goldbetter_model=os.path.join(current_directory,copasi_file)
report=os.path.join(current_directory,'TimeCourseOutput.txt')
noisy_report=os.path.join(current_directory,'NoisyTimeCourseOutput.txt')


#set up a parameter estimation 
'''
First define the method variables within the PE class using the key word arguments

    
'''

PE= PyCoTools.pycopi.ParameterEstimation(goldbetter_model, #model
                                           noisy_report, #experimental data
                                           Method='GeneticAlgorithm',#use a quick global algorithm 
                                           NumberOfGenerations=10, #set low number of generations for speed
                                           PopulationSize=10, #set low population size parameter for speed
                                           Separator=[',']) #we wrote data to csv so need to tell copasi
'''
Then write a template file. This contains all your model variables. 
Delete the rows containing variables that you do not want to estimate, modify
the estimation boundaries as you see fit, save and close.

In this example I've removed the initial concentration varibles from the estimation

Comment and uncomment the below lines of code as you need
'''
#PE.write_item_template()


#Perform the setting up of the parameter estimation
PE.set_up()

'''
The run method enables you to run the parameter estimation from Python. 
If the Plot keyword was set to 'true' in the instantiation of the ParameterEstimation
class, plots would be generated of the experimental vs simulated data. 
In this tutorial however we want to run the parameter estimation via the repeat
scan task so we'll not use the run method.
'''
#PE.run() 

PEData_report=os.path.join(current_directory,'PEData.txt')

'''
Run the parameter estimation via the scan task to run 500 of them

Other options include copying the goldbetter model to four other file paths. 
Then you could run the same code in a loop and have n copasi's running parameter
estimations. Careful not to do too many at once though as it will eat all your 
computer power

'''
PyCoTools.pycopi.Scan(goldbetter_model,ScanType='repeat',
                      ReportName=PEData_report,
                      ReportType='parameter_estimation',
                      NumberOfSteps=500,Run='true')






























