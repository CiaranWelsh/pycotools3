# -*- coding: utf-8 -*-
"""
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
Run Profile likelihoods
"""

import PyCoTools
import os
import argparse


##==============================================================================
des=''' run profile likelihoods using copasi''' 
parser=argparse.ArgumentParser(description=des)

parser.add_argument('Model',help='Model to run profile likelihood analysis on')

parser.add_argument('Index',nargs='+',
                    help='''-1 for parameters already in model, integer value for
                    index of best fit (0 is best) or list of integers for multiple''',
                    type=int,
                    default=None)

parser.add_argument('--ParameterPath',
                    help='Full path to parameter results file or folder of results files from the same problem',
                    type=str,
                    default=None)

parser.add_argument('--UpperBoundMultiplier',
                    help='number to multiple parameter of interest by',
                    default=1000,
                    type=int)

parser.add_argument('--LowerBoundMultiplier',
                    help='number to multiple parameter of interest by',
                    default=1000,
                    type=int)

parser.add_argument('--NumberOfSteps',
                    help='How densily to sample the profile likelihoods',
                    default=10,
                    type=int)

parser.add_argument('--Run',
                    help='''One of 'false','slow','multiprocess','SGE' ''',
                    default='slow')

args=parser.parse_args()

##==============================================================================

if args.Index==None:
    args.Index=-1
    
if args.ParameterPath!=None:
    parameters=PyCoTools.PEAnalysis.ParsePEData(args.ParameterPath)
    print parameters.data.iloc[args.Index].sort_index().transpose()

PyCoTools.pydentify2.ProfileLikelihood(args.Model, #full path to the model
                                       ParameterPath=args.ParameterPath, #full path to the PEData
                                       Index=args.Index, #index of PE set for profiling. (best is 0)
                                       NumberOfSteps=args.NumberOfSteps, #resolution of profile likelihood 
                                       Run=args.Run,#Run method, 
                                       
                                       ##specify multipliers for scan boundaries\
                                       ##i.e. if estimated parameter was 0.1, \
                                       ##Boundaries with the present settings would be \
                                       ##between 0.1/1000 and 0.1*1000 = 0.0001 and 100\
                                       UpperBoundMultiplier=args.UpperBoundMultiplier, 
                                       LowerBoundMultiplier=args.LowerBoundMultiplier)  


























