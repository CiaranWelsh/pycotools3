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
site.addsitedir('/home/b3053674/Documents/PyCoTools')
# site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
import unittest
import glob
import os
import shutil 
import pandas
from PyCoTools.Tests import _test_base
import subprocess




class CopasiMLParserTests(_test_base._BaseTest):
    def setUp(self):
        super(CopasiMLParserTests, self).setUp()
        


#
if __name__ == '__main__':
    unittest.main()
