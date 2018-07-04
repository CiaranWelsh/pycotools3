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
import errors, misc, viz
import _base
import tasks
import pandas
import re
import sys, inspect
from copy import deepcopy
from mixin import mixin, Mixin
from functools import wraps
from cached_property import cached_property_with_ttl, cached_property
from subprocess import check_call, call
from shutil import copy
from functools import reduce

LOG = logging.getLogger(__name__)

try:
    import tellurium as te

except ImportError:
    LOG.warning('tellurium module not loaded. Either install with `pip install tellurium` '
                'or if its already installed there could be a problem with tellurium '
                'and the tellurium functions of PyCoTools will be temporarile unavailable')
    pass


## TODO add list of reports property to model
## TODO after running a task, bind the results to the model instance so that they are retrievable


class GetModelComponentFromStringMixin(Mixin):
    """
    For Developers

    Take a :py:class:`Model`, a component type and a string giving
    the name of that component and return the pycotools object
    for that component. Uses :py:meth:`Model.get`. Implemented as
    :py:mod:`mixin` to facilitate reuse across all necessary classes.

    .. highlight::

        @mixin(GetModelComponentFromStringMixin)
        class NewClass(object):
            def __init__(self, model, component, string):
                self.model = model
                self.component = component
                self.string = string

            def use_get_component(self):
                \"""
                Demonstration of how to use
                GetModelComponentFromStringMixin
                :return: model component
                \"""
                return self.get_component(
                    self.model, self.component, self.string
                )
        ## Get global quantity called 'A'
        >>> new_class = NewClass(model, 'global_quantity', 'A')
        >>> A = new_class.use_get_component()

        ## Get metabolite called B
        >>> new_class = NewClass(model, 'metabolite', 'B')
        >>> b = new_class.use_get_component()

        >>> ## Get reaction called A2B
        >>> new_class = NewClass(model, 'reaction', 'A2B')
        >>> c = new_class.use_get_component()
    """

    @staticmethod
    def get_component(model, component, string):
        """
        Get component called string from model

        :param model:
            a pytocools :py:class:`Model`

        :param component:
            a :py:mod:`model` component

        :param string:
            `str`. name of model component

        :return: `model.<component>`
        """
        if isinstance(component, LocalParameter):
            return model.get(component, string, by='global_name')
        else:
            return model.get(component, string, by='name')


class ComparisonMethodsMixin(Mixin):
    """
    For Developers.

    Not presently used in any object
    but ready for future implementation.

    Over ride the magic methods `__eq__`,
    `__ne__` and `__hash__`.  This code comes from directly from
    [Stack overflow](https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
) and enables the of `==` and `!=`  for comparisons.

    This is implemented as a Mixin since its general
    code which can be used for multiple classes

    Usage:
        @mixin(ComparisonMethodsMixin)
        class NewClass(object):
            def __init__(self):
                \"""
                Cool new code here
                \"""
                 pass
    """

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))


class Build(object):
    """
    Context manager for building a copasi model with
    only PyCoTools Functions.

    Users should also see :py:class:`BuildAntimony'
    """

    def __init__(self, copasi_file):
        self.copasi_file = copasi_file

    def __enter__(self):
        self.model = Model(self.copasi_file, new=True)
        return self.model

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.model.save()
        self.model = Model(self.copasi_file, new=True)


class BuildAntimony(object):
    """
    Context manager around telluriums antimony to SBML conversion.
    Builds an sbml from antimony code, converts it to a copasi
    file which is then coerced into a pycotools model.
    """

    def __init__(self, copasi_file):
        self.copasi_file = copasi_file
        self.copasiSE_output_file = self.copasi_file[:-4] + '.sbml.cps'
        self.sbml_file = os.path.splitext(self.copasi_file)[0] + '.sbml'
        ## place for saving model
        self.mod = None
        ## place for saving any exceptions that occur
        self.E = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ## remove intermediate sbml file
        if os.path.isfile(self.sbml_file):
            os.remove(self.sbml_file)

        if isinstance(exc_type, type):
            raise exc_type(exc_val)#.with_traceback(exc_tb)

    def load(self, antimony_str):
        """
        :param antimony_str:
        :return:
        """
        ## wrap conversion function in try block
        ## so we can store the exception
        ## for raising in the __exit__ function
        ## Otherwise the error gets suppressed.
        self.sbml = te.antimonyToSBML(antimony_str)

        ## save sbml
        with open(self.sbml_file, 'w') as f:
            f.write(self.sbml)

        ## ensure sbml exists. This code should never be invoked
        if not os.path.isfile(self.sbml_file):
            raise errors.FileDoesNotExistError('Sbml file does not exist')

        ## Perform conversion wtih CopasiSE
        check_call(['CopasiSE', '-i', self.sbml_file])

        ## copy from temporary copasiSE output name to user specified name
        copy(self.copasiSE_output_file, self.copasi_file)
        os.remove(self.copasiSE_output_file)

        ## create a pycotools model from the resulting copasi_file
        self.mod = Model(self.copasi_file)

        ## return the model so that we can change its name on exit
        return self.mod


class ImportSBML(object):
    """
    Accepts an SBML file, converts it to copasi
    format and reads it into a Model object
    """

    def __init__(self, sbml_file, copasi_file=None):
        """

        :param sbml_file:
        :param copasi_file: Defaults is None. If left None,
                            copasi filename is the same as
                            sbml_file with cps extension.
        """
        self.sbml_file = sbml_file
        self.copasi_file = copasi_file

        if self.copasi_file is None:
            self.copasi_file = self.copasi_filename()

        if os.path.splitext(self.sbml_file)[1] != '.sbml':
            raise errors.InputError('"sbml_file" argument should be an sbml file. '
                                    'Got "{}" instead'.format(self.sbml_file))

        self.convert()

        self.model = self.load_model()

    def copasi_filename(self):
        return os.path.splitext(self.sbml_file)[0] + '.cps'

    def convert(self):
        """
        Perform conversion using CopasiSE
        :return: 
        """
        check_call(['CopasiSE', '-i', self.sbml_file])
        temp_copasi_file = self.sbml_file + '.cps'
        if not os.path.isfile(temp_copasi_file):
            raise errors.FileDoesNotExistError('SBML file has not been translated. '
                                               'Please ensure your environment variables are '
                                               'correctly configured so that the "CopasiSE" command'
                                               ' gives you the CopasiSE help text. ')

        ## copy to desired copasi filename
        copy(temp_copasi_file, self.copasi_file)

        ##remove temporary copasi file
        os.remove(temp_copasi_file)

        return self.copasi_file

    def load_model(self):
        return Model(self.copasi_file)


