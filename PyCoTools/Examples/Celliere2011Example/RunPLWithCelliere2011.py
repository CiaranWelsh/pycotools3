# -*- coding: utf-8 -*-

import PyCoTools
import os
import pandas
import numpy
import sys
import FilePaths

K=FilePaths.KholodenkoExample()


param=PyCoTools.PEAnalysis.ParsePEData(K.local_PEData_dir)
print param.data.iloc[0].sort_index()

PyCoTools.pydentify2.ProfileLikelihood(K.kholodenko_model, #full path to the model
                                       parameter_path=K.local_PEData_dir, #full path to the PEData
                                       index=[0,1], #index of PE set for profiling. (best is 0)
                                       number_of_steps=100, #resolution of profile likelihood 
                                       run='SGE',#run method, 
                                       
                                       ##specify multipliers for scan boundaries\
                                       ##i.e. if estimated parameter was 0.1, \
                                       ##Boundaries with the present settings would be \
                                       ##between 0.1/1000 and 0.1*1000 = 0.0001 and 100\
                                       upper_boundMultiplier=1000, 
                                       lower_boundMultiplier=1000)  






































