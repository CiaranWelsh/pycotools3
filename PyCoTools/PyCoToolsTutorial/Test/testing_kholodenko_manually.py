#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:47:47 2017

@author: b3053674
"""

import site
site.addsitedir('/home/b3053674/Documents/PyCoTools')
import PyCoTools
import os, glob
import numpy

model = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Kholodenko.cps'
model2 = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Kholodenko_1.cps'


dire = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/MultipleParameterEstimationResults'

pl_d='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ProfileLikelihood/0/(phosphorylation_of_MAPKK).KK3.txt'
pl_f='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ProfileLikelihood/0/(phosphorylation_of_MAPKK).KK3.cps'
#
#

results_d = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Test4'
results_f = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/test1/ParameterFit1.txt'







import pandas
import os,glob
import site
site.addsitedir(r'/home/b3053674/Documents/PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models

TM = test_models.TestModels()
kholodenko_string = TM.get_kholodenko_variant1()
dire = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial'
kholodenko_model = os.path.join(dire, 'kholodenko_model.cps')

with open(kholodenko_model, 'w') as f:
    f.write(kholodenko_string)
    
    
#GMQ = PyCoTools.pycopi.GetModelQuantities(kholodenko_model)
#print GMQ.get_local_kinetic_parameters_cns()    
    
    

report= 'parameter_estimation_synthetic_data.txt'
TC=PyCoTools.pycopi.TimeCourse(kholodenko_model,end=1000,intervals=10,step_size=100,
                            report_name = report, global_quantities=None)


## Give fake data a meaningful name
data1 = TC['report_name']


from PyCoTools.pycopi import RunMultiplePEs

#%% 
report = 'parameter_estimation_data.txt'
RMPE=RunMultiplePEs(kholodenko_model,data1, copy_number=6, pe_number=50,
                       method='GeneticAlgorithm',plot=True,
                       population_size = 100,number_of_generations= 300,
                       report_name = report, lower_bound=0.1, upper_bound=100,
                       metabolites=[], global_quantities=[], savefig=True,
                       font_size=40)

#%%
#RMPE.write_config_template()
#%% 
RMPE.setup()
#%%
RMPE.run()
#%% 

#RMPE.format_results()
#PyCoTools.PEAnalysis.ParsePEData(RMPE['results_directory'])


#
##%%
#RMPE.format_results()
#'''
#End of multi param est stuff
#'''
#PE.format_results()

#os.system('CopasiUI {}'.format(kholodenko_model))





#from PyCoTools import PEAnalysis

#PEAnalysis.Boxplot(RMPE['results_directory'])










































