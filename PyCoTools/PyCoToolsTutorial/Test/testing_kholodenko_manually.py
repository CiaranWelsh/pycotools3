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









from PyCoTools.pycopi import ParameterEstimation 

report = 'parameter_estimation_data2.txt'
PE=ParameterEstimation(kholodenko_model,data1,method='GeneticAlgorithm',plot=True,
                       population_size = 100,number_of_generations= 300,
                       report_name = report, lower_bound=0.1, upper_bound=100,
                       metabolites=[], global_quantities=[])


PE.write_config_template()
PE.setup()
PE.run()
#PE.format_results()

os.system('CopasiUI {}'.format(kholodenko_model))
#






#PyCoTools.pycopi.FormatPEData(model, '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ParameterFit0.txt', 
#                              report_type='multi_parameter_estimation')


#TC = PyCoTools.pycopi.TimeCourse(model, end = 1000, step_size=100, intervals=10,
#                            plot=False)



#noisy = PyCoTools.Misc.add_noise(TC['report_name'])
#if os.path.isfile(TC['report_name']):
#    os.remove(TC['report_name'])
#noisy.to_csv(TC['report_name'], sep='\t')
#RMPE = PyCoTools.pycopi.RunMultiplePEs(model, TC['report_name'], copy_number = 4,
#                                       pe_number = 25, population_size = 50, 
#                                       number_of_generations=200, results_directory = 'Test4')
###
##RMPE.write_config_template()
#RMPE.setup()
#RMPE.run()
#RMPE.format_results()



#data = PyCoTools.PEAnalysis.ParsePEData(results_d , log10=True).data
#PyCoTools.PEAnalysis.Boxplot(data, results_directory=os.path.dirname(model), save=True)
##
#PyCoTools.PEAnalysis.RssVsIterations(data, results_directory=os.path.dirname(model), save=True)
#
#
#
#[PyCoTools.PEAnalysis.Pca(data, results_directory=os.path.dirname(model), save=True, orientation=i) for i in ['parameters','iterations'] ]
#PyCoTools.PEAnalysis.Histograms(data, results_directory=os.path.dirname(model), save=True)
#PyCoTools.PEAnalysis.Scatters(data, results_directory=os.path.dirname(model), save=True)



#PyCoTools.PEAnalysis.PlotParameterEnsemble(model, 
#                                           TC['report_name'], 
#                                           results_d, save=True,
#                                           results_directory=os.path.dirname(model))
#I = PyCoTools.pycopi.InsertParameters(model2, parameter_path = results_d, index=0)
#print I.parameters.transpose().sort_index()
#
#
#os.system('CopasiUI {}'.format(model2))

#import pandas
#import seaborn
#
#time = [0, 100, 200, 0, 100, 200]
#experiment = [0,0,0,1,1,1]
#A = [0 ,5 ,10, 1, 3, 6]
#B= [0,6,11, 3,6, 9]
#C= [4,9,13, 5, 6, 8]
#D= [5, 10, 3,7,9, 10]
#
#df = pandas.DataFrame(numpy.array([experiment, time, 
#                                    A, B, C, D])).transpose()
#df.columns = ['Experiment','Time','A','B','C','D']
##print df
#seaborn.tsplot(data=df, time='Time', unit='Experiment', value='A')

#                        ,
#                        repeat2_species1,
#                        repeat1_species2,
#                        repeat2_species2])


#d = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/test1/ParameterFit1.txt'
#1
#PyCoTools.pycopi.FormatPEData(model2, d, report_type = 'multi_parameter_estimation')


#
#PyCoTools.pycopi.Reports(model, report_type='multi_parameter_estimation')
#
#
#







#PyCoTools.pydentify.FormatPLData(pl_f, pl_d).format


#P = PyCoTools.pydentify.Plot(model, parameter_path = dire, rss=0.1)#, index=0)#, mode='one', plot_index = 0, plot_parameter='(dephosphorylation of MAPK-PP).V9')
#
#PyCoTools.pycopi.Reports(model, report_type='profilelikelihood2', variable='A')
##
#os.system('CopasiUI {}'.format(model))
#S=PyCoTools.pycopi.Scan(model, scan_type='scan', variable='A')


#os.system('CopasiUI {}'.format(model))

#PL = PyCoTools.pydentify.ProfileLikelihood(model, run='slow', index=-1, iteration_limit=25, 
#                                           number_of_steps = 10,
#                                           tolerance = 1e-3)

#PyCoTools.pydentify.Plot(model, rss=0.01, index=-1, mode='one',
#                         plot_index=-1, plot_parameter='(MAPKKK activation).K1',
#                         log10=True)

#f=r'/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ProfileLikelihood/-1/B.cps'
#import subprocess
#
#def run(copasi_file):
#    '''
#    Process the copasi file using CopasiSE
#    Must be Copasi version 16
#    
#    '''
#    args=['CopasiSE',"{}".format(copasi_file)] 
#    p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
#    output,err= p.communicate()
#    d={}
#    d['output']=output
#    d['error']=err
#    if err!='':
#       raise PyCoTools.Errors.CopasiError('Failed with Copasi error: \n\n'+d['error'])
#    return d['output']
#
#run(f)
#

#
#TC = PyCoTools.pycopi.TimeCourse(model, end = 1000, step_size=1, intervals=1000,
#                            plot=False)
#PyCoTools.Misc.add_noise(TC['report_name'])
#RMPE = PyCoTools.pycopi.RunMultiplePEs(model, TC.kwargs['report_name'], copy_number = 4,
#                                       pe_number = 25, population_size = 20, 
#                                       number_of_generations=20, results_directory = 'test1')
###
#RMPE.write_config_template()
#RMPE.setup()
#RMPE.run()
#RMPE.format_results()












#RMPE.format_results()
#PE = PyCoTools.pycopi.ParameterEstimation(model, TC.kwargs['report_name'],
#                                          method = 'GeneticAlgorithm',
#                                          population_size=20,
#                                          number_of_generations=20,
#                                          plot=True)
#
##PE.write_config_template()
#PE.setup()
#PE.run()
#print PE.format_results()

#GMQ=PyCoTools.pycopi.GetModelQuantities(model)
#print GMQ.get_fit_item_order()


#
#pe_data ='/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/Kholodenko_PE_results.txt'
#
#
#I=PyCoTools.pycopi.InsertParameters(model, parameter_path=pe_data, index=0)
#print I.parameters.transpose().sort_index()
#
#
#os.system('CopasiUI {}'.format(model))
#















