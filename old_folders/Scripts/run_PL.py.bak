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
run Profile likelihoods
"""

import PyCoTools
import os
import argparse


##==============================================================================
des=''' run profile likelihoods using copasi''' 
parser=argparse.ArgumentParser(description=des)

parser.add_argument('model',help='model to run profile likelihood analysis on')

parser.add_argument('index',nargs='+',
                    help='''-1 for parameters already in model, integer value for
                    index of best fit (0 is best) or list of integers for multiple''',
                    type=int,
                    default=None)

parser.add_argument('--parameter_path',
                    help='Full path to parameter results file or folder of results files from the same problem',
                    type=str,
                    default=None)

parser.add_argument('--upper_boundMultiplier',
                    help='number to multiple parameter of interest by',
                    default=1000,
                    type=int)

parser.add_argument('--lower_boundMultiplier',
                    help='number to multiple parameter of interest by',
                    default=1000,
                    type=int)

parser.add_argument('--number_of_steps',
                    help='How densily to sample the profile likelihoods',
                    default=10,
                    type=int)

parser.add_argument('--run',
                    help='''One of 'false','slow','multiprocess','SGE' ''',
                    default='slow')

args=parser.parse_args()

##==============================================================================

if args.index==None:
    args.index=-1
    
if args.parameter_path!=None:
    parameters=PyCoTools.PEAnalysis.ParsePEData(args.parameter_path)
    print(parameters.data.iloc[args.index].sort_index().transpose())

PyCoTools.pydentify2.ProfileLikelihood(args.model, #full path to the model
                                       parameter_path=args.parameter_path, #full path to the PEData
                                       index=args.index, #index of PE set for profiling. (best is 0)
                                       number_of_steps=args.number_of_steps, #resolution of profile likelihood 
                                       run=args.run,#run method, 
                                       
                                       ##specify multipliers for scan boundaries\
                                       ##i.e. if estimated parameter was 0.1, \
                                       ##Boundaries with the present settings would be \
                                       ##between 0.1/1000 and 0.1*1000 = 0.0001 and 100\
                                       upper_boundMultiplier=args.upper_boundMultiplier, 
                                       lower_boundMultiplier=args.lower_boundMultiplier)  


























