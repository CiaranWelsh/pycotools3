# -*- coding: utf-8 -*-
"""
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
 analysis and the plot class to calculate confidence intervals and visualize the
 results.


"""

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
    """
    This class uses the profile likelihood method of identifiability analysis
    to assess whether parameters can be uniquely determined with the defined
    optimization problem.

    copasi_file:
        The copasi file you wish to conduct a profile likelihood on

    **kwargs:
        parameter_path:
            The absolute path to either a parameter estimation results file
            ('.txt','.xlsx','.xls' or '.csv') or a folder of parameter
            estimation results files. Default=None

        index:
            The index of the parameter estimation run you want to calculate
            a profile likelihood around. Parameter estimations are ranked in
            order of best fit, with 0 being the best fit value from your set of
            estimations. Can be either an integer or list of integers to give
            the option of conducting multiple profile likelihoods using the same
            line of code. Use index=-1 if you want to calculate profile likelihood
            around parameters already in copasi. If index is not equal
            to -1 you must specificy a valid argument to the parameter_path
            keyword argument. Default is -1.


        save:
            One of, False,'overwrite' or 'duplicate'

        upper_bound_multiplier:
            Number of times above the current value of the parameter of interest
            to extend profile likleihood to. Default=1000

        lower_bound_multiplier:
            Number of times below the current value of the parameter of interest
            to extend profile likleihood to. Default=1000

        number_of_steps:
            How many times to sample between lower and upper boundaries. Default=10

        log10:
            Sample in log10 space. Default=False

        iteration_limit:
            Hook and Jeeves algorithm iteration limit parameter. Default=50

        tolerance:
            Hook and Jeeves algorithm tolerance parameter. Default=1e-5

        rho:
            Hook and Jeeves algorithm rho parameter. Default=0.2

        run:
            Either [False,'slow','multiprocess','SGE']. 'multiprocess'
            will use the number of processes specified in the NumProcesses
            keyword argument to work. This features doesn't work well yet and
            user is reccommended to use slow mode which runs each
            copasi file in serial. 'SGE' mode can be used specifically
            on a SunGridEngine managed cluster. Deault=False

    """
    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=pycopi.CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML
        self.GMQ=pycopi.GetModelQuantities(self.copasi_file)
        os.chdir(os.path.dirname(self.copasi_file))

        default_outputML=os.path.split(self.copasi_file)[1][:-4]+'_Duplicate.cps'
        options={#report variables
                 'save':'overwrite',
                 'index':-1,
                 'parameter_path':None,
                 'quantity_type':'concentration',
                 'upper_bound_multiplier':1000,
                 'lower_bound_multiplier':1000,
                 'number_of_steps':10,
                 'log10':True,
                 'iteration_limit':50,
                 'tolerance':1e-5,
                 'rho':0.2,
                 'run':False,
                 'Verbose':True,
                 'max_time':None,
                 'results_directory':None}
                 

        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for ProfileLikelihood'.format(i)
        options.update( kwargs) 
        self.kwargs=options    
        
        if self.kwargs.get('index')!=-1:
            assert self.kwargs.get('parameter_path')!=None,'If you specify an index, you need to specify an argument to parameter_path'
        
        #if no index or parameter_path specified, use current parameteres in cps
        self.mode='current'
        if self.kwargs.get('parameter_path')!=None:
            #if parameter path is file or folder set the self.mode variablee accordingly
            if os.path.exists(self.kwargs.get('parameter_path')):
                self.mode='file'
        
        #if parameter_path specified without an index, set index to 0 (i.e. best parameter set)
