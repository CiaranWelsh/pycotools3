# -*- coding: utf-8 -*-

'''
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
Author:
    Ciaran Welsh
Date:
    19-08-2017
 '''
import pycotools3
import unittest
from Tests import _test_base


class DeterministicTimeCourseTests(_test_base._BaseTest):
    def setUp(self):
        super(DeterministicTimeCourseTests, self).setUp()
        self.TC = pycotools3.tasks.TimeCourse(self.model, end=1000,
                                              step_size=100, intervals=10,
                                              max_internal_steps=50000,
                                              report_name='test_time_course.csv')
        self.timecourse = self.TC.model  # self.TC.set_timecourse()
        self.timecourse.save()
        self.new_model = pycotools3.tasks.CopasiMLParser(self.copasi_file).copasiML
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'
        self.list_of_reports = '{http://www.copasi.org/static/schema}ListOfReports'

    def test_report_definition(self):
        for i in self.new_model.find(self.list_of_reports):
            if i.attrib['name'] == 'Time-Course':
                self.assertTrue(i.attrib['name'] == 'Time-Course')

    def test_report_definition2(self):
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                for j in i:
                    if 'target' in list(j.attrib.keys()):
                        self.assertEqual(j.attrib['target'], self.TC.report_name)

    def test_deterministic_options1(self):
        """
        """
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                self.assertTrue(i[2].attrib['name'] == 'Deterministic (LSODA)')

    def test_deterministic_options2(self):
        """
        """
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                for j in list(i[1]):
                    if j.attrib['name'] == 'Relative Tolerance':
                        self.assertTrue(j.attrib['value'] == str(self.TC.relative_tolerance))

    def test_deterministic_options3(self):
        """
        """
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                for j in list(i[1]):
                    if j.attrib['name'] == 'Max Internal Steps':
                        self.assertTrue(j.attrib['value'] == str(self.TC.max_internal_steps))

    def test_deterministic_write_data(self):
        """
        Check that the data containing data is actually produced
        :return:
        """
        self.assertTrue(os.path.isfile(self.TC.report_name))

    def test_deterministic_read_output(self):
        """
        Ensure that pandas can read the output from TimeCourse
        and that it looks like what we expect
        :return:
        """
        df = pandas.read_csv(self.TC.report_name, sep='\t', index_col=0)
        self.assertEqual(df.shape, (11, 6))

    def test_specific_variables(self):
        """
        Test being selective about which output user wants
        :return:
        """
        TC = pycotools3.tasks.TimeCourse(
            self.model, intervals=10, step_size=100, end=1000,
            metabolites=['A', 'B'], global_quantities=['B2C']
        )
        df = pandas.read_csv(TC.report_name, sep='\t', index_col=0)
        self.assertEqual(df.shape[1], 3)

    def test_parser_in_viz(self):
        """
        :return:
        """
        p = pycotools3.viz.Parse(self.TC)
        df = p.from_timecourse()
        self.assertTrue(isinstance(df, pandas.core.frame.DataFrame))

    def test_parser_in_viz2(self):
        """
        :return:
        """
        p = pycotools3.viz.Parse(self.TC)
        df = p.from_timecourse()
        boolean = True
        ## set boolean to false if square brackets still in timecourse
        for i in list(df.columns):
            if '[' in i:
                boolean = False
        self.assertTrue(boolean)

    def test_parser_in_viz3(self):
        """
        :return:
        """
        pycotools3.viz.PlotTimeCourse(self.TC, y='metabolites')

    def test_for_docs(self):
        """
        :return:
        """
        print(self.model.simulate(0, 100, 0.1))




