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


import pandas


class _Kwargs(object):
    """
    Base class for setting class attributes
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.__dict__.update((key, value) for key, value in self.kwargs.items() )

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
        return df

    def as_dict(self):
        """
        get kwargs as dictionary
        :return: dict
        """
        return self.kwargs
