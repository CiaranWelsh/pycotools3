'''
 This file is part of PyCoTools.

 PyCoTools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 PyCoTools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with PyCoTools.  If not, see <http://www.gnu.org/licenses/>.


 $Author: Ciaran Welsh
 $Date: 12-09-2016 
 Time:  14:50
 
 
  This file uses the pycopi module to set up and run a profile likleihool
 method of identifiability analysis (Raue2009) by automating the COAPSI method
 (shaber2012). Use the ProfileLikelihood class to setup and run an identifiability
 analysis and the Plot class to calculate confidence intervals and visualize the 
 results. 
     

'''

import unittest
import os
import re
import pandas
import numpy
import scipy
import scipy.stats
import pycopi,Errors, PEAnalysis,Misc
import glob
import multiprocessing
import subprocess
from shutil import copyfile
import psutil
from collections import Counter
from time import sleep
import math
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from textwrap import wrap
import logging

LOG=logging.getLogger(__name__)


class ProfileLikelihood():
    '''
    This class uses the profile likelihood method of identifiability analysis
    to assess whether parameters can be uniquely determined with the defined 
    optimization problem. 
    
    copasi_file:
        The copasi file you wish to conduct a profile likelihood on
        
    **kwargs:
        ParameterPath:
            The absolute path to either a parameter estimation results file 
            ('.txt','.xlsx','.xls' or '.csv') or a folder of parameter 
            estimation results files. Default=None
            
        Index:
            The index of the parameter estimation run you want to calculate 
            a profile likelihood around. Parameter estimations are ranked in
            order of best fit, with 0 being the best fit value from your set of
            estimations. Can be either an integer or list of integers to give 
            the option of conducting multiple profile likelihoods using the same 
            line of code. Use Index=-1 if you want to calculate profile likelihood 
            around parameters already in copasi. If Index is not equal
            to -1 you must specificy a valid argument to the ParameterPath 
            keyword argument. Default is -1. 
    
        OutputML:
            When Save set to 'duplicate' this is the file name
            of the output cps file. Default='overwrite'

        Save:
            One of, 'false','overwrite' or 'duplicate'
            
        UpperBoundMultiplier:
            Number of times above the current value of the parameter of interest
            to extend profile likleihood to. Default=1000
        
        LowerBoundMultiplier:
            Number of times below the current value of the parameter of interest
            to extend profile likleihood to. Default=1000  
            
        NumberOfSteps:
            How many times to sample between lower and upper boundaries. Default=10
            
        Log:
            Sample in Log space. Default='false'
            
        IterationLimit:
            Hook and Jeeves algorithm iteration limit parameter. Default=50
            
        Tolerance:
            Hook and Jeeves algorithm tolerance parameter. Default=1e-5
            
        Rho:
            Hook and Jeeves algorithm Rho parameter. Default=0.2
            
        Run:
            Either ['false','slow','multiprocess','SGE']. 'multiprocess' 
            will use the number of processes specified in the NumProcesses 
            keyword argument to work. This features doesn't work well yet and
            user is reccommended to use slow mode which runs each 
            copasi file in serial. 'SGE' mode can be used specifically
            on a SunGridEngine managed cluster. Deault='false'
            
        NumProcesses:
            Deprecated: do not use
            How many processors to use at the same time. NumProcesses=0 will
            prevent running the estimations. Default 1

        SleepTime: 
            Deprecated: Do not use. 
            How many seconds to wait before running each copasi file. If running
            too many parameter estimations at the same time will slow your computer
            considerably. In this situation use a longer SleepTime.
    '''
    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=pycopi.CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML
        self.GMQ=pycopi.GetModelQuantities(self.copasi_file)
        os.chdir(os.path.dirname(self.copasi_file))

        default_outputML=os.path.split(self.copasi_file)[1][:-4]+'_Duplicate.cps'
        options={#report variables
                 'OutputML':default_outputML,
                 'Save':'overwrite',
                 'Index':-1,
                 'ParameterPath':None,
                 'QuantityType':'concentration',
                 'UpperBoundMultiplier':1000,
                 'LowerBoundMultiplier':1000,
                 'NumberOfSteps':10,
                 'Log':'false',
                 'IterationLimit':50,
                 'Tolerance':1e-5,
                 'Rho':0.2,
                 'Run':'false',
                 'NumProcesses':1, #when runset to 'true' determines, how many NumProcesses to use at the same time
                 'SleepTime':0, #How long to wait between running each copasi file
                 'Verbose':'true',
                 'MaxTime':None}
                 

        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for ProfileLikelihood'.format(i)
        options.update( kwargs) 
        self.kwargs=options    
        
        if self.kwargs.get('Index')!=-1:
            assert self.kwargs.get('ParameterPath')!=None,'If you specify an index, you need to specify an argument to ParameterPath'
        
        #if no index or ParameterPath specified, use current parameteres in cps
        self.mode='current'
        if self.kwargs.get('ParameterPath')!=None:
            #if parameter path is file or folder set the self.mode variablee accordingly
            if os.path.exists(self.kwargs.get('ParameterPath')):
                self.mode='file'
        
        #if ParameterPath specified without an index, set index to 0 (i.e. best parameter set)
