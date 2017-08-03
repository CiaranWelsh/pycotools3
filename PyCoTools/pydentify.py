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

import os
import re
import pandas
import numpy
import numpy as np
import scipy
import scipy.stats
import pycopi,Errors, PEAnalysis,Misc
import glob
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import logging
import seaborn
import pickle
import difflib
from shutil import copyfile
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

        default_results_directory = os.path.join(os.path.dirname(self.copasi_file),'ProfileLikelihood')
        default_pickle_path = os.path.join(os.path.dirname(self.copasi_file),'ProfileLikelihoodPickle.pickle')
        options={#report variables
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
                 'results_directory':default_results_directory, 
                 'pickle_path': default_pickle_path}
                 

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
#        print self.PE_data
#        
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
#
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
        
        ## write pickle
        self.write_pickle()
        self.run()

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]

    def __setitem__(self,key,value):
        self.kwargs[key] = value
        
    def write_pickle(self):
        with open(self['pickle_path'], 'w') as f:
            pickle.dump(self.cps_dct, f)
            
            
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

    def copy_copasi_files_and_insert_parameters(self,IA_dir=None):
        '''
        Its easier to do these two functions together
        1) create relevant folders and copy copasi file into these based on the index parameter
        '''
        cps_dct={}
        estimated_parameters= self.GMQ.get_fit_items().keys()
        IA_dir=self.kwargs['results_directory']
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
        self.IA_dir = self.kwargs['results_directory']
        q='//*[@name="File Name"]'
        data_file_dct={}
        for i in self.copasiML.xpath(q):
            data_path= os.path.join(os.path.dirname(self.copasi_file),i.attrib['value'])
            LOG.debug('Data path is: {}'.format( data_path))
            data_file_dct[i.attrib['value']]=data_path
            if self.kwargs.get('index')==-1:
                IA_dir1=os.path.join(self.IA_dir,'-1')
                new_data_file1=os.path.join(IA_dir1,i.attrib['value'])
                copyfile(data_path,new_data_file1)
                
            elif isinstance(self.kwargs.get('index'),int):
                IA_dir2=os.path.join(self.IA_dir,str(self.kwargs['index']))
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
        method_params={'name':"Hooke &amp; Jeeves", 'type':'HookeJeeves'}
        iteration_limit={'type': 'unsignedInteger', 'name': 'Iteration Limit', 'value': self.kwargs['iteration_limit']}
        tolerance={'type': 'float', 'name': 'Tolerance', 'value': self.kwargs['tolerance']}
        rho={'type': 'float', 'name': 'Rho', 'value': self.kwargs.get('rho')}

        method_element=pycopi.etree.Element('Method',attrib=method_params)
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
                pycopi.Reports(self.cps_dct[i][j],report_type='parameter_estimation',
                               report_name=st+'.txt',save='overwrite')
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
                                     report_name=os.path.join(os.path.dirname(self.cps_dct[i][j]), Misc.RemoveNonAscii(j).filter+'.txt' ),
                                     report_type='profilelikelihood2',
                                     subtask='parameter_estimation',
                                     scan_type='scan',
                                     output_in_subtask=True,
                                     adjust_initial_conditions=False,
                                     append = False,
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
                res[self.cps_dct[i][j]]= pycopi.Run(self.cps_dct[i][j],task='scan',mode='slow').run()
        return res
    
    def multi_run(self):
        
        def run(f):
            import pycopi
            LOG.info('Running {}'.format(f))
            pycopi.Run(f, task = 'scan', mode='multiprocess').run()
            
        from multiprocessing import Pool
        pool = Pool(processes=4)
        for index in self.cps_dct:
            result = pool.apply_async(run, (self.cps_dct[index].values(),))
            pool.close()
            pool.join()

    def run_SGE(self):
        '''
        run using one process, separately, one after another
        '''
        res={}
        for i in self.cps_dct.keys():
            for j in self.cps_dct[i]:
                LOG.debug( 'running {}'.format(j))
                res[self.cps_dct[i][j]]= pycopi.Run(self.cps_dct[i][j],
                   task='scan',mode='SGE').run()
        return res
    
    def run(self):
        if self['run']=='slow':
            self.run_slow()
        elif self['run']=='multiprocess':
            self.multi_run()
        elif self['run'] == 'SGE':
            self.run_SGE()

