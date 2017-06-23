# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 11:29:22 2016

@author: b3053674
"""

import PyCoTools
import os
import glob
import subprocess
import time 
import pickle


def get_cps(directory):
    '''
    returns dict[model_name]=model_path
    '''
    #get directories as a list
    cps_dirs=[]
    for i in os.listdir(directory):
        cps_dirs.append(os.path.join(directory,i))
    
    #convert to dict
    d={}
    for i in cps_dirs:
        try:
            os.chdir(i)
        except WindowsError:
            continue
        for j in glob.glob('*.cps'):
            d[os.path.split(i)[1]]= os.path.abspath(j)
    return d


def run_phase_space(cps,n,pickle_path,ignore_previously_completed=False):
    '''
    run a time course for each copasi file in the cps dict and plot as phase
    space diagrams
    
    cps:
        dictionary of copasi files 
    n:
        A model with more than n parameters is bypassed
        
    pickle_path: path for pickling 
    
    ignore_previously_completed: Use True if you need to restart for some reason
    
    returns:
        dict[sucess|fail]=[result|error] (where '|' mean 'or')
        
        Any time course which already exists is skipped
        models that produce a copasi error are ignored
        models that are too big to run in just a few seconds can be skipped
        by using KeyboardInterrutp. Many big models were manually deleted
        from the analysis.
        all data is pickled for later use
        
        Any model without any metabolites was ignored
        
        models with non-ascii characters in the name were ignored
        
        
    '''
    assert isinstance(cps,dict)
    assert isinstance(n,int)
    
    result={}
    result['successful']={}
    result['CopasiError']={}
    result['KeyboardInterrupt']={}
    result['NometabolitesError']={}
    result['IncompatibleStringError']={}
    result['OverNSpecies']={}

    time_d={}
    for i in sorted(cps.keys()):
        print 'running {}: '.format(i)
        start=time.time()
        time_course_name=os.path.join(os.path.dirname(cps[i]),'{}_TimeCourse.txt'.format(i))
        GMQ=PyCoTools.pycopi.GetmodelQuantities(cps[i])
        if len(GMQ.get_IC_cns())>n:
            result['OverNSpecies'][i]='More than {} parameters'.format(n)
            continue
        if ignore_previously_completed==True:
            if os.path.isdir(os.path.join(os.getcwd(),'Phaseplots')):
                continue
        try:
            TC=PyCoTools.pycopi.PhaseSpaceplots(cps[i],
                                 global_quantities=None,
                                 Intervals=10,
                                 StepSize=100,
                                 Start=0,
                                 End=1000,
                                 Linecolor='black',
                                 savefig='true',
                                 save='overwrite',
                                 plot='false')
            print '...successful'
            result['successful'][i]=TC.data
            end=time.time()
            time_d[i]=end-start
            
        except PyCoTools.Errors.CopasiError as C:
            '''
            Catch copasi errors. These errors arise as a result
            of incompatibility between copasi and the model            
            '''
            name=os.path.join(os.path.dirname(cps[i]),'ErrorPipe.txt')
            result['CopasiError'][i]=str(C)
            with open(name,'w') as f:
                '''
                Write the copasi error to a file called ErrorPipe
                '''
                f.write(str(C))
            print 'running {}: unsucessful'.format(i)
            continue
        except KeyboardInterrupt:
            '''
            If a model is taking too long to run a time course
            you can use keyboard interrupt to skip to the next
            model
            '''
            result['KeyboardInterrupt'][i]='KeyboardInterrupt'
            print 'running {}: unsucessful. User quit'.format(i)
            continue
        except PyCoTools.Errors.NometabolitesError as E:
            '''
            Some models downloaded from biomodels don't have any metabolites
            and therefore we cannot run a time course with them
            '''
            result['NometabolitesError'][i]=E
        except PyCoTools.Errors.IncompatibleStringError as E:
            '''
            Some models use non-ascii characters. Non-ascii characters are not 
            currently supported in this pycopi. 
            '''
            result['IncompatibleStringError'][i]=E
    with open(pickle_path,'w') as f:
        pickle.dump((result,time_d),f)
    return result,time_d


        




if __name__=='__main__':
    model_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
    assert os.path.isdir(model_dir)
    pickle_path=os.path.join(os.getcwd(),'timecourseResultPickle.pickle')
    
    #first get a handle on all the cps files we want to run
    cps=get_cps(model_dir)
    res=run_phase_space(cps,9,pickle_path,ignore_previously_completed=False)
    
    #pickle the result tuple that the run_timecourse function spits out
    with open(pickle_path,'w') as f:
        pickle.dump(res,f)
        
    assert os.path.isfile(pickle_path)
    
    
    print res[0].keys()
    print 'total number of copasi models: {}'.format(len(res[0]['successful'].keys()) + len(res[0]['CopasiError'].keys()) + len(res[0]['IncompatibleStringError'].keys()) + len(res[0]['IncompatibleStringError'].keys()) + len(res[0]['NometabolitesError'].keys()) + len(res[0]['KeyboardInterrupt'].keys()) + len(res[0]['OverNSpecies'].keys()))
    print 'number of successful time courses: {}'.format(len(res[0]['successful'].keys()))

    print 'number failed because model contains more than N species: {}'.format(len(res[0]['OverNSpecies'].keys()))
    print 'number failed with copasi error: {}'.format(len(res[0]['CopasiError'].keys()))
    print 'number failed because the model contains non-ascii characters: {}'.format(len(res[0]['IncompatibleStringError'].keys()))
    print 'number failed because model has no metabolites: {}'.format(len(res[0]['NometabolitesError'].keys()))
    print 'number failed because of keyboardInterrupt: {}'.format(len(res[0]['KeyboardInterrupt'].keys()))
#
    os.chdir(model_dir)


#    f=r'D:\MPhil\Python\My_Python_Modules\modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\BIOMD0000000063\Galazzo1990_FermentationPathwayKinetics.cps'
    
    
    
#    TC=PyCoTools.pycopi.PhaseSpaceplots(f,
#                     global_quantities=None,
#                     Intervals=100,
#                     StepSize=10,
#                     Start=0,
#                     End=1000,
#                     Linecolor='black',
#                     savefig='true',
#                     save='overwrite',
#                     plot='false')
#

#    g=PyCoTools.pycopi.GetmodelQuantities(f)
#    print g.get_metabolites().keys()
#    print g.get_metabolites()['Fructose 1\\,6-phosphate']


















