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

"""

import PyCoTools
import os
import FilePaths
import shutil
import sys

K=FilePaths.KholodenkoExample()

if os.path.isdir(K.PEData_dir):
    PEData_path=K.PEData_dir
elif os.path.isdir(K.PEData_dir) !=True:
    if os.path.isfile(K.PEData_file):
        PEData_path=K.PEData_file
        
        
data= PyCoTools.PEAnalysis.ParsePEData(PEData_path).data








def runHJ(copasi_file,parameters,report_name,mode):
    '''
    copasi_file:
        file to run hook and jeeves from 
    parameters:
        dictionary of parameters. Keys must match model names, values are input parameters
    report_name:
        name of the report to output PE data.
    mode:
        either 'SGE' for SGE cluster or 'true' to run on current machine
    
    Take parameters from global parameter estimation and perform local parameter
    estimation around these parameters.
    
    Need to instantiate ParameterEstimation class before inserting parameters
    '''
    if 'RSS' in parameters.keys():
        del parameters['RSS']
    for i in parameters:
        print i,':\t',parameters[i]
    PyCoTools.pycopi.InsertParameters(copasi_file,parameter_dict=parameters)
    
    PE=PyCoTools.pycopi.ParameterEstimation(copasi_file,K.noisy_timecourse_report,
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
    PyCoTools.pycopi.Scan(copasi_file,scan_type='repeat',run=mode,
                          number_of_steps=1,
                          report_name=report,
                          report_type='parameter_estimation')

#data.shape[0]*0.01)
if __name__=='__main__':
    if sys.platform=='win32':
        '''
        run hook and jeeves from the top 1 percent
        best estimated parameter from the genetic algorithm
        run on windows machine
        '''
        mode='true'
        for i in range(int(data.shape[0]*0.025)):
            print 'running index {} with starting RSS of {}'.format(i,data.iloc[i]['RSS'])
            if os.path.isdir(K.local_PEData_dir)!=True:
                os.mkdir(K.local_PEData_dir)
            report=os.path.join(K.local_PEData_dir,'{}.txt'.format(i))
            print runHJ(K.kholodenko_model,data.iloc[i].to_dict(),report,mode)

    elif sys.platform=='linux2':
        '''
        A few differences required when running on a clutser. 
        Generally there is a time delay between submitting job and 
        running the job. This time delay is longer than the time between an iteration
        of the below loop meaning that by the time the job gets submitted, all
        jobs get the same report name. Solution - copy and enumerate copasi file. 
        
        '''
        mode='SGE'
        for i in range(int(data.shape[0]*0.025)):
            print 'running index {} with starting RSS of {}'.format(i,data.iloc[i]['RSS'])
            if os.path.isdir(K.local_PEData_dir)!=True:
                os.mkdir(K.local_PEData_dir)
            report=os.path.join(K.local_PEData_dir,'{}.txt'.format(i))
            enum_cps=os.path.splitext(K.kholodenko_model)[0]+'temp{}.cps'.format(str(i))
            shutil.copyfile(K.kholodenko_model,enum_cps)
            print runHJ(enum_cps,data.iloc[i].to_dict(),report,mode)        
        