#==============================================================================
class FormatPLData():
    def __init__(self,copasi_file,report_name):
        self.copasi_file = copasi_file
        self.GMQ = pycopi.GetModelQuantities(self.copasi_file)
        self.report_name = report_name
        if os.path.isfile(self.report_name)!=True:
            raise Errors.InputError('file {} does not exist'.format(self.report_name))
            
        try:
            self.format = self.format_results()
        except IOError:
            raise Errors.FileIsEmptyError('{} is empty and therefore cannot be read by pandas. Make sure you have waited until there is data in the parameter estimation file before formatting parameter estimation output')
        
        
    def format_results(self):
        """
        Results come without headers - parse the results
        give them the proper headers then overwrite the file again
        :return:
        """
        try:
            data = pandas.read_csv(self.report_name, sep='\t', header=None, skiprows=[0])
        except pandas.parser.CParserError as e:
            raise Errors.InputError('Report {} caused Error --> {}'.format(self.report_name, e.message))
        except:
            raise Errors.InputError('File is empty. Check {}'.format(self.report_name))
        bracket_columns = data[data.columns[[1,-2]]]
        if bracket_columns.iloc[0].iloc[0] != '(':
            data = pandas.read_csv(self.report_name, sep='\t')

            LOG.info('Data already formatted. Skipping the formatting')
            return self.report_name
        else:
            data = data.drop(data.columns[[1,-2]], axis=1)
            data.columns = range(data.shape[1])
            LOG.debug('Shape of estimated parameters: {}'.format(data.shape))
            poe = os.path.split(self.copasi_file)[1][:-4]
            ### parameter of interest has been removed. 
            names = [poe]+self.GMQ.get_fit_item_order()+['RSS']
            data.columns = names
#            d,f = os.path.split(self.report_name)
#            new_report_name = os.path.join(d,f[:-4]+'_'+self.suffix+'.txt')
            data.to_csv(self.report_name, sep='\t', index=False)
            return self.report_name
    
    
    

        
class Plot2():
    """
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
            is anything other than minus 1x. when index=-1, the rss value must be 
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
            
        interpolation_resolution;
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
        
    """

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
                 'interpolation_resolution':1000,
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
                 'log10':True,
                 'use_pickle':False,
                 'overwrite_pickle':False,
                 'results_directory':None,
                 
                 
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
            
        if isinstance(self.kwargs.get('interpolation_resolution'),int)!=True:
            raise TypeError('interpolation_resolution argument should be of type int')

        if isinstance(self.kwargs.get('title_wrap_size'),int)!=True:
            raise TypeError('title_wrap_size argument should be of type int')


        if isinstance(self.kwargs.get('interpolation_resolution'),int)!=True:
            raise TypeError('interpolation_resolution argument should be of type int')

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
            
        self.PL_dir = self.get_PL_dir()
        self.indices = self.get_index_dirs()
        self.result_paths = self.get_results()
#        print self.result_paths
        self.format_pl_data()
        self.data = self.parse_results()
        if self['log10']:
            self.data = self.log10_transformation()
        
        
        '''
        The below arguments rely on the above code. Do not change
        the ordering!
        
        '''
        #default dof is num estimated parameters minus 1 but can be manually overrider by specifying dof keyword
        if self.kwargs.get('dof')==None:
            self.kwargs['dof']=self.degrees_of_freedom()
        if self.kwargs['dof']==None:
            raise Errors.InputError('Please specify argument to dof keyword')
            
        
        #defult n is number of data points in your data set. 
        #This can be overridden by manually specifying n
        
        if self.kwargs.get('n')==None :
            self.kwargs['n']=self.num_data_points()
        assert self.kwargs.get('n')!=None        

        if self.kwargs.get('mode') not in ['all','one',None]:
            raise Errors.InputError('{} is not a valid mode. mode should be either all or one'.format(self.kwargs.get('mode')))
            
            

        if self.kwargs.get('mode')=='one':
            if self['plot_parameter'] not in self.list_parameters():
                raise Errors.InputError('{} is not a valid Parameter. Your parameters are: {}'.format(self.kwargs.get('plot_parameter'),self.list_parameters()))

            if isinstance(self.kwargs.get('index'),int):
                if self.kwargs.get('plot_index') != self.kwargs.get('index'):
                    raise Errors.InputError('{} is not an index in your Indices: {}'.format(self.kwargs.get('plot_index'),self.kwargs.get('index')))
            
            elif isinstance(self.kwargs.get('index'),list):
                if self.kwargs.get('plot_index') not in self.kwargs.get('index'):
                    raise Errors.InputError('{} is not an index in your Indices: {}'.format(self.kwargs.get('plot_index'),self.kwargs.get('index')))


