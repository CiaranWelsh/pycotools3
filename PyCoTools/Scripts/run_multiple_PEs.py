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
run multiple parameter estimations on a copasi file
"""
from shutil import copy
import PyCoTools
import os
import argparse
##==============================================================================
des=''' Setup n parameter estimations on a single file using 
ParameterEstimation and Scan tasks then copy the file m times and 
process each model through CopasiSE simultaneously'''
parser=argparse.ArgumentParser(description=des)
parser.add_argument('model',help='model to perform parameter estimation on')
parser.add_argument('ConfigFile',help='Pre-configured PyCoTools parameter estimation configuration file')
parser.add_argument('Data',nargs='+',help='data to use in parameter estimation. Accepts multiple file paths')
parser.add_argument('--method',help='method of parameter estimation',default='GeneticAlgorithm')
parser.add_argument('--randomize_start_values',help='Start parameter estimation from random initial values',default='true')
parser.add_argument('-n',help='Number of parameter estimations for model copy to perform',default=3,type=int)
parser.add_argument('-m',help='Number of times to copy the model. >6 will probably cause problems.',default=4,type=int)
parser.add_argument('--report_name',help='Name of parameter estimation report file to store results',default=None)

## arguments to control optimization specific parameterswith defaults
parser.add_argument('--NumberOfGenerations',help='method specific parameter',default=200,type=int)
parser.add_argument('--population_size',help='method specific parameter',default=50,type=int)
parser.add_argument('--random_number_generator',help='method specific parameter',default=1,type=int)
parser.add_argument('--seed',help='method specific parameter',default=0,type=int)
parser.add_argument('--pf',help='method specific parameter',default=0.475,type=float)
parser.add_argument('--iteration_limit',help='method specific parameter',default=50,type=int)
parser.add_argument('--tolerance',help='method specific parameter',default=0.00001,type=float)
parser.add_argument('--rho',help='method specific parameter',default=0.2,type=float)
parser.add_argument('--scale',help='method specific parameter',default=10,type=int)
parser.add_argument('--swarm_size',help='method specific parameter',default=50,type=int)
parser.add_argument('--std_deviation',help='method specific parameter',default=0.000001,type=float)
parser.add_argument('--number_of_iterations',help='method specific parameter',default=100000,type=int)
parser.add_argument('--start_temperature',help='method specific parameter',default=1,type=int)
parser.add_argument('--cooling_factor',help='method specific parameter',default=0.85,type=float)
args=parser.parse_args()
##==============================================================================


                      
                      

def copy_copasi(copasi_file,m):
    '''
    run a copasi file m times on the same computer 
    '''
    sub_copasi_files_dct={}
    copasi_path,copasi_filename=os.path.split(copasi_file)
    for i in range(m):
        new_cps=os.path.join(copasi_path,copasi_filename[:-4]+'{}.cps'.format(str(i)))
        copy(copasi_file,new_cps)
        sub_copasi_files_dct[i]= new_cps
    return sub_copasi_files_dct

def enumerate_PE_output(output_filename,m):
    '''
    make some more filenames for our analysis
    '''
    dct={}
    dire,fle=os.path.split(output_filename)
    output_dir=os.path.join(dire,'MultiplePEResults')
    if os.path.isdir(output_dir)!=True:
        os.mkdir(output_dir)
    for i in range(m):
        new_file=os.path.join(output_dir,fle[:-4]+'{}.txt'.format(str(i)))
        dct[i]=new_file
    return dct

if __name__=='__main__':
    copasi_files=copy_copasi(args.model,args.m)
    result_files=enumerate_PE_output(args.model,args.m)

    if args.report_name==None:
        args.report_name=os.path.join(os.path.dirname(args.model),'ParameterEstimationResults.txt')
    # general call to ParameterEstimation
    PE= PyCoTools.pycopi.ParameterEstimation(args.model,
                                               args.Data, 
                                               method=args.method, #change to genetic algorithm (why not?)
                                               plot='false', #don't want to plot this time
                                               savefig='false',
                                               randomize_start_values=args.randomize_start_values,
                                               report_name=args.report_name,
                                               
                                               config_filename=args.ConfigFile,
                                               NumberOfGenerations=args.NumberOfGenerations,
                                               population_size=args.population_size,
                                               random_number_generator=args.random_number_generator,
                                               seed=args.seed,
                                               pf=args.pf,
                                               iteration_limit=args.iteration_limit,
                                               tolerance=args.tolerance,
                                               rho=args.rho,
                                               scale=args.scale,
                                               swarm_size=args.swarm_size,
                                               std_deviation=args.std_deviation,
                                               number_of_iterations=args.number_of_iterations,
                                               start_temperature=args.start_temperature,
                                               cooling_factor=args.cooling_factor,
                                               )
    PE.set_up()
    for i in range(args.m):
        '''
        Set up n repeat items with number_of_steps repeats of parameter estimation
        Set run to false as we want to use the multiprocess mode of the run class
        to process all m files at once in CopasiSE
        '''
        PyCoTools.pycopi.Scan(copasi_files[i],
                              scan_type='repeat', #set up repeat item under scan. 
                              number_of_steps=args.n, #run the parameter estimation task 3 times
                              subtask='parameter_estimation', #this is the default, but included here for demonstration anyway
                              report_type='parameter_estimation', ## report automatically set up within copasi. 
                              report_name=result_files[i],
                              run='false') #run the scan task automatically in the background
    for i in copasi_files.values():
        PyCoTools.pycopi.run(i,mode='multiprocess',Task='scan')
    
                                    

    
    
    
    
    
    
    
    
    
    
    
