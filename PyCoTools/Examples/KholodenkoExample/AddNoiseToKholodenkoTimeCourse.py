# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 21:59:01 2017

@author: b3053674
"""
import PyCoTools
import os
import pandas
import numpy

import sys
from FilePaths import KholodenkoExample


def add_noise(f,noise_factor=0.05):
    '''
    add noise to time course data
    
    f:
        Single experiment file to add noise too
    
    noise_factor:
        limits the amount of noise to add. Must be float between 0 and 1
        . default is 0.05 for 5% 
    
    '''
    ## check file is real file
    assert os.path.isfile(f),'{} is not a file'.format(f)
    ## read into pandas
    df=pandas.read_csv(f,sep='\t')
    ## Count number of data points to add noise too
    ## remember to account for the time varible by minus 1 from column dimension 
    number_of_data_points= df.shape[0]*(df.shape[1]-1)
    ## sample from uniform distribution 'number_of_data_points' times and assign to u vector
    u= numpy.random.uniform(1-noise_factor,1+noise_factor,number_of_data_points)
    ## reshape u vector into a 'u matrix'
    u_matrix= u.reshape(df.shape[0],df.shape[1]-1)
    ## remove the time colum but save as 't' variable for later
    try:
        
        t=df['Time']
        df.drop('Time',axis=1,inplace=True)
        df_noise=pandas.DataFrame(u_matrix,columns=df.columns)
    except KeyError:
        return None
    ## Check we have the corect shape for matrix
    assert df.shape==df_noise.shape
    ## Perform dot multiplication on two matrices to get noisy matrix
    noise= df_noise.rmul(df,axis=0)
    ## change index to be time
    noise.index=t
    ## return noisy vector
    return noise
    
    
if __name__=='__main__':
    ## instantiate FilePaths.KhodenkoExmaple to get necessary file paths
    K=KholodenkoExample()
    ## add noise to simulated kholodenko output
    add_noise(K.timecourse_report).to_csv(K.noisy_timecourse_report,sep='\t')






