#        self.interpolate_data()
        if self.kwargs['mode']=='all':
            self.plot_all()
        elif self.kwargs['mode']=='one':
            self.plot1(self.kwargs['plot_index'],self.kwargs['plot_parameter'])
            
        
        self.plot_chi2_CI()
        CI=self.calc_chi2_CI()
        for i in CI:
            LOG.info( 'Confidence level for index {} is {} or {} on a log10 scale'.format(i,CI[i],numpy.log10(CI[i])))

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
            
        return self.kwargs[key]
    
    def __setitem__(self,key,value):
        self.kwargs[key] = value
        
        
    def log10_transformation(self):
        """
        Conevrt data to lo10 scale
        """
        res = {}
        for column in self.data:
            res[column] = {}
            for parameter in self.data[column ]:
                try:
                    res[column ][parameter] = numpy.log10(self.data[column ][parameter])
                except AttributeError:
                    LOG.critical('Cannot perform log10 transformation on string.\n{}'.format(self.data[column][parameter]))
        return res
    
    def format_pl_data(self):
        """
        
        """
        res = {}
        for i in self.result_paths:
            res[i] = {}
            for j in self.result_paths[i]:
                cps = self.result_paths[i][j][:-4]+'.cps'
                try:
                    res[i][j] = FormatPLData(cps, self.result_paths[i][j]).format
                except Errors.FileDoesNotExistError:
                    pass
        return res
            
    def trim_infinite_values(self):
        LOG.info('removing infinite values from PL data.')
        for index in self.data:
            for param in self.data[index]:
                self.data[index][param] = self.data[index][param].replace([numpy.inf, -numpy.inf], numpy.nan)
                self.data[index][param].dropna(how='any',inplace=True)    
        return self.data
            
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
        dirs = os.listdir(self.PL_dir)
        dirs = [os.path.join(self.PL_dir,i) for i in dirs]
        dirs = [i for i in dirs if os.path.isdir(i)]
        for i in dirs:
            assert os.path.isdir(i)
        return dirs
        
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
                f,ext=os.path.splitext(j)
                d[int(os.path.split(i)[1])][f]=os.path.join(i,j)
        return d


        
    def parse_results(self):
        df_dict={}
        experiment_files= [os.path.split(i)[1] for i in self.kwargs['experiment_files'] ]
        experiment_files = list(set(experiment_files))
        LOG.debug('These are experiment keys: {}'.format(experiment_files))
        for index in self.result_paths:
            df_dict[index]={}
            for param in self.result_paths[index]:
                if os.path.split( self.result_paths[index][param])[1] not in experiment_files:
                    data= pandas.read_csv(self.result_paths[index][param],sep='\t')#self.kwargs['separator'])
                    df_dict[index][param]=data
        return df_dict
        
#    def remove_experimental_files(self):
#        '''
#        Remove experimental data files from list of fiels to plot
#        '''
#        df_dict={}
#
#        experiment_keys= [os.path.splitext(i)[0] for i in self.kwargs['experiment_files']]
#        experiment_keys = list(set(experiment_keys))
#        LOG.debug('These are experiment keys: {}'.format(experiment_keys))
#        for i in self.result_paths:
#            df_dict[i]={}
#            for j in self.result_paths[i]:
#                LOG.debug('result path j: {}'.format(self.result_paths[i][j]))
#                if self.result_paths[i][j] not in experiment_keys:
#                    data= pandas.read_csv(self.result_paths[i][j],sep='\t')#self.kwargs['separator'])
#                    best_value_str='TaskList[Parameter Estimation].(Problem)Parameter Estimation.Best Value'
#                    data=data.rename(columns={best_value_str:'rss'})
##                    if self.kwargs['log10']==True:
##                        df_dict[i][j]=numpy.log10(data)
##                    else:
#                    df_dict[i][j]=data
#        return df_dict
##        
    def list_parameters(self):
        return self.GMQ.get_fit_items().keys()