class Model(_base._Base):
    """
    The Model object is of central importance in pycotools as
    it extracts relevant information from a copasi definition
    file into python objects.

    These are :py:class:`Model` properties:

    =======================     =======================
    Property                    Description
    =======================     =======================
    copasi_file                 Full path to model
    root                        Full path directory containing model
    reference                   Copasi model reference
    time_unit                   Time unit
    name                        Model name
    volume_unit                 Volume unit
    quantity_unit               Quantity unit
    area_unit                   Area Unit
    length_unit                 Length unit
    avagadro                    Avagadro's number
    key                         Model key
    states                      List of states in correct order defined
                                by copasi StateTemplate element.
    fit_item_order              Order in which fit items appear
    all_variable_names          List of reactions, metabolites, global_quantities
                                local_parameters, compartment names as string
    number_of_reactions         Number of reactions in :py:class:`model.Model`
    =======================     =======================


    Properties get re-evaluate each time they are called which
    is expensive due to re-reading the xml and unnecessary.
    The :py:mod:`cached_property` module written by Daniel Greenfeld and redistributed
    in pycotools enables these components to be read once and cached for later use. This
    cache set on instantiation is reset each time a new component is added or changed.
    The following components are cached_properties:

    =======================     =======================
    Cached Property                    Description
    =======================     =======================
    compartments                List of :py:class:`model.Compartment`
    metabolites                 List of :py:class:`model.Metabolite`
    global_quantities           List of :py:class:`model.GlobalQuantity`
    functions                   List of :py:class:`model.Function`
    parameter_descriptions      List of :py:class:'model.ParameterDescription`
    constants                   List of :py:class:`LocalParameter`
    reactions                   List of :py:class:`Reaction`
    parameters                  List of :py:class:'LocalParameter`
    =======================     =======================

    Usage:
        >>> from pycotools.model import Model
        >>> model_path = r'/full/path/to/model.cps'
        >>> model = Model(model_path) ##work in concentration units
        >>> model = Model(model_path, quantity_type='particle_numbers') ## work in particle numbers

    """

    def __init__(self, copasi_file, quantity_type='concentration',
                 new=False, **kwargs):
        """
        :param copasi_file:
            `str`. Full path to a copasi file

        :param quantity_type:
            `str`. 'concentration' or 'particle_numbers'

        :param new:
            `bool`. Begin new empty model. Untested.

        :param kwargs:
            Unused.
        """
        super(Model, self).__init__(**kwargs)
        self._copasi_file = copasi_file
        self.quantity_type = quantity_type
        self.new_model = new
        if self.new_model:
            misc.new_model(copasi_file)
        self.xml = tasks.CopasiMLParser(copasi_file).copasiML
        ## fill this dict after class is finished
        self.default_properties = {}
        self.default_properties.update(kwargs)

        if self.quantity_type not in ['concentration',
                                      'particle_numbers']:
            raise errors.InputError('quantity_type argument should be concentration or particle_numbers')

    def __str__(self):
        return 'Model(name={}, time_unit={}, volume_unit={}, quantity_unit={})'.format(self.name, self.time_unit,
                                                                                       self.volume_unit,
                                                                                       self.quantity_unit)

    def __repr__(self):
        return self.__str__()

    def reset_cache(self, prop):
        """
        Delete property from cache then
        reset it

        :param prop:
            `str`. property to reset

        :return:
            :py:class:`Model`
        """
        if prop not in self.__dict__:
            raise errors.InputError('Property "{}" does not '
                                    'exist from model.Model class'.format(prop))
        del self.__dict__[prop]
        getattr(self, prop)
        return self

    @property
    def copasi_file(self):
        """
        Return the copasi file from which the
        :py:class:`Model` was built

        :return:
            str.
        """
        return self._copasi_file

    @copasi_file.setter
    def copasi_file(self, filename):
        """
        Set the copasi file

        :param filename:
            str. Different path.

        :return: None
        """
        fle, ext = os.path.splitext(filename)
        if ext != '.cps':
            raise errors.InputError('expected a .cps file. Got {} instead'.format(ext))
        self._copasi_file = filename

    def copy(self, filename):
        """
        Copy the model to `filename`

        :return:
            :py:class:`Model`

        """
        model = deepcopy(self)
        model.copasi_file = filename
        return model

    # def refresh(self):
    #     """
    #     Refresh the model by reading the xml
    #     into :py:mod:`lxml.etree` again.
    #
    #     :return: :py:class:`Model`
    #     """
    #
    #     self.xml = tasks.CopasiMLParser(self.copasi_file).copasiML
    #     return self

    def to_antimony(self):
        """
        Return model as Antimony model string
        :return:
        """
        sbml_file = self.to_sbml()
        assert os.path.isfile(sbml_file)
        with open(sbml_file) as f:
            antimony = te.sbmlToAntimony(f.read())
        os.remove(sbml_file)
        return antimony

    @property
    def root(self):
        """
        Root directory for model. The directory
        where copasi_file is saved.

        Does not need a setter since root is derived from
        copasi_file property

        :return:
            `str`
        """
        return os.path.dirname(self.copasi_file)

    @property
    def reference(self):
        """
        Get model reference from xml

        :return:
            `str`
        """
        return "CN=Root,Model={}".format(self.name)

    @property
    def time_unit(self):
        """

        :return:
            `str` current time unit defined by copasi
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['timeUnit']

    @property
    def name(self):
        """

        :return:
            `str`. The model name
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['name']

    @name.setter
    def name(self, name):
        """

        name setter

        :param name:
            `str`

        :return: :py:class:`Model`
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        self.xml.xpath(query)[0].attrib['name'] = str(name)
        return self

    @property
    def volume_unit(self):
        """

        :return:
            `str`. The currently defined volume unit
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['volumeUnit']

    @property
    def quantity_unit(self):
        """

        :return:
            `str`. The currently defined quantity unit
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['quantityUnit']

    @property
    def area_unit(self):
        """

        :return:
            `str`. The currently defined area unit.
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['areaUnit']

    @property
    def length_unit(self):
        """

        :return:
            `str`
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['lengthUnit']

    @property
    def avagadro(self):
        """
        Not really needed but good to check
        consistancy of avagadros number.
        **This number was updated between between version 16 and 19

        :return:
            `int`
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        avagadro_from_model = float(self.xml.xpath(query)[0].attrib['avogadroConstant'])
        avagadros_from_version19 = 6.022140857e+23
        if avagadro_from_model != avagadros_from_version19:
            raise errors.AvagadrosError(
                'Avagadro from model {} is not equal to {}. Check to see whether COPASI have updated the value of avagadro\'s number'.format(
                    avagadro_from_model, avagadros_from_version19))
        return avagadro_from_model

    @property
    def key(self):
        """
        Get the model reference - the 'key' from self.get_model_units

        :return:
            `str`
        """
        query = '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.xml.xpath(query)[0].attrib['key']

    @property
    def states(self):
        """
        The states (metabolites, globals, compartments) in the order they
        are read by Copasi from the StateTemplate element.

        :return:
            `OrderedDict`
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
        state_values = [i for i in state_values if i not in ['', ' ', '\n']]
        state_values = [float(i) for i in state_values]

        return OrderedDict(list(zip(collection, state_values)))

    @states.setter
    def states(self, states):
        """
        :param states:
            `list`. list of `int` of len(self.states)

        :return:
            :py:class:`Model`
        """
        ## first check what data type states is
        if not isinstance(states, str):
            ## if not str then convert list to str in appropriate format
            state_string = reduce(lambda x, y: '{} {}'.format(x, y), states)

        ## get number of model states
        number_of_model_states = len(self.states)

        ##check we have correct number of model states
        if len(states) != number_of_model_states:
            raise errors.InputError(
                'Not entered the currect number of states. Expected {} and got {}'.format(number_of_model_states,
                                                                                          len(states)))

        ## enter states into model
        query = '//*[@type="initialState"]'
        for i in self.xml.xpath(query):
            i.text = state_string
        return self

    @property
    def fit_item_order(self):
        """
        Get names of parameters being fitted in the
        order they appear

        :return:
            `list`
        """
        lst = []
        query = '//*[@name="FitItem"]'
        for i in self.xml.xpath(query):
            ## exclude FitItems that match elements of the constraint list
            if i.getparent().attrib['name'] == 'OptimizationConstraintList':
                continue

            for j in list(i):
                if j.attrib['name'] == 'ObjectCN':
                    match = re.findall('Reference=(.*)', j.attrib['value'])[0]

                    if match == 'Value':
                        match2 = re.findall('Reactions\[(.*)\].*Parameter=(.*),', j.attrib['value'])[0]
                        match2 = '({}).{}'.format(match2[0], match2[1])
                        lst.append(match2)

                    elif match == 'InitialValue':
                        match2 = re.findall('Values\[(.*)\]', j.attrib['value'])[0]
                        lst.append(match2)

                    elif match == 'InitialConcentration':
                        match2 = re.findall('Metabolites\[(.*)\]', j.attrib['value'])[0]
                        lst.append(match2)
        return lst

    def add_state(self, state, value):
        """
        Append state on to end of state template.
        Used within add_metabolite and add_global_quantity. Shouldn't
        need to use manually

        :param state:
            `str`. A valid key

        :param value:
            `int`, `float`. Value for state

        :return:
        """
        element = etree.Element('{http://www.copasi.org/static/schema}StateTemplateVariable',
                                attrib={'objectReference': state})
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}StateTemplate':
                i.append(element)
                for j in i.getparent():
                    if j.tag == '{http://www.copasi.org/static/schema}InitialState':
                        j.text = "{} {} \n".format(j.text.replace('\n', '').strip(), str(value))  # + '\n'
        return self

    def remove_state(self, state):
        """
        Remove state from StateTemplate and
        InitialState fields. USed for deleting metabolites
        and global quantities.

        :param state:
            `str`. key of state to remove (i.e. Metabolite_1)

        :return:
            :py:class:`Model`
        """
        ##count the number of states
        count = -1  # 0 indexed python

        stop_count = 0
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}StateTemplate':
                for j in i:
                    count = count + 1
                    if j.attrib['objectReference'] == state:
                        j.getparent().remove(j)
                        ##collect the number where we hit our desired state
                        stop_count = count

            if i.tag == '{http://www.copasi.org/static/schema}InitialState':
                states = i.text.strip().split(' ')
                del states[stop_count]  ## get component of interest
        # reassign the states list to the InitialState
        states = [float(i) for i in states]
        self.states = states
        return self

    # @property
    @cached_property
    def compartments(self):
        """
        Get list of model compartments

        :return:
            `list`. Each element is :py:class:`Compartment`
        """
        collection = {}
        lst = []
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfCompartments':
                df_list = []
                for j in i:
                    lst.append(Compartment(self,
                                           key=j.attrib['key'],
                                           name=j.attrib['name'],
                                           simulation_type=j.attrib['simulationType'],
                                           initial_value=float(self.states[j.attrib['key']])))
        if 'compartments' in self.__dict__:
            del self.__dict__['compartments']

        return lst

    def add_compartment(self, compartment):
        """
        Add compartment to model

        :param compartment:
            :py:class:`Compartment`

        :return:
            :py:class:`Model`
        """
        if isinstance(compartment, str):
            compartment = Compartment(self, compartment)

        if not isinstance(compartment, Compartment):
            raise errors.InputError(
                'Expecting "{}" but '
                'got "{}" instead'.format('Compartment', type(compartment))
            )

        ## ensure we don't add compartment with existing name
        existing = self.get('compartment', compartment.name, by='name')
        if existing != []:
            LOG.info(
                'Model already contains compartment '
                'with name: "{}". Skipping'.format(compartment.name)
            )
            return self

        ## ensure we don't add compartment with existing key
        existing = self.get('compartment', compartment.key, by='key')
        if existing != []:
            raise errors.AlreadyExistsError(
                'Model already contains compartment '
                'with key: "{}"'.format(compartment.key)
            )

        if 'compartments' in self.__dict__:
            del self.__dict__['compartments']

        ## if ListOfCompartment tag not exist, create
        comp_tag = '{http://www.copasi.org/static/schema}ListOfCompartments'
        mod_tag = '{http://www.copasi.org/static/schema}Model'
        miriam = r'{http://www.copasi.org/static/schema}MiriamAnnotation'

        if self.xml.find(mod_tag).find(comp_tag) is None:
            new_comp = etree.Element('{http://www.copasi.org/static/schema}ListOfCompartments')
            for i in range(len(self.xml.find(mod_tag))):
                if self.xml.find(mod_tag)[i].tag == miriam:
                    miriam_index = i

            self.xml.find(mod_tag).insert(miriam_index + 1, new_comp)

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

        :param value:
            `str`. Value of attribute to match i.e. 'Nucleus'

        :param by:
            `str` which attribute to match i.e. 'name' or 'key'

        :return:
            :py:class:`Model`
        """
        ## get the compartment
        comp = self.get('compartment', value, by=by)

        if comp == []:
            raise errors.ComponentDoesNotExistError('Component with {}={} does not exist'.format(by, value))

        ## first remove compartment from list of compartments
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfCompartments':
                for j in i:
                    if j.attrib[by] == value:
                        j.getparent().remove(j)

        ## then remove from state template and initial state
        self.remove_state(comp.key)
        if 'compartments' in self.__dict__:
            del self.__dict__['compartments']
        return self

    @property
    def all_variable_names(self):
        """
        The names of all compartments, metabolites, global quantities,
        reactions and local parameters in the model.

        :return:
            `list`. Each element is `str`
        """
        ##first delete from cache
        m = [i.name for i in self.metabolites]
        g = [i.name for i in self.global_quantities]
        l = [i.global_name for i in self.local_parameters]
        c = [i.name for i in self.compartments]
        return m + g + l + c

    @cached_property
    def local_parameters(self):
        """
        Get local parameters in model. local_parameters are
        those which are actively used in reactions and do not have
        a global variable assigned to them. The constant property
        returns all local parameters regardless of simulation type
        (fixed or assignment)

        :return:
            `list`. Each element is :py:class:`LocalParameter`
        """
        # if 'local_parameters' in self.__dict__:
        #     del self.__dict__['local_parameters']

        loc = self.constants

        ## We don't want to consider parameters tahat have already been assigned
        ## to a global parameter in any downstream operation.
        ##therefore we remove locals with assignments
        loc = [i for i in loc if i.simulation_type != 'assignment']
        return loc

    def add_local_parameter(self, local_parameter):
        """
        Add a local parameter to the model, specifically into
        the String='kinetic Parameters' section of parameter sets

        :param local_parameter:
            :py:class:`LocalParameter`

        :return:
            :py:class:`Model`
        """
        ## remove frome cache
        if 'local_parameters' in self.__dict__:
            del self.__dict__['local_parameters']

        ## do not add if already exists
        if local_parameter.global_name in [i.global_name for i in self.local_parameters]:
            return self

        query = '//*[@cn="String=Kinetic Parameters"]'
        for i in self.xml.xpath(query):
            i.append(local_parameter.to_xml())

        # self.refresh()
        # print self.refresh().local_parameters
        return self

    @staticmethod
    def convert_particles_to_molar(particles, mol_unit, compartment_volume):
        """
        Converts particle numbers to Molarity.

        ##TODO build support for copasi's newest units

        :param particles:
            `int` Number of particles to convert

        :param mol_unit:
            `str`. The quantity unit, i.e:
                fmol, pmol, nmol, umol, mmol or mol

        :param compartment_volume:
            `int`, `float`. Volume of compartment containing specie to convert

        :return:
            `float`. Molarity
        """
        mol_dct = {
            'fmol': 1e-15,
            'pmol': 1e-12,
            'nmol': 1e-9,
            '\xb5mol': 1e-6,
            'mmol': 1e-3,
            'mol': float(1),
            'dimensionless': float(1),
            '1': float(1),
            '#': float(1)}

        try:
            mol_unit_value = mol_dct[mol_unit]
        except KeyError:
            raise KeyError('"{}" unit is not yet supported. Please use a different unit'.format(mol_unit))

        avagadro = 6.022140857e+23

        molarity = float(particles) / (avagadro * mol_unit_value * compartment_volume)
        if mol_unit == 'dimensionless':
            molarity = float(particles)

        if mol_unit == '#':
            molarity = float(particles)

        if mol_unit == '1':
            molarity = float(particles)
        return molarity

    @staticmethod
    def convert_molar_to_particles(moles, mol_unit, compartment_volume):
        """
        Convert molarity to particle numbers

        :param moles:
            `int` or `float`. Number of moles in mol_unit to convert

        :param mol_unit:
            `str`. Mole unit to convert from.
            suppoerted: fmol, pmol, nmol, umol, mmol or mol

        :param compartment_volume:
            `int` or `float`. Volume of compartment containing specie to convert

        :return:
            `int`. number of particles
        """
        '''
        Converts particle numbers to Molarity.
        particles=number of particles you want to convert
        mol_unit=one of, ''
        '''
        if isinstance(compartment_volume, (float, int)) != True:
            raise errors.InputError(
                'compartment_volume is the volume of the compartment for species and must be either a float or a int')

        mol_dct = {
            'fmol': 1e-15,
            'pmol': 1e-12,
            'nmol': 1e-9,
            '\xb5mol': 1e-6,
            'mmol': 1e-3,
            'mol': float(1),
            'dimensionless': 1,
            '1': 1,
            '#': 1}
        try:
            mol_unit_value = mol_dct[mol_unit]
        except KeyError:
            raise KeyError('"{}" unit is not yet supported. Please use a different unit'.format(mol_unit))
        avagadro = 6.022140857e+23
        particles = float(moles) * avagadro * mol_unit_value * compartment_volume

        if mol_unit == 'dimensionless':  # or '#':
            particles = float(moles)

        if mol_unit == '#':
            particles = float(moles)

        if mol_unit == '1':
            molarity = float(particles)
        return particles

    @cached_property
    def metabolites(self):
        """
        :return:
            `list`. Each element is :py:class:`Metabolite`
        """
        metabs = {}
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfMetabolites':
                for j in i:
                    metabs[j.attrib['key']] = j.attrib

        for key, value in list(self.states.items()):
            if key in list(metabs.keys()):
                metabs[key]['particle_numbers'] = str(value)

        lst = []
        for key in metabs:
            comp = self.get('compartment', metabs[key]['compartment'], 'key')
            lst.append(Metabolite(self, name=metabs[key]['name'],
                                  compartment=comp,
                                  key=metabs[key]['key'],
                                  particle_numbers=metabs[key]['particle_numbers'],
                                  concentration=self.convert_particles_to_molar(
                                      metabs[key]['particle_numbers'], self.quantity_unit, comp.initial_value),
                                  simulation_type=metabs[key]['simulationType']))

        return lst

    def add_metabolite(self, metab):
        """
        Add a metabolite to the model xml

        :param metab:
            `str` or :py:class:`Metabolite`. If str
            is the name of metabolite to add and default
            :py:class:`Metabolite` properties are adopted.
            If :py:class:`Metabolite`, a :py:class:`Metabolite`
            instance must be prebuilt and passes as arg.

        :return:
            :py:class:`Model`
        """
        ## if no compartments exist, make one
        if self.compartments == []:
            self.add_component('compartment', 'NewCompartment')
            self.save()

        ## If metab is str convert to Metabolite
        ## with default parameters
        ## This must occur before deleting
        ## the metabolites cache
        if isinstance(metab, str):
            metab = Metabolite(self, metab)

        if 'metabolites' in self.__dict__:
            del self.__dict__['metabolites']

        if not isinstance(metab, Metabolite):
            raise errors.InputError('Input must be Metabolite class')

        ## if ListOfCompartment tag not exist, create
        m = '{http://www.copasi.org/static/schema}ListOfMetabolites'
        mod_tag = '{http://www.copasi.org/static/schema}Model'
        comp = r'{http://www.copasi.org/static/schema}ListOfCompartments'

        if self.xml.find(mod_tag).find(m) is None:
            new_m = etree.Element('{http://www.copasi.org/static/schema}ListOfMetabolites')
            for i in range(len(self.xml.find(mod_tag))):
                if self.xml.find(mod_tag)[i].tag == comp:
                    miriam_index = i

            self.xml.find(mod_tag).insert(miriam_index + 1, new_m)

        metabolite_element = metab.to_xml()
        ## add the metabolute to list of metabolites
        list_of_metabolites = '{http://www.copasi.org/static/schema}ListOfMetabolites'
        for i in self.xml.iter():
            if i.tag == list_of_metabolites:
                i.append(metabolite_element)

        ## add metabolite to state_template and initial state fields
        self.add_state(metab.key, metab.particle_numbers)

        ## call the metabolites property again
        ## to reset the cache
        self.metabolites
        return self

    def remove_metabolite(self, value, by='name'):
        """
        Remove metabolite from model.

        :param value:
            `str`. Attribute value to remove

        :param by:
            `str` Any metabolite attribute type to match

        :return:
            :py:class:`Model`

        Usage:
            ## Remove attribute called 'A'
            >>> model.remove_metabolite('A', by='name')

            ## Remove metabolites with initial concentration of 0
            >>> model.remove_metabolite(0, by='concentration')
        """
        list_of_metabolites = '{http://www.copasi.org/static/schema}ListOfMetabolites'

        metab = self.get('metabolite', value, by=by)
        if metab == []:
            raise TypeError('No metab with "{}" attribute == "{}" exists'.format(by, value))
        for i in self.xml.iter():
            if i.tag == list_of_metabolites:
                for j in i:
                    if j.attrib[by] == value:
                        j.getparent().remove(j)
        self.remove_state(metab.key)

        ## remove cached
        if 'metabolites' in self.__dict__:
            del self.__dict__['metabolites']
        return self

    def add_global_quantity(self, global_quantity):
        """
        Add global quantity to model

        :param global_quantity:
            `str` or :py:class:`GlobalQuantity`. If str
            is the name of global_quantity to add and default
            :py:class:`GlobalQuantity` properties are adopted.
            If :py:class:`GlobalQuantity`, a :py:class:`GlobalQuantity`
            instance must be prebuilt and passes as arg.

        :return:
            :py:class:`Model`
        """

        ## accept str arguments
        if isinstance(global_quantity, str):
            global_quantity = GlobalQuantity(self, global_quantity)

        if not isinstance(global_quantity, GlobalQuantity):
            raise errors.InputError('Input must be a GlobalQuantity')

        ## try and get existing
        existing = self.get('global_quantity', global_quantity.name, by='name')
        if existing != []:
            LOG.info(
                'Model already contains global_quantity '
                'with name: "{}". Skipping'.format(global_quantity.name)
            )
            return self

        if 'global_quantities' in self.__dict__:
            del self.__dict__['global_quantities']

        ## if ListOfCompartment tag not exist, create
        m = '{http://www.copasi.org/static/schema}ListOfModelValues'
        mod_tag = '{http://www.copasi.org/static/schema}Model'
        comp = r'{http://www.copasi.org/static/schema}ListOfCompartments'
        idx = 0
        if self.xml.find(mod_tag).find(m) is None:
            new_m = etree.Element(m)
            for i in range(len(self.xml.find(mod_tag))):
                if self.xml.find(mod_tag)[i].tag == comp:
                    idx = i

            self.xml.find(mod_tag).insert(idx + 1, new_m)

        model_value = global_quantity.to_xml()
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                i.append(model_value)

        self.add_state(global_quantity.key, global_quantity.initial_value)

        self.global_quantities
        return self

    @cached_property
    def global_quantities(self):
        """

        :return:
            `list` each element is :py:class:`GlobalQuantity`
        """
        model_values = {}
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                for j in i:
                    model_values[j.attrib['key']] = j.attrib

        for key, value in list(self.states.items()):
            if key in list(model_values.keys()):
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

        :param value:
            value to match by (i.e. ProteinA or ProteinB)

        :param by:
            attribute to match (i.e. name or key)

        :return:
            :py:class:`model.Model`
        """

        global_value = self.get('global_quantity',
                                value,
                                by)

        ##remove cached
        del self.__dict__['global_quantities']

        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                for j in i:
                    if j.attrib[by] == value:
                        j.getparent().remove(j)

        self.remove_state(global_value.key)
        return self

    @cached_property
    def functions(self):
        """
        get model functions
        :return:
            `list` each element a `py:class:`Function`
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
                                                         role=greatgrandchild.attrib['role']))
                    lst.append(Function(self,
                                        name=name,
                                        key=key,
                                        type=type,
                                        expression=expression,
                                        reversible=reversible,
                                        list_of_parameter_descriptions=list_of_parameter_descriptions))
        return lst

    @property
    def parameter_descriptions(self):
        """

        :return:
            `list`. Each element a :py:class:`ParameterDescription`
        """
        lst = []
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ParameterDescription':
                lst.append(ParameterDescription(self,
                                                name=i.attrib['name'],
                                                key=i.attrib['key'],
                                                order=i.attrib['order'],
                                                role=i.attrib['role']))
        return lst

    def add_function(self, function):
        """
        Add function to model

        :param function:
            :py:class:`Function`.

        :return:
            :py:class:`Model`
        """
        ##commented below bit out. Might still need
        # if function.key == None:
        #     function.key = KeyFactory(self, type='function').generate()

        if function.type == 'user_defined':
            function.type = 'UserDefined'

        if function.reversible == True:
            function.reversible = 'true'
        else:
            function.reversible = 'false'

        ## If ListOfFunctions element not exist, create
        m = '{http://www.copasi.org/static/schema}ListOfFunctions'
        if self.xml.find(m) is None:
            self.xml.insert(0, etree.Element(m))

        ## add the function to list of functions
        if function.key in [i.key for i in self.functions]:
            return self

        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
                i.append(function.to_xml())
        del self.__dict__['functions']
        return self

    def remove_function(self, value, by='name'):
        """
        remove a function from model

        :param value:
            `str` value of attribute to match (i.e the functions name)

        :param by:
            `str` which attribute to match by. default='name'

        :return:
            :py:class:`model.Model`
        """
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfFunctions':
                for j in i:
                    if j.attrib[by] == value:
                        j.getparent().remove(j)
        return self

    @property
    def number_of_reactions(self):
        """
        :return:
            `int` number of reactions
        """
        count = 0
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in list(i):
                    count = count + 1
        return count

    @cached_property
    def constants(self):
        """
        Get list of constants from xml attribute
        `cn="String=Kinetic Parameters"
        :return:
            `list` each element :py:class:`LocalParameter`
        """
        if 'constants' in self.__dict__:
            del self.__dict__['keys']
        query = '//*[@cn="String=Kinetic Parameters"]'
        dct = {}
        for i in self.xml.xpath(query):
            for j in i:
                for k in j:
                    reaction_name, parameter_name = re.findall('.*Reactions\[(.*)\].*Parameter=(.*)', k.attrib['cn'])[0]
                    global_name = "({}).{}".format(reaction_name, parameter_name)
                    value = k.attrib['value']
                    simulation_type = k.attrib['simulationType']
                    dct[global_name] = {}
                    dct[global_name]['reaction_name'] = reaction_name
                    dct[global_name]['parameter_name'] = parameter_name
                    dct[global_name]['value'] = value
                    dct[global_name]['simulation_type'] = simulation_type

        res = []
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    reaction_name = j.attrib['name']
                    for k in j:
                        for l in k:
                            if l.tag == '{http://www.copasi.org/static/schema}Constant':
                                parameter_name = l.attrib['name']
                                global_name = "({}).{}".format(reaction_name, parameter_name)
                                parameter_key = l.attrib['key']
                                loc = LocalParameter(self,
                                                     name=dct[global_name]['parameter_name'],
                                                     value=dct[global_name]['value'],
                                                     key=parameter_key,
                                                     reaction_name=dct[global_name]['reaction_name'],
                                                     global_name=global_name,
                                                     simulation_type=dct[global_name]['simulation_type']
                                                     )
                                res.append(loc)

        return res

    @cached_property
    def reactions(self):
        """
        assemble a list of reactions
        :return:
            `list` each element a :py:class:`Reaction`
        """
        ## make sure list of reaction tag exists befor continuing
        exist = False
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                exist = True

        if exist == False:
            return []

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
                    reactions_dict[reaction_count]['function'] = []
                    for k in list(j):
                        reactions_dict[reaction_count]['reversible'] = j.attrib['reversible']
                        reactions_dict[reaction_count]['name'] = j.attrib['name']
                        reactions_dict[reaction_count]['key'] = j.attrib['key']
                        if k.tag == '{http://www.copasi.org/static/schema}ListOfSubstrates':
                            list_of_substrates = []
                            for l in list(k):
                                substrate = self.get('metabolite', l.attrib['metabolite'], by='key')
                                if isinstance(substrate, list):
                                    raise errors.SomethingWentHorriblyWrongError('substrate matched >1 substrate')
                                ##convert to substrate
                                substrate = substrate.to_substrate()
                                list_of_substrates.append(substrate)
                            reactions_dict[reaction_count]['substrates'] = list_of_substrates

                        elif k.tag == '{http://www.copasi.org/static/schema}ListOfProducts':
                            list_of_products = []
                            for l in list(k):
                                ## get list of metabolites and convert them to Product class
                                product = self.get('metabolite', l.attrib['metabolite'], by='key')
                                product = product.to_product()
                                list_of_products.append(product)
                                reactions_dict[reaction_count]['products'] = list_of_products

                        elif k.tag == '{http://www.copasi.org/static/schema}ListOfModifiers':
                            list_of_modifiers = []
                            for l in list(k):
                                ## get list of metabolites and convert them to Moifier class
                                modifier = self.get('metabolite', l.attrib['metabolite'], by='key')
                                modifier = modifier.to_product()
                                list_of_modifiers.append(modifier)
                                reactions_dict[reaction_count]['modifiers'] = list_of_modifiers

                        elif k.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                            list_of_constants = []

                            ##assertain the parameters simulation type
                            for l in list(k):
                                global_name = "({}).{}".format(j.attrib['name'], l.attrib['name'])
                                # LOG.warning('Experimental section of reactions function')
                                constant = self.get('local_parameter', global_name, by='global_name')
                                list_of_constants.append(constant)

                        elif k.tag == '{http://www.copasi.org/static/schema}KineticLaw':
                            function = self.get('function', k.attrib['function'], by='key')
                            reactions_dict[reaction_count]['function'] = function

        ## assemble the expression for the reaction
        # LOG.warning('move below code to separate function for clean code')
        ## return empty list when no reactions are in model
        if len(reactions_dict) == 0:
            return []

        for i, dct in list(reactions_dict.items()):
            ## default constant flux or mass action
            substrates = [j.name for j in reactions_dict[i]['substrates']]
            if dct['function'] == []:
                # if dct['substrates'] == []:
                #     dct['function'] = "v".format(reduce(lambda x, y: '{}*{}'.format(x, y), products))
                # else:
                dct['function'] = "k*{}".format(reduce(lambda x, y: '{}*{}'.format(x, y), substrates))
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
                raise errors.SomethingWentHorriblyWrongError

            if modifier_expression == '':
                expression = "{} {} {}".format(sub_expression,
                                               operator,
                                               prod_expression)
            else:
                expression = '{} {} {}; {}'.format(sub_expression, operator,
                                                   prod_expression, modifier_expression)
            reactions_dict[i]['expression'] = expression

        lst = []

        for i, dct in list(reactions_dict.items()):
            ## skip the skipped reactions
            # if i not in skipped:
            r = Reaction(self,
                         name=dct['name'].strip(),
                         key=dct['key'],
                         expression=dct['expression'],
                         rate_law=dct['function'],
                         reversible=dct['reversible'],
                         substrates=dct['substrates'],
                         products=dct['products'],
                         parameters=dct['constants'],
                         parameters_dict={j.name: j for j in dct['constants']},
                         )
            lst.append(r)

        # self.reset_cache('reactions')
        return lst

    def add_reaction(self, reaction, expression=None,
                     rate_law=None):
        """
        :param reaction:
            :py:class:`Reaction` or `str`. If `str` then
            must be the name of the reaction.

        :return:
            :py:class:`Model`
        """
        if not isinstance(reaction, Reaction):
            if not isinstance(reaction, str):
                raise errors.InputError(
                    'Expecting Reaction or string as'
                    ' first argument but '
                    'got "{}" instead'.format(type(reaction))
                )
            elif isinstance(reaction, str):
                if expression is None or rate_law is None:
                    raise errors.InputError(
                        'When passing string as first argument '
                        'to add_reaction, the expression and '
                        'rate law arguments must be specified'
                    )
                reaction = Reaction(self, reaction, expression, rate_law)
        ## try and get existing
        existing = self.get('reaction', reaction.name, by='name')
        if existing != []:
            raise errors.AlreadyExistsError(
                'Model already contains reaction '
                'with name: "{}"'.format(reaction.name)
            )

        if reaction.key in [i.key for i in self.reactions]:
            reaction.key = '{}_{}'.format(
                reaction.key.split('_')[0],
                int(reaction.key.split('_')[1]) + 1
            )
            LOG.info('Model already contains a reaction with the key: {}. Changing key'.format(reaction.key))

        if reaction.name in [i.name for i in self.reactions]:
            raise errors.ReactionAlreadyExists(
                'Your model already contains a reaction with the name: {}'.format(reaction.name))

        if 'reactions' in self.__dict__:
            del self.__dict__['reactions']

        existing_functions = [i.name for i in self.functions]
        if reaction.rate_law.name not in existing_functions:
            self.add_function(reaction.rate_law)

        # existing_function = self.get('function', reaction.rate_law.expression, by='expression')
        #
        # if existing_function == []:
        #     self.add_function(reaction.rate_law)
        # else:
        #     LOG.warning('Bug might occur here'
        #                 'if an existing function '
        #                 'exists but has different'
        #                 'roles. then its not the same function'
        #                 'and should be added separetly')
        #     reaction.rate_law = existing_function

        ## if ListOFReactions tag not exist, create
        m = '{http://www.copasi.org/static/schema}ListOfReactions'
        mod_tag = '{http://www.copasi.org/static/schema}Model'
        metab = r'{http://www.copasi.org/static/schema}ListOfMetabolites'
        idx = 0
        if self.xml.find(mod_tag).find(m) is None:
            new_m = etree.Element(m)
            for i in range(len(self.xml.find(mod_tag))):
                if self.xml.find(mod_tag)[i].tag == metab:
                    idx = i

            self.xml.find(mod_tag).insert(idx + 1, new_m)

        for i in self.xml.iter():
            if i.tag == m:
                i.append(reaction.to_xml())
        ## needed?
        # self.save()
        for local_parameter in reaction.parameters:
            if local_parameter.key in [i.key for i in self.local_parameters]:
                local_parameter.key = KeyFactory(self, 'parameter').generate()
            self.add_local_parameter(local_parameter)
        return self.refresh()

    def remove_reaction(self, value, by='name'):
        """
        Remove reaction
        :param value:
            `str`. Value of attibute

        :param by: attribute of reaction to match default='name
            `str` which :py:class`Reaction` atrribute to match

        :return:
            :py:class:`Model`
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

        if 'reactions' in self.__dict__:
            del self.__dict__['reactions']
        return self

    def refresh(self):
        """
        Save the file then reload the Model. Can't use the
        save method though because the save method uses
        the refresh method.
        :return:
        """
        with open(self.copasi_file, 'w') as f:
            f.write(etree.tostring(self.xml, pretty_print=True))

        return Model(self.copasi_file)

    def save(self, copasi_file=None):
        """
        Save copasiML to copasi_filename.

        :param copasi_filename:
            `str` or `None`. Deafult is `None`. When `None`
            defaults to same filepath the model came from.
            If another path, saves to that path.

        :return:
            :py:class:`Model`
        """
        if copasi_file == None:
            copasi_file = self.copasi_file

        ##
        if not os.path.isdir(self.root):
            os.makedirs(self.root)

        ## Then remove existing copasi file for ovewrite
        if os.path.isfile(copasi_file):
            os.remove(copasi_file)

        ## write
        tasks.CopasiMLParser.write_copasi_file(self.copasi_file, self.xml)

        ## update copasi file for when copasi_file is not None
        self.copasi_file = copasi_file
        self.refresh()
        return self

    def open(self, copasi_file=None, as_temp=False):
        """
        Open model with the gui. In order to work
        the environment variables must be properly set
        so that the command `CopasiUI` in the terminal
        or command prompt opens the model.

        First :py:meth:`Model.save` the model to copasi_file
        then open with CopasiUI. Optionally open with a temporary
        filename.

        :param copasi_file:
            `str` or `None`. Same as :py:meth:`model.Save`

        :param as_temp:
            `bool`. Use temp file to open the model and remove
            afterwards
        :return:
            `None`
        """
        if copasi_file == None:
            copasi_file = self.copasi_file
        if as_temp:
            copasi_temp = os.path.join(self.root, os.path.split(self.copasi_file)[1][:-4] + '_1.cps')
        self.save(copasi_file)
        os.system('CopasiUI "{}"'.format(copasi_file))
        if as_temp:
            os.remove(copasi_temp)

    def _model_components(self):
        """
        list of model components that
        are changable
        :return:
        """
        return ['metabolite', 'compartment', 'reaction',
                'local_parameter', 'global_quantity',
                'function']

    def get(self, component, value, by='name'):
        """
        Factory method for getting a model component by a value of a certain type

        :param component:
            `str`. The component i.e. `metabolite` or `local_parameter`

        :param value:
            `str`. Value of the attribute to match by i.e. metabolite called A

        :param by:
            `str`. Which attribute to search by. i.e. name or key or value

        :return:
            Instance of `:py:class:Model.<component>`

        Get reaction called A2B:

            >>> model.get('reaction', 'A2B', by='name')

        Get metabolite called A:

            >>> model.get('metabolite', 'A', by='name')

        Get all reactions which have a fixed simulation_type:

            >>> model.get('global_quantity', 'fixed', by='simulation_type')

        Get all compartments with an initial value of 15
        (concentration or particles depending on quantity_type):

            >>> model.get('compartment', 15, by='initial_value')

        Get metabolites in the nucleus compartment:

            >>> model.get('metabolite', 'nuc', by='compartment')
        """
        if component not in self._model_components():
            raise errors.InputError('{} not in list of components: {}'.format(component, self._model_components()))

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
            match_field='name', change_field='name'):
        """
        Set a model components attribute to a new value

        :param component:
            `str` type of component to change (i.e. metbaolite)

        :param match_value:
            `str`, `int`, `float` depending on value of `match_field`.
            The value to match.

        :param new_value:
            `str`, `int` or `float` depending on value of `match_field`
            new value for component attribute

        :param match_field:
            `str`. The attribute of component to match by.

        :param change_field:
            `str` The attribute of the component matched that you want to change?

        :return:
            :py:class:`Model`

        Set initial concentration of metabolite called 'X' to 50:
            >>> model.set('metabolite', 'X', 50, match_field='name', change_field='concentration')

        Set name of global quantity called 'G' to 'H':
            >>> model.set('global_quantity', 'G', 'H', match_field='name', change_field='name')
        """
        if component not in self._model_components():
            raise errors.InputError('{} not in list of components'.format(component))

        ##get the component of interest
        comp = self.get(component, match_value, by=match_field)

        if isinstance(comp, list):
            raise errors.SomethingWentHorriblyWrongError(
                'model.get has returned a list --> {}'.format(comp)
            )

        if change_field not in list(comp.__dict__.keys()):
            raise errors.InputError('"{}" not valid for component type "{}"'.format(
                change_field, component
            ))

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
                change_field = 'particle_numbers'

        ##remove component of interest from model
        self.remove(component, match_value)

        ## set the attribute
        setattr(comp, change_field, new_value)

        ##add back to model with new attribute
        return self.add_component(component, comp)

    def add_component(self, component_name, component,
                      reaction_expression=None, reaction_rate_law=None):
        """
        add a model component to the model
        :param component_name:
            `str`. i.e. 'reaction', 'function', 'metabolite

        :param component:
            :py:class:`model.<component>`. The component class to add i.e. Metabolite

        :param reaction_expression:
            When adding reaction using string as first arg,
            this argument takes the reaction expression (i.e. A -> B)

        :param reaction_rate_law:
            When adding reaction using string as first argument
            this argument takes the reaction rate law (i.e. k*A)

        :return: :py:class:`Model
        """
        if component_name not in self._model_components():
            raise errors.InputError(
                '"{}" not valid. These are valid: {}'.format(component_name, self._model_components()))

        if component_name == 'metabolite':
            return self.add_metabolite(component)

        elif component_name == 'function':
            return self.add_function(component)

        elif component_name == 'reaction':
            return self.add_reaction(component, reaction_expression, reaction_rate_law)

        elif component_name == 'global_quantity':
            return self.add_global_quantity(component)

        elif component_name == 'compartment':
            return self.add_compartment(component)

    def add(self, component_name, **kwargs):
        """
        add a model component to the model
        :param component_name:
            `str`. i.e. 'reaction', 'function', 'metabolite

        :param component:
            :py:class:`model.<component>`. The component class to add i.e. Metabolite

        :param reaction_expression:
            When adding reaction using string as first arg,
            this argument takes the reaction expression (i.e. A -> B)

        :param reaction_rate_law:
            When adding reaction using string as first argument
            this argument takes the reaction rate law (i.e. k*A)

        :return: :py:class:`Model
        """
        if component_name not in self._model_components():
            raise errors.InputError(
                '"{}" not valid. These are valid: {}'.format(component_name, self._model_components()))

        if component_name == 'metabolite':
            metab = Metabolite(self, **kwargs)
            return self.add_metabolite(metab)

        elif component_name == 'function':
            f = Function(self, **kwargs)
            return self.add_function(f)

        elif component_name == 'reaction':
            react = Reaction(self, **kwargs)
            return self.add_reaction(react)

        elif component_name == 'global_quantity':
            global_q = GlobalQuantity(self, **kwargs)
            return self.add_global_quantity(global_q)

        elif component_name == 'compartment':
            comp = Compartment(self, **kwargs)
            return self.add_compartment(comp)

    def remove(self, component, name):
        """
        General factor method for removing model components

        :param component:
            `str` which component to remove (i.e. metabolite)

        :param name:
            `str` name of component to remove

        :return:
            :py:class:`Model`
        """
        if component in self._model_components() == False:
            raise errors.InputError('{} not in list of components'.format(component))

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
            raise errors.InputError('{} is not an accepted type. Choose from: {}'.format(self._model_components()))

    @property
    def active_parameter_set(self):
        """
        get active parameter set

        **Not really in use**

        :return:
            :py:class:`etree.Element`
        """
        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfModelParameterSets':
                return i.attrib['active_set']

    @active_parameter_set.setter
    def active_parameter_set(self, parameter_set):
        """
        set the active parameter set.

        **not really in use**

        :return:
            :py:class:`Model`
        """
        if parameter_set not in self.active_parameter_set:
            raise errors.InputError('{} not in available parameter sets'.format(parameter_set))

        for i in self.xml.iter():
            if i.tag == '{http://www.copasi.org/static/schema}ListOfModelParameterSets':
                i.attrib['active_set'] = parameter_set
        return self

    @property
    def parameter_sets(self):
        """
        Here for potential future implementation of easy switching between parameter
        sets
        :return:
        """
        return NotImplementedError

    @property
    def parameters(self):
        """
        get all locals, globals and metabs as pandas dataframe

        :return:
            :py:class:`pandas.DataFrame`
        """
        if self.quantity_type == 'concentration':
            metabs = {i.name: i.concentration for i in self.metabolites}
        elif self.quantity_type == 'particle_numbers':
            metabs = {i.name: i.particle_numbers for i in self.metabolites}

        locals = {i.global_name: i.value for i in self.local_parameters}
        globals_q = {i.name: i.initial_value for i in self.global_quantities}
        d = {}
        d.update(metabs)
        d.update(locals)
        d.update(globals_q)
        d = pandas.DataFrame(d, index=[0])
        return d

    def to_sbml(self, sbml_file=None):
        """
        convert model to sbml

        :param sbml_file:
            `str`. Path for SBML. Defaults to same as copasi filename

        :return:
            `str`. Path to smbl file
        """
        if sbml_file is None:
            sbml_file = os.path.join(self.root, self.copasi_file[:-4] + '.sbml')

        os.system('CopasiSE {} -e {}'.format(self.copasi_file, sbml_file))
        return sbml_file

    def insert_parameters(self, **kwargs):
        """
        Wrapper around the InsetParameters class
        :param kwargs:
            Arguments for InsertParameters
        :return:
            :py:class:`Model`
        """
        I = InsertParameters(self, **kwargs)
        if kwargs.get('show_parameters'):
            LOG.info('Parameter set that was inserted: \n\n{}'.format(I.parameters.transpose()))


