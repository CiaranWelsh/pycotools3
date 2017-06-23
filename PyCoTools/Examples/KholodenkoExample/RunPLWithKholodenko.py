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
 run profile likelihood with the kholodenko model
 '''
import PyCoTools
import os
import pandas
import numpy
import sys
import FilePaths
import subprocess

K=FilePaths.KholodenkoExample()


param=PyCoTools.PEAnalysis.ParsePEData(K.PE_data2_2)
print param.data.iloc[0].sort_index()

PyCoTools.pydentify2.ProfileLikelihood(K.kholodenko_model, #full path to the model
                                       parameter_path=K.PE_data2_2, #full path to the PEData
                                       index=range(5), #index of PE set for profiling. (best is 0)
                                       number_of_steps=25, #resolution of profile likelihood 
                                       run='SGE',#run method, 
                                       
                                       ##specify multipliers for scan boundaries\
                                       ##i.e. if estimated parameter was 0.1, \
                                       ##Boundaries with the present settings would be \
                                       ##between 0.1/1000 and 0.1*1000 = 0.0001 and 100\
                                       upper_boundMultiplier=1000, 
                                       lower_boundMultiplier=1000)  

































