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

import pycopi
import pandas
from lxml import etree
class _Base(object):
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
        df = pandas.DataFrame(self.kwargs, index=[self.kwargs['key']]).transpose()
        df.index.name = 'Property'
        df = df.drop('key', index=1)
        return df

    def as_dict(self):
        """
        get kwargs as dictionary
        :return: dict
        """
        return self.kwargs



class _ModelBase(_Base):
    def __init__(self, model, **kwargs):
        super(_ModelBase, self).__init__(**kwargs)
        assert isinstance(model, (str, etree._Element))
        self.model = model
        self.model = self.read_model()

    def read_model(self):
        if isinstance(self.model, etree._Element):
            return self.model
        elif isinstance(self.model, str):
            return pycopi.CopasiMLParser(self.model).copasiML
        else:
            raise Errors.InputError('Model shold be either etree._Element or string to copasi file')


#
#
# class _ModelBase2(_Base):
#     def __init__(self, model, **kwargs):
#         super(_ModelBase2, self).__init__()
#         self.kwargs = kwargs
#         self.model = model




# if __name__ == '__main__':
#     MB2 = _ModelBase2('string')
#     print MB2.test()