#        first_index = self.data.keys()[0]
#        return sorted(self.data[first_index].keys())


    def num_estimated_params(self):
        """
        
        """
        first_key= self.data.keys()[0]
        count= len( self.data[first_key].keys())
        return count
        
        
    def degrees_of_freedom(self):
        '''
        The number of parameters being estimated minus 1
        '''
        return self.num_estimated_params()-1
        
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
            PED= PEAnalysis.ParsePEData(self.kwargs.get('parameter_path'))
            if isinstance(self.kwargs.get('index'),int):
                rss[self['index']]=PED.data.iloc[self['index']['RSS']]
            elif isinstance(self.kwargs.get('index'),list):
                for i in self.kwargs.get('index'):
                    rss[i]=PED.data.iloc[i]['RSS']
            return rss
        
    def chi2_lookup_table(self,alpha):
        '''
        Looks at the cdf of a chi2 distribution at incriments of 
        0.1 between 0 and 100. 
        
        Returns the x axis value at which the alpha interval has been crossed, 
        i.e. gets the cut off point for chi2 dist with dof and alpha . 
        '''
        nums= numpy.arange(0,100,0.1)
        table=zip(nums,scipy.stats.chi2.cdf(nums,self.kwargs['dof']) )
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
        seaborn.set_context(context='poster', font_scale=3)

#        matplotlib.pyplot.rcParams.update({'font.size':self.kwargs.get('axis_size')})
        best_parameter_value=self.get_original_value(index,parameter)  
        LOG.debug('best parameter value is {}'.format(best_parameter_value))

        if best_parameter_value != None:
            if self.kwargs['log10']==True:
                best_parameter_value = round(numpy.log10(float(best_parameter_value)),6)
                
        try:
            data = self.data[index][parameter]
        except KeyError:
            parameter = parameter.replace(' ','_')
            data = self.data[index][parameter]
                
                
        if self.kwargs.get('multiplot')==True:
            plt.figure(parameter)
        else:
            plt.figure()
        ax = plt.subplot(111)
        if self.kwargs['log10']==True:
            LOG.debug('data before log10: {}'.format(data))
            data= numpy.log10(data)
        else:
            data= data
            
        data = data[data.columns[[0,-1]]]
            
            
            
        parameter_val,RSS_val=(data[data.keys()[0]],data[data.keys()[1]])
        #plot parameter vs rss once as green circles the other as lines
        try:
            plt.plot(parameter_val,RSS_val,'bo')#,markersize=self.kwargs.get('marker_size'))
        except ValueError as e:
            if e.message=='invalid literal for float(): 1.#INF':
                return True

        LOG.debug('Interpolation kind arg: {}'.format(self.kwargs['interpolation_kind']))
        LOG.debug('len parameter_val: {}'.format(len(parameter_val)))
        #now get your interpolation on...
        f=interp1d(parameter_val,RSS_val,kind=self.kwargs['interpolation_kind'])
        interp_parameter_value=numpy.linspace(min(parameter_val),
                                              max(parameter_val), 
                                              num=self.kwargs['interpolation_resolution']*len(parameter_val), endpoint=True)
        interp_RSS_value=f(interp_parameter_value)        
        handle=plt.plot(interp_parameter_value,interp_RSS_value,'black')
        plt.setp(handle,'color','black')#,linewidth=self.kwargs.get('line_width'))
        
        #plot the confidence interval 
        if self.kwargs.get('log10')==True:
            CI= numpy.log10(self.calc_chi2_CI()[index])
        else:
            CI= self.calc_chi2_CI()[index]
        
        
        plt.plot(parameter_val,[CI]*len(parameter_val),'g--')#,linewidth=self.kwargs.get('line_width'))
#        print self.GMQ.get_all_model_variables()
#        print parameter
        st=Misc.RemoveNonAscii(parameter).filter
