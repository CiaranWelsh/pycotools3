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

This module provides a set of base classes that are used in PyCoTools
"""
# import model as m
import pycopi
# import model
import os
import pandas
from lxml import etree
import Errors
import logging
# from model import Model
from contextlib import contextmanager
from copy import deepcopy
# from model import Model

LOG = logging.getLogger(__name__)

class _Base(object):
    """
    Base class for setting class attributes
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.update_properties(self.kwargs)
        # self.__dict__.update((key, value) for key, value in self.kwargs.items() )

    def __str__(self):
        return "_Base({})".format(self.to_string())

    def __repr__(self):
        return self.__str__()

    def to_string(self):
        """
        Produce kwargs as string format for using in __str__ methods
        in subclasses.

        Useage in subclass:

            def __str__(self):
                return 'SubClassName({})'.format(self.as_string)

        :return: str
        """
        prop = deepcopy(self.__dict__)
        del prop['kwargs']
        if 'default_properties' in prop:
            del prop['default_properties']
        str_list = []
        for attr in sorted(prop):
            if isinstance(prop[attr], str)==False:
                str_list.append('{}={}'.format(attr, prop[attr] ))
            else:
                str_list.append('{}=\'{}\''.format(attr, prop[attr]))

        string = ','.join(str_list)
        return string.replace(',', ', ')

    def to_df(self):
        """
        Convert kwargs to 1D df
        :return: pandas.DataFrame
        """
        df = pandas.DataFrame(self.kwargs, index=['Value']).transpose()
        df.index.name = 'Property'
        # df = df.drop('key', index=1)
        return df

    def to_dict(self):
        """
        get kwargs as dictionary
        :return: dict
        """
        return self.kwargs

    def update_properties(self, kwargs):
        """
        method for updating properties from subclasses kwargs

        usage in subclass:
            class New(_base._ModelBase):
                def __init__(self, model, **kwargs):
                    super(New, self).__init__(model, **kwargs)

                    options = {'A':'not_a',
                               'B':'b'}

                    self.update_kwargs(options)
                    print self.A
                    print self.B
        output:
            >>> print PyCoTools.pycopi.New(self.copasi_file, A='a')
                a
                b

        :param kwargs: dict of options for subclass
        :return: void
        """
        for k in kwargs:
            try:
                getattr(self, k)
            except AttributeError:
                setattr(self, k, kwargs[k])

    def update_kwargs(self, new_kwargs):
        """
        Method for updating options
        defined by user with default options
        :param new_kwargs: dict
        :return: void
        """
        return self.kwargs.update(new_kwargs)

    @staticmethod
    def convert_bool_to_numeric(dct):
        """
        CopasiML uses 1's and 0's for True or False in some
        but not all places. When one of these options
        is required by the user and is specified as bool,
        this class converts them into 1's or 0's.

        Use this method in early on in constructor for
        all subclasses where this applies.

        Usage in subclass:
            class New(PyCoTools._base._ModelBase):
                def __init__(self, model, **kwargs):
                    super(New, self).__init__(model, **kwargs)

                    options = {'append': True,
                               'confirm_overwrite': False,
                               'output_event': False,
                               'scheduled': True,
                               'plot': True}

                    options = self.convert_bool_to_numeric(options)
                    self.update_properties(options)


        :param: dct. Python dictionary.  __dict__ or kwargs or options
        :return:
        """
        lst = ['append',
               'confirm_overwrite',
               'output_event',
               'scheduled',
               'automatic_step_size',
               'start_in_steady_state',
               'output_event',
               'start_in_steady_state',
               'integrate_reduced_model',
               'use_random_seed',
               'output_in_subtask',
               'adjust_initial_conditions',
               'update_model',
               'output_in_subtask',
               'adjust_initial_conditions',
               'create_parameter_sets',
               'calculate_statistics',
               'randomize_start_values',
               ]
        for k, v in dct.items():
            if k in lst:
                if v == True:
                    dct[k] = '1'
                elif v == False:
                    dct[k] = '0'
                elif v == '1':
                    pass
                elif v == '0':
                    pass
                else:
                    raise Exception('{} is not True or False'.format(v))
        return dct

    @staticmethod
    def check_integrity(allowed, given):
        """
        Method to raise an error when a wrong
        kwarg is passed to a subclass
        :param: allowed. List of allowed kwargs
        :param: given. List of kwargs given by user or default
        :return: 0
        """
        for key in given:
            if key not in allowed:
                raise Errors.InputError('{} not in {}'.format(key, allowed))


class _ModelBase(_Base):
    def __init__(self, mod, **kwargs):
        """
        A base class which defines some methods that
        will be useful in multiple subclasses.

        Major task is to read the model into python.
        :param mod: either model.Model or str
        :param kwargs:
        """
        super(_ModelBase, self).__init__(**kwargs)
        self.model = mod

        ##import here because of namespace conflict.
        ## Bad practice but functional. Change when you id conflict
        import model
        if isinstance(self.model, (model.Model,
                                   str)) != True:
            raise Errors.InputError('First argument should be either PyCoTools.model.Model object or path (str) pointing to a copasi file. Got {} instead.'.format(type(self.model)))
        self.model = self.read_xml()

    def read_xml(self):
        """
        if self.model is str (path to copasi file)
        return the xml. If already a model, do nothing.
        :return:
        """
        if isinstance(self.model, str):
            from model import Model
            return Model(self.model)
        else:
            ## should be model.Model or etree._Element
            return self.model
