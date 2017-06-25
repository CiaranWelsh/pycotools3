# -*- coding: utf-8 -*-
"""
Created on Fri Sep 02 12:13:22 2016

@author: b3053674
"""

import PyCoTools
import os
import glob
import subprocess
import time 
import pickle
import pandas,numpy,scipy
import re


def get_cps_dirs(d):
    '''
    return list of folders containing downloaded models from 
    biomodels
    '''
    cps_dirs=[]
    for i in os.listdir(d):
        cps_dirs.append(os.path.join(d,i))
    return cps_dirs
    

def get_cps(cps_dirs):
    '''
    returns dict[model_name]=model_path
    '''
    d={}
    for i in cps_dirs:
        os.chdir(i)
        for j in glob.glob('*.cps'):
            d[os.path.split(i)[1]]= os.path.abspath(j)
    return d


def get_timecourse_cps(all_cps,timecourse_cps):
    '''
    Separate models which failed to run time course from
    models which a time course was sucessfully completed
    '''
    res=[]
    sucess=timecourse_cps['successful'].keys()
    for i in all_cps:
        for j in sucess:
            if os.path.split(i)[1] ==j:
                res.append(i)
    return res
    
def get_timecourse_files(timecourse_models):
    '''
    return handle to time course which should be the only text
    file in the folder
    
    timecourse_models represents the subset of models in biomodels 
    with n parameters or less and runs without error in copasi
    
    '''
    experiment_files=[]
    for i in timecourse_models:
        os.chdir(i)
        for j in glob.glob('*.txt'):
            if '_with_noise'  not in j and 'ErrorPipe'  not in j and 'PE_results' not in j:
                experiment_files.append(os.path.abspath(j))
    return experiment_files
    
    
def add_noise1(f,noise_factor=0.05):
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
    '''
    The below commented out code is for replacing elements 
    of specie names.  Might not still needs this!
    '''
#    l=[]
#    replace_list=[',','{','}','[',']']
#    for i in df.keys():
#        for j in replace_list:
#            l.append(re.sub(j,'\\{}'.format(j)))
#    df.columns=l
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
    
    
def add_noise(experiment_path_list):
    '''
    add noise to all time courses 
    
    returns the paths to the cps files and the corresponding noisy data as tuple
    '''
#    print add_noise1(cps_list[5])
    paths=[]
    for i in experiment_path_list:
        path= os.path.join(os.path.dirname(i),'data_with_noise.txt')
        paths.append(path)
#        print i
        noise=add_noise1(i)
        if os.path.isfile(path)==False:
            noise.to_csv(path,sep='\t')
        assert os.path.isfile(path)
    return paths
    

    


if __name__=='__main__':
    d=os.path.join(os.getcwd(),'PydentifyingBiomodels')
#    model_dir=os.path.join(os.getcwd(),'models')
    '''
    Get a handle to the time course results from the runTimeCourseForEachmodel.py 
    script
    '''
    timecourse_pickle=os.path.join(os.getcwd(),'timecourseResultPickle.pickle')
    assert os.path.isfile(timecourse_pickle),'{} is not a file. Have you ran the runTimeCourseForEachmodel.py script yet?'.format(timecourse_pickle)
    cps_dirs=get_cps_dirs(d)
    '''
    get timecourse results paths from the runTimeCourse script
    '''
    with open(timecourse_pickle) as f:
        result,time_d= pickle.load(f)    
        
    '''
    Get the directories to the models which had a time 
    course ran sucessfully in the previous script
    '''
    timecourse_models=get_timecourse_cps(cps_dirs,result)
#    print timecourse_models
    
    #from the directories get the time course times
    timecourse_files=get_timecourse_files(timecourse_models)  
#    print timecourse_files
    paths= add_noise(timecourse_files)
    
    #make sure your in the correct directory
    os.chdir(os.path.dirname(d))    
    
    noisy_simulated_data_paths=os.path.join(os.getcwd(),'NoisySimulatedDataPickle.pickle')
    
    #save the noisy simulated data files in pickle for use in the parameter estimation script
    with open(noisy_simulated_data_paths,'w') as f:
        pickle.dump(paths,f)
        
    assert os.path.isfile(noisy_simulated_data_paths),'{} does not exist'.format(noisy_simulated_data_paths)
    

    print 'Number of data noise was added to is: {}'.format(len(paths))



    d=r'D:\MPhil\model_Building\models\Exercises\VilarForPoster\Vilar2006_TGFbeta\tc.txt'
    d2=r'D:\MPhil\model_Building\models\Exercises\VilarForPoster\Vilar2006_TGFbeta\tc2.txt'

    df=add_noise1(d)
    print df.to_csv(d2,sep='\t')




    os.chdir('..')




