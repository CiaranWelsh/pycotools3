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
site.addsitedir(r'C:\Users\Ciaran\Documents\PyCoTools')
# site.addsitedir(r'/home/b3053674/Documents/PyCoTools')

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
from mixin import Mixin, mixin

import contextlib


f = r'C:\Users\Ciaran\Documents\PyCoTools\PyCoTools\Tests\test_model.cps'
f2 = r'C:\Users\Ciaran\Documents\PyCoTools\PyCoTools\Tests\test_model2.cps'


model = PyCoTools.model.Model(f)
metab = PyCoTools.model.Metabolite(model, name='X',
                                   concentration=1000)

model = model.add('metabolite', metab)

model = model.set_metabolite('X', 1234, attribute='concentration')

for i in model.metabolites:
    print i
# model.open()


















