#        if self.kwargs.get('ParameterPath')!=None and self.kwargs.get('Index') !=-1 and self.kwargs.get('Index')!=None:
#            self.kwargs['Index']=98
        self.PE_data=self.read_PE_data()
        if self.kwargs.get('MaxTime')!=None:
            if isinstance(self.kwargs.get('MaxTime'),(float,int))!=True:
                raise Errors.InputError('MaxTime argument should be float or int')
        
        if self.kwargs.get('Index') !=None:
            assert isinstance(self.kwargs.get('Index'),(list,int)),'index must be an integer or a list of integers'
        if isinstance(self.kwargs.get('Index'),list):
            for i in self.kwargs.get('Index'):
                assert isinstance(i,int),'Index is int type'
                try:
                    assert i<=self.PE_data.shape[0],'PE data contains {} parameter estimations. You have indicated that you want to use run {}'.format(self.PE_data.shape[0],i)
                except AttributeError:
                    raise Errors.Errors.InputError('No data')
        elif isinstance(self.kwargs.get('Index'),list):
            assert self.kwargs.get('Index')<=self.PE_data.shape[0],'PE data contains {} parameter estimations. You have indicated that you want to use run {}'.format(self.PE_data.shape[0],self.kwargs.get('Index'))

        if self.GMQ.get_fit_items()=={}:
            raise Errors.InputError('Your copasi file doesnt have a parameter estimation defined')
        #convert some numeric input variables to string
        self.kwargs['UpperBoundMultiplier']=str(self.kwargs['UpperBoundMultiplier'])
        self.kwargs['LowerBoundMultiplier']=str(self.kwargs['LowerBoundMultiplier'])
        self.kwargs['NumberOfSteps']=str(self.kwargs['NumberOfSteps'])
        self.kwargs['IterationLimit']=str(self.kwargs['IterationLimit'])
        self.kwargs['Tolerance']=str(self.kwargs['Tolerance'])
        self.kwargs['Rho']=str(self.kwargs['Rho'])
        
        if self.kwargs.get('Run') not in ['false','slow','multiprocess','SGE']:
            raise Errors.InputError('\'Run\' keyword must be one of \'slow\', \'false\',\'multiprocess\', or \'SGE\'')
        assert isinstance(self.kwargs.get('NumProcesses'),int)
        if self.kwargs.get('NumProcesses')!=0:
            self.kwargs['NumProcesses']=self.kwargs.get('NumProcesses')-1
        assert isinstance(self.kwargs.get('SleepTime'),int)
        
        
        assert self.kwargs.get('QuantityType') in ['concentration','particle_number']

        
        if self.kwargs.get('NumProcesses')>multiprocessing.cpu_count():
            raise Errors.Errors.InputError('You have selected {} processes but your computer only has {} available'.format(self.kwargs.get('NumProcesses'),multiprocessing.cpu_count()))
        
        assert self.kwargs.get('Log') in ['false','true']
