#-*-coding: utf-8 -*-
"""

 This file is part of pycotools3.

 pycotools3 is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pycotools3 is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with pycotools3.  If not, see <http://www.gnu.org/licenses/>.


 $Author: Ciaran Welsh


"""

import pycotools3

from Tests import _test_base
import unittest


class TestMetabolites(_test_base._BaseTest):
    def setUp(self):
        super(TestMetabolites, self).setUp()
        self.nucleus = pycotools3.model.Compartment(self.model,
                                                    name='Nuc', initial_value=5,
                                                    simulation_type='fixed', key='compartment_1')
        self.A = pycotools3.model.Metabolite(self.model,
                                             name='A',
                                             compartment=self.nucleus,
                                             concentration=5)
    def test_string_method(self):
        """

        :return:
        """
        ## TODO update string method tests
        pass
        # string =  "Metabolite(compartment=Compartment(key='compartment_1',  name='Nuc',  type='fixed',  value=5), concentration=5, name='A')"
        # self.assertEqual(string, self.A.__str__())

    def test_error(self):
        """
        test that Metabolite raises error if
        neither particle number or concentration
        is called.

        Learn how to do this when you have internet
        :return:
        """
        pass

    def test_name(self):
        self.assertEqual(self.A.name, 'A')

    def test_compartment(self):


        self.assertEqual(self.A.compartment, self.nucleus)

    def test_reference_initial(self):
        self.assertEqual(self.A.initial_reference, 'Vector=Metabolites[A],Reference=InitialConcentration')

    def test_reference_transient(self):
        self.assertEqual(self.A.transient_reference, 'Vector=Metabolites[A],Reference=Concentration')

    def test_particle_numbers(self):
        A = pycotools3.model.Metabolite(self.model,
                                        particle_numbers=10e23, compartment=self.nucleus)
        self.assertTrue(A.particle_numbers, 10e23)

    def test_concentration(self):
        """
        Test metabolite particle number to concentration conversion

        When concentration is changed, particle numbers change accordingly
        When particle number is changes, concenrtation is changes accordingly
        :param self:
        :return:
        """
        A = pycotools3.model.Metabolite(self.model,
                                        concentration=5,
                                        compartment=self.nucleus)
        self.assertTrue(A.concentration, 5)


class TestSubstrate(_test_base._BaseTest):
    def setUp(self):
        super(TestSubstrate, self).setUp()
        self.nucleus = pycotools3.model.Compartment(self.model, name='Nuc',
                                                    initial_value=5,
                                                    simulation_type='fixed', key='compartment_1')
        self.A = pycotools3.model.Substrate(self.model,
                                            name='A', compartment=self.nucleus,
                                            concentration=5)

    def test_name(self):
        self.assertEqual(self.A.name, 'A')

    def test_comp(self):
        self.assertEqual(self.A.compartment, self.nucleus)

    def test_concentration(self):
        self.assertEqual(self.A.concentration, 5)

    def test_to_substrate(self):
        # print self.B.to_substrate()
        self.assertTrue(isinstance(self.A.to_substrate(), pycotools3.model.Substrate))


class TestProduct(_test_base._BaseTest):
    def setUp(self):
        super(TestProduct, self).setUp()
        self.nucleus = pycotools3.model.Compartment(self.model,
                                                    name='Nuc',
                                                    initial_value=5,
                                                    simulation_type='fixed', key='compartment_1')
        self.B = pycotools3.model.Product(self.model,
                                          name='B', compartment=self.nucleus,
                                          concentration=60)

    def test_name(self):
        self.assertEqual(self.B.name, 'B')

    def test_comp(self):
        self.assertEqual(self.B.compartment, self.nucleus)

    def test_concentration(self):
        self.assertEqual(self.B.concentration, 60)

    ##todo put tests here for concentration and particle numbers




if __name__=='__main__':
    unittest.main()







