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
        print('base class setUp being called')
        #make sure were in the same directory every time
        os.chdir(os.path.dirname(__file__))
        self.copasi_file = os.path.join(os.path.dirname(__file__), 'test_model.cps')

        self.ant = """// Created by libAntimony v2.9.4
                        model *TestModel1()
                        
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
                          A = 1
                          B = 1
                          C = 1
                        
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
        if os.path.isfile(self.copasi_file):
            raise ValueError('copasi file "{}" is already a file before test'.format(self.copasi_file))
        self.model = pycotools3.model.loada(self.ant, self.copasi_file)
        print(self.model)

        if not os.path.isfile(self.copasi_file):
            raise FileNotFoundError('copasi file "{}" is not found after creating with loada'.format(self.copasi_file))

    def tearDown(self):
        print('tearing down')

        dire = os.path.dirname(__file__)
        subdirs = ['Boxplots', 'TimeCourseGraphs',
                   'ParameterEstimationPlots', 'test_mpe',
                   'EnsembleTimeCourse', 'Histograms',
                   'LinearRegression', 'MultipleParameterEstimationResults',
                   'PCA', 'Scatters', 'ProfileLikelihoods',
                   'ParameterEstimationResults', 'Problem1',
                   'CrossValidation', 'AntimonyModels',
                   'SensitivityTests']

        for i in subdirs:
            d = os.path.join(dire, i)
            if os.path.isdir(d):
                try:
                    shutil.rmtree(d)
                except WindowsError:
                    print('failed with windows error')

        file_types_to_remove = [
            '*.xlsx',
            '*.log',
            '*.cps',
            '*.txt',
            '*.csv',
            '*.pickle',
            '*.json',
            '*.yaml',
            '*.yml',
            '*.yaml',
            '*.sbml',
        ]
        for i in file_types_to_remove:
            for j in glob.glob(os.path.join(dire, i)):
                os.remove(j)



if __name__ == '__main__':
    unittest.main()
