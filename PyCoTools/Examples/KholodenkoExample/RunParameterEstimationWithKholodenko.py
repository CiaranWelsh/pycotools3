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

"""
import PyCoTools
import os
import pandas
import numpy
from shutil import copy
import FilePaths

## Instantiate class contianing file paths for Kholodenko example
K=FilePaths.KholodenkoExample()

## Set up a parameter estimation 
'''
First instantiate ParameterEstimation class
with chosen keyword arguments. define the method variables within the PE class using the key word arguments
'''

PE= PyCoTools.pycopi.ParameterEstimation(K.kholodenko_model, #model
                                           K.noisy_timecourse_report, #experimental data
                                           method='GeneticAlgorithm',#use a quick global algorithm 
                                           NumberOfGenerations=300, #set Generation Number and population size
                                           population_size=150,
                                           swarm_size=200,
                                           iteration_limit=3000,
                                           )
#                                           plot='true',savefig='true') ## Optionally use to get experimental Vs simualted graphs
'''
Then write a template file. This contains all your model variables. 
Delete the rows containing variables that you do not want to estimate, modify
the estimation boundaries as you see fit, save and close. The last three columns
are for PyCoTools to set and map your variables and do not need to be touched. 

In this example I've removed the initial concentration varibles from the estimation

Comment and uncomment the below lines of code as you need
'''
#PE.write_item_template()


'''
Perform the setting up of the parameter estimation
variable names in the experimental data header need to exactly match the 
corresponding variables in the model to be mapped correctly. 
'''
PE.set_up()

'''
The run method enables you to run the parameter estimation from Python. 
If the plot keyword was set to 'true' in the instantiation of the ParameterEstimation
class, plots are generated of the experimental vs simulated data. 
In this tutorial however we want to run the parameter estimation via the repeat
scan task so we'll not use the run method.
'''
#PE.run() 
#

'''
run the parameter estimation via the scan task to run 'number_of_steps' of them

Other options include copying the model to 'n' other file locations. 
Then you could run the same code in a loop and have n copasi's running parameter
estimations on one machine. Alternatively the 'submit_copasi_multijob.py' 
script under the 'Scripts' folder in PyCoTools main directory will submit 
a copasi file 'n' times to a SunGrinEngine based cluster. Support for 
other job schedulers is not currently supported but modular nature of PyCoTools
allows for extension code to support other systems. 

#'''
PyCoTools.pycopi.Scan(K.kholodenko_model,scan_type='repeat',
                      report_name=K.PEData_file, 
                      report_type='parameter_estimation',
                      number_of_steps=2,run='false')




from shutil import copy
def copy_copasi(copasi_file,n):
    '''
    run a copasi file n times on the same computer 
    '''
    sub_copasi_files_dct={}
    copasi_path,copasi_filename=os.path.split(copasi_file)
    for i in range(n):
        new_cps=os.path.join(copasi_path,copasi_filename[:-4]+'{}.cps'.format(str(i)))
        copy(copasi_file,new_cps)
        sub_copasi_files_dct[i]= new_cps
    return sub_copasi_files_dct

def enumerate_PE_output(output_filename,n):
    '''
    make some more filenames for our analysis
    '''
    dct={}
    dire,fle=os.path.split(output_filename)
    output_dir=os.path.join(dire,'Results')
    if os.path.isdir(output_dir)!=True:
        os.mkdir(output_dir)
    
    for i in range(n):
        new_file=os.path.join(output_dir,fle[:-4]+'{}.txt'.format(str(i)))
        dct[i]=new_file
    return dct

#n=3
#copasi_files=copy_copasi(K.kholodenko_model,n)
#result_files=enumerate_PE_output(K.PEData_file,n)

        

#

#import matplotlib.pyplot as plt
#import numpy as np
#
## Generate data...
#x = np.random.random(10)
#y = np.random.random(10)
#print x,y
#plt.scatter(x, y, c=y, s=50, cmap='hsv')
#plt.show()


#for i in range(n):
#    PyCoTools.pycopi.Scan(copasi_files[i],scan_type='repeat',
#                          report_name=result_files[i], 
#                          report_type='parameter_estimation',
#                          number_of_steps=3,run='false')
#    PyCoTools.pycopi.run(copasi_files[i],mode='multiprocess',Task='scan')
#
#

#
f=r"D:\MPhil\Python\My_Python_Modules\modelling_Tools\temp\kholodenkoTemp\attempt1\SecondIteration\PEResults"
data=PyCoTools.PEAnalysis.ParsePEData(f).data
#print pandas.read_pickle(K.PEData_pickle)
#f=r"D:\MPhil\Python\My_Python_Modules\modelling_Tools\temp\kholodenkoTemp\attempt1\ThirdIteration\2GlobalPEData.pickle"
#PyCoTools.PEAnalysis.plotHistogram(f,log10='true')
#PyCoTools.PEAnalysis.plotScatters(f,log10='true')



PyCoTools.PEAnalysis.plotHexMap(f,show='false',log10='true',
                                truncate_model='percent',x=100,savefig='true',
                                grid_size=50,
                                mode='RSS',bins=100)







