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
site.addsitedir('/home/b3053674/Documents/PyCoTools')

import PyCoTools
from PyCoTools.Tests import _test_base

import os, glob
import pandas
import unittest
from lxml import etree




class ModelTests(_test_base._BaseTest):
    def setUp(self):
        super(ModelTests, self).setUp()
        self.model = PyCoTools.model.Model(self.copasi_file)

    def test_time_unit(self):
        self.assertEqual(self.model.time_unit, 's')

    def test_model_name(self):
        self.assertEqual(self.model.name, 'New Model')

    def test_volume(self):
        self.assertEqual(self.model.volume_unit, 'ml')

    def test_quantity(self):
        self.assertEqual(self.model.area_unit, u'm\xb2')

    def test_length(self):
        self.assertEqual(self.model.length_unit, 'm')

    def test_avagadro(self):
        self.assertEqual(self.model.avagadro, 6.022140857e+23)

    def test_model_key(self):
        self.assertEqual(self.model.key, 'Model_3')

    def test_reference(self):
        self.assertTrue('CN=Root,Model=New Model', self.model.reference)

    def test_metabolites(self):
        self.assertEqual(len(self.model.metabolites), 3)

    def test_metabolites2(self):
        for i in self.model.metabolites:
            self.assertTrue(isinstance(i, PyCoTools.model.Metabolite))

    def test_metabolites3(self):
        check = True
        for i in self.model.metabolites:
            try:
                i.simulation_type
            except AttributeError:
                check = False
        self.assertTrue(check)

    def test_compartments(self):
        self.assertEqual(len(self.model.compartments ),2)

    def test_global_quantities(self):
        # print self.model.global_quantities()
        self.assertEqual(len(self.model.global_quantities), 3)

    def test_global_quantities2(self):
        check = True
        for i in self.model.global_quantities:
            try:
                i.simulation_type
            except AttributeError:
                check = False
        self.assertTrue(check)

    def test_local_parameters(self):
        '''
        Currently giving the wrong keys
        :return:
        '''
        self.assertTrue(len(self.model.local_parameters), 3)
    #
    def test_local_parameters2(self):
        for i in self.model.local_parameters:
            self.assertTrue(isinstance(i, PyCoTools.model.LocalParameter))

    def test_local_parameters3(self):
        check = True
        for i in self.model.local_parameters:
            try:
                i.simulation_type
            except AttributeError:
                check = False
        self.assertTrue(check)

    def test_local_parameters4(self):
        """

        :return:
        """

        L= PyCoTools.model.LocalParameter(name='k1', reaction_name='v1')
        self.assertEqual(L.global_name, '(v1).k1')

    def test_local_parameters5(self):
        L= PyCoTools.model.LocalParameter(name='k1', reaction_name='v1')
        self.assertTrue('global_name' in L.__dict__.keys())

    def test_functions(self):
        self.assertTrue(len(self.model.functions), 2)

    def test_functions2(self):
        [self.assertTrue(isinstance(i, PyCoTools.model.Function) for i in self.model.functions) ]

    def test_number_of_reactions(self):
        self.assertEqual(self.model.number_of_reactions, 4)


    # def test_reactions(self):
    #     self.assertEqual(len( self.model.reactions() ), 4)


    def test_xml(self):
        self.assertTrue(isinstance(self.model.xml, etree._Element))


    def test_concentration_calculation(self):
        """

        :return:
        """
        print self.model.metabolites
        # self.model.open()


    def test_convert_particles_to_molar(self):
        """
        6.022140857e+20 = 1mmol/ml
        :return:
        """
        particles = 6.022140857e+20
        conc = 1
        self.assertAlmostEqual(self.model.convert_particles_to_molar(particles, 'mmol', 1), 1)

    def test_convert_to_molar_to_particles(self):
        """
        1mmol/ml = 6.022140857e+20
        :return:
        """
        particles = 6.022140857e+20
        conc = 1
        self.assertAlmostEqual(self.model.convert_molar_to_particles(conc, 'mmol', 1), particles)


    def test_metabolites(self):
        """

        :return:
        """
        print self.model.global_quantities
        # print self.model.local_parameters






























if __name__ == '__main__':
    unittest.main()