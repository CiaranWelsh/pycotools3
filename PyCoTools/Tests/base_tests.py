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

class _TestModel2File(unittest.TestCase):
    def setUp(self):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        with open(self.copasi_file,'w') as f:
            f.write(test_models.TestModels.get_model1())
            
    def tearDown(self):
        os.remove(self.copasi_file)
            
            
            
class _TimeCourseBase(_TestModel2File):
    
    def setUp(self):
        super(_TimeCourseBase, self).setUp()
        
        self.TC = PyCoTools.pycopi.TimeCourse(self.copasi_file, end=1000, step_size=1000, 
                                              intervals=1000)
        
    def tearDown(self):
        super(_TimeCourseBase, self).tearDown()
        os.remove(self.TC['report_name'])
        
    def test(self):
        pass
        
        
    
    
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




















