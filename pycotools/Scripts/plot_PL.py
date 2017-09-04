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
 
 
script for viualization of profile likelihoods
"""

import PyCoTools
import argparse

##==============================================================================

parser=argparse.ArgumentParser(description='plot Profile likelihood data ')

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

parser.add_argument('--RSS',
                    help='value for RSS. Only used when index = -1',
                    type=int,
                    default=None)

parser.add_argument('--log10',help='Sample in log10 space',default='true',choices=['true','false'])
parser.add_argument('--savefig',help='Sample in log10 space',default='true',choices=['true','false'])
parser.add_argument('--Multiplot',help='plot multiple runs on the same canvas',default='true',choices=['true','false'])
parser.add_argument('--UsePickle',help='Parse estimation data using pickled data file',default='false',choices=['true','false'])
parser.add_argument('--overwrite_pickle',help='Overwrite the automatically produced pickle file',default='false',choices=['true','false'])

args=parser.parse_args()






##==============================================================================

if args.index==-1 and args.RSS==None:
    raise PyCoTools.Errors.InputError('if index=-1, a value to RSS must be specified')
    
    
if args.index==-1:
    PyCoTools.pydentify2.plot(args.model,
                           parameter_path=args.parameter_path,
                           RSS=args.RSS,
                           index=args.index,
                           log10=args.log10,
                           savefig=args.savefig,
                           Multiplot=args.Multiplot,
                           UsePickle=args.UsePickle,
                           overwrite_pickle=args.overwrite_pickle)
else:
    PyCoTools.pydentify2.plot(args.model, 
                           parameter_path=args.parameter_path,
                           index=args.index,
                           log10=args.log10,
                           savefig=args.savefig,
                           Multiplot=args.Multiplot,
                           UsePickle=args.UsePickle,
                           overwrite_pickle=args.overwrite_pickle)



























