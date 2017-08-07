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

class Model(_base._ModelBase):
    def __init__(self, model, **kwargs):
        super(Model, self).__init__(model, **kwargs)

    @property
    def time(self):
        """

        :return:
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.model.xpath(query)[0].attrib['timeUnit']

    @property
    def name(self):
        """

        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.model.xpath(query)[0].attrib['name']

    @property
    def volume(self):
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.model.xpath(query)[0].attrib['volumeUnit']

    @property
    def quantity(self):
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.model.xpath(query)[0].attrib['quantityUnit']

    @property
    def area(self):
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.model.xpath(query)[0].attrib['areaUnit']

    @property
    def length(self):
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.model.xpath(query)[0].attrib['lengthUnit']

    @property
    def avagadro(self):
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return float(self.model.xpath(query)[0].attrib['avogadroConstant'])

    @property
    def key(self):
        """
        Get the model reference - the 'key' from self.get_model_units
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.model.xpath(query)[0].attrib['key']

    @property
    def states(self):
        """
        The states (metabolites and globals) in the order they
        are read by Copasi from the StateTemplate element.
        :Returns: set.
        """
        collection = []
        for i in self.model.iter():
            if i.tag == '{http://www.copasi.org/static/schema}StateTemplate':
                for j in i:
                    collection.append(j.attrib['objectReference'])

        query = '//*[@type="initialState"]'
        for i in self.model.xpath(query):
            state_values = i.text

        state_values = state_values.split(' ')
        state_values = [i for i in state_values if i not in ['',' ', '\n']]
        state_values = [float(i) for i in state_values]
        return  dict(zip(collection, state_values))

    def compartments(self):
        """
        Get dict of compartments. dict[compartment_name] = corresponding xml code as nested dict
        """
        collection= {}
        lst = []
        for i in self.model.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfCompartments':
                df_list = []
                for j in i:
                    key, name, type, value = j.attrib.values()
                    lst.append(Compartment(key=key, name=name, type=type, value=float(value)))
        # return pandas.concat([i.as_df() for i in lst], axis=1)
        return lst

    @property
    def metabolites(self):
        """
        List of model metabolites as type metabolite
        :return: Metabolite

        name, compartment, key, conc, particle
        """
        collection = {}
        for i in self.model.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfMetabolites':
                for j in i:
                    collection[j.attrib['key']] = dict(j.attrib)


        for key in collection:
            collection[key]['particle_number'] = self.states[key]


        keys = [collection[metab]['compartment'] for metab in collection]
        comp_dct = {}
        for key in keys:
            comp_dct[key] = [i for i in self.compartments()  if i.key==key][0]

        for key in collection:
            comp_key = collection[key]['compartment']
            collection[key]['compartment']=comp_dct[comp_key]

        lst = []
        for key in collection:
            lst.append(Metabolite(name=collection[key]['name'],
                            compartment=collection[key]['compartment'],
                            key=collection[key]['key'],
                            particle_number=collection[key]['particle_number']) )

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
        for i in self.model.iter():
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
        for i in self.model.xpath(query):
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
                                      type=model_values[key]['simulationType'],
                                      value=model_values[key]['value']))
        return lst

    @property
    def local_parameters(self):
        """
        return local parameters used in your model

        :return:list of Parameters
        """
        query='//*[@cn="String=Kinetic Parameters"]'
        d={}
        for i in self.model.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['simulationType']=='fixed':
                        match=re.findall('Reactions\[(.*)\].*Parameter=(.*)', k.attrib['cn'])[0]
                        assert isinstance(match,tuple),'get species regex hasn\'t been found. Do you have species in your model?'
                        assert match !=None
                        assert match !=[]
                        assert len(match)==2
                        match='({}).{}'.format(match[0],match[1])
                        d[match]=k.attrib

        parameters = {}
        count = 0
        for i in self.model.iter():
            if i.tag == '{http://www.copasi.org/static/schema}Constant':
                reaction_name = i.getparent().getparent().attrib['name']
                parameter_name = i.attrib['name']
                id = "({}).{}".format(reaction_name, parameter_name)
                parameters[id] = {}
                parameters[id] = i.attrib['key']
                count += 1

        lst =[]
        for param in parameters:
            if param in d.keys():
                d[param]['key'] = parameters[param]
                lst.append(LocalParameter(**d[param]))
                # print d[param]
        return lst

    @property
    def functions(self):
        """
        get model functions
        :return: return list of functions from ListOfFunctions
        """
        lst = []
        for element in self.model.iter():
            if element.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
                for child in list(element):
                    lst.append( Function(**child.attrib) )
        return lst

    @property
    def number_of_reactions(self):
        count = 0
        for i in self.model.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in list(i):
                    count = count + 1
        return count

    # def reactions(self):
    #     """
    #
    #     key, name, reversible,
    #     prmeter, substrate, products, stoiciometry
    #
    #     reaction class needs a stoiciometry
    #     :return:
    #
    #
    #     Count the number of reactions in the model and hold as constant.
    #     Then iterate over the number of reactions rather than the reactiosn themselves.
    #     This way if  reaction doesnt have a substrate or product we catch it.
    #
    #     I think this way is slightly failing. Maybe I can write a method for building individual
    #     reactions rather than all reactions at the same time from ListOfReactions.
    #     """
    #     reactions = {}
    #     s = []
    #     p = []
    #     c = []
    #     f = []
    #
    #     for i in self.model.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
    #             for j in list(i):
    #                 reactions[j.attrib['key']] = {}
    #                 reactions[j.attrib['key']]['name'] = j.attrib['name']
    #                 reactions[j.attrib['key']]['reversible'] = j.attrib['reversible']
    #                 for k in list(j):
    #                     if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
    #                         for substrate in list(k):
    #                             print substrate.attrib
                            # for substrate_num in range(self.number_of_reactions):
                                # print k[1]
                                # print [l for l in self.metabolites if l.key in k]
                                # substrate_list = [l for l in self.metabolites if l.key in k[substrate_num].attrib['metabolite']]
                                # substrate_list = [l.to_substrate() for l in substrate_list]
                                # s.append(substrate_list)
                        # elif k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
                        #     for product_num in range(self.number_of_reactions):
                        #         print self.number_of_reactions
                                # print substrate.attrib['metabolite']
                                # product_list = [l for l in self.metabolites if l.key in k[product_num].attrib['metabolite']]
                                # product_list = [l.to_product() for l in product_list]
                                # p.append(product_list)
        # for i in p:
        #     print i
                        # elif k.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                        #     for constant in list(k):
                        #         constant_list = [l for l in self.local_parameters if l.key in constant.attrib['key']]
                        #         c.append(constant_list)
                        # elif k.tag == '{http://www.copasi.org/static/schema}KineticLaw':
                        #     function_list = [l for l in self.functions if l.key in k.attrib['function']]
                        #     f.append(function_list)

        # print len(s), len(p), len(c), len(f)

        # print len(s), len(p)
        # for i in p:
        #     print i
        # if len(s)!= len(p):
        #     raise Errors.SomethingWentHorriblyWrongError(
        #         'number of substrate lists not equal to number of product lists')
        #
        # if len(s) != len(c):
        #     raise Errors.SomethingWentHorriblyWrongError(
        #         'number of constant lists not equal to number of product lists')
        #
        # if len(s) != len(f):
        #     raise Errors.SomethingWentHorriblyWrongError(
        #         'number of function lists not equal to number of product lists')