#        if self.kwargs.get('Log')=='false':
#            self.kwargs['Log']=str(0)
#        else:
#            self.kwargs['Log']=str(1)

        
        self.cps_dct=self.copy_copasi_files_and_insert_parameters()
        self.copy_data_files()
        self.cps_dct= self.setup_report()
        self.cps_dct=self.setup_scan()
        self.cps_dct=self.setup_PE_task()        
        self.save()
        os.chdir(os.path.dirname(self.copasi_file))
        self.run()

        
    def save(self):
        if self.kwargs.get('Save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('Save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML

                
    def read_PE_data(self):
        '''
        if self.mode='current' do nothing
        if self.mode = file read from file
        if self.mode = folder read from folder
        '''
        if self.mode=='current':
            return None
        elif self.mode=='file':
            return PEAnalysis.ParsePEData(self.kwargs.get('ParameterPath')).data

    def copy_copasi_files_and_insert_parameters(self):
        '''
        Its easier to do these two functions together
        1) create relevant folders and copy copasi file into these based on the Index parameter
        '''
        cps_dct={}
        estimated_parameters= self.GMQ.get_fit_items().keys()
        IA_dir=os.path.join(os.path.dirname(self.copasi_file),'ProfileLikelihood')
        if os.path.isdir(IA_dir)==False:
            os.mkdir(IA_dir)
        os.chdir(IA_dir)
        if self.kwargs.get('Index')==-1:
            IA_dir=os.path.join(IA_dir,'-1')
            cps_dct[-1]={}
            if os.path.isdir(IA_dir)==False:
                os.mkdir(IA_dir)
            os.chdir(IA_dir)
            for i in estimated_parameters:
                st=Misc.RemoveNonAscii(i).filter
                filename=os.path.join(IA_dir,'{}.cps'.format(st))
                cps_dct[-1][i]=filename
                if os.path.isfile(filename)==True:
                    os.remove(filename)
                copyfile(self.copasi_file,filename)
            os.chdir(os.path.dirname(self.copasi_file))
#            os.chdir('..')
#            os.chdir('..')
            return cps_dct
            
        elif isinstance(self.kwargs.get('Index'),int):
            assert self.kwargs.get('Index')!=-1
            IP=pycopi.InsertParameters(self.copasi_file,
                                          Index=self.kwargs.get('Index'),
                                          QuantityType=self.kwargs.get('QuantityType'),
                                          DF=self.PE_data,Save='overwrite')
            IA_dir=os.path.join(IA_dir,str(self.kwargs.get('Index')))
            cps_dct[self.kwargs.get('Index')]={}
            if os.path.isdir(IA_dir)==False:
                os.mkdir(IA_dir)
            os.chdir(IA_dir)
            for i in estimated_parameters:
                st=Misc.RemoveNonAscii(i).filter
                filename=os.path.join(IA_dir,'{}.cps'.format(st))
                cps_dct[self.kwargs.get('Index')][i]=filename
                if os.path.isfile(filename)==True:
                    os.remove(filename)
                copyfile(self.copasi_file,filename)
            os.chdir('..')
            os.chdir('..')
            return cps_dct
            
        elif isinstance(self.kwargs.get('Index'),list):
            for i in self.kwargs.get('Index'):
                IP=pycopi.InsertParameters(self.copasi_file,
                                          Index=i,
                                          QuantityType=self.kwargs.get('QuantityType'),DF=self.PE_data,Save='overwrite')

                IA_dir2=os.path.join(IA_dir,str(i))
                cps_dct[i]={}
                if os.path.isdir(IA_dir2)==False:
                    os.mkdir(IA_dir2)
                os.chdir(IA_dir2)
                for j in estimated_parameters:
                    st=Misc.RemoveNonAscii(j).filter

                    filename=os.path.join(IA_dir2,'{}.cps'.format(st))
                    cps_dct[i][j]=filename
                    if os.path.isfile(filename)==True:
                        os.remove(filename)
                    copyfile(self.copasi_file,filename)
                    os.chdir('..')
            return cps_dct

    def copy_data_files(self):
        '''
        Move parameter estimation data from the directory with the parent cps
        file in to each relevant ProfileLikelihood sub folder. 
        
        Note that you must have your data files int the same directory as the 
        cps file you want to perform profile likeliood on. 
        '''
        self.IA_dir=os.path.join(os.path.dirname(self.copasi_file),'ProfileLikelihood')
        q='//*[@name="File Name"]'
        data_file_dct={}
#        print self.copasi_file
        for i in self.copasiML.xpath(q):
            data_path= os.path.join(os.path.dirname(self.copasi_file),i.attrib['value'])
            data_file_dct[i.attrib['value']]=data_path
            if self.kwargs.get('Index')==-1:
                IA_dir1=os.path.join(self.IA_dir,'-1')
                new_data_file1=os.path.join(IA_dir1,i.attrib['value'])
                copyfile(data_path,new_data_file1)
                
            elif isinstance(self.kwargs.get('Index'),int):
                IA_dir2=os.path.join(self.IA_dir,str(self.kwargs.get('Index')))
                new_data_file2=os.path.join(IA_dir2,i.attrib['value'])
                copyfile(data_path,new_data_file2)
                
            elif isinstance(self.kwargs.get('Index'),list):
                for j in self.kwargs.get('Index'):
                    IA_dir3=os.path.join(self.IA_dir,str(j))
                    new_data_file3=os.path.join(IA_dir3,i.attrib['value'])
                    copyfile(data_path,new_data_file3)
        return data_file_dct

    def setup_PE_task(self):
        '''
        remove parameter of interest from parameter estimation task
        and change method parameters 
        '''
        method_params={'name':'Hooke &amp; Jeeves', 'type':'HookeJeeves'}
        IterationLimit={'type': 'unsignedInteger', 'name': 'Iteration Limit', 'value': self.kwargs.get('IterationLimit')}
        Tolerance={'type': 'float', 'name': 'Tolerance', 'value': self.kwargs.get('Tolerance')}
        Rho={'type': 'float', 'name': 'Rho', 'value': self.kwargs.get('Rho')}

        method_element=pycopi.etree.Element('Method',attrib=method_params)
        pycopi.etree.SubElement(method_element,'Parameter',attrib=IterationLimit)
        pycopi.etree.SubElement(method_element,'Parameter',attrib=Tolerance)
        pycopi.etree.SubElement(method_element,'Parameter',attrib=Rho)
            
            
        query="//*[@name='FitItem']" 
        for i in self.cps_dct:
            for j in self.cps_dct[i]:
                C= pycopi.CopasiMLParser(self.cps_dct[i][j])
                childML=C.copasiML
                for k in childML.xpath(query):
                    for l in list(k):
                        if l.attrib['name']=='ObjectCN':
                            #metabolites first
                            match= re.findall('Metabolites\[{}\]'.format(j),l.attrib['value'])
                            if match !=[]:
                                parent=l.getparent()
                                parent.getparent().remove(parent) 
                            
                            #globals
                            match= re.findall('Values\[{}\]'.format(j),l.attrib['value'])
                            if match !=[]:
                                parent=l.getparent()
                                parent.getparent().remove(parent) 
                                
                            #locals
                            if len( j.split('.'))==2:
                                r,v= j.split('.')
                                r=r[1:-1]
                                match= re.findall('Reactions\[{}\].*Parameter={},'.format(r,v),l.attrib['value'])
                                if match!=[]:
                                    parent=l.getparent()
                                    parent.getparent().remove(parent)
                tasks=childML.find('{http://www.copasi.org/static/schema}ListOfTasks')
                method= tasks[5][2]
                parent=method.getparent()
                parent.remove(method)
                parent.insert(2,method_element)
                
                #turn off the randomize start values button (also turns off the corresponding for optimization task!)
                q='//*[@name="Randomize Start Values"]'
                for k in childML.xpath(q):
                    k.attrib['value']=str(0)
        
                C.write_copasi_file(self.cps_dct[i][j],childML)
        return self.cps_dct
        
    def setup_report(self):
        for i in self.cps_dct:
            for j in self.cps_dct[i]:
                st=Misc.RemoveNonAscii(j).filter
                pycopi.Reports(self.cps_dct[i][j],ReportType='profilelikelihood',
                               ReportName=st+'.txt',Save='overwrite',Variable=j)
        return self.cps_dct
        
    def setup_scan(self):
        for i in self.cps_dct:
            for j in self.cps_dct[i]:
                GMQ_child=pycopi.GetModelQuantities(self.cps_dct[i][j])
                if self.kwargs.get('QuantityType')=='concentration':
                    try:
                        variable_value= GMQ_child.get_all_model_variables()[j]['concentration'] 
                    except KeyError:
                        variable_value= GMQ_child.get_all_model_variables()[j]['value'] 
                elif self.kwargs.get('QuantityType')=='particle_number':
                    variable_value= GMQ_child.get_all_model_variables()[j]['value']  
                lb=float(variable_value)/float(self.kwargs.get('LowerBoundMultiplier'))
                ub=float(variable_value)*float(self.kwargs.get('UpperBoundMultiplier'))
                
                pycopi.Scan(self.cps_dct[i][j],
                                     Variable=j,
                                     ReportName=Misc.RemoveNonAscii(j).filter+'.txt',
                                     ReportType='profilelikelihood',
                                     SubTask='parameter_estimation',
                                     ScanType='scan',
                                     OutputInSubtask='false',
                                     AdjustInitialConditions='false',
                                     NumberOfSteps=self.kwargs.get('NumberOfSteps'),
                                     Maximum=ub,
                                     Minimum=lb,
                                     Log=self.kwargs.get('Log'),
                                     Scheduled='true',
                                     Save='overwrite',
                                     ClearScans='true')
        return self.cps_dct
        
    def run_slow(self):
        '''
        Run using one process, separately, one after another
        '''
        res={}
        for i in self.cps_dct.keys():
            for j in self.cps_dct[i]:
#                args=['CopasiSE',self.cps_dct[i][j]]
                if self.kwargs.get('Verbose')=='true':
                    print 'running {}'.format(j)
                res[self.cps_dct[i][j]]= pycopi.Run(self.cps_dct[i][j],Task='scan',MaxTime=self.kwargs.get('MaxTime'),Mode='slow').run()
        return res

#    def run_fast(self):
#        '''
#        self.cps_dct is a nested dictionary dct[index1][index2]=filename
#        CopasiSE is a program for simulating mathematical models using the terminal/cmd
#        
#        '''
#        for i in self.cps_dct.keys():
#            for j in self.cps_dct[i]:
#                subprocess.Popen('CopasiSE {}'.format(self.cps_dct[i][j]))
#        return self.cps_dct
        
    def multi_run(self):
        def run(x):
            subprocess.Popen('CopasiSE "{}"'.format(x))
        if self.kwargs.get('NumProcesses')==0:
            return False
        else:
            pool=multiprocessing.Pool(self.kwargs.get('NumProcesses'))
            for i in self.cps_dct.keys():
                for j in self.cps_dct[i]:
                    p=[k.name() for k in psutil.process_iter()]
                    count= Counter(p)['CopasiSE.exe']
                    if count>self.kwargs.get('NumProcesses'):
                        sleep(self.kwargs.get('SleepTime'))
                    pool.Process(run(self.cps_dct[i][j]))
            return True
                
    def run_SGE(self):
        for i in self.cps_dct.keys():
            for j in self.cps_dct[i]:
                with open('run_script.sh','w') as f:
                    f.write('#!/bin/bash\n#$ -V -cwd\nmodule addapps/COPASI/4.16.104-Linux-64bit\nCopasiSE "{}"'.format(self.cps_dct[i][j]))
                os.system('qsub {}'.format('run_script.sh'))
                os.remove('run_script.sh')         
        return True
                
    def run(self):
        if self.kwargs.get('Run')=='false':
            return False
        elif self.kwargs.get('Run')=='multiprocess':
            self.multi_run()
            return True
        elif self.kwargs.get('Run')=='slow':
            self.run_slow()
            return True
        elif self.kwargs.get('Run')=='SGE':
            self.run_SGE()
            return True


#==============================================================================
            
class Plot():
    '''    
    After ProfileLikelihood class has been run, the Plot class will plot the
    profile likelihoods for you. 
    
    copasi_file:
        The copasi file you ran a profile likelihood on
        
    **kwargs:
    
        ParameterPath:
            When Index is anything other than -1 you need to specify the absolute
            path to your parameters. 
            
        Index:
            Which Index to plot. Either an integer or list of integers. Default=-1, 
            means profile likelihoods were calculated around the parameters present 
            in the model. When Index=-1 you must speficy an argument to the 
            RSS argument. An integer Index other than -1 specifies that a profile
            likleihood was calculated around the integer best set of parameters and 
            to plot them. A list of integers specifies the plotting of an 
            arbtrary number of profile likelihoods. When Index is an Int or list of Int
            the RSS argument is taken directly from the PE data specified by ParameterPath
            
        NumProcesses:
            How many processes to use for plotting, which can be fairly intensive 
            computationally. Default=1
            
        Alpha:
            The alpha cut off for the chi squared based confidence interval. 
            Default=0.95
            
        N:
            Number of data points in use. The data files that were used for 
            parameter estimation in the original copasi file (the argument to copasi_file)
            were extracted, parsed and data points were counted. This value is the default
            but can be over-ridden if value given to this argument.
            
        DOF:
            Degrees of freedom. The number of parameters that you want to calculate
            profile likelihoods for minus 1 is calcualted automatically. This is 
            default but can be overridden by specifying an argument to this keyword
            
        RSS:
            Residual Sum of Squared. The objective function used as a measure of distance
            of the experimental to simulated data. The RSS is minimized by copasi's 
            parameter estimation algorithms. The smaller the better. This value is 
            automatically taken from parameter estimation data if the Index kwarg 
            is anything other than minus 1. when Index=-1, the RSS value must be 
            given to this argument for the calculation of the chi squared based 
            confidence interval

        FontSize:
            Control graph label font size

        AxisSize:
            Control graph axis font size

        ExtraTitle:
            When savefig='true', given the saved
            file an extra label in the file path

        LineWidth:
            Control graph LineWidth
            
        DotSize:
            How big to plot the dots on the graph

        Bins:
            Control number of bins in any histograms. Used???

        MultiPlot:
            Plot results of sequential profile likelihoods for the same 
            parameter but with different Index on the same graph. Results
            accumulate with Index value, so desired graphs are in the
            folder with the largest index. 
            
        SaveFig:
            Save graphs to file labelled after the index

        InterpolationKind:
            Which method to use for interpolation. Can be any of ['linear', 
            'nearest', 'zero', 'slinear', 'quadratic', 'cubic'] but be careful
            with these. Default=slinear

        TitleWrapSize:
            When graph titles are long, how many characters to have per 
            line before word wrap. Default=30. 
            
        Show:
            When not using iPython, use Show='true' to display graphs
            
        InterpolationResolution;
            Number of points to split line into for interpolation. Defualt=1000
            
        Ylimit: 
            default==None, restrict amount of data shown on y axis. 
            Useful for honing in on small confidence intervals

        Xlimit: 
            default==None, restrict amount of data shown on x axis. 
            Useful for honing in on small confidence intervals
        
        DPI:
            How big saved figure should be. Default=125
        
        XTickRotation:
            How many degrees to rotate the X tick labels
            of the output. Useful if you have very small or large
            numbers that overlay when plotting. 
            
        Mode: 
            either 'all', 'one' or 'none to either plot all results 
            or just a certain parameter. Defulat='all'
            
        PlotIndex:
            if Mode set to 'one', this specifies the index of the 
            profile likelihood run you want to plot (i.e -1,0,[0,3,5])
            
        PlotParameter:
            If Mode set to 'one' which parameter to plot. Must
            be an item in your results. 
            
        Separator:
            Separator used in csv file for experimental data. 
            Default='\t'
            
        Log10:
            'true' or 'false'. Default='true'. Plot on log10-log10 scale
            
        UsePickle:
            Data read by PEAnalysis.ParsePEData are automatically pickled
            for speed. 'true' or 'false' to use pickle. Default='false'
        
        OverwritePickle:
            If data has changed set 'OverwritePickle' to 'true' to rewrite 
            pickle before 'UsePickle' can be useful again. Default='false'
        
    '''

    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=pycopi.CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML
        self.GMQ=pycopi.GetModelQuantities(self.copasi_file)
        os.chdir(os.path.dirname(self.copasi_file))

        options={#report variables
                 'ParameterPath':None,                 
                 'Index':-1,
                 'NumProcesses':1, 
                 'Alpha':0.95,
                 'DOF':None,
                 'N':None,
                 'RSS':None,
                 'QuantityType':'concentration',
                 
                 #graph features
                 'FontSize':22,
                 'AxisSize':15,
                 'ExtraTitle':None,
                 'LineWidth':3,
                 'Bins':100,
                 'Show':'false',
                 'MultiPlot':'false',
                 'SaveFig':'false',
                 'InterpolationKind':'slinear',
                 'InterpolationResolution':1000,
                 'TitleWrapSize':30,
                 'Ylimit':None,
                 'Xlimit':None,
                 'DPI':125,
                 'XTickRotation':35,
                 'Mode':'all',
                 'PlotIndex':-1,
                 'PlotParameter':None,
                 'DotSize':4,
                 'Separator':'\t',
                 'Log10':'true',
                 
                 'UsePickle':'false',
                 'OverwritePickle':'false',
                 }
                 
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for Plot'.format(i)
        options.update( kwargs) 
        self.kwargs=options       
    
        assert isinstance(self.kwargs.get('NumProcesses'),int)
        if self.kwargs.get('NumProcesses')!=0:
            self.kwargs['NumProcesses']=self.kwargs.get('NumProcesses')-1

        if self.kwargs.get('Log10') not in ['true','false']:
            raise Errors.InputError('Log10 argument should be \'true\' or \'false\' not {}'.format(self.kwargs.get('Log10')))

        if self.kwargs.get('UsePickle') not in ['true','false']:
            raise Errors.InputError('UsePickle argument should be \'true\' or \'false\' not {}'.format(self.kwargs.get('Log10')))


        if self.kwargs.get('OverwritePickle') not in ['true','false']:
            raise Errors.InputError('OverwritePickle argument should be \'true\' or \'false\' not {}'.format(self.kwargs.get('Log10')))

            
            
        if self.kwargs.get('NumProcesses')>multiprocessing.cpu_count():
            raise Errors.InputError('You have selected {} processes but your computer only has {} available'.format(self.kwargs.get('NumProcesses'),multiprocessing.cpu_count()))
        
        #if Index is -1 i.e. current parameters, user needs to give RSS
        if self.kwargs.get('Index')==-1:
            if self.kwargs.get('RSS')==None:
                raise Errors.InputError('when calculating PL around current parameter sets must specify the current RSS as keyword argument to Plot')
        
        #otherwise the RSS is ascertained automatically from the ParameterPath
        if self.kwargs.get('Index')!=-1:
            assert self.kwargs.get('ParameterPath')!=None,'If Index!=-1 then you need to suply argument to ParameterPath'
        

        #line interpolation options
        assert self.kwargs.get('InterpolationKind') in ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic'],"interpolation kind must be one of ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic']"

        #limit parameters
        if self.kwargs.get('Ylimit')!=None:
            assert isinstance(self.kwargs.get('Ylimit'),list),'Ylimit is a list of coordinates for y axis,i.e. [0,10]'
            assert len(self.kwargs.get('Ylimit'))==2,'length of the Ylimit list must be 2'
        
        if self.kwargs.get('Xlimit')!=None:
            assert isinstance(self.kwargs.get('Xlimit'),list),'Xlimit is a list of coordinates for X axis,i.e. [0,10]'
            assert len(self.kwargs.get('Xlimit'))==2,'length of the Xlimit list must be 2'
        
        if isinstance(self.kwargs.get('XTickRotation'),int)!=True:
            raise TypeError('XTickRotation parameter should be a Python integer')

        
        if self.kwargs.get('ExtraTitle')!=None:
            if isinstance(self.kwargs.get('ExtraTitle'),str)!=True:
                raise TypeError('ExtraTitle should be of type str')
                
        if isinstance(self.kwargs.get('FontSize'),int)!=True:
            raise TypeError('FontSize argument should be of type int')
            
        if isinstance(self.kwargs.get('AxisSize'),int)!=True:
            raise TypeError('AxisSize argument should be of type int')
            
        if isinstance(self.kwargs.get('LineWidth'),int)!=True:
            raise TypeError('LineWidth argument should be of type int')
            
        if isinstance(self.kwargs.get('InterpolationKind'),str)!=True:
            raise TypeError('InterpolationKind argument should be of type str')
            
        if isinstance(self.kwargs.get('InterpolationResolution'),int)!=True:
            raise TypeError('InterpolationResolution argument should be of type int')

        if isinstance(self.kwargs.get('TitleWrapSize'),int)!=True:
            raise TypeError('TitleWrapSize argument should be of type int')


        if isinstance(self.kwargs.get('InterpolationResolution'),int)!=True:
            raise TypeError('InterpolationResolution argument should be of type int')

            
            


        if self.kwargs.get('Ylimit')!=None:
            assert isinstance(self.kwargs.get('Ylimit'),str)
            
        if self.kwargs.get('Xlimit')!=None:
            assert isinstance(self.kwargs.get('Xlimit'),str)
            
            
        assert isinstance(self.kwargs.get('DPI'),int)
        assert isinstance(self.kwargs.get('XTickRotation'),int)
    
        assert self.kwargs.get('Show') in ['false','true']
        assert self.kwargs.get('SaveFig') in ['false','true']
        assert self.kwargs.get('MultiPlot') in ['false','true']
        assert self.kwargs.get('QuantityType') in ['concentration','partical_numbers']
        self.PL_dir=self.get_PL_dir()
        self.indices=self.get_index_dirs()
        self.result_paths=self.get_results()
        self.data=self.parse_results() 
        
        
        '''
        The below arguments rely on the above code. Do not change
        the ordering!
        
        '''
        #default DOF is num estimated parameters minus 1 but can be manually overrider by specifying DOF keyword
        if self.kwargs.get('DOF')==None:
            self.kwargs['DOF']=self.degrees_of_freedom()
        if self.kwargs.get('DOF')==None:
            raise Errors.InputError('Please specify argument to DOF keyword')
        
        #defult N is number of data points in your data set. 
        #This can be overridden by manually specifying N
        
        if self.kwargs.get('N')==None :
            self.kwargs['N']=self.num_data_points()
        assert self.kwargs.get('N')!=None        
        
        if self.kwargs.get('Mode') not in ['all','one','none']:
            raise Errors.InputError('{} is not a valid mode. Mode should be either all or one'.format(self.kwargs.get('Mode')))
