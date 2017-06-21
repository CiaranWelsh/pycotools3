import PyCoTools
import os
import pickle




#
#
#import sys
#
#if sys.platform=='win32':
#    PLpickle=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\BioModelsPydentify\Models\PLResultPathsPickle.pickle'
#else:
#    PLpickle=r'/sharedlustre/users/b3053674/2016/09_Sept/BioModelsPydentify/Models/PLResultPathsPickle.pickle'
#
#
#
#
#
#with open(PLpickle) as f:
#    PL=pickle.load(f)
#
##print PL.keys()
#
#
#print 'total number of PLs attempter: {}'.format(len(PL['successful'].keys())+len(PL['KeyError'].keys())+len(PL['IOError'].keys())+len(PL['IndexError'].keys()))
#print 'Number of successful PL runs: {}'.format(len(PL['successful'].keys()))
#
#print 'Number failed with IOError: {}'.format(len(PL['IOError'].keys()))
#
#print 'Number failed with IndexError: {}'.format(len(PL['IndexError'].keys()))
#
#print 'Number failed with KeyError: {}'.format(len(PL['KeyError'].keys()))


#print PL['successful']

#for i in PL['successful']:
#    PyCoTools.pydentify2.Plot(i,Index=0,ParameterPath=PL['successful'][i],SaveFig='true',)
#
#
#
#

def PLPlot(PL_results):
    results={}
    results['successful']={}
    results['KeyError']={}

    for i in range(len(PL_results['successful'].keys()))[4:]:
        print 'plotting {} of {}:\n{}'.format(i,len(PL_results['successful'].keys()),PL_results['successful'].keys()[i])
#        GMQ=PyCoTools.pycopi.GetModelQuantities(i)
#        print GMQ.get_global_quantities()
        copasi_file=PL_results['successful'].keys()[i]
        PE_data=PL_results['successful'][PL_results['successful'].keys()[i]]

        try:
            
            PyCoTools.pydentify2.Plot(copasi_file,
                                      ParameterPath=PE_data,
                                      Index=0,
                                      Show='false',
                                      SaveFig='true')
        except KeyError:
            results['KeyError'][copasi_file]=PE_data
            
#    
    
    
    
    
    
    
    
    
#==========================================================


if __name__=='__main__':
    model_dir=os.path.join(os.getcwd(),'PydentifyingBiomodels')
    os.chdir(model_dir)

    PL_results_pickle=os.path.join(os.getcwd(),'PLResultPathsPickle.pickle')
    
    with open(PL_results_pickle) as f:
        results=pickle.load(f)
        
        
    print PLPlot(results)

#    f=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\BIOMD0000000418\Ratushny2012_SPF.cps'
#    d=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Documentation\Examples\PydentifyingBiomodels\BIOMD0000000418\PE_results_pruned_titles.txt'
#
#    p=PyCoTools.pydentify2.Plot(f,ParameterPath=d,
#                              SaveFig='true',
#                              Index=0)
##    
#    p.plot_all()
#    k= p.data[0].keys()[4]
#    print k
#    GMQ=PyCoTools.pycopi.GetModelQuantities(f)
#    print GMQ.get_global_quantities()[k]
#    print GMQ.get_local_kinetic_parameters_cns().keys()
#    
#    print p.get_original_value(0,k)
#    print p.plot1(0,k)    
#    print p.data[0].keys()
    
    
    
    
    
    
    
    
    
    