#




class Compartment(_base._Base):
    def __init__(self, **kwargs):
        super(Compartment, self).__init__(**kwargs)
        self.allowed_keys = {'name',
                             'key',
                             'value',
                             'type'}

        for key in self.kwargs:
            if key not in self.allowed_keys:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, self.allowed_keys))

        self._do_checks()


    def __str__(self):
        return 'Compartment({})'.format(self.as_string())

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
        self.allowed_keys = ['compartment',
                             'key',
                             'name',
                             'particle_number',
                             'concentration',
                             'stoiciometry',
                             'reaction_key'
                             ]

        for key in kwargs:
            if key not in self.allowed_keys:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, self.allowed_keys) )
        ##update all keys to none
        self._do_checks()

    def __str__(self):
        return 'Metabolite({})'.format(self.as_string())

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
    def reference(self):
        """
        The copasi object reference for
        transient metabolite
        :return:
        """
        return 'Vector=Metabolites[{}]'.format(self.name)

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
        avagadro=6.02214179e+023
        molarity=float(particles)/(avagadro*mol_unit_value*compartment_volume)
        if mol_unit=='dimensionless':
            molarity=float(particles)
        if mol_unit=='#':
            molarity=float(particles)
        return round(molarity,33)

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
        avagadro=6.02214179e+023
        particles=float(moles)*avagadro*mol_unit_value*compartment_volume
        if mol_unit=='dimensionless':# or '#':
            particles=float(moles)
        if mol_unit=='#':
            particles=float(moles)
        return particles

    def to_substrate(self):
        return Substrate(**self.kwargs)

    def to_product(self):
        return Product(**self.kwargs)