#        if self.kwargs.get('parameter_path')!=None and self.kwargs.get('index') !=-1 and self.kwargs.get('index')!=None:
#            self.kwargs['index']=98
        self.PE_data=self.read_PE_data()
        if self.kwargs.get('max_time')!=None:
            if isinstance(self.kwargs.get('max_time'),(float,int))!=True:
                raise Errors.InputError('max_time argument should be float or int')
        
        if self.kwargs.get('index') !=None:
            assert isinstance(self.kwargs.get('index'),(list,int)),'index must be an integer or a list of integers'
        if isinstance(self.kwargs.get('index'),list):
            for i in self.kwargs.get('index'):
                assert isinstance(i,int),'index is int type'
                try:
                    assert i<=self.PE_data.shape[0],'PE data contains {} parameter estimations. You have indicated that you want to use run {}'.format(self.PE_data.shape[0],i)
                except AttributeError:
                    raise Errors.Errors.InputError('No data')
        elif isinstance(self.kwargs.get('index'),list):
            assert self.kwargs.get('index')<=self.PE_data.shape[0],'PE data contains {} parameter estimations. You have indicated that you want to use run {}'.format(self.PE_data.shape[0],self.kwargs.get('index'))

        if self.GMQ.get_fit_items()=={}:
            raise Errors.InputError('Your copasi file doesnt have a parameter estimation defined')
        #convert some numeric input variables to string
        self.kwargs['upper_bound_multiplier']=str(self.kwargs['upper_bound_multiplier'])
        self.kwargs['lower_bound_multiplier']=str(self.kwargs['lower_bound_multiplier'])
        self.kwargs['number_of_steps']=str(self.kwargs['number_of_steps'])
        self.kwargs['iteration_limit']=str(self.kwargs['iteration_limit'])
        self.kwargs['tolerance']=str(self.kwargs['tolerance'])
        self.kwargs['rho']=str(self.kwargs['rho'])
        
        if self.kwargs.get('run') not in [False,'slow','multiprocess','SGE']:
            raise Errors.InputError('\'run\' keyword must be one of \'slow\', \'false\',\'multiprocess\', or \'SGE\'')

        assert self.kwargs.get('quantity_type') in ['concentration','particle_number']

        
        assert self.kwargs.get('log10') in [False,True]

        self.cps_dct=self.copy_copasi_files_and_insert_parameters()
        self.copy_data_files()
        self.cps_dct= self.setup_report()
        self.cps_dct=self.setup_scan()
        self.cps_dct=self.setup_PE_task()        
        self.save()
        os.chdir(os.path.dirname(self.copasi_file))
        self.run()

    def save(self):
        self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        
    def save_dep(self):
        if self.kwargs.get('save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('save')=='overwrite':
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
            return PEAnalysis.ParsePEData(self.kwargs.get('parameter_path')).data

    def copy_copasi_files_and_insert_parameters(self):
        '''
        Its easier to do these two functions together
        1) create relevant folders and copy copasi file into these based on the index parameter
        '''
        cps_dct={}
        estimated_parameters= self.GMQ.get_fit_items().keys()
        IA_dir=os.path.join(os.path.dirname(self.copasi_file),'ProfileLikelihood')
        if os.path.isdir(IA_dir)==False:
            os.mkdir(IA_dir)
        os.chdir(IA_dir)
        if self.kwargs.get('index')==-1:
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
            return cps_dct
            
        elif isinstance(self.kwargs.get('index'),int):
            assert self.kwargs.get('index')!=-1
            IP=pycopi.InsertParameters(self.copasi_file,
                                          index=self.kwargs.get('index'),
                                          quantity_type=self.kwargs.get('quantity_type'),
                                          df=self.PE_data,save='overwrite')
            IA_dir=os.path.join(IA_dir,str(self.kwargs.get('index')))
            cps_dct[self.kwargs.get('index')]={}
            if os.path.isdir(IA_dir)==False:
                os.mkdir(IA_dir)
            os.chdir(IA_dir)
            for i in estimated_parameters:
                st=Misc.RemoveNonAscii(i).filter
                filename=os.path.join(IA_dir,'{}.cps'.format(st))
                cps_dct[self.kwargs.get('index')][i]=filename
                if os.path.isfile(filename)==True:
                    os.remove(filename)
                copyfile(self.copasi_file,filename)
            os.chdir('..')
            os.chdir('..')
            return cps_dct
            
        elif isinstance(self.kwargs.get('index'),list):
            for i in self.kwargs.get('index'):
                IP=pycopi.InsertParameters(self.copasi_file,
                                          index=i,
                                          quantity_type=self.kwargs.get('quantity_type'),df=self.PE_data,save='overwrite')

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
        if self.kwargs['result_directory'] == None:
            self.IA_dir=os.path.join(os.path.dirname(self.copasi_file),'ProfileLikelihoods')
        if os.path.abspath(self.kwargs['results_directory'])!=True:
            self.IA_dir = os.path.join(os.path.dirname(self.copasi_file),self.kwargs['results_directory'])
        else:
            self.IA_dir = self.kwargs['results_directory']
        q='//*[@name="File Name"]'
        data_file_dct={}
#        print self.copasi_file
        for i in self.copasiML.xpath(q):
            data_path= os.path.join(os.path.dirname(self.copasi_file),i.attrib['value'])
            data_file_dct[i.attrib['value']]=data_path
            if self.kwargs.get('index')==-1:
                IA_dir1=os.path.join(self.IA_dir,'-1')
                new_data_file1=os.path.join(IA_dir1,i.attrib['value'])
                copyfile(data_path,new_data_file1)
                
            elif isinstance(self.kwargs.get('index'),int):
                IA_dir2=os.path.join(self.IA_dir,str(self.kwargs.get('index')))
                new_data_file2=os.path.join(IA_dir2,i.attrib['value'])
                copyfile(data_path,new_data_file2)
                
            elif isinstance(self.kwargs.get('index'),list):
                for j in self.kwargs.get('index'):
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
        iteration_limit={'type': 'unsignedInteger', 'name': 'Iteration Limit', 'value': self.kwargs.get('iteration_limit')}
        tolerance={'type': 'float', 'name': 'tolerance', 'value': self.kwargs.get('tolerance')}
        rho={'type': 'float', 'name': 'rho', 'value': self.kwargs.get('rho')}

        method_element=pycopi.etree.Element('method',attrib=method_params)
        pycopi.etree.SubElement(method_element,'Parameter',attrib=iteration_limit)
        pycopi.etree.SubElement(method_element,'Parameter',attrib=tolerance)
        pycopi.etree.SubElement(method_element,'Parameter',attrib=rho)
            
            
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
                pycopi.Reports(self.cps_dct[i][j],report_type='profilelikelihood',
                               report_name=st+'.txt',save='overwrite',variable=j)
        return self.cps_dct
        
    def setup_scan(self):
        for i in self.cps_dct:
            for j in self.cps_dct[i]:
                GMQ_child=pycopi.GetModelQuantities(self.cps_dct[i][j])
                if self.kwargs.get('quantity_type')=='concentration':
                    try:
                        variable_value= GMQ_child.get_all_model_variables()[j]['concentration'] 
                    except KeyError:
                        variable_value= GMQ_child.get_all_model_variables()[j]['value'] 
                elif self.kwargs.get('quantity_type')=='particle_number':
                    variable_value= GMQ_child.get_all_model_variables()[j]['value']  
                lb=float(variable_value)/float(self.kwargs.get('lower_bound_multiplier'))
                ub=float(variable_value)*float(self.kwargs.get('upper_bound_multiplier'))
                
                pycopi.Scan(self.cps_dct[i][j],
                                     variable=j,
                                     report_name=Misc.RemoveNonAscii(j).filter+'.txt',
                                     report_type='profilelikelihood',
                                     subtask='parameter_estimation',
                                     scan_type='scan',
                                     output_in_subtask=False,
                                     adjust_initial_conditions=False,
                                     number_of_steps=self.kwargs.get('number_of_steps'),
                                     maximum=ub,
                                     minimum=lb,
                                     log10=self.kwargs.get('log10'),
                                     scheduled=True,
                                     save='overwrite',
                                     clear_scans=True)
        return self.cps_dct
        
    def run_slow(self):
        '''
        run using one process, separately, one after another
        '''
        res={}
        for i in self.cps_dct.keys():
            for j in self.cps_dct[i]:
                LOG.debug( 'running {}'.format(j))
                res[self.cps_dct[i][j]]= pycopi.Run(self.cps_dct[i][j],task='scan',max_time=self.kwargs.get('max_time'),mode='slow').run()
        return res
        
    def multi_run(self):
        def run(x):
            subprocess.Popen('CopasiSE "{}"'.format(x))
        if self.kwargs.get('NumProcesses')==0:
            return False
        else:
            pool=multiprocessing.Pool(self.kwargs.get('NumProcesses'))
            for i in self.cps_dct.keys():
                for j in self.cps_dct[i]:
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
        if self.kwargs.get('run')==False:
            return False
        elif self.kwargs.get('run')=='multiprocess':
            self.multi_run()
            return True
        elif self.kwargs.get('run')=='slow':
            self.run_slow()
            return True
        elif self.kwargs.get('run')=='SGE':
            self.run_SGE()
            return True


#==============================================================================
            
class Plot():
    '''    
    After ProfileLikelihood class has been run, the plot class will plot the
    profile likelihoods for you. 
    
    copasi_file:
        The copasi file you ran a profile likelihood on
        
    **kwargs:
    
        parameter_path:
            When index is anything other than -1 you need to specify the absolute
            path to your parameters. 
            
        index:
            Which index to plot. Either an integer or list of integers. Default=-1, 
            means profile likelihoods were calculated around the parameters present 
            in the model. When index=-1 you must speficy an argument to the 
            rss argument. An integer index other than -1 specifies that a profile
            likleihood was calculated around the integer best set of parameters and 
            to plot them. A list of integers specifies the plotting of an 
            arbtrary number of profile likelihoods. When index is an Int or list of Int
            the rss argument is taken directly from the PE data specified by parameter_path
            
        alpha:
            The alpha cut off for the chi squared based confidence interval. 
            Default=0.95
            
        n:
            Number of data points in use. The data files that were used for 
            parameter estimation in the original copasi file (the argument to copasi_file)
            were extracted, parsed and data points were counted. This value is the default
            but can be over-ridden if value given to this argument.
            
        dof:
            Degrees of freedom. The number of parameters that you want to calculate
            profile likelihoods for minus 1 is calcualted automatically. This is 
            default but can be overridden by specifying an argument to this keyword
            
        rss:
            Residual Sum of Squared. The objective function used as a measure of distance
            of the experimental to simulated data. The rss is minimized by copasi's 
            parameter estimation algorithms. The smaller the better. This value is 
            automatically taken from parameter estimation data if the index kwarg 
            is anything other than minus 1. when index=-1, the rss value must be 
            given to this argument for the calculation of the chi squared based 
            confidence interval

        font_size:
            Control graph label font size

        axis_size:
            Control graph axis font size

        extra_title:
            When savefig=True, given the saved
            file an extra label in the file path

        line_width:
            Control graph line_width
            
        marker_size:
            How big to plot the dots on the graph

        bins:
            Control number of bins in any histograms. Used???

        multiplot:
            plot results of sequential profile likelihoods for the same 
            parameter but with different index on the same graph. Results
            accumulate with index value, so desired graphs are in the
            folder with the largest index. 
            
        savefig:
            save graphs to file labelled after the index

        interpolation_kind:
            Which method to use for interpolation. Can be any of ['linear', 
            'nearest', 'zero', 'slinear', 'quadratic', 'cubic'] but be careful
            with these. Default=slinear

        title_wrap_size:
            When graph titles are long, how many characters to have per 
            line before word wrap. Default=30. 
            
        show:
            When not using iPython, use show=True to display graphs
            
        InterpolationResolution;
            Number of points to split line into for interpolation. Defualt=1000
            
        ylimit: 
            default==None, restrict amount of data shown on y axis. 
            Useful for honing in on small confidence intervals

        xlimit: 
            default==None, restrict amount of data shown on x axis. 
            Useful for honing in on small confidence intervals
        
        dpi:
            How big saved figure should be. Default=125
        
        xtick_rotation:
            How many degrees to rotate the x tick labels
            of the output. Useful if you have very small or large
            numbers that overlay when plotting. 
            
        mode: 
            either 'all', 'one' or 'none to either plot all results 
            or just a certain parameter. Defulat='all'
            
        plot_index:
            if mode set to 'one', this specifies the index of the 
            profile likelihood run you want to plot (i.e -1,0,[0,3,5])
            
        plot_parameter:
            If mode set to 'one' which parameter to plot. Must
            be an item in your results. 
            
        separator:
            separator used in csv file for experimental data. 
            Default='\t'
            
        log10:
            True or False. Default=True. plot on log10-log10 scale
            
        use_pickle:
            Data read by PEAnalysis.ParsePEData are automatically pickled
            for speed. True or False to use pickle. Default=False
        
        overwrite_pickle:
            If data has changed set 'overwrite_pickle' to True to rewrite 
            pickle before 'use_pickle' can be useful again. Default=False
        
    '''

    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=pycopi.CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML
        self.GMQ=pycopi.GetModelQuantities(self.copasi_file)
        os.chdir(os.path.dirname(self.copasi_file))

        options={#report variables
                 'experiment_files':None,
                 'parameter_path':None,                 
                 'index':-1,
                 'alpha':0.95,
                 'dof':None,
                 'n':None,
                 'rss':None,
                 'quantity_type':'concentration',
                 
                 #graph features
                 'font_size':22,
                 'axis_size':15,
                 'extra_title':None,
                 'line_width':3,
                 'bins':100,
                 'show':False,
                 'multiplot':False,
                 'savefig':False,
                 'interpolation_kind':'slinear',
                 'InterpolationResolution':1000,
                 'title_wrap_size':30,
                 'ylimit':None,
                 'xlimit':None,
                 'dpi':125,
                 'xtick_rotation':35,
                 'mode':'all',
                 'plot_index':-1,
                 'plot_parameter':None,
                 'marker_size':4,
                 'separator':'\t',
                 'log10':False,
                 'use_pickle':False,
                 'overwrite_pickle':False,
                 }
                 
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for plot'.format(i)
        options.update( kwargs) 
        self.kwargs=options       
        
        if self.kwargs['experiment_files']==None:
            self.kwargs['experiment_files']=self.get_experiment_files_in_use()
    
        if self.kwargs.get('log10') not in [True,False]:
            raise Errors.InputError('log10 argument should be \'true\' or \'false\' not {}'.format(self.kwargs.get('log10')))

        if self.kwargs.get('use_pickle') not in [True,False]:
            raise Errors.InputError('use_pickle argument should be \'true\' or \'false\' not {}'.format(self.kwargs.get('log10')))


        if self.kwargs.get('overwrite_pickle') not in [True,False]:
            raise Errors.InputError('overwrite_pickle argument should be \'true\' or \'false\' not {}'.format(self.kwargs.get('log10')))

            
        #if index is -1 i.e. current parameters, user needs to give rss
        if self.kwargs.get('index')==-1:
            if self.kwargs.get('rss')==None:
                raise Errors.InputError('when calculating PL around current parameter sets must specify the current rss as keyword argument to plot')
        
        #otherwise the rss is ascertained automatically from the parameter_path
        if self.kwargs.get('index')!=-1:
            assert self.kwargs.get('parameter_path')!=None,'If index!=-1 then you need to suply argument to parameter_path'
        

        #line interpolation options
        assert self.kwargs.get('interpolation_kind') in ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic'],"interpolation kind must be one of ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic']"

        #limit parameters
        if self.kwargs.get('ylimit')!=None:
            assert isinstance(self.kwargs.get('ylimit'),list),'ylimit is a list of coordinates for y axis,i.e. [0,10]'
            assert len(self.kwargs.get('ylimit'))==2,'length of the ylimit list must be 2'
        
        if self.kwargs.get('xlimit')!=None:
            assert isinstance(self.kwargs.get('xlimit'),list),'xlimit is a list of coordinates for x axis,i.e. [0,10]'
            assert len(self.kwargs.get('xlimit'))==2,'length of the xlimit list must be 2'
        
        if isinstance(self.kwargs.get('xtick_rotation'),int)!=True:
            raise TypeError('xtick_rotation parameter should be a Python integer')

        
        if self.kwargs.get('extra_title')!=None:
            if isinstance(self.kwargs.get('extra_title'),str)!=True:
                raise TypeError('extra_title should be of type str')
                
        if isinstance(self.kwargs.get('font_size'),int)!=True:
            raise TypeError('font_size argument should be of type int')
            
        if isinstance(self.kwargs.get('axis_size'),int)!=True:
            raise TypeError('axis_size argument should be of type int')
            
        if isinstance(self.kwargs.get('line_width'),int)!=True:
            raise TypeError('line_width argument should be of type int')
            
        if isinstance(self.kwargs.get('interpolation_kind'),str)!=True:
            raise TypeError('interpolation_kind argument should be of type str')
            
        if isinstance(self.kwargs.get('InterpolationResolution'),int)!=True:
            raise TypeError('InterpolationResolution argument should be of type int')

        if isinstance(self.kwargs.get('title_wrap_size'),int)!=True:
            raise TypeError('title_wrap_size argument should be of type int')


        if isinstance(self.kwargs.get('InterpolationResolution'),int)!=True:
            raise TypeError('InterpolationResolution argument should be of type int')

            
            


        if self.kwargs.get('ylimit')!=None:
            assert isinstance(self.kwargs.get('ylimit'),str)
            
        if self.kwargs.get('xlimit')!=None:
            assert isinstance(self.kwargs.get('xlimit'),str)
            
            
        assert isinstance(self.kwargs.get('dpi'),int)
        assert isinstance(self.kwargs.get('xtick_rotation'),int)
    
        assert self.kwargs.get('show') in [False,True]
        assert self.kwargs.get('savefig') in [False,True]
        assert self.kwargs.get('multiplot') in [False,True]
        assert self.kwargs.get('quantity_type') in ['concentration','partical_numbers']
        
        if self.kwargs['experiment_files']==None:
            LOG.critical('Experimental Files not None')
            self.kwargs['experiment_files']=self.get_experiment_files_in_use()
            
            
        self.PL_dir=self.get_PL_dir()
        self.indices=self.get_index_dirs()
        self.result_paths=self.get_results()
        self.data=self.parse_results() 
        
        
        '''
        The below arguments rely on the above code. Do not change
        the ordering!
        
        '''
        #default dof is num estimated parameters minus 1 but can be manually overrider by specifying dof keyword
        if self.kwargs.get('dof')==None:
            self.kwargs['dof']=self.degrees_of_freedom()
        if self.kwargs.get('dof')==None:
            raise Errors.InputError('Please specify argument to dof keyword')
        
        #defult n is number of data points in your data set. 
        #This can be overridden by manually specifying n
        
        if self.kwargs.get('n')==None :
            self.kwargs['n']=self.num_data_points()
        assert self.kwargs.get('n')!=None        
        
        if self.kwargs.get('mode') not in ['all','one','none']:
            raise Errors.InputError('{} is not a valid mode. mode should be either all or one'.format(self.kwargs.get('mode')))