class GibsonBruckTimeCourseTests(_test_base._BaseTest):
    def setUp(self):
        super(GibsonBruckTimeCourseTests, self).setUp()
        self.TC = pycotools3.tasks.TimeCourse(self.model, end=1000,
                                              step_size=100, intervals=10,
                                              max_internal_steps=50000,
                                              method='gibson_bruck')
        self.timecourse = self.TC.model  # self.TC.set_timecourse()
        self.timecourse.save()
        self.new_model = pycotools3.tasks.CopasiMLParser(self.copasi_file).xml
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'
        self.list_of_reports = '{http://www.copasi.org/static/schema}ListOfReports'

        # TODO test stochastic algorithms

        def test_report_definition(self):
            for i in self.new_model.find(self.list_of_reports):
                if i.attrib['name'] == 'Time-Course':
                    self.assertTrue(i.attrib['name'] == 'Time-Course')

        def test_gibson_bruck1(self):
            """
            """
            for i in self.new_model.find(self.list_of_tasks):
                if i.attrib['name'] == 'Time-Course':
                    self.assertTrue(i[2].attrib['name'] == 'Stochastic (Gibson + Bruck)')

        def test_gibson_bruck2(self):
            """
            """
            for i in self.new_model.find(self.list_of_tasks):
                if i.attrib['name'] == 'Time-Course':
                    for j in list(i[1]):
                        if j.attrib['name'] == 'Max Internal Steps':
                            self.assertTrue(j.attrib['value'] == str(self.TC.max_internal_steps))

        def test_gibson_bruck3(self):
            """
            """
            for i in self.new_model.find(self.list_of_tasks):
                if i.attrib['name'] == 'Time-Course':
                    for j in list(i[1]):
                        if j.attrib['name'] == 'Subtype':
                            self.assertTrue(j.attrib['value'] == str(self.TC.subtype))

        def test_gibson_bruck5(self):
            """
            Check that the data containing data is actually produced
            :return:
            """
            self.assertTrue(os.path.isfile(self.TC.report_name))

        def test_gibson_bruck_read_output(self):
            """
            Ensure that pandas can read the output from TimeCourse
            and that it looks like what we expect
            :return:
            """
            df = pandas.read_csv(self.TC.report_name, sep='\t', index_col=0)
            self.assertEqual(df.shape, (11, 6))


if __name__ == '__main__':
    unittest.main()  # -*- coding: utf-8 -*-

'''
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
Author:
    Ciaran Welsh
Date:
    19-08-2017
 '''
import site

site.addsitedir('/home/b3053674/Documents/pycotools3')
# site.addsitedir('C:\Users\Ciaran\Documents\pycotools3')

import pycotools3
import unittest
import os
import pandas
from Tests import _test_base


class DeterministicTimeCourseTests(_test_base._BaseTest):
    def setUp(self):
        super(DeterministicTimeCourseTests, self).setUp()
        self.TC = pycotools3.tasks.TimeCourse(self.model, end=1000,
                                              step_size=100, intervals=10,
                                              max_internal_steps=50000,
                                              report_name='test_time_course.csv')
        self.timecourse = self.TC.model  # self.TC.set_timecourse()
        self.timecourse.save()
        self.new_model = pycotools3.tasks.CopasiMLParser(self.copasi_file).copasiML
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'
        self.list_of_reports = '{http://www.copasi.org/static/schema}ListOfReports'

    def test_report_definition(self):
        for i in self.new_model.find(self.list_of_reports):
            if i.attrib['name'] == 'Time-Course':
                self.assertTrue(i.attrib['name'] == 'Time-Course')

    def test_report_definition2(self):
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                for j in i:
                    if 'target' in list(j.attrib.keys()):
                        self.assertEqual(j.attrib['target'], self.TC.report_name)

    def test_deterministic_options1(self):
        """
        """
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                self.assertTrue(i[2].attrib['name'] == 'Deterministic (LSODA)')

    def test_deterministic_options2(self):
        """
        """
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                for j in list(i[1]):
                    if j.attrib['name'] == 'Relative Tolerance':
                        self.assertTrue(j.attrib['value'] == str(self.TC.relative_tolerance))

    def test_deterministic_options3(self):
        """
        """
        for i in self.new_model.find(self.list_of_tasks):
            if i.attrib['name'] == 'Time-Course':
                for j in list(i[1]):
                    if j.attrib['name'] == 'Max Internal Steps':
                        self.assertTrue(j.attrib['value'] == str(self.TC.max_internal_steps))

    def test_deterministic_write_data(self):
        """
        Check that the data containing data is actually produced
        :return:
        """
        self.assertTrue(os.path.isfile(self.TC.report_name))

    def test_deterministic_read_output(self):
        """
        Ensure that pandas can read the output from TimeCourse
        and that it looks like what we expect
        :return:
        """
        df = pandas.read_csv(self.TC.report_name, sep='\t', index_col=0)
        self.assertEqual(df.shape, (11, 9))

    def test_parser_in_viz(self):
        """
        :return:
        """
        p = pycotools3.viz.Parse(self.TC)
        df = p.parse()
        self.assertTrue(isinstance(df, pandas.core.frame.DataFrame))

    def test_parser_in_viz2(self):
        """
        :return:
        """
        p = pycotools3.viz.Parse(self.TC)
        df = p.parse()
        boolean = True
        ## set boolean to false if square brackets still in timecourse
        for i in list(df.columns):
            if '[' in i:
                boolean = False
        self.assertTrue(boolean)

    def test_for_docs(self):
        """
        :return:
        """
        model_string = """
        model model1()
    
            R1:   => A ; k1*S;
            R2: A =>   ; k2*A;
            R3:   => B ; k3*A;
            R4: B =>   ; k4*B*C; //feedback term
            R5:   => C ; k5*B;
            R6: C =>   ; k6*C;
    
            S = 1;
            k1 = 0.0001;
            k2 = 0.0001;
            k3 = 0.0001;
            k4 = 0.0001;
            k5 = 0.0001;
            k6 = 0.0001;
            
            A = 0;
            B = 0;
            C = 0;
            APlusB := A + B;

        end
        """
        copasi_file = os.path.join(os.path.dirname(__file__), 'copasi_file.cps')
        mod = pycotools3.model.loada(model_string, copasi_file)
        df = mod.simulate(0, 10, 1, variables='m')
        import matplotlib.pyplot as plt
        import seaborn as sns
        sns.set_context('talk')

        variables = ['']
        print(df.plot())
        plt.show()

