# -*- coding: utf-8 -*-
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
"""
from pycotools import *
import unittest
import os


class Test(unittest.TestCase):

    def setUp(self):
        self.directory = os.path.join(os.path.dirname(__file__), 'SensitivityTests')
        os.makedirs(self.directory) if not os.path.isdir(self.directory) else None
        self.cps_file = os.path.join(self.directory, 'test_model.cps')

        self.antimony_string = """
            model test_model()
                R1: A => B; kAtoB*A
                R2: B => C; kBtoC*B
                
                kAtoB = 0.1
                kBtoC = 0.1
                A = 1000
                B = 0
                C = 0 
            end
            """

        with model.BuildAntimony(self.cps_file) as loader:
            self.mod = loader.load(antimony_str=self.antimony_string)

        assert isinstance(self.mod, model.Model)

        ##  add reaction using oo interfce to get a local parameter in
        self.mod.add_reaction('R3', 'C -> D', 'k*C')
        self.mod.save()

    def tearDown(self):
        import shutil
        # shutil.rmtree(self.directory)

    def test(self):
        self.mod.open()



if __name__ == '__main__':
    unittest.main()



