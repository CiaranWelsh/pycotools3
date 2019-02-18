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

Module that tests the operations of the _Base base test

"""

import os, glob
# import site
# site.addsitedir(os.path.dirname(os.path.dirname(__file__)))
from . import _test_base
import pycotools3

import pandas
import unittest
from lxml import etree
from collections import OrderedDict

class ModelLevelAttributeTests(_test_base._BaseTest):
    """
    Test things like volume and mole units
    """
    def setUp(self):
        super(ModelLevelAttributeTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)

    def test_time_unit(self):
        self.assertEqual(self.model.time_unit, 's')

    def test_model_name(self):
        self.assertEqual(self.model.name, 'TestModel1')

    def test_volume(self):
        self.assertEqual(self.model.volume_unit, 'ml')

    def test_length(self):
        self.assertEqual(self.model.length_unit, 'm')

    def test_avagadro(self):
        self.assertEqual(self.model.avagadro, 6.02214179e+23)

    def test_model_key(self):
        self.assertEqual(self.model.key, 'Model_1')

    def test_reference(self):
        self.assertTrue('CN=Root,Model=New Model', self.model.reference)

    def test_xml(self):
        self.assertTrue(isinstance(self.model.xml, etree._Element))


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

    def test_new_model1(self):
        """
        Test building of empty new model
        :return:
        """
        new_filename = os.path.join(self.model.root, 'New_model.cps')
        m = pycotools3.model.Model(new_filename, new=True)
        self.assertTrue(os.path.isfile(new_filename))

    def test_new_model2(self):
        """
        Test building of empty new model
        :return:
        """
        new_filename = os.path.join(self.model.root, 'New_model.cps')
        m = pycotools3.model.Model(new_filename, new=True)
        self.assertTrue(isinstance(m, pycotools3.model.Model))

class ModelComponentAttributeTests(_test_base._BaseTest):
    """
    Test aspects of model components, such as metbaolite or
    global quantity
    """

    def setUp(self):
        super(ModelComponentAttributeTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)

    def test_get_variable_names_all(self):
        expected = ['A', 'A2B', 'ADeg_k1', 'B', 'B2C', 'B2C_0_k2', 'C', 'C2A_k1', 'ThisIsAssignment', 'cyt', 'nuc']
        self.assertListEqual(expected, self.model.get_variable_names('a'))

    def test_get_variable_names_local(self):
        expected = []
        self.assertListEqual(expected, self.model.get_variable_names('l'))

    def test_get_variable_names_global(self):
        expected = ['A2B', 'ADeg_k1', 'B2C', 'B2C_0_k2', 'C2A_k1', 'ThisIsAssignment']
        self.assertListEqual(expected, self.model.get_variable_names('g'))

    def test_get_variable_names_global_and_compartment(self):
        expected = ['A2B', 'ADeg_k1', 'B2C', 'B2C_0_k2', 'C2A_k1', 'ThisIsAssignment', 'cyt', 'nuc']
        actual = self.model.get_variable_names('gc')
        self.assertListEqual(expected, actual)

    def test_get_variable_names_global_and_metabolite(self):
        expected = ['A', 'A2B', 'ADeg_k1', 'B', 'B2C', 'B2C_0_k2', 'C', 'C2A_k1', 'ThisIsAssignment']
        actual = self.model.get_variable_names('mg')
        self.assertListEqual(expected, actual)

    def test_get_variable_names_global_without_assignments_and_metabolite(self):
        expected = ['A', 'A2B', 'ADeg_k1', 'B', 'B2C', 'B2C_0_k2', 'C', 'C2A_k1']
        actual = self.model.get_variable_names('mg', include_assignments=False)
        self.assertListEqual(expected, actual)


    def test_contains_protocol(self):
        self.assertTrue('A' in self.model)

    def test_metabolites(self):
        self.assertEqual(len(self.model.metabolites), 3)

    def test_metabolites2(self):
        for i in self.model.metabolites:
            self.assertTrue(isinstance(i, pycotools3.model.Metabolite))

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
        self.assertEqual(len(self.model.global_quantities), 6)

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
        self.assertEqual(len(self.model.local_parameters), 0)
    #
    def test_local_parameters2(self):
        for i in self.model.constants:
            self.assertTrue(isinstance(i, pycotools3.model.LocalParameter))

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
        k = pycotools3.model.KeyFactory(self.model, type='constant').generate()
        L= pycotools3.model.LocalParameter(self.model,
                                           key=k,
                                           name='k1', reaction_name='v1',
                                           global_name='(v1).k1')
        self.assertEqual(L.global_name, '(v1).k1')

    def test_local_parameters5(self):
        k = pycotools3.model.KeyFactory(self.model, type='constant').generate()
        L= pycotools3.model.LocalParameter(self.model,
                                           key=k,
                                           name='k1',
                                           reaction_name='v1')
        self.assertTrue('global_name' in list(L.__dict__.keys()))

    def test_functions(self):
        self.assertTrue(len(self.model.functions), 2)

    def test_functions2(self):
        [self.assertTrue(isinstance(i, pycotools3.model.Function) for i in self.model.functions)]

    def test_number_of_reactions(self):
        self.assertEqual(self.model.number_of_reactions, 4)


    def test_reactions(self):
        self.assertEqual(len( self.model.reactions), 4)


    def test_metabolite_concentration2(self):
        """

        :return:
        """
        metab = pycotools3.model.Metabolite(self.model,
                                            name='X',
                                            concentration=123445)
        self.assertEqual(str(metab.concentration), str(123445))

    def test_metabolite_concentration2(self):
        """

        :return:
        """
        metab = pycotools3.model.Metabolite(self.model,
                                            name='X',
                                            concentration=55)
        self.assertEqual(str(metab.particle_numbers), str(3.3121774713500003e+22))



class SetTests(_test_base._BaseTest):
    """
    Test setting of existing model variables
    """

    def setUp(self):
        super(SetTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)

    def test_set_name(self):
        """

        :return:
        """
        self.model.name = 'new_name'
        self.assertEqual(self.model.name, 'new_name')


    def test_create_metabolite(self):
        """

        :return:
        """
        metab = pycotools3.model.Metabolite(self.model, name='F', particle_numbers=25,
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
        state_numbers = [0.0, 1, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10]
        self.model.states = state_numbers
        self.assertListEqual([float(i) for i in state_numbers],
                             [float(i) for i in list(self.model.states.values())])

    def test_set_global_initial_value(self):
        """

        :return:
        """
        glob = pycotools3.model.GlobalQuantity(self.model, name='X', initial_value=1)
        self.model = self.model.add_global_quantity(glob)
        self.model.save()
        assert glob.name in [i.name for i in self.model.global_quantities]
        self.model = self.model.set('global_quantity', 'X', 100, 'name', 'initial_value')
        self.assertEqual(100.0,
                         float([i.initial_value for i in self.model.global_quantities if i.name == 'X'][0]))

    def test_change_metab_particle_numer(self):
        """

        :return:
        """
        metab = pycotools3.model.Metabolite(self.model, name='X',
                                            particle_numbers=1000)
        model = self.model.add_component('metabolite', metab)
        model = self.model.set('metabolite', 'X', 1234, 'name', 'particle_numbers')
        metab = self.model.get('metabolite', 'X', by='name')
        self.assertEqual(metab.particle_numbers, str(1234.0))



    def test_change_metab_concentration(self):
        """

        :return:
        """
        metab = pycotools3.model.Metabolite(self.model, name='X',
                                            concentration=1000)
        model = self.model.add_component('metabolite', metab)
        model = self.model.set('metabolite', 'X', str(1234), 'name', 'concentration')
        metab = self.model.get('metabolite', 'X', by='name')
        self.assertAlmostEqual(float(metab.concentration), float(1234.0))

    def test_change_metab_particle_numer_using_set(self):
        """

        :return:
        """
        metab = pycotools3.model.Metabolite(self.model, name='X',
                                            particle_numbers=1000)
        model = self.model.add_component('metabolite', metab)
        model = self.model.set('metabolite',
                               match_value='X',
                               new_value=1234,
                               match_field='name',
                               change_field='particle_numbers')

        metab = self.model.get('metabolite', 'X', by='name')
        self.assertEqual(metab.particle_numbers, str(1234.0))

    def test_change_metab_concentration_using_set(self):
        """

        :return:
        """
        metab = pycotools3.model.Metabolite(self.model, name='X',
                                            concentration=1000)
        model = self.model.add_component('metabolite', metab)
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

class GetTests(_test_base._BaseTest):
    """
    Test getting of existing model variables
    """

    def setUp(self):
        super(GetTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)

    def test_get_metabolite_by_key(self):
        """

        :return:
        """
        metab = self.model.get('metabolite', 'Metabolite_1', by='key')
        self.assertEqual(metab.name, 'B')


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

    def test_get_parameters(self):
        """

        :return:
        """
        self.assertEqual(self.model.parameters.shape[1], 9)


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


class RemoveTests(_test_base._BaseTest):
    """
    Test removal of  model variables
    """

    def setUp(self):
        super(RemoveTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)


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
        metab = pycotools3.model.Metabolite(self.model, name='F', particle_numbers=25,
                                            compartment=self.model.compartments[0])
        self.model = self.model.add_metabolite(metab)
        F = self.model.get('metabolite', 'F', by='name')
        self.model = self.model.remove_metabolite('F', by='name')
        new_F = self.model.get('metabolite', 'F', by='name')
        self.assertEqual(new_F, [])

    def test_remove_compartment(self):
        """

        :return:
        """
        comp = pycotools3.model.Compartment(self.model,
                                            name='Medium', initial_value=6)
        self.model = self.model.add_compartment(comp)
        comp = self.model.get('compartment', 'Medium', 'name')
        assert comp != []
        self.model = self.model.remove_compartment(comp.name, by='name')
        comp = self.model.get('compartment', 'Medium', 'name')
        self.assertEqual(comp, [])

    def test_remove_functions(self):
        fun = pycotools3.model.Function(self.model, name='new_funct',
                                        expression='K*M*S',
                                        roles={'K': 'parameter',
                                              'M': 'modifier',
                                              'S': 'substrate'})
        self.model = self.model.add_function(fun)
        self.model.save()
        self.model = self.model.remove_function('new_funct', by='name')
        for i in self.model.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
                for j in i:
                    self.assertNotEqual(j.attrib['name'], fun.name)

    def test_remove_method_global(self):
        """

        :return:
        """
        glob = pycotools3.model.GlobalQuantity(self.model, name='X')
        self.model = self.model.add_global_quantity(glob)
        assert 'X' in [i.name for i in self.model.global_quantities]
        self.model = self.model.remove('global_quantity', 'X')
        boolean = True
        for i in self.model.global_quantities:
            if i.name == 'X':
                boolean = False
        self.assertTrue(boolean)

    def test_remove_method_compartment(self):
        """

        :return:
        """
        comp = pycotools3.model.Compartment(self.model, name='Cell')
        self.model = self.model.add_compartment(comp)
        assert 'Cell' in [i.name for i in self.model.compartments]
        self.model = self.model.remove('compartment', 'Cell')
        boolean = True
        for i in self.model.compartments:
            if i.name == 'X':
                boolean = False
        self.assertTrue(boolean)

    def test_remove_raction(self):
        """
        Test different reaction
        :return:
        """
        r = pycotools3.model.Reaction(self.model,
                                      name='fake_reaction2',
                                      expression='A + B -> C',
                                      rate_law='k * A * B')
        self.model = self.model.add_reaction(r)
        self.model = self.model.remove_reaction('fake_reaction2', by='name')
        # self.model = self.model.remove('reaction', 'fake_reaction2')
        self.model.save()
        new_model = pycotools3.tasks.CopasiMLParser(self.model.copasi_file).xml
        boolean = True
        for i in new_model.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    if j.attrib['name'] == 'fake_reaction2':
                        boolean = False
        self.assertTrue(boolean)


class AddTests(_test_base._BaseTest):
    """
    Test adding of  model variables
    """

    def setUp(self):
        super(AddTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)


    def test_add_compartment(self):
        """

        :return:
        """
        comp = pycotools3.model.Compartment(self.model,
                                            name='Medium', initial_value=6)
        compartment_model = self.model.add_compartment(comp)
        comp_filename = os.path.join(os.path.dirname(self.model.copasi_file), 'comp_model.cps')
        compartment_model.save(comp_filename)

    def test_add_compartment_using_add(self):
        """
        Test the add method.
        :return:
        """
        comp = {'name': 'Medium',
                'initial_value': 154}
        self.model.add('compartment', **comp)
        self.model.save()
        comp2 = self.model.get('compartment', 'Medium')
        self.assertEqual(comp2.name, 'Medium')
        self.assertEqual(comp2.initial_value, 154)


    def test_add_compartment2(self):
        """

        :return:
        """
        comp = pycotools3.model.Compartment(self.model, name='X')
        self.model = self.model.add_component('compartment', comp)
        boolean = False

        for i in self.model.compartments:
            if i.name == 'X':
                boolean = True
        self.assertTrue(boolean)

    def test_add_compartment_from_string(self):
        """

        :return:
        """
        self.model = self.model.add_component('compartment', 'comp')
        boolean = False
        for i in self.model.compartments:
            if i.name == 'comp':
                boolean = True
        self.assertTrue(boolean)

    def test_add_global_quantity(self):
        """

        :return:
        """
        global_quantity = pycotools3.model.GlobalQuantity(self.model, name='NewGlobal',
                                                          initial_value=5)
        new_model = self.model.add_global_quantity(global_quantity)

        new_global = new_model.get('global_quantity', 'NewGlobal',
                                   by='name')
        self.assertEqual(new_global.name, 'NewGlobal')


    def test_remove_global_quantities(self):
        """

        :return:
        """
        global_quantity = pycotools3.model.GlobalQuantity(self.model, name='NewGlobal',
                                                          initial_value=5)
        new_model = self.model.add_global_quantity(global_quantity)
        new_global = new_model.get('global_quantity', 'NewGlobal')
        assert new_global != []
        new_model = new_model.remove_global_quantity('NewGlobal', by='name')
        new_global = new_model.get('global_quantity', 'NewGlobal')
        self.assertEqual(new_global, [])

    def test_get_list_of_call_parameters(self):
        for i in self.model.parameter_descriptions:
            self.assertTrue(isinstance(i, pycotools3.model.ParameterDescription))


    def test_mass_action_class(self):
        ma = pycotools3.model.MassAction(self.model, reversible=True)
        self.assertEqual(ma.expression, 'k1*PRODUCT&lt;substrate_i>-k2*PRODUCT&lt;product_j>')
    #

    def test_add_mass_action(self):
        ma = pycotools3.model.MassAction(self.model, reversible=False)
        self.model = self.model.add_function(ma)
        ##todo find better test condition


    def test_create_parameter_description_key(self):
        KF = pycotools3.model.KeyFactory(self.model, type='function_parameter')
        self.assertEqual(len(KF.create_function_parameter_key(n=4)), 4)

    def test_function_user_defined1(self):
        """
        make sure that roles are converted into parameter descriptions
        (function parameters)
        :return:
        """
        fun = pycotools3.model.Function(self.model, name='new_funct',
                                        expression='K*M*S',
                                        roles={'K': 'parameter',
                                              'M': 'modifier',
                                              'S': 'substrate'})

        for i in fun.list_of_parameter_descriptions:
            self.assertTrue(isinstance(i, pycotools3.model.ParameterDescription))

    def test_add_function(self):
        """

        :return:
        """
        fun = pycotools3.model.Function(self.model, name='new_funct',
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

    def test_add_reaction1(self):
        """
        Test the reaction name is correct
        :return:
        """
        r = pycotools3.model.Reaction(self.model,
                                      name='fake_reaction',
                                      expression='A + B + C + D -> E + F',
                                      rate_law='k * A * B * C / D')

        self.model = self.model.add_reaction(r)
        self.model.save()
        xml = pycotools3.tasks.CopasiMLParser(self.model.copasi_file).xml

        boolean = False
        for i in xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    if j.attrib['name'] == 'fake_reaction':
                        boolean = True

        self.assertTrue(boolean)

    def test_add_reaction2(self):
        """
        Test correct number of substrates
        :return:
        """
        r = pycotools3.model.Reaction(self.model,
                                      name='fake_reaction',
                                      expression='A + B + C + D -> E + F',
                                      rate_law='k * A * B * C / D')
        self.model.add_reaction(r)
        self.model.save()
        xml = pycotools3.tasks.CopasiMLParser(self.model.copasi_file).xml

        boolean = False
        for i in xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    if j.attrib['name'] == 'fake_reaction':
                        for k in j:
                            if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
                                self.assertTrue(len(k)==4)

    def test_add_reaction3(self):
        """
        Test correct number of products
        :return:
        """
        r = pycotools3.model.Reaction(self.model,
                                      name='fake_reaction',
                                      expression='A + B + C + D -> E + F',
                                      rate_law='k * A * B * C / D')
        self.model.add_reaction(r)
        self.model.save()
        xml = pycotools3.tasks.CopasiMLParser(self.model.copasi_file).xml

        boolean = False
        for i in xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    if j.attrib['name'] == 'fake_reaction':
                        for k in j:
                            if k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
                                self.assertEqual(len(k), 2)

    def test_add_reaction4(self):
        """
        Test correct number of constants
        :return:
        """
        r = pycotools3.model.Reaction(self.model,
                                      name='fake_reaction',
                                      expression='A + B + C + D -> E + F',
                                      rate_law='k * A * B * C / D')
        self.model.add_reaction(r)
        self.model.save()
        xml = pycotools3.tasks.CopasiMLParser(self.model.copasi_file).xml

        boolean = False
        for i in xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    if j.attrib['name'] == 'fake_reaction':
                        for k in j:
                            if k.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                                self.assertEqual(len(k), 1)

    def test_add_reaction5(self):
        """
        Test different reaction
        :return:
        """
        r = pycotools3.model.Reaction(self.model,
                                      name='fake_reaction2',
                                      expression='A + F + irs -> ; G',
                                      rate_law='k * A * B * C / D')
        self.model.add_reaction(r)
        self.model.save()
        xml = pycotools3.tasks.CopasiMLParser(self.model.copasi_file).xml

        boolean = False
        for i in xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    if j.attrib['name'] == 'fake_reaction2':
                        for k in j:
                            if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
                                self.assertTrue(len(k) == 3)

    def test_add_reaction6(self):
        """
        Test different reaction
        :return:
        """
        r = pycotools3.model.Reaction(self.model,
                                      name='fake_reaction2',
                                      expression='A + F + irs -> ; G',
                                      rate_law='k * A * F / irs + G')
        self.model = self.model.add_reaction(r)
        self.model.save()
        xml = pycotools3.tasks.CopasiMLParser(self.model.copasi_file).xml
        boolean = False
        for i in xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    if j.attrib['name'] == 'fake_reaction2':
                        for k in j:
                            if k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
                                self.assertTrue(len(k) == 0)

    def test_reaction_with_kwargs(self):
        self.model.add('reaction', name='new_reaction', expression='A -> B',
                       rate_law='k*A')
        r = self.model.get('reaction', 'new_reaction')
        self.assertEqual(r.name, 'new_reaction')
        self.assertEqual(r.expression, 'A -> B')

    def test_add_metabolite(self):
        metab = pycotools3.model.Metabolite(
            self.model, 'metab'
        )
        self.model.add_component('metabolite', metab)

        m = self.model.get('metabolite', 'metab')
        self.assertEqual(m.name, metab.name)

    def test_add_metabolite_by_string(self):
        """
        Use string instead of Metabolite
        :return:
        """
        self.model.add_component('metabolite', 'p')
        m = self.model.get('metabolite', 'p', by='name')
        self.assertNotEqual(m, [])

    def test_add_metabolite_with_kwargs(self):
        """

        :return:
        """
        model = self.model.add('metabolite', name='X', particle_numbers=1001)
        metab = self.model.get('metabolite', 'X')
        self.assertEqual(metab.particle_numbers, str(1001.0))

    def test_add_global_quantity(self):
        """

        :return:
        """
        glo = pycotools3.model.GlobalQuantity(self.model, 'X')
        self.model.add_component('global_quantity', glo)
        self.assertEqual(self.model.get('global_quantity', 'X', by='name').name, 'X')

    def test_add_global_quantity_with_kwargs(self):
        """

        :return:
        """
        glo = pycotools3.model.GlobalQuantity(self.model, 'X')
        self.model.add('global_quantity', name='X', initial_value=50)
        g = self.model.get('global_quantity', 'X')
        self.assertEqual(g.name, 'X')
        self.assertEqual(g.initial_value, '50.0')

    def test_add_global_quantity_from_string(self):
        """

        :return:
        """
        self.model.add_component('global_quantity', 'X')
        self.assertEqual(self.model.get('global_quantity', 'X', by='name').name, 'X')


class TranslatorTests(_test_base._BaseTest):
    """
    Test the Translator class
    """

    def setUp(self):
        super(TranslatorTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)

    def test_translator(self):
        trans = pycotools3.model.Translator(self.model, '-> B')
        self.assertTrue(isinstance(trans.all_components, list))

    def test_translator2(self):
        trans = pycotools3.model.Translator(self.model, 'A -> B')
        self.assertTrue(isinstance(trans.all_components, list))

    def test_translator3(self):
        trans = pycotools3.model.Translator(self.model, 'A + A + B -> B; C D')
        self.assertTrue(isinstance(trans.all_components, list))

    def test_translator4(self):
        trans = pycotools3.model.Translator(self.model, 'B ->')
        self.assertTrue(isinstance(trans.all_components, list))


    def test_local_parameters(self):
        self.assertEqual(len(self.model.constants), 5)



    def test_key_factory_constant(self):
        """

        :return:
        """
        p =pycotools3.model.KeyFactory(self.model, type='constant').generate(2)
        self.assertEqual(len(p), 2)

    def test_translater_again(self):
        trans = pycotools3.model.Translator(self.model, 'A + F + irs -> ;G')
        self.assertEqual(trans.products, [])

    def test_translater_again2(self):
        trans = pycotools3.model.Translator(self.model, 'A ->')
        self.assertEqual(trans.products, [])

    def test_translater_again3(self):
        trans = pycotools3.model.Translator(self.model, 'A -> B; C ')
        self.assertEqual(trans.modifiers[0].name, 'C')


    def test_metabolite_concentration(self):
        """

        :return:
        """
        metab =  pycotools3.model.Metabolite(self.model,
                                             name='X')
        self.assertEqual(str(metab.concentration), str(float(1)))




class InsertParameterTests(_test_base._BaseTest):
    """
    Test the Translator class
    """

    def setUp(self):
        super(InsertParameterTests, self).setUp()
        self.model = pycotools3.model.Model(self.copasi_file)


    def test_insert_parameters_metabolite(self):
        """

        :return:
        """
        I= pycotools3.model.InsertParameters(self.model, parameter_dict={'B': 35,
                                                                        'B2C_0_k2': 45,
                                                                        'A2B':55})
        self.model = I.insert()

        conc = [i.concentration for i in self.model.metabolites if i.name == 'B']
        self.assertAlmostEqual(float(conc[0]), float(35))


    def test_insert_parameters_metabolite_particles(self):
        """

        :return:
        """
        I= pycotools3.model.InsertParameters(
            self.model,
            parameter_dict={
                # 'nuc': 85,
                'B': 78,
                'B2C_0_k2': 96,
                'A2B':55
            }, quantity_type='particle_numbers')
        self.model = I.insert()
        part = [i.particle_numbers for i in self.model.metabolites if i.name == 'B']
        self.assertAlmostEqual(float(part[0]), float(78))

    def test_insert_parameters_globals(self):
        """

        :return:
        """
        I= pycotools3.model.InsertParameters(
            self.model,
            parameter_dict={
                # 'nuc': 85,
                'B': 35,
                'B2C_0_k2': 45,
                'A2B': 32
            })
        self.model = I.insert()
        val = [i.initial_value for i in self.model.global_quantities if i.name == 'A2B']
        self.assertAlmostEqual(float(val[0]), float(32))

    def test_insert_parameters_locals(self):
        """

        :return:
        """
        I= pycotools3.model.InsertParameters(
            self.model,
            parameter_dict={
                # 'nuc': 85,
                'B': 35,
                'B2C_0_k2': 64,
                'A2B': 597,
            }, inplace=True).model
        val = [i.initial_value for i in self.model.global_quantities if i.name == 'A2B']
        self.assertAlmostEqual(float(val[0]), float(597))

    def test_insert_parameters_global_df(self):
        """

        :return:
        """
        parameter_dict = {'B': 35,
                          'B2C_0_k2': 64,
                          'A2B': 597}

        df = pandas.DataFrame(parameter_dict, index=[0])
        I= pycotools3.model.InsertParameters(
            self.model, df=df, inplace=True).model
        val = [i.initial_value for i in self.model.global_quantities if i.name == 'A2B']
        self.assertAlmostEqual(float(val[0]), float(597))

    def test_insert_parameters_metabolite_df(self):
        """

        :return:
        """
        parameter_dict = {'B': 35,
                          'B2C_0_k2': 64,
                          'A2B': 597}

        df = pandas.DataFrame(parameter_dict, index=[0])
        self.model = pycotools3.model.InsertParameters(self.model, df=df, inplace=True).model
        conc = [i.concentration for i in self.model.metabolites if i.name == 'B']
        self.assertAlmostEqual(float(conc[0]), float(35))


class InsertParameterTestsWithAssignments(unittest.TestCase):
    """
    May have found a bug when inserting parameters that are global
    variables and have assignments. This test was built to ensure
    everything is working correctly in this situation
    """

    def setUp(self):
        self.ant_str = """
        
        model TestyModel()
           R1: A => B ; k1*A 
           R2: B => C ; k2*B
           R3: C + A => D ; k3*C*A
           R4: D => ; k4*D
           
           k1 = 0.5
           k2 := k1
           k3 = 0.1
           k4 = 0.3
           
           A = 300
           B = 0
           C = 0
           D = 0
           
        end
        """

        self.cps_file = os.path.join(os.path.dirname(__file__), 'testy_model.cps')
        with pycotools3.model.BuildAntimony(self.cps_file) as loader:
            self.mod = loader.load(self.ant_str)


    def test_model_builds(self):
        """
        ensure antimony builds
        :return:
        """

        self.assertTrue(isinstance(self.mod, pycotools3.model.Model))

    def test_k2_is_assignment(self):
        ##
        k2 = self.mod.get('global_quantity', 'k2')
        self.assertEqual(k2.simulation_type, 'assignment')

    def test_insert_parameter_works(self):
        d = {'k3': 50, 'k1': 60}
        self.mod.insert_parameters(parameter_dict=d, inplace=True)
        self.assertEqual(self.mod.get('global_quantity', 'k1').initial_value, str(60.0))

    def test_insert_parameter_with_assignment(self):
        d = {'k2': 50, 'k1': 60}
        self.mod.insert_parameters(parameter_dict=d, inplace=True)
        '''
        Test not finished because I do not yet have mechanism for 
        accessing global variable expressions. 
        ## todo build expressions into global variables
        '''
        # self.mod.open()
        # self.assertEqual(self.mod.get('global_quantity', 'k1').initial_value, str(60.0))






class NewModelTests(unittest.TestCase):
    """
    tests relating to the development of new models from
    nothing.
    """
    def setUp(self):
        self.cps_file = os.path.join(os.path.dirname(__file__), 'NewModelTest.cps')
        self.cps_file2 = os.path.join(os.path.dirname(__file__), 'NewModelTest2.cps')

    def test_new_model_saves(self):#
        """
        Test that a new model is created and saved.
        :return:
        """
        model = pycotools3.model.Model(self.cps_file, new=True)
        model.save()

    # def test_compartment(self):
    #     """
    #     Test we can make a new compartment
    #     in a empty model
    #     :return:
    #     """
    #     model = pycotools3.model.Model(self.cps_file, new=True)
    #     model = model.add('compartment', 'NewCompartment')
    #     comp = model.get('compartment', 'NewCompartment')
    #     self.assertEqual(comp.name, 'NewCompartment')
    #
    # def test_metabolite(self):
    #     """
    #     Test we can make a new metabolite
    #     in a empty model
    #     :return:
    #     """
    #     model = pycotools3.model.Model(self.cps_file, new=True)
    #     model = model.add('metabolite', 'NewMetabolite')
    #     model.save()
    #     metab = model.get('metabolite', 'NewMetabolite')
    #     self.assertEqual(metab.name, 'NewMetabolite')

    def test_global(self):
        """
        Test we can make a new global
        in a empty model
        :return:
        """
        model = pycotools3.model.Model(self.cps_file, new=True)
        model = model.add_component('global_quantity', 'NewGlob')
        glo = model.get('global_quantity', 'NewGlob')
        self.assertEqual(glo.name, 'NewGlob')

    def tearDown(self):
        # pass
        if os.path.isfile(self.cps_file):
            os.remove(self.cps_file)
        if os.path.isfile(self.cps_file2):
            os.remove(self.cps_file2)