#

  

        if self.kwargs.get('Mode')!='all':
            if self.kwargs.get('PlotParameter') not in self.list_parameters():
                raise Errors.InputError('{} is not a valid Parameter. Your parameters are: {}'.format(self.kwargs.get('PlotParameter'),self.list_parameters()))

            if isinstance(self.kwargs.get('Index'),int):
                if self.kwargs.get('PlotIndex') != self.kwargs.get('Index'):
                    raise Errors.InputError('{} is not an index in your Indices: {}'.format(self.kwargs.get('PlotIndex'),self.kwargs.get('Index')))
            
            elif isinstance(self.kwargs.get('Index'),list):
                if self.kwargs.get('PlotIndex') not in self.kwargs.get('Index'):
                    raise Errors.InputError('{} is not an index in your Indices: {}'.format(self.kwargs.get('PlotIndex'),self.kwargs.get('Index')))


        if self.kwargs.get('Mode')=='all':
            self.plot_all()
        elif self.kwargs.get('Mode')=='one':
            self.plot1(self.kwargs.get('PlotIndex'),self.kwargs.get('PlotParameter'))
            
        
        self.plot_chi2_CI()
        CI=self.calc_chi2_CI()
        for i in CI:
            print 'Confidence level for Index {} is {} or {} on a Log10 scale'.format(i,CI[i],numpy.log10(CI[i]))
            
    def get_PL_dir(self):
        '''
        Find the ProfleLikelihood directory within the same directory as copasi_file
        '''
        d=os.path.dirname(self.copasi_file)
        path= os.path.join(d,'ProfileLikelihood')
        assert os.path.isdir(path),'The current directory: {} \t does not contain a directory called ProfileLikelihood, have you used the ProfileLikelihood class with the Run option enabled?'.format(d)
        return path
        
    def get_index_dirs(self):
        '''
        Under the ProfileLikelihood folder are a list of folders named after
        the integer rank of best fit (.e. -1,0,1,2 ...)
        returns list of these directories
        '''
        dirs= os.listdir(self.PL_dir)
        dirs2= [os.path.join(self.PL_dir,i) for i in dirs]
        for i in dirs2:
            assert os.path.isdir(i)
        return dirs2
        
    def get_index_dirs_as_dict(self):
        '''
        returns dict[index]=directory to index
        '''
        d={}
        dirs= os.listdir(self.PL_dir)
        dirs2= [os.path.join(self.PL_dir,i) for i in dirs]
        for i in dirs2:
            assert os.path.isdir(i)
            split=os.path.split(i)[1]
            d[int(split)]=i
        return d
        
    def get_experiment_files_in_use(self):
        '''
        Need to exclude data files fromlist of parameters to plot
        '''
        query='//*[@name="File Name"]'
        l=[]
        for i in self.copasiML.xpath(query):
            l.append(i.attrib['value'])
        return l
        
        
    def get_results(self):
        d={}
        for i in  self.indices:
            os.chdir(i)
            d[int(os.path.split(i)[1])]={}
            for j in glob.glob('*.txt'):
