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
site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.Tests import _test_base
import os, glob
import pandas
import unittest
from lxml import etree




class UnitsTests(_test_base._BaseTest):
    def setUp(self):
        super(UnitsTests, self).setUp()
        self.Model = PyCoTools.model.Model(self.copasi_file)

    def test_time_unit(self):
        self.assertEqual(self.Model.time, 's')

    def test_model_name(self):
        self.assertEqual(self.Model.name, 'New Model')


    def test_volume(self):
        self.assertEqual(self.Model.volume, 'ml')

    def test_quantity(self):
        self.assertEqual(self.Model.area, u'm\xb2')

    def test_length(self):
        self.assertEqual(self.Model.length, 'm')

    def test_avagadro(self):
        self.assertEqual(self.Model.avagadro, 6.022140857e+23)

    def test_model_key(self):
        self.assertEqual(self.Model.key, 'Model_3')


    # def test_metabolites(self):
    #     print self.Model.metabolites()
    def test_compartments(self):
        self.assertEqual(len(self.Model.compartments() ),2)

    def test_compartments2(self):
        self.assertTrueisinstance( [i for i in self.Model.compartments()], 2)



































if __name__ == '__main__':
    unittest.main()