class ReadModelMixin(Mixin):
    """
    if self.model is str (path to copasi file)
    return the xml. If already a model, do nothing.
    :return: model.Model
    """

    @staticmethod
    def read_model(m):
        if isinstance(m, str):
            ## import here due to namespace conflict. Do not change
            # from model import Model
            return Model(m)
        else:
            ## should be model.Model or etree._Element
            return m


@mixin(ReadModelMixin)
@mixin(ComparisonMethodsMixin)
class Compartment(object):

    def __init__(self, model, name=None, initial_value=None,
                 key=None, simulation_type='fixed'):
        self.model = self.read_model(model)
        self.name = name
        self.initial_value = initial_value

        self.key = key
        self.simulation_type = simulation_type

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

    def initial_volume_reference(self):
        """

        :return:
        """
        return "Vector=Compartments[{}],Reference=InitialVolume".format(self.name)

    def to_xml(self):
        """

        :return:
        """
        if self.key == None:
            self.key = KeyFactory(self.model, type='compartment').generate()

        simulation_types = ['reactions', 'ode', 'fixed', 'assignment']
        if self.simulation_type not in simulation_types:
            raise errors.InputError('{} not in {}'.format(self.simulation_type, simulation_types))

        compartment_element = etree.Element('{http://www.copasi.org/static/schema}Compartment', attrib={'key': self.key,
                                                                                                        'name': self.name,
                                                                                                        'simulationType': self.simulation_type,
                                                                                                        'dimensionality': '3'})
        return compartment_element


