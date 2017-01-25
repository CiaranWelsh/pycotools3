import PyCoTools
import os
import glob
import subprocess
import shutil 
import multiprocessing 
import threading
import time


class DirDoesNotExistError(Exception):
    pass
class FileDoesNotExistError(Exception):
    pass



def get_model_list():
    '''
    get list of model in the curent directory
    '''
    d={}
    d['successful']={}
    d['Error']={}
    subdirs= [i for i in os.listdir(os.getcwd()) if os.path.isdir(i)]
    subdirs=[os.path.abspath(i) for i in subdirs]
    for i in subdirs:
        if os.path.isdir(i)!=True:
            raise DirDoesNotExistError('{} does not exist'.format(i))
        os.chdir(i)
        for j in os.listdir(i):
            if j.endswith('.xml'):
                abs_path=os.path.abspath(j)

                if os.path.isfile(abs_path)==False:
                    d['Error'][j]=abs_path
                else:
                    d['successful'][j]=abs_path

    return d

def worker(path):
    return subprocess.check_call('CopasiSE -i "{}"'.format(path),shell=True)
    
        
def xml2cps(paths):
    '''
    use CopasiSE to convert the xml into copasi files
    (needs to be done only once hence why its commented out)
    '''
    start=time.time()
#    P=multiprocessing.Pool(4)
    jobs=[]
    for i in paths['successful']:
        print i
        p=threading.Thread(target=worker,args=(paths['successful'][i],))
        jobs.append(p)
#        print p
        p.start()
        p.join()
#        subprocess.check_call('CopasiSE -i "{}"'.format(paths['successful'][i]))
    return 'program took {}s'.format(time.time()-start)

#        num+=1
#    return num-

    

if __name__=='__main__':
    '''
    replace the dire variable to the path 
    to the models on your own machine
    '''
    d=os.path.join(os.getcwd(),'PydentifyingBiomodels')
    os.chdir(d)

    model_paths= get_model_list()
#    print len(model_paths['successful'])
    
    
    print xml2cps(model_paths)
    print 'number of models converted to copasi files is {}'.format(len(model_paths['successful']))

    os.chdir('..')

    import pickle
    cps_dirs_pickle=os.path.join(os.path.dirname(d),'cps_file_pickle.pickle')
    if os.path.isfile(cps_dirs_pickle):
        os.remove(cps_dirs_pickle)
    with open(cps_dirs_pickle , 'w') as f:
        pickle.dump(model_paths,f)
   
'''
65s with threading and 241.539999962s without threading = 3.7 times faster
'''





