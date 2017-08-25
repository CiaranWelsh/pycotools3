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

LOG = logging.getLogger(__name__)


## TODO after running a task, bind the results to the model instance so that they are retrievable
class Model(_base._Base):
    def __init__(self, copasi_file, **kwargs):
        super(Model, self).__init__(**kwargs)
        self.copasi_file = copasi_file
        self.xml = pycopi.CopasiMLParser(copasi_file).copasiML
        ## fill this dict after class is finished
        self.allowed_keys = {}
        self.update_properties(self.allowed_keys)

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
        return  dict(zip(collection, state_values))

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
                    key, name, type, dimensionality = j.attrib.values()
                    lst.append(Compartment(key=key, name=name, type=type, value=float(self.states[key])) )
        return lst

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
        """
        List of model metabolites as type metabolite
        :return: Metabolite
        name, compartment, key, conc, particle
        """
        collection = {}
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfMetabolites':
                for j in i:
                    collection[j.attrib['key']] = dict(j.attrib)

        for key in collection:
            collection[key]['particle_number'] = self.states[key]

        keys = [collection[metab]['compartment'] for metab in collection]
        # print self.compartments
        comp_dct = {}
        for key in keys:
            comp_dct[key] = [i for i in self.compartments if i.key == key][0]

        for key in collection:
            comp_key = collection[key]['compartment']
            collection[key]['compartment']=comp_dct[comp_key]

        lst = []
        for key in collection:
            lst.append(Metabolite(name=collection[key]['name'],
                                  compartment=collection[key]['compartment'],
                                  key=collection[key]['key'],
                                  particle_number=collection[key]['particle_number'],
                                  concentration=self.convert_particles_to_molar(
                                      collection[key]['particle_number'], self.quantity_unit, collection[key]['compartment'].value),
                                  simulation_type=collection[key]['simulationType']))

        return lst

    @property
    def global_quantities(self):
        '''
        return global quantities in your model that have simulationType='fixed'
        Note: This method does not return global quantities with simulationType='assignment'
        but I'm not sure whether they are needed just yet.
        :return:list
        '''
        model_values = {}
        for i in self.xml.iter():
            """
            This loop gets model value name, key and simulation type
            """
            if i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                for j in i:
                    model_values[j.attrib['key']] = dict(j.attrib)
        # print model_values

        collection = {}
        query='//*[@cn="String=Initial Global Quantities"]'
        d={}
        for i in self.xml.xpath(query):
            '''
            gets name, simulationType and value
            '''
            for j in list(i):
                match= re.findall('Values\[(.*)\]',j.attrib['cn'])[0]
                assert isinstance(match.encode('utf8'),str),'{} should be a string but is instead a {}'.format(match,type(match))
                assert match !=None
                assert match !=[]
                d[match]=j.attrib['value']
        #
        for key in model_values:
            name = model_values[key]['name']
            model_values[key]['value'] = d[name]


        lst = []
        for key in model_values:
            lst.append(GlobalQuantity(name=model_values[key]['name'],
                                      key=model_values[key]['key'],
                                      simulation_type=model_values[key]['simulationType'],
                                      value=model_values[key]['value']))
        return lst

    @property
    def local_parameters(self):
        """
        return local parameters used in your model
        :return: dict[local_str] = LocalParameter
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
                                      'value': k.attrib['value'],
                                      'simulation_type': k.attrib['simulationType'],
                                      'parameter_type': k.attrib['type'],
                                      'global_name': match_key}
                        d[match_key]=attributes

        lst = []
        for param in d:
            lst.append(LocalParameter(**d[param]) )
        return lst

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


    def reactions(self):
        """
{'name':None,
                             'key':None,
                             'reactants':None,
                             'products':None,
                             'rate_law':None,
                             'parameters':None}
        :return:
        """
        reactions_dct = {}
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in list(i):
                    for k in list(j):
                        list_of_substrates = None
                        list_of_products = None
                        list_of_constants = None
                        function_list = None
                        if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
                            for l in list(k):
                                list_of_substrates = [m for m in self.metabolites if m.key in l.attrib['metabolite'] ]
                                list_of_substrates = [m.to_substrate() for m in list_of_substrates]
                        elif k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
                            for l in list(k):
                                list_of_products = [m for m in self.metabolites if
                                                    m.key in l.attrib['metabolite']]
                                list_of_products = [m.to_product() for m in list_of_products]
                        elif k.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                            for l in list(k):
                                list_of_constants = [m for m in self.local_parameters if m.key in l.attrib['key']]
                        elif k.tag == '{http://www.copasi.org/static/schema}KineticLaw':
                            function_list = [m for m in self.functions if m.key in k.attrib['function']]
                    r = Reaction(name=j.attrib['name'], key=j.attrib['key'],
                                   reactants=list_of_substrates,
                                   products = list_of_products,
                                   parameters = list_of_constants,
                                   rate_law=function_list)
                    reactions_dct[r.name] = r
        return reactions_dct


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

        if os.path.isfile(copasi_file):
            os.remove(copasi_file)
        # first convert the copasiML to a root element tree
        root = etree.ElementTree(self.xml)
        root.write(copasi_file)

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

class Compartment(_base._Base):
    def __init__(self, **kwargs):
        super(Compartment, self).__init__(**kwargs)
        self.allowed_keys = {'name':None,
                             'key':None,
                             'value':None,
                             'type':None}

        for key in self.kwargs:
            if key not in self.allowed_keys:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, self.allowed_keys))

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
        for attr in self.allowed_keys:
            if attr not in sorted(self.__dict__.keys() ):
                raise Errors.InputError('Required attribute not specified: {}'.format(attr))

    @property
    def reference(self):
        return 'Vector=Compartments[{}]'.format(self.name)

class Compartment(_base._Base):
    def __init__(self, **kwargs):
        super(Compartment, self).__init__(**kwargs)
        self.allowed_keys = {'name':None,
                             'key':None,
                             'value':None,
                             'type':None}

        for key in self.kwargs:
            if key not in self.allowed_keys:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, self.allowed_keys))

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
        for attr in self.allowed_keys:
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
        self.allowed_keys = {'compartment':None,
                             'key':None,
                             'name':None,
                             'particle_number':None,
                             'concentration':None,
                             'stoiciometry':None,
                             'reaction_key':None,
                             'simulation_type':None,
                             }

        for key in kwargs:
            if key not in self.allowed_keys:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, self.allowed_keys) )
        self.update_properties(self.allowed_keys)
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

        # print getattr(self, 'particle_number'
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
            if key not in self.allowed_keys:
                raise Errors.InputError('{} not in {}'.format(key, self.allowed_keys))
        self.update_properties(self.allowed_keys)

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
            if key not in self.allowed_keys:
                raise Errors.InputError('{} not in {}'.format(key, self.allowed_keys))

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

        self.allowed_properties = {'name': None,
                                   'key': None,
                                   'simulation_type': None,
                                   'value': None,
                                   'type': None}

        for key in kwargs:
            if key not in self.allowed_properties:
                raise Errors.InputError('Attribute not allowed. "{}" not in {}'.format(key, self.allowed_properties.keys()) )
        self.update_properties(self.allowed_properties)

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
        self.allowed_properties = {'name': None,
                             'key': None,
                             'reactants': None,
                             'products': None,
                             'rate_law': None,
                             'parameters': None}
        for key in self.kwargs:
            if key not in self.allowed_properties:
                raise Errors.InputError('{} not valid key. Valid keys are: {}'.format(key, self.allowed_properties))
        self.update_properties(self.allowed_properties)

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
                    raise Error.InputError('{} should be a Metabolite'.format(i))
        if isinstance(self.reactants, Metabolite)==False:
            raise Error.InputError('{} should be a Metabolite'.format(self.reactants))

        if isinstance(self.products, list):
            for i in self.products:
                if isinstance(i, Metabolite) == False:
                    raise Error.InputError('{} should be a Metabolite'.format(i))
        if isinstance(self.products, Metabolite) == False:
            raise Error.InputError('{} should be a Metabolite'.format(self.reactants))

        if isinstance(self.products, list):
            for i in self.products:
                if isinstance(i, Metabolite) == False:
                    raise Error.InputError('{} should be a Metabolite'.format(i))
        if isinstance(self.products, Metabolite) == False:
            raise Error.InputError('{} should be a Metabolite'.format(self.reactants))


class Function(_base._Base):
    """
    Class to hold copasi function definitions for rate laws
    """

    def __init__(self, **kwargs):
        super(Function, self).__init__(**kwargs)
        self.allowed_properties = {'name':None,
                        'key':None,
                        'type':None,
                        'reversible':None}

        for key in self.kwargs:
            if key not in self.allowed_properties:
                raise Errors.InputError('{} not in {}'.format(key, allowed_properties))
        self.update_properties(self.allowed_properties)

    def __str__(self):
        return 'Function({})'.format(self.to_string())

    def __repr__(self):
        return self.__str__()

class LocalParameter(_base._Base):
    def __init__(self, **kwargs):
        super(LocalParameter, self).__init__(**kwargs)
        self.allowed_properties = {'name':None,
                                   'key':None,
                                   'value':None,
                                   'simulation_type':None,
                                   'parameter_type':None,
                                   'reaction_name': None,
                                   'global_name': None}
                                   # 'global_name': '({}).{}'.format(self.reaction_name,
                                   #                                 self.name)}


        for key in self.kwargs:
            if key not in self.allowed_properties:
                raise Errors.InputError('{} not in {}'.format(key, allowed_properties))
        self.update_properties(self.allowed_properties)

    def __str__(self):
        return 'LocalParameter({})'.format(self.to_string())

    def __repr__(self):
        return self.__str__()

    @property
    def reference(self):
        return "Vector=Reactions[{}],ParameterGroup=Parameters,Parameter={},Reference=Value".format(self.reaction_name, self.name)




