#                if os.path.splitext(j)[0]  in [Misc.RemoveNonAscii(i).filter for i in self.GMQ.get_fit_items().keys()]:
                    f,ext=os.path.splitext(j)
                    d[int(os.path.split(i)[1])][f]=os.path.join(i,j)
        return d
        
    def parse_results(self):
        df_dict={}
        experiment_keys= [os.path.splitext(i)[0] for i in self.get_experiment_files_in_use()]
        for i in self.result_paths:
            df_dict[i]={}
            for j in self.result_paths[i]:
                if j not in experiment_keys:
                    data= pandas.read_csv(self.result_paths[i][j],sep=self.kwargs['Separator'])
                    best_value_str='TaskList[Parameter Estimation].(Problem)Parameter Estimation.Best Value'
                    data=data.rename(columns={best_value_str:'RSS'})
                    df_dict[i][j]=data
        return df_dict
#        
    def list_parameters(self):
        return sorted(self.GMQ.get_all_model_variables().keys())


    def num_estimated_params(self):
#        try:
        first_key= self.data.keys()[0]
        count= len( self.data[first_key].keys())
        return count
#        except AttributeError:
#            raise Errors.InputError('Index set to -1 and therefore a ParameterPath is not present to count data points. Specify an argument to N kwarg')
        
        
    def degrees_of_freedom(self):
        '''
        The number of parameters being estimated minus 1
        '''
