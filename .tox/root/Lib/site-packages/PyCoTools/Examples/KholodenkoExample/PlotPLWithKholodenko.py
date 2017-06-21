# -*- coding: utf-8 -*-
'''
 This file is part of PyCoTools.

 PyCoTools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 PyCoTools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with PyCoTools.  If not, see <http://www.gnu.org/licenses/>.


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
Plot profile likelihoods
'''
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
