class TestReactionStuff(unittest.TestCase):
    def setUp(self):
        self.cps = os.path.join(os.path.dirname(__file__), 'test_model_2.cps')
        if os.path.isfile(self.cps):
            os.remove(self.cps)
        self.mod = pycotools3.model.Model(self.cps, new=True)
        self.Y = pycotools3.model.Reaction(self.mod, 'Y', '-> Y; Z X', '-X*Z + r*X - Y')
        self.X = pycotools3.model.Reaction(self.mod, 'X', '-> X; Y', 'sigma*(Y-X)')
        self.Z = pycotools3.model.Reaction(self.mod, 'Z', '-> Z; X Y', 'X*Y - b*Z ')


    def test_expression1(self):
        expr = 'sigma*(Y-X)'
        E = pycotools3.model.Expression(expr)
        self.assertListEqual(
            E.to_list(), sorted(['sigma', 'Y', 'X']
        ))

    def test_expression2(self):
        expr = '-X*Z + r*X -Y'
        E = pycotools3.model.Expression(expr)
        self.assertListEqual(
            E.to_list(), sorted(['X', 'Y', 'Z', 'r'])
        )

    def test_add_two_reactions(self):
        r1 = pycotools3.model.Reaction(self.mod, '1', 'q -> w', 'k*k2*q')
        self.mod.add_reaction(r1)
        r2 = pycotools3.model.Reaction(self.mod, '2', 'e -> r', 'k3*k4*e')
        self.mod.add_reaction(r2)
        self.assertEqual(len(self.mod.reactions), 2)

    def test_add_x(self):
        self.mod.add_reaction(self.X)
        self.mod.save()
        mod_tag = '{http://www.copasi.org/static/schema}Model'
        reactions_tag = '{http://www.copasi.org/static/schema}ListOfReactions'
        for i in self.mod.xml.find(mod_tag).find(reactions_tag):
            self.assertEqual(i.attrib['name'], 'X')

    # def test_add_x_alternative(self):
    #     print self.mod.add('metabolite', name='A')
        # r_kwargs = {'name': 'X', 'expression': '-> X', 'rate_law': 'k'}
        # self.mod.add2('reaction', reaction_kwargs=r_kwargs)
        # self.mod.add('reaction', name='X', '-> X', '-X*Z + r*X - Y')
        # self.mod.save()
        # mod_tag = '{http://www.copasi.org/static/schema}Model'
        # reactions_tag = '{http://www.copasi.org/static/schema}ListOfReactions'
        # for i in self.mod.xml.find(mod_tag).find(reactions_tag):
        #     self.assertEqual(i.attrib['name'], 'X')

    def test_add_y(self):
        self.mod.add_reaction(self.Y)
        self.mod.save()
        mod_tag = '{http://www.copasi.org/static/schema}Model'
        reactions_tag = '{http://www.copasi.org/static/schema}ListOfReactions'

        for i in self.mod.xml.find(mod_tag).find(reactions_tag):
            self.assertEqual(i.attrib['name'], 'Y')

    def test_add_z(self):
        self.mod.add_reaction(self.Z)
        self.mod.save()
        mod_tag = '{http://www.copasi.org/static/schema}Model'
        reactions_tag = '{http://www.copasi.org/static/schema}ListOfReactions'

        for i in self.mod.xml.find(mod_tag).find(reactions_tag):
            self.assertEqual(i.attrib['name'], 'Z')

    def test_add_xy(self):
        self.mod.add_reaction(self.X)
        self.mod.add_reaction(self.Y)
        self.assertEqual(len(self.mod.reactions), 2)
        self.assertEqual(len(self.mod.functions), 2)
        self.assertEqual(len(self.mod.metabolites), 3)
        self.assertEqual(len(self.mod.global_quantities), 0)
        self.assertEqual(len(self.mod.compartments), 1)

    def test_add_xyz(self):
        self.mod.add_reaction(self.X)
        self.mod.add_reaction(self.Y)
        self.mod.add_reaction(self.Z)
        self.assertEqual(len(self.mod.reactions), 3)
        self.assertEqual(len(self.mod.metabolites), 3)

    def tearDown(self):
        if os.path.isfile(self.cps):
            os.remove(self.cps)



