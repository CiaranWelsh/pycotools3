#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:47:47 2017

@author: b3053674
"""

import site
site.addsitedir('/home/b3053674/Documents/PyCoTools')
import PyCoTools
import os, glob
import numpy




class FilePaths():
    """
    Class to manage directories 
    """
    def __init__(self):
        ## unchanged model
        self.dire = '/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/ModelSelection'
        self.kholodeko_model = os.path.join(self.dire, 'Kholodenko2000.cps')
        ## True Model that we simulate data from for the selection problem
        self.variant1 = os.path.join(self.dire, 'Kholodenko2000_variant1.cps')
        ## kholodenko model with one single phosphorylation reactions
        self.variant2 = os.path.join(self.dire, 'Kholodenko2000_variant2.cps')
        ## Kholodenko model with mass action reactions
        self.variant3 = os.path.join(self.dire, 'Kholodenko2000_variant3.cps')
        
        self.fit1_dir = os.path.join(self.dire, 'KholodenkoFit1')
        if os.path.isdir(self.fit1_dir)!=True:
            os.mkdir(self.fit1_dir)
        
        
F = FilePaths()





## Use GetModelQuantities to quickly locate our model variables we want to simulate
GMQ = PyCoTools.pycopi.GetModelQuantities(F.variant1)
global_quantities = GMQ.get_global_quantities().keys()
## Simulate Synthetic Data
TC = PyCoTools.pycopi.TimeCourse(F.variant1, step_size=100, intervals=10, 
                                end=1000, 
                                global_quantities = global_quantities,
                                metabolites=[],plot=False)




import shutil
[shutil.copy2(i, F.fit1_dir) for i in [F.variant1,
                                       F.variant2,
                                       F.variant3,
                                       TC['report_name']] ]


MMF = PyCoTools.pycopi.MultiModelFit(F.fit1_dir,
                                     copy_number=3, pe_number=50,
                                     method='GeneticAlgorithm',
                                     population_size=100,
                                     number_of_generations=300,
                                     lower_bound=1e-3,
                                     upper_bound=1e3)




MMF.format_data()


































