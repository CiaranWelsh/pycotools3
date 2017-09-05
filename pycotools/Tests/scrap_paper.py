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
# site.addsitedir(r'C:\Users\Ciaran\Documents\pycotools')
site.addsitedir(r'/home/b3053674/Documents/pycotools')

import pycotools
from pycotools.Tests import test_models
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


f = r'/home/b3053674/Documents/pycotools/pycotools/Tests/test_model.cps'


model = pycotools.model.Model(f)

TC1 = pycotools.tasks.TimeCourse(model, end=1000, step_size=100,
                                      intervals=10, report_name='report1.txt')

pycotools.misc.correct_copasi_timecourse_headers(TC1.report_name)
## add some noise
data1 = pycotools.misc.add_noise(TC1.report_name)

## remove the data
os.remove(TC1.report_name)

## rewrite the data with noise
data1.to_csv(TC1.report_name, sep='\t')

MPE = pycotools.tasks.MultiParameterEstimation(
    model,
    TC1.report_name,
    copy_number=2,
    pe_number=8,
    method='genetic_algorithm',
    population_size=10,
    number_of_generations=10,
    results_directory='test_mpe')

MPE.write_config_file()
MPE.setup()
# MPE.run()


p = viz.Parse(MPE)














