@mixin(ReadModelMixin)
@mixin(ComparisonMethodsMixin)
@mixin(ComparisonMethodsMixin)
class Metabolite(object):
    """

    """

    def __init__(self, model, name='new_metabolite', particle_numbers=None,
                 concentration=None, compartment=None, simulation_type=None,
                 key=None):
        """

        :param model:
            :py:class:`Model`.

        :param name:
            `str`. Do not use non-ascii characters

        :param particle_numbers:
            `int` or `float`. Number of initial particles for new metabolite.
            Calculated from concentration if missing.

        :param concentration:
            `int` or `float`. Concentration in model units for new metabolite at t=0.
            Calculated from particle_numbers if missing.

        :param compartment:
            :py:class:`Compartment` or `str`. The compartment the metabolite belongs to.
            If `str`, must be the name of a compartment. If left `None`, defaults to the
            first compartment in the :py:meth:`Model.compartments`

        :param simulation_type:
            `str`. default is 'fixed'. Room for assignments but not implemented yet.

        :param key:
            `str`. Automatically assigned but can be overriden if you like.
        """
        # super(Metabolite, self).__init__(model)
        self.model = self.read_model(model)
        self.name = name
        self.particle_numbers = particle_numbers
        self.concentration = concentration
        self.simulation_type = simulation_type
        self.compartment = compartment
        self.key = key

        ##update all keys to none
        self._do_checks()

    def __str__(self):
        return 'Metabolite(name="{}", key="{}", compartment="{}", concentration="{}", particle_numbers="{}", simulation_type="{}")'.format(
            self.name, self.key, self.compartment.name, self.concentration, self.particle_numbers,
            self.simulation_type)

    def __repr__(self):
        return self.__str__()

    def to_df(self):
        """

        :return:
        """
        dict_of_properties = {
            'name': self.name,
            'particle_numbers': self.particle_numbers,
            'concentration': self.concentration,
            'simulation_type': self.simulation_type,
            'compartment': self.compartment,
            'key': self.key
        }
        df = pandas.DataFrame(dict_of_properties, index=['Value']).transpose()
        df.index.name = 'Property'
        return df

    def _do_checks(self):
        """

        :return:
        """
        if self.compartment == None:
            try:
                self.compartment = self.model.compartments[0]
            except IndexError:
                self.model = self.model.add_component('compartment', 'NewCompartment')
                # self.model.save()#model.refresh()
                self.compartment = self.model.compartments[0]
                LOG.info('No compartments in model. adding default compartment '
                         'called NewCompartment with initial volume == 1')

        if self.compartment != None:
            if isinstance(self.compartment, str):
                self.compartment = self.model.get('compartment', self.compartment, by='name')

                if self.compartment == []:
                    raise errors.InputError('No compartment with name "{}"'.format(self.compartment))
                # assert len(self.compartment) == 1
                # self.compartment = self.compartment[0]
            else:
                if isinstance(self.compartment, Compartment) != True:
                    raise errors.InputError('compartment argument should be of type PyCoTools.tasks.Compartment')

        if ('particle_numbers' not in list(self.__dict__.keys())) and ('concentration' not in list(self.__dict__.keys())):
            raise errors.InputError('Must specify either concentration or particle numbers')

        if self.simulation_type == None:
            self.simulation_type = 'reactions'

        if (self.concentration is None) and (self.particle_numbers is None):
            self.concentration = str(float(1))

        if (self.particle_numbers is None) and (self.concentration is not None):
            self.particle_numbers = self.model.convert_molar_to_particles(
                self.concentration,
                self.model.quantity_unit,
                self.compartment.initial_value
            )

        if (self.concentration is None) and (self.particle_numbers is not None):
            self.concentration = self.model.convert_particles_to_molar(
                self.particle_numbers,
                self.model.quantity_unit,
                self.compartment.initial_value
            )

        if self.key is None:
            self.key = KeyFactory(self.model, type='metabolite').generate()

        if not isinstance(self.particle_numbers, (float, int, str)):
            raise errors.InputError('particle number should be float or int or string of numbers')

        if isinstance(self.particle_numbers, (float, int)):
            self.particle_numbers = str(self.particle_numbers)

    @property
    def initial_reference(self):
        """
        The copasi object reference for
        transient metabolite
        :return:
            `str`
        """
        return 'Vector=Metabolites[{}],Reference=InitialConcentration'.format(self.name)

    @property
    def transient_reference(self):
        """
        The copasi object reference for
        transient metabolite
        :return:
            `str`
        """
        return 'Vector=Metabolites[{}],Reference=Concentration'.format(self.name)

    @property
    def initial_particle_reference(self):
        """
        The copasi object reference for
        initial  metabolite particle numbers
        :return:
            `str`
        """
        return 'Vector=Metabolites[{}],Reference=InitialParticleNumber'.format(self.name)

    @property
    def transient_particle_reference(self):
        """
        The copasi object reference for
        transient metabolite particle numbers
        :return:
            `str`
        """
        return 'Vector=Metabolites[{}],Reference=ParticleNumber'.format(self.name)

    @property
    def reference(self):
        """
        The copasi object reference for
        transient metabolite particle numbers
        :return:
            `str`
        """
        return 'Vector=Metabolites[{}]'.format(self.name)

    def to_substrate(self):
        """
        Create :py:class:`Substrate' from Metabolite
        :return:
            :py:class:`Substrate`
        """
        return Substrate(
            self.model, name=self.name,
            particle_numbers=self.particle_numbers,
            concentration=self.concentration,
            compartment=self.compartment,
            simulation_type=self.simulation_type,
            key=self.key
        )

    def to_product(self):
        """
        Create :py:class:`Product' from Metabolite
        :return:
            :py:class:`Product`
        """
        return Product(
            self.model, name=self.name,
            particle_numbers=self.particle_numbers,
            concentration=self.concentration,
            compartment=self.compartment,
            simulation_type=self.simulation_type,
            key=self.key
        )

    def to_modifier(self):
        """
        Create :py:class:`Modifier' from Metabolite
        :return:
            :py:class:`Modifier`
        """
        return Modifier(
            self.model, name=self.name,
            particle_numbers=self.particle_numbers,
            concentration=self.concentration,
            compartment=self.compartment,
            simulation_type=self.simulation_type,
            key=self.key
        )

    def to_xml(self):
        """
        Product the xml needed to represent a Metabolite
        in the Copasi xml
        :return:
            `str`
        """
        metabolite_element = etree.Element('{http://www.copasi.org/static/schema}Metabolite', attrib={'key': self.key,
                                                                                                      'name': self.name,
                                                                                                      'simulationType': self.simulation_type,
                                                                                                      'compartment': self.compartment.key})

        return metabolite_element

    def get_compartment(self):
        """
        Get compartment which the metabolite belongs to
        :return:
            :py:class:`Compartment`
        """
        return self.compartment