#

  

        if self.kwargs.get('mode')!='all':
            if self.kwargs.get('plot_parameter') not in self.list_parameters():
                raise Errors.InputError('{} is not a valid Parameter. Your parameters are: {}'.format(self.kwargs.get('plot_parameter'),self.list_parameters()))

            if isinstance(self.kwargs.get('index'),int):
                if self.kwargs.get('plot_index') != self.kwargs.get('index'):
                    raise Errors.InputError('{} is not an index in your Indices: {}'.format(self.kwargs.get('plot_index'),self.kwargs.get('index')))
            
            elif isinstance(self.kwargs.get('index'),list):
                if self.kwargs.get('plot_index') not in self.kwargs.get('index'):
                    raise Errors.InputError('{} is not an index in your Indices: {}'.format(self.kwargs.get('plot_index'),self.kwargs.get('index')))


        if self.kwargs.get('mode')=='all':
            self.plot_all()
        elif self.kwargs.get('mode')=='one':
            self.plot1(self.kwargs.get('plot_index'),self.kwargs.get('plot_parameter'))
            
        
        self.plot_chi2_CI()
        CI=self.calc_chi2_CI()
        for i in CI:
            LOG.info( 'Confidence level for index {} is {} or {} on a log10 scale'.format(i,CI[i],numpy.log10(CI[i])))
            
    def get_PL_dir(self):
        '''
        Find the ProfleLikelihood directory within the same directory as copasi_file
        '''
        d=os.path.dirname(self.copasi_file)
        if self.kwargs['results_directory']==None:
            path= os.path.join(d,'ProfileLikelihood')
        if self.kwargs['results_directory']!=None:
            if os.path.abspath(self.kwargs['results_directory'])==False:
                path = os.path.join(os.path.dirname(self.copasi_file),self.kwargs['results_directory'])
            else:
                path = self.kwargs['results_directory']
            assert os.path.isdir(path),'The current directory: {} \t does not contain a directory called ProfileLikelihood, have you used the ProfileLikelihood class with the run option enabled?'.format(d)
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
            f=os.path.abspath(i.attrib['value'])
            if os.path.isfile(f)!=True:
                raise Errors.InputError('Experimental files in use cannot be automatically determined. Please give a list of experiment file paths to the experiment_files keyword'.format())
            l.append(os.path.abspath(i.attrib['value']))
        
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

        experiment_keys= [os.path.splitext(i)[0] for i in self.kwargs['experiment_files']]
        for i in self.result_paths:
            df_dict[i]={}
            for j in self.result_paths[i]:
                if j not in experiment_keys:
                    data= pandas.read_csv(self.result_paths[i][j],sep='\t')#self.kwargs['separator'])
                    best_value_str='TaskList[Parameter Estimation].(Problem)Parameter Estimation.Best Value'
                    data=data.rename(columns={best_value_str:'rss'})