#        print st
        
        print LOG.warning(best_parameter_value)

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
            plt.plot(best_parameter_value,best_RSS_value,'ro')#,markersize=self.kwargs.get('marker_size'))
        
        #plot labels
        if self.kwargs['log10']:
            plt.title('{}\nlog10({})'.format(parameter,best_parameter_value))
        else:
            plt.title('{}\n{}'.format(parameter,best_parameter_value))

        
        if self.kwargs['log10']==True:
            plt.xlabel('Parameter Value (log10)')#,fontsize=self.kwargs.get('font_size'))  
            plt.ylabel('RSS (log10)')#,fontsize=self.kwargs.get('font_size'))
        else:
            plt.xlabel('Parameter Value')#,fontsize=self.kwargs.get('font_size'))         
            plt.ylabel('RSS')#,fontsize=self.kwargs.get('font_size'))
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
        plt.legend(loc=(1,0))
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
            
        
#    def interpolate_data(self):
#        res = {}
#        for index in self.data:
#            res[index] = {}
#            for parameter in self.data[index]:
#                print self.data[index][parameter]
#                f=interp1d(self.data[index][parameter],RSS_val,kind=self.kwargs['interpolation_kind'])
#                interp_parameter_value=numpy.linspace(min(self.data[index][parameter]),
#                                              max(self.data[index][parameter]), 
#                                              num=self['interpolation_resolution']*len(min(self.data[index][parameter]),
#                                                      endpoint=True) )
#                res[index][parameter]=f(interp_parameter_value)        
#        return res
#                handle=plt.plot(interp_parameter_value,interp_RSS_value,'black')        
        
#    def plot1(self, index, parameter):
#        """
#        plot a single normal plot 
#        but optionally plot a fill plot for when
#        user has multiple indexes
#        """
#        print self.interpolate_data
#        print self.data[index][parameter]
#        print self.data[index][parameter]

    def plot_all(self):
        if isinstance(self.kwargs.get('index'),int)and self.kwargs.get('index')==-1:
            try:
                for i in self.data[-1]:
                    LOG.debug('Plot index: {}, plot parameter: {}'.format(-1,i))
                    self.plot1(self.kwargs['index'],i)
            except KeyError:
                raise Errors.InputError('index out of bounds, i.e. index>number PE runs')
                
        if isinstance(self.kwargs.get('index'),int) and self.kwargs.get('index')!=-1:
            for i in self.data[self.kwargs.get('index')]:
                self.plot1(self.kwargs.get('index'),i)
                
        elif isinstance(self.kwargs.get('index'),list):
            for i in reversed(self.kwargs.get('index')):
                for j in self.data[i]:
                    self.plot1(i,j)
                    
                    
                    

class ChiSquaredStatistics():
    def __init__(self, rss, dof, num_data_points, alpha, plot_chi2=False):
        self.alpha = alpha
        self.dof = dof
        self.rss = rss
        self.num_data_points = num_data_points
        self.CL = self.calc_chi2_CL()
        
        if plot_chi2:
            self.plot_chi2_CL()

    def chi2_lookup_table(self,alpha):
        '''
        Looks at the cdf of a chi2 distribution at incriments of 
        0.1 between 0 and 100. 
        
        Returns the x axis value at which the alpha interval has been crossed, 
        i.e. gets the cut off point for chi2 dist with dof and alpha . 
        '''
        nums= numpy.arange(0,100,0.1)
        table=zip(nums,scipy.stats.chi2.cdf(nums,self.dof) )
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
        return dct[self.alpha]

    def plot_chi2_CL(self):
        '''
        Visualize where the alpha cut off is on the chi2 distribution
        '''
        x = numpy.linspace(scipy.stats.chi2.ppf(0.01, self.dof),scipy.stats.chi2.ppf(0.99, self.dof), 100)
        
        plt.figure()        
        plt.plot(x, scipy.stats.chi2.pdf(x, self.dof),'k-', lw=4, label='chi2 pdf')
        
        y_alpha=numpy.linspace(plt.ylim()[0],plt.ylim()[1])
        x_alpha=[self.get_chi2_alpha()]*len(y_alpha)
        
        plt.plot(x_alpha,y_alpha,'--',linewidth=4)
        plt.xlabel('x',fontsize=22)
        plt.ylabel('Probability',fontsize=22)
        plt.title('Chi2 distribution with {} dof'.format(self.dof),fontsize=22)
        
        
    def calc_chi2_CL(self):
        '''
        '''
        return self.rss * math.exp(  (  self.get_chi2_alpha()/self.num_data_points  )  )
        
    
    