class Substrate(Metabolite):
    """
    Inherits from Metabolite. Takes the same argument as Metabolite.
    """

    def __init__(self, model, name='new_metabolite', particle_numbers=None,
                 concentration=None, compartment=None, simulation_type=None,
                 key=None):
        self.name = name
        self.particle_numbers = particle_numbers
        self.concentration = concentration
        self.compartment = compartment
        self.simulation_type = simulation_type
        self.key = key
        super(Substrate, self).__init__(
            model, name=self.name,
            particle_numbers=self.particle_numbers,
            concentration=self.concentration,
            compartment=self.compartment,
            simulation_type=self.simulation_type,
            key=self.key
        )

    def __str__(self):
        return 'Substrate(name="{}", key="{}", compartment="{}", concentration="{}", particle_numbers="{}", simulation_type="{}")'.format(
            self.name, self.key, self.compartment.name, self.concentration, self.particle_numbers,
            self.simulation_type)

    def __repr__(self):
        return self.__str__()


class Product(Metabolite):
    """
    Inherits from Metabolite. Takes the same argument as Metabolite.
    """

    def __init__(self, model, name='new_metabolite', particle_numbers=None,
                 concentration=None, compartment=None, simulation_type=None,
                 key=None):
        self.name = name
        self.particle_numbers = particle_numbers
        self.concentration = concentration
        self.compartment = compartment
        self.simulation_type = simulation_type
        self.key = key
        super(Product, self).__init__(
            model, name=self.name,
            particle_numbers=self.particle_numbers,
            concentration=self.concentration,
            compartment=self.compartment,
            simulation_type=self.simulation_type,
            key=self.key
        )

    def __str__(self):
        return 'Product(name="{}", key="{}", compartment="{}", concentration="{}", particle_numbers="{}", simulation_type="{}")'.format(
            self.name, self.key, self.compartment.name, self.concentration, self.particle_numbers,
            self.simulation_type)

    def __repr__(self):
        return self.__str__()


class Modifier(Metabolite):
    """
    Inherits from Metabolite. Takes the same argument as Metabolite.
    """

    def __init__(self, model, name='new_metabolite', particle_numbers=None,
                 concentration=None, compartment=None, simulation_type=None,
                 key=None):
        self.name = name
        self.particle_numbers = particle_numbers
        self.concentration = concentration
        self.compartment = compartment
        self.simulation_type = simulation_type
        self.key = key
        super(Modifier, self).__init__(
            model, name=self.name,
            particle_numbers=self.particle_numbers,
            concentration=self.concentration,
            compartment=self.compartment,
            simulation_type=self.simulation_type,
            key=self.key
        )

    def __str__(self):
        return 'Modifier(name="{}", key="{}", compartment="{}", concentration="{}", particle_numbers="{}", simulation_type="{}")'.format(
            self.name, self.key, self.compartment.name, self.concentration, self.particle_numbers,
            self.simulation_type)

    def __repr__(self):
        return self.__str__()


