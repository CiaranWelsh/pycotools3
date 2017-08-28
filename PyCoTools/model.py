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

import site

# site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
# import PyCoTools
import pycopi, Errors, _base
from PyCoTools.Tests import _test_base
import os, glob
import pandas
import unittest
import re
from lxml import etree
from copy import deepcopy
import logging
from collections import OrderedDict

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
        self.update_properties(self.default_properties)

    def __str__(self):
        return 'Model(name={}, time_unit={}, volume_unit={}, quantity_unit={})'.format(self.name, self.time_unit,self.volume_unit, self.quantity_unit)

    def __repr__(self):
        return self.__str__()

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
        Change the current value of the InitialState field to states
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
                states = i.text.split(' ')
                del states[-1] ##remove trailing newline
                del states[count]  ## get component of interest
        #
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
                    lst.append(Compartment(key=j.attrib['key'],
                                           name=j.attrib['name'],
                                           type=j.attrib['simulationType'],
                                           value=float(self.states[j.attrib['key']])) )
        return lst

    def add_compartment(self, name, key=None, simulation_type='fixed',
                        initial_value=1):
        """
        Add compartment to model
        :param name: name of compartment
        :param key: key of compartment. If None, key automatically generated
        :param simulation_type: fixed, reactions, ode or assignment
        :return: model.Model
        """
        if key == None:
            key = KeyFactory(self, type='compartment').generate()

        simulation_types = ['reactions', 'ode', 'fixed', 'assignment']
        if simulation_type not in simulation_types:
            raise Errors.InputError('{} not in {}'.format(simulation_type, simulation_types))


        compartment = etree.Element('Compartment', attrib={'key':key,
                                                           'name': name,
                                                           'simulationType': simulation_type,
                                                           'dimensionality': '3'})

        ## add compartment to the list of compartments
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfCompartments':
                # for j in i:
                #     print j.tag
                i.append(compartment)

        ## add compartment to state template
        self.add_state(key, initial_value)

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
            lst.append(Metabolite(name=metabs[key]['name'],
                                  compartment=comp,
                                  key=metabs[key]['key'],
                                  particle_number=metabs[key]['particle_number'],
                                  concentration=self.convert_particles_to_molar(
                                      metabs[key]['particle_number'], self.quantity_unit, comp.value),
                                  simulation_type=metabs[key]['simulationType']))

        return lst


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
            lst.append(GlobalQuantity(name=model_values[key]['name'],
                                      key=model_values[key]['key'],
                                      simulation_type=model_values[key]['simulationType'],
                                      value=model_values[key]['initial_value']))
        return lst




    def add_global_quantity(self, name, key=None, initial_value=None,
                            simulation_type='fixed'):
        """

        :param name: name of global quantity to be added
        :param key:  unique id for global quantity. Automatically assigned if left None
        :param initial_value: amount at simulation start time
        :param simulation_type: fixed, ode assignment or reactions
        :return: model.Model
        """
        if key == None:
            key = KeyFactory(self, type='global_quantity').generate()

        if simulation_type not in ['assignment', 'fixed', 'ode', 'reactions']:
            raise TypeError('wrong simulation type')

        model_value = etree.Element('ModelValue', attrib={'key': key,
                                                          'name': name,
                                                          'simulationType': simulation_type})

        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                i.append(model_value)

        self.add_state(key, initial_value)

        return self

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


    @property
    def local_parameters(self):
        """
        return local parameters used in your model
        :return: list
        """
        query='//*[@cn="String=Kinetic Parameters"]'
        d={}
        for i in self.xml.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['simulationType']=='fixed':
                        match=re.findall('Reactions\[(.*)\].*Parameter=(.*)', k.attrib['cn'])[0]
                        assert isinstance(match,tuple),'get species regex hasn\'t been found. Do you have species in your model?'
                        assert match !=None
                        assert match !=[]
                        assert len(match)==2
                        match_key='({}).{}'.format(match[0],match[1])
                        attributes = {'reaction_name':match[0],
                                      'name': match[1],
                                      # 'key': k.attrib['key'],
                                      'value': k.attrib['value'],
                                      'simulation_type': k.attrib['simulationType'],
                                      'parameter_type': k.attrib['type'],
                                      'global_name': match_key}
                        d[match_key]=attributes

        lst = []
        for param in d:
            lst.append(LocalParameter(**d[param]) )
        return lst

    def get_local_parameters(self):
        print

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
                    lst.append( Function(**child.attrib) )
        return lst

    @property
    def number_of_reactions(self):
        count = 0
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in list(i):
                    count = count + 1
        return count

    @property
    def reactions(self):
        """
        :return: list of current model reactions
        """
        list_of_reactions = []
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in list(i):
                    for k in list(j):
                        list_of_substrates = []
                        list_of_products = []
                        list_of_constants = []
                        function_list = []
                        if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
                            for l in list(k):
                                ## get a list of metabolites used as substrate
                                list_of_substrates = [m for m in self.metabolites if m.key in l.attrib['metabolite']]

                                ## convert list to substrates
                                list_of_substrates = [m.to_substrate() for m in list_of_substrates]

                        elif k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
                            for l in list(k):
                                ## get list of metabolites and convert them to Product class
                                list_of_products = [m for m in self.metabolites if
                                                    m.key in l.attrib['metabolite']]
                                list_of_products = [m.to_product() for m in list_of_products]

                        elif k.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                            loc = []
                            for l in list(k):
                                list_of_constants.append(LocalParameter(key=l.attrib['key'],
                                                          name=l.attrib['name'],
                                                          value=l.attrib['value'],
                                                          reaction_name=j.attrib['name'],
                                                          global_name="({}).{}".format(j.attrib['name'], l.attrib['name']))  )

                        elif k.tag == '{http://www.copasi.org/static/schema}KineticLaw':
                            function_list = [m for m in self.functions if m.key in k.attrib['function']]
                    r = Reaction(name=j.attrib['name'],
                                 key=j.attrib['key'],
                                 reactants=list_of_substrates,
                                 products = list_of_products,
                                 parameters = list_of_constants,
                                 rate_law=function_list)
                    list_of_reactions.append(r)
        return list_of_reactions


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
        root = etree.ElementTree(self.xml)

        ## Then remove existing copasi file for ovewrite
        if os.path.isfile(copasi_file):
            os.remove(copasi_file)
        root.write(copasi_file)
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
        os.remove(copasi_file)

    def add_metabolite(self, name=None, key=None, concentration=None,
                       particle_number=None, compartment=None,
                       simulation_type=None):
        """
        Add a metabolite to the model xml
        :param metabolite_args: Dict. Arguments to pass to Metabolite
        :return:
        """

        if name in [i.name for i in self.metabolites]:
            raise Errors.InputError('Already a specie with the name "{}" in your model'.format(metabolite_args['name']))

        if key == None:
            key = KeyFactory(self,type='metabolite').generate()

        if name == None:
            name = key

        if (concentration == None) or (particle_number == None):
            concentration= str(0)

        if concentration != None:
            if isinstance(concentration, (float, int)):
                concentration = str(concentration)

        if compartment == None:
            compartment = self.compartments[0]

        if not isinstance(compartment, Compartment):
            raise Errors.InputError('compartment should be of type model.Compartment')

        if simulation_type == None:
            simulation_type = 'reactions'

        if particle_number == None:
            particle_number = self.convert_molar_to_particles(concentration,
                                                              self.quantity_unit,
                                                              compartment.value)


        if isinstance(particle_number, (float, int)):
            particle_number = str(particle_number)


        ##TODO fix metabolite converion finctions to fully support copasi
        ##TODO work out whether I need to actively add metabolite to metabolite list or whether I can make it update itself from the xml
        metab = etree.Element('Metabolite', attrib={'key': key,
                                                    'name': name,
                                                    'simulationType': simulation_type,
                                                    'compartment': compartment.key})

        ## add the metabolute to list of metabolites
        list_of_metabolites = '{http://www.copasi.org/static/schema}ListOfMetabolites'
        for i in self.xml.iter():
            if i.tag == list_of_metabolites:
                i.append(metab)

        ## add metabolite to state_template and initial state fields
        self.add_state(key, particle_number)

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

    def get(self, component, value, by='name'):
        """
        Factory method
        get a model component by a value of a certain type
        :param component: the component i.e. metabolite or local_parameter
        :param value: value of the attribute to match by i.e. metabolite called A
        :param by: which attribute to search by. i.e. name or key or value
        :return: component
        """
        list_of_accepted_components = ['metabolite',
                                       'compartment',
                                       'local_parameter',
                                       'global_quantity']
        if component not in list_of_accepted_components:
            raise Errors.InputError('{} not in list of components'.format(component))

        if component == 'metabolite':
            res = [i for i in self.metabolites if getattr(i, by) == value]

        elif component == 'compartment':
            res = [i for i in self.compartments if getattr(i, by) == value]

        elif component == 'local_parameter':
            res = [i for i in self.local_parameters if getattr(i, by) == value]

        elif component == 'global_quantity':
            res = [i for i in self.global_quantities if getattr(i, by) == value]

        if len(res) == 1:
            res = res[0]
        return res