#                    if self.kwargs['log10']==True:
#                        df_dict[i][j]=numpy.log10(data)
#                    else:
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
#            raise Errors.InputError('index set to -1 and therefore a parameter_path is not present to count data points. Specify an argument to n kwarg')
        
        
    def degrees_of_freedom(self):
        '''
        The number of parameters being estimated minus 1
        '''
#        try:
        return self.num_estimated_params()-1
#        except AttributeError:
#            raise Errors.InputError('index set to -1 and therefore a parameter_path is not present to count number of parameter. Specify an argument to dof kwarg')
        
    def num_data_points(self):
        '''
        returns number of data points in your data files
        '''
        experimental_data= [pandas.read_csv(i,sep=self.kwargs['separator']) for i in self.kwargs['experiment_files']]
        l=[]        
        for i in experimental_data:
            l.append( i.shape[0]*(i.shape[1]-1))
        s= sum(l)
        if s==0:
            raise Errors.InputError('Number of data points cannot be 0. This is wrong')
        return s

    def get_RSS(self):
        rss={}

        if self.kwargs.get('index')==-1:
            assert self.kwargs.get('rss')!=None
            rss[-1]= self.kwargs.get('rss')
            return rss
        else:
            PED= PEAnalysis.ParsePEData(self.kwargs.get('parameter_path'),
                                        use_pickle=self.kwargs['use_pickle'],
                                        overwrite_pickle=False)#self.kwargs['overwrite_pickle'])
            if isinstance(self.kwargs.get('index'),int):
                rss[self.kwargs.get('index')]=PED.data.iloc[self.kwargs.get('index')]['rss']
            elif isinstance(self.kwargs.get('index'),list):
                for i in self.kwargs.get('index'):
                    rss[i]=PED.data.iloc[i]['rss']
            return rss
        
    def chi2_lookup_table(self,alpha):
        '''
        Looks at the cdf of a chi2 distribution at incriments of 
        0.1 between 0 and 100. 
        
        Returns the x axis value at which the alpha interval has been crossed, 
        i.e. gets the cut off point for chi2 dist with dof and alpha . 
        '''
        nums= numpy.arange(0,100,0.1)
        table=zip(nums,scipy.stats.chi2.cdf(nums,self.kwargs.get('dof')) )
        for i in table:
            if i[1]<=alpha:
                chi2_df_alpha=i[0]
        return chi2_df_alpha  
        
    def get_chi2_alpha(self):
        '''
        return the chi2 threshold for cut off point alpha and dof degrees of freedom
        '''
        dct={}
        alphas=numpy.arange(0,1,0.01)
        for i in alphas:
            dct[round(i,3)]=self.chi2_lookup_table(i)
        return dct[self.kwargs.get('alpha')]

    def plot_chi2_CI(self):
        
        '''
        Visualize where the alpha cut off is on the chi2 distribution
        '''
        x = numpy.linspace(scipy.stats.chi2.ppf(0.01, self.kwargs.get('dof')),scipy.stats.chi2.ppf(0.99, self.kwargs.get('dof')), 100)
        
        plt.figure()        
        plt.plot(x, scipy.stats.chi2.pdf(x, self.kwargs.get('dof')),'k-', lw=self.kwargs.get('line_width'), label='chi2 pdf')
        
        y_alpha=numpy.linspace(plt.ylim()[0],plt.ylim()[1])
        x_alpha=[self.get_chi2_alpha()]*len(y_alpha)
        
        plt.plot(x_alpha,y_alpha,'--',linewidth=self.kwargs.get('line_width'))
        plt.xlabel('x',fontsize=self.kwargs.get('Fontsize'))
        plt.ylabel('Probability',fontsize=self.kwargs.get('Fontsize'))
        plt.title('Chi2 distribution with {} dof'.format(self.kwargs.get('dof')),fontsize=self.kwargs.get('Fontsize'))
        
        
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
            if self.kwargs.get('quantity_type')=='concentration':
                best_parameter_value= self.GMQ.get_IC_cns()[parameter]['concentration']
            else:
                best_parameter_value= self.GMQ.get_IC_cns()[parameter]['value']


        try:
            return best_parameter_value
        except UnboundLocalError:
            best_parameter_value=None
            return best_parameter_value
            

    def plot1(self,index,parameter):
        '''
        plot one parameter. 
        
        things to check:
            that we are plotting the correct data
            that the CI line is calculated correctly
            that the red dot is in the correct place
        '''
        matplotlib.pyplot.rcParams.update({'font.size':self.kwargs.get('AxisSize')})
        best_parameter_value=self.get_original_value(index,parameter)  
        LOG.debug('best parameter value is {}'.format(best_parameter_value))
        
        if best_parameter_value != None:
            if self.kwargs['Log10']==True:
                best_parameter_value = round(numpy.log10(float(best_parameter_value)),6)
                
                
        if self.kwargs.get('MultiPlot')==True:
            plt.figure(parameter)
        else:
            plt.figure()
        ax = plt.subplot(111)
        if self.kwargs['log10']==True:
            data= numpy.log10(self.data[index][parameter])
        else:
            data= self.data[index][parameter]
        parameter_val,RSS_val=(data[data.keys()[0]],data[data.keys()[1]])
        #plot parameter vs rss once as green circles the other as lines
        try:
            plt.plot(parameter_val,RSS_val,'bo',markersize=self.kwargs.get('marker_size'))
        except ValueError as e:
            if e.message=='invalid literal for float(): 1.#INF':
                return True

        #now get your interpolation on...
        f=interp1d(parameter_val,RSS_val,kind=self.kwargs.get('interpolation_kind'))
        interp_parameter_value=numpy.linspace(min(parameter_val),
                                              max(parameter_val), 
                                              num=self.kwargs.get('InterpolationResolution')*len(parameter_val), endpoint=True)
        interp_RSS_value=f(interp_parameter_value)        
        handle=plt.plot(interp_parameter_value,interp_RSS_value,'black')
        plt.setp(handle,'color','black',linewidth=self.kwargs.get('line_width'))
        
        #plot the confidence interval 
        if self.kwargs.get('log10')==True:
            CI= numpy.log10(self.calc_chi2_CI()[index])
        else:
            CI= self.calc_chi2_CI()[index]
        
        
        plt.plot(parameter_val,[CI]*len(parameter_val),'g--',linewidth=self.kwargs.get('line_width'))