@mixin(ComparisonMethodsMixin)
@mixin(ReadModelMixin)
class GlobalQuantity(object):
    """
    Create a global quantity.

    ##TODO:
        Build support for assignments
    """

    def __init__(self, model, name='global_quantity', initial_value=None,
                 key=None, simulation_type=None):
        """

        :param model:
            :py:class:`Model`

        :param name:
            `str`. Name of GlobalQuantity. Do not use non-ascii characters.

        :param initial_value:
            `int` or `float`. default=1. Starting amount of GlobalQuantity.

        :param key:
            `str`. This is automatically assigned

        :param simulation_type:
            `str`. default=`fixed`. Assignment not yet supported.
        """
        self.model = self.read_model(model)
        self.name = name
        self.initial_value = initial_value
        self.key = key
        self.simulation_type = simulation_type

        self._do_checks()

    def _do_checks(self):
        if self.simulation_type != None:
            if self.simulation_type not in ['fixed', 'assignment']:
                raise errors.InputError(
                    'type should be either fixed or assignment. ODE not supported as Reactions can be used.')

        if self.simulation_type == 'assignment':
            errors.NotImplementedError('Assignments not yet implemented')

        if self.name == None:
            raise errors.InputError('name property cannot be None')

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

    def to_df(self):
        """
        Return pandas.DataFrame with GlobalQuntity Attributes
        :return:
        """
        dict_of_properties = {
            'name': self.name,
            'initial_value': self.initial_value,
            'key': self.key,
            'simulation_type': self.simulation_type,
        }
        df = pandas.DataFrame(dict_of_properties, index=['Value']).transpose()
        df.index.name = 'Property'
        return df

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

    @property
    def reference(self):
        """
        compose the transient reference for the global quantity.
            i.e. not initial concentration
        :return: string
        """
        return "Vector=Values[{}]".format(self.name)

    def to_xml(self):
        """
        Build xml element needed to represent a global quantity in
        copasi xml
        :return:
            :py:class:`etree.Element`
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


@mixin(ReadModelMixin)
@mixin(ComparisonMethodsMixin)
class Reaction(object):
    """
    Build a copasi reaction.

    ##TODO remove parameters, parameters_dict, substrate, products
    and modifiers from the constructor of this class. They are not
    needed.
    """

    def __init__(self, model, name='reaction_1', expression=None,
                 rate_law=None, reversible=False, simulation_type='reactions',
                 parameters=[], parameters_dict={}, substrates=[],
                 products=[], modifiers=[], key=None, parameter_values={}):
        """

        :param model:
            A :py:class:`Model`

        :param name:
            `str`. Name of reaction.

        :param expression:
            `str`. The reaction string, i.e. "A -> B; C". Same syntax as the COPASI GUI

        :param rate_law:
            `str`. The reaction rate law. i.e. "k*A*C". Components of the expression are
            recongized and assigned depending on position in the expression. Therefore
            here, for example `A` will be a substrate but B would be a product and C a modifier.
            All COPASI operators are recognized and all other strings (such as `k` here) become
            reaction parameters.

        :param reversible:
            `bool` default=False

        :param simulation_type:
            `str`. default='reactions`. Assignments not yet supported

        :param parameter_values:
            `dict`. key to value mapping of parameter name to required value.

        :param key:
        """
        self.model = self.read_model(model)
        self.name = name
        self.expression = expression
        self.rate_law = rate_law
        self.reversible = reversible
        self.simulation_type = simulation_type
        self.substrates = substrates
        self.products = products
        self.modifiers = modifiers
        self.parameters = parameters
        self.parameters_dict = parameters_dict
        self.parameter_values = parameter_values
        self.fast = False
        self.key = key

        self._do_checks()
        self.create()

    def __str__(self):
        return 'Reaction(name="{}", expression="{}", rate_law="{}", parameters={}, reversible={}, simulation_type="{}")'.format(
            self.name, self.expression, self.rate_law.expression,
            {i.name: i.value for i in self.parameters},
            self.reversible, self.simulation_type
        )

    def __repr__(self):
        return self.__str__()

    @property
    def reference(self):
        """
        Get reaction reference
        :return:
            `str`
        """
        return "Vector=Reactions[{}]".format(self.name)

    def _do_checks(self):
        """
        :return:
        """
        if not isinstance(self.fast, bool):
            raise errors.InputError('fast argument is boolean')

        if self.simulation_type is not None:
            if self.simulation_type not in ['fixed',
                                            'assignment',
                                            'reactions',
                                            'ode']:
                raise errors.InputError(
                    'type should be either fixed or assignment. ODE not supported as Reactions can be used.')

        if self.key is None:
            self.key = KeyFactory(self.model, type='reaction').generate()

        if self.name is None:
            raise errors.InputError('name property cannot be None')

        if self.simulation_type is None:
            self.simulation_type = 'fixed'

        if self.expression is None:
            raise errors.InputError('expression is a required argument')

        if self.rate_law is None:
            raise errors.InputError('rate_law is a required argument')

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
            None
        """

        trans = Translator(self.model, self.expression)
        self.substrates = trans.substrates
        self.products = trans.products
        self.modifiers = trans.modifiers
        self.reversible = trans.reversible

        reaction_components = [i.name for i in trans.all_components]

        if (self.rate_law is None) or (self.rate_law is []):
            raise errors.InputError('rate_law is {}'.format(self.rate_law))

        if isinstance(self.rate_law, str):
            expression_components = Expression(self.rate_law).to_list()

        ## for handling existing functions
        elif isinstance(self.rate_law, Function):
            if 'mass action' in self.rate_law.name.lower():
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

        parameter_collection = []
        parameter_collection_dct = {}
        for i in range(len(parameter_list)):
            if parameter_list[i] not in [j.name for j in parameter_collection]:

                ## do not re-add a parameter if it already exists
                # LOG.info('adding parameter called --> {}'.format(parameter_list[i]))
                try:
                    p = LocalParameter(self.model,
                                       name=parameter_list[i],
                                       key=local_keys[i],
                                       value=self.parameter_values[parameter_list[i]],
                                       reaction_name=self.name,
                                       global_name='({}).{}'.format(self.name, parameter_list[i]),
                                       )
                except KeyError:
                    p = LocalParameter(self.model,
                                       name=parameter_list[i],
                                       key=local_keys[i],
                                       value=0.1,
                                       reaction_name=self.name,
                                       global_name='({}).{}'.format(self.name, parameter_list[i]),
                                       )

                # LOG.warning('deleted simulation_type from local parameter definition. May cause bugs')
                parameter_collection.append(p)
                parameter_collection_dct[parameter_list[i]] = p
        self.parameters = parameter_collection
        self.parameters_dict = parameter_collection_dct

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
        #     raise errors.SomethingWentHorriblyWrongError('Both substrates and products are empty')

        for i in exp:
            if i in [j.name for j in self.substrates]:
                role_dct[i] = 'substrate'
            elif i in [j.name for j in self.products]:
                role_dct[i] = 'product'
            elif i in [j.name for j in self.modifiers]:
                role_dct[i] = 'modifier'
            else:
                role_dct[i] = 'constant'

        existing = self.model.get('function', self.rate_law, 'expression')
        function = Function(
            self.model,
            name="({}).{}".format(
                self.name,
                self.rate_law),
            expression=self.rate_law,
            roles=role_dct
        )
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
        Create necessary xml Elements required to represent a
        reaction in COPASI
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

        reaction = etree.Element('{http://www.copasi.org/static/schema}Reaction', attrib={'key': self.key,
                                                                                          'name': self.name,
                                                                                          'reversible': self.reversible,
                                                                                          'fast': self.fast})
        list_of_substrates = etree.SubElement(reaction, '{http://www.copasi.org/static/schema}ListOfSubstrates')
        for i in self.substrates:
            etree.SubElement(list_of_substrates, '{http://www.copasi.org/static/schema}Substrate',
                             attrib={'metabolite': i.key,
                                     'stoichiometry': str(i.stoichiometry)})

        list_of_products = etree.SubElement(reaction, '{http://www.copasi.org/static/schema}ListOfProducts')
        for i in self.products:
            etree.SubElement(list_of_products, '{http://www.copasi.org/static/schema}Product',
                             attrib={'metabolite': i.key,
                                     'stoichiometry': str(i.stoichiometry)})

        list_of_modifiers = etree.SubElement(reaction, '{http://www.copasi.org/static/schema}ListOfModifiers')
        for i in self.modifiers:
            etree.SubElement(list_of_modifiers, '{http://www.copasi.org/static/schema}Modifier',
                             attrib={'metabolite': i.key,
                                     'stoichiometry': str(i.stoichiometry)})

        list_of_constants = etree.SubElement(reaction, '{http://www.copasi.org/static/schema}ListOfConstants')

        for i in self.parameters:
            etree.SubElement(list_of_constants, '{http://www.copasi.org/static/schema}Constant', attrib={'key': i.key,
                                                                                                         'name': i.name,
                                                                                                         'value': str(
                                                                                                             i.value)})
        if 'mass_action' in self.rate_law.name.lower().replace(' ', '_'):
            kinetic_law = self.rate_law.to_xml()
        else:
            try:
                comp = self.substrates[0].compartment.reference
            except IndexError:
                comp = self.products[0].compartment.reference

            kinetic_law = etree.SubElement(reaction,
                                           '{http://www.copasi.org/static/schema}KineticLaw',
                                           attrib={'function': self.rate_law.key,
                                                   'unitType': 'Default',
                                                   'scalingCompartment': "{},{}".format(
                                                       self.model.reference,
                                                       comp)})
            call_parameters = etree.SubElement(kinetic_law, '{http://www.copasi.org/static/schema}ListOfCallParameters')
            for i in self.rate_law.list_of_parameter_descriptions:
                call_parameter = etree.SubElement(call_parameters,
                                                  '{http://www.copasi.org/static/schema}CallParameter',
                                                  attrib={'functionParameter': i.key})

                if i.role == 'constant':
                    ##TODO implement global quantities here

                    source_parameter = self.parameters_dict[i.name].key

                elif (i.role == 'substrate') or (i.role == 'product') or (i.role == 'modifier'):
                    source_parameter = self.model.get('metabolite', i.name, by='name').key

                etree.SubElement(call_parameter, '{http://www.copasi.org/static/schema}SourceParameter',
                                 attrib={'reference': source_parameter})

        return reaction


@mixin(ReadModelMixin)
@mixin(ComparisonMethodsMixin)
class Function(object):
    """
    Class to hold copasi function definitions for rate laws
    """

    def __init__(self, model, name='function_1', expression=None,
                 type=None, key=None, reversible=None,
                 list_of_parameter_descriptions=[],
                 roles={}):
        """
        :param model:
            :py:class:`Model`

        :param name:
            `str`

        :param expression:
            `str`. The expression for the function. Like k*A for example

        :param type:
            defaults to `user_defined`.

        :param key:
            `str` Automatically assigned

        :param reversible:
            `bool`.

        :param list_of_parameter_descriptions:
            `list`. ParameterDescription objects. Created from roles
            dict if empty.

        :param roles:
            `dict`. Roles for elements of expression. dict[name] = role
            Used to create list_of_parameter_descriptions automatically
        """
        self.model = self.read_model(model)
        self.name = name
        self.expression = expression
        self.type = type
        self.key = key
        self.reversible = reversible
        self.list_of_parameter_descriptions = list_of_parameter_descriptions
        self.roles = roles

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
        ## If list of parameter descriptions already
        ## contains content keep it.
        if self.list_of_parameter_descriptions != []:
            return self.list_of_parameter_descriptions

        ## else reverse engineer new parameter descriptions
        ## from the info that we have
        else:
            function_parameter_keys = KeyFactory(
                self.model, type='function_parameter'
            ).generate(len(self.roles))

            self.list_of_parameter_descriptions = []
            keys = list(self.roles.keys())
            values = list(self.roles.values())

            ## if our function param keys is singular and string, convert to list
            ## so we can iterate over it (and not the characters in the string by mistake)
            if isinstance(function_parameter_keys, str):
                function_parameter_keys = [function_parameter_keys]

            for i in range(len(self.roles)):
                self.list_of_parameter_descriptions.append(
                    ParameterDescription(self.model,
                                         key=function_parameter_keys[i],
                                         name=keys[i],
                                         role=values[i],
                                         order=i))
            return self.list_of_parameter_descriptions

    def to_xml(self):
        """

        :return:
        """
        if self.reversible == None:
            raise errors.SomethingWentHorriblyWrongError('reversible argument is None')

        if self.key == None:
            raise errors.SomethingWentHorriblyWrongError('key argument is None')

        if self.name == None:
            self.name = self.expression

        if self.name == None:
            raise errors.SomethingWentHorriblyWrongError('name argument is None')

        func = etree.Element('{http://www.copasi.org/static/schema}Function', attrib=OrderedDict({'key': self.key,
                                                                                                  'name': self.name,
                                                                                                  'type': 'UserDefined',
                                                                                                  'reversible': self.reversible}))

        expression = etree.SubElement(func, '{http://www.copasi.org/static/schema}Expression')
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
            etree.SubElement(list_of_p_desc, '{http://www.copasi.org/static/schema}ParameterDescription',
                             attrib={'key': i.key,
                                     'name': i.name,
                                     'order': str(i.order),
                                     'role': i.role})

        return func


