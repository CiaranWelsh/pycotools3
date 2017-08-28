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

# site.addsitedir('/home/b3053674/Documents/PyCoTools')
site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
import unittest
import glob
import os
import shutil
import pandas
from PyCoTools.Tests import _test_base
from random import shuffle, random
from PyCoTools.pycopi import InsertParameters


class KeyFactoryTests(_test_base._BaseTest):
    def setUp(self):
        super(KeyFactoryTests, self).setUp()

    def test_metabolite_key(self):
        KF = PyCoTools.model.KeyFactory(self.model, type='metabolite')
        key = KF.generate()
        metabolite_keys = [i.key for i in self.model.metabolites]
        x = True
        if key in metabolite_keys:
            x = False
        self.assertTrue(x)

    def test_compartment_key(self):
        KF = PyCoTools.model.KeyFactory(self.model, type='compartment')
        key = KF.generate()
        compartment_keys = [i.key for i in self.model.compartments]
        x = True
        print key
        if key in compartment_keys:
            x = False
        self.assertTrue(x)



if __name__=='__main__':
    unittest.main()