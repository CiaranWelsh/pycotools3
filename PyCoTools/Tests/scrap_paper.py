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

#
# test_model = r'C:\Users\Ciaran\Documents\PyCoTools\PyCoTools\Tests\test_model.cps'
#
# test_report_name = os.path.join(os.path.dirname(test_model), 'testing_report.txt')
# model = PyCoTools.model.Model(test_model)
#
# test_ss_data = r'C:\Users\Ciaran\Documents\PyCoTools\PyCoTools\Tests\report4.txt'
#
# E = PyCoTools.pycopi.ExperimentMapper(model, test_ss_data, experiment_type='steadystate')
#
#

class CheckArgumentsMixin(Mixin):
    def check_integrity(self, allowed, given):
        for key in given:
            if key not in allowed:
                raise Exception('{} not in {}'.format(key, allowed))

class Base(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.update_properties(self.kwargs)
        super(Base, self).__init__()


    def update_properties(self, new_properties):
        for k in new_properties:
            try:
                getattr(self, k)
                # setattr(self, k, kwargs[k])
            except AttributeError:
                setattr(self, k, new_properties[k])
        ## now delete the new_properties in subclass to prevent it from clogging up self.__dict__


@mixin(CheckArgumentsMixin)
class A(Base):
    def __init__(self, **kwargs):
        super(A, self).__init__(**kwargs)

        ##class specific keyword arguments
        self.default_properties = {'a': 1,
                                   'b': 2}

        ## now update the class properties from defaults
        self.update_properties(self.default_properties)

        '''
        check the integrity of the user input
        (i.e. i'm enforcing the restriction that kwargs supplied by
        a user are predefined in the self.default_properties dict. 
        '''
        self.check_integrity(self.default_properties.keys(), kwargs.keys())

@mixin(CheckArgumentsMixin)
class B(A):
    def __init__(self, **kwargs):
        super(B, self).__init__(**kwargs)
        super(B, self).check_integrity()

        self.default_properties = {'c': 3,
                                   'd': 4}

        self.update_properties(self.default_properties)

base = Base()
print base.__dict__
##outputs: {'kwargs': {}}

a = A(a=4)
print a.__dict__
'''
output:
{'a': 4, 'default_properties': {'a': 1, 'b': 2}, 'b': 2, 'kwargs': {'a': 4}}
'''

b = B(d=5)
'''
output: 
Exception: d not in ['a', 'b'] #i.e. exception from check_integrity
'''













