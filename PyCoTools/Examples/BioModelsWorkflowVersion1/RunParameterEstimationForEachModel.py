import PyCoTools
import os
import glob
import subprocess
import time 
import pickle
import pandas,numpy,scipy
import re
import string

    
def pair_cps_with_data(data):
    '''
    return dict[cps_file]=data_with_noise_file
    '''
    paths=[]
    for i in data:
        dire= os.path.dirname(i)#[:-19]+'.cps'
        os.chdir(dire)
        for j in glob.glob('*.cps'):
            if isinstance(j,list):
                raise
            cps=os.path.join(dire,j)
            assert os.path.isfile(cps)
        paths.append((cps,i))
    return paths
            
def run_parameter_estimation(input_args,skip_already_done=False):
    '''
    run a parameter estimation on the list of models that we have simulated noisy
    time courses for. This estimation is generic in the sense that the same algorithm and 
    algorithm parameters are used for each model. Since this is proof of principle and we already 
    know the data fits the model, we can use estimation settings that will not take a long time
    
    input_args:
        Tuple: (copasi_file,experiment_file)
        
    skip_already_done:
        if you need to rerun the program for what ever reason you can 
        bypass estimations already completed by setting this to True
    '''
    result={}
    result['KeyboardInterrupt']={}
    result['ExperimentMappingError']={}
    result['CopasiError']={}
    result['successful']={}
    result['KeyError']={}
    for i in input_args:
        key=i[0]
        print 'running: {}'.format( i[0])
        report_name=os.path.join(os.path.dirname(i[0]),'PE_results.txt')
#        reports.append(report_name)
#        if os.path.isfile(report_name)==True:
#            os.remove(report_name)
        if skip_already_done==True:
            if os.path.isfile(report_name)==True:
                continue
            
        try:
            
            PE= PyCoTools.pycopi.ParameterEstimation(i[0],[i[1]],
                                                      save='overwrite',
                                                      Verbose='true',
                                                      OverwriteItemTemplate='true',
                                                      append='false',
                                                      method='GeneticAlgorithm',
                                                      population_size=20,
                                                      NumberOfGenerations=50,
                                                      report_name=report_name,
                                                      randomize_start_values='false',
                                                      savefig='true')
            PE.write_item_template()
            PE.set_up() 
            PE.run()  
            result['successful'][key]=report_name
        except KeyboardInterrupt:
            '''
            Allow user to use keyboard interrupt to skip a long estimation
            '''
            result['KeyboardInterrupt'][key]=report_name
            continue
        except PyCoTools.Errors.ExperimentMappingError:
            '''
            Sometimes an experimental mapping error occurs under unusual circumstances
            These are placed here
            '''
            result['ExperimentMappingError'][key]=report_name
            continue
        except PyCoTools.Errors.CopasiError:
            result['CopasiError'][key]=report_name
        except KeyError:
            result['KeyError'][key]=report_name
        
    return result
        
    


if __name__=='__main__':
    model_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
    
    '''
    Get a handle to the noisy data that was simulated from the running 
    runTimeCourseForEachmodel.py script
    '''
    noisy_simulated_data_paths=os.path.join(os.getcwd(),'NoisySimulatedDataPickle.pickle')
    with open(noisy_simulated_data_paths) as f:
        noisy_data_paths=pickle.load(f)
    
    '''
    To use ParameterEstimation you must have both the copasi file you want
    to run a parameter estimation on and the experiment path that you want to 
    use for fitting. The below function collects the correct input arguments
    '''
    PE_input_args= pair_cps_with_data( noisy_data_paths)
    
    '''
    Pass the ParameterEstimation input args (as a tuple) to the 
    run_parameter_estimation function: A generic function that uses
    the ParameterEstimation class to run a small Genetic algorithm estimation
    with a population size of 10 and a 50 generations. 
    '''
    pe_files= run_parameter_estimation(PE_input_args,skip_already_done=False)
    os.chdir(os.path.join('..',model_dir))
    
    os.chdir(model_dir)
    PE_data_pickle=os.path.join(os.getcwd(),'PEDataFilesPickle.pickle')
    with open(PE_data_pickle,'w') as f:
        pickle.dump(pe_files,f)
    

    with open(PE_data_pickle,'r') as f:
        PE_data_paths=pickle.load(f)

    print 'Summary:'
    print 'Conducted {} parameter estimations'.format(len(PE_data_paths))
    print 'Total number of parameter estimations attempted: {}'.format(len(pe_files['successful'].keys()) + len(pe_files['KeyboardInterrupt'].keys()) + len(pe_files['ExperimentMappingError'].keys()))
    print 'Number of sucessful parameter estiamtions: {}'.format(len(pe_files['successful']))
    print 'Number of parameter estimations failed because of an experiment mapping error: {}'.format(len(pe_files['ExperimentMappingError'].keys()))
    print 'Number of parameter estimations failed because KeyboardInterrupt: {}'.format(len(pe_files['KeyboardInterrupt'].keys()))
#
    os.chdir('..')
#


#
#    f=r'D:\MPhil\Python\My_Python_Modules\modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\BIOMD0000000104\Klipp2002_MetabolicOptimization_linearPathway(n=2).cps'
#    
#    r=r'D:\MPhil\Python\My_Python_Modules\modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\BIOMD0000000104\data_with_noise.txt'
#    
#    t=r'D:\MPhil\Python\My_Python_Modules\modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\BIOMD0000000104\PE_results.txt'
#    
#    PE= PyCoTools.pycopi.ParameterEstimation(f,r,
#                                              save='overwrite',
#                                              Verbose='true',
#                                              OverwriteItemTemplate='true',
#                                              append='false',
#                                              method='GeneticAlgorithm',
#                                              population_size=10,
#                                              NumberOfGenerations=50,
#                                              report_name='report.txt',
#                                              randomize_start_values='true')
#    PE.write_item_template()
#    PE.set_up()
#    PE.run()

#    PE=PyCoTools.pycopi.PlotPEData(f,r,t)
#
#    R=PyCoTools.pycopi.run(f,Task='parameter_estimation')

#    p=PyCoTools.pycopi.GetmodelQuantities(f)
#    for i in  p.get_all_params_dict().keys():
#        print i.decode('utf8')
#
#    ICP=PyCoTools.pycopi.InsertParameters(f,parameter_path=)