#        try:
        return self.num_estimated_params()-1
#        except AttributeError:
#            raise Errors.InputError('Index set to -1 and therefore a ParameterPath is not present to count number of parameter. Specify an argument to DOF kwarg')
        
    def num_data_points(self):
        '''
        returns number of data points in your data files
        '''
        experimental_data= [pandas.read_csv(i,sep=self.kwargs['Separator']) for i in self.get_experiment_files_in_use()]
        l=[]        
        for i in experimental_data:
            l.append( i.shape[0]*(i.shape[1]-1))
        s= sum(l)
        if s==0:
            raise Errors.InputError('Number of data points cannot be 0. This is wrong')
        return s

    def get_RSS(self):
        RSS={}

        if self.kwargs.get('Index')==-1:
            assert self.kwargs.get('RSS')!=None
            RSS[-1]= self.kwargs.get('RSS')
            return RSS
        else:
            PED= PEAnalysis.ParsePEData(self.kwargs.get('ParameterPath'),
                                        UsePickle=self.kwargs['UsePickle'],
                                        OverwritePickle=self.kwargs['OverwritePickle'])
            if isinstance(self.kwargs.get('Index'),int):
                RSS[self.kwargs.get('Index')]=PED.data.iloc[self.kwargs.get('Index')]['RSS']
            elif isinstance(self.kwargs.get('Index'),list):
                for i in self.kwargs.get('Index'):
                    RSS[i]=PED.data.iloc[i]['RSS']
            return RSS
        
    def chi2_lookup_table(self,alpha):
        '''
        Looks at the cdf of a chi2 distribution at incriments of 
        0.1 between 0 and 100. 
        
        Returns the x axis value at which the alpha interval has been crossed, 
        i.e. gets the cut off point for chi2 dist with DOF and alpha . 
        '''
        nums= numpy.arange(0,100,0.1)
        table=zip(nums,scipy.stats.chi2.cdf(nums,self.kwargs.get('DOF')) )
        for i in table:
            if i[1]<=alpha:
                chi2_df_alpha=i[0]
        return chi2_df_alpha  
        
    def get_chi2_alpha(self):
        '''
        return the chi2 threshold for cut off point alpha and DOF degrees of freedom
        '''
        dct={}
        alphas=numpy.arange(0,1,0.01)
        for i in alphas:
            dct[round(i,3)]=self.chi2_lookup_table(i)
        return dct[self.kwargs.get('Alpha')]

    def plot_chi2_CI(self):
        
        '''
        Visualize where the alpha cut off is on the chi2 distribution
        '''
        x = numpy.linspace(scipy.stats.chi2.ppf(0.01, self.kwargs.get('DOF')),scipy.stats.chi2.ppf(0.99, self.kwargs.get('DOF')), 100)
        
        plt.figure()        
        plt.plot(x, scipy.stats.chi2.pdf(x, self.kwargs.get('DOF')),'k-', lw=self.kwargs.get('LineWidth'), label='chi2 pdf')
        
        y_alpha=numpy.linspace(plt.ylim()[0],plt.ylim()[1])
        x_alpha=[self.get_chi2_alpha()]*len(y_alpha)
        
        plt.plot(x_alpha,y_alpha,'--',linewidth=self.kwargs.get('LineWidth'))
        plt.xlabel('x',fontsize=self.kwargs.get('Fontsize'))
        plt.ylabel('Probability',fontsize=self.kwargs.get('Fontsize'))
        plt.title('Chi2 distribution with {} DOF'.format(self.kwargs.get('DOF')),fontsize=self.kwargs.get('Fontsize'))
        
        
    def calc_chi2_CI(self):
        '''
        get chi2 CI at alpha
        alpha=decimal between 0 and 1 with 2 decimal places 
        '''
        CI_dct={}
        for i in  self.get_RSS():
            r= self.get_RSS()[i]
            a=self.get_chi2_alpha()
            n=self.num_data_points()
            CI_dct[i]=r*math.exp((a/n))
        return CI_dct
        
        
    def get_original_value(self,index,parameter):
        '''
        go and find out what the value of the parameter was in the PE data 
        at index
        '''
        if parameter in self.GMQ.get_global_quantities():
            best_parameter_value=self.GMQ.get_global_quantities()[parameter]
        
        if parameter in self.GMQ.get_local_kinetic_parameters_cns():
            best_parameter_value= self.GMQ.get_local_kinetic_parameters_cns()[parameter]['value']
        
        if parameter in self.GMQ.get_IC_cns():
            if self.kwargs.get('QuantityType')=='concentration':
                best_parameter_value= self.GMQ.get_IC_cns()[parameter]['concentration']
            else:
                best_parameter_value= self.GMQ.get_IC_cns()[parameter]['value']





        