#        print self.GMQ.get_all_model_variables()
#        print parameter
        st=Misc.RemoveNonAscii(parameter).filter
#        print st
        
        

        if best_parameter_value!=None:         
            #best parameter value contains the model value for pparameter
            #we now need to look this value up on the interpolation and read off the corresponding rss value
            #first find the parameter value in the interolation that is closest to the best param val
            pandas.set_option('precision',15)
            interp_df= pandas.DataFrame([interp_parameter_value,interp_RSS_value],index=[parameter,'rss']).transpose()
            best_parameter_value=numpy.round(float(best_parameter_value),15)
            abs_diff_df= abs(interp_df-best_parameter_value)
            minimum_index= abs_diff_df.idxmin()[parameter]
            best_parameter_value= interp_df.iloc[minimum_index][parameter]
            best_RSS_value=interp_df.iloc[minimum_index]['rss']
            plt.plot(best_parameter_value,best_RSS_value,'ro',markersize=self.kwargs.get('marker_size'))
        
        #plot labels
        plt.title('\n'.join(wrap('{},OriginalParameterValue={}'.format(parameter,best_parameter_value),self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))

        
        if self.kwargs['log10']==True:
            plt.xlabel('Parameter Value (log10)',fontsize=self.kwargs.get('font_size'))  
            plt.ylabel('rss (log10)',fontsize=self.kwargs.get('font_size'))
        else:
            plt.xlabel('Parameter Value',fontsize=self.kwargs.get('font_size'))         
            plt.ylabel('rss',fontsize=self.kwargs.get('font_size'))
       #pretty stuff

        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        
        #xtick rotation
        plt.xticks(rotation=self.kwargs.get('xtick_rotation'))
        
        ##legend
        plt.legend(loc='best')
        #options for changing the plot axis
        if self.kwargs.get('ylimit')!=None:
            ax.set_ylim(self.kwargs.get('ylimit'))
        if self.kwargs.get('xlimit')!=None:
            ax.set_xlim(self.kwargs.get('xlimit'))

        def save_plot():
            filename={}
            if self.kwargs.get('extra_title') !=None:
                filename[parameter]=os.path.join(os.getcwd(),parameter+'_'+self.kwargs.get('extra_title')+'.png')
                plt.savefig(parameter+'_'+self.kwargs.get('extra_title')+'.png',bbox_inches='tight',format='png',dpi=self.kwargs.get('dpi'))
            else:
                filename[parameter]=os.path.join(os.getcwd(),parameter+'.png')
                plt.savefig(parameter+'.png',format='png',bbox_inches='tight',dpi=self.kwargs.get('dpi'))     
            return filename

        if self.kwargs.get('show')==True:
            plt.show()
            
        #save figure options
        if self.kwargs.get('savefig')==True:
            os.chdir(self.get_index_dirs_as_dict()[index])
            graph_dirs=save_plot()
            #change back to parent directory
            os.chdir(os.path.dirname(self.copasi_file))
            return graph_dirs
        else:
            return True
            
    def plot_all(self):
        if isinstance(self.kwargs.get('index'),int)and self.kwargs.get('index')==-1:
#            print self.data
            try:
                for i in self.data[-1]:
                    self.plot1(self.kwargs.get('index'),i)
            except KeyError:
                raise Errors.InputError('index out of bounds, i.e. index>number PE runs')
#                
        if isinstance(self.kwargs.get('index'),int) and self.kwargs.get('index')!=-1:
            for i in self.data[self.kwargs.get('index')]:
                self.plot1(self.kwargs.get('index'),i)
#            except KeyError:
#                raise Errors.InputError('index out of bounds, i.e. index>number PE runs')
                
        elif isinstance(self.kwargs.get('index'),list):
            for i in reversed(self.kwargs.get('index')):
                for j in self.data[i]:
                    self.plot1(i,j)




        
#==============================================================================

        
if __name__=='__main__':
    pass
