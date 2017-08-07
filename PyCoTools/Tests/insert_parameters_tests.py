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

import pickle
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
from PyCoTools.Tests import test_base
from random import shuffle, random
from PyCoTools.pycopi import InsertParameters



class InsertParametersTests(test_base._MultiParameterEstimationBase):
    def setUp(self):
        super(InsertParametersTests, self).setUp()
        self.metabolites = self.GMQ.get_IC_cns()
        self.local_parameters = self.GMQ.get_local_parameters()
        self.global_quantities = self.GMQ.get_global_kinetic_parameters_cns()

#    def test_local_from_dct(self):
#        """
#        test currently fails. Still a useful test but first go through
#        and ensure parameters get inserted properly on an individual basis
#        """
#        keys = self.local_parameters.keys()
#        shuffle(keys)
#        new_dct = dict(zip(keys, range(len(keys))))
#        I = PyCoTools.pycopi.InsertParameters(self.copasi_file, 
#                                              parameter_dict=new_dct)
#        GMQ = PyCoTools.pycopi.GetModelQuantities(self.copasi_file)
#        local_parameters = GMQ.get_local_parameters()
#        for parameter in sorted(local_parameters):
#            print self.local_parameters[parameter], local_parameters[parameter]
#            
#        os.system('CopasiUI {}'.format(self.copasi_file))
        
    def test_local_k1s(self):
        k1s = [i for i in self.local_parameters if 'k1' in i]
        print kls
        # shuffle(k1s)
        # old = dict(zip(k1s, [self.local_parameters[i] for i in k1s]))
        # new= dict(zip(k1s, [i*random() for i in range(1,len(k1s)+1)]))
        # print new
        # InsertParameters(self.copasi_file, parameter_dict=new)
        
#        os.system('CopasiUI {}'.format(self.copasi_file))
        
        
        
        
    def tearDown(self):
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__=='__main__':
    unittest.main()