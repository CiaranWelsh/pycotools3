# -*- coding: utf-8 -*-
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


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
 
"""
import site
#site.addsitedir('/home/b3053674/Documents/PyCoTools')
site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.PyCoToolsTutorial import test_models
from PyCoTools.Tests import _test_base
import unittest
import glob
import os
import shutil 
import pandas
import random

#
class GetModelQuantitiesTests(_test_base._BaseTest):
    def setUp(self):
        super(GetModelQuantitiesTests, self).setUp()
        
        
    def test_get_local_parameters(self):
        """
        
        """
        sh = self.GMQ.get_local_parameters().shape
        self.assertEqual(sh, (3,5))
#        print self.GMQ.get_local_parameters()

    def test_get_compartments(self):
        sh = self.GMQ.get_compartments().shape
        self.assertEqual(sh, (2,3))

    def test_get_metabolites(self):
        """

        :return:
        """
        sh = self.GMQ.get_metabolites().shape
        self.assertEqual(sh, (3,4))

    def test_particle_to_conc_conversion1(self):
        particle_number = 6.022140857e+20
        vol_unit = 'ml'
        quantity_unit = 'mmol'
        conc = PyCoTools.pycopi.GetModelQuantities.convert_particles_to_molar(particle_number,
                                                                              quantity_unit,
                                                                              compartment_volume=1)
        self.assertAlmostEqual(round(conc,0), 1)

    def test_particle_to_conc_conversion2(self):
        particle_number = 6.022140857e+20
        vol_unit = 'ml'
        quantity_unit = 'nmol'
        conc = PyCoTools.pycopi.GetModelQuantities.convert_particles_to_molar(particle_number,
                                                                              quantity_unit,
                                                                              compartment_volume=1)
        self.assertAlmostEqual(round(conc,0), 1000000)


        # os.system('CopasiUI {}'.format(self.copasi_file))

    def test_get_global_quantities(self):
        """

        :return:
        """
        print self.GMQ.get_global_quantities()
        
if __name__ == '__main__':
    unittest.main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
