# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 09:17:04 2017

@author: b3053674
"""

import PyCoTools
import os
import sys
import subprocess
import threading
import pickle
import pandas
import time
'''
First download models using:
    >>>import PyCoTools
    >>>directory=<'/path/to/your/chosen/directory>
    >>PyCoTools.Misc.download_models(directory)
Then give this script the download directory as the 'DOWNLOAD_DIRECTORY' variable
Run this script to pass the models in curated biomodels to the pydentify_model
script.

'''







if sys.platform=='win32':
    DOWNLOAD_DIRECTORY=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PydentifyingBiomodelFoldersFromPyCoTools\PydentifyingBiomodels4'
    CLUSTER=False
else:
    DOWNLOAD_DIRECTORY=r'/sharedlustre/users/b3053674/12_Dec/PydentifyingBiomodelsAgain'
    CLUSTER=True
    
class FilePaths():
    def __init__(self):
        self.wd=DOWNLOAD_DIRECTORY
        if os.path.isdir(self.wd)!=True:
            raise PyCoTools.Errors.InputError('{} doesn\'t exist'.format(self.wd))
        
        self.model_downloads_pickle=os.path.join(self.wd,'BioModelsFilesPickle.pickle')
        self.cps_files_pickle=os.path.join(self.wd,'cpsFilesPickle.pickle')

        self.models_downloads_xlsx=os.path.join(self.wd,'ModelsMap.xlsx')
        
def xml2cps(model_pickle,cps_pickle):
    '''
    use CopasiSE to convert the xml into copasi files
    
    model_pickle:
        pickle file produced by PyCoTools.Misc.download_models
        
    cps_pickle:
        Path to name cps pickle output
    =================
    returns:
        list of copasi files
    '''
    
    paths= pandas.read_pickle(model_pickle)
#    print pandas.read_excel(models,header=0,index_col=0)
    def worker(path,output_path):
        return subprocess.check_call('CopasiSE -i "{}" -s {}'.format(path,output_path),shell=True)
        
    start=time.time()
    jobs=[]
    cps_files=[]
    for i in paths.index:
        path= paths.iloc[i][0]
#        print path
        cps_path=PyCoTools.Misc.RemoveNonAscii(os.path.splitext(path)[0]).filter+'.cps'
#        print cps_path
        print 'cps file:{}'.format(cps_path).decode('utf8')
        cps_files.append(cps_path)        
        if os.path.isfile(cps_path):
            continue
        p=threading.Thread(target=worker,args=(path,cps_path))
        jobs.append(p)
        p.start()
        p.join()
#        subprocess.check_call('CopasiSE -i "{}"'.format(paths['successful'][i]))
    print 'SBML to cps conversion took {}s'.format(time.time()-start)
    
    df=pandas.DataFrame( cps_files)
    df.to_pickle(cps_pickle)
#    
    
def pydentify_biomodels_cluster(cps_pickle):
    '''
    cps_pickle:
        Input to function. This is the pickle file containing copasi file paths
        produced by xml2cps function
        
    pydentify_model_file:
        Full path to script called pydentify_model.py distributed with 
        PyCoTools under the scripts folder. 
    '''
    skipped=[]
    copasi_files=pandas.read_pickle(cps_pickle)
    for i in copasi_files.index:
        cps_file= copasi_files.iloc[i][0]
        if os.path.isfile(cps_file)==False:
            raise PyCoTools.Errors.InputError('{} doesn\' exist.'.format(cps_file))
        dire,fle=os.path.split(cps_file)
        try:
            if CLUSTER:
                sh_file=os.path.join(dire,fle[:-4]+'_sh_file.sh')
                with open(sh_file,'w') as f:
                    f.write('module load apps/python27/2.7.8\nmodule load apps/COPASI/4.16.104-Linux-64bit\npython -m PyCoTools.Scripts.pydentify_model "{}"'.format(cps_file))
                os.system('qsub {}'.format(sh_file))
            else:
                subprocess.call('python -m PyCoTools.Scripts.pydentify_model "{}"'.format(cps_file),shell=True)

        except:
            skipped.append(cps_file)
    return skipped
            



if __name__=='__main__':
    
    F=FilePaths()
    PyCoTools.Misc.download_models(F.wd,percent=1)
    cps_files=xml2cps(F.model_downloads_pickle,F.cps_files_pickle)
    print pydentify_biomodels_cluster(F.cps_files_pickle)
    
    


















        
        
