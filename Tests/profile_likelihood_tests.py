# -*-coding: utf-8 -*-
"""

 This file is part of pycotools3.

 pycotools3 is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pycotools3 is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with pycotools3.  If not, see <http://www.gnu.org/licenses/>.


 $Author: Ciaran Welsh

Module that tests the operations of the _Base base test

"""

from pycotools3 import viz, tasks, model
from Tests import _test_base
import unittest
import os
import glob


## todo update profile likelihood test model
class ProfileLikelihoodTests(_test_base._BaseTest):

    def setUp(self):
        super(ProfileLikelihoodTests, self).setUp()
        self.fname = os.path.join(os.path.dirname(__file__), 'timecourse.txt')
        self.data = self.model.simulate(0, 10, 1, report_name=self.fname)

    def test(self):
        """
        Returns:

        """
        with tasks.ParameterEstimation.Context(
                self.model, self.fname, context='pl', parameters='g'
        ) as context:
            context.set('method', 'hooke_jeeves')
            context.set('run_mode', True)
            config = context.get_config()
        pe = tasks.ParameterEstimation(config)
        expected = 11
        actual = viz.Parse(pe)['A2B'].shape[0]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