@mixin(ReadModelMixin)
@mixin(ComparisonMethodsMixin)
class ParameterDescription(object):
    """
    ParameterDescription objects are part of a function which in turn
    are used as rate laws.
    """

    def __init__(self, model, name='parameter_description',
                 role='substrate', order=0, key=None):
        """
        :param model:
            a :py:class:`Model`

        :param name:
            `str`

        :param role:
            `str`, parameter, substrate, modifier or product

        :param order:
            `int`. Used internally, leave defaults

        :param key:
            `str` assigned automatically.
        """
        self.model = self.read_model(model)
        self.name = name
        self.role = role
        self.order = order
        self.key = key

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

        roles = ['constant', 'modifier', 'substrate',
                 'product', 'volume']
        if self.role not in roles:
            raise errors.InputError('{} is not one of {}'.format(self.role, roles))


@mixin(ReadModelMixin)
@mixin(ComparisonMethodsMixin)
class LocalParameter(object):
    """
    A Parameter within the scope of a reaction
    """

    def __init__(self, model, name='local_parameter', value=None,
                 parameter_type=None, reaction_name=None,
                 global_name=None, key=None, simulation_type='fixed'):
        """
        :param model:
            :py:class:`Model`

        :param name:
            `str`

        :param value:
            `int` or `float`. Value of parameter

        :param parameter_type:
            `

        :param reaction_name:
            `str` The name of a reactions to which the parameter belongs.

        :param global_name:
            `str`. The reaction name in parenthesis followed by parameter
            name. i.e. "(reaction1).k1". This is automatically assigned.

        :param key:
            `str` automatically assigned

        :param simulation_type:
            `str` automatically assigned. Will support assignments in future release.
        """
        self.model = self.read_model(model)
        self.name = name
        self.value = value
        self.parameter_type = parameter_type
        self.simulation_type = simulation_type
        self.reaction_name = reaction_name
        self.global_name = global_name
        self.key = key

        if self.name is None:
            raise errors.InputError('Name is "{}"'.format(self.name))

        if self.key is None:
            self.key = KeyFactory(self.model, type='parameter')
            if self.key is None:
                raise errors.InputError('Key is "{}"'.format(self.key))

    def __str__(self):
        return 'LocalParameter(name="{}", reaction_name="{}", value="{}", simulation_type="{}")'.format(
            self.name, self.reaction_name, self.value, self.simulation_type
        )

    def __repr__(self):
        return self.__str__()

    def to_df(self):
        """

        :return:
        """
        dict_of_properties = {
            'name': self.name,
            'value': self.value,
            'parameter_type': self.parameter_type,
            'simulation_type': self.simulation_type,
            'reaction_name': self.reaction_name,
            'global_name': self.global_name,
            'key': self.key
        }
        df = pandas.DataFrame(dict_of_properties, index=['Value']).transpose()
        df.index.name = 'Property'
        return df

    @property
    def reference(self):
        return "ParameterGroup=Parameters,Parameter={}".format(self.name)

    @property
    def value_reference(self):
        return "ParameterGroup=Parameters,Parameter={},Reference=Value".format(self.name)

    def to_xml(self):
        """
        Create xml to go in the string=kinetic parameters
        section of parameter set
        :return: xml element
        """
        reaction = self.model.get('reaction', self.reaction_name, 'name')
        # self.model.open()
        if reaction == []:
            raise errors.SomethingWentHorriblyWrongError('Reaction called "{}" not in model'.format(
                self.reaction_name
            ))
        # print reaction
        cn = "{},{}".format(self.model.reference, reaction.reference)
        model_parameter_group = etree.Element('ModelParameterGroup',
                                              attrib={
                                                  'cn': cn,
                                                  'type': 'reaction'
                                              })
        # TODO implement assignments for kinetic parameters.
        '''
        This requires the below section of xml be modified to include
        the InitialExpression component. I'm going to get everything 
        else to work first then come back to this. 
        '''
        model_parameters_ref = "{},{},{}".format(
            self.model.reference,
            reaction.reference,
            self.reference
        )
        model_parameters = etree.SubElement(
            model_parameter_group,
            '{http://www.copasi.org/static/schema}ModelParameter',
            attrib={
                'cn': model_parameters_ref,
                'value': str(0.1) if self.value is None else str(self.value),
                'type': 'ReactionParameter',
                'simulationType': 'fixed'
            }
        )
        return model_parameter_group

    def get_reaction(self):
        """
        get the reaction object from which
        parameter comes from
        :return:
            :py:class:`Reaction`
        """
        reaction = self.model.get('reaction', self.reaction_name, 'name')
        if reaction == []:
            raise errors.SomethingWentHorriblyWrongError('Reaction not in model')
        return reaction


@mixin(ReadModelMixin)
class KeyFactory(object):
    """
    Class for generating all keys required by COPASI components
    """

    def __init__(self, model, type='metabolite'):
        """

        :param model:
            :py:class:`Model`
        :param type:
            `str`. The type of needed.

        .. highlight::

            Generate one metabolite key
            >>> KF = KeyFactory(model, type='metabolite')
            >>> KF.generate(n=1)
        """
        self.model = self.read_model(model)
        self.type = type

        # self._do_checks()

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
            raise errors.InputError('{} not a valid type. {}'.format(self.type, type_list))

    def generate(self, n=1):
        """

        :return:
        """
        if self.type == 'metabolite':
            return next(self.create_key(self.model.metabolites))

        elif self.type == 'compartment':
            return next(self.create_key(self.model.compartments))

        elif self.type == 'global_quantity':
            return next(self.create_key(self.model.global_quantities))

        elif self.type == 'reaction':
            key = self.create_reaction_key(n)
            return key

        elif self.type == 'parameter_set':
            return next(self.create_key(self.model.parameter_sets))

        elif self.type == 'parameter':
            return next(self.create_key(self.model.local_parameters))

        elif self.type == 'function':
            return self.create_function_key(n)

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
        word_list = [i[0].upper() + i[1:] for i in word_list]

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

    def create_reaction_key(self, n=1):
        """
        create_key only works for generating a single key at a time.
        When creating ParameterDescriptions, we often need several keys
        generated at a time. This method generates these unique keys.
        :return:
        """
        ## get keys
        existing = [i.key for i in self.model.reactions]

        for i in existing:
            assert '_' in i
        existing = [i.split('_')[1] for i in existing]
        existing = [int(i) for i in existing]

        bool = True
        count = 0
        keys = []
        while count != n:
            random_number = randint(1000, 100000000)
            if random_number not in existing:
                existing.append(random_number)
                keys.append(random_number)
                count += 1
        keys = ['{}_{}'.format('Reaction', i) for i in keys]
        if len(keys) == 1:
            return keys[0]
        else:
            return keys

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
        while count != n:
            random_number = randint(1000, 100000000)
            if random_number not in existing:
                existing.append(random_number)
                keys.append(random_number)
                count += 1
        keys = ['{}_{}'.format('FunctionParameter', i) for i in keys]
        if len(keys) == 1:
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
        while count != n:
            random_number = randint(1000, 100000000)
            if random_number not in existing:
                existing.append(random_number)
                keys.append(random_number)
                count += 1
        keys = ['{}_{}'.format('Parameter', i) for i in keys]
        if (len(keys) == 1) and (isinstance(keys, list)):
            return keys[0]
        else:
            return keys

    def create_function_key(self, n=1):
        """
        create_key only works for generating a single key at a time.
        When creating ParameterDescriptions, we often need several keys
        generated at a time. This method generates these unique keys.
        :return:
        """
        ## get keys
        existing = [i.key for i in self.model.functions]

        existing = [i.split('_')[1] for i in existing]
        existing = [int(i) for i in existing]

        bool = True
        count = 0
        keys = []
        while count != n:
            random_number = randint(1000, 100000000)
            if random_number not in existing:
                existing.append(random_number)
                keys.append(random_number)
                count += 1
        keys = ['{}_{}'.format('Function', i) for i in keys]
        if (len(keys) == 1) and (isinstance(keys, list)):
            return keys[0]
        else:
            return keys


