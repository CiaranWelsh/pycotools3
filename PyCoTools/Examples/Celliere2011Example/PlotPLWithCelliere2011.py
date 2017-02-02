# -*- coding: utf-8 -*-

import PyCoTools
import os
import pandas
import numpy


import FilePaths

K=FilePaths.KholodenkoExample()

PyCoTools.pydentify2.Plot(K.kholodenko_model, #full path to the model
                           ParameterPath=K.local_PEData_dir, #full path to the PEData
                           Index=[0,1],
                           Log10='true',
                           SaveFig='true')
#                           RSS=618.648)
                           






































