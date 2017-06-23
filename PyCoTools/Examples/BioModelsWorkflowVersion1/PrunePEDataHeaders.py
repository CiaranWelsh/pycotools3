
import PyCoTools
import glob
import subprocess
import time 
import pickle
import pandas,numpy,scipy
import re
import os

def prune1(f,delete_old=False):
    '''
    f
        text file containing PE results
    '''
    df=pandas.DataFrame.from_csv(f,sep='\t')
    l=list( df.keys())
    new_titles=[] 
    for j in l:
        #match anything between two square brackets with regex
        match= re.findall('.*\[(.*)\]',j)
#            print match
        #we need the residual sum of squares value to be called 'RSS'
        #and everything else to be an exact match to the corresponding
        #model element
        if match==[]:
#                if match[0]=='Parameter Estimation':
            new_titles.append(j)
        elif match[0]=='Parameter Estimation':
            new_titles.append('RSS')
        else:
            new_titles.append(match[0])
    assert len(df.columns)==len(new_titles)
    df.columns=new_titles
    df=pandas.DataFrame(df.iloc[-1]).transpose()
    new_path= os.path.splitext(f)[0]+'_pruned_titles.txt'
    if delete_old==True:
        assert os.path.isfile(new_path),'{} is not a file, set delete_old to False'.format(new_path)
        os.remove(new_path)            
    if os.path.isfile(new_path)==False:
        df.to_csv(new_path,sep='\t',index=False)
    return new_path
    
    
    
    
def prune_PE_titles(PE_files,delete_old=False):
    '''
    Take the output of copasi PE and remove additional
    elements of the titles (i.e. metabolites, Values etc...)
    
    delete_old:
        if True, files are pruned again and overwriten
    '''
#    print PE_files
    d={}
    for i in PE_files:
        d[i]=prune1(PE_files[i])
    return d






if __name__=='__main__':
    model_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
    os.chdir(model_dir)
    
    PE_data_pickle=os.path.join(os.getcwd(),'PEDataFilesPickle.pickle')
    
    
   
   
    with open(PE_data_pickle) as f:
        PE_result=pickle.load(f)
            
#    print PE_result.keys()
        
        
        
    
##    print len(PE_result.values())
#    print PE_result.values()
    os.chdir(model_dir)
    PE_data_pickle_pruned=os.path.join(os.getcwd(),'PEDataFilesPrunedPickle.pickle')
    
    pruned= prune_PE_titles(PE_result['successful'])
    with open (PE_data_pickle_pruned,'w') as f:
        pickle.dump(pruned,f)
#    
##    
##    
#    
    
    os.chdir('..')

    
    
    
    
    
    