class GibsonBruckTimeCourseTests(_test_base._BaseTest):
    def setUp(self):
        super(GibsonBruckTimeCourseTests, self).setUp()
        self.TC = pycotools3.tasks.TimeCourse(self.model, end=1000,
                                              step_size=100, intervals=10,
                                              max_internal_steps=50000,
                                              method='gibson_bruck')
        self.timecourse = self.TC.model  # self.TC.set_timecourse()
        self.timecourse.save()
        self.new_model = pycotools3.tasks.CopasiMLParser(self.copasi_file).xml
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'
        self.list_of_reports = '{http://www.copasi.org/static/schema}ListOfReports'

        # TODO test stochastic algorithms

        def test_report_definition(self):
            for i in self.new_model.find(self.list_of_reports):
                if i.attrib['name'] == 'Time-Course':
                    self.assertTrue(i.attrib['name'] == 'Time-Course')

        def test_gibson_bruck1(self):
            """
            """
            for i in self.new_model.find(self.list_of_tasks):
                if i.attrib['name'] == 'Time-Course':
                    self.assertTrue(i[2].attrib['name'] == 'Stochastic (Gibson + Bruck)')

        def test_gibson_bruck2(self):
            """
            """
            for i in self.new_model.find(self.list_of_tasks):
                if i.attrib['name'] == 'Time-Course':
                    for j in list(i[1]):
                        if j.attrib['name'] == 'Max Internal Steps':
                            self.assertTrue(j.attrib['value'] == str(self.TC.max_internal_steps))

        def test_gibson_bruck3(self):
            """
            """
            for i in self.new_model.find(self.list_of_tasks):
                if i.attrib['name'] == 'Time-Course':
                    for j in list(i[1]):
                        if j.attrib['name'] == 'Subtype':
                            self.assertTrue(j.attrib['value'] == str(self.TC.subtype))

        def test_gibson_bruck5(self):
            """
            Check that the data containing data is actually produced
            :return:
            """
            self.assertTrue(os.path.isfile(self.TC.report_name))

        def test_gibson_bruck_read_output(self):
            """
            Ensure that pandas can read the output from TimeCourse
            and that it looks like what we expect
            :return:
            """
            df = pandas.read_csv(self.TC.report_name, sep='\t', index_col=0)
            self.assertEqual(df.shape, (11, 6))


if __name__ == '__main__':
    unittest.main()