class Substrate(Metabolite):
    def __init__(self, **kwargs):
        super(Substrate, self).__init__(**kwargs)

        ## in addition to Metboliteproperties
        ## substrates and products need
        ## stoiciometry

        for key in self.kwargs:
            if key not in self.allowed_keys:
                raise Errors.InputError('{} not in {}'.format(key, self.allowed_keys))

    def __str__(self):
        """

        :return:
        """
        return 'Substrate({})'.format(self.as_string())


    def __repr__(self):
        return self.__str__()


class Product(Metabolite):
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

        ## in addition to Metboliteproperties
        ## substrates and products need
        ## stoiciometry

        for key in self.kwargs:
            if key not in self.allowed_keys:
                raise Errors.InputError('{} not in {}'.format(key, self.allowed_keys))

    def __str__(self):
        """

        :return:
        """
        return 'Product({})'.format(self.as_string())


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

        allowed_keys = {'name',
                        'key',
                        'type',
                        'value',
                        }

        for key in kwargs:
            if key not in allowed_keys:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, allowed_keys) )
        ##update all keys to none
        self._do_checks()

    def _do_checks(self):
        if self.type not in ['fixed','assignment']:
            raise Errors.InputError('type should be either fixed or assignment. ODE not supported as Reactions can be used.')

        if self.type == 'assignment':
            Errors.NotImplementedError('Assignments not yet implemented')

    def __str__(self):
        return 'GlobalQuantity({})'.format(self.as_string())

    def __repr__(self):
        return self.__str__()


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
        self.allowed_keys = ['name',
                             'key',
                             'reactants',
                             'products',
                             'rate_law',
                             'parameters']
        for key in self.kwargs:
            if key not in self.allowed_keys:
                raise Errors.InputError('{} not valid key. Valid keys are: {}'.format(key, self.allowed_keys))

        def __str__(self):
            return 'Reaction({})'.format(self.as_string())

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
        allowed_keys = ['name',
                        'key',
                        'type',
                        'reversible']

        for key in self.kwargs:
            if key not in allowed_keys:
                raise Errors.InputError('{} not in {}'.format(key, allowed_keys))

    def __str__(self):
        return 'Function({})'.format(self.as_string())

    def __repr__(self):
        return self.__str__()




class LocalParameter(_base._Base):
    def __init__(self, **kwargs):
        super(LocalParameter, self).__init__(**kwargs)
        allowed_keys = {'name',
                        'key',
                        'value',
                        'simulationType',
                        'type',
                        'cn'}


        for key in self.kwargs:
            if key not in allowed_keys:
                raise Errors.InputError('{} not in {}'.format(key, allowed_keys))

    def __str__(self):
        return 'LocalParameter({})'.format(self.as_string())

    def __repr__(self):
        return self.__str__()





















