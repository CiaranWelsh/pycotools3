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
import pandas
import pycotools
from pycotools.Tests import _test_base
import unittest
import os
import pickle
import test_data
import numpy
import shutil
import glob



class ProfileLikelihoodTests(_test_base._BaseTest):
    def setUp(self):
        super(ProfileLikelihoodTests, self).setUp()
        self.root = self.model.root
        self.TC1 = pycotools.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        pycotools.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        ## add some noise
        data1 = pycotools.misc.add_noise(self.TC1.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')

        self.MPE = pycotools.tasks.MultiParameterEstimation(
            self.model,
            self.TC1.report_name,
            copy_number=2,
            pe_number=8,
            method='genetic_algorithm',
            population_size=10,
            number_of_generations=10,
            results_directory='test_mpe')
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

        self.MPE.write_config_file()
        self.MPE.setup()
        os.chdir(self.root)
        # self.MPE.run()

    def test_data_files_are_absolute(self):
        """

        :return:
        """
        pass

    def test(self):
        df = pycotools.viz.Parse(self.MPE).data
        mod = pycotools.model.Model(self.model.copasi_file[:-4]+'_1.cps')
        pl = pycotools.tasks.ProfileLikelihood(
            mod, df=df, index=[5], run='parallel',
            processes=4,
        )







        # f=r'/home/b3053674/Documents/pycotools/pycotools/Tests/ProfileLikelihoods/0/A2B.cps'
        # f2=r'/home/b3053674/Documents/pycotools/pycotools/Tests/ProfileLikelihoods/0/B2C.cps'
        # dire = r'/home/b3053674/Documents/pycotools/pycotools/Tests/ProfileLikelihoods/0'
        # import glob
        # files = glob.glob(dire+'/*.cps')
        # models = [pycotools.model.Model(i) for i in files]
        # R = pycotools.tasks.RunParallel(models, processes=2)













        # print R.get_result()
        # import Queue
        # q = Queue.Queue(maxsize=3)
        # print R.run_parallel(q)

        # pl.setup_scan()
        # print pl.index_dct






if __name__=='__main__':
    unittest.main()

































































