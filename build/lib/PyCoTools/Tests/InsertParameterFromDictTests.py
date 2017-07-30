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

class TestInsertPEFromDict(unittest.TestCase):
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
        
        self.M=PyCoTools.pycopi.Model(self.copasi_file)
        
        
            
    def test_local(self):
        print self.M.get_local_parameters()
        
        
        
        
        
    def tearDown(self):
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__=='__main__':
    unittest.main()