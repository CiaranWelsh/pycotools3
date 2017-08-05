#-*-coding: utf-8 -*-
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

Module that tests the operations of the _Kwargs base test

"""

import site
site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
import os, glob
import pandas
import unittest




class TestKwargs(unittest.TestCase):
    def setUp(self):
        self.kwargs = PyCoTools._base._Kwargs(A='a', B='b')

    def test_num_kwargs(self):
        ## three kwargs defined. A and B in setUp
        ## and the kwargs dict
        self.assertEqual(len(self.kwargs.__dict__), 3)

    def test_set_random_attribute(self):
        self.assertEqual(self.kwargs.A, 'a')

    def test_set_random_attribute2(self):
        self.assertEqual(self.kwargs.B, 'b')

    def test_name(self):
        """
        Test that assignments work in a subclass
        :return:
        """
        comp = PyCoTools.pycopi.Compartment(name='A', size=5)
        self.assertTrue(comp.name=='A')
        # self.assertRaises(PyCoTools.pycopi.Compartment(not_a_key='raise exception'), PyCoTools.Errors.InputError)

    def test_setattr(self):
        self.kwargs.A = 4
        self.assertEqual(self.kwargs.A, 4)

    def test_str(self):
        kwarg_string = "A='a', B='b'"
        self.assertEqual(kwarg_string,self.kwargs._as_string() )

    def test_as_df_index(self):
        index = ['A','B']
        self.assertListEqual(list(self.kwargs.as_df().index ), index)

    def test_as_df_values(self):
        index = ['A','B']
        self.assertListEqual(list(self.kwargs.as_df()['Value'] ), ['a','b'])

    def test_as_dict_values(self):
        keys = ['A', 'B']
        self.assertListEqual(keys, self.kwargs.as_dict().keys())

    def test_as_dict_values(self):
        keys = ['a', 'b']
        self.assertListEqual(keys, self.kwargs.as_dict().values())


if __name__ == '__main__':
    unittest.main()