@mixin(ComparisonMethodsMixin)
class Expression(object):
    """
    Convert a expression (i.e. rate law expression) into
    Expression object such that we can split by existing copasi
    operators.

    .. _expression_operators:

    Operators
    =========

    These can be used anywhere and do not need to be enclosed
    by <>

    =============   ===================
    Operator List   Description
    =============   ===================
    +               Addition
    -               Subtraction
    *               Multiplication
    /               Dicision
    %               Modulus
    ^               Power
    =============   ===================

    The following operators can be used but must be enclosed by an
    `<>` in the expression string. See the `copasi documentation <http://copasi.org/Support/User_Manual/Model_Creation/User_Defined_Functions/>`_
    for more details.

    =============   ===================
    Operator List   Description
    =============   ===================
    abs             Absolute value
    floor           floor division
    ceil            Ceiling dividion
    factorial       Factorial
    log             Natural log
    log10           Log base 10
    exp             Expentional
    sin             sine
    cos             Cosine
    tan             Tangent
    sec
    csc
    cot
    tanh
    sech
    csch
    coth
    asin
    acos
    atan
    arcsec
    arccsc
    arcccot
    arcsinh
    arccosh
    arctanh
    arcsech
    arccsch
    arccoth
    uniform         Uniform distribution
    normal          Normal distibution
    le              less than or equal
    lt              less than
    ge              greater than or equal
    gt              greater than
    ne              not equal
    eq              equal
    and             and
    or              or
    xor
    not             not
    if              if statement
    =============   ===================

    """

    def __init__(self, expression):
        self.expression = expression

        ## list of available operators according the copasi website
        self.operator_list = ['+', '-', '*', r'/', '%', '^', '(', ')']
        self.letter_operators = ['abs', 'floor',
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
        for i in ['<{}>'.format(op) for op in self.letter_operators] + self.operator_list:
            if i in self.expression:
                self.expression = self.expression.replace(i, ',')

        ## get list of elements by split
        split = self.expression.split(',')
        split = [i.strip() for i in split]
        split = sorted(list(set([i for i in split if i != ''])))
        return split

    def __str__(self):
        return "Expression({})".format(self.expression)


@mixin(ReadModelMixin)
class Translator(object):
    """
    Translate a copasi style reaction into
    lists of substrates, products and modifiers.
    """

    def __init__(self, model, reaction, reversible=False):
        """

        :param model:
            :py:class:`Model`

        :param reaction:
            :py:class:`Reaction`

        :param reversible:
            `bool`
        """
        self.model = self.read_model(model)
        self.reaction = reaction
        self.reversible = reversible

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
            raise errors.InputError('{} not in {}'.format(component, component_options))

        if type == 'substrate':
            return [i.replace(' ', '').strip() for i in self.substrates.split('+')]

        elif type == 'product':
            return [i.replace(' ', '').strip() for i in self.products.split('+')]

        elif type == 'modifier':
            return [i.replace(' ', '').strip() for i in self.modifiers.split(' ') if i != '']

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
        return list(count.keys())

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

        operators = ['+', '-', '*', '/']
        lst = []
        for comp in component_list:
            if comp in operators:
                continue
            stoic = 1
            ## check for non 1 stoichiometry
            if '*' in comp:
                stoic, comp = comp.split('*')

            ## if metab doesn't exist, create and add it to the model
            # if comp == '':
            #     continue
            metab = self.model.get('metabolite', comp, by='name')
            if metab == []:
                try:
                    metab = Metabolite(self.model, name=comp,
                                       concentration=1,
                                       compartment=self.model.compartments[0],
                                       key=KeyFactory(self.model,
                                                      type='metabolite').generate())
                except IndexError:
                    self.model.add_component('compartment', 'NewCompartment')
                    metab = Metabolite(self.model, name=comp,
                                       concentration=1,
                                       compartment=self.model.compartments[0],
                                       key=KeyFactory(self.model,
                                                      type='metabolite').generate())

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
    """
    Recreates the COPASI MassAction rate law but didn't get used
    in main code.
    """

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
            substrate = ParameterDescription(self.model, key='FunctionParameter_1000', name='substrate', order='1',
                                             role='substrate')
            parameter = ParameterDescription(self.model, key='FunctionParameter_1001', name='k1', order='0',
                                             role='constant')
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
            s = ParameterDescription(self.model, key='FunctionParameter_1003', name='substrate', order='1',
                                     role='substrate')
            k2 = ParameterDescription(self.model, key='FunctionParameter_1004', name='k2', order='2', role='constant')
            p = ParameterDescription(self.model, key='FunctionParameter_1005', name='product', order='3',
                                     role='product')
            self.list_of_parameter_descriptions = [k1, s, k2, p]
        return self

    def to_xml(self):
        """
        write mass action function as xml element
        :return:
        """
        mass_action = etree.Element('{http://www.copasi.org/static/schema}Function',
                                    attrib=OrderedDict({'key': self.key,
                                                        'name': self.name,
                                                        'type': 'MassAction',
                                                        'reversible': self.reversible}))

        expression = etree.SubElement(mass_action, '{http://www.copasi.org/static/schema}Expression')
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
@mixin(ReadModelMixin)
@mixin(ComparisonMethodsMixin)
class ParameterSet(object):
    """
    """

    def __init__(self, model, name='Initial State', initial_time=0,
                 compartments=[], metabolites=[], global_quantities=[],
                 kinetic_parameters=[], key=None):
        self.model = self.read_model(model)
        self.name = name
        self.initial_time = initial_time
        self.compartments = compartments
        self.metabolites = metabolites
        self.global_quantities = global_quantities
        self.kinetic_parameters = kinetic_parameters
        self.key = key

        ##update all keys to none
        self._do_checks()

    def _do_checks(self):
        """

        :return:
        """
        if self.key is None:
            pass
            # self.key = KeyFactory(self.model, type='parameter_set').generate()

    # def read_parameter_set_from_xml(self):
    #     """
    #     :return: the parameter set defined as self.key (defaults to ModelParameterSet1)
    #     """
    #     # print self.model.xml
    #     for i in self.model.xml.iter():
    #         if i.tag == '{http://www.copasi.org/static/schema}ListOfModelParameterSets':
    #             for j in i:
    #                 if j.attrib['key'] == self.key:
    #                     for k in j:
    #                         if k.attrib['cn'] == 'String=Initial Time':
    #                             for l in k:
    #                                 self.initial_time = l.attrib['value']
    #
    #                         elif k.attrib['cn'] == 'String=Initial Compartment Sizes':
    #                             for l in k:
    #                                 compartment_references = [m for m in self.model.compartments if "{},{}".format(
    #                                     self.model.reference, m.reference == l.attrib['cn'])]
    #                                 self.compartments.append(compartments)
    #
    #                         elif k.attrib['cn'] == 'String=Initial Species Values':
    #
    #
    #                         elif k.attrib['cn'] == 'String=Initial Global Quantities':
    #                             pass
    #
    #
    #                         elif k.attrib['cn'] == 'String=Kinetic Parameters':
    #                             pass

    def to_xml(self):

        ## top element
        parameter_set = etree.Element('{http://www.copasi.org/static/schema}ModelParameterSet', attrib={'key': self.key,
                                                                                                        'name': self.name})

        ## time element
        model_parameter_group = etree.SubElement(
            parameter_set, '{http://www.copasi.org/static/schema}ModelParameterGroup',
            attrib={'cn': 'String=Initial Time',
                    'type': 'Group'})

        ## time sub element
        etree.SubElement(model_parameter_group, '{http://www.copasi.org/static/schema}ModelParameter',
                         attrib={'cn': self.model.reference,
                                 'value': str(self.initial_time),
                                 'type': 'Model',
                                 'simulationType': 'time'})

        ##compartment element
        model_parameter_group = etree.SubElement(
            parameter_set, '{http://www.copasi.org/static/schema}ModelParameterGroup',
            attrib={'cn': 'String=Initial Compartment Sizes',
                    'type': 'Group'}
        )

        #
        ##compartment subelement
        for compartment in self.model.compartments:
            etree.SubElement(model_parameter_group, '{http://www.copasi.org/static/schema}ModelParameter',
                             attrib={'cn': '{},{}'.format(self.model.reference, compartment.reference),
                                     'value': str(compartment.initial_value),
                                     'type': 'Compartment',
                                     'simulationType': compartment.simulation_type})

        ##metabolites element
        model_parameter_group = etree.SubElement(
            parameter_set, '{http://www.copasi.org/static/schema}ModelParameterGroup',
            attrib={'cn': 'String=Initial Species Values',
                    'type': 'Group'}
        )

        ##metabolite subelement
        for i in self.model.metabolites:
            etree.SubElement(model_parameter_group,
                             '{http://www.copasi.org/static/schema}ModelParameter',
                             attrib={
                                 'cn': '{},{},{}'.format(
                                     self.model.reference,
                                     i.compartment.reference,
                                     i.reference),
                                 'value': i.particle_numbers,
                                 'type': 'Species',
                                 'simulationType': i.simulation_type})
        #
        ##global quantities element
        model_parameter_group = etree.SubElement(
            parameter_set, '{http://www.copasi.org/static/schema}ModelParameterGroup',
            attrib={'cn': 'String=Initial Global Quantities',
                    'type': 'Group'}
        )

        ##global quantity subelement
        for global_q in self.model.global_quantities:
            etree.SubElement(model_parameter_group, '{http://www.copasi.org/static/schema}ModelParameter',
                             attrib={'cn': '{},{}'.format(
                                 self.model.reference, global_q.reference),
                                 'value': global_q.initial_value,
                                 'type': 'ModelValue',
                                 'simulationType': global_q.simulation_type})

        ##kinetic parameters
        model_parameter_group = etree.SubElement(
            parameter_set, 'ModelParameterGroup',
            attrib={'cn': 'String=Kinetic Parameters',
                    'type': 'Group'}
        )
        print(etree.tostring(parameter_set, pretty_print=True))

        ##kinetic parameters  subelement
        for r in self.model.reactions:
            reaction = etree.SubElement(model_parameter_group,
                                        '{http://www.copasi.org/static/schema}ModelParameterGroup',
                                        attrib={
                                            'cn': "{},{}".format(self.model.reference,
                                                                 r.reference),
                                            'type': 'Reaction',
                                        })
            for k in r.parameters:
                etree.SubElement(model_parameter_group, 'ModelParameter',
                                 attrib={
                                     'cn': '{},{},{}'.format(
                                         self.model.reference,
                                         r.reference,
                                         k.reference),
                                     'value': k.value,
                                     'type': 'ReactionParameter',
                                     'simulationType': k.simulation_type})

        print(etree.tostring(parameter_set, pretty_print=True))


#
#


##TODO reactions, metabs, globs and comp
## all need additional reference without the reference part.
##either string manit or write a new function to produce
##in each class

## implement means ofadding initial expresion
## to each ompontnt


@mixin(ReadModelMixin)
class InsertParameters(object):
    """
    Insert parameters from a file, dictionary or a pandas dataframe into a copasi
    file.
    """

    def __init__(self, model, parameter_dict=None, df=None,
                 parameter_path=None, index=0, quantity_type='concentration',
                 inplace=False):
        """
        :param model:
            :py:class:`Model`

        :param parameter_dict:
            `dict`. dict[ParameterName] = new_value

        :param df:
            :py:class:`Pandas.DataFrame`. Column headings must equate to model components.
            If more than 1 row then `index` agument is required to specify which row you
            want to insert

        :param parameter_path:
            `str` Full path to a directory containing parameter estimation output
            such as output from :py:class:`tasks.MultiParameterEstimation`. `index` argument
            specified which row to insert. Data is automatically ordered in increasing RSS order.

        :param index:
            `int`. index of parameter_path or df to insert. Indexes the rank of best fit. 0 is best.


        :param quantity_type:
            `str`. default='concentration'. Can also be `particle_numbers`

        :param inplace:
            `bool` default=False. Change the model you're working with. If False,
            the model with new parameters are in the `model` attribute. If True,
            the parameters get inserted into the model you used as argument to the
            InsertParameters class.
        """
        self.model = self.read_model(model)
        self.parameter_dict = parameter_dict
        self.df = df
        self.parameter_path = parameter_path
        self.index = index
        self.quantity_type = quantity_type
        self.inplace = inplace
        self._do_checks()

        self.model = self.insert()
        if self.inplace:
            self.model.save()

    # def __str__(self):
    #     return "InsertParameters({})".format(self.to_string())

    def _do_checks(self):
        """
        Verity user input
        :return:
        """
        assert self.quantity_type in ['concentration', 'particle_numbers']
        if self.parameter_dict != None:
            if isinstance(self.parameter_dict, dict) != True:
                raise errors.InputError('Argument to \'parameter_dict\' keyword needs to be of type dict')

            for i in list(self.parameter_dict.keys()):
                if i not in self.model.all_variable_names:
                    raise errors.InputError(
                        'Parameter \'{}\' is not in your model. \n\nThese are in your model:\n{}'.format(
                            i, sorted(self.model.all_variable_names)
                        )
                    )
        if (self.parameter_dict is None) and (self.parameter_path is None) and (self.df is None):
            raise errors.InputError(
                'You need to give at least one of parameter_dict,parameter_path or df keyword arguments')

        assert isinstance(self.index, int)

        # make sure user gives the right number of arguments
        num = 0
        if self.parameter_dict != None:
            num += 1

        if self.df is not None:
            num += 1

        if self.parameter_path != None:
            num += 1

        if num != 1:
            raise errors.InputError(
                'You need to supply exactly one of parameter_dict,parameter_path or df keyord argument. You cannot give two or three.')

    def to_dict(self):
        """
        return parameters as dict
        :return:
        """
        if isinstance(self.parameters, dict):
            return self.parameters

        elif isinstance(self.parameters, pandas.core.frame.DataFrame):
            return self.parameters.to_dict()

    @cached_property
    def parameters(self):
        """
        Get parameters depending on the type of input.
        Converge on a pandas dataframe.
        Columns = parameters, rows = parameter sets

        Use check parameter consistency to see
        whether headers have been pruned or not. If not try pruning them

        """
        if self.parameter_dict != None:
            assert isinstance(self.parameter_dict, dict), 'The parameter_dict argument takes a Python dictionary'
            for i in self.parameter_dict:
                assert i in self.model.all_variable_names, '{} is not a parameter. These are your parameters:{}'.format(
                    i, list(self.GMQ.get_all_model_variables().keys()))
            return pandas.DataFrame(self.parameter_dict, index=[0])

        if self.parameter_path != None:
            P = viz.Parse(self.parameter_path, copasi_file=self.model.copasi_file)
            if isinstance(self.index, int):
                return pandas.DataFrame(P.data.iloc[self.index]).transpose()
            else:
                return P.data.iloc[self.index]

        if self.df is not None:
            df = pandas.DataFrame(self.df.iloc[self.index]).transpose()
        return df

    def insert_locals(self):
        """

        :return:
        """
        # print self.parameters

        locals = [j for i in self.model.reactions for j in i.parameters if j.global_name in list(self.parameters.keys())]
        if locals == []:
            return self.model
        else:
            for loc in locals:
                for element_tags in self.model.xml.iter():
                    if element_tags.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                        for reaction in element_tags:
                            if reaction.attrib['name'] == loc.reaction_name:
                                for reaction_xml in reaction:
                                    if reaction_xml.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                                        for constant_xml in reaction_xml:
                                            if constant_xml.attrib['name'] == loc.name:
                                                constant_xml.attrib['value'] = str(
                                                    float(self.parameters[loc.global_name]))
        return self.model

    def insert_compartments(self):
        """
        insert new parameters into compartment
        :return:
        """
        compartments = [i for i in self.model.compartments if i.name in self.parameters]
        if compartments == []:
            return self.model
        else:

            LOG.critical(
                'Changing a compartment volume has consequences for the rest of the metabolites assigned to that compartment')
            for i in compartments:
                self.model = self.model.set('compartment', i.name, str(self.parameters[i.name][self.index]),
                                            match_field='name', change_field='initial_value')
            return self.model

    def insert_metabolites(self):
        """
        insert new parameters into compartment
        :return:
        """
        metabolites = [i for i in self.model.metabolites if i.name in self.parameters]
        if metabolites == []:
            return self.model
        else:
            for i in metabolites:
                self.model = self.model.set('metabolite',
                                            i.name,
                                            str(self.parameters[i.name][self.index]),
                                            match_field='name', change_field=self.quantity_type)
            return self.model

    def insert_global_quantities(self):
        """
        insert new parameters into compartment
        :return:
        """
        global_quantities = [i for i in self.model.global_quantities if i.name in self.parameters]
        if global_quantities == []:
            return self.model
        else:
            for i in global_quantities:
                if i.simulation_type == 'assignment':
                    LOG.info('Global quantity "{}" skipped because it is set to assignment'.format(i.name))
                    continue

                self.model = self.model.set('global_quantity',
                                            i.name,
                                            str(self.parameters[i.name][self.index]),
                                            match_field='name', change_field='initial_value')
            return self.model

    def insert(self):
        """
        User other methods defined in this class to insert parameters
        into the model
        :return:
        """
        self.model = self.insert_locals()
        self.model = self.insert_compartments()
        self.model = self.insert_global_quantities()
        self.model = self.insert_metabolites()
        return self.model
