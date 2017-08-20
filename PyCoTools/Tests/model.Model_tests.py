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




class ModelTests(_test_base._BaseTest):
    def setUp(self):
        super(ModelTests, self).setUp()
        self.Model = PyCoTools.model.Model(self.copasi_file)

    def test_time_unit(self):
        self.assertEqual(self.Model.time_unit, 's')

    def test_model_name(self):
        self.assertEqual(self.Model.name, 'New Model')

    def test_volume(self):
        self.assertEqual(self.Model.volume_unit, 'ml')

    def test_quantity(self):
        self.assertEqual(self.Model.area_unit, u'm\xb2')

    def test_length(self):
        self.assertEqual(self.Model.length_unit, 'm')

    def test_avagadro(self):
        self.assertEqual(self.Model.avagadro, 6.022140857e+23)

    def test_model_key(self):
        self.assertEqual(self.Model.key, 'Model_3')

    def test_reference(self):
        self.assertTrue('CN=Root,Model=New Model', self.model.reference)

    def test_metabolites(self):
        self.assertEqual(len(self.Model.metabolites), 3)

    def test_metabolites(self):
        for i in self.Model.metabolites:
            self.assertTrue(isinstance(i, PyCoTools.model.Metabolite))

    def test_compartments(self):
        self.assertEqual(len(self.Model.compartments() ),2)

    def test_global_quantities(self):
        # print self.Model.global_quantities()
        self.assertEqual(len(self.Model.global_quantities), 3)

    def test_local_parameters(self):
        '''
        Currently giving the wrong keys
        :return:
        '''
        self.assertTrue(len(self.Model.local_parameters), 3)
    #
    def test_local_parameters2(self):
        [self.assertTrue(isinstance(i, PyCoTools.model.LocalParameter) ) for (j,i) in self.Model.local_parameters.items() ]

    def test_local_parameters3(self):
        keys = self.Model.local_parameters.keys()
        keys_in_local_parameters = sorted(['reaction_name', 'name', 'value', 'simulationType', 'kwargs', 'type',
                                           'allowed_properties', 'key'])
        # self.assertListEqual(sorted(self.Model.local_parameters[keys[0]].__dict__.keys(), keys_in_local_parameters  )  )
        self.assertListEqual(sorted(self.Model.local_parameters[keys[0]].__dict__.keys()), keys_in_local_parameters)

    def test_functions(self):
        self.assertTrue(len(self.Model.functions), 2)

    def test_functions2(self):
        [self.assertTrue(isinstance(i, PyCoTools.model.Function) for i in self.Model.functions) ]

    def test_number_of_reactions(self):
        self.assertEqual(self.Model.number_of_reactions, 4)


    # def test_reactions(self):
    #     self.assertEqual(len( self.Model.reactions() ), 4)


    def test_xml(self):
        self.assertTrue(isinstance(self.Model.xml, etree._Element))

































if __name__ == '__main__':
    unittest.main()