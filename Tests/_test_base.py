#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:43:23 2017

@author: b3053674

This file provides a set of base classes for pycotools3.Tests only.
It is not used in pycotools3 itself.


"""
import pycotools3
import unittest
import glob
import os
import shutil


class _BaseTest(unittest.TestCase):
    """
    class for all tests to inherit from. 
        -> Take string model from TestModels and write to file
        -> Initiate model
    """

    def setUp(self, test_model='test_model1'):
        self.copasi_file = os.path.join(os.getcwd(), 'test_model.cps')

        self.ant = """// Created by libAntimony v2.9.4
                        model *New_Model()
                        
                          // Compartments and Species:
                          compartment nuc, cyt;
                          species A in nuc, B in nuc, C in nuc;
                        
                          // Assignment Rules:
                          ThisIsAssignment := A2B + B2C;
                        
                          // Reactions:
                          A2B_0: A => B; nuc*A2B*A;
                          B2C_0: B -> C; nuc*(B2C*B - B2C_0_k2*C);
                          C2A: C => A; nuc*C2A_k1*C;
                          ADeg: A => ; nuc*ADeg_k1*A;
                        
                          // Species initializations:
                          A = 0.999999999999998;
                          B = 0.999999999999998;
                          C = 0.999999999999998;
                        
                          // Compartment initializations:
                          nuc = 1;
                          cyt = 3;
                        
                          // Variable initializations:
                          A2B = 4;
                          B2C = 9;
                          B2C_0_k2 = 0.1;
                          C2A_k1 = 0.1;
                          ADeg_k1 = 0.1;
                        
                          // Other declarations:
                          var ThisIsAssignment;
                          const nuc, cyt, A2B, B2C;
                        
                          // Unit definitions:
                          unit volume = 1e-3 litre;
                          unit substance = 1e-3 mole;
                        
                          // Display Names:
                          A2B_0 is "A2B";
                          B2C_0 is "B2C";
                        end"""

        with pycotools3.model.BuildAntimony(self.copasi_file) as loader:
            self.model = loader.load(self.ant)

    def tearDown(self):
        tear_down = True
        delete_dirs = True

        if tear_down:
            dire = os.path.dirname(self.copasi_file)
            subdirs = ['Boxplots', 'TimeCourseGraphs',
                       'ParameterEstimationPlots', 'test_mpe',
                       'EnsembleTimeCourse', 'Histograms',
                       'LinearRegression', 'MultipleParameterEstimationResults',
                       'PCA', 'Scatters', 'ProfileLikelihoods',
                       'ParameterEstimationResults']
            if delete_dirs:
                for i in subdirs:
                    d = os.path.join(dire, i)
                    if os.path.isdir(d):
                        try:
                            shutil.rmtree(d)
                        except WindowsError:
                            print('failed with windows error')

            for i in glob.glob(os.path.join(dire, '*.xlsx')):
                os.remove(i)

            for i in glob.glob(os.path.join(dire, '*.cps')):
                os.remove(i)

            for i in glob.glob(os.path.join(dire, '*.txt')):
                os.remove(i)

            for i in glob.glob(os.path.join(dire, '*.csv')):
                os.remove(i)

            for i in glob.glob(os.path.join(dire, '*.pickle')):
                dire, fle = os.path.split(i)
                ## keep until I know keep list is not needed.
                keep_list = []
                if fle not in keep_list:
                    os.remove(i)


if __name__ == '__main__':
    unittest.main()
