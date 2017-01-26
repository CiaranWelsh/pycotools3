# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 21:59:01 2017

@author: b3053674
"""
import PyCoTools
import os
import pandas
import numpy

current_directory='D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Examples\GoldbetterExample'
copasi_file=r'Goldbeter1995_CircClock.cps'
goldbetter_model=os.path.join(current_directory,copasi_file)
report=os.path.join(current_directory,'TimeCourseOutput.txt')
noisy_report=os.path.join(current_directory,'NoisyTimeCourseOutput.txt')

#

def add_noise(f,noise_factor=0.05):
    '''
    add noise to time course data
    
    f:
        only one experiment file called f
    
    noise_factor:
        limits the amount of noise to add. Must be float between 0 and 1
        . default is 0.05 or 5% 
    
    '''
    assert os.path.isfile(f),'{} is not a file'.format(f)
    df=pandas.read_csv(f,sep='\t')
    #remember to account for the time varible
    number_of_data_points= df.shape[0]*(df.shape[1]-1)
    u= numpy.random.uniform(1-noise_factor,1+noise_factor,number_of_data_points)
    matrix= u.reshape(df.shape[0],df.shape[1]-1)
    #save time for later
    try:
        
        t=df['Time']
        df.drop('Time',axis=1,inplace=True)
        df_noise=pandas.DataFrame(matrix,columns=df.columns)
    except KeyError:
        return None
    assert df.shape==df_noise.shape
    noise= df_noise.rmul(df,axis=0)
    noise.index=t
    return noise
    
    
print add_noise(report).to_csv(noisy_report)






