class Plot():
    def __init__(self,data, **kwargs):
        self.data = data

    
        options={'x':None,
                 'y': None,
                 'log10':True,
                 'estimator':numpy.mean,
                 'n_boot':10000, 
                 'ci_band_level':95, ## CI for estimator bootstrap
                 'err_style':'ci_band',
                 'savefig':False,
                 'results_directory':os.getcwd(),
                 'dpi':300,
                 'plot_cl':True,
                 'title':None,
                 'xlabel':None,
                 'ylabel':None,
                 'color_palette':'bright',
                 'legend_location':None,
                 }
        
        
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for plot'.format(i)
        options.update( kwargs) 
        self.kwargs=options  
        
        if isinstance(self.data, pandas.core.frame.DataFrame)!=True:
            raise Errors.InputError('{} should be a dataframe. Parse data with ParsePEData first.'.format(self.data))
        
        self.parameter_list = sorted(list(self.data.columns))
        
        if self['x'] == None:
            raise Errors.InputError('x cannot be None')
            
        if self['y'] == None:
            self['y'] = self.parameter_list
            
        if self['y'] == None:
            raise Errors.InputError('y cannot be None')
            
        if self['x'] not in self.parameter_list:
            raise Errors.InputError('{} not in {}'.format(self['x'], self.parameter_list))
            
        if isinstance(self['y'],str):
            if self['y'] not in self.parameter_list:
                raise Errors.InputError('{} not in {}'.format(self['y'], self.parameter_list))
        if isinstance(self['y'], list):
            for y_param  in self['y']:
                if y_param not in self.parameter_list:
                    raise Errors.InputError('{} not in {}'.format(y_param, self.parameter_list))
                
            
        
        n = list(set(self.data.index.get_level_values(0)))
        if self['title'] == None:
            self['title'] = 'Profile Likelihood for\n{} (Rank={})'.format(self['x'],n)
        
        self.data.rename(columns={'ParameterOfInterestValue':self['x']})
        
        self.plot()
        
        


    def __getitem__(self,key):
        if key not in self.kwargs:
            raise Errors.InputError('{} not in {}'.format(key, self.kwargs.keys()))
        return self.kwargs[key]
    
    def __setitem__(self,key, value):
        self.kwargs[key] = value

    
    def plot(self):
        """
        
        """
        if self['y'] == self['x']:
            LOG.warning( Errors.InputError('x parameter {} cannot equal y parameter {}. Plot function returned None'.format(self['x'],self['y']))  )
            return None
        
        for label, df in self.data.groupby(level=[2]):
            if label== self['x']:
                data = df[self['y']]
                if isinstance(data, pandas.core.frame.Series):
                    data = pandas.DataFrame(data)
                if isinstance(data, pandas.core.frame.DataFrame):
                    data = pandas.DataFrame(data.stack(), columns=['Value'])
        try:
            data.index = data.index.rename(['ParameterSetRank',
                                        'ConfidenceLevel',
                                        'ParameterOfInterest',
                                        'ParameterOfInterestValue',
                                        'YParameter'])
        except UnboundLocalError:
            return 1
        
        data = data.reset_index()
        if self['log10']:
            data['ConfidenceLevel'] = numpy.log10(data['ConfidenceLevel'])
            data['Value'] = numpy.log10(data['Value'])
            data['ParameterOfInterestValue'] = numpy.log10(data['ParameterOfInterestValue'])
            


        plt.figure()
        if self['plot_cl']:
            cl_data = data[['ParameterSetRank','ConfidenceLevel',
                        'ParameterOfInterestValue']]
            cl_data = cl_data.drop_duplicates()
            seaborn.tsplot(data=cl_data,
                           time='ParameterOfInterestValue',
                           value='ConfidenceLevel', 
                           unit='ParameterSetRank',
                           color='green',linestyle='--',
                           estimator=self['estimator'],
                           err_style=self['err_style'],
                           n_boot=self['n_boot'],
                           ci=self['ci_band_level'])

        seaborn.color_palette('husl',8)
        seaborn.tsplot(data=data, 
                       time='ParameterOfInterestValue',
                       value='Value',
                       condition='YParameter',
                       unit='ParameterSetRank',
                       estimator=self['estimator'],
                       err_style=self['err_style'],
                       n_boot=self['n_boot'],
                       ci=self['ci_band_level'],
                       color=seaborn.color_palette(self['color_palette'],len(self['y']))
                       )
        plt.title(self['title'])
        if self['ylabel']!=None:
            plt.ylabel(self['ylabel'])
        if self['xlabel']!=None:
            plt.xlabel(self['x_label'])
            
        if self['legend_location']!=None:
            plt.legend(loc=self['legend_location'])
            
        if self['savefig']:
            save_dir = os.path.join(self['results_directory'], 'ProfileLikelihood')
            if os.path.isdir(save_dir)!=True:
                os.mkdir(save_dir)
            os.chdir(save_dir)
            plt.savefig(os.path.join(save_dir, '{}Vs{}.jpeg'.format(self['x'],self['y'])  ),
                        dpi=self['dpi'], bbox_inches='tight')

    
    
    
