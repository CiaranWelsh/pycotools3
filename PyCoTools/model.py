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
        return set(collection)

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

    # @property
    def metabolites(self):
        """
        List of model metabolites as type metabolite
        :return: Metabolite

        name, compartment, key, conc, particle
        """
        query='//*[@cn="String=Initial Species Values"]'
        for i in self.model.xpath(query):
            for j in list(i):
                match=re.findall('.*Vector=Metabolites\[(.*)\]',j.attrib['cn'])
                if match == []:
                    return self.copasiML
                else:

                    comp = re.findall('Compartments\[(.*?)\]', j.attrib['cn'])[0]
                    compartment_vol = self.get_compartments().loc[comp]['Value']
        return

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
        allowed_keys = {'compartment',
                        'key',
                        'name',
                        'particle_number',
                        'concentration'}

        for key in kwargs:
            if key not in allowed_keys:
                raise Errors.InputError('Attribute not allowed. {} not in {}'.format(key, allowed_keys) )
        ##update all keys to none
        self._do_checks()
        # print self.as_string()


    def __str__(self):
        """

        :return:
        """
        return 'Metabolite({})'.format(self.as_string())

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


class Reaction(_base._Base):
    """
    Reactions have rectants, products, rate laws and parameters
    Not sure if this is a priority just yet
    """
    pass



class LocalParameter(_base._Base):
    def __init__(self, **kwargs):
        super(LocalParameter, self).__init__(**kwargs)
        allowed_keys = {'name',
                        'key',
                        'value'}

























