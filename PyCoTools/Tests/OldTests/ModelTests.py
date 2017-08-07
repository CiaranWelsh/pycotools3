#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 13:01:38 2017

@author: b3053674
"""

import unittest
import site
site.addsitedir('/home/b3053674/Documents/PyCoTools')
import PyCoTools
import TestModels
import lxml.etree as etree
import os, glob


MODEL_STRING = TestModels.Testmodels.get_model1()


'''
This set of tests are tailored specifically to
model1 from the TestModels module. 

'''

class ModelTests(unittest.TestCase):
    """
    
    """
    def setUp(self):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')
        self.copasiML = etree.fromstring(MODEL_STRING)
        if os.path.isfile(self.copasi_file):
            os.remove(self.copasi_file)
            
        ## get model from TestModels and write to file for use in this
        ## set of tests
        root = etree.ElementTree(self.copasiML)
        root.write(self.copasi_file)
        self.M = PyCoTools.pycopi.Model(self.copasi_file)

    
    def test_get_time_unit(self):
        self.assertEqual(self.M.get_time_unit(),'s')
        
    def test_get_volume_unit(self):
        self.assertEqual(self.M.get_volume_unit(),'ml')
    
    def test_get_quantity_unit(self):
        self.assertEqual(self.M.get_quantity_unit(),'mmol')
        
    def test_get_area_unit(self):
        self.assertEqual(self.M.get_area_unit(), u'm\xb2')
        
    def test_get_length_unit(self):
        self.assertEqual(self.M.get_length_unit(), 'm')
        
    def test_get_avagadro(self):
        self.assertEqual(self.M.get_avagadro(), 6.022140857e+23 )
    
    def test_get_model_key(self):
        self.assertEqual(self.M.get_model_key(), 'Model_3')
        
    def test_get_compartments1(self):
        """
        Ensure there are 2 compartments
        """
        self.assertEqual(len(self.M.get_compartments().keys() ),  2)
        
    def test_get_compartments2(self):
        """
        ensure the dict has correct keys
        """
        key_list = ['dimensionality', 'simulationType', 'name', 'key']
        compartment_keys =  self.M.get_compartments().keys()
        compartment1 = self.M.get_compartments()[compartment_keys[0]]
        self.assertEqual(sorted(key_list), sorted(compartment1.keys() ))
        
    def test_get_compartments3(self):
        """
        
        """
        name_dct = {'Compartment_1': 'nuc', 'Compartment_3': 'cyt'}
        self.assertEqual( self.M.get_compartments('name'), name_dct)
        
        
        
        
    def test_get_metabolites1(self):
        """
        Ensure there are 4 metablites
        """
        self.assertEqual(len(self.M.get_metabolites().keys() ),  3)
        
    def test_get_metabolites2(self):
        """
        ensure the dict has correct keys
        """
        key_list = ['key', 'name', 'simulationType', 'compartment']
        metabolite_keys =  self.M.get_metabolites().keys()
        metabolite1 = self.M.get_metabolites()[metabolite_keys[0]]
        self.assertEqual(sorted(key_list), sorted(metabolite1.keys() ))
        
    def test_get_metabolites3(self):
        """
        test using name as attribute
        """
        self.assertEqual( self.M.get_metabolites('name')['Metabolite_3'],'B')
        
        
        
    def test_get_global_quantities1(self):
        self.assertEqual( len(self.M.get_global_quantities() )  , 2)
        
    
    def test_get_global_quantities2(self):
        key_list = ['key', 'name', 'simulationType']
        global_quantity_keys =  self.M.get_global_quantities().keys()
        global_quantity1 = self.M.get_global_quantities()[global_quantity_keys[0]]
        self.assertEqual(sorted(key_list), sorted(global_quantity1.keys() ))


    def test_get_model_constants(self):
        """
        
        """
        self.assertEqual(len( self.M.get_local_parameters()), 5)
        
    def test_get_reactions(self):
        """
        
        """
        self.assertEqual(len( self.M.get_reactions()['Reaction_2'].keys()), 4)



if __name__=='__main__':
    unittest.main()




























