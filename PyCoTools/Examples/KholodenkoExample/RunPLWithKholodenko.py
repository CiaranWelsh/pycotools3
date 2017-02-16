# -*- coding: utf-8 -*-

import PyCoTools
import os
import pandas
import numpy
import sys
import FilePaths
import subprocess

K=FilePaths.KholodenkoExample()


param=PyCoTools.PEAnalysis.ParsePEData(K.local_PEData_dir)
print param.data.iloc[0].sort_index()

PyCoTools.pydentify2.ProfileLikelihood(K.kholodenko_model, #full path to the model
                                       ParameterPath=K.local_PEData_dir, #full path to the PEData
                                       Index=range(5), #index of PE set for profiling. (best is 0)
                                       NumberOfSteps=100, #resolution of profile likelihood 
                                       Run='SGE',#Run method, 
                                       
                                       ##specify multipliers for scan boundaries\
                                       ##i.e. if estimated parameter was 0.1, \
                                       ##Boundaries with the present settings would be \
                                       ##between 0.1/1000 and 0.1*1000 = 0.0001 and 100\
                                       UpperBoundMultiplier=1000, 
                                       LowerBoundMultiplier=1000)  



copasiML=PyCoTools.pycopi.CopasiMLParser( K.kholodenko_model)
print copasiML.copasiML






























