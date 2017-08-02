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
run local chaser parameter estimations
"""

import PyCoTools
import os
import argparse


##==============================================================================
parser=argparse.ArgumentParser(description='run  local (HookJeeves) PE starting at output from global')
parser.add_argument('model',help='model to chase')
parser.add_argument('experimental_data',help='data to fit')
parser.add_argument('data_dir',help='path to parameter estimation data file')
parser.add_argument('-o', help='output data directory name',default=None)
parser.add_argument('-p',help='float between 0 and 1. Proportion of runs to chase with local',default=0.1,type=float)
args=parser.parse_args()
##==============================================================================



def runHJ(copasi_file,experimental_data,parameters,report_name):
    '''
    copasi_file:
        file to run hook and jeeves from 
    parameters:
        dictionary of parameters. Keys must match model names, values are input parameters
    report_name:
        name of the report to output PE data.
    
    Take parameters from global parameter estimation and perform local parameter
    estimation around these parameters.
    
    Need to instantiate ParameterEstimation class before inserting parameters
    '''
    if 'RSS' in parameters.keys():
        del parameters['RSS']
    for i in parameters:
        print i,':\t',parameters[i]
    PyCoTools.pycopi.InsertParameters(copasi_file,parameter_dict=parameters)
    
    PE=PyCoTools.pycopi.ParameterEstimation(copasi_file,experimental_data,
                                         method='HookeJeeves',
                                         iteration_limit=20000,
                                         tolerance=1e-30,
                                         randomize_start_values='false',
                                         plot='true',
                                         savefig='true',
                                         use_config_start_values='false',
                                         )

        
    PE.set_up()
    ## run via scan task because this gives only best values in function
    ## evaluations, rather than the periodic function evaluations as well
    print '\n\n'
    print report_name
    print '\n'
    PyCoTools.pycopi.Scan(copasi_file,scan_type='repeat',
                          number_of_steps=1,
                          report_name=report,
                          report_type='parameter_estimation',run='true')

#data.shape[0]*0.01)
if __name__=='__main__':
    os.chdir(os.path.dirname(args.model))
    
    if args.o==None:
        args.o=os.path.join(os.path.dirname(args.model),'ChaserParameterEstimations')
    
    data= PyCoTools.PEAnalysis.ParsePEData(args.data_dir).data
    '''
    run hook and jeeves from the top 1 percent
    best estimated parameter from the genetic algorithm
    run on windows machine
    '''
    if args.p>1 or args.p<0:
        raise Exception('args.p should be between 0 and 1')
    for i in range(int(data.shape[0]*args.p)):
        print 'running index {} with starting RSS of {}'.format(i,data.iloc[i]['RSS'])
        if os.path.isdir(args.o)!=True:
            os.mkdir(args.o)
        report=os.path.join(args.o,'{}.txt'.format(i))
        print runHJ(args.model,args.experimental_data,data.iloc[i].to_dict(),report)
        











