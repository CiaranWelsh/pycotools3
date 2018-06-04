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
site.addsitedir('C:\\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.Tests import _test_base
import os, glob
import pandas
import unittest
from lxml import etree




class ReactionTests(_test_base._BaseTest):
    def setUp(self):
        super(ReactionTests, self).setUp()
        self.nuc = PyCoTools.model.Compartment(name='nuc', key='compartment_1',
                                          value=5, type='fixed')
        self.A = PyCoTools.model.Metabolite(name='A', compartment=self.nuc, concentration=10)
        self.B = PyCoTools.model.Metabolite(name='B', compartment=self.nuc, concentration=0)
        self.mass_action = PyCoTools.model.Function(name='MassAction', type='MassAction',
                                               reversible=False, key=1)
        self.k1 = PyCoTools.model.LocalParameter(name='k1',key=1, value=10)

        self.reaction = PyCoTools.model.Reaction(name='A2B', reactants=self.A,
                                                 products=self.B, rate_law=self.mass_action,
                                                 parameters=self.k1, key='reaction_1')

    def test_name(self):
        self.assertEqual(self.reaction.name, 'A2B')

    def test_key(self):
        self.assertEqual(self.reaction.key, 'reaction_1')

    def test_reactants(self):
        self.assertEqual(self.reaction.reactants, self.A)

    def test_products(self):
        self.assertEqual(self.reaction.products, self.B)

    def test_rate_law(self):
        self.assertEqual(self.reaction.rate_law, self.mass_action)

    def test_parameter(self):
        self.assertEqual(self.reaction.parameters, self.k1)








if __name__=='__main__':
    unittest.main()

















