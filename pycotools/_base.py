# -*-coding: utf-8 -*-
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


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
 
Miscellaneous bunch of useful classes and functions
"""

import tasks
import os
import pandas
from lxml import etree
import errors
import logging
from contextlib import contextmanager
from copy import deepcopy
from mixin import Mixin, mixin
LOG = logging.getLogger(__name__)

class _Base(object):
    """
    Base class for setting class attributes
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        # self.update_properties(self.kwargs)
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











