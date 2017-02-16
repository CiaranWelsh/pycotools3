# -*- coding: utf-8 -*-

import PyCoTools
import os
import pandas
import numpy


import FilePaths

K=FilePaths.KholodenkoExample()

data= PyCoTools.PEAnalysis.ParsePEData(K.local_PEData_dir,
                                 UsePickle='true',
                                 OverwritePickle='true').data

print data.iloc[0]

PyCoTools.pydentify2.Plot(K.kholodenko_model, #full path to the model
                           ParameterPath=K.local_PEData_dir, #full path to the PEData
                           Index=range(3),
                           Log10='true',
                           SaveFig='true',
                           MultiPlot='true',
                           UsePickle='true',
                           OverwritePickle='false')
#                           
































