#-*-coding: utf-8 -*-
"""

 This file is part of pycotools.

 pycotools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pycotools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with pycotools.  If not, see <http://www.gnu.org/licenses/>.


 $Author: Ciaran Welsh

Module that tests the operations of the _Base base test

"""

import site
# site.addsitedir('C:\Users\Ciaran\Documents\pycotools')
site.addsitedir('/home/b3053674/Documents/pycotools')

import pycotools
from pycotools.Tests import _test_base

import os, glob
import pandas
import unittest
from lxml import etree
from collections import OrderedDict



class ModelTests(_test_base._BaseTest):
    def setUp(self):
        super(ModelTests, self).setUp()
        self.model = pycotools.model.Model(self.copasi_file)

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
            self.assertTrue(isinstance(i, pycotools.model.Metabolite))

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
        for i in self.model.constants:
            self.assertTrue(isinstance(i, pycotools.model.LocalParameter))

    def test_local_parameters3(self):
        check = True
        for i in self.model.constants:
            try:
                i.simulation_type
            except AttributeError:
                check = False
        self.assertTrue(check)

    def test_local_parameters4(self):
        """

        :return:
        """
        k = pycotools.model.KeyFactory(self.model, type='constant').generate()
        L= pycotools.model.LocalParameter(self.model,
                                          key=k,
                                          name='k1', reaction_name='v1',
                                          global_name='(v1).k1')
        self.assertEqual(L.global_name, '(v1).k1')

    def test_local_parameters5(self):
        k = pycotools.model.KeyFactory(self.model, type='constant').generate()
        L= pycotools.model.LocalParameter(self.model,
                                          key=k,
                                          name='k1',
                                          reaction_name='v1')
        self.assertTrue('global_name' in L.__dict__.keys())

    # def test_functions(self):
    #     self.assertTrue(len(self.model.functions), 2)

    def test_functions2(self):
        [self.assertTrue(isinstance(i, pycotools.model.Function) for i in self.model.functions) ]

    def test_number_of_reactions(self):
        self.assertEqual(self.model.number_of_reactions, 4)


    # def test_reactions(self):
    #     self.assertEqual(len( self.model.reactions() ), 4)


    def test_xml(self):
        self.assertTrue(isinstance(self.model.xml, etree._Element))


    # def test_concentration_calculation(self):
    #     """
    #
    #     :return:
    #     """
    #     print self.model.metabolites
    #     # self.model.open()


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

    def test_set_name(self):
        """

        :return:
        """
        self.model.name = 'new_name'
        self.assertEqual(self.model.name, 'new_name')
    # def test_metabolites(self):
    #     """
    #
    #     :return:
    #     """
    #     print self.model.global_quantities
    #     # print self.model.local_parameters
    #
    def test_create_metabolite(self):
        """

        :return:
        """
        metab = pycotools.model.Metabolite(self.model, name='F', particle_number=25,
                                           compartment=self.model.compartments[0])
        self.model = self.model.add_metabolite(metab)
        check = False
        for i in self.model.metabolites:
            if i.name == 'F':
                check = True
        self.assertTrue(check)

    def test_change_states(self):
        """

        :return:
        """
        state_numbers = [0.0, 1, 2, 3, 3, 4, 5, 6, 7]
        self.model.states = state_numbers
        self.assertListEqual([float(i) for i in state_numbers],
                             [float(i) for i in self.model.states.values()])

    def test_get_metabolite_by_key(self):
        """

        :return:
        """
        metab = self.model.get('metabolite', 'Metabolite_1', by='key')
        self.assertEqual(metab.name, 'A')


    def test_get_metbolite_by_name(self):
        """

        :return:
        """
        metab = self.model.get('metabolite', 'A', by='name')
        self.assertEqual(metab.name, 'A')

    def test_get_compartment_by_name(self):
        res = self.model.get('compartment', 'nuc', by='name')
        self.assertEqual(res.name, 'nuc')

    def get_local_parameter_by_name(self):
        res = self.model.get('local_parameter', '(B2C).k1', by='name')
        self.assertEqual(res.name, '(B2C).k1')

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
    def test_remove_state(self):
        """

        :return:
        """
        ##TODO fix concentration attribute in set_metabolites
        metab = pycotools.model.Metabolite(self.model, name='F', particle_number=25,
                                           compartment=self.model.compartments[0])
        self.model = self.model.add_metabolite(metab)
        F = self.model.get('metabolite', 'F', by='name')
        self.model = self.model.remove_metabolite('F', by='name')
        new_F = self.model.get('metabolite', 'F', by='name')
        self.assertEqual(new_F, [])

    def test_add_compartment(self):
        """

        :return:
        """
        comp = pycotools.model.Compartment(self.model,
                                           name='Medium', initial_value=6)
        compartment_model = self.model.add_compartment(comp)
        comp_filename = os.path.join(os.path.dirname(self.model.copasi_file), 'comp_model.cps')
        compartment_model.save(comp_filename)


    def test_remove_compartment(self):
        """

        :return:
        """
        comp = pycotools.model.Compartment(self.model,
                                           name='Medium', initial_value=6)
        self.model = self.model.add_compartment(comp)
        comp = self.model.get('compartment', 'Medium', 'name')
        assert comp != []
        self.model = self.model.remove_compartment(comp.name, by='name')
        comp = self.model.get('compartment', 'Medium', 'name')
        self.assertEqual(comp, [])

    def test_add_global_quantity(self):
        """

        :return:
        """
        global_quantity = pycotools.model.GlobalQuantity(self.model, name='NewGlobal',
                                                         initial_value=5)
        new_model = self.model.add_global_quantity(global_quantity)

        new_global = new_model.get('global_quantity', 'NewGlobal',
                                   by='name')
        self.assertEqual(new_global.name, 'NewGlobal')


    def test_remove_global_quantities(self):
        """

        :return:
        """
        global_quantity = pycotools.model.GlobalQuantity(self.model, name='NewGlobal',
                                                         initial_value=5)
        new_model = self.model.add_global_quantity(global_quantity)
        new_global = new_model.get('global_quantity', 'NewGlobal')
        assert new_global != []
        new_model = new_model.remove_global_quantity('NewGlobal', by='name')
        new_global = new_model.get('global_quantity', 'NewGlobal')
        self.assertEqual(new_global, [])


    def test_get_list_of_call_parameters(self):
        for i in self.model.parameter_descriptions:
            self.assertTrue(isinstance(i, pycotools.model.ParameterDescription))


    def test_mass_action_class(self):
        ma = pycotools.model.MassAction(self.model, reversible=True)
        self.assertEqual(ma.expression, 'k1*PRODUCT&lt;substrate_i>-k2*PRODUCT&lt;product_j>')
    #

    def test_add_mass_action(self):
        ma = pycotools.model.MassAction(self.model, reversible=False)
        self.model = self.model.add_function(ma)
        ##todo find better test condition


    def test_create_parameter_description_key(self):
        KF = pycotools.model.KeyFactory(self.model, type='function_parameter')
        self.assertEqual(len(KF.create_function_parameter_key(n=4)), 4)

    def test_function_user_defined1(self):
        """
        make sure that roles are converted into parameter descriptions
        (function parameters)
        :return:
        """
        fun = pycotools.model.Function(self.model, name='new_funct',
                                       expression='K*M*S',
                                       roles={'K': 'parameter',
                                              'M': 'modifier',
                                              'S': 'substrate'})

        for i in fun.list_of_parameter_descriptions:
            self.assertTrue(isinstance(i, pycotools.model.ParameterDescription))

    def test_add_function(self):
        """

        :return:
        """
        fun = pycotools.model.Function(self.model, name='new_funct',
                                       expression='K*M*S',
                                       roles={'K': 'parameter',
                                              'M': 'modifier',
                                              'S': 'substrate'})
        self.model =  self.model.add_function(fun)
        self.model.save()
        for i in self.model.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
                for j in i:
                    if j.attrib['name'] == fun.name:
                        self.assertEqual(j.attrib['name'], fun.name)



    def test_remove_functions(self):
        fun = pycotools.model.Function(self.model, name='new_funct',
                                       expression='K*M*S',
                                       roles={'K': 'parameter',
                                              'M': 'modifier',
                                              'S': 'substrate'})
        self.model =  self.model.add_function(fun)
        self.model.save()
        self.model = self.model.remove_function('new_funct', by='name')
        for i in self.model.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
                for j in i:
                    self.assertNotEqual(j.attrib['name'], fun.name)

    def test_translator(self):
        trans = pycotools.model.Translator(self.model, '-> B')
        self.assertTrue(isinstance(trans.all_components, list))

    def test_translator2(self):
        trans = pycotools.model.Translator(self.model, 'A -> B')
        self.assertTrue(isinstance(trans.all_components, list))

    def test_translator3(self):
        trans = pycotools.model.Translator(self.model, 'A + A + B -> B; C D')
        self.assertTrue(isinstance(trans.all_components, list))

    def test_translator4(self):
        trans = pycotools.model.Translator(self.model, 'B ->')
        self.assertTrue(isinstance(trans.all_components, list))


    def test_local_parameters(self):
        self.assertEqual(len(self.model.constants), 5)

    def test_key_factory_constant(self):
        """

        :return:
        """
        p =pycotools.model.KeyFactory(self.model, type='constant').generate(2)
        self.assertEqual(len(p), 2)


    def test_add_reaction1(self):
        """
        Test the reaction name is correct
        :return:
        """
        r = pycotools.model.Reaction(self.model,
                                     name='fake_reaction',
                                     expression='A + B + C + D -> E + F',
                                     rate_law='k * A * B * C / D')

        self.model = self.model.add_reaction(r)
        self.model.save()
        xml = pycotools.tasks.CopasiMLParser(self.model.copasi_file).xml

        boolean = False
        for i in xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    if j.attrib['name'] == 'fake_reaction':
                        boolean = True

        self.assertTrue(boolean)

    # # def test_add_reaction2(self):
    # #     """
    # #     Test correct number of substrates
    # #     :return:
    # #     """
    # #     r = pycotools.model.Reaction(self.model,
    # #                                  name='fake_reaction',
    # #                                  expression='A + B + C + D -> E + F',
    # #                                  rate_law='k * A * B * C / D')
    # #     self.model.add_reaction(r)
    # #     self.model.save()
    # #     xml = pycotools.tasks.CopasiMLParser(self.model.copasi_file).xml
    # #
    # #     boolean = False
    # #     for i in xml.iter():
    # #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    # #             for j in i:
    # #                 if j.attrib['name'] == 'fake_reaction':
    # #                     for k in j:
    # #                         if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
    # #                             self.assertTrue(len(k)==4)
    # #
    # # def test_add_reaction3(self):
    # #     """
    # #     Test correct number of products
    # #     :return:
    # #     """
    # #     r = pycotools.model.Reaction(self.model,
    # #                                  name='fake_reaction',
    # #                                  expression='A + B + C + D -> E + F',
    # #                                  rate_law='k * A * B * C / D')
    # #     self.model.add_reaction(r)
    # #     self.model.save()
    # #     xml = pycotools.tasks.CopasiMLParser(self.model.copasi_file).xml
    # #
    # #     boolean = False
    # #     for i in xml.iter():
    # #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    # #             for j in i:
    # #                 if j.attrib['name'] == 'fake_reaction':
    # #                     for k in j:
    # #                         if k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
    # #                             self.assertTrue(len(k)==2)
    # #
    # # def test_add_reaction4(self):
    # #     """
    # #     Test correct number of products
    # #     :return:
    # #     """
    # #     r = pycotools.model.Reaction(self.model,
    # #                                  name='fake_reaction',
    # #                                  expression='A + B + C + D -> E + F',
    # #                                  rate_law='k * A * B * C / D')
    # #     self.model.add_reaction(r)
    # #     self.model.save()
    # #     xml = pycotools.tasks.CopasiMLParser(self.model.copasi_file).xml
    # #
    # #     boolean = False
    # #     for i in xml.iter():
    # #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    # #             for j in i:
    # #                 if j.attrib['name'] == 'fake_reaction':
    # #                     for k in j:
    # #                         if k.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
    # #                             self.assertTrue(len(k) == 1)
    # #
    # # def test_add_reaction5(self):
    # #     """
    # #     Test different reaction
    # #     :return:
    # #     """
    # #     r = pycotools.model.Reaction(self.model,
    # #                                  name='fake_reaction2',
    # #                                  expression='A + F + irs -> ; G',
    # #                                  rate_law='k * A * B * C / D')
    # #     self.model.add_reaction(r)
    # #     self.model.save()
    # #     xml = pycotools.tasks.CopasiMLParser(self.model.copasi_file).xml
    # #
    # #     boolean = False
    # #     for i in xml.iter():
    # #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    # #             for j in i:
    # #                 if j.attrib['name'] == 'fake_reaction2':
    # #                     for k in j:
    # #                         if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
    # #                             self.assertTrue(len(k) == 3)
    # #
    # # def test_add_reaction6(self):
    # #     """
    # #     Test different reaction
    # #     :return:
    # #     """
    # #     r = pycotools.model.Reaction(self.model,
    # #                                  name='fake_reaction2',
    # #                                  expression='A + F + irs -> ; G',
    # #                                  rate_law='k * A * F / irs + G')
    # #     self.model = self.model.add_reaction(r)
    # #     self.model.save()
    # #     xml = pycotools.tasks.CopasiMLParser(self.model.copasi_file).xml
    # #     boolean = False
    # #     for i in xml.iter():
    # #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    # #             for j in i:
    # #                 if j.attrib['name'] == 'fake_reaction2':
    # #                     for k in j:
    # #                         if k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
    # #                             self.assertTrue(len(k) == 0)
    # #
    # #
    # def test_translater_again(self):
    #     trans = pycotools.model.Translator(self.model, 'A + F + irs -> ;G')
    #     self.assertEqual(trans.products, [])
    #
    # def test_translater_again2(self):
    #     trans = pycotools.model.Translator(self.model, 'A ->')
    #     self.assertEqual(trans.products, [])
    #
    # def test_translater_again3(self):
    #     trans = pycotools.model.Translator(self.model, 'A -> B; C ')
    #     self.assertEqual(trans.modifiers[0].name, 'C')
    # #
    # #
    # # # def test_set_global_quantity(self):
    # # #     """
    # # #
    # # #     :return:
    # # #     """
    # # #     ## add new global
    # # #     glob = pycotools.model.GlobalQuantity(self.model,
    # # #                                           name='X')
    # # #
    # # #     self.model = self.model.add_global_quantity(glob)
    # # #     self.model = self.model.set('global_quantity', 'X', 55)
    # # #     x = self.model.get('global_quantity', 'X')
    # # #     self.assertEqual(float(x.initial_value), 55.0)
    # #
    # #
    def test_remove_method_global(self):
        """

        :return:
        """
        glob = pycotools.model.GlobalQuantity(self.model, name='X')
        self.model = self.model.add_global_quantity(glob)
        assert 'X' in [i.name for i in self.model.global_quantities]
        self.model = self.model.remove('global_quantity', 'X')
        boolean = True
        for i in self.model.global_quantities:
            if i.name == 'X':
                boolean = False
        self.assertTrue(boolean)

    def test_add_compartment(self):
        """

        :return:
        """
        comp = pycotools.model.Compartment(self.model, name='X')
        self.model = self.model.add('compartment', comp)
        boolean = False

        for i in self.model.compartments:
            if i.name == 'X':
                boolean = True
        self.assertTrue(boolean)

    def test_remove_method_compartment(self):
        """

        :return:
        """
        comp = pycotools.model.Compartment(self.model, name='Cell')
        self.model = self.model.add_compartment(comp)
        assert 'Cell' in [i.name for i in self.model.compartments]
        self.model = self.model.remove('compartment', 'Cell')
        boolean = True
        for i in self.model.compartments:
            if i.name == 'X':
                boolean = False
        self.assertTrue(boolean)


    # def test_remove_raction(self):
    #     """
    #     Test different reaction
    #     :return:
    #     """
    #     r = pycotools.model.Reaction(self.model,
    #                                  name='fake_reaction2',
    #                                  expression='A + B -> C',
    #                                  rate_law='k * A * B')
    #     self.model = self.model.add_reaction(r)
    #     self.model = self.model.remove_reaction('fake_reaction2', by='name')
    #     # self.model = self.model.remove('reaction', 'fake_reaction2')
    #     self.model.save()
    #     new_model = pycotools.tasks.CopasiMLParser(self.model.copasi_file).xml
    #     boolean = True
    #     for i in new_model.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    #             for j in i:
    #                 if j.attrib['name'] == 'fake_reaction2':
    #                     boolean = False
    #     self.assertTrue(boolean)


    def test_set_global_initial_value(self):
        """

        :return:
        """
        glob = pycotools.model.GlobalQuantity(self.model, name='X', initial_value=1)
        self.model = self.model.add_global_quantity(glob)
        self.model.save()
        assert glob.name in [i.name for i in self.model.global_quantities]
        self.model = self.model.set('global_quantity', 'X', 100, 'name', 'initial_value')
        self.assertEqual(100.0,
                         float([i.initial_value for i in self.model.global_quantities if i.name == 'X'][0]))


    def test_metabolite_concentration(self):
        """

        :return:
        """
        metab =  pycotools.model.Metabolite(self.model,
                                            name='X')
        self.assertEqual(str(metab.concentration), str(1))

    def test_metabolite_concentration2(self):
        """

        :return:
        """
        metab = pycotools.model.Metabolite(self.model,
                                           name='X',
                                           concentration=123445)
        self.assertEqual(str(metab.concentration), str(123445))

    def test_metabolite_concentration2(self):
        """

        :return:
        """
        metab = pycotools.model.Metabolite(self.model,
                                           name='X',
                                           concentration=55)
        self.assertEqual(str(metab.particle_number), str(3.31217747135e+22))

    #
    # # def test_set_metabolite_initial_value(self):
    # #     """
    # #
    # #     :return:
    # #     """
    # #     metab = pycotools.model.Metabolite(self.model,
    # #                                        name='X', concentration=15)
    # #     self.model = self.model.add('metabolite', metab)
    # #     self.model.save()
    # #     assert metab.name in [i.name for i in self.model.metabolites]
    # #     self.model = self.model.set_metabolite('X', 100, 'concentration')
    # #
    # #     self.model.open()
    # #     for i in self.model.metabolites:
    # #         print i.name, i.concentration
    # #     self.assertEqual(100.0,
    # #                      float([i.concentration for i in self.model.metabolites if i.name == 'X'][0]))
    #


    def test_change_metab_particle_numer(self):
        """

        :return:
        """
        metab = pycotools.model.Metabolite(self.model, name='X',
                                           particle_number=1000)
        model = self.model.add('metabolite', metab)
        model = self.model.set('metabolite', 'X', 1234, 'name', 'particle_number')
        metab = self.model.get('metabolite', 'X', by='name')
        self.assertEqual(metab.particle_number, str(1234.0))


    def test_change_metab_concentration(self):
        """

        :return:
        """
        metab = pycotools.model.Metabolite(self.model, name='X',
                                           concentration=1000)
        model = self.model.add('metabolite', metab)
        model = self.model.set('metabolite', 'X', str(1234), 'name', 'concentration')
        metab = self.model.get('metabolite', 'X', by='name')
        self.assertAlmostEqual(float(metab.concentration), float(1234.0))



    def test_change_metab_particle_numer_using_set(self):
        """

        :return:
        """
        metab = pycotools.model.Metabolite(self.model, name='X',
                                           particle_number=1000)
        model = self.model.add('metabolite', metab)
        model = self.model.set('metabolite',
                               match_value='X',
                               new_value=1234,
                               match_field='name',
                               change_field='particle_number')

        metab = self.model.get('metabolite', 'X', by='name')
        self.assertEqual(metab.particle_number, str(1234.0))

    def test_change_metab_concentration_using_set(self):
        """

        :return:
        """
        metab = pycotools.model.Metabolite(self.model, name='X',
                                           concentration=1000)
        model = self.model.add('metabolite', metab)
        model = self.model.set('metabolite',
                               match_value='X',
                               new_value=1234,
                               match_field='name',
                               change_field='concentration')

        metab = self.model.get('metabolite', 'X', by='name')
        self.assertAlmostEqual(float(metab.concentration), float(1234.0))


    def test_set_compartment_value(self):
        """

        :return:
        """
        compartment = self.model.compartments[0]
        self.model = self.model.set('compartment', 'nuc', 55,
                                    match_field='name',
                                    change_field='initial_value')
        comp = self.model.get('compartment', 'nuc')
        self.assertEqual(str(comp.initial_value), str(55.0))

    def test_set_compartment_name(self):
        """

        :return:
        """
        compartment = self.model.compartments[0]
        self.model = self.model.set('compartment',
                                    'nuc',
                                    'nucleus',
                                    match_field='name',
                                    change_field='name')
        comp = self.model.get('compartment', 'nucleus', by='name')
        self.assertEqual(comp.name, 'nucleus')

    def test_set_metabolite_name(self):
        """

        :return:
        """
        self.model = self.model.set('metabolite',
                                    'B',
                                    'Bees',
                                    match_field='name',
                                    change_field='name')
        metab = self.model.get('metabolite', 'Bees')
        self.assertEqual(metab.name, 'Bees')
    #
    def test_change_global_value(self):
        """

        :return:
        """
        self.model = self.model.set('global_quantity',
                                    'A2B',
                                    'IveBeenChanged',
                                    match_field='name',
                                    change_field='name')
        glob = self.model.get('global_quantity', 'IveBeenChanged')
        self.assertEqual(glob.name, 'IveBeenChanged')

    def test_insert_parameters_metabolite(self):
        """

        :return:
        """
        I= pycotools.model.InsertParameters(self.model, parameter_dict={'B': 35,
                                                                        '(B2C).k2': 45,
                                                                        'A2B':55})
        self.model = I.insert()

        conc = [i.concentration for i in self.model.metabolites if i.name == 'B']
        self.assertAlmostEqual(float(conc[0]), float(35))


    def test_insert_parameters_metabolite_particles(self):
        """

        :return:
        """
        I= pycotools.model.InsertParameters(
            self.model,
            parameter_dict={
                # 'nuc': 85,
                'B': 78,
                '(B2C).k2': 96,
                'A2B':55
            }, quantity_type='particle_number')
        self.model = I.insert()
        part = [i.particle_number for i in self.model.metabolites if i.name == 'B']
        self.assertAlmostEqual(float(part[0]), float(78))

    def test_insert_parameters_globals(self):
        """

        :return:
        """
        I= pycotools.model.InsertParameters(
            self.model,
            parameter_dict={
                # 'nuc': 85,
                'B': 35,
                '(B2C).k2': 45,
                'A2B':32
            })
        self.model = I.insert()
        val = [i.initial_value for i in self.model.global_quantities if i.name == 'A2B']
        self.assertAlmostEqual(float(val[0]), float(32))

    def test_insert_parameters_locals(self):
        """

        :return:
        """
        I= pycotools.model.InsertParameters(
            self.model,
            parameter_dict={
                # 'nuc': 85,
                'B': 35,
                '(B2C).k2': 64,
                'A2B': 597,
            }, inplace=True).model
        val = [i.initial_value for i in self.model.global_quantities if i.name == 'A2B']
        self.assertAlmostEqual(float(val[0]), float(597))

    def test_insert_parameters_global_df(self):
        """

        :return:
        """
        parameter_dict = {'B': 35,
                          '(B2C).k2': 64,
                          'A2B': 597}

        df = pandas.DataFrame(parameter_dict, index=[0])
        I= pycotools.model.InsertParameters(
            self.model, df=df, inplace=True).model
        val = [i.initial_value for i in self.model.global_quantities if i.name == 'A2B']
        self.assertAlmostEqual(float(val[0]), float(597))

    def test_insert_parameters_metabolite_df(self):
        """

        :return:
        """
        parameter_dict = {'B': 35,
                          '(B2C).k2': 64,
                          'A2B': 597}

        df = pandas.DataFrame(parameter_dict, index=[0])
        self.model = pycotools.model.InsertParameters(self.model, df=df, inplace=True).model
        conc = [i.concentration for i in self.model.metabolites if i.name == 'B']
        self.assertAlmostEqual(float(conc[0]), float(35))
    #

    def test_number_of_local_parameters(self):
        """

        :return:
        """
        r = self.model.get('reaction', 'B2C')

        self.assertEqual(len(r.parameters_dict), 2)

    def test_names_of_local_paramers(self):
        """

        :return:
        """
        r = self.model.get('reaction', 'B2C')
        names = ['k1', 'k2']
        self.assertListEqual(names, [i.name for i in r.parameters])

    # def test_change_reaction_name(self):
    #     """
    #     At present this test fails.
    #     Not high enough priority to fix now.
    #     :return:
    #     """
    #     ## get reaction
    #     reaction = self.model.get('reaction', 'B2C')
    #     self.model = self.model.set('reaction', 'B2C', 'changed_name',
    #                                 'name', 'name')
    #     self.model.save()
    #     changed =  self.model.get('reaction', 'changed_name')
    #     self.assertEqual(changed.name, 'changed_name')
    #

    def test_get_parameters(self):
        """

        :return:
        """
        self.assertEqual(self.model.parameters.shape[1], 9)



    def test_export_sbml(self):
        """

        :return:
        """
        sbml_file = self.model.to_sbml()
        self.assertTrue(os.path.isfile(sbml_file))

    def test_copasi_file_setter(self):
        """

        :return:
        """
        new_filename = os.path.join(self.model.root+'/test', 'CopasiModel2.cps')
        self.model.copasi_file = new_filename
        self.assertEqual(new_filename, self.model.copasi_file)

    def test_copasi_file_root(self):
        """

        :return:
        """
        new_root = self.model.root+'/test'
        new_file_name = os.path.join(new_root, 'CopasiModel2.cps')
        self.model.copasi_file = new_file_name
        self.assertEqual(new_root, self.model.root)

    def test_copy_model(self):
        """

        :return:
        """
        new_filename = os.path.join(self.model.root, 'CopasiModel2.cps')
        new_model = self.model.copy(new_filename)
        new_model.save()
        self.assertTrue(os.path.isfile(new_filename))

    # def test_func(self):
    #     """
    #
    #     :return:
    #     """
    #     # print self.model.reactions
    #     r = pycotools.model.Reaction(self.model,
    #                        name='smad7_prod', expression='Smads_Complex_c -> Smads_Complex_c + Smad7',
    #                        rate_law='k1*Smads_Complex_c')
    #
    #     # f = pycotools.model.Function(self.model, name='f1', expression='A*B*k1', roles={'A': 'substrate'})
    #
    #     # model = self.model.add_function(f)
    #
    #
    #     model = self.model.add_reaction(r)
    #     print model.open()
    #     print r.rate_law

























if __name__ == '__main__':
    unittest.main()