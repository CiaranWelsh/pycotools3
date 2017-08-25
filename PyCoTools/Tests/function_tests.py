#-*-coding: utf-8 -*-
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


 $Author: Ciaran Welsh

Module that tests the operations of the _Base base test

"""

import site
# site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
site.addsitedir(r'/home/b3053674/Documents/PyCoTools')

import PyCoTools
from PyCoTools.Tests import _test_base
import os, glob
import pandas
import unittest
from lxml import etree




class FunctionTests(_test_base._BaseTest):
    def setUp(self):
        super(FunctionTests, self).setUp()
        self.function = PyCoTools.model.Function(name='Mass Action', type='MassAction',key=1,
                                                 reversible=True)

    def test_name(self):
        self.assertEqual(self.function.name, 'Mass Action')

    def test_type(self):
        self.assertEqual(self.function.type, 'MassAction')

    def test_key(self):
        self.assertEqual(self.function.key, 1)

    def test_reversible(self):
        self.assertEqual(self.function.reversible, True)










if __name__=='__main__':
    unittest.main()

















