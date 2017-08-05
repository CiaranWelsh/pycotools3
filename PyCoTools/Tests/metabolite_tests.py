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


"""

import site
site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.Tests import _test_base
import os, glob
import pandas
import unittest



class TestMetabolites(_test_base._BaseTest):
    def setUp(self):
        super(TestMetabolites, self).setUp()
        self.nucleus = PyCoTools.pycopi.Compartment(name='Nuc', size=5)
        self.A = PyCoTools.pycopi.Metabolite(name='A', compartment=self.nucleus,
                                             concentration=5)
    def test_string_method(self):
        """

        :return:
        """
        string = "Metabolite(compartment=Compartment(name='Nuc',  size=5), concentration=5, name='A')"
        self.assertEqual(string, self.A.__str__())

    def test_name(self):
        self.assertEqual(self.A.name, 'A')

    def test_compartment(self):
        self.assertEqual(self.A.compartment, self.nucleus)

    def test_reference(self):
        self.assertEqual(self.A.reference, 'Vector=Metabolites[A]')

    # def test_particle_numbers(self):
    #     A = PyCoTools.pycopi.Metabolite(particle_number=10e23)
    #     self.assertTrue(A.particle_number, 10e23)
    #
    # def test_concentration(self):
    #     """
    #     Test metabolite particle number to concentration conversion
    #
    #     When concentration is changed, particle numbers change accordingly
    #     When particle number is changes, concenrtation is changes accordingly
    #     :param self:
    #     :return:
    #     """
    #     A = PyCoTools.pycopi.Metabolite(concentration=5)
    #     self.assertTrue(A.concentration, 5)
    #
    # def test_base(self):
    #     B = PyCoTools.pycopi._Kwargs(none=None)
    #     print B.none

if __name__=='__main__':
    unittest.main()







