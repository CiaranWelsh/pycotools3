# -*- coding: utf-8 -*-
"""
 This file is part of pycotools.

 pycotools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pycotools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with pycotools.  If not, see <http://www.gnu.org/licenses/>.


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
 
"""

import pickle
import site
site.addsitedir('/home/b3053674/Documents/pycotools')
# site.addsitedir('C:\Users\Ciaran\Documents\pycotools')
import pycotools
from pycotools.Tests import test_models
import unittest
import glob
import os
import shutil 
import pandas
from pycotools.Tests import _test_base
from random import shuffle, random
from pycotools.model import InsertParameters



class InsertParametersTests(_test_base._BaseTest):
    def setUp(self):
        super(InsertParametersTests, self).setUp()
        self.param_dct = {'A': 5,
                          'B2C': 6,
                          '(B2C).k2': 7}
        self.I = pycotools.model.InsertParameters(self.model,
                                                   parameter_dict=self.param_dct)

    def test_insert_dct_local(self):
        self.model = self.I.insert_locals()
        # self.model.save()
        self.model.open()
        # new_model =  pycotools.model.Model(self.model.copasi_file)
        # print pandas.concat([i.to_dict() for i in new_model.local_parameters])
        # df= pandas.concat([i.to_df() for i in new_model.local_parameters], axis=1)
        # print new_model.open()
        # print df
        # print new_model.local_parameters[0].__dict__



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__=='__main__':
    unittest.main()