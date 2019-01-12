# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 09:06:25 2017

@author: b3053674
"""

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
 
After the biomodels workflow has been completed, this file iterates
through these files in search of the record of how long it took to 
profile the model. Then this is visualized to observe the relationship between 
model size and computation time.
'''

import PyCoTools
import os
import pickle
import pandas
import datetime
from . import pydentify_biomodels
import logging
import matplotlib.pyplot as  plt
import seaborn 



def read_computation_time_pickle(pickle_file):
    '''
    Args:
        pickle_file containing computation times from profile 
        likelihood calculations
        
    ===============================================
    returns:
        float. Number of minutes taken to calculate profile likelihoods

    '''
    if os.path.isfile(pickle_file)!=True:
        PyCoTools.Errors.InputError('Pickle file {} doesn\'t exist'.format(pickle_file))

    if os.path.splitext(pickle_file)[1]!='.pickle':
        raise PyCoTools.Errors.InputError('pickle_file should be a pickle file not {}'.format(os.path.splitext(pickle_file)))
    with open(pickle_file) as f:
        computation_time=pickle.load(f)
        
    minutes= computation_time/60
    return minutes
    
    
    
def get_num_parameters(model):
    '''
    Args:
        model. model to get information from 
        
    =======================
    returns:
        
    '''
    GMQ=PyCoTools.pycopi.GetModelQuantities(model)
    model_vars= GMQ.get_all_model_variables()
    return len(list(model_vars.keys()))
    
    
    
def get_computation_times(pickle_path):
    '''
    args:
        pickle_path. Path to copasi file pickle
    =====================
    returns
        pandas dataframe. number of params Vs computation time/num_params
    '''
    pickle_filename='profile_likelihood_computation_time_pickle.pickle'
    not_completed=[]
    copasi_files=pandas.read_pickle(pickle_path)
    df_list=[]
    for i in copasi_files.index:
        pickle_filename_i=os.path.join(os.path.dirname( copasi_files.iloc[i][0]),pickle_filename)
        if os.path.isfile( pickle_filename_i)!=True:
            not_completed.append(pickle_filename_i)
            continue
        else:
            computation_time=read_computation_time_pickle(pickle_filename_i)
            num_params=get_num_parameters(copasi_files.iloc[i][0])
            time_per_parameter= computation_time/num_params
            df= pandas.DataFrame([num_params,time_per_parameter]).transpose()
            df.columns=['Num params','computation_time/num_params(min per parameter)']
            df_list.append(df)
    df=pandas.concat(df_list)
    df=df.sort_values(by='Num params')
    df.reset_index(inplace=True,drop=True)
    df.to_pickle(F.computation_time_pickle)
    not_completed_df= pandas.DataFrame(not_completed)
    return df,not_completed_df
            
    
    
    
def plot_computation_times(df,figure_path,fontsize=22):
    '''
    
    '''
    df=df.reset_index()
    seaborn.set(font_scale=2)
    plt.figure()
    plt.scatter(df['Num params'],df[r'computation_time/num_params(min per parameter)'])
    plt.ylabel('Computation Time (Min)/num parameters')
    plt.xlabel('Num parameters')
    plt.title('Computation time of profile likelihoods\n per number of parameters')
    plt.savefig(figure_path,dpi=300,bbox_inches='tight')
    
    
    
    
    
    
    
if __name__=='__main__':
    F=pydentify_biomodels.FilePaths()
    df,d= get_computation_times(F.cps_files_pickle)
    plot_computation_times(df,F.figure_path)
    log=os.path.join(os.path.dirname(F.cps_files_pickle),'stats_log.pickle')
    with open(log,'w') as f:
        pickle.dump((df.shape,'\n',d.shape),f)
        
    print('computation times shape: {}'.format(df.shape))
    print('not processed shape: {}'.format(d.shape))
        


































