# -*-coding: utf-8 -*-
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


"""

import site

# site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
site.addsitedir('/home/b3053674/Documents/PyCoTools')

import PyCoTools

from PyCoTools.model import Compartment
from PyCoTools.Tests import _test_base
import os, glob
import pandas
import unittest


class TestCompartments(_test_base._BaseTest):
    def setUp(self):
        super(TestCompartments, self).setUp()
        self.comp = Compartment(name='Nucleus', value=5,
                                type='fixed', key='compartment_1')

    def test_checks(self):
        """
        Doesnot work at present.
        :return:
        """
        pass
        # with self.assertRaises(Exception):
        #     PyCoTools.pycopi.Compartments()

    def test_comp_name(self):
        self.assertEqual(self.comp.name, 'Nucleus')

    def test_comp_size(self):
        self.assertEqual(self.comp.value, 5)

    def test_compartment_str(self):
        ## TODO modify this test for updated compartment string
        pass
        # comp_str = "Compartment(key='compartment_1', name='Nucleus', type='fixed', value=5)"
        # self.assertEqual(comp_str, self.comp.__str__())

    def test_reference(self):
        ref = 'Vector=Compartments[Nucleus]'
        self.assertTrue(self.comp.reference == ref)


if __name__ == '__main__':
    unittest.main()
