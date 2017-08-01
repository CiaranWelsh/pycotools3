#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:43:23 2017

@author: b3053674
"""

import site
site.addsitedir('/home/b3053674/Documents/PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
import unittest
import glob
import os
import shutil 
import pandas

class _BaseTest(unittest.TestCase):
    """
    class for all tests to inherit from. 
        -> Take string model from TestModels and write to file
        -> Initiate GetModelQuantities
    """
    def setUp(self):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        with open(self.copasi_file,'w') as f:
            f.write(test_models.TestModels.get_model1())
            
        self.GMQ = PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
        self.M = PyCoTools.pycopi.Model(self.copasi_file)
            
    def tearDown(self):
        os.remove(self.copasi_file)
        del self.GMQ
        del self.copasi_file
            
            
            
class _TimeCourseBase(_BaseTest):
    
    def setUp(self):
        super(_TimeCourseBase, self).setUp()
        
        self.TC = PyCoTools.pycopi.TimeCourse(self.copasi_file, end=1000, step_size=1, 
                                              intervals=1000)
        
    def tearDown(self):
        super(_TimeCourseBase, self).tearDown()
        os.remove(self.TC['report_name'])
        del self.TC
        
class _ParameterEstimationBase(_BaseTest):
    """
    Simulate 2 time courses. Add noise then use PE class
    """
    def setUp(self):
        super(_ParameterEstimationBase, self).setUp()
        
        self.parameter_estimation_options={#report variables
                 'metabolites':self.GMQ.get_IC_cns().keys(),
                 'global_quantities':self.GMQ.get_global_quantities().keys(),
                 'append': True, 
                 'confirm_overwrite': True,
                 'overwrite_config_file':True,
                 #
                 'update_model':True,
                 'randomize_start_values':True,
                 'create_parameter_sets':True,
                 'calculate_statistics':True,
                 #method options
                 'method':'ScatterSearch',
                 #'DifferentialEvolution',
                 'number_of_generations':64,
                 'population_size':10,
                 'random_number_generator':4,
                 'seed':0,
                 'pf':0.675,
                 'iteration_limit':1140,
                 'tolerance':0.1,
                 'rho':0.2,
                 'scale':100,
                 'swarm_size':500,
                 'std_deviation':0.0000004641,
                 'number_of_iterations':1516400000,
                 'start_temperature':100,
                 'cooling_factor':0.85498,
                 #experiment definition options
                 'scheduled':True,
                 'plot':True,
                 'savefig':True
                 }
        
        
        
        
        self.TC1 = PyCoTools.pycopi.TimeCourse(self.copasi_file, end=1000, step_size=100, 
                                              intervals=10, report_name='report1.txt')
        self.TC2 = PyCoTools.pycopi.TimeCourse(self.copasi_file, end=1000, step_size=100, 
                                              intervals=10, report_name='report2.txt')
        
        data1 = PyCoTools.Misc.add_noise(self.TC1['report_name'])
        data2 = PyCoTools.Misc.add_noise(self.TC2['report_name'])
        
        os.remove(self.TC1['report_name'])
        os.remove(self.TC2['report_name'])
        
        data1.to_csv(self.TC1['report_name'], sep='\t')
        data2.to_csv(self.TC2['report_name'], sep='\t')
        
        self.PE = PyCoTools.pycopi.ParameterEstimation(self.copasi_file,[self.TC1['report_name'],self.TC2['report_name'] ],
                                                        **self.parameter_estimation_options)
        
    def tearDown(self):
        super(_ParameterEstimationBase, self).tearDown()
        os.remove(self.TC1['report_name'])
        os.remove(self.TC2['report_name'])    
    
    
#class 
#    self.TC = PyCoTools.pycopi.TimeCourse(self.copasi_file, end=1000, step_size=100,
#                                     intervals=10)
    

#
#class _MultiParameterEstimationBase(_TestModel2File):
#    def setUp(self):
#        super(_MultiParameterEstimation, self).setUp()
#        
#        ## do time course
#        self.TC=PyCoTools.pycopi.TimeCourse(self.copasi_file,step_size=100,plot=False,
#                                               intervals=50,end=5000)
#
#
#        
#        self.RMPE=PyCoTools.pycopi.RunMultiplePEs(self.copasi_file, self.TC['report_name'],
#                                                copy_number=2,
#                                                pe_number=2,
#                                                population_size=10,
#                                                number_of_generations=20,
#                                                randomize_start_values=True,
#                                                plot=False,
#                                                lower_bound=0.1, upper_bound=100,
#                                                metabolites=[], global_quantities=[])
#        self.RMPE.write_config_template()
#        self.RMPE.set_up()
#        self.RMPE.run()
#        self.data = self.wait_for_PEs()
#        self.RMPE.format_results()
#        
##        
#    def wait_for_PEs(self):
#        number_of_expected_PEs = 4
#        x=0
#        
#        while x!=number_of_expected_PEs:
#            df_dct = {}
#            for f in os.listdir(self.RMPE['results_directory']):
#                f = os.path.join(self.RMPE['results_directory'], f)
#                try:
#                    df_dct[f] = pandas.read_csv(f, sep='\t', skiprows=1,header=None)
#                except IOError:
#                    continue
#                except pandas.io.common.EmptyDataError:
#                    continue
#            try:
#                df = pandas.concat(df_dct)
#
#            except ValueError:
#                continue
#            x = df.shape[0]
#        
#        return df
#
#
#
#    def tearDown(self):
##        os.remove(self.TC['report_name'])
##        os.remove(self.RMPE['results_directory'])
#        for i in glob.glob('*.xlsx'):
#            os.remove(i)
#            
#        for i in glob.glob('*.txt'):
#            os.remove(i)
#            
#        for i in glob.glob('*.cps'):
#            os.remove(i)    
#            





#class Base(unittest.TestCase):
#    def setUp(self):
#        self.shared = 'I am shared between everyone'
#        
#    def tearDown(self):
#        del self.shared
#        
#        
#class Base2(Base):
#    def setUp(self):
#        super(Base2, self).setUp()
#        self.partial_shared = 'I am shared between only some tests'
#        
#    def tearDown(self):
#        del self.partial_shared
#        
#        
#class Test1(Base):
#    
#    def test(self):
#        print self.shared
#        test_var = 'I only need Base'
#        print test_var
#        
#        
#        
#class Test2(Base2):
#    
#    def test(self):
#        print self.partial_shared
#        test_var = 'I only need Base2'
#        
#        
#class Test3(Base2):
#    
#    def test(self):
#        test_var = 'I need both Base and Base2'
#        print self.shared
#        print self.partial_shared
#        
#    
if __name__=='__main__':
    unittest.main()




















