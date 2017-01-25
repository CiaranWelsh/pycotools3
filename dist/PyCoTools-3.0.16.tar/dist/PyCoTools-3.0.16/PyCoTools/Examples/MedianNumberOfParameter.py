# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 18:14:47 2016

@author: b3053674
"""

import PyCoTools
import os
import glob
import subprocess
import time 
import pickle
import pandas
import matplotlib
import numpy
import matplotlib.pyplot as plt
import sys


class PickleError(Exception):
    pass

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
        try:
            os.chdir(i)
        except OSError:
            continue
        for j in glob.glob('*.cps'):
            d[os.path.split(i)[1]]= os.path.abspath(j)
    return d

def investivate_parameters(cps,p,from_pickle=False):
    '''

        
    '''
    assert isinstance(cps,dict)
    if from_pickle==True:
        if  os.path.isfile(p):
            raise PickleError('{}, Your pickle path does not exist. Set \'from_pickle\' to False'.format(p))
        return pandas.read_pickle(p)
    IC=[]
    local=[]
    glob=[]
    Sum=[]
    for i in sorted(cps.keys()):
        print 'reading {}: sucessful'.format(i)
        time_course_name=os.path.join(os.path.dirname(cps[i]),'{}_TimeCourse.txt'.format(i))
        try:
            GMQ=PyCoTools.pycopi.GetModelQuantities(cps[i])
            glob.append( len(GMQ.get_global_kinetic_parameters_cns().keys()))
            IC.append( len(GMQ.get_IC_cns().keys()))
            local.append( len(GMQ.get_local_kinetic_parameters_cns().keys()))
        except :
            continue
    df=pandas.DataFrame([IC,local,glob],index=['ICs','local','global']).transpose()
    df['All']=df.sum(axis=1)
    df.to_pickle(p)
    return df






if __name__=='__main__':
    
    d=os.path.join(os.getcwd(),'PydentifyingBiomodels')

    pickle_path=os.path.join(d,'number_of_parameters.pickle')
    
    os.chdir(d)
    dirs= get_cps_dirs(d)
    cps=get_cps(dirs)
    matplotlib.rcParams.update({'font.size':20})
    df= investivate_parameters(cps,pickle_path,from_pickle=False)
    df=pandas.DataFrame( df[['All','ICs']])
    
    log10=False
    if log10==True:
        ax=numpy.log10(df).boxplot(fontsize=22,return_type='axes')
        ax.set_ylabel('Number of Parameters(Log10)')

    else:
        ax=df.boxplot(fontsize=26,return_type='axes',sym='',vert=True,widths=0.7,
                      patch_artist=False)
        ax.set_ylabel('Number of Parameters',fontsize=26)
    ax.set_title('Distribution of numbers of parameters \nin 595 of 613 curated models biomodels',fontsize=22)


 
    ICs_median= df['ICs'].median()
    
    all_median= df['All'].median()
    
    plt.annotate(s='Median={}'.format(str(ICs_median)),xy=(1.75,60))
    plt.annotate(s='Median={}'.format(str(all_median)),xy=(1.02,160))
    os.chdir(os.path.dirname(d))
    plt.savefig(os.path.join(d,'NumParametersData'),dpi=200,bbox_inches='tight')
    plt.show()
    
#    print 'The median number of parameters in the set of models downloaded from biomodels is {}'
#    print 'The median nu
#    
    
    
    
    os.chdir('..')

    
    
    
    
    
    
    
#
