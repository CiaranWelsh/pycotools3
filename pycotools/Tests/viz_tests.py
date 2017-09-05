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

Module that tests the operations of the _Base base test

"""

import site
site.addsitedir('C:\Users\Ciaran\Documents\pycotools')
site.addsitedir('/home/b3053674/Documents/pycotools')
import pandas
import pycotools
from pycotools.Tests import _test_base
import unittest
import os
import pickle
import test_data



class VizTests(_test_base._BaseTest):
    def setUp(self):
        super(VizTests, self).setUp()
        self.model = pycotools.model.Model(self.copasi_file)


        '''
        instead of generating data on the fly like
        I should do (for good testing practivce), I've pre-ran the parameter estimations
        and saved the data to pickle under the extra_data_for_tests
        file. Now I can read this pickle and not have to run the 
        parameter estimations each time I run a test. I've also 
        parsed the data into a pandas dataframe using viz.parse for ease
        '''

        self.data = pandas.read_pickle(
            pycotools.Tests.test_data.Paths().pe_results_pickle)

        assert isinstance(self.data, pandas.core.frame.DataFrame)


    def test_pycotools_dataframe(self):
        """

        :return:
        """
        df = pandas.DataFrame([10, 100, 1000])
        df = pycotools.viz.DataFrame(df, islog10=False)
        self.assertFalse(df.islog10)

    def test_pycotools_dataframe2(self):
        """

        :return:
        """
<<<<<<< HEAD
        df = pandas.DataFrame([10, 100, 1000])
        df = pycotools.viz.DataFrame(df, islog10=False)
        l = [1, 2, 3]
=======
        df = pandas.DataFrame([1, 10, 100])
        df = pycotools.viz.DataFrame(df, islog10=False)
        l = [0, 1, 2]
>>>>>>> 46ee243ed1b7b203c9113f9e6195fd3d292b613f
        self.assertListEqual(
            list(df.to_log10()[0]),l
        )

    def test_pycotools_dataframe3(self):
        """

        :return:
        """
<<<<<<< HEAD
        df = pandas.DataFrame([1,2, 3])
        df = pycotools.viz.DataFrame(df, islog10=True)
        l = [1, 2, 3]
        self.assertListEqual(
            list(df.to_log10()[0]),l
        )
=======
        df = pandas.DataFrame([1, 10, 100])
        df = pycotools.viz.DataFrame(df, islog10=False)
        df = df.to_log10()
        self.assertTrue(df.islog10)

    def test_pycotools_dataframe3(self):
        """

        :return:
        """
        df = pandas.DataFrame([1, 2, 3])
        df = pycotools.viz.DataFrame(df, islog10=True)
        df = df.to_linear()
        self.assertFalse(df.islog10)
>>>>>>> 46ee243ed1b7b203c9113f9e6195fd3d292b613f

    # def test_boxplot(self):
    #     """
    #
    #     :return:
    #     """
    #     df = pandas.DataFrame([01,2,3])
    #     print pycotools.viz.DataFrame(df, islog10=False)

        # pycotools.viz.Boxplot(self.data, savefig=True,
        #                       results_directory=os.path.join(os.path.dirname(
        #                           self.model.copasi_file), 'Boxplots'
        #                         )
        #                       )

        # pycotools.viz.Boxplot(self.data, savefig=True)






        # import time
        # time.sleep(5)
        # x=self.MPE.copy_number*self.MPE.pe_number
        # self.MPE.run()
        # df_dct = {}
        # for f in os.listdir(self.MPE.results_directory):
        #     f = os.path.join(self.MPE.results_directory, f)
        #     df_dct[f] = pandas.read_csv(f, sep='\t', skiprows=1, header=None)
        # df = pandas.concat(df_dct)
        # assert df.shape[0] == x
        # P = pycotools.viz.Parse(self.MPE)
        # print P.parse_multi_parameter_estimation()


            # def test_run_(self):
    #     # pass
    #     self.MPE.write_config_file()
    #     self.MPE.setup()
    #     self.MPE.run()

    # def test(self):
        ##format the data first
        # self.MPE.format_results()
        # print viz.ParsePEData(self.MPE.result_directory)
        """
        try incorporating the format data stuff in the vis class for mpe
        """


if __name__ == '__main__':
    unittest.main()

