#            else:
#                best_parameter_value=self.GMQ.get_IC_cns()[parameter]['value']
            
#        if st in [Misc.RemoveNonAscii(i).filter for i in self.GMQ.get_IC_cns().keys()] or self.GMQ.get_IC_cns().keys():
#            if self.kwargs.get('QuantityType')=='concentration':
#                best_parameter_value=self.GMQ.get_IC_cns()[parameter]['concentration']
#            else:
#                best_parameter_value=self.GMQ.get_IC_cns()[parameter]['value']
#        if st in [Misc.RemoveNonAscii(i).filter for i in self.GMQ.get_local_kinetic_parameters_cns()] or self.GMQ.get_local_kinetic_parameters_cns().keys():
#            best_parameter_value=self.GMQ.get_local_kinetic_parameters_cns()[parameter]['value']
#
#        if st in [Misc.RemoveNonAscii(i).filter for i in self.GMQ.get_global_quantities()] or self.GMQ.get_global_quantities().keys():
#            best_parameter_value= self.GMQ.get_global_quantities()[parameter]
        try:
            return best_parameter_value
        except UnboundLocalError:
            best_parameter_value=None
            return best_parameter_value
            

    def plot1(self,index,parameter):
        '''
        Plot one parameter. 
        
        things to check:
            that we are plotting the correct data
            that the CI line is calculated correctly
            that the red dot is in the correct place
        '''
        matplotlib.pyplot.rcParams.update({'font.size':self.kwargs.get('AxisSize')})
