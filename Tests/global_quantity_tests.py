#-*-coding: utf-8 -*-
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


 $Author: Ciaran Welsh


"""

import pycotools
from Tests import _test_base
import unittest


class TestGlobalQuantities(_test_base._BaseTest):
    def setUp(self):
        super(TestGlobalQuantities, self).setUp()

    def test_string_method(self):
        ## TODO update test for string method
        pass
        # A = pycotools.model.GlobalQuantity(name='A', type='fixed', value=5)
        # self.assertEqual("GlobalQuantity(name='A', type='fixed', value=5)",
        #                  A.__str__())

    def test_fixed_type(self):
        A = pycotools.model.GlobalQuantity(self.model, name='A', simulation_type='fixed', initial_value=5)
        self.assertTrue(A.simulation_type=='fixed')

    def test_fixed_type2(self):
        A = pycotools.model.GlobalQuantity(self.model, name='A', simulation_type='fixed', initial_value=5)
        self.assertTrue(isinstance(A.initial_value, (int, float)) )

    def test_reference_transient(self):
        A = pycotools.model.GlobalQuantity(self.model, name='A', simulation_type='fixed', initial_value=5)
        self.assertTrue(A.transient_reference, 'Vector=Values[A],Reference=Value')

    def test_reference_initial(self):
        A = pycotools.model.GlobalQuantity(self.model, name='A', simulation_type='fixed', initial_value=5)
        self.assertTrue(A.initial_reference, 'Vector=Values[A],Reference=InitialValue')


if __name__=='__main__':
    unittest.main()