class Compartment(_base._Base):
    def __init__(self, **kwargs):
        super(Compartment, self).__init__(**kwargs)
        self.default_properties = {'name':None,
                             'key':None,
                             'value':None,
                             'type':None}

        for key in self.kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, self.default_properties))

        self._do_checks()


    def __str__(self):
        return 'Compartment({})'.format(self.to_string())

    def __repr__(self):
        return self.__str__()

    def _do_checks(self):
        """
        Make sure none of the arguments are empty
        :return: void
        """
        for attr in self.default_properties:
            if attr not in sorted(self.__dict__.keys() ):
                raise Errors.InputError('Required attribute not specified: {}'.format(attr))

    @property
    def reference(self):
        return 'Vector=Compartments[{}]'.format(self.name)

class Compartment(_base._Base):
    def __init__(self, **kwargs):
        super(Compartment, self).__init__(**kwargs)
        self.default_properties = {'name':None,
                             'key':None,
                             'value':None,
                             'type':None}

        for key in self.kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, self.default_properties))

        self._do_checks()


    def __str__(self):
        return 'Compartment({})'.format(self.to_string())

    def __repr__(self):
        return self.__str__()

    def _do_checks(self):
        """
        Make sure none of the arguments are empty
        :return: void
        """
        for attr in self.default_properties:
            if attr not in sorted(self.__dict__.keys() ):
                raise Errors.InputError('Required attribute not specified: {}'.format(attr))

    @property
    def reference(self):
        return 'Vector=Compartments[{}]'.format(self.name)

