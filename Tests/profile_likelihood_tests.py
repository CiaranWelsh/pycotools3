#-*-coding: utf-8 -*-
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
        what about changing the output of get config such that it
        returns an instance of the parametre estimation class
        or any other valid class. i.e. factory.

        context.run()???
        Returns:

        """
        with tasks.ParameterEstimation.Context(
            self.model, self.fname, context='pl', parameters='g'
        ) as context:
            context.set('method', 'hooke_jeeves')
            config = context.get_config()
        print(config)
        tasks.ParameterEstimation(config)
        ## affected models attribute has no effect

    def test_undefine_other_reports(self):
        """

        :return:
        """
        self.MPE.run()
        os.chdir(self.root)
        import time
        time.sleep(1)
        PL = tasks.ProfileLikelihood(self.model, parameter_path=self.MPE.results_directory,
                                                method='hooke_jeeves', iteration_limit=1,
                                                log10=True, run=False, index=[0],
                                                output_in_subtask=False)  # , parameter_path=param)
        # self.MPE.run()
        boolean = True
        query = '//*[@name="Parameter Estimation"]'
        for i in self.model.xml.xpath(query):
            if 'type' in list(i.keys()):
                if i.attrib['type'] == 'parameterFitting':
                    for j in i:
                        if j.tag == '{http://www.copasi.org/static/schema}Problem':
                            for k in j:
                                if k.attrib['name'] == 'Randomize Start Values':
                                    if k.attrib['value'] == str(0):
                                        boolean = False
        self.assertFalse(boolean)


    def test_method(self):
        """
        Test method is correct
        :return:
        """
        self.MPE.run()
        os.chdir(self.root)
        import time
        time.sleep(2)
        PL = pycotools3.tasks.ProfileLikelihood(self.model, parameter_path=self.MPE.results_directory,
                                                method='particle_swarm', iteration_limit=1,
                                                log10=True, run=False, index=[0],
                                                output_in_subtask=False)  # , parameter_path=param)

        boolean = False
        query = '//*[@name="Parameter Estimation"]'
        for i in self.model.xml.xpath(query):
            if 'type' in list(i.keys()):
                if i.attrib['type'] == 'parameterFitting':
                    for j in i:
                        if j.tag == 'Method':
                            if j.attrib['name'] == 'Particle Swarm':
                                boolean = True
        self.assertTrue(boolean)

    def test_parameters(self):
        """

        :return:
        """

        self.MPE.run()
        os.chdir(self.root)
        import time
        time.sleep(2)
        PL = pycotools3.tasks.ProfileLikelihood(self.model, parameter_path=self.MPE.results_directory,
                                                method='hooke_jeeves', iteration_limit=1,
                                                log10=True, run=False, index=[0],
                                                output_in_subtask=False)  # , parameter_path=param)
        PL.model.save()
        boolean = False
        A = self.model.get('metabolite', 'A')
        # k1 = self.model.get('local_parameter', '(B2C).k2', by='global_name')
        A2B = self.model.get('global_quantity', 'A2B')
        self.assertAlmostEqual(PL.parameters[0]['A'].item(), float(A.concentration))
        # self.assertAlmostEqual(PL.parameters[0]['(B2C).k2'].item(), float(k1.value))
        self.assertAlmostEqual(PL.parameters[0]['A2B'].item(), float(A2B.initial_value))

    def test_copy_model(self):
        """

        :return:
        """
        ##TODO global variables and local parameters which point to the same model should only be included once in the copying
        ##todo work out why number of estimated parameter does not match number of models
        self.MPE.run()
        os.chdir(self.root)
        import time
        time.sleep(2)
        # self.model.open()
        PL = pycotools3.tasks.ProfileLikelihood(self.model, parameter_path=self.MPE.results_directory,
                                                method='hooke_jeeves', iteration_limit=1,
                                                log10=True, run=False, index=[0])

        index_dir = os.path.join(PL.results_directory, '0')
        self.assertTrue(os.path.isdir(index_dir))
        model_paths = glob.glob(os.path.join(index_dir, '*.cps'))
        mod = pycotools3.model.Model(model_paths[0])
        num_estimated_params = len(mod.fit_item_order)+1
        num_models = len(model_paths)
        self.assertEqual(num_estimated_params, num_models)

    def test_absolute_experiment_files(self):
        """

        :return:
        """
        self.MPE.run()
        os.chdir(self.root)
        import time
        time.sleep(2)
        PL = pycotools3.tasks.ProfileLikelihood(self.model, parameter_path=self.MPE.results_directory,
                                                method='hooke_jeeves', iteration_limit=1,
                                                log10=True, run=False, index=[0])

        query = '//*[@name="File Name"]'
        for i in PL.model.xml.xpath(query):
            self.assertTrue(os.path.isabs(i.attrib['value']))



    def test_setup_parameter_estimation(self):
        """

        :return:
        """
        self.MPE.run()
        os.chdir(self.root)
        import time
        time.sleep(2)
        # self.model.open()
        PL = pycotools3.tasks.ProfileLikelihood(self.model, parameter_path=self.MPE.results_directory,
                                                method='hooke_jeeves', iteration_limit=1,
                                                log10=True, run=False, index=[0])
        index_dir = os.path.join(PL.results_directory, '0')
        model_paths = glob.glob(os.path.join(index_dir, '*.cps'))
        mods = {i: pycotools3.model.Model(i) for i in model_paths}
        query = "//*[@name='FitItem']" #query="//*[@name='FitItem']"
        len_original = len(self.MPE.model.fit_item_order)
        for model in mods:
            self.assertEqual( len(mods[model].fit_item_order)+1, len_original)

if __name__=='__main__':
    unittest.main()

































































