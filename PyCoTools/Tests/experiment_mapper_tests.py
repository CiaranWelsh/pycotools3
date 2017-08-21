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
    12/03/2017

 Object:
'''


import site
# site.addsitedir(r'C:\Users\Ciaran\Documents\PyCoTools')
site.addsitedir(r'/home/b3053674/Documents/PyCoTools')

import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
import unittest
import glob
import os
import shutil
import pandas
from PyCoTools.Tests import _test_base
import re
from lxml import etree

class ExperimentMapperTests(_test_base._BaseTest):
    def setUp(self):
        super(ExperimentMapperTests, self).setUp()
        self.TC1 = PyCoTools.pycopi.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report1.txt')
        self.TC2 = PyCoTools.pycopi.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report2.txt')

    def test_experiment(self):
        E = PyCoTools.pycopi.ExperimentMapper(self.model, [self.TC1.report_name,
                                                           self.TC2.report_name])

        self.model = E.model
        self.model.open()
        # exp = E.create_experiment(0)
        # print etree.tostring(exp, pretty_print=True)
        # for i in exp:
        #     for j in i:
        #         for k in j:
        #             print k.tag
        #             print k.attrib
        # self.model = E.model
        # self.model.save()

        # self.model.open()
if __name__=='__main__':
    unittest.main()