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
from PyCoTools.Tests import base_tests
import subprocess




class CopasiMLParserTests(base_tests._BaseTest):
    def setUp(self):
        super(RunMultiplePETests, self).setUp()
        

    def test_file_was_written(self):
        """
        Test that the model string can be correctly written to file
        :return:
        """
        self.assertTrue(os.path.isfile(self.copasi_file))

    def test_CoapsiSE_is_set_up(self):
        """
        A test that the command 'CoapsiSE' does indeed point
        to the Copasi simulation engine
        :return:
        """
        worked = False
        try:
            subprocess.call('CopasiSE', shell = True)
            worked = True
        except:
            Exception('The command \'CopasiSE\' did not work. Ensure your PATH environment variable includes the copasi bin directory')
        self.assertTrue(worked)

    def test_file_is_executable(self):
        """
        Test that the can be run using CopasiSEfile
        :return:
        """
        worked = False
        try:
            subprocess.call('CopasiSE {}'.format(self.copasi_file), shell=True)
            worked = True
        except:
            Exception('Test model did not run with CopasiSE')
        self.assertTrue(worked)


#
if __name__ == '__main__':
    unittest.main()
