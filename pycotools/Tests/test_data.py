# -*-coding: utf-8 -*-


import os
import pandas
import site
site.addsitedir('/home/b3053674/Documents/pycotools')
# site.addsitedir('C:\Users\Ciaran\Documents\pycotools')

import pycotools

class TestData():
    @staticmethod
    def model1():
        """
        Corresponds to test model 1.

        Particle swarm parameter estimations were simulated
        from the model using time course data simulated
        from the model for each species. Data was read into
        a pandas dataframe then pickled and stored here
        :return:
        """

        f = r'/home/b3053674/Documents/pycotools/pycotools/Tests/test_model_0.cps'
        P = pycotools.viz.Parse(r'/home/b3053674/Documents/pycotools/pycotools/Tests/MultipleParameterEstimationResults')
        print P.format_multi_pe_data(f)



T = TestData().model1()
print T

















































































































