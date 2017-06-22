import PyCoTools
import os
import glob
import subprocess
import time 
import pickle
import pandas,numpy,scipy
import re
import time
import sys


def run1PL(cps,data,skip_completed=False):
    os.chdir(os.path.dirname(cps)) #change to copasi file directory
    assert os.path.splitext(cps)[1]=='.cps','{} not a copasi file'.format(cps)
    assert os.path.splitext(data)[1]=='.txt','{} not a datafile'.format(data)
    if sys.platform=='win32':
        mode='slow'
    else:
        mode='SGE'
        
    '''
    Set run to false to that we can check if results files already 
    exist for parameters in this model. This is necessary to 
    skip already completed PLs and prevent this taking forever
    '''
    if skip_completed==True:
        
        GMQ=PyCoTools.pycopi.GetmodelQuantities(cps)
        fit_item_length= len(GMQ.get_fit_items().keys())
        PL_dir= os.path.join(os.path.dirname(cps),'ProfileLikelihood')
        PL_dir= os.path.join(PL_dir,'0')
        if os.path.isdir(PL_dir):
            os.chdir(PL_dir)
            len_text_files=0
            for i in glob.glob('*.txt'):
                len_text_files+=1
            if fit_item_length==len_text_files-1:#minus 1 to account for data_with_noise data file
                return cps
    PL= PyCoTools.pydentify2.ProfileLikelihood(cps,
                                                   parameter_path=data,
                                                   index=0,
                                                   iteration_limit=50,
                                                   tolerance=1e-3,
                                                   run=mode,
                                                   max_time=300,
                                                   )

                        

def run_all_PLs(model_data_dict,skip_completed=False):
    d={}
    d['successful']={}
    d['indexError']={}
    d['IOError']={}
    d['KeyError']={}
    d['CopasiError']={}
    for i in range(len(sorted(model_data_dict.keys()))):
#        print i,model_data_dict[model_data_dict.keys()[i]]
#        print model_data_dict.keys()[i]
        print 'running model number {} ({}) of {}'.format(i,model_data_dict.keys()[i],len(model_data_dict.keys()))
        try:
            run1PL(model_data_dict.keys()[i],model_data_dict[model_data_dict.keys()[i]],skip_completed)
            d['successful'][model_data_dict.keys()[i]]=model_data_dict[model_data_dict.keys()[i]]
        except indexError:
            '''
            some models give an index error because they have no metabolites. 
            '''
            d['indexError'][model_data_dict.keys()[i]]=model_data_dict[model_data_dict.keys()[i]]
            continue
        except IOError:
            d['IOError'][model_data_dict.keys()[i]]=model_data_dict[model_data_dict.keys()[i]]
            continue
        except KeyError:
            d['KeyError'][model_data_dict.keys()[i]]=model_data_dict[model_data_dict.keys()[i]]
            continue
        except PyCoTools.Errors.CopasiError:
            d['CopasiError'][model_data_dict.keys()[i]]=model_data_dict[model_data_dict.keys()[i]]
            continue
    return d




if __name__=='__main__':
    model_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
    os.chdir(model_dir)
#    PE_data_pickle=os.path.join(os.getcwd(),'PEDataFilesPickle.pickle')

    PE_data_pickle=os.path.join(os.getcwd(),'PEDataFilesPickle.pickle')
    PL_results_pickle=os.path.join(os.getcwd(),'PLResultPathsPickle.pickle')

    
#    PE_data_pickle=os.path.join((r'..\..'),'PEDataFilesPickle.pickle')
    with open(PE_data_pickle) as f:
        data=pickle.load(f)
        
        
    PL_results_paths= run_all_PLs(data['successful'],skip_completed=True)
    
    with open(PL_results_pickle,'wb') as f:
        pickle.dump(PL_results_paths,f)
    
    
#    print PL_results_paths
    
    os.chdir(model_dir)
#    print pruned[one]

    print '{} parameter estimations were ran'.format(len(data['successful'].keys()))
    




    
    
    
    
    
    
    
    