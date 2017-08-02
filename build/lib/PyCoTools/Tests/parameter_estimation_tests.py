# -*- coding: utf-8 -*-

'''
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


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
 
'''

import site
#site.addsitedir('/home/b3053674/Documents/PyCoTools')
site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
import unittest
import glob
import os
import shutil 
import pandas
from PyCoTools.Tests import base_tests



class ParameterEstimationTests(base_tests._ParameterEstimationBase):

    def setUp(self):
        super(ParameterEstimationTests, self).setUp()

            

    def test_write_config_template(self):
        '''
        testthat the item file template is written
        '''
        self.PE.write_config_template()
        self.assertTrue(os.path.isfile(self.PE['config_filename'] )  )
        

    def test_insert_fit_items(self):
        '''
        Tests that there are the same number of rows in the template file 
        as there are fit items inserted into copasi
        '''
        self.PE.write_config_template()
        self.PE.copasiML=self.PE.remove_all_fit_items()
        self.PE.copasiML= self.PE.insert_all_fit_items()
        num_fit_items= self.PE.read_item_template().shape[0]
        self.assertEqual(num_fit_items, len(self.PE.get_fit_items()))

    def test_set_PE_method(self):
        '''
        test to see if method has been properly inserted into the copasi file
        '''
        self.PE.write_config_template()
        self.PE.setup()
        
        tasks=self.PE.copasiML.find('{http://www.copasi.org/static/schema}ListOfTasks')
        for i in tasks:
            if i.attrib['name']=='Parameter Estimation':
                self.assertEqual(i[-1].attrib['type'].lower(),self.parameter_estimation_options['method'].lower())
#
    def test_set_PE_options(self):
        self.PE.write_config_template()
        self.PE.setup()


        tasks=self.PE.copasiML.find('{http://www.copasi.org/static/schema}ListOfTasks')
        for i in tasks:
            if i.attrib['name']=='Parameter Estimation':
                self.assertEqual(i.attrib['scheduled'],'true')
                
    def test_results_folder(self):
        """
        
        """
        self.PE.write_config_template()
        self.PE.setup()
        self.PE.run()
        self.assertTrue(os.path.isdir(self.PE['results_directory']) )
        
        
    def test_results_folder(self):
        """
        
        """
        self.PE.write_config_template()
        self.PE.setup()
        self.PE.run()
        self.assertTrue(len(self.GMQ.get_fit_items()), 
                        len(os.listdir(self.PE['results_directory'])))
            
        
        


    def tearDown(self):
        super(ParameterEstimationTests,self).tearDown()
        
        for i in glob.glob('*.txt'):
            os.remove(i)
            
        for i in glob.glob('*.xlsx'):
            os.remove(i)
            
        shutil.rmtree(self.PE['results_directory'])




        
if __name__=='__main__':
    unittest.main()