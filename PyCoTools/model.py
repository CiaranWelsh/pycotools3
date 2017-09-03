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

import logging
import os
from collections import OrderedDict, Counter
from random import randint

from lxml import etree

# site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
# import PyCoTools
import Errors
import _base
import pycopi
import pandas

LOG = logging.getLogger(__name__)


## TODO add list of reports property to model
## TODO after running a task, bind the results to the model instance so that they are retrievable
class Model(_base._Base):
    def __init__(self, copasi_file, **kwargs):
        super(Model, self).__init__(**kwargs)
        self.copasi_file = copasi_file
        self.xml = pycopi.CopasiMLParser(copasi_file).copasiML
        ## fill this dict after class is finished
        self.default_properties = {}
        self.update_kwargs(kwargs)

    def __str__(self):
        return 'Model(name={}, time_unit={}, volume_unit={}, quantity_unit={})'.format(self.name, self.time_unit,self.volume_unit, self.quantity_unit)

    def __repr__(self):
        return self.__str__()

    def refresh(self):
        """

        :return:
        """
        self.xml = pycopi.CopasiMLParser(self.copasi_file).copasiML
        return self

    @property
    def reference(self):
        return "CN=Root,Model={}".format(self.name)

    @property
    def time_unit(self):
        """
        :return:
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['timeUnit']

    @property
    def name(self):
        """
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['name']

    @name.setter
    def name(self, name):
        """
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        self.xml.xpath(query)[0].attrib['name'] = str(name)
        return self

    @property
    def volume_unit(self):
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['volumeUnit']

    @property
    def quantity_unit(self):
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['quantityUnit']

    @property
    def area_unit(self):
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['areaUnit']

    @property
    def length_unit(self):
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['lengthUnit']

    @property
    def avagadro(self):
        """
        Not really needed but good to check
        consistancy of avagadros number.
            **since the number was changed
              between version 16 and 19
        :return: numeric
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        avagadro_from_model = float(self.xml.xpath(query)[0].attrib['avogadroConstant'])
        avagadros_from_version19 = 6.022140857e+23
        if avagadro_from_model != avagadros_from_version19:
            raise Errors.AvagadrosError('Avagadro from model {} is not equal to {}. Check to see whether COPASI have updated the value of avagadro\'s number'.format(avagadro_from_model, avagadros_from_version19))
        return avagadro_from_model

    @property
    def key(self):
        """
        Get the model reference - the 'key' from self.get_model_units
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['key']



    @property
    def states(self):
        """
        The states (metabolites and globals) in the order they
        are read by Copasi from the StateTemplate element.
        :Returns: set.
        """
        collection = []
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}StateTemplate':
                for j in i:
                    collection.append(j.attrib['objectReference'])

        query = '//*[@type="initialState"]'
        for i in self.xml.xpath(query):
            state_values = i.text

        state_values = state_values.split(' ')
        state_values = [i for i in state_values if i not in ['',' ', '\n']]
        state_values = [float(i) for i in state_values]

        return OrderedDict(zip(collection, state_values))

    @states.setter
    def states(self, states):
        """
        :param states: list of number of len(self.states)
        :return:
        """
        ## first check what data type states is
        if not isinstance(states, str):
            ## if not str then convert list to str in appropriate format
            state_string = reduce(lambda x, y: '{} {}'.format(x, y), states)

        ## get number of model states
        number_of_model_states = len(self.states)

        ##check we have correct number of model states
        if len(states) != number_of_model_states:
            raise Errors.InputError('Not entered the currect number of states. Expected {} and got {}'.format(number_of_model_states, len(states)))

        ## enter states into model
        query = '//*[@type="initialState"]'
        for i in self.xml.xpath(query):
            i.text = state_string
        return self

    def add_state(self, state, value):
        """
        Append state on to end of state template.
        Used within add_metabolite and add_global_quantity. Shouldn't
        need to use manually
        :param state: A valid key
        :param value: Amount for value
        :return:
        """
        element = etree.Element('StateTemplateVariable', attrib={'objectReference': state})
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}StateTemplate':
                i.append(element)
                for j in i.getparent():
                    if j.tag =='{http://www.copasi.org/static/schema}InitialState':
                        j.text = "{} {} \n".format(j.text.replace('\n', '').strip(), str(value) ) # + '\n'
        return self

    def remove_state(self, state):
        """
        Remove state from StateTemplate and
        InitialState fields. USed for deleting metabolites
        and global quantities.
        :param state: key of state to remove (i.e. Metabolite_1)
        :return: Model
        """
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}StateTemplate':
                count = -1 #0 indexed python
                for j in i:
                    count += 1
                    if j.attrib['objectReference'] == state:
                        j.getparent().remove(j)

        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}InitialState':
                states = i.text.strip().split(' ')
                del states[count]  ## get component of interest
        #reassign the states list to the InitialState
        states = [float(i) for i in states]
        self.states = states
        return self

    @property
    def compartments(self):
        """
        Get dict of compartments. dict[compartment_name] = corresponding xml code as nested dict
        """
        collection= {}
        lst = []
        for i in self.xml.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfCompartments':
                df_list = []
                for j in i:
                    lst.append(Compartment(self,
                                           key=j.attrib['key'],
                                           name=j.attrib['name'],
                                           simulation_type=j.attrib['simulationType'],
                                           initial_value=float(self.states[j.attrib['key']])) )
        return lst

    def add_compartment(self, compartment):
        """
        Add compartment to model
        :param compartment: Compartment
        :return: model.Model
        """
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfCompartments':
                i.append(compartment.to_xml())

        ## add compartment to state template
        self.add_state(compartment.key, compartment.initial_value)

        return self

    def remove_compartment(self, value, by='name'):
        """
        Remove a compartment with the attribute given
        as the 'by' and value arguments
        :param value: Value to match i.e. Nucleus
        :param by: attribute i.e. 'name' or 'key'
        :return: model.Model
        """
        ## get the compartment
        comp = self.get('compartment', value, by=by)
        if comp == []:
            raise Errors.ComponentDoesNotExistError('Component with {}={} does not exist'.format(by, value))

        ## first remove compartment from list of compartments
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfCompartments':
                for j in i:
                    if j.attrib[by] == value:
                        j.getparent().remove(j)

        ## then remove from state template and initial state
        self.remove_state(comp.key)
        return self

    @property
    def all_variable_names(self):
        """
        The names of all metabolites, global quantities
        and local parameters in the model.
        :return: list of str
        """
        m = [i.name for i in self.metabolites]
        g = [i.name for i in self.global_quantities]
        l = [i.global_name for i in self.local_parameters]
        return m + g + l

    @staticmethod
    def convert_particles_to_molar(particles, mol_unit, compartment_volume):#,vol_unit):
        '''
        Converts particle numbers to Molarity.
        particles=number of particles you want to convert
        mol_unit=one of, 'fmol, pmol, nmol, umol, mmol or mol'
        '''
        mol_dct={
            'fmol':1e-15,
            'pmol':1e-12,
            'nmol':1e-9,
            u'\xb5mol':1e-6,
            'mmol':1e-3,
            'mol':float(1),
            'dimensionless':float(1),
            '#':float(1)}
        mol_unit_value=mol_dct[mol_unit]
        avagadro=6.022140857e+23
        molarity=float(particles)/(avagadro*mol_unit_value*compartment_volume)
        if mol_unit=='dimensionless':
            molarity=float(particles)
        if mol_unit=='#':
            molarity=float(particles)
        return molarity

    @staticmethod
    def convert_molar_to_particles(moles, mol_unit, compartment_volume):
        '''
        Converts particle numbers to Molarity.
        particles=number of particles you want to convert
        mol_unit=one of, 'fmol, pmol, nmol, umol, mmol or mol'
        '''
        if isinstance(compartment_volume,(float,int))!=True:
            raise Errors.InputError('compartment_volume is the volume of the compartment for species and must be either a float or a int')

        mol_dct={
            'fmol':1e-15,
            'pmol':1e-12,
            'nmol':1e-9,
            u'\xb5mol':1e-6,
            'mmol':1e-3,
            'mol':float(1),
            'dimensionless':1,
            '#':1}
        mol_unit_value=mol_dct[mol_unit]
        avagadro=6.022140857e+23
        particles=float(moles)*avagadro*mol_unit_value*compartment_volume
        if mol_unit=='dimensionless':# or '#':
            particles=float(moles)
        if mol_unit=='#':
            particles=float(moles)
        return particles


    @property
    def metabolites(self):
        metabs = {}
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfMetabolites':
                for j in i:
                    metabs[j.attrib['key']] = j.attrib

        for key, value in self.states.items():
            if key in metabs.keys():
                metabs[key]['particle_number'] = str(value)


        lst = []
        for key in metabs:
            comp = self.get('compartment',
                     metabs[key]['compartment'],
                     'key')
            lst.append(Metabolite(self, name=metabs[key]['name'],
                                  compartment=comp,
                                  key=metabs[key]['key'],
                                  particle_number=metabs[key]['particle_number'],
                                  concentration=self.convert_particles_to_molar(
                                      metabs[key]['particle_number'], self.quantity_unit, comp.initial_value),
                                  simulation_type=metabs[key]['simulationType']))

        return lst

    def add_metabolite(self, metab):
        """
        Add a metabolite to the model xml
        :param metab:
        :return:
        """

        if not isinstance(metab, Metabolite):
            raise Errors.InputError('Input must be Metabolite class')

        metabolite_element = metab.to_xml()
        ## add the metabolute to list of metabolites
        list_of_metabolites = '{http://www.copasi.org/static/schema}ListOfMetabolites'
        for i in self.xml.iter():
            if i.tag == list_of_metabolites:
                i.append(metabolite_element)

        ## add metabolite to state_template and initial state fields
        self.add_state(metab.key, metab.particle_number)

        return self


    def remove_metabolite(self, value, by='name'):
        """
        Remove metabolite from model.
        :param value: value of the by argument (i.e. A)
        :param by: attribute to match (i.e. name)
        :return:
        """
        list_of_metabolites = '{http://www.copasi.org/static/schema}ListOfMetabolites'
        metab = self.get('metabolite', value, by=by)
        for i in self.xml.iter():
            if i.tag == list_of_metabolites:
                for j in i:
                    if j.attrib[by] == value:
                        j.getparent().remove(j)
        self.remove_state(metab.key)
        return self

    def add_global_quantity(self, global_quantity):
        """

        :param name: name of global quantity to be added
        :param key:  unique id for global quantity. Automatically assigned if left None
        :param initial_value: amount at simulation start time
        :param simulation_type: fixed, ode assignment or reactions
        :return: model.Model
        """
        if not isinstance(global_quantity, GlobalQuantity):
            raise Errors.InputError('Input must be a GlobalQuantity')

        model_value = global_quantity.to_xml()
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                i.append(model_value)

        self.add_state(global_quantity.key, global_quantity.initial_value)

        return self



    @property
    def global_quantities(self):
        """

        :return:
        """
        model_values = {}
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                for j in i:
                    model_values[j.attrib['key']] = j.attrib

        for key, value in self.states.items():
            if key in model_values.keys():
                model_values[key]['initial_value'] = str(value)

        lst = []
        for key in model_values:
            lst.append(GlobalQuantity(self, name=model_values[key]['name'],
                                      key=model_values[key]['key'],
                                      simulation_type=model_values[key]['simulationType'],
                                      initial_value=model_values[key]['initial_value']))
        return lst

    def remove_global_quantity(self, value, by='name'):
        """
        Remove a global quantity from your model
        :param value: value to match by (i.e. ProterinA or ProteinB)
        :param by: attribute to match (i.e. name or key)
        :return: model.Model
        """

        global_value = self.get('global_quantity',
                                value,
                                by)
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                for j in i:
                    if j.attrib[by] == value:
                        j.getparent().remove(j)

        self.remove_state(global_value.key)
        return self


    # @property
    @property
    def functions(self):
        """
        get model functions
        :return: return list of functions from ListOfFunctions
        """
        lst = []
        for element in self.xml.iter():
            if element.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
                for child in list(element):
                    name = child.attrib['name']
                    key = child.attrib['key']
                    type = child.attrib['type']
                    reversible = child.attrib['reversible']
                    list_of_parameter_descriptions = []
                    for grandchild in child:
                        if grandchild.tag == '{http://www.copasi.org/static/schema}Expression':
                            expression = grandchild.text.replace('\n', '').strip()

                        if grandchild.tag == '{http://www.copasi.org/static/schema}ListOfParameterDescriptions':
                            for greatgrandchild in grandchild:
                                list_of_parameter_descriptions.append(
                                    ParameterDescription(self,
                                                         name=greatgrandchild.attrib['name'],
                                                         key=greatgrandchild.attrib['key'],
                                                         order=greatgrandchild.attrib['order'],
                                                         role=greatgrandchild.attrib['role']) )
                    lst.append(Function(self,
                                        name=name,
                                        key=key,
                                        type=type,
                                        expression=expression,
                                        reversible=reversible,
                                        list_of_parameter_descriptions=list_of_parameter_descriptions))
        return lst

    # def add_function(self, name, expression, role, type='user_defined',
    #                  key=None, reversible=False):

    @property
    def parameter_descriptions(self):
        """

        :return:
        """
        lst = []
        for i in self.xml.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ParameterDescription':
                lst.append(ParameterDescription(self,
                                                name=i.attrib['name'],
                                                key=i.attrib['key'],
                                                order=i.attrib['order'],
                                                role=i.attrib['role'] ) )
        return lst


    def add_function(self, function):
        """

        :param name:
        :param expression:
        :param type:
        :param key:
        :param reversible:
        :return:
        """
        if function.key == None:
            function.key = KeyFactory(self, type='function').generate()

        if function.type == 'user_defined':
            function.type = 'UserDefined'

        if function.reversible == True:
            function.reversible = 'true'
        else:
            function.reversible = 'false'

        ## add the function to list of functions
        if function.key in [i.key for i in self.functions]:
            return self
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
                i.append(function.to_xml())

        return self

    def remove_function(self, value, by='name'):
        """
        remove a function with attribute specified with by and
        value with value
        :param value: string to match atttribute (i.e the functions name)
        :param by: attribute of function. default='name'
        :return: model.Model
        """
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
                for j in i:
                    if j.attrib[by] == value:
                        j.getparent().remove(j)
        return self

    @property
    def number_of_reactions(self):
        count = 0
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in list(i):
                    count = count + 1
        return count

    @property
    def constants(self):
        """

        :return:
        """
        res = []
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                for j in i:
                    name = j.attrib['name']
                    value = j.attrib['value']
                    key = j.attrib['key']
                    reaction_name = i.getparent().attrib['name']
                    global_name = '({}).{}'.format(reaction_name, name)

                    l = LocalParameter(self,
                                       name=name,
                                       value=value,
                                       key=key,
                                       reaction_name=reaction_name,
                                       global_name=global_name)
                    res.append(l)

        return res

    @property
    def reactions(self):
        # self.refresh()
        # self.open()
        list_of_reactions = []
        reaction_count = 0
        reactions_dict = {}
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in list(i):
                    reaction_count += 1
                    reactions_dict[reaction_count] = {}
                    ##defaults
                    reactions_dict[reaction_count]['reversible'] = 'false'
                    ## sometimes these are not being updated
                    reactions_dict[reaction_count]['substrates'] = []
                    reactions_dict[reaction_count]['products'] = []
                    reactions_dict[reaction_count]['modifiers'] = []
                    reactions_dict[reaction_count]['constants'] = []
                    reactions_dict[reaction_count]['function'] = []#ListOfSubstrates
                    for k in list(j):
                        reactions_dict[reaction_count]['reversible'] = j.attrib['reversible']
                        reactions_dict[reaction_count]['name'] = j.attrib['name']
                        reactions_dict[reaction_count]['key'] = j.attrib['key']
                        if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
                            for l in list(k):
                                list_of_substrates = [m for m in self.metabolites if m.key in l.attrib['metabolite']]

                                ## convert list to substrates
                                list_of_substrates = [m.to_substrate() for m in list_of_substrates]
                                reactions_dict[reaction_count]['substrates']= list_of_substrates
                        elif k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
                            for l in list(k):
                                ## get list of metabolites and convert them to Product class
                                list_of_products = [m for m in self.metabolites if m.key in l.attrib['metabolite']]
                                list_of_products = [m.to_product() for m in list_of_products]
                                #
                                reactions_dict[reaction_count]['products'] = list_of_products

                        elif k.tag == '{http://www.copasi.org/static/schema}ListOfModifiers':
                            for l in list(k):
                                ## get list of metabolites and convert them to Moifier class
                                list_of_modifiers = [m for m in self.metabolites if m.key in l.attrib['metabolite']]
                                list_of_modifiers = [m.to_modifier() for m in list_of_modifiers]
                                reactions_dict[reaction_count]['modifiers'] = list_of_modifiers

                        elif k.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                            list_of_constants = []
                            for l in list(k):
                                list_of_constants.append(
                                    LocalParameter(self,
                                                   key=l.attrib['key'],
                                                   name=l.attrib['name'],
                                                   value=l.attrib['value'],
                                                   reaction_name=j.attrib['name'],
                                                   global_name="({}).{}".format(j.attrib['name'], l.attrib['name'])))
                                reactions_dict[reaction_count]['constants'] = list_of_constants


                        elif k.tag == '{http://www.copasi.org/static/schema}KineticLaw':
                            function_list = [m for m in self.functions if m.key == k.attrib['function']]
                            assert len(function_list) == 1
                            reactions_dict[reaction_count]['function'] = function_list[0]

        for i, dct in reactions_dict.items():
            if dct['function'] == []:
                dct['function'] = "k*{}".format(reduce(lambda x, y: '{}*{}'.format(x, y), substrates))

            substrates = [j.name for j in reactions_dict[i]['substrates']]
            if substrates != []:
                sub_expression = reduce(lambda x, y: "{} + {}".format(x, y), substrates)
            else:
                sub_expression = ''

            products = [j.name for j in reactions_dict[i]['products']]
            if products != []:
                prod_expression = reduce(lambda x, y: "{} + {}".format(x, y), products)
            else:
                prod_expression = ''

            modifiers = [j.name for j in reactions_dict[i]['modifiers']]
            if modifiers != []:
                modifier_expression = reduce(lambda x, y: "{} + {}".format(x, y), modifiers)
            else:
                modifier_expression = ''

            if reactions_dict[i]['reversible'] == 'true':
                operator = '='
            elif reactions_dict[i]['reversible'] == 'false':
                operator = '->'
            else:
                raise Errors.SomethingWentHorriblyWrongError

            if modifier_expression == '':
                expression = "{} {} {}".format(sub_expression,
                                               operator,
                                               prod_expression)
            else:
                expression = '{} {} {}; {}'.format(sub_expression, operator,
                                                   prod_expression, modifier_expression)
            reactions_dict[i]['expression'] = expression

        lst=[]

        for i, dct in reactions_dict.items():
            ## skip the skipped reactions
            # if i not in skipped:
            lst.append(Reaction(self,
                            name=dct['name'],
                            key=dct['key'],
                            expression=dct['expression'],
                            rate_law=dct['function']))

        return lst

    def add_reaction(self, reaction):
        """

        :param reaction: reaction as you would type into copasi
        :param rate_law: mathematical expression or mass_action (default)
        :return:
        """
        if reaction.key in [i.key for i in self.reactions]:
            raise Errors.ReactionAlreadyExists('Your model already contains a reaction with the key: {}'.format(reaction.key))

        if reaction.name in [i.name for i in self.reactions]:
            raise Errors.ReactionAlreadyExists('Your model already contains a reaction with the name: {}'.format(reaction.name))

        existing_functions = [i.expression for i in self.functions]
        if reaction.rate_law.expression not in existing_functions:
            self.add_function(reaction.rate_law)


        # print reaction.to_xml()
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                i.append(reaction.to_xml())
        return self

    def remove_reaction(self, value, by='name'):
        """
        Remove reaction matched by value
        :param value: value to match reaction by
        :param by: attribute of reaction to match default='name
        :return:
        """

        ##Now because of what I've done with
        ##the reactions property (bypass reactions with empty substrates and
        ## products, it seems that I cannot find the reaction
        ## here which is why it is not being removed.

        ##Why does the new reaction give empty lists of substrates
        ## and products?
        reaction = self.get('reaction', value, by)
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    if j.attrib[by] == value:
                        j.getparent().remove(j)
        return self

    def save(self, copasi_file=None):
        """
        Save copasiML to copasi_filename. This
        version is not static and already
        knows which copasiML you want to save

        :param copasi_filename:
        :return:
        """
        if copasi_file == None:
            copasi_file = self.copasi_file

        # first convert the copasiML to a root element tree
        # root = etree.ElementTree(self.xml)

        ## Then remove existing copasi file for ovewrite
        if os.path.isfile(copasi_file):
            os.remove(copasi_file)

        with open(copasi_file, 'w') as f:
            f.write(etree.tostring(self.xml, pretty_print=True))
        # self.xml.getroot().write(copasi_file)
        self.refresh()
        return self

    def open(self, copasi_file=None):
        """
        Open model with the gui
        :return:
        """
        if copasi_file == None:
            copasi_file = self.copasi_file
        self.save(copasi_file)
        os.system('CopasiUI {}'.format(copasi_file))
        # os.remove(copasi_file)

    def _model_components(self):
        """
        list of model components that
        are changable
        :return:
        """
        return ['metabolite','compartment', 'reaction',
                'local_parameter','global_quantity',
                'function']

    def get(self, component, value, by='name'):
        """
        Factory method
        get a model component by a value of a certain type
        :param component: the component i.e. metabolite or local_parameter
        :param value: value of the attribute to match by i.e. metabolite called A
        :param by: which attribute to search by. i.e. name or key or value
        :return: component
        """
        if component not in self._model_components():
            raise Errors.InputError('{} not in list of components: {}'.format(component, self._model_components()))

        if component == 'metabolite':
            res = [i for i in self.metabolites if getattr(i, by) == value]

        elif component == 'compartment':
            res = [i for i in self.compartments if getattr(i, by) == value]

        elif component == 'local_parameter':
            res = [i for i in self.constants if getattr(i, by) == value]

        elif component == 'global_quantity':
            res = [i for i in self.global_quantities if getattr(i, by) == value]

        elif component == 'function':
            res = [i for i in self.functions if getattr(i, by) == value]

        elif component == 'reaction':
            res = [i for i in self.reactions if getattr(i, by) == value]

        if len(res) == 1:
            res = res[0]
        return res

    def set(self, component, match_value, new_value,
            match_field='name', change_field='initial_value'):
        """

        :param component: metabolite, compartment, global_quantity, constant, reaction
        :param name: name of the attribute to change (i.e. species 'X', if attribute='name)
        :param value: new value for component attibute
        :param attribute: attribute of component to change (i.e. name or value)
        :return:
        """
        if component not in self._model_components():
            raise Errors.InputError('{} not in list of components'.format(component))

        ##get the component of interest
        comp = self.get(component, match_value, by=match_field)

        if isinstance(comp, list):
            raise Errors.SomethingWentHorriblyWrongError(
                'model.get has returned a list --> {}'.format(comp)
            )

        ##cater for special case when changing concentration.
        ## --> Only change metabolite particle number
        if component == 'metabolite':
            if change_field == 'concentration':
                new_value = self.convert_molar_to_particles(
                    new_value,
                    self.quantity_unit,
                    comp.compartment.initial_value
                )
                ##now change the field of interest to particle number
                change_field = 'particle_number'
        ## set the attribute
        setattr(comp, change_field, new_value)

        ##remove component of interest from model
        self.remove(component, match_value)

        ##add back to model with new attribute
        return self.add(component, comp)

    def set_metabolite(self, name, value, attribute='concentration'):
        """

        :return:
        """
        if name not in [i.name for i in self.metabolites]:
            raise Errors.InputError('metabolite "{}" does not exist'.format(name))

        metab= self.get('metabolite', 'X', by='name')

        ##If we want to set the concentration
        ##first convert to particle numbers
        if attribute == 'concentration':
            value = self.convert_molar_to_particles(value,
                                                    self.quantity_unit,
                                                    metab.compartment.initial_value)
            attribute = 'particle_number'

        ## set the attribute

        setattr(metab, attribute, value)
        ##remove component of interest from model
        self.remove('metabolite', name)

        ##add back to model with new attribute
        model = self.add('metabolite', metab)
        return model

    def add(self, component_name, component):
        """
        add a model component to the model
        :param component_name: i.e. 'reaction', 'function', 'metabolite
        :param component: the component class to add i.e. Metabolite
        :return:
        """
        if component_name not in self._model_components():
            raise Errors.InputError('"{}" not valid. These are valid: {}'.format(component_name, self._model_components()))

        if component_name == 'metabolite':
            #TODO work out whether this below bit is needed
            # if component_name in [i.name for i in self.metabolites]:
            #     self.remove('metabolite', component_name)
            return self.add_metabolite(component)

        elif component_name == 'function':
            return self.add_function(component)

        elif component_name == 'reaction':
            return self.add_reaction(component)

        elif component_name == 'global_quantity':
            return self.add_global_quantity(component)

        elif component_name == 'compartment':
            return self.add_compartment(component)

    def remove(self, component, name):
        """

        :param component:
        :param name:
        :param value:
        :return:
        """
        if component in self._model_components() == False:
            raise Errors.InputError('{} not in list of components'.format(component))

        if component == 'compartment':
            return self.remove_compartment(name, by='name')

        elif component == 'global_quantity':
            return self.remove_global_quantity(name, by='name')

        elif component == 'reaction':
            return self.remove_reaction(name, by='name')

        elif component == 'function':
            return self.remove_function(name, by='name')

        elif component == 'metabolite':
            return self.remove_metabolite(name, by='name')

        else:
            raise Errors.InputError('{} is not an accepted type. Choose from: {}'.format(self._model_components()))

    @property
    def active_parameter_set(self):
        """

        :return: get active parameter set
        """
        for i in self.xml.iter():
            if i.tag=='{http://www.copasi.org/static/schema}ListOfModelParameterSets':
                return i.attrib['active_set']

    @active_parameter_set.setter
    def active_parameter_set(self, parameter_set):
        """
        set the active parameter set
        :return:
        """
        if parameter_set not in self.active_parameter_set:
            raise Errors.InputError('{} not in available parameter sets'.format(parameter_set))

        for i in self.xml.iter():
            if i.tag=='{http://www.copasi.org/static/schema}ListOfModelParameterSets':
                i.attrib['active_set'] = parameter_set
        return self

    @property
    def parameter_sets(self):
        """

        :return:
        """
        for i in self.xml.iter():
            if i.tag=='{http://www.copasi.org/static/schema}ListOfModelParameterSets':
                for j in i:
                    print j


class Compartment(_base._ModelBase):
    def __init__(self, model, **kwargs):
        super(Compartment, self).__init__(model, **kwargs)
        default_properties = {'name': None,
                              'key': None,
                              'initial_value':None,
                              'simulation_type': 'fixed'}

        self.update_properties(default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(default_properties.keys(),
                             kwargs.keys())
        self._do_checks()


    def __str__(self):
        return 'Compartment(name={}, key={}, initial_value={})'.format(
            self.name, self.key, self.initial_value
        )

    def __repr__(self):
        return self.__str__()

    def _do_checks(self):
        """
        Make sure none of the arguments are empty
        :return: void
        """
        if self.key is None:
            self.key = KeyFactory(self.model, type='compartment').generate()

        if self.name is None:
            LOG.warning('name attribute for compartment not set. Defaulting to key --> {}'.format(self.key))
            self.name == self.key

        if self.simulation_type is None:
            self.simulation_type = 'fixed'

        if self.initial_value is None:
            self.initial_value = 1




    @property
    def reference(self):
        return 'Vector=Compartments[{}]'.format(self.name)

    def to_xml(self):
        """

        :return:
        """
        if self.key == None:
            self.key = KeyFactory(self.model, type='compartment').generate()

        simulation_types = ['reactions', 'ode', 'fixed', 'assignment']
        if self.simulation_type not in simulation_types:
            raise Errors.InputError('{} not in {}'.format(self.simulation_type, simulation_types))

        compartment_element = etree.Element('Compartment', attrib={'key': self.key,
                                                                   'name': self.name,
                                                                   'simulationType': self.simulation_type,
                                                                   'dimensionality': '3'})
        return compartment_element



class Metabolite(_base._ModelBase):
    """
    Metabolite class to hole attributes
    associated with a Metabolite.

    Concentration and particle numbers
    are separate. Calculate them in Model
    and assign from outside the Metabolite class
    becuse that way the metabolite class doesn't
    need to know about the Model

    """
    def __init__(self, model, **kwargs):
        super(Metabolite, self).__init__(model, **kwargs)
        self.default_properties = {'compartment':None,
                             'key':None,
                             'name':None,
                             'particle_number':None,
                             'concentration':None,
                             'simulation_type':None,
                             }

        for key in kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, self.default_properties) )
        self.update_properties(self.default_properties)
        ##update all keys to none
        self._do_checks()

    def __str__(self):
        return 'Metabolite(name="{}", key="{}", compartment="{}", concentration="{}", particle_number="{}", simulation_type="{}")'.format(
            self.name, self.key, self.compartment.name, self.concentration, self.particle_number,
            self.simulation_type)

    def __repr__(self):
        return self.__str__()

    def _do_checks(self):
        """

        :return:
        """
        if self.compartment == None:
            try:
                self.compartment = self.model.compartments[0]
            except IndexError:
                raise Errors.InputError('No compartments in your model')

        if self.compartment != None:
            if isinstance(self.compartment, Compartment)!=True:
                raise Errors.InputError('compartment argument should be of type PyCoTools.pycopi.Compartment')

        if ('particle_number' not in self.__dict__.keys()) and  ('concentration' not in self.__dict__.keys() ):
            raise Errors.InputError('Must specify either concentration or particle numbers')

        if self.simulation_type == None:
            self.simulation_type = 'reactions'

        if (self.concentration is None) and (self.particle_number is None):
            self.concentration = str(1)

        if (self.particle_number is None) and (self.concentration is not None):
            self.particle_number = self.model.convert_molar_to_particles(
                self.concentration,
                self.model.quantity_unit,
                self.compartment.initial_value
            )

        if (self.concentration is None) and (self.particle_number is not None):
            self.concentration = self.model.convert_particles_to_molar(
                self.particle_number,
                self.model.quantity_unit,
                self.compartment.initial_value
            )

        if self.key is None:
            self.key = KeyFactory(self.model, type='metabolite').generate()

        if not isinstance(self.particle_number, (float, int, str)):
            raise Errors.InputError('particle number should be float or int or string of numbers')


        if isinstance(self.particle_number, (float, int)):
            self.particle_number = str(self.particle_number)





    @property
    def initial_reference(self):
        """
        The copasi object reference for
        transient metabolite
        :return:
        """
        return 'Vector=Metabolites[{}],Reference=InitialConcentration'.format(self.name)

    @property
    def transient_reference(self):
        """
        The copasi object reference for
        transient metabolite
        :return:
        """
        return 'Vector=Metabolites[{}],Reference=Concentration'.format(self.name)

    @property
    def initial_particle_reference(self):
        """
        The copasi object reference for
        initial  metabolite particle numbers
        :return:
        """
        return 'Vector=Metabolites[{}],Reference=InitialParticleNumber'.format(self.name)

    @property
    def transient_particle_reference(self):
        """
        The copasi object reference for
        transient metabolite particle numbers
        :return:
        """
        return 'Vector=Metabolites[{}],Reference=ParticleNumber'.format(self.name)

    def to_substrate(self):
        return Substrate(self.model, **self.kwargs)

    def to_product(self):
        return Product(self.model, **self.kwargs)

    def to_modifier(self):
        return Modifier(self.model, **self.kwargs)

    def to_xml(self):
        """

        :return:
        """

        metabolite_element = etree.Element('Metabolite', attrib={'key': self.key,
                                                                 'name': self.name,
                                                                 'simulationType': self.simulation_type,
                                                                 'compartment': self.compartment.key})

        return metabolite_element


class Substrate(Metabolite):
    def __init__(self, model, **kwargs):
        super(Substrate, self).__init__(model, **kwargs)

        for key in self.kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('{} not in {}'.format(key, self.default_properties))
        self.update_properties(self.default_properties)

    def __str__(self):
        """

        :return:
        """
        return 'Substrate({})'.format(self.to_string())

    def __repr__(self):
        return self.__str__()


class Product(Metabolite):
    def __init__(self, model, **kwargs):
        super(Product, self).__init__(model, **kwargs)

        for key in self.kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('{} not in {}'.format(key, self.default_properties))

    def __str__(self):
        """

        :return:
        """
        return 'Product({})'.format(self.to_string())

    def __repr__(self):
        return self.__str__()


class Modifier(Metabolite):
    def __init__(self, model, **kwargs):
        super(Modifier, self).__init__(model, **kwargs)

        for key in self.kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('{} not in {}'.format(key, self.default_properties))

    def __str__(self):
        """

        :return:
        """
        return 'Modifier({})'.format(self.to_string())

    def __repr__(self):
        return self.__str__()

class GlobalQuantity(_base._ModelBase):
    """
    Global quantities have names and are associated with a vlue.
    This value can be constant or an assignment

    Type can be either fixed or assignment. If assignment
    value can be defined in terms of other model

    To Do:
        implement the assignment part of this class.
        Generally unless we're using this class to set assignment
        global variables they are not all that useful within pycotools. Since
        I'm not implementing 'setters' for PyCoTools just yet this feature
        is of lower priority.

    """
    def __init__(self, model, **kwargs):
        super(GlobalQuantity, self).__init__(model, **kwargs)

        self.default_properties = {'name': None,
                                   'key': None,
                                   'simulation_type': None,
                                   'initial_value': None,
                                   }

        for key in kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('Attribute not allowed. "{}" not in {}'.format(key, self.default_properties.keys()) )
        self.update_properties(self.default_properties)

        self._do_checks()

    def _do_checks(self):
        if self.simulation_type != None:
            if self.simulation_type not in ['fixed','assignment']:
                raise Errors.InputError('type should be either fixed or assignment. ODE not supported as Reactions can be used.')

        if self.simulation_type == 'assignment':
            Errors.NotImplementedError('Assignments not yet implemented')

        if self.name == None:
            raise Errors.InputError('name property cannot be None')

        if self.key == None:
            self.key = KeyFactory(self.model, type='global_quantity').generate()

        if self.initial_value is None:
            self.initial_value = 1

        if self.simulation_type is None:
            self.simulation_type = 'fixed'

    def __str__(self):
        return "GlobalQuantity(name='{}', key='{}', initial_value='{}', simulation_type='{}')".format(
            self.name,
            self.key,
            self.initial_value,
            self.simulation_type,
        )

    def __repr__(self):
        return self.__str__()

    @property
    def transient_reference(self):
        """
        compose the transient reference for the global quantity.
            i.e. not initial concentration
        :return: string
        """
        return "Vector=Values[{}],Reference=Value".format(self.name)

    @property
    def initial_reference(self):
        """
        compose the transient reference for the global quantity.
            i.e. not initial concentration
        :return: string
        """
        return "Vector=Values[{}],Reference=InitialValue".format(self.name)

    def to_xml(self):
        """

        :return:
        """
        if self.key == None:
            self.key = KeyFactory(self.model, type='global_quantity').generate()

        if self.simulation_type == None:
            self.simulation_type = 'fixed'

        if self.simulation_type not in ['assignment', 'fixed', 'ode', 'reactions']:
            raise TypeError('wrong simulation type')

        model_value = etree.Element('ModelValue', attrib={'key': self.key,
                                                          'name': self.name,
                                                          'simulationType': self.simulation_type})
        return model_value


    def insert_parameters(self):
        """
        class to insert parameters from dict, file, folder of files
        or pandas dataframe
        :return:
        """
        pass

class Reaction(_base._ModelBase):
    """
    Reactions have rectants, products, rate laws and parameters
    Not sure if this is a priority just yet


    Here's an idea. Would it be a good idea to have just
    a Parmeter class which a scope property which defines
    whether its a model parameter or specific to a individual
    reaction.
    """
    def __init__(self, model, **kwargs):
        super(Reaction, self).__init__(model, **kwargs)
        self.default_properties = {'name': None,
                                   'expression': None,
                                   'rate_law': None,
                                   'key': None,
                                   'substrates': [],
                                   'products': [],
                                   'modifiers': [],
                                   'reversible': False,
                                   ##TODO delete parameters as we have rate law instead
                                   'parameters': [],
                                   'parameters_dict': {},
                                   'fast': False,
                                   'simulation_type': 'reactions'}
        for key in self.kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('{} not valid key. Valid keys are: {}'.format(key, self.default_properties))
        self.update_properties(self.default_properties)

        self._do_checks()
        self.create()
        # print self.to_df()




    def __str__(self):
        return 'Reaction(name="{}", expression="{}", rate_law="{}", parameters={}, reversible={})'.format(
            self.name, self.expression, self.rate_law,
            {i.name: i.value for i in self.parameters},
            self.reversible
        )

    def __repr__(self):
        return self.__str__()

    def _do_checks(self):
        """


        :return:
        """
        if not isinstance(self.fast, bool):
            raise Errors.InputError('fast argument is boolean')

        if self.simulation_type is not None:
            if self.simulation_type not in ['fixed',
                                            'assignment',
                                            'reactions',
                                            'ode']:
                raise Errors.InputError('type should be either fixed or assignment. ODE not supported as Reactions can be used.')

        if self.key is None:
            self.key = KeyFactory(self.model, type='reaction').generate()

        if self.name is None:
            raise Errors.InputError('name property cannot be None')

        if self.simulation_type is None:
            self.simulation_type = 'fixed'

        if self.expression is None:
            raise Errors.InputError('expression is a required argument')

        if self.rate_law is None:
            raise Errors.InputError('rate_law is a required argument')


        if self.key is None:
            self.key = KeyFactory(self.model, type='reaction').generate()

        if self.name == None:
            self.name = self.key

    def translate_reaction(self):
        """
        convert the reaction string (self.expression)
        into lists of substrate, product, modifiers, constants.
        Assign reversible.
        :return:
        """

        trans = Translator(self.model, self.expression)
        self.substrates = trans.substrates
        self.products = trans.products
        self.modifiers = trans.modifiers
        self.reversible = trans.reversible


        reaction_components = [i.name for i in trans.all_components]


        if (self.rate_law is None) or (self.rate_law is []):
            raise Errors.InputError('rate_law is {}'.format(self.rate_law))

        if isinstance(self.rate_law, str):
            expression_components = Expression(self.rate_law).to_list()

        ## for handling existing functions
        elif isinstance(self.rate_law, Function):
            if 'mass action' in self.rate_law.name.lower():
                ##TODO add reversible here
                forward = reduce(
                    lambda x, y: '{}*{}'.format(
                        x, y), [i.name for i in self.substrates]
                )
                self.rate_law = 'k1*{}'.format(forward)
                if self.reversible in ['true', True]:
                    backward = reduce(
                        lambda x, y: '{}*{}'.format(
                            x, y), [i.name for i in self.products]
                        )
                    self.rate_law = 'k1*{}-k2*{}'.format(forward, backward)

                expression_components = Expression(self.rate_law).to_list()

            else:
                expression_components = Expression(self.rate_law.expression).to_list()


        parameter_list = []
        for i in expression_components:
            if i not in reaction_components:
                parameter_list.append(i)


        local_keys = KeyFactory(self.model, type='constant').generate(len(parameter_list))
        if isinstance(local_keys, str):
            local_keys = [local_keys]

        ##for excluding elements of built in rate laws
        exclusion_list = []#['PRODUCT<substrate_i>', 'PRODUCT<product_j>']
        for i in range(len(parameter_list)):
            if parameter_list[i] not in exclusion_list:
                p = LocalParameter(self.model,
                                   name=parameter_list[i],
                                   key=local_keys[i],
                                   value=0.1,
                                   reaction_name=self.name,
                                   global_name='({}).{}'.format(self.name, parameter_list[i]))
                self.parameters.append(p)
                self.parameters_dict[parameter_list[i]] = p

    def create_rate_law_function(self):
        """
        interpret the exression given for rate law
        and produce a pycotools function object
        :return:
        """

        ##todo check if ratelaw exists
        if isinstance(self.rate_law, str):
            if self.rate_law == 'mass_action':
                ma = MassAction(self.model, reversible=self.reversible)
                return ma
            else:
                exp = Expression(self.rate_law).to_list()
        elif isinstance(self.rate_law, Function):
            # return self.rate_law
            exp = Expression(self.rate_law.expression).to_list()
        role_dct = {}


        # if self.substrates + self.products == []:
        #     raise Errors.SomethingWentHorriblyWrongError('Both substrates and products are empty')

        for i in exp:
            if i in [j.name for j in self.substrates]:
                role_dct[i] = 'substrate'
            elif i in [j.name for j in self.products]:
                role_dct[i] = 'product'
            elif i in [j.name for j in self.modifiers]:
                role_dct[i] = 'modifier'
            else:
                role_dct[i] = 'parameter'


        function = Function(self.model, name=self.name,
                            expression=self.rate_law,
                            roles=role_dct)
        return function

    def create(self):
        """

        :return:
        """
        ## get lists of substrate, products, modifiers and constants

        self.translate_reaction()

        ## interpret rate law
        self.rate_law = self.create_rate_law_function()


    def to_xml(self):
        """

        :return:
        """
        if self.fast:
            self.fast = 'true'
        else:
            self.fast = 'false'

        if self.reversible:
            self.reversible = 'true'
        else:
            self.reversible = 'false'


        if isinstance(self.name, bool):
            raise Exception

        if isinstance(self.fast, bool):
            raise Exception

        reaction = etree.Element('Reaction', attrib={'key': self.key,
                                                     'name': self.name,
                                                     'reversible': self.reversible,
                                                     'fast': self.fast})
        list_of_substrates = etree.SubElement(reaction, 'ListOfSubstrates')
        for i in self.substrates:
            etree.SubElement(list_of_substrates, 'Substrate', attrib={'metabolite': i.key,
                                                                      'stoichiometry': str(i.stoichiometry)} )

        list_of_products = etree.SubElement(reaction, 'ListOfProducts')
        for i in self.products:
            etree.SubElement(list_of_products, 'Product', attrib={'metabolite': i.key,
                                                                  'stoichiometry': str(i.stoichiometry)})


        list_of_modifiers= etree.SubElement(reaction, 'ListOfModifiers')
        for i in self.modifiers:
            etree.SubElement(list_of_modifiers, 'Modifier', attrib={'metabolite': i.key,
                                                                   'stoichiometry': str(i.stoichiometry)})

        list_of_constants = etree.SubElement(reaction, 'ListOfConstants')

        for i in self.parameters:
            etree.SubElement(list_of_constants, 'Constant', attrib={'key': i.key,
                                                                    'name': i.name,
                                                                    'value': str(i.value)})

        if self.rate_law.name == 'mass_action':
            kinetic_law = self.rate_law.to_xml()

        else:
            kinetic_law = etree.SubElement(reaction,
                                       'KineticLaw',
                                       attrib={'function': self.rate_law.key,
                                               'unitType': 'Default',
                                               'scalingCompartment': "{},{}".format(
                                                   self.model.reference,
                                                   self.substrates[0].compartment.reference)})
            call_parameters = etree.SubElement(kinetic_law, 'ListOfCallParameters')
            for i in self.rate_law.list_of_parameter_descriptions:
                call_parameter = etree.SubElement(call_parameters,
                                                  'CallParameter',
                                                  attrib={'functionParameter': i.key})

                if i.role == 'constant':
                    ##TODO implement global quantities here
                    source_parameter = self.parameters_dict[i.name].key

                elif (i.role == 'substrate') or (i.role == 'product') or (i.role == 'modifier'):
                    source_parameter = self.model.get('metabolite', i.name, by='name').key


                etree.SubElement(call_parameter, 'SourceParameter', attrib={'reference': source_parameter})

        return reaction


class Function(_base._ModelBase):
    """
    Class to hold copasi function definitions for rate laws
    """

    def __init__(self, model, **kwargs):
        super(Function, self).__init__(model, **kwargs)
        default_properties = {'name': None,
                              'key': None,
                              'type': None,
                              'reversible': None,
                              'expression': None,
                              'list_of_parameter_descriptions': [],
                              'roles': {}}

        for key in self.kwargs:
            if key not in default_properties:
                raise Errors.InputError('{} not in {}'.format(key, default_properties))
        self.update_properties(default_properties)
        self._do_checks()
        self.list_of_parameter_descriptions = self.create_parameter_descriptions_from_roles()

        # self.create_mass_action()

    def __str__(self):
        return 'Function(name="{}", key="{}", expression="{}", roles={})'.format(
            self.name, self.key, self.expression,
            self.roles,
        )


    def __repr__(self):
        return self.__str__()

    def _do_checks(self):
        if self.reversible == None:
            self.reversible = 'false'

        if self.reversible:
            self.reversible = 'true'
        else:
            self.reversible = 'false'

        if self.type == None:
            self.type = 'user_defined'

        if not self.key:
            self.key = KeyFactory(self.model, type='function').generate()

        if self.name == None:
            self.name = self.key



    def create_parameter_descriptions_from_roles(self):
        """
        Use roles dict to create parameter descriptions
        :return:
        """
        if self.roles == None:
            return self.list_of_parameter_descriptions
        else:
            if not self.list_of_parameter_descriptions:
                # if self.roles == None:
                #     raise Errors.InputError('please specify either roles or list_of_parameter_descriptions')

                function_parameter_keys = KeyFactory(self.model, type='function_parameter').generate(len(self.roles))

                keys = self.roles.keys()
                values = self.roles.values()
                for i in range(len(self.roles)):
                    self.list_of_parameter_descriptions.append(
                        ParameterDescription(self.model,
                                             key=function_parameter_keys[i],
                                             name=keys[i],
                                             role=values[i],
                                             order=i) )
                return self.list_of_parameter_descriptions

    def to_xml(self):
        """
        write mass action function as xml element
        :return:
        """
        if self.reversible == None:
            raise Errors.SomethingWentHorriblyWrongError('reversible argument is None')

        if self.key == None:
            raise Errors.SomethingWentHorriblyWrongError('key argument is None')

        if self.name == None:
            self.name = self.expression

        if self.name == None:
            raise Errors.SomethingWentHorriblyWrongError('name argument is None')

        func = etree.Element('Function', attrib=OrderedDict({'key': self.key,
                                                             'name': self.name,
                                                             'type': 'UserDefined',
                                                             'reversible': self.reversible}) )

        expression = etree.SubElement(func, 'Expression')
        if isinstance(self.expression, str):
            expression.text = self.expression
        elif isinstance(self.expression, Function):
            expression.text = self.expression.expression
        else:
            raise TypeError(
                'self.expression is of type {} but expected str or function'.format(type(self.expression))
            )
        # expression.text = self.expression
        list_of_p_desc = etree.SubElement(func, 'ListOfParameterDescriptions')

        for i in self.list_of_parameter_descriptions:
            etree.SubElement(list_of_p_desc, 'ParameterDescription', attrib={'key': i.key,
                                                                             'name': i.name,
                                                                             'order': str(i.order),
                                                                             'role': i.role})

        return func


class ParameterDescription(_base._ModelBase):
    def __init__(self, model, **kwargs):
        super(ParameterDescription, self).__init__(model, **kwargs)
        default_properties = {'key': None,
                                   'name': None,
                                   'order' : 0,
                                   'role': 'substrate'}

        self.update_properties(default_properties)
        self.update_kwargs(self.kwargs)
        self.check_integrity(default_properties.keys(),
                             kwargs.keys())
        self._do_checks()

    def __str__(self):
        return 'ParameterDescription(name="{}", role="{}")'.format(
            self.name, self.role
        )

    def _do_checks(self):
        """
        verify integrity of user input
        :return:
        """
        if self.role == 'parameter':
            self.role = 'constant'
        elif self.role == None:
            self.role = 'constant'

        roles = ['constant', 'modifier', 'substrate', 'product']
        if self.role not in roles:
            raise Errors.InputError('{} is not one of {}'.format(self.role, roles))





class LocalParameter(_base._ModelBase):
    def __init__(self, model, **kwargs):
        super(LocalParameter, self).__init__(model, **kwargs)
        self.default_properties = {'name':None,
                                   'key':None,
                                   'value':None,
                                   'simulation_type':None,
                                   'parameter_type':None,
                                   'reaction_name': None,
                                   'global_name': None}
                                   # 'global_name': '({}).{}'.format(self.reaction_name,
                                   #                                 self.name)}


        for key in self.kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('{} not in {}'.format(key, self.default_properties))
        self.update_properties(self.default_properties)

        if self.name is None:
            raise Errors.InputError('Name is "{}"'.format(self.name))

        if self.key is None:
            raise Errors.InputError('Key is "{}"'.format(self.key))


    def __str__(self):
        return 'LocalParameter(name="{}", key="{}", reaction_name="{}, value={}")'.format(
            self.name, self.key, self.reaction_name, self.value
        )

    def __repr__(self):
        return self.__str__()

    @property
    def reference(self):
        return "Vector=Reactions[{}],ParameterGroup=Parameters,Parameter={},Reference=Value".format(self.reaction_name, self.name)


class LocalParameterList(list):
    def __init__(self):
        pass
## TODO create a LocalParameterList class which is like a normal list but with to_dict() and to_df() methods



class KeyFactory(_base._ModelBase):
    def __init__(self, model, **kwargs):
        super(KeyFactory, self).__init__(model, **kwargs)
        self.default_properties = {'type': 'metabolite'}

        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(), self.kwargs.keys())
        self._do_checks()

    def __str__(self):
        return "KeyFactory({})".format(self.to_string())

    def _do_checks(self):
        """

        :return:
        """
        type_list = ['metabolite',
                     'compartment',
                     'global_quantity',
                     'reaction',
                     'parameter_set',
                     'parameter',
                     'constant',
                     'report',
                     'function',
                     'function_parameter']
        if self.type not in type_list:
            raise Errors.InputError('{} not a valid type. {}'.format(self.type, type_list))

    def generate(self, n=1):
        """

        :return:
        """
        if self.type == 'metabolite':
            return self.create_key(self.model.metabolites).next()

        elif self.type == 'compartment':
            return self.create_key(self.model.compartments).next()

        elif self.type == 'global_quantity':
            return self.create_key(self.model.global_quantities).next()

        elif self.type == 'reaction':
            key = self.create_key(self.model.reactions).next()
            return key

        elif self.type == 'parameter_set':
            raise NotImplementedError#self.create_key(self.model.metabolites).next()

        elif self.type == 'parameter':
            return self.create_key(self.model.local_parameters).next()

        elif self.type == 'function':
            return self.create_key(self.model.functions).next()

        elif self.type == 'constant':
            return self.create_constant_key(n)

        elif self.type == 'report':
            raise NotImplementedError
            # return self.create_key(self.model.metabolites).next()

        elif self.type == 'function_parameter':
            return self.create_function_parameter_key(n)


    def create_key(self, model_component):
        """

        :return:
        """
        ##TODO fix bug where create key only works for generating single key at a time.
        ##be consistent with the rest of copasi
        if self.type == 'global_quantity':
            self.type = 'model_value'
        ## split by underscore
        word_list = self.type.split('_')

        ## get uppercase for camel caps
        word_list = [i[0].upper()+i[1:] for i in word_list]

        ## convert word list to camel caps
        word = reduce(lambda x, y: x + y, word_list)

        bool = True
        count = 10000
        ## list for remembering already generated keys
        key_list = []
        while bool:
            key = '{}_{}'.format(word, count)
            new_list = [i.key for i in model_component] + key_list
            if key not in new_list:
                key_list.append(key)
                yield key
            count += 1

    def create_function_parameter_key(self, n=1):
        """
        create_key only works for generating a single key at a time.
        When creating ParameterDescriptions, we often need several keys
        generated at a time. This method generates these unique keys.
        :return:
        """
        ## get keys
        existing = [i.key for i in self.model.parameter_descriptions]

        for i in existing:
            assert '_' in i
        existing = [i.split('_')[1] for i in existing]
        existing = [int(i) for i in existing]

        bool = True
        count = 0
        keys = []
        while count!=n:
            random_number = randint(1000, 100000000)
            if random_number not in existing:
                existing.append(random_number)
                keys.append(random_number)
                count += 1
        keys = ['{}_{}'.format('FunctionParameter',i) for i in  keys]
        if len(keys)==1:
            return keys[0]
        else:
            return keys

    def create_constant_key(self, n=1):
        """
        create_key only works for generating a single key at a time.
        When creating ParameterDescriptions, we often need several keys
        generated at a time. This method generates these unique keys.
        :return:
        """
        ## get keys
        existing = [i.key for i in self.model.constants]

        existing = [i.split('_')[1] for i in existing]
        existing = [int(i) for i in existing]

        bool = True
        count = 0
        keys = []
        while count!=n:
            random_number = randint(1000, 100000000)
            if random_number not in existing:
                existing.append(random_number)
                keys.append(random_number)
                count += 1
        keys = ['{}_{}'.format('Parameter',i) for i in  keys]
        if (len(keys)==1) and (isinstance(keys, list)):
            return keys[0]
        else:
            return keys


class Expression(object):
    def __init__(self, expression, **kwargs):
        # super(Expression, self).__init__(**kwargs)
        self.expression = expression
        self.default_properties = {}

        ## list of available operators according the copasi website
        self.operator_list = ['+', '-', '*', r'/', '%',
                         '%', '^', 'abs', 'floor',
                         'ceil', 'factorial', 'log',
                         'log10', 'exp', 'sin'
                                         'cos', 'tan', 'sec',
                         'csc', 'cot', 'tanh',
                         'sech', 'csch', 'coth',
                         'asin', 'acos', 'atan',
                         'arcsec', 'arccsc', 'arcccot',
                         'arcsinh', 'arccosh', 'arctanh',
                         'arcsech', 'arccsch', 'arccoth',
                         'uniform', 'normal', 'le',
                         'lt', 'ge', 'gt', 'ne', 'eq',
                         'and', 'or', 'xor', 'not', 'if']


    def to_list(self):
        """
        convert a mathematical expression into a list of elements
        in the equation
        :return:
        """
        ## replace operators with comma so we can subsequently split the string at comma
        for i in self.operator_list:
            self.expression = self.expression.replace(i, ',')

        ##get list of elements by split
        return self.expression.split(',')

    def __str__(self):
        return "Expression({})".format(self.expression)




class Translator(_base._ModelBase):
    """
    Translate a copasi style reaction into
    lists of substrates, products and modifiers.

    """
    def __init__(self, model, reaction, **kwargs):
        super(Translator, self).__init__(model, **kwargs)
        self.reaction = reaction
        self.default_properties = {'reversible': False}


        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(),
                             kwargs.keys())

        ## split reaction by -> or = and ;. determine reversibility
        self.substrates, self.products, self.modifiers = self.split_reaction()

        ## split substrates and products by + and modifiers by empty spaces
        if self.substrates != []:
            self.substrates = self.split_reaction_components(self.substrates, type='substrate')
        if self.products != []:
            self.products = self.split_reaction_components(self.products, type='product')
        if self.modifiers != []:
            self.modifiers = self.split_reaction_components(self.modifiers, type='modifier')

        ## lump together like metabolites (i.e. convert A + A into 2*A)
        self.substrates = self.determine_stoichiometry(self.substrates)
        self.products = self.determine_stoichiometry(self.products)

        ## get lists of substrates, products and modifiers, creating if component doesn't exist
        self.substrates = self.get_components('substrate')
        self.products = self.get_components('product')
        self.modifiers = self.get_components('modifier')

        self.all_components = self.substrates + self.products + self.modifiers


    def __str__(self):
        """

        :return:
        """
        return "Translator({})".format(self.to_string())

    def split_reaction(self):
        """
        split the reaction into reactants, products
        and modifiers
        :return:
        """
        list_of_substrates = []
        list_of_products = []
        list_of_modifiers = []

        ## handle case where modifiers included in reaction
        if ';' in self.reaction:
            ## for irreversible reactions
            if '->' in self.reaction:
                list_of_substrates, reaction = self.reaction.split('->')

            ## for reversible reactions
            elif '=' in self.reaction:
                list_of_substrates, reaction = self.reaction.split('=')
                self.reversible = True

            list_of_products, list_of_modifiers = reaction.split(';')
        ##for reactions without modifi
        # ers
        else:
            ## irreversible reactions
            if '->' in self.reaction:
                list_of_substrates, list_of_products = self.reaction.split('->')
            ## for reversible reactions
            elif '=' in self.reaction:
                list_of_substrates, list_of_products = self.reaction.split('=')
                self.reversible = True
        ## convert back to list if the above produced an empty string
        ##for the cases such as "A + B -> "
        if (list_of_products == ' ') or (list_of_products == ''):
            list_of_products = []

        if (list_of_substrates == ' ') or (list_of_substrates == ''):
            list_of_substrates = []

        if (list_of_modifiers == ' ') or (list_of_modifiers == ''):
            list_of_modifiers = []

        return list_of_substrates, list_of_products, list_of_modifiers

    def split_reaction_components(self, component, type='substrate'):
        """
        split a reaction or product component by + operator and
        modifier by empty spaces
        :param component: one of substrate, product or modifier
        :return:
        """
        component_options = ['substrate', 'product', 'modifier']
        if type not in component_options:
            raise Errors.InputError('{} not in {}'.format(component, component_options))

        if type == 'substrate':
            return [i.strip() for i in self.substrates.split('+')]

        elif type == 'product':
            return [i.strip() for i in self.products.split('+')]

        elif type == 'modifier':
            return [i.strip() for i in self.modifiers.split(' ') if i != '']


    def determine_stoichiometry(self, component):
        """
        determine the reaction stoichiometry for a reaction component.
        Converts syntax such as 'X + X -> Y + Y' into 2*X for substrates
        and 2*Y for products.
        :param component: either substrate or product side of the ->. Modifiers are 1
        :return: list
        """

        count = Counter(component)
        for i in count:
            if count[i] > 1:
                count['{}*{}'.format(count[i], i)] = 1
                del count[i]
        return count.keys()


    def get_components(self, component='substrate'):
        """
        create or get substrates, products or modifiers
        :return: list
        """

        if component == 'substrate':
            component_list = self.substrates

        elif component == 'product':
            component_list = self.products

        elif component == 'modifier':
            component_list = self.modifiers

        lst = []
        for comp in component_list:
            stoic = 1
            ## check for non 1 stoichiometry
            if '*' in comp:
                stoic, comp = comp.split('*')

            ## if metab doesn't exist, create and add it to the model
            # if comp == '':
            #     continue
            metab = self.model.get('metabolite', comp, by='name')
            if metab == []:
                metab = Metabolite(self.model, name=comp,
                                   concentration=1,
                                   compartment=self.model.compartments[0],
                                   key=KeyFactory(self.model,
                                                  type='metabolite').generate() )

                self.model = self.model.add_metabolite(metab)

            ## now get the metabolite.
            ## Note we do this again anyway beause adding the metabolite
            ## calculates particle numbers from concentration.
            metab = self.model.get('metabolite', comp, by='name')
            ## convert to respective classes
            if component == 'substrate':
                metab = metab.to_substrate()

            elif component == 'product':
                metab = metab.to_product()

            elif component == 'modifier':
                metab = metab.to_modifier()

            ##add stoichiometry
            metab.stoichiometry = int(stoic)
            lst.append(metab)

        return lst


class MassAction(Function):
    def __init__(self, model, **kwargs):
        super(MassAction, self).__init__(model, **kwargs)
        self.model = model

        self.create_mass_action()

    def __str__(self):
        """

        :return:
        """
        return "MassAction(reversible={})".format(self.reversible)

    def get_mass_action(self):
        """

        :return:
        """
        if self.reversible == 'false':
            ma = [i for i in self.model.functions if i.name == 'Mass action (reversible)']
        elif self.reversible == 'true':
            ma = [i for i in self.model.functions if i.name == 'Mass action (reversible']
        if ma == []:
            raise Exception
        return ma

    def create_mass_action(self):
        """
        if name == mass_action, create the mass action function
        :return:
        """

        self.key = KeyFactory(self.model, type='function').generate()

        if self.reversible == 'false':
            self.name = 'Mass action (irreversible)'
            self.type = 'MassAction'
            substrate = ParameterDescription(self.model, key='FunctionParameter_1000', name='substrate', order='1', role='substrate')
            parameter = ParameterDescription(self.model, key='FunctionParameter_1001', name='k1', order='0', role='constant')
            self.list_of_parameter_descriptions = [substrate, parameter]
            self.reversible = 'false'
            self.expression = 'k1*PRODUCT&lt;substrate_i>'

        elif self.reversible == 'true':
            self.name = 'Mass action (reversible)'
            self.key = self.key
            self.type = 'MassAction'
            self.reversible = 'true'
            self.expression = 'k1*PRODUCT&lt;substrate_i>-k2*PRODUCT&lt;product_j>'

            k1 = ParameterDescription(self.model, key='FunctionParameter_1002', name='k1', order='0', role='constant')
            s = ParameterDescription(self.model, key='FunctionParameter_1003', name='substrate', order='1', role='substrate')
            k2 = ParameterDescription(self.model, key='FunctionParameter_1004', name='k2', order='2', role='constant')
            p = ParameterDescription(self.model, key='FunctionParameter_1005', name='product', order='3', role='product')
            self.list_of_parameter_descriptions = [k1, s, k2, p]
        return self

    def to_xml(self):
        """
        write mass action function as xml element
        :return:
        """
        mass_action = etree.Element('Function', attrib=OrderedDict({'key': self.key,
                                                                    'name': self.name,
                                                                    'type': 'MassAction',
                                                                    'reversible': self.reversible}) )

        expression = etree.SubElement(mass_action, 'Expression')
        if self.reversible == 'false':
            expression.text = 'k1*PRODUCT&lt;substrate_i>'

        elif self.reversible == 'true':
            expression.text = 'k1*PRODUCT&lt;substrate_i>-k2*PRODUCT&lt;product_j>'

        list_of_p_desc = etree.SubElement(mass_action, 'ListOfParameterDescriptions')

        for i in self.list_of_parameter_descriptions:
            etree.SubElement(list_of_p_desc, 'ParameterDescription', attrib={'key': i.key,
                                                                             'name': i.name,
                                                                             'order': i.order,
                                                                             'role': i.role})

        return mass_action





##TODO work out why both rate law and expression are function in reaction

class ParameterSet(_base._ModelBase):
    def __init__(self, model, **kwargs):
        super(ParameterSet, self).__init__(model, **kwargs)


        self.default_properties = {'key': None,
                                   'name': 'Initial State',
                                   'initial_time': 0,
                                   'compartments': None,
                                   'metabolites': None,
                                   'global_quantities': None,
                                   'kinetic_parameters': None,
                                   'state_template': None,
                                   'initial_state': None}

        self.update_properties(self.default_properties)
        self.update_kwargs(kwargs)
        self.check_integrity(self.default_properties.keys(), kwargs.keys())
        self._do_checks()

    def _do_checks(self):
        """

        :return:
        """
        if self.key is None:
            self.key = KeyFactory(self.model, type='parameter_set').generate()



    def to_xml(self):

        ## top element
        parameter_set = etree.Element('ModelParameterSet', attrib={'key': self.key,
                                                         'name': self.name})

        ## time element
        model_parameter_group = etree.SubElement(
            parameter_set,'ModelParameterGroup',
            attrib={'cn': 'String=Initial Time',
                    'type': 'Group'})

        ## time sub element
        etree.SubElement(model_parameter_group, 'ModelParameter',
                         attrib={'cn': self.model.reference,
                                 'value': self.initial_time,
                                 'type': 'Model',
                                 'simulationType': 'time'})

        ##compartment element
        model_parameter_group = etree.SubElement(
            parameter_set, 'ModelParameterGroup',
            attrib={'cn': 'String=Initial Compartment Sizes',
                    'type': 'Group'}
        )

        ##compartment subelement
        for compartment in self.model.compartments:
            etree.SubElement(model_parameter_group, 'ModelParameter',
                         attrib={'cn': '{},{}'.format(self.model.reference, compartment.reference),
                                 'value': compartment.initial_value,
                                 'type': 'Compartment',
                                 'simulationType': compartment.simulation_type})


        ##metabolites element
        model_parameter_group = etree.SubElement(
            parameter_set, 'ModelParameterGroup',
            attrib={'cn': 'String=Initial Species Values',
                    'type': 'Group'}
        )

        ##metabolite subelement
        for metab in self.model.metabolites:
            etree.SubElement(model_parameter_group, 'ModelParameter',
                         attrib={'cn': '{},{},{}'.format(
                             self.model.reference, metab.compartment.reference,metab.reference),
                                 'value': matab.particle_number,
                                 'type': 'Species',
                                 'simulationType': metab.simulation_type})

        ##global quantities element
        model_parameter_group = etree.SubElement(
            parameter_set, 'ModelParameterGroup',
        attrib = {'cn': 'String=Initial Global Quantities',
                  'type': 'Group'}
        )

        ##global quantity subelement
        for global_q  in self.model.global_quantities:
            etree.SubElement(model_parameter_group, 'ModelParameter',
                             attrib={'cn': '{},{}'.format(
                                 self.model.reference, global_q.reference),
                                 'value': global_q.initial_value,
                                 'type': 'ModelValue',
                                 'simulationType': global_q.simulation_type})

        ##kinetic parameters
        model_parameter_group = etree.SubElement(
            parameter_set, 'ModelParameterGroup',
        attrib = {'cn': 'String=Kinetic Parameters',
                  'type': 'Group'}
        )

        ##global quantity subelement
        for global_q  in self.model.reactions:
            # etree.SubElement(model_parameter_group, 'ModelParameter',
            #                  attrib={'cn': '{},{}'.format(
            #                      self.model.reference, global_q.reference),
            #                      'value': global_q.initial_value,
            #                      'type': 'ModelValue',
            #                      'simulationType': global_q.simulation_type})
#
#
#


    ##TODO reactions, metabs, globs and comp
    ## all need additional reference without the reference part.
    ##either string manit or write a new function to produce
    ##in each class

    ## implement means ofadding initial expresion
    ## to each ompontnt




