class Metabolite(_base._Base):
    """
    Metabolite class to hole attributes
    associated with a Metabolite.

    Concentration and particle numbers
    are separate. Calculate them in Model
    and assign from outside the Metabolite class
    becuse that way the metabolite class doesn't
    need to know about the Model

    """
    def __init__(self, **kwargs):
        super(Metabolite, self).__init__(**kwargs)
        self.default_properties = {'compartment':None,
                             'key':None,
                             'name':None,
                             'particle_number':None,
                             'concentration':None,
                             'stoiciometry':None,
                             # 'reaction_key':None,
                             'simulation_type':None,
                             }

        for key in kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, self.default_properties) )
        self.update_properties(self.default_properties)
        ##update all keys to none
        self._do_checks()

    def __str__(self):
        return 'Metabolite({})'.format(self.to_string())

    def __repr__(self):
        return self.__str__()

    def _do_checks(self):
        """

        :return:
        """

        if isinstance(self.compartment, Compartment)!=True:
            raise Errors.InputError('compartment argument should be of type PyCoTools.pycopi.Compartment')

        if ('particle_number' not in self.__dict__.keys()) and  ('concentration' not in self.__dict__.keys() ):
            raise Errors.InputError('Must specify either concentration or particle numbers')

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
        return Substrate(**self.kwargs)

    def to_product(self):
        return Product(**self.kwargs)