class BuildWithAntimony(unittest.TestCase):

    def setUp(self):
        self.antimony_str = 'S1 -> S2; k1*S1; k1 = 0.1; S1 = 10'
        self.cps = os.path.join(os.path.dirname(__file__), 'antimony_model.cps')
        if os.path.isfile(self.cps):
            os.remove(self.cps)

    def tearDown(self):
        if os.path.isfile(self.cps):
            os.remove(self.cps)

    def test_build_with_antimony(self):
        # mod = pycotools3.model.Model(self.cps, new=True)
        with pycotools3.model.BuildAntimony(self.cps) as loader:
            mod = loader.load(
                'S1 -> S2; k1*S1; k1 = 0.1; S1 = 10'
            )
        self.assertTrue(type(mod), pycotools3.model.Model)
        # print pycotools3.viz.PlotTimeCourse(tasks.timecourse(end=100, intervals=100, step_size=1), savefig=True)



# class FitItemOrderWithConstraingsTests(unittest.TestCase):
#
#     def setUp(self):
#         self.antimony_str = 'S1 -> S2; k1*S1; k1 = 0.1; S1 = 10'
#         self.cps = os.path.join(os.path.dirname(__file__), 'antimony_model.cps')
#         if os.path.isfile(self.cps):
#             os.remove(self.cps)
#
#         with pycotools3.model.BuildAntimony(self.cps) as loader:
#             mod = loader.load(
#                 'S1 -> S2; k1*S1; k1 = 0.1; S1 = 10'
#             )
#
#         ## simulate some data
#         pycotools3.tasks.TimeCourse(mod, end=100, intervals=100, step_size=1)
#
#
#
#     def tearDown(self):
#         if os.path.isfile(self.cps):
#             os.remove(self.cps)
#
#     def test(self):
#         pass


if __name__ == '__main__':
    # pass
    unittest.main()



