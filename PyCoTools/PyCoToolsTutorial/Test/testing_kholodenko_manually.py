#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:47:47 2017

@author: b3053674
"""

import site
#site.addsitedir('/home/b3053674/Documents/PyCoTools')
site.addsitedir(r'C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
import os, glob
import numpy

#model = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Kholodenko.cps'
#model2 = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Kholodenko_1.cps'
#
#
#dire = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/MultipleParameterEstimationResults'
#
#pl_d='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ProfileLikelihood/0/(phosphorylation_of_MAPKK).KK3.txt'
#pl_f='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ProfileLikelihood/0/(phosphorylation_of_MAPKK).KK3.cps'
##
##
#
#results_d = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Test4'
#results_f = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/test1/ParameterFit1.txt'







import pandas
import os,glob
import site
#site.addsitedir(r'/home/b3053674/Documents/PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models

TM = test_models.TestModels()
kholodenko_string = TM.get_kholodenko_variant1()
dire = r'C:\Users\Ciaran\Documents\PyCoTools\PyCoTools\PyCoToolsTutorial'
kholodenko_model = os.path.join(dire, 'kholodenko_model.cps')

with open(kholodenko_model, 'w') as f:
    f.write(kholodenko_string)
    
    
#GMQ = PyCoTools.pycopi.GetModelQuantities(kholodenko_model)
#print GMQ.get_local_kinetic_parameters_cns()    
    
    
#
report= 'parameter_estimation_synthetic_data.txt'
TC=PyCoTools.pycopi.TimeCourse(kholodenko_model,end=1000,intervals=10,step_size=100,
                            report_name = report, global_quantities=None)
#
#
## Give fake data a meaningful name
data1 = TC['report_name']


from PyCoTools.pycopi import RunMultiplePEs

report = 'parameter_estimation_data2.txt'
RMPE=RunMultiplePEs(kholodenko_model,data1, copy_number=6, pe_number=100,
                       method='ParticleSwarm',plot=True,
                       swarm_size=100, iteration_limit=2000,
                       report_name = report, lower_bound=0.1, upper_bound=100,
                       metabolites=[], global_quantities=[], savefig=True,
                       font_size=40)

RMPE.write_config_template()
RMPE.setup()
#RMPE.format_results()
RMPE.run()

#print PyCoTools.PEAnalysis.ParsePEData(RMPE['results_directory']).data

#PyCoTools.PEAnalysis.Boxplot(data=RMPE['results_directory'], log10=True, savefig=True, num_per_plot=23)
#PyCoTools.PEAnalysis.RssVsIterations(RMPE['results_directory'], log10=True,savefig=True)
#PyCoTools.PEAnalysis.Histograms(RMPE['results_directory'], log10=True, savefig=True,title_fontsize=40 )

#PyCoTools.PEAnalysis.EnsembleTimeCourse(kholodenko_model, data1, RMPE['results_directory'], 
#                                           savefig=True,
#                                           )
#PyCoTools.PEAnalysis.Pca(RMPE['results_directory'], log10=True, savefig=True, by='parameters')
#PyCoTools.PEAnalysis.Pca(RMPE['results_directory'],
#                         log10=True, savefig=True, by='iterations',
#                         x=10)
#
#PyCoTools.PEAnalysis.LinearRegression(RMPE['results_directory'],
#                                      savefig=True, title_fontsize=70)



#'''
#profile likelihood stuff
#'''
#model = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/kholodenko_model_1.cps'
#
#PyCoTools.pydentify.ProfileLikelihood(model, parameter_path=RMPE['results_directory'],
#                                      index = [0,1], run='slow', log10=True)

#path = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/MultipleParameterEstimationResults'
#PyCoTools.pydentify.Plot2(model, parameter_path=path, 
#                         index=[0,1], log10=True,
#                         mode='one',plot_parameter='(MAPKKK activation).K1',
#                         plot_index=0)



#
pl_dir = r'C:\Users\Ciaran\Documents\PyCoTools\PyCoTools\PyCoToolsTutorial\ProfileLikelihood'
model = r'C:\Users\Ciaran\Documents\PyCoTools\PyCoTools\PyCoToolsTutorial\kholodenko_model_1.cps'
parameter_path = r'C:\Users\Ciaran\Documents\PyCoTools\PyCoTools\PyCoToolsTutorial\MultipleParameterEstimationResults'
#'/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/ProfileLikelihood'
PL = PyCoTools.pydentify.ParsePLData(model,pl_dir, parameter_path=parameter_path,
                                     index=[0,1])
keys = list(PL.data.keys())

for k in keys:
    PyCoTools.pydentify.Plot2(PL.data, x=k, y='RSS')
    



'''

Could have a class to plot the parameter of interest against
the RSS. 
Or make the class accept the list of parameters to plot
in a single plot. 

The independent values will be on the x axis (i.e. 1 to 10if the 
parameter of interest scanned between 1 nd 10. 
Then all other parameters will be on the y. 

Arguments then --> x is a single parameter name
                --> y is  single parameter or list of parameters 
                            to put on the y axis. 
)

Need copasi file and parameter path as args


'''


#data = PL.data
#print data
#data.to_csv(os.path.join(os.path.dirname(pl_dir), 'test_pl_data.csv') )
'''
sort out PL boundaries when running PL
'''