class ParsePLData():
    """
    get data from file into an appropriate format
    1) ensure data is properly formatted with headers
    2) read data into a df. 
        index 1 = parameter set
        index 2 = parameter of interest 
        index 3 = best parameter value
        index 4 = parameter scan value
            data = matrix
    """
    def __init__(self,copasi_file, pl_directory,**kwargs):
        self.copasi_file=copasi_file
        self.pl_directory = pl_directory
        self.copasiML = pycopi.CopasiMLParser(self.copasi_file).copasiML

    
        options={'parameter_path':None,
                 'index':-1,
                 'rss':None,
                 'dof':None,
                 'num_data_points':None,
                 'experiment_files':None,
                 'alpha':0.95,
                 'log10':True,
                 }
        
        
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for plot'.format(i)
        options.update( kwargs) 
        self.kwargs=options  
        
        if self['parameter_path']==None:
            if self['rss']==None:
                raise Errors.InputError('If parameter_path equals None then rss must not equal None')
        if self['parameter_path']!=None:
            if self['index']==-1:
                raise Errors.InputError('An argument is given to parameter_path but index is -1 (for PL around current parameter set). Change the index parameter')

        
        if self['index']!=-1:
            if self['parameter_path']==None:
                raise Errors.InputError('If index is not -1 (i.e. current parameter set in model) then an argument to parameter_path needs to be specified')
             
        if self['experiment_files'] == None:
            self['experiment_files'] = self.get_experiment_files_in_use()

        self.index_dirs = self.get_index_dirs()
        
        self.pl_data_files = self.get_pl_data_files()
        self.pl_data_files = self.format_pl_data_files()
        self.data = self.parse_data()
        self.data = self.infer_parameter_of_interest()
        if self['dof'] == None:
            self['dof'] = self.get_dof()
            
        if self['num_data_points'] == None:
            self['num_data_points'] = self.get_num_data_points()
        
        if self['rss'] == None:
            self['rss'] = self.get_rss()
        

        self.data = self.get_confidence_level()
        self.data = self.data.drop('ParameterFile', axis=1)
        


    def __getitem__(self,key):
        if key not in self.kwargs:
            raise Errors.InputError('{} not in {}'.format(key, self.kwargs.keys()))
        return self.kwargs[key]
    
    def __setitem__(self,key, value):
        self.kwargs[key] = value
        
    
    def get_index_dirs(self):
        '''
        Under the ProfileLikelihood folder are a list of folders named after
        the integer rank of best fit (.e. -1,0,1,2 ...)
        returns list of these directories
        '''
        l = []
        for i in glob.glob(os.path.join(self.pl_directory,'*')):
            if os.path.isdir(i):
                dire, fle = os.path.split(i)
                try:
                    int(fle)
                    l.append(i)
                except ValueError:
                    LOG.warning('{} is not a number and therefore does not contain a profile likleihood analysis. It will be ignored')
                    continue
                if os.path.isdir(i)!=True:
                    raise Errors.FolderDoesNotExistError(i)
        return l
    
    
    def get_pl_data_files(self):
        """
        return all text files in 
        """
        res = {}
        for index_dir in self.index_dirs:
            i = os.path.split(index_dir)[1]
            try:
                int(i)
            except ValueError:
                raise Errors.InputError('Cannot convert {} to int. Check there are no extra files in your profile likelihood directory'.format(i) )
            res[int(i)] = {}
            for f in glob.glob(os.path.join(index_dir,'*.txt')):
                dire, fle = os.path.split(f)
                res[int(i)][fle] = f
        return res
            
    def format_pl_data_files(self):
        """
        
        """
        res = {}
        for i in self.pl_data_files:
            res[i] = {}
            for j in self.pl_data_files[i]:
                cps = self.pl_data_files[i][j][:-4]+'.cps'
                try:
                    res[i][j] = FormatPLData(cps, self.pl_data_files[i][j]).format
                except Errors.FileDoesNotExistError:
                    pass
        return res
        
    
    def parse_data(self):
        """
        
        """
        res = {}
        df_dct = {}
        for index in self.pl_data_files:
            res[index] = {}
            for data_file in self.pl_data_files[index]:
                df_temp = pandas.read_csv(self.pl_data_files[index][data_file], 
                                          sep='\t', index_col=0)
                res[index][data_file] = pandas.read_csv( self.pl_data_files[index][data_file], 
                   sep='\t',
                   index_col=0)
            df_dct[index] = pandas.concat(res[index])
        df = pandas.concat(df_dct)
        df.index = df.index.rename(['ParameterSetRank','ParameterFile','ParameterOfInterestValue'])
        return df

    def infer_parameter_of_interest(self):
        """
        """
        parameters = sorted(list(self.data.columns))
        filenames = sorted(list(set(self.data.index.get_level_values(1))))
