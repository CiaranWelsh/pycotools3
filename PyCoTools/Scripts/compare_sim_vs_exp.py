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
run a comparison between simulated and experimental profiles
"""

import PyCoTools
import argparse
#
##==============================================================================
parser=argparse.ArgumentParser()
parser.add_argument('Model',help='Model that was used in parameter estimation')
parser.add_argument('ParameterPath',help='File or folder of files containing parameter estimation data')
parser.add_argument('Index',help='index of parameter set to visualize (best=0)',type=int)
parser.add_argument('-s',help='Save figures to file',choices=['true','false'],default='true')


args=parser.parse_args()
##==============================================================================

GMQ=PyCoTools.pycopi.GetModelQuantities(args.Model)
##get experiment files defined in model
experiment_files= GMQ.get_experiment_files()
##insert data



#run a 

PEData=PyCoTools.PEAnalysis.ParsePEData(args.ParameterPath)

print 'best estimated parameters:\n',PEData.data.iloc[args.Index].sort_index()
PyCoTools.pycopi.InsertParameters(args.Model,ParameterPath=args.ParameterPath,Index=args.Index)
PE=PyCoTools.pycopi.ParameterEstimation(args.Model,experiment_files,
                                        Method='CurrentSolutionStatistics',
                                        Plot='true',
                                        SaveFig=args.s,
                                        RandomizeStartValues='false') #important to turn this off
PE.set_up() ## setup
PE.run()    ## and run the current solution statistics parameter estimation





























