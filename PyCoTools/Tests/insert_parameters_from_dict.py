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
site.addsitedir('/home/b3053674/Documents/PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
from PyCoTools.Tests import base_tests
import unittest
import glob
import os
import shutil 
import pandas
import random


class TestInsertPEFromDict(base_tests._BaseTest):
    def setUp(self):
        super(TestInsertPEFromDict, self).setUp()


        
    def test_local(self):
        names = self.GMQ.get_local_parameters()
        values = [i*random.random() for i in range(1, len(names)+1)]
        parameter_dict = dict(zip(names, values) )
        I = PyCoTools.pycopi.InsertParameters(self.copasi_file, 
                                          parameter_dict=parameter_dict)
        GMQ = PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
        inserted = I.parameters
        extracted = GMQ.get_local_parameters()
        for i in inserted:
            self.assertAlmostEqual(float(inserted[i]), float(extracted[i] ))
            
            

    def test_metabolites(self):
        names = self.GMQ.get_metabolites().keys()
        print names
#        values = [i*random.random() for i in range(1, len(names)+1)]
#        parameter_dict = dict(zip(names, values))
##        print parameter_dict
##        os.system('CopasiUI {}'.format(self.copasi_file))
#        I = PyCoTools.pycopi.InsertParameters(self.copasi_file,
#                                       parameter_dict=parameter_dict)
#        GMQ = PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
##        os.system('CopasiUI {}'.format(self.copasi_file))
#        conc = {}
#        for metab in GMQ.get_metabolites():
#            conc[metab] = GMQ.get_metabolites()[metab]['concentration']
#        
#        for i in conc:
#            self.assertAlmostEqual(float(I.parameters[i]), conc[i]  )

















if __name__=='__main__':
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