#        if parameter not in self.GMQ.get_all_model_variables().keys():
#            raise Errors.InputError('{} is not in your model. These are parameters in your model: {}'.format(parameter,self.GMQ.get_all_model_variables().keys()))
        if self.kwargs.get('MultiPlot')=='true':
            plt.figure(parameter)
        else:
            plt.figure()
        ax = plt.subplot(111)
        if self.kwargs['Log10']=='true':
            data= numpy.log10(self.data[index][parameter])
        else:
            data= self.data[index][parameter]
        parameter_val,RSS_val=(data[data.keys()[0]],data[data.keys()[1]])
        #plot parameter vs RSS once as green circles the other as lines
        try:
            plt.plot(parameter_val,RSS_val,'bo',markersize=self.kwargs.get('DotSize'))
        except ValueError as e:
            if e.message=='invalid literal for float(): 1.#INF':
                return True
            
        #now get your interpolation on...
        f=interp1d(parameter_val,RSS_val,kind=self.kwargs.get('InterpolationKind'))
        interp_parameter_value=numpy.linspace(min(parameter_val),
                                              max(parameter_val), 
                                              num=self.kwargs.get('InterpolationResolution')*len(parameter_val), endpoint=True)
        interp_RSS_value=f(interp_parameter_value)        
        handle=plt.plot(interp_parameter_value,interp_RSS_value,'black')
        plt.setp(handle,'color','black',linewidth=self.kwargs.get('LineWidth'))
        
        #plot the confidence interval 
        if self.kwargs.get('Log10')=='true':
            CI= numpy.log10(self.calc_chi2_CI()[index])
        else:
            CI= self.calc_chi2_CI()[index]
        
        
        plt.plot(parameter_val,[CI]*len(parameter_val),'g--',linewidth=self.kwargs.get('LineWidth'))
#        print self.GMQ.get_all_model_variables()
#        print parameter
        st=Misc.RemoveNonAscii(parameter).filter
#        print st
        best_parameter_value=self.get_original_value(index,parameter)   
        if best_parameter_value!=None:         
            #best parameter value contains the model value for pparameter
            #we now need to look this value up on the interpolation and read off the corresponding RSS value
            #first find the parameter value in the interolation that is closest to the best param val
            pandas.set_option('precision',15)
            interp_df= pandas.DataFrame([interp_parameter_value,interp_RSS_value],index=[parameter,'RSS']).transpose()
            best_parameter_value=numpy.round(float(best_parameter_value),15)
            abs_diff_df= abs(interp_df-best_parameter_value)
            minimum_index= abs_diff_df.idxmin()[parameter]
            best_parameter_value= interp_df.iloc[minimum_index][parameter]
            best_RSS_value=interp_df.iloc[minimum_index]['RSS']
            plt.plot(best_parameter_value,best_RSS_value,'ro',markersize=self.kwargs.get('DotSize'))
        
        #plot labels
        plt.title('\n'.join(wrap('{}'.format(parameter),self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))
        
        
        if self.kwargs['Log10']=='true':
            plt.xlabel('Parameter Value (Log10)',fontsize=self.kwargs.get('FontSize'))  
            plt.ylabel('RSS (Log10)',fontsize=self.kwargs.get('FontSize'))
        else:
            plt.xlabel('Parameter Value',fontsize=self.kwargs.get('FontSize'))         
            plt.ylabel('RSS',fontsize=self.kwargs.get('FontSize'))
       #pretty stuff

        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        
        #xtick rotation
        plt.xticks(rotation=self.kwargs.get('XTickRotation'))
        
        #options for changing the plot axis
        if self.kwargs.get('Ylimit')!=None:
            ax.set_ylim(self.kwargs.get('Ylimit'))
        if self.kwargs.get('xlimit')!=None:
            ax.set_xlim(self.kwargs.get('xlimit'))

        def save_plot():
            filename={}
            if self.kwargs.get('ExtraTitle') !=None:
                filename[parameter]=os.path.join(os.getcwd(),parameter+'_'+self.kwargs.get('ExtraTitle')+'.png')
                plt.savefig(parameter+'_'+self.kwargs.get('ExtraTitle')+'.png',bbox_inches='tight',format='png',dpi=self.kwargs.get('DPI'))
            else:
                filename[parameter]=os.path.join(os.getcwd(),parameter+'.png')
                plt.savefig(parameter+'.png',format='png',bbox_inches='tight',dpi=self.kwargs.get('DPI'))     
            return filename

        if self.kwargs.get('Show')=='true':
            plt.show()
            
        #save figure options
        if self.kwargs.get('SaveFig')=='true':
            os.chdir(self.get_index_dirs_as_dict()[index])
            graph_dirs=save_plot()
            #change back to parent directory
            os.chdir(os.path.dirname(self.copasi_file))
            return graph_dirs
        else:
            return True
            
    def plot_all(self):
        if isinstance(self.kwargs.get('Index'),int)and self.kwargs.get('Index')==-1:
#            print self.data
            try:
                for i in self.data[-1]:
                    self.plot1(self.kwargs.get('Index'),i)
            except KeyError:
                raise Errors.InputError('Index out of bounds, i.e. Index>number PE runs')
#                
        if isinstance(self.kwargs.get('Index'),int) and self.kwargs.get('Index')!=-1:
            for i in self.data[self.kwargs.get('Index')]:
                self.plot1(self.kwargs.get('Index'),i)
#            except KeyError:
#                raise Errors.InputError('Index out of bounds, i.e. Index>number PE runs')
                
        elif isinstance(self.kwargs.get('Index'),list):
            for i in reversed(self.kwargs.get('Index')):
                for j in self.data[i]:
                    self.plot1(i,j)




        
#==============================================================================

        
if __name__=='__main__':
    f=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Tests\VilarModel2006pycopitestModel.cps'
    
    r=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Tests\vilarTimeCourse.txt'
    r2=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Tests\vilarTimeCourse2.txt'
        
    p=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Tests\output.txt'
    
    t=r'D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\Tests\cheese.txt'
 







