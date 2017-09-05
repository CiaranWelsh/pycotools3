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
# site.addsitedir('C:\Users\Ciaran\Documents\pycotools')
site.addsitedir('/home/b3053674/Documents/pycotools')

import pycotools
from pycotools.Tests import _test_base
import unittest
import os
import pickle



class VizTests(_test_base._BaseTest):
    def setUp(self):
        super(VizTests, self).setUp()
        self.model = pycotools.model.Model(self.copasi_file)


        '''
        instead of generating data on the fly like
        I should do, I've pre-ran the parameter estimations
        and saved the data to pickle under the extra_data_for_tests
        file. Now I can read this pickle and not have to run the 
        parameter estimations each time I run a test. 
        '''
        extra_data_folder = os.path.join(os.path.dirname(__file__), 'extra_data_for_tests')
        multi_data_pickle = os.path.join(extra_data_folder, 'multi_PE_data.pickle')
        ## load the data
        with open(multi_data_pickle) as f:
            self.pe_data_dict = pickle.load(f)

        assert isinstance(self.pe_data_dict, dict)

        ##recreate the results folder
        self.fake_results_folder = os.path.join(os.path.dirname(__file__), 'multi_pe_test_folder')

        if os.path.isdir(self.fake_results_folder) !=True:
            os.mkdir(self.fake_results_folder)

        for i in self.pe_data_dict:
            f = os.path.join(self.fake_results_folder, i)
            self.pe_data_dict[i].to_csv(f)

    def test_viz_parser(self):
        """

        :return:
        """
        print# self.pe_data_dict






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

















