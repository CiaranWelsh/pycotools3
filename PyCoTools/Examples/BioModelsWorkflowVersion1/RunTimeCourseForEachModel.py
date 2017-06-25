import PyCoTools
import os
import glob
import subprocess
import time 
import pickle


class FileDoesNotExistError(Exception):
    pass

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

    
    
def worker(cps):
    
    TC=PyCoTools.pycopi.TimeCourse(cps,
                     global_quantities=None,
                     Intervals=1000,
                     StepSize=0.1,
                     End=100,
                     Linecolor='black',
                     savefig='true',
                     save='overwrite',
                     plot='true')    
    return TC

def run_timecourse(cps,n,pickle_path,ignore_previously_completed=False):
    '''
    run a time course for each copasi file in the cps dict
    
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
#    assert isinstance(cps,dict)
    assert isinstance(n,int)
    
    result={}
    result['successful']={}
    result['CopasiError']={}
    result['KeyboardInterrupt']={}
    result['NometabolitesError']={}
    result['IncompatibleStringError']={}
    result['OverNSpecies']={}
    result['already_completed']={}
    result['FileDoesNotExistError']={}

    time_d={}
    for i in sorted(cps):
        print 'running {}: '.format(i)
        start=time.time()
        time_course_name=os.path.join(os.path.dirname(i),'{}_TimeCourse.txt'.format(i))

        try:
            
            GMQ=PyCoTools.pycopi.GetmodelQuantities(i)
            if len(GMQ.get_IC_cns())>n:
                result['OverNSpecies'][i]=i
                print '...over n species'
                continue
            if ignore_previously_completed==True:
                if os.path.isfile(time_course_name):
                    result['already_completed']=i
                    print '...already completed'
                    continue
            TC=PyCoTools.pycopi.TimeCourse(i,
                                 global_quantities=None,
                                 Intervals=1000,
                                 StepSize=0.1,
                                 End=100,
                                 report_name=time_course_name,
                                 Linecolor='black',
                                 savefig='true',
                                 save='overwrite',
                                 plot='true')
            print '...successful'
            result['successful'][i]=TC.data
            end=time.time()
            time_d[i]=end-start
            
        except PyCoTools.Errors.CopasiError as C:
            '''
            Catch copasi errors. These errors arise as a result
            of incompatibility between copasi and the model            
            '''
            name=os.path.join(os.path.dirname(i),'ErrorPipe.txt')
            result['CopasiError'][i]=str(C)
            with open(name,'w') as f:
                '''
                Write the copasi error to a file called ErrorPipe
                '''
                f.write(str(C))
            print 'running {}: unsucessful CopasiError'.format(i)
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
            print 'unsuccessful: NometabolitesError'
        except PyCoTools.Errors.IncompatibleStringError as E:
            '''
            Some models use non-ascii characters. Non-ascii characters are not 
            currently supported in this pycopi. 
            '''
            result['IncompatibleStringError'][i]=E
            print 'Unsuccessful: Non-Ascii strings'
            continue
        except PyCoTools.Errors.FileDoesNotExistError as E:
            result['FileDoesNotExistError'][i]=E
            print '...FileDoesNotExistError'
            continue
        
    
    with open(pickle_path,'w') as f:
        pickle.dump((result,time_d),f)
    return result,time_d


        




if __name__=='__main__':
    model_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
    assert os.path.isdir(model_dir)
    
    
    '''
    This is the path to the pickle containing paths to the xml
    files. This file is produced by the 'ConvertmodelsToCps.py' script. 
    Read the paths from the script and manipulate strings to get the paths
    to cps rather than xml
    '''
    cps_dirs_pickle=os.path.join(os.getcwd(),'cps_file_pickle.pickle')
    with open(cps_dirs_pickle) as f:
        cps=pickle.load(f)

    cps_list=[]
    for i in cps['successful']:
        f=  cps['successful'][i]    
        '''
        Raise error if path does not exist
        '''
        if os.path.isfile(f)!=True:
            raise FileDoesNotExistError('{} doesn\' exist. Ensure you have ran the ConvertmodelsToCps.py file properly'.format(i))
        cps_list.append(f[:-4]+'.cps')
    
    '''
    Provide another pickle path for collection of time course results. 
    This pickle path will go on to be used in subsequent scripts. 
    '''
    pickle_path=os.path.join(os.getcwd(),'timecourseResultPickle.pickle')
    res=run_timecourse(cps_list,9,pickle_path,ignore_previously_completed=False)

    '''
    pickle the result tuple that the run_timecourse function spits out
    '''
    with open(pickle_path,'w') as f:
        pickle.dump(res,f)
        
    
    '''
    print out some stats about the program performance 
    '''
    print res[0].keys()
    print 'total number of copasi models: {}'.format(len(res[0]['successful'].keys()) + len(res[0]['CopasiError'].keys()) + len(res[0]['IncompatibleStringError'].keys()) + len(res[0]['IncompatibleStringError'].keys()) + len(res[0]['NometabolitesError'].keys()) + len(res[0]['KeyboardInterrupt'].keys()) + len(res[0]['OverNSpecies'].keys()))
    print 'number of successful time courses: {}'.format(len(res[0]['successful'].keys()))

    print 'number failed because model contains more than N species: {}'.format(len(res[0]['OverNSpecies'].keys()))
    print 'number failed with copasi error: {}'.format(len(res[0]['CopasiError'].keys()))
    print 'number failed because the model contains non-ascii characters: {}'.format(len(res[0]['IncompatibleStringError'].keys()))
    print 'number failed because model has no metabolites: {}'.format(len(res[0]['NometabolitesError'].keys()))
    print 'number failed because of keyboardInterrupt: {}'.format(len(res[0]['KeyboardInterrupt'].keys()))

    print 'number failed because of FileDoesNotExistError: {}'.format(len(res[0]['FileDoesNotExistError'].keys()))

    os.chdir('..')











    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#    
#    
#    
#    
#    
#    
#    
#    
#    import PyCoTools
#import os
#import glob
#import subprocess
#import time 
#import pickle
#
#
#class FileDoesNotExistError(Exception):
#    pass
#
#def get_cps(directory):
#    '''
#    returns dict[model_name]=model_path
#    '''
#    #get directories as a list
#    cps_dirs=[]
#    for i in os.listdir(directory):
#        cps_dirs.append(os.path.join(directory,i))
#    
#    #convert to dict
#    d={}
#    for i in cps_dirs:
#        try:
#            os.chdir(i)
#        except WindowsError:
#            continue
#        for j in glob.glob('*.cps'):
#            d[os.path.split(i)[1]]= os.path.abspath(j)
#    return d
#
#    
#    
#def worker(cps):
#    
#    TC=PyCoTools.pycopi.TimeCourse(cps,
#                     global_quantities=None,
#                     Intervals=1000,
#                     StepSize=0.1,
#                     End=100,
#                     Linecolor='black',
#                     savefig='true',
#                     save='overwrite',
#                     plot='true')    
#    return TC
#
#def run_timecourse(cps,n,pickle_path,ignore_previously_completed=False):
#    '''
#    run a time course for each copasi file in the cps dict
#    
#    cps:
#        dictionary of copasi files 
#    n:
#        A model with more than n parameters is bypassed
#        
#    pickle_path: path for pickling 
#    
#    ignore_previously_completed: Use True if you need to restart for some reason
#    
#    returns:
#        dict[sucess|fail]=[result|error] (where '|' mean 'or')
#        
#        Any time course which already exists is skipped
#        models that produce a copasi error are ignored
#        models that are too big to run in just a few seconds can be skipped
#        by using KeyboardInterrutp. Many big models were manually deleted
#        from the analysis.
#        all data is pickled for later use
#        
#        Any model without any metabolites was ignored
#        
#        models with non-ascii characters in the name were ignored
#        
#        
#    '''
##    assert isinstance(cps,dict)
#    assert isinstance(n,int)
#    
#    result={}
#    result['successful']={}
#    result['CopasiError']={}
#    result['KeyboardInterrupt']={}
#    result['NometabolitesError']={}
#    result['IncompatibleStringError']={}
#    result['OverNSpecies']={}
#    result['already_completed']={}
#    result['FileDoesNotExistError']={}
#
#    time_d={}
#    for i in sorted(cps):
#        print 'running {}: '.format(i)
#        start=time.time()
#        time_course_name=os.path.join(os.path.dirname(i),'{}_TimeCourse.txt'.format(i))
#
#        try:
#            
#            GMQ=PyCoTools.pycopi.GetmodelQuantities(i)
#            if len(GMQ.get_IC_cns())>n:
#                result['OverNSpecies'][i]=i
#                print '...over n species'
#                continue
#            if ignore_previously_completed==True:
#                if os.path.isfile(time_course_name):
#                    result['already_completed']=i
#                    print '...already completed'
#                    continue
#            TC=PyCoTools.pycopi.TimeCourse(i,
#                                 global_quantities=None,
#                                 Intervals=1000,
#                                 StepSize=0.1,
#                                 End=100,
#                                 report_name=time_course_name,
#                                 Linecolor='black',
#                                 savefig='true',
#                                 save='overwrite',
#                                 plot='true')
#            print '...successful'
#            result['successful'][i]=TC.data
#            end=time.time()
#            time_d[i]=end-start
#            
#        except PyCoTools.Errors.CopasiError as C:
#            '''
#            Catch copasi errors. These errors arise as a result
#            of incompatibility between copasi and the model            
#            '''
#            name=os.path.join(os.path.dirname(i),'ErrorPipe.txt')
#            result['CopasiError'][i]=str(C)
#            with open(name,'w') as f:
#                '''
#                Write the copasi error to a file called ErrorPipe
#                '''
#                f.write(str(C))
#            print 'running {}: unsucessful CopasiError'.format(i)
#            continue
#        except KeyboardInterrupt:
#            '''
#            If a model is taking too long to run a time course
#            you can use keyboard interrupt to skip to the next
#            model
#            '''
#            result['KeyboardInterrupt'][i]='KeyboardInterrupt'
#            print 'running {}: unsucessful. User quit'.format(i)
#            continue
#        except PyCoTools.Errors.NometabolitesError as E:
#            '''
#            Some models downloaded from biomodels don't have any metabolites
#            and therefore we cannot run a time course with them
#            '''
#            result['NometabolitesError'][i]=E
#            print 'unsuccessful: NometabolitesError'
#        except PyCoTools.Errors.IncompatibleStringError as E:
#            '''
#            Some models use non-ascii characters. Non-ascii characters are not 
#            currently supported in this pycopi. 
#            '''
#            result['IncompatibleStringError'][i]=E
#            print 'Unsuccessful: Non-Ascii strings'
#            continue
#        except PyCoTools.Errors.FileDoesNotExistError as E:
#            result['FileDoesNotExistError']=i
#            print '...FileDoesNotExistError'
#            continue
#        
#    
#    with open(pickle_path,'w') as f:
#        pickle.dump((result,time_d),f)
#    return result,time_d
#
#
#        
#
#
#
#
#if __name__=='__main__':
#    model_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
#    assert os.path.isdir(model_dir)
#    
#    
#    '''
#    This is the path to the pickle containing paths to the xml
#    files. This file is produced by the 'ConvertmodelsToCps.py' script. 
#    Read the paths from the script and manipulate strings to get the paths
#    to cps rather than xml
#    '''
#    cps_dirs_pickle=os.path.join(os.getcwd(),'cps_file_pickle.pickle')
#    with open(cps_dirs_pickle) as f:
#        cps=pickle.load(f)
#
#    cps_list=[]
#    for i in cps['successful']:
#        f=  cps['successful'][i]    
#        '''
#        Raise error if path does not exist
#        '''
#        if os.path.isfile(f)!=True:
#            raise FileDoesNotExistError('{} doesn\' exist. Ensure you have ran the ConvertmodelsToCps.py file properly'.format(i))
#        cps_list.append(f[:-4]+'.cps')
#    
#    '''
#    Provide another pickle path for collection of time course results. 
#    This pickle path will go on to be used in subsequent scripts. 
#    '''
#    pickle_path=os.path.join(os.getcwd(),'timecourseResultPickle.pickle')
#    res=run_timecourse(cps_list,9,pickle_path,ignore_previously_completed=True)
#
#    '''
#    pickle the result tuple that the run_timecourse function spits out
#    '''
#    with open(pickle_path,'w') as f:
#        pickle.dump(res,f)
#        
#    
#    '''
#    print out some stats about the program performance 
#    '''
#    print res[0].keys()
#    print 'total number of copasi models: {}'.format(len(res[0]['successful'].keys()) + len(res[0]['CopasiError'].keys()) + len(res[0]['IncompatibleStringError'].keys()) + len(res[0]['IncompatibleStringError'].keys()) + len(res[0]['NometabolitesError'].keys()) + len(res[0]['KeyboardInterrupt'].keys()) + len(res[0]['OverNSpecies'].keys()))
#    print 'number of successful time courses: {}'.format(len(res[0]['successful'].keys()))
#
#    print 'number failed because model contains more than N species: {}'.format(len(res[0]['OverNSpecies'].keys()))
#    print 'number failed with copasi error: {}'.format(len(res[0]['CopasiError'].keys()))
#    print 'number failed because the model contains non-ascii characters: {}'.format(len(res[0]['IncompatibleStringError'].keys()))
#    print 'number failed because model has no metabolites: {}'.format(len(res[0]['NometabolitesError'].keys()))
#    print 'number failed because of keyboardInterrupt: {}'.format(len(res[0]['KeyboardInterrupt'].keys()))
#
#    print 'number failed because of FileDoesNotExistError: {}'.format(len(res[0]['FileDoesNotExistError'].keys()))
#
#    os.chdir('..')
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#









































