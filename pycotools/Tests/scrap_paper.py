# -*- coding: utf-8 -*-
'''
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
'''


import site
site.addsitedir(r'C:\Users\Ciaran\Documents\pycotools')
# site.addsitedir(r'/home/b3053674/Documents/pycotools')

import pycotools
from pycotools.pycotoolsTutorial import test_models
import unittest
import glob
import os
import shutil
import pandas
from pycotools.Tests import _test_base
import re
from lxml import etree
from mixin import Mixin, mixin

import contextlib


f = r'C:\Users\Ciaran\Documents\pycotools\pycotools\Tests\test_model.cps'
f2 = r'C:\Users\Ciaran\Documents\pycotools\pycotools\Tests\test_model2.cps'


model = pycotools.model.Model(f)
metab = pycotools.model.Metabolite(model, name='X',
                                   concentration=1000)

model = model.add('metabolite', metab)

model = model.set_metabolite('X', 1234, attribute='concentration')

for i in model.metabolites:
    print i
# model.open()


















































