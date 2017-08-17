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
import pandas
from lxml import etree
import Errors
# from model import Model


class _Base(object):
    """
    Base class for setting class attributes
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.__dict__.update((key, value) for key, value in self.kwargs.items() )

    def __str__(self):
        return "_Base({})".format(self.as_string())

    def __repr__(self):
        return self.__str__()

    def as_string(self):
        """
        Produce kwargs as string format for using in __str__ methods
        in subclasses.

        Useage in subclass:

            def __str__(self):
                return 'SubClassName({})'.format(self.as_string)

        :return: str
        """
        str_list = []
        for attr in sorted(self.kwargs):
            if isinstance(self.kwargs[attr], str)==False:
                str_list.append('{}={}'.format(attr, self.kwargs[attr] ))
            else:
                str_list.append('{}=\'{}\''.format(attr, self.kwargs[attr]))

        string = ','.join(str_list)
        return string.replace(',', ', ')

    def as_df(self):
        """
        Convert kwargs to 1D df
        :return: pandas.DataFrame
        """
        df = pandas.DataFrame(self.kwargs, index=['Value']).transpose()
        df.index.name = 'Property'
        # df = df.drop('key', index=1)
        return df

    def as_dict(self):
        """
        get kwargs as dictionary
        :return: dict
        """
        return self.kwargs

    def update_properties(self, kwargs):
        """
        method for updating kwargs from subclasses

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
                getattr(self,k)
            except AttributeError:
                setattr(self, k, kwargs[k])

class _ModelBase(_Base):
    def __init__(self, mod, **kwargs):
        super(_ModelBase, self).__init__(**kwargs)
        self.model = mod
        self.model = self.read_model()

    def read_model(self):
        if isinstance(self.model, str):
            return pycopi.CopasiMLParser(self.model).copasiML
        else:
            ## should be model.Model or etree._Element
            return self.model

    @staticmethod
    def save(copasi_filename, copasiML):
        """
        Save copasiML to copasi_filename. Static.
        :param copasi_filename:
        :param copasiML:
        :return:
        """
        # first convert the copasiML to a root element tree
        root = etree.ElementTree(copasiML)
        root.write(copasi_filename)
        LOG.debug('model written to {}'.format(copasi_filename))
