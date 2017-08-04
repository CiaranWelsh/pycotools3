# -*- coding: utf-8 -*-
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


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
 
"""
import site
#site.addsitedir('/home/b3053674/Documents/PyCoTools')
site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
from PyCoTools.Tests import base_tests
import unittest
import glob
import os
import shutil 
import pandas
import random

#
class ModelTests(base_tests._BaseTest):
    def setUp(self):
        super(ModelTests, self).setUp()
        
    def test_get_local_parameters_keys_model1(self):
        """
        Ensure we can successfully get local 
        parameters for model1        
        """
        if self.test_model == 'test_model1':
            locals = {'(ADeg).k1': 0.1, '(B2C).k2': 0.1, '(C2A).k1': 0.1}
            keys = sorted(locals.keys())
            self.assertListEqual(sorted(list(self.M.get_local_parameters().index)),
                                 sorted(keys) )
            
    def test_get_local_parameters_values_model1(self):
        """
        Ensure we can successfully get local 
        parameters for model1        
        """
        if self.test_model == 'test_model1':
            locals = {'(ADeg).k1': 0.1, '(B2C).k2': 0.1, '(C2A).k1': 0.1}
            values = sorted(locals.values())
            self.assertListEqual(sorted(list(self.M.get_local_parameters()['Value'])),
                                 sorted(values) )


    def test_get_compartments(self):
        """
        Ensure we can successfully get local 
        parameters for model1        
        """
        if self.test_model == 'test_model1':
            compartment_IDs = ['Compartment_1', 'Compartment_3']
            compartment_names = ['nuc','cyt']
            compartment_values = [3,3]
            compartments_df = self.M.get_compartments()
            for i in range(3):
                k = compartments_df.keys()[i]
                if k == 'Name':
                    self.assertListEqual(  list(compartments_df[k] ), compartment_names)
                elif k == 'IDs':
                    self.assertListEqual(  list(compartments_df[k] ), compartment_IDs)
                elif k == 'Value':
                    self.assertListEqual(  list(compartments_df[k] ), compartment_values)  
#            
#    def test_get_global_quntities_keys_model1(self):
#        """
#        Ensure we can successfully get local 
#        parameters for model1        
#        """
#        if self.test_model == 'test_model1':
#            locals = {'(ADeg).k1': 0.1, '(B2C).k2': 0.1, '(C2A).k1': 0.1}
#            values = sorted(locals.values())
#            self.assertListEqual(sorted(list(self.M.get_local_parameters()['Value'])),
#                                 sorted(values) )

            
#    def test_get_global_quantities(self):
#        print self.M.get_global_quantities()
            
    def test_get_metabolites(self):
        print self.M.get_metabolites()
        
        
if __name__=='__main__':
    unittest.main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
