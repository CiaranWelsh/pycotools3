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
# site.addsitedir('/home/b3053674/Documents/PyCoTools')

import PyCoTools
from PyCoTools.Tests import _test_base

import os, glob
import pandas
import unittest
from lxml import etree
from collections import OrderedDict



class ModelTests(_test_base._BaseTest):
    def setUp(self):
        super(ModelTests, self).setUp()
        self.model = PyCoTools.model.Model(self.copasi_file)

    # def test_time_unit(self):
    #     self.assertEqual(self.model.time_unit, 's')
    #
    # def test_model_name(self):
    #     self.assertEqual(self.model.name, 'New Model')
    #
    # def test_volume(self):
    #     self.assertEqual(self.model.volume_unit, 'ml')
    #
    # def test_quantity(self):
    #     self.assertEqual(self.model.area_unit, u'm\xb2')
    #
    # def test_length(self):
    #     self.assertEqual(self.model.length_unit, 'm')
    #
    # def test_avagadro(self):
    #     self.assertEqual(self.model.avagadro, 6.022140857e+23)
    #
    # def test_model_key(self):
    #     self.assertEqual(self.model.key, 'Model_3')
    #
    # def test_reference(self):
    #     self.assertTrue('CN=Root,Model=New Model', self.model.reference)
    #
    # def test_metabolites(self):
    #     self.assertEqual(len(self.model.metabolites), 3)
    #
    # def test_metabolites2(self):
    #     for i in self.model.metabolites:
    #         self.assertTrue(isinstance(i, PyCoTools.model.Metabolite))
    #
    # def test_metabolites3(self):
    #     check = True
    #     for i in self.model.metabolites:
    #         try:
    #             i.simulation_type
    #         except AttributeError:
    #             check = False
    #     self.assertTrue(check)
    #
    # def test_compartments(self):
    #     self.assertEqual(len(self.model.compartments ),2)
    #
    # def test_global_quantities(self):
    #     # print self.model.global_quantities()
    #     self.assertEqual(len(self.model.global_quantities), 3)
    #
    # def test_global_quantities2(self):
    #     check = True
    #     for i in self.model.global_quantities:
    #         try:
    #             i.simulation_type
    #         except AttributeError:
    #             check = False
    #     self.assertTrue(check)
    #
    # def test_local_parameters(self):
    #     '''
    #     Currently giving the wrong keys
    #     :return:
    #     '''
    #     self.assertTrue(len(self.model.local_parameters), 3)
    # #
    # def test_local_parameters2(self):
    #     for i in self.model.constants:
    #         self.assertTrue(isinstance(i, PyCoTools.model.LocalParameter))
    #
    # def test_local_parameters3(self):
    #     check = True
    #     for i in self.model.constants:
    #         try:
    #             i.simulation_type
    #         except AttributeError:
    #             check = False
    #     self.assertTrue(check)
    #
    # def test_local_parameters4(self):
    #     """
    #
    #     :return:
    #     """
    #     k = PyCoTools.model.KeyFactory(self.model, type='constant').generate()
    #     L= PyCoTools.model.LocalParameter(self.model,
    #                                       key=k,
    #                                       name='k1', reaction_name='v1',
    #                                       global_name='(v1).k1')
    #     self.assertEqual(L.global_name, '(v1).k1')
    #
    # def test_local_parameters5(self):
    #     k = PyCoTools.model.KeyFactory(self.model, type='constant').generate()
    #     L= PyCoTools.model.LocalParameter(self.model,
    #                                       key=k,
    #                                       name='k1',
    #                                       reaction_name='v1')
    #     self.assertTrue('global_name' in L.__dict__.keys())
    #
    # # def test_functions(self):
    # #     self.assertTrue(len(self.model.functions), 2)
    #
    # def test_functions2(self):
    #     [self.assertTrue(isinstance(i, PyCoTools.model.Function) for i in self.model.functions) ]
    #
    # def test_number_of_reactions(self):
    #     self.assertEqual(self.model.number_of_reactions, 4)
    #
    #
    # # def test_reactions(self):
    # #     self.assertEqual(len( self.model.reactions() ), 4)
    #
    #
    # def test_xml(self):
    #     self.assertTrue(isinstance(self.model.xml, etree._Element))
    #
    #
    # # def test_concentration_calculation(self):
    # #     """
    # #
    # #     :return:
    # #     """
    # #     print self.model.metabolites
    # #     # self.model.open()
    #
    #
    # def test_convert_particles_to_molar(self):
    #     """
    #     6.022140857e+20 = 1mmol/ml
    #     :return:
    #     """
    #     particles = 6.022140857e+20
    #     conc = 1
    #     self.assertAlmostEqual(self.model.convert_particles_to_molar(particles, 'mmol', 1), 1)
    #
    # def test_convert_to_molar_to_particles(self):
    #     """
    #     1mmol/ml = 6.022140857e+20
    #     :return:
    #     """
    #     particles = 6.022140857e+20
    #     conc = 1
    #     self.assertAlmostEqual(self.model.convert_molar_to_particles(conc, 'mmol', 1), particles)
    #
    # def test_set_name(self):
    #     """
    #
    #     :return:
    #     """
    #     self.model.name = 'new_name'
    #     self.assertEqual(self.model.name, 'new_name')
    # # def test_metabolites(self):
    # #     """
    # #
    # #     :return:
    # #     """
    # #     print self.model.global_quantities
    # #     # print self.model.local_parameters
    #
    # def test_create_metabolite(self):
    #     """
    #
    #     :return:
    #     """
    #     metab = PyCoTools.model.Metabolite(self.model, name='F', particle_number=25,
    #                                        compartment=self.model.compartments[0])
    #     self.model = self.model.add_metabolite(metab)
    #     check = False
    #     for i in self.model.metabolites:
    #         if i.name == 'F':
    #             check = True
    #     self.assertTrue(check)
    #
    # def test_change_states(self):
    #     """
    #
    #     :return:
    #     """
    #     state_numbers = [0.0, 1, 2, 3, 3, 4, 5, 6, 7]
    #     self.model.states = state_numbers
    #     self.assertListEqual([float(i) for i in state_numbers],
    #                          [float(i) for i in self.model.states.values()])
    #
    # def test_get_metabolite_by_key(self):
    #     """
    #
    #     :return:
    #     """
    #     metab = self.model.get('metabolite', 'Metabolite_1', by='key')
    #     self.assertEqual(metab.name, 'A')
    #
    #
    # def test_get_metbolite_by_name(self):
    #     """
    #
    #     :return:
    #     """
    #     metab = self.model.get('metabolite', 'A', by='name')
    #     self.assertEqual(metab.name, 'A')
    #
    # def test_get_compartment_by_name(self):
    #     res = self.model.get('compartment', 'nuc', by='name')
    #     self.assertEqual(res.name, 'nuc')
    #
    # def get_local_parameter_by_name(self):
    #     res = self.model.get('local_parameter', '(B2C).k1', by='name')
    #     self.assertEqual(res.name, '(B2C).k1')
    #
    # # def test_remove_metabolite(self):
    # #     """
    # #
    # #     :return:
    # #     """
    # #     ##first add a metabolite to model
    # #     self.model = self.model.add_metabolite(name='F')
    # #     self.model.remove_metabolite('F', by='name')
    #
    #
    # def test_remove_state(self):
    #     """
    #
    #     :return:
    #     """
    #     ##TODO fix concentration attribute in set_metabolites
    #     metab = PyCoTools.model.Metabolite(self.model, name='F', particle_number=25,
    #                                        compartment=self.model.compartments[0])
    #     self.model = self.model.add_metabolite(metab)
    #     F = self.model.get('metabolite', 'F', by='name')
    #     self.model = self.model.remove_metabolite('F', by='name')
    #     new_F = self.model.get('metabolite', 'F', by='name')
    #     self.assertEqual(new_F, [])
    #
    # def test_add_compartment(self):
    #     """
    #
    #     :return:
    #     """
    #     comp = PyCoTools.model.Compartment(self.model,
    #                                        name='Medium', initial_value=6)
    #     compartment_model = self.model.add_compartment(comp)
    #     comp_filename = os.path.join(os.path.dirname(self.model.copasi_file), 'comp_model.cps')
    #     compartment_model.save(comp_filename)
    #
    #
    # def test_remove_compartment(self):
    #     """
    #
    #     :return:
    #     """
    #     comp = PyCoTools.model.Compartment(self.model,
    #                                        name='Medium', initial_value=6)
    #     self.model = self.model.add_compartment(comp)
    #     comp = self.model.get('compartment', 'Medium', 'name')
    #     assert comp != []
    #     self.model = self.model.remove_compartment(comp.name, by='name')
    #     comp = self.model.get('compartment', 'Medium', 'name')
    #     self.assertEqual(comp, [])
    #
    # def test_add_global_quantity(self):
    #     """
    #
    #     :return:
    #     """
    #     global_quantity = PyCoTools.model.GlobalQuantity(self.model, name='NewGlobal',
    #                                                      initial_value=5)
    #     new_model = self.model.add_global_quantity(global_quantity)
    #
    #     new_global = new_model.get('global_quantity', 'NewGlobal',
    #                                by='name')
    #     self.assertEqual(new_global.name, 'NewGlobal')
    #
    #
    # def test_remove_global_quantities(self):
    #     """
    #
    #     :return:
    #     """
    #     global_quantity = PyCoTools.model.GlobalQuantity(self.model, name='NewGlobal',
    #                                                      initial_value=5)
    #     new_model = self.model.add_global_quantity(global_quantity)
    #     new_global = new_model.get('global_quantity', 'NewGlobal')
    #     assert new_global != []
    #     new_model = new_model.remove_global_quantity('NewGlobal', by='name')
    #     new_global = new_model.get('global_quantity', 'NewGlobal')
    #     self.assertEqual(new_global, [])
    #
    #
    # def test_get_list_of_call_parameters(self):
    #     for i in self.model.parameter_descriptions:
    #         self.assertTrue(isinstance(i, PyCoTools.model.ParameterDescription))
    #
    #
    # def test_mass_action_class(self):
    #     ma = PyCoTools.model.MassAction(self.model, reversible=True)
    #     self.assertEqual(ma.expression, 'k1*PRODUCT&lt;substrate_i>-k2*PRODUCT&lt;product_j>')
    # #
    #
    # def test_add_mass_action(self):
    #     ma = PyCoTools.model.MassAction(self.model, reversible=False)
    #     self.model = self.model.add_function(ma)
    #     ##todo find better test condition
    #
    #
    # def test_create_parameter_description_key(self):
    #     KF = PyCoTools.model.KeyFactory(self.model, type='function_parameter')
    #     self.assertEqual(len(KF.create_function_parameter_key(n=4)), 4)
    #
    # def test_function_user_defined1(self):
    #     """
    #     make sure that roles are converted into parameter descriptions
    #     (function parameters)
    #     :return:
    #     """
    #     fun = PyCoTools.model.Function(self.model, name='new_funct',
    #                                    expression='K*M*S',
    #                                    roles={'K': 'parameter',
    #                                           'M': 'modifier',
    #                                           'S': 'substrate'})
    #
    #     for i in fun.list_of_parameter_descriptions:
    #         self.assertTrue(isinstance(i, PyCoTools.model.ParameterDescription))
    #
    # def test_add_function(self):
    #     """
    #
    #     :return:
    #     """
    #     fun = PyCoTools.model.Function(self.model, name='new_funct',
    #                                    expression='K*M*S',
    #                                    roles={'K': 'parameter',
    #                                           'M': 'modifier',
    #                                           'S': 'substrate'})
    #     self.model =  self.model.add_function(fun)
    #     self.model.save()
    #     for i in self.model.xml.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
    #             for j in i:
    #                 if j.attrib['name'] == fun.name:
    #                     self.assertEqual(j.attrib['name'], fun.name)
    #
    #
    #
    # def test_remove_functions(self):
    #     fun = PyCoTools.model.Function(self.model, name='new_funct',
    #                                    expression='K*M*S',
    #                                    roles={'K': 'parameter',
    #                                           'M': 'modifier',
    #                                           'S': 'substrate'})
    #     self.model =  self.model.add_function(fun)
    #     self.model.save()
    #     self.model = self.model.remove_function('new_funct', by='name')
    #     for i in self.model.xml.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
    #             for j in i:
    #                 self.assertNotEqual(j.attrib['name'], fun.name)
    #
    # def test_translator(self):
    #     trans = PyCoTools.model.Translator(self.model, '-> B')
    #     self.assertTrue(isinstance(trans.all_components, list))
    #
    # def test_translator2(self):
    #     trans = PyCoTools.model.Translator(self.model, 'A -> B')
    #     self.assertTrue(isinstance(trans.all_components, list))
    #
    # def test_translator3(self):
    #     trans = PyCoTools.model.Translator(self.model, 'A + A + B -> B; C D')
    #     self.assertTrue(isinstance(trans.all_components, list))
    #
    # def test_translator4(self):
    #     trans = PyCoTools.model.Translator(self.model, 'B ->')
    #     self.assertTrue(isinstance(trans.all_components, list))
    #
    #
    # def test_local_parameters(self):
    #     self.assertEqual(len(self.model.constants), 5)
    #
    # def test_key_factory_constant(self):
    #     """
    #
    #     :return:
    #     """
    #     p =PyCoTools.model.KeyFactory(self.model, type='constant').generate(2)
    #     self.assertEqual(len(p), 2)
    #
    #
    # def test_add_reaction1(self):
    #     """
    #     Test the reaction name is correct
    #     :return:
    #     """
    #     r = PyCoTools.model.Reaction(self.model,
    #                                  name='fake_reaction',
    #                                  expression='A + B + C + D -> E + F',
    #                                  rate_law='k*A*B*C/D')
    #     self.model.add_reaction(r)
    #     self.model.save()
    #     xml = PyCoTools.pycopi.CopasiMLParser(self.model.copasi_file).xml
    #
    #     boolean = False
    #     for i in xml.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    #             for j in i:
    #                 if j.attrib['name'] == 'fake_reaction':
    #                     boolean = True
    #
    #     self.assertTrue(boolean)
    #
    # def test_add_reaction2(self):
    #     """
    #     Test correct number of substrates
    #     :return:
    #     """
    #     r = PyCoTools.model.Reaction(self.model,
    #                                  name='fake_reaction',
    #                                  expression='A + B + C + D -> E + F',
    #                                  rate_law='k*A*B*C/D')
    #     self.model.add_reaction(r)
    #     self.model.save()
    #     xml = PyCoTools.pycopi.CopasiMLParser(self.model.copasi_file).xml
    #
    #     boolean = False
    #     for i in xml.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    #             for j in i:
    #                 if j.attrib['name'] == 'fake_reaction':
    #                     for k in j:
    #                         if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
    #                             self.assertTrue(len(k)==4)
    #
    # def test_add_reaction3(self):
    #     """
    #     Test correct number of products
    #     :return:
    #     """
    #     r = PyCoTools.model.Reaction(self.model,
    #                                  name='fake_reaction',
    #                                  expression='A + B + C + D -> E + F',
    #                                  rate_law='k*A*B*C/D')
    #     self.model.add_reaction(r)
    #     self.model.save()
    #     xml = PyCoTools.pycopi.CopasiMLParser(self.model.copasi_file).xml
    #
    #     boolean = False
    #     for i in xml.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    #             for j in i:
    #                 if j.attrib['name'] == 'fake_reaction':
    #                     for k in j:
    #                         if k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
    #                             self.assertTrue(len(k)==2)
    #
    # def test_add_reaction4(self):
    #     """
    #     Test correct number of products
    #     :return:
    #     """
    #     r = PyCoTools.model.Reaction(self.model,
    #                                  name='fake_reaction',
    #                                  expression='A + B + C + D -> E + F',
    #                                  rate_law='k*A*B*C/D')
    #     self.model.add_reaction(r)
    #     self.model.save()
    #     xml = PyCoTools.pycopi.CopasiMLParser(self.model.copasi_file).xml
    #
    #     boolean = False
    #     for i in xml.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    #             for j in i:
    #                 if j.attrib['name'] == 'fake_reaction':
    #                     for k in j:
    #                         if k.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
    #                             self.assertTrue(len(k) == 1)
    #
    # def test_add_reaction5(self):
    #     """
    #     Test different reaction
    #     :return:
    #     """
    #     r = PyCoTools.model.Reaction(self.model,
    #                                  name='fake_reaction2',
    #                                  expression='A + F + irs -> ; G',
    #                                  rate_law='k*A*B*C/D')
    #     self.model.add_reaction(r)
    #     self.model.save()
    #     xml = PyCoTools.pycopi.CopasiMLParser(self.model.copasi_file).xml
    #
    #     boolean = False
    #     for i in xml.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    #             for j in i:
    #                 if j.attrib['name'] == 'fake_reaction2':
    #                     for k in j:
    #                         if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
    #                             self.assertTrue(len(k) == 3)
    #
    # def test_add_reaction6(self):
    #     """
    #     Test different reaction
    #     :return:
    #     """
    #     r = PyCoTools.model.Reaction(self.model,
    #                                  name='fake_reaction2',
    #                                  expression='A + F + irs -> ; G',
    #                                  rate_law='k*A*F/irs+G')
    #     self.model = self.model.add_reaction(r)
    #     self.model.save()
    #     xml = PyCoTools.pycopi.CopasiMLParser(self.model.copasi_file).xml
    #     boolean = False
    #     for i in xml.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    #             for j in i:
    #                 if j.attrib['name'] == 'fake_reaction2':
    #                     for k in j:
    #                         if k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
    #                             self.assertTrue(len(k) == 0)
    #
    #
    # def test_translater_again(self):
    #     trans = PyCoTools.model.Translator(self.model, 'A + F + irs -> ;G')
    #     self.assertEqual(trans.products, [])
    #
    # def test_translater_again2(self):
    #     trans = PyCoTools.model.Translator(self.model, 'A ->')
    #     self.assertEqual(trans.products, [])
    #
    # def test_translater_again2(self):
    #     trans = PyCoTools.model.Translator(self.model, 'A -> B; C ')
    #     self.assertEqual(trans.modifiers[0].name, 'C')
    #     # self.assertEqual(trans.products, [])
    #
    #
    # def test_set_global_quantity(self):
    #     """
    #
    #     :return:
    #     """
    #     ## add new global
    #     glob = PyCoTools.model.GlobalQuantity(self.model,
    #                                           name='X')
    #
    #     self.model = self.model.add_global_quantity(glob)
    #     self.model = self.model.set('global_quantity', 'X', 55)
    #     x = self.model.get('global_quantity', 'X')
    #     self.assertEqual(float(x.initial_value), 55.0)
    #
    #
    # def test_remove_method_global(self):
    #     """
    #
    #     :return:
    #     """
    #     glob = PyCoTools.model.GlobalQuantity(self.model, name='X')
    #     self.model = self.model.add_global_quantity(glob)
    #     assert 'X' in [i.name for i in self.model.global_quantities]
    #     self.model = self.model.remove('global_quantity', 'X')
    #     boolean = True
    #     for i in self.model.global_quantities:
    #         if i.name == 'X':
    #             boolean = False
    #     self.assertTrue(boolean)
    #
    # def test_add_compartment(self):
    #     """
    #
    #     :return:
    #     """
    #     comp = PyCoTools.model.Compartment(self.model, name='X')
    #     self.model = self.model.add_compartment(comp)
    #     boolean = False
    #
    #     for i in self.model.compartments:
    #         if i.name == 'X':
    #             boolean = True
    #     self.assertTrue(boolean)
    #
    # def test_remove_method_compartment(self):
    #     """
    #
    #     :return:
    #     """
    #     comp = PyCoTools.model.Compartment(self.model, name='Cell')
    #     self.model = self.model.add_compartment(comp)
    #     assert 'Cell' in [i.name for i in self.model.compartments]
    #     self.model = self.model.remove('compartment', 'Cell')
    #     boolean = True
    #     for i in self.model.compartments:
    #         if i.name == 'X':
    #             boolean = False
    #     self.assertTrue(boolean)


    def test_remove_raction(self):
        """
        Test different reaction
        :return:
        """
        r = PyCoTools.model.Reaction(self.model,
                                     name='fake_reaction2',
                                     expression='A + B -> C',
                                     rate_law='k*A*B')
        self.model = self.model.add_reaction(r)
        # self.model = self.model.remove_reaction('fake_reaction2', by='name')
        # # self.model = self.model.remove('reaction', 'fake_reaction2')
        self.model.save()
        #self.model.open()

        self.model.reactions
        # new_model = PyCoTools.pycopi.CopasiMLParser(self.model.copasi_file).xml
        # boolean = True
        # for i in new_model.iter():
        #     if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
        #         for j in i:
        #             if j.attrib['name'] == 'fake_reaction2':
        #                 boolean = False
        # self.assertTrue(boolean)




if __name__ == '__main__':
    unittest.main()