class Substrate(Metabolite):
    def __init__(self, **kwargs):
        super(Substrate, self).__init__(**kwargs)

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
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

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

class GlobalQuantity(_base._Base):
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
    def __init__(self, **kwargs):
        super(GlobalQuantity, self).__init__(**kwargs)

        self.default_properties = {'name': None,
                                   'key': None,
                                   'simulation_type': None,
                                   'value': None,
                                   'type': None}

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

    def __str__(self):
        return 'GlobalQuantity({})'.format(self.to_string())

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


class Reaction(_base._Base):
    """
    Reactions have rectants, products, rate laws and parameters
    Not sure if this is a priority just yet


    Here's an idea. Would it be a good idea to have just
    a Parmeter class which a scope property which defines
    whether its a model parameter or specific to a individual
    reaction.
    """
    def __init__(self, **kwargs):
        super(Reaction, self).__init__(**kwargs)
        self.default_properties = {'name': None,
                             'key': None,
                             'reactants': None,
                             'products': None,
                             'rate_law': None,
                             'parameters': None}
        for key in self.kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('{} not valid key. Valid keys are: {}'.format(key, self.default_properties))
        self.update_properties(self.default_properties)

    def __str__(self):
        return 'Reaction({})'.format(self.to_string())

    def __repr__(self):
        return self.__str__()

    def do_checks(self):
        """


        :return:
        """
        if isinstance(self.reactants, list):
            for i in self.reactants:
                if isinstance(i, Metabolite)==False:
                    raise Errors.InputError('{} should be a Metabolite'.format(i))
        if isinstance(self.reactants, Metabolite)==False:
            raise Errors.InputError('{} should be a Metabolite'.format(self.reactants))

        if isinstance(self.products, list):
            for i in self.products:
                if isinstance(i, Metabolite) == False:
                    raise Errors.InputError('{} should be a Metabolite'.format(i))
        if isinstance(self.products, Metabolite) == False:
            raise Errors.InputError('{} should be a Metabolite'.format(self.reactants))

        if isinstance(self.products, list):
            for i in self.products:
                if isinstance(i, Metabolite) == False:
                    raise Errors.InputError('{} should be a Metabolite'.format(i))
        if isinstance(self.products, Metabolite) == False:
            raise Errors.InputError('{} should be a Metabolite'.format(self.reactants))


class Function(_base._Base):
    """
    Class to hold copasi function definitions for rate laws
    """

    def __init__(self, **kwargs):
        super(Function, self).__init__(**kwargs)
        self.default_properties = {'name':None,
                        'key':None,
                        'type':None,
                        'reversible':None}

        for key in self.kwargs:
            if key not in self.default_properties:
                raise Errors.InputError('{} not in {}'.format(key, default_properties))
        self.update_properties(self.default_properties)

    def __str__(self):
        return 'Function({})'.format(self.to_string())

    def __repr__(self):
        return self.__str__()

class LocalParameter(_base._Base):
    def __init__(self, **kwargs):
        super(LocalParameter, self).__init__(**kwargs)
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

    def __str__(self):
        return 'LocalParameter({})'.format(self.to_string())

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
                     'report']
        if self.type not in type_list:
            raise Errors.InputError('{} not a valid type. {}'.format(self.type, type_list))

    def generate(self):
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
            return self.create_key(self.model.reactions()).next()

        elif self.type == 'parameter_set':
            raise NotImplementedError#self.create_key(self.model.metabolites).next()

        elif self.type == 'parameter':
            return self.create_key(self.model.local_parameters).next()

        elif self.type == 'report':
            raise NotImplementedError
            # return self.create_key(self.model.metabolites).next()


    def create_key(self, model_component):
        """

        :return:
        """
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
        count = 0
        while bool:
            key = '{}_{}'.format(word, count)
            if key not in [i.key for i in model_component]:
                yield key
            count += 1