#        print parameters, filenames
        zipped =  dict(zip(filenames, parameters))
        self.data = self.data.reset_index(level=1)
        l = []
        for i in self.data['ParameterFile']:
            l.append( zipped[i])
        self.data['ParameterOfInterest'] = l
        return self.data 
    

    
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
        
        
    def get_dof(self):
        '''
        The number of parameters being estimated minus 1
        '''
        GMQ = pycopi.GetModelQuantities(self.copasi_file)
        return len(GMQ.get_fit_items().keys())-1
#        return self.get_num_estimated_paraemters()-1
        
    def get_num_data_points(self):
        '''
        returns number of data points in your data files
        '''
        experimental_data= [pandas.read_csv(i,sep='\t') for i in self.kwargs['experiment_files']]
        l=[]        
        for i in experimental_data:
            l.append( i.shape[0]*(i.shape[1]-1))
        s= sum(l)
        if s==0:
            raise Errors.InputError('''Number of data points cannot be 0.
Experimental data is inferred from the parameter estimation task definition. 
It might be that copasi_file refers to a 'fresh' copy of the model.
Try redefining the same parameter estimation problem that you used in the profile likelihood, 
using the setup method but not running the parameter estimation before trying again.''')
        return s

    def get_rss(self):
        rss={}

        if self['index']==-1:
            assert self['rss']!=None
            rss[-1]= self['rss']
            return rss
        else:
            PED= PEAnalysis.ParsePEData(self['parameter_path'])
            if isinstance(self['index'],int):
                rss[self['index']]=PED.data.iloc[self['index']['RSS']]
            elif isinstance(self['index'],list):
                for i in self['index']:
                    rss[i]=PED.data.iloc[i]['RSS']
            return rss
        
    def get_confidence_level(self):
        """
        
        """
        CL_dct= {}
        for index in self['rss']:
            rss = self['rss'][index]
            CL_dct[index] =  ChiSquaredStatistics(rss, self['dof'], self['num_data_points'],
                                       self['alpha']).CL
                  
        ranks = list(self.data.index.get_level_values(0))
        CL_list = [CL_dct[i] for i in ranks]
        self.data['ConfidenceLevel'] = CL_list
        self.data = self.data.reset_index()
        self.data = self.data.set_index(['ParameterSetRank','ConfidenceLevel','ParameterOfInterest','ParameterOfInterestValue'])
        return self.data
    
    
    
    
    
    
    
#==============================================================================

        
if __name__=='__main__':
    pass
#    execfile('./PyCoToolsTutorial/Test/testing_kholodenko_manually.py')

