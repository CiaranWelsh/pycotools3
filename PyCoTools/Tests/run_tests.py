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
    19-08-2017
 '''
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
from lxml import etree


class RunTests(_test_base._BaseTest):
    def setUp(self):
        super(RunTests, self).setUp()

    def test(self):
        print PyCoTools.model.Model(self.model)
        # R=PyCoTools.pycopi.Run(self.copasi_file)
        # print R.model
        # model = R.set_task()
        # print model
        # model.save(self.copasi_file)
        # new_model = PyCoTools.pycopi.CopasiMLParser(self.copasi_file).copasiML
        # print new_model



if __name__=='__main__':
    unittest.main()





















































