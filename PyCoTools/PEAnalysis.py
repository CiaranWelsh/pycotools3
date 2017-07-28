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




 Object:
 
 PEAnalysis provies a number of convenient classes for visualizing 
 and analysing parameter estimation data. The module can be used with 
 any PE data regardless of origin but has been developed with copasi in 
 mind. 
  


 $Author: Ciaran Welsh
 $Date: 12-09-2016 
 Time:  20:33


Features to include:
    PCA for dimensionality reduction of the PE data. Identify component with most variance 
    
    Create class for computing model selection criteria
        AIC/BIC
        
        
    I could begin giving my python classes things like iteration capabilities or
    getters...


'''
import string
import pandas 
import matplotlib.pyplot as plt
import scipy 
import os
import matplotlib
import itertools
import pycopi,Errors, Misc
import seaborn 
import logging
from subprocess import check_call,Popen
import glob
import numpy 
from textwrap import wrap
from sklearn.decomposition import PCA
LOG=logging.getLogger(__name__)

SEABORN_OPTIONS = {'context':'poster',
                   'font_scale':2}

seaborn.set_context(context=SEABORN_OPTIONS['context'], font_scale=SEABORN_OPTIONS['font_scale'])
    
class ParsePEData():
    '''
    parse parameter estimation data from file
    
    Args:
        results_path: 
            Absolute path to file or folder of files containing parameter
            estimation data. 
            
    kwargs:
        use_pickle:
            Allow one to overwrite the pickle file automatically
            produced for speed. Default=False
    '''
    def __init__(self,results_path, sep='\t', log10=False):
        self.results_path = results_path
        self.log10 = log10
        self.sep = sep

        if self.log10:
            self.data = numpy.log10(self._read_data())
        else:
            self.data = self._read_data()
        
        
        
    def _read_data(self):
        """
        
        """
        if os.path.isfile(self.results_path):
            return self.read_PE_data_file(self.results_path)
        elif os.path.isdir(self.results_path):
            return self.read_PE_data_folder()
        else:
            raise Errors.InputError('results_path argument should be a PE data file or folder of identically formed PE data files')

    
    def read_PE_data_file(self, path):
        """
        
        """
        ## check that the data has been formatted before entry into PEAnalysis module
        data = pandas.read_csv(path, sep='\t', header=None)
        for i in data.iloc[0]:
            if i=='(':
                raise Errors.InputError('Brackets are still in your data file. Ensure you\'ve properly formatted PE data using the format_results() method')
        return pandas.read_csv(path, sep=self.sep).sort_values(by='RSS').reset_index(drop=True)

    def read_PE_data_folder(self):
        """
        
        """
        ## check that the data has been formatted before entry into PEAnalysis module
        df_list = []
        for i in glob.glob(os.path.join(self.results_path,'*.txt')):
            df_list.append(self.read_PE_data_file(i))
            
        return pandas.concat(df_list).sort_values(by='RSS').reset_index(drop=True)
    
    

    
class Boxplot():
    def __init__(self, data, **kwargs):
        self.data = data
        
        options={'sep':'\t',
                 'log10':False,
                 'truncate_mode':'percent',
                 'x':100,
                 'num_per_plot':6,
                 'xtick_rotation':'vertical',
                 'ylabel':'Estimated Parameter\n Value(Log10)',
                 'title':'Boxplot Showing Distribution of Parameter Estimates',
                 'savefig':False,
                 'results_directory':os.path.join(os.getcwd(), 'BoxplotResults'),
                 'dpi':300}
        
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for Boxplot'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        
        self.data = self.read_data()
        self.data = self.truncate_data()
        
        self.plot()

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]
    
    
    def read_data(self):
        """
        Both a pandas.DataFrame or a file or list of files can be passed
        as the data argument. 
        """
        if isinstance(self.data, pandas.core.frame.DataFrame)!=True:
            return ParsePEData(self.data, sep=self['sep'], log10=self['log10']).data
        else:
            return self.data
    
    def plot(self):
        """
        
        """
            
        os.chdir(self['results_directory'])
            
        labels=self.divide_data()
        for label_set in range(len(labels)):
            plt.figure()#        
            data = self.data[labels[label_set]]
            seaborn.boxplot(data = data )
            plt.xticks(rotation=self['xtick_rotation'])
            plt.title(self['title'])
            plt.ylabel(self['ylabel'])
            if self['savefig']:
                boxplot_dir = os.path.join(self['results_directory'], 'Boxplots')
                if os.path.isdir(boxplot_dir)!=True:
                    os.mkdir(boxplot_dir)
                os.chdir(boxplot_dir)
                plt.savefig(os.path.join(boxplot_dir, 'Boxplot{}.jpeg'.format(label_set)), dpi=self['dpi'], bbox_inches='tight')
        
    def truncate_data(self):
        """
        
        """
        return TruncateData(self.data,mode=self['truncate_mode'],x=self['x'], log10=self['log10']).data

            
    def divide_data(self):
        n_vars=len(self.data.keys())
        n_per_plot= self['num_per_plot']
#        assert n_per_plot<n_vars,'number of variables per plot must be smaller than the number of variables'
        int_division= n_vars//n_per_plot
        remainder=n_vars-(n_per_plot*int_division)
        l=[]
        for i in range(int_division):
            l.append(self.data.keys()[i*n_per_plot:(i+1)*n_per_plot])
        l.append(self.data.keys()[-remainder:])
        return [list(i) for i in l]
        
    
class RssVsIterations():
    def __init__(self, data, **kwargs):
        self.data = data
        
        options={'sep':'\t',
                 'log10':False,
                 'truncate_mode':'percent',
                 'x':100,
                 'xtick_rotation':'horizontal',
                 'ylabel':'Iteration',
                 'title':'RSS Versus Iteration',
                 'savefig':False,
                 'results_directory':os.path.join(os.getcwd(), 'RssVsIteration'),
                 'dpi':300}
        
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for RssVsIteration'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        
        self.data = self.read_data()
        self.data = self.truncate_data()
        
        
        LOG.info('plotting RSS Vs Iterations')
        self.plot()

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]
    
    
    def read_data(self):
        """
        Both a pandas.DataFrame or a file or list of files can be passed
        as the data argument. 
        """
        if isinstance(self.data, pandas.core.frame.DataFrame)!=True:
            return ParsePEData(self.data, sep=self['sep'], log10=self['log10']).data
        else:
            return self.data
    
    def plot(self):
        """
        
        """
            
        os.chdir(self['results_directory'])
            
        plt.figure()#        
        plt.plot(range(self.data['RSS'].shape[0]), self.data['RSS'].sort_values(ascending=False))
        plt.xticks(rotation=self['xtick_rotation'])
        plt.title(self['title'])
        plt.ylabel(self['ylabel'])
        if self['savefig']:
            save_dir = os.path.join(self['results_directory'], 'RssVsIteration')
            if os.path.isdir(save_dir)!=True:
                os.mkdir(save_dir)
            os.chdir(save_dir)
            plt.savefig(os.path.join(save_dir, 'RssVsIteration.jpeg'), dpi=self['dpi'], bbox_inches='tight')
        
    def truncate_data(self):
        """
        
        """
        return TruncateData(self.data,mode=self['truncate_mode'],x=self['x'], log10=self['log10']).data



 
    
    
class Pca():
    def __init__(self, data, **kwargs):
        self.data = data
        
        options={'sep':'\t',
                 'log10':False,
                 'ylabel':'Iteration',
                 'title':'RSS Versus Iteration',
                 'savefig':False,
                 'results_directory':os.path.join(os.getcwd(), 'PCAPlots'),
                 'dpi':300,
                 'n_components':2,
                 'orientation':'parameters', ##iterations or parameters
                 }
        
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for RssVsIteration'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        
        if self['orientation'] not in ['parameters','iterations']:
            raise Errors.InputError('{} not in {}'.format(self['orientation'], ['parameters','iterations']))
        
        self.data = self.read_data()
        
        
        LOG.info('plotting PCA {}'.format(self['orientation']))
        self.pca()
        
        
    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]
    
    
    def read_data(self):
        """
        Both a pandas.DataFrame or a file or list of files can be passed
        as the data argument. 
        """
        if isinstance(self.data, pandas.core.frame.DataFrame)!=True:
            return ParsePEData(self.data, sep=self['sep'], log10=self['log10']).data
        else:
            return self.data
        
        
    def pca(self):
        pca = PCA(n_components=self['n_components'])
        if self['orientation']=='parameters':
            projected = pca.fit(self.data.transpose()).transform(self.data.transpose())
            projected = pandas.DataFrame(projected, index=self.data.columns)
            title = 'PCA grouping parameters'
        else:
            projected = pca.fit(self.data).transform(self.data)
            projected = pandas.DataFrame(projected, index=self.data.index)
            title = 'PCA grouping iterations'
            
        plt.figure()
        plt.plot(projected[0],projected[1], 'o')
        plt.ylabel('PC2')
        plt.xlabel('PC1')
        plt.title(title)
        if self['savefig']:
            save_dir = os.path.join(self['results_directory'], 'PCA')
            if os.path.isdir(save_dir)!=True:
                os.mkdir(save_dir)
            os.chdir(save_dir)
            plt.savefig(os.path.join(save_dir, 'PCA_{}.jpeg'.format(self['orientation'])), dpi=self['dpi'], bbox_inches='tight')

        
    
class Histograms():
    def __init__(self, data, **kwargs):
        self.data = data
        
        options={'sep':'\t',
                 'log10':False,
                 'truncate_mode':'percent',
                 'x':100,
                 'xtick_rotation':'horizontal',
                 'ylabel':'Frequency',
                 'savefig':False,
                 'results_directory':os.path.join(os.getcwd(), 'Histograms'),
                 'dpi':300}
        
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for RssVsIteration'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        
        self.data = self.read_data()
        self.data = self.truncate_data()
        
        LOG.info('plotting histograms')
        self.plot()

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]
    
    
    def read_data(self):
        """
        Both a pandas.DataFrame or a file or list of files can be passed
        as the data argument. 
        """
        if isinstance(self.data, pandas.core.frame.DataFrame)!=True:
            return ParsePEData(self.data, sep=self['sep'], log10=self['log10']).data
        else:
            return self.data
    
    def plot(self):
        """
        
        """
        for parameter in self.data.keys():
            plt.figure()
            seaborn.distplot(self.data[parameter])
            plt.ylabel(self['ylabel'])
            plt.title('Parameter Distribution, n={}'.format(self.data[parameter].shape[0]))
            if self['savefig']:
                save_dir = os.path.join(self['results_directory'], 'Histograms')
                if os.path.isdir(save_dir)!=True:
                    os.mkdir(save_dir)
                os.chdir(save_dir)
                fname = os.path.join(save_dir, Misc.RemoveNonAscii(parameter).filter+'.jpeg')
                plt.savefig(fname, dpi=self['dpi'], bbox_inches='tight')
            
    def truncate_data(self):
        """
        
        """
        return TruncateData(self.data, mode=self['truncate_mode'], x=self['x'], log10=self['log10']).data
    


class Scatters():
    def __init__(self, data, **kwargs):
        self.data = data
        
        options={'sep':'\t',
                 'log10':False,
                 'truncate_mode':'percent',
                 'x':100,
                 'xtick_rotation':'horizontal',
                 'ylabel':'Frequency',
                 'savefig':False,
                 'results_directory':os.path.join(os.getcwd(), 'Scatters'),
                 'dpi':300}
        
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for Scatters'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        
        self.data = self.read_data()
        self.data = self.truncate_data()
        
        self.plot()

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]
    
    
    def read_data(self):
        """
        Both a pandas.DataFrame or a file or list of files can be passed
        as the data argument. 
        """
        if isinstance(self.data, pandas.core.frame.DataFrame)!=True:
            return ParsePEData(self.data, sep=self['sep'], log10=self['log10']).data
        else:
            return self.data
    
    def plot(self):
        """
        
        """
#        for parameter in self.data.keys():
        plt.figure()
        plt.ioff()
        seaborn.pairplot(self.data,hue='RSS',size=5 )
        
#        plt.ylabel(self['ylabel'])
#        plt.title('Parameter Distribution, n={}'.format(self.data[parameter].shape[0]))
        if self['savefig']:
            save_dir = os.path.join(self['results_directory'], 'ScatterMatrix')
            if os.path.isdir(save_dir)!=True:
                os.mkdir(save_dir)
            os.chdir(save_dir)
            fname = os.path.join(save_dir, 'ScatterMatrix.jpeg')
            plt.savefig(fname, dpi=self['dpi'], bbox_inches='tight')
        plt.ion()
            
    def truncate_data(self):
        """
        
        """
        return TruncateData(self.data, mode=self['truncate_mode'], x=self['x'], log10=self['log10']).data
    



#==============================================================================
#
#class WritePEData():
#    '''
#    Write the sorted parameter estimation data as a flat xlsx file
#    Args
#        results_path:
#            The path to the results file or folder of files with parameter
#            estimation data in
#    **kwargs 
#        log10:
#    '''
#    def __init__(self,results_path,**kwargs):
#        self.results_path=results_path
#        self.PED=ParsePEData(self.results_path)
#        
#        
#        options={'log10':False,
#                 
#                     }
#        for i in kwargs.keys():
#            assert i in options.keys(),'{} is not a keyword argument for TruncateData'.format(i)
#        options.update( kwargs)  
#        self.kwargs=options
#        
#        if self.kwargs.get('log10')==True:
#            self.data=numpy.log10(self.PED.data)
#            self.data_file=os.path.join(os.path.dirname(self.results_path),'pe_data_log.xlsx')
#
#        else:
#            self.data=self.PED.data
#            self.data_file=os.path.join(os.path.dirname(self.results_path),'PE_Data.xlsx')
#            
#        if os.path.isfile(self.data_file):
#            os.remove(self.data_file)
#        
#        self.data= self.prune_headers()
#        self.write_to_xlsx()
#        
#    def prune_headers(self):
#        return pycopi.PruneCopasiHeaders(self.data).df
#    
#    def write_to_xlsx(self):
#        if self.kwargs.get('log10')==True:
#            self.data.to_excel(self.data_file)
#        else:
#            self.data.to_excel(self.data_file)
    
#==============================================================================    
class TruncateData():
    '''
    Parameter estimation data in systems biology usually have runs which fall
    into a local minima. Usually a user wants to remove these runs from further 
    analysis. TruncateData does this and provides two modes to do so. A useful 
    indication of where to truncate the data is to look at the plot produced
    by the EvaluateOptimizationPerformance class and the histograms/boxplots/
    profile likelihoods for your specific optimization problem. 
    
    Args:
        data:
            The parameter estiamtion data for truncation. This is a pandas dataframe. 
            
    kwargs:
        mode:
            Two modes accepted. When set to 'percent' take xth percentile of 
            data. when set to 'below_x', truncate data below the value x. Pay
            attention to whether you are in log10 mode or not. 
            
        x:
            Either xth percentive or value to truncate data below. 
    '''
    def __init__(self,data,mode='percent',x=100, log10=False):
        self.data=data
        self.mode=mode        
        self.x=x
        self.log10=log10
        assert isinstance(self.data,pandas.core.frame.DataFrame)
        assert self.mode in ['below_x','percent']
        
        self.data=self.truncate()
        
    def below_x(self):
        assert self.data.shape[0]!=0,'There are no data with RSS below {}. Choose a higher number'.format(self.x)
        return self.data[self.data['RSS']<self.x]
        
            
    def top_x_percent(self):
        '''
        get top x percent data. 
        Defulat= 100 = all data
        '''
        if self.x>100 or self.x<1:
            raise Errors.InputError('{} should be between 0 and 100')
        x_quantile= int(numpy.round(self.data.shape[0]*(float(self.x)/100.0)))
        return self.data.iloc[:x_quantile]
            
    def truncate(self):
        if self.mode=='below_x':
            return self.below_x()#self.data
        elif self.mode=='percent':
            return self.top_x_percent()
        
        
class PlotParameterEnsemble():
    def __init__(self, copasi_file, experiment_files, param_data, **kwargs):
        self.copasi_file = copasi_file
        self.param_data = param_data
        self.experiment_files = experiment_files
        
        if isinstance(self.experiment_files, str):
            self.experiment_files = [self.experiment_files]
        
        options={'sep':'\t',
                 'log10':False,
                 'truncate_mode':'percent',
                 'x':5,
                 'xtick_rotation':'horizontal',
                 'ylabel':'Frequency',
                 'savefig':False,
                 'results_directory':os.path.join(os.getcwd(), 'Scatters'),
                 'dpi':300,
                 'resolution':10} ##resolution: intervals in time course
        
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for Scatters'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        
        self.param_data = self.read_param_data()
        self.param_data = self.truncate_param_data()
        self.experiment_data = self.parse_experimental_files()
        self.exp_times = self.get_experiment_times()
        self.ensemble_data =  self.simulate_ensemble()
#        print self.ensemble_data
#        self.ensemble_data.index = self.ensemble_data.index.rename(['Index','Time'])
        self.plot()
#        
        
        
        '''
        To plot a parameter ensemble:
            1) input parmeters into model
            2) plot time course with same data points (time as experimental data)
            3) plot distributions
        
        '''
        
#        self.plot()

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]
    
    
    def read_param_data(self):
        """
        Both a pandas.DataFrame or a file or list of files can be passed
        as the data argument. 
        """
        if isinstance(self.param_data, pandas.core.frame.DataFrame)!=True:
            return ParsePEData(self.param_data, sep=self['sep'], log10=self['log10']).data
        else:
            return self.param_data
    
            
    def truncate_param_data(self):
        """
        
        """    
        return TruncateData(self.param_data, 
                            mode=self['truncate_mode'],x=self['x'], 
                            log10=self['log10']).data


    def parse_experimental_files(self):
        df_dct={}
        for i in range(len(self.experiment_files)):
            df=pandas.read_csv(self.experiment_files[i],sep=self['sep'][i])
            df_dct[self.experiment_files[i]]=df
        return df_dct
        
    
    def get_experiment_times(self):
        d={}
        for i in self.experiment_data:
            d[i]={}
            for j in self.experiment_data[i].keys():
                if j.lower()=='time':
                    d[i]= self.experiment_data[i][j]
                    
        times={}
        for i in d:
            times[i]={}
            times[i]['start']=d[i].iloc[0]
            times[i]['end']=d[i].iloc[-1]
            times[i]['step_size']=d[i].iloc[1]-d[i].iloc[0]
            '''
            subtract 1 from intervals to account for header
            '''
            times[i]['intervals']=int(d[i].shape[0])-1
        return times
        
    def simulate_ensemble(self):
        """
        
        """
#        d = {}
        
        ## collect end times for each experiment
        ##in order to find the biggest
        end_times = []
        for i in self.exp_times:
            ## start creating a results dict while were at it
#            d[i] = {}
            end_times.append(self.exp_times[i]['end'])
        step_size =  max(end_times)/self['resolution']
        
        d={}
        for i in range(self.param_data.shape[0]):
            I=pycopi.InsertParameters(self.copasi_file, df=self.param_data, index=i)
            TC = pycopi.TimeCourse(self.copasi_file, end = max(end_times), 
                                             step_size = step_size, 
                                             intervals = self['resolution'], 
                                             plot=False)
            d[i] = pandas.read_csv(TC['report_name'], sep='\t')
            
        return pandas.concat(d)
    
    
    def plot(self):
        """
        
        """
        data = self.ensemble_data.reset_index(level=1, drop=True)
        data.index.name = 'ParameterFitIndex'
        data = data.reset_index()
        for parameter in data.keys():
            plt.figure()
            seaborn.tsplot(data, time='Time', value=parameter,
                             unit='ParameterFitIndex')
            plt.title('Ensemble Time Course\n for {} (n={})'.format(parameter, self.param_data.shape[0]))
            if self['savefig']:
                save_dir = os.path.join(self['results_directory'], 'EnsemblePlots')
                if os.path.isdir(save_dir)!=True:
                    os.mkdir(save_dir)
                os.chdir(save_dir)
                fname = os.path.join(save_dir, '{}.jpeg'.format(Misc.RemoveNonAscii(parameter).filter))
                plt.savefig(fname, dpi=self['dpi'], bbox_inches='tight')
    
    
    
class PlotPEData(object):
    '''
    plot a parameter estimation run against experimental data. 
    Suport currently only exists for time course experiments. In future versions
    a SteadyState Task will be introduced and then we can build a plotting feature
    for fitting steady state experiments
    
    Positional Arguments:
    
        copasi_file:
            The copasi file you want to enter parameters into
            
        experiment_files
        
        PE_result_files
    
    **Kwargs
        index:
            index of parameter estimation run to input into the copasi file. 
            The index is ordered by rank of best fit, with 0 being the best.
            Default=0            
            
        prune_headers:
            Prune copasi variable names of Copasi references. True or False
            
        quantity_type:
            Either 'particle_number' or 'concentration'. Default='concentration'
            
        OutputML:
            If savefig set to 'duplicate', this is the duplicate filename. 
            
        savefig:
            either False,'overwrite' or 'duplicate'
            
        parameter_dict:
            A python dictionary with keys correponding to parameters in the model
            and values the parameters (dict[parameter_name]=parameter value). 
            Default=None
            
        df:
            A pandas dataframe with parameters being column names matching 
            parameters in your model and RSS values and rows being individual 
            parameter estimationruns. In this case, ensure you have set the 
            index parameter to the index you want to use. Dataframes are 
            automatically sorted by the RSS column. 
            
        parameter_path:
            Full path to a parameter estimation file ('.txt','.xls','.xlsx' or 
            '.csv') or a folder containing parameter estimation files. 
            
        output_directory:
            Name of an output directory. 
        
    '''
    def __init__(self,copasi_file,experiment_files,PE_result_file,**kwargs):

        self.copasi_file=copasi_file
        self.experiment_files=experiment_files
        self.PE_result_file=PE_result_file
        
        
        
        self.CParser=pycopi.CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=pycopi.GetModelQuantities(self.copasi_file)

        default_report_name=os.path.join(os.path.dirname(self.copasi_file),
                                         os.path.split(self.copasi_file)[1][:-4]+'_PE_results.txt')
        default_outputML=os.path.split(self.copasi_file)[1][:-4]+'_Duplicate.cps'
        options={#report variables
                 'report_name':default_report_name,
                 'savefig':False,
                 'index':0,
                 'line_width':4,
                 'prune_headers':True,
                 
                 #graph features
                 'font_size':22,
                 'axis_size':15,
                 'extra_title':None,
                 'show':False,
                 'multiplot':False,
                 'savefig':False,
                 'title_wrap_size':30,
                 'ylimit':None,
                 'xlimit':None,
                 'dpi':125,
                 'xtick_rotation':35,
                 'marker_size':10,
                 'legend_loc':(1,0),
                 'output_directory':os.path.join(os.path.dirname(self.copasi_file),'ParameterEstimationplots'),
                 'plot':True,                 
                 'separator':['\t']*len(self.experiment_files),
                 
                 }
                 
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for plot'.format(i)
        options.update( kwargs) 
        self.kwargs=options       
        
        
        if self.kwargs.get('plot') not in [False,True]:
            raise Errors.InputError('The plot kwarg takes only \'false\' or \'true\'')
        #limit parameters
        if self.kwargs.get('ylimit')!=None:
            assert isinstance(self.kwargs.get('ylimit'),list),'ylimit is a list of coordinates for y axis,i.e. [0,10]'
            assert len(self.kwargs.get('ylimit'))==2,'length of the ylimit list must be 2'
        
        if self.kwargs.get('xlimit')!=None:
            assert isinstance(self.kwargs.get('xlimit'),list),'xlimit is a list of coordinates for x axis,i.e. [0,10]'
            assert len(self.kwargs.get('xlimit'))==2,'length of the xlimit list must be 2'
        
        assert isinstance(self.kwargs.get('xtick_rotation'),int),'xtick_rotation parameter should be a Python integer'

        
        if self.kwargs.get('extra_title')!=None:
            assert isinstance(self.kwargs.get('extra_title'),str)
        assert isinstance(self.kwargs.get('font_size'),int)
        assert isinstance(self.kwargs.get('axis_size'),int)
        assert isinstance(self.kwargs.get('line_width'),int)

        assert isinstance(self.kwargs.get('title_wrap_size'),int)

        if self.kwargs.get('ylimit')!=None:
            assert isinstance(self.kwargs.get('ylimit'),str)
            
        if self.kwargs.get('xlimit')!=None:
            assert isinstance(self.kwargs.get('xlimit'),str)
            
            
        assert isinstance(self.kwargs.get('dpi'),int)
        assert isinstance(self.kwargs.get('xtick_rotation'),int)
    
        assert self.kwargs.get('show') in [False,True]
        assert self.kwargs.get('savefig') in [False,True]
        assert self.kwargs.get('multiplot') in [False,True]                
                     
        assert self.kwargs.get('prune_headers') in [False,True]                
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for PlotPEData'.format(i)
        options.update( kwargs) 
        self.kwargs=options
        
        if os.path.isfile(self.copasi_file)==False:
            raise Errors.InputError('Your copasi file {}doesn\' exist'.format(self.copasi_file))
            
        if isinstance(self.experiment_files,str):
            if os.path.isfile(self.experiment_files)==False:
                raise Errors.InputError('Your experiment file {} doesn\'t exist'.format(self.experiment_files))
            #make a 1 element list to iterate over later
            self.experiment_files=[self.experiment_files]
            
        if isinstance(self.experiment_files,list):
            for i in self.experiment_files:
                if os.path.isfile(i)==False:
                    raise Errors.InputError('{} doesn\'t exist'.format(i))
        
        if os.path.isfile(self.PE_result_file)==False:
            raise Errors.InputError('Your PE data file {} doesn\'t exist'.format(self.PE_result_file))
        
        if isinstance(self.kwargs['separator'],str):
            self.kwargs['separator']=[self.kwargs['separator']]
        
        matplotlib.rcParams.update({'font.size':self.kwargs.get('axis_size')})
        
        self.experiment_data=self.parse_experimental_files()
        self.exp_times=self.get_experiment_times()
        self.parameters=self.parse_parameters()
        self.insert_parameters()
        self.sim_data=self.simulate_time_course()
        
##        '''
##        Only change directory before doing the actual plotting. 
##        You want to be in the model directory for all the while your collecting
##        data then move on over to the results directory when plotting. 
##        '''
        if self.kwargs.get('plot')==True:
            self.change_directory()
            self.plot()
        os.chdir(os.path.dirname(self.copasi_file))
        
        
    def change_directory(self):
        dire=os.path.join(os.path.dirname(self.copasi_file),'ParameterEstimationplots')
        if os.path.isdir(dire)==False:
            os.mkdir(dire)
        os.chdir(dire)
        return dire
        
        
    def parse_experimental_files(self):
        df_dct={}
        for i in range(len(self.experiment_files)):
            df=pandas.read_csv(self.experiment_files[i],sep=self.kwargs['separator'][i])
            df_dct[self.experiment_files[i]]=df
        return df_dct
        
    
    def get_experiment_times(self):
        d={}
        for i in self.experiment_data:
            d[i]={}
            for j in self.experiment_data[i].keys():
                if j.lower()=='time':
                    d[i]= self.experiment_data[i][j]
                    
        times={}
        for i in d:
            times[i]={}
            times[i]['start']=d[i].iloc[0]
            times[i]['end']=d[i].iloc[-1]
            times[i]['step_size']=d[i].iloc[1]-d[i].iloc[0]
            '''
            subtract 1 from intervals to account for header
            '''
            times[i]['intervals']=int(d[i].shape[0])-1
        return times
        
    def parse_parameters(self):
        if self.kwargs.get('prune_headers')==True:
            pycopi.PruneCopasiHeaders(self.PE_result_file,replace=True)
        df= pandas.read_csv( self.PE_result_file,sep='\t')
        df=ParsePEData(self.PE_result_file)
        df= df.data
        return pandas.DataFrame(df.iloc[-1]).transpose()
    
    def insert_parameters(self):
        pycopi.InsertParameters(self.copasi_file,df=self.parameters)
        return self.copasi_file
        
        
    def simulate_time_course(self):
        '''
        This function does not work with irregular time courses
        '''
        data_dct={}
        for i in self.exp_times:
            '''
            need to subtract 1 from the intervals
            '''
            TC=pycopi.TimeCourse(self.copasi_file,start=0,
                          end=self.exp_times[i]['end'],
                          intervals=self.exp_times[i]['end'],
                          step_size=1,
                          plot=False)
            df = pandas.read_csv(TC.kwargs['report_name'], sep='\t')
            data_dct[i]=df
        return data_dct


#    def simulate_time_course(self):
#        data_dct={}
#        for i in self.exp_times:
#            '''
#            need to subtract 1 from the intervals
#            '''
#            TC=pycopi.TimeCourse(self.copasi_file,Start=self.exp_times[i]['Start'],
#                          End=self.exp_times[i]['End'],
#                          Intervals=self.exp_times[i]['End'],
#                          StepSize=1,plot=False)
#            P=pycopi.PruneCopasiHeaders(TC.data,replace=True)
#            data_dct[i]=P.df
#        return data_dct
        
        
                            
    def plot1(self,fle,parameter):
        '''
        plot one parameter of one experiment. for iterating over in 
        other functions
        '''
        seaborn.set_context(context='poster',font_scale=2)
        if fle not in self.experiment_files:
            raise Errors.InputError('{} not in {}'.format(fle,self.exp_times))
        if parameter not in self.sim_data[fle].keys() and parameter not in self.experiment_data[fle].keys():
            raise Errors.InputError('{} not in {} or {}'.format(parameter,self.sim_data[fle.keys()],self.experiment_data[fle].keys()))
        sim= self.sim_data[fle][parameter]
        exp= self.experiment_data[fle][parameter]
        time_exp= self.experiment_data[fle]['Time']
        time_sim=self.sim_data[fle]['Time']
        plt.figure()
        ax = plt.subplot(111)
        plt.plot(time_sim,sim,'k-',label='simulated',linewidth=self.kwargs.get('line_width'))
        plt.plot(time_exp,exp,'ro',label='experimental',markersize=self.kwargs.get('marker_size'))
        plt.legend(loc=self.kwargs.get('legend_loc'))


   
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        
        #xtick rotation
        plt.xticks(rotation=self.kwargs.get('xtick_rotation'))
        
        #options for changing the plot axis
        if self.kwargs.get('ylimit')!=None:
            ax.set_ylim(self.kwargs.get('ylimit'))
        if self.kwargs.get('xlimit')!=None:
            ax.set_xlim(self.kwargs.get('xlimit'))
        
        plt.title('\n'.join(wrap('{}'.format(parameter),self.kwargs.get('title_wrap_size'))),fontsize=self.kwargs.get('font_size'))
        try:
            plt.ylabel('Quantity Unit ({})'.format(self.GMQ.get_quantity_units().encode('ascii')),fontsize=self.kwargs.get('font_size'))
        except UnicodeEncodeError:
            plt.ylabel('Quantity Unit (micromol)',fontsize=self.kwargs.get('font_size'))
                        
        plt.xlabel('Time ({})'.format(self.GMQ.get_time_unit()),fontsize=self.kwargs.get('font_size'))  


        for j in parameter:
            if j not in string.ascii_letters+string.digits+'_-[]':
                parameter=parameter.replace(j,'_')
                
#        parameter=re.sub(p,'_',parameter) 
                                
                                
                                
        if self.kwargs.get('savefig')==True:
            if self.kwargs.get('extra_title')!=None:
                assert isinstance(self.kwargs.get('extra_title'),str),'extra title should be a string'
                fle=os.path.join(self.kwargs.get('output_directory'),'{}_{}.png'.format(parameter,self.kwargs.get('extra_title')))                
            else:
                fle=os.path.join(self.kwargs.get('output_directory'),'{}.png'.format(parameter))
            plt.savefig(fle,dpi=self.kwargs.get('dpi'),bbox_inches='tight')

        if self.kwargs.get('show')==True:
            plt.show()             
        
        
    def plot1file(self,fle):
        '''
        plot only parameters from a single experiment file
        (for the event that the user has multiple time course
        experiments)
        '''
        for parameter in  self.experiment_data[fle]:
            if parameter !='Time':
                if parameter[-6:]=='_indep':
                    pass
                else:
                    self.plot1(fle,parameter)
        
    def plot(self):
        '''
        plot all parameters
        '''
#        LOG.warning('the plotting function is temporarily disabled')
        for f in self.experiment_files:
            dire,p= os.path.split(f)
            fle=os.path.splitext(p)[0]  
            self.plot1file(f)

    
    
class ModelSelection():
    '''
    ## could give
    '''
    def __init__(self,multi_model_fit, **kwargs):
        LOG.debug('Instantiate ModelSelection class')
        self.multi_model_fit=multi_model_fit
        self.number_models=self.get_num_models()
        
        options={#report variables
                 'savefig':False,
                 'output_directory':self.multi_model_fit.project_dir,
                 'dpi':300}
                 
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for ModelSelection'.format(i)
        options.update( kwargs) 
        self.kwargs=options  
        
        
#        if self.model_selection_filename==None:
#            self.model_selection_filename=os.path.join(self.multi_model_fit.wd,'ModelSelectionData.xlsx')
        self.results_folder_dct=self._get_results_directories()
        self._PED_dct=self._parse_data()
        self.GMQ_dct=self._get_GMQ_dct()
        self.number_model_parameters=self._get_number_estimated_model_parameters()
        self.number_observations=self._get_n()
        self.model_selection_data=self.calculate_model_selection_criteria()
        

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]

    def get_num_models(self):
        return len(self.multi_model_fit.cps_files)
    ## void
    def to_excel(self,filename):
        self.model_selection_data.to_excel(filename)
        
    def _get_results_directories(self):
        '''
        Find the results directories embedded within MultimodelFit
        and RunMutliplePEs. 
        '''
        LOG.debug('Finding location of parameter estimation results:')
        dct=self.multi_model_fit.results_folder_dct
        for key in dct:
            LOG.debug('Key to results folder dict is the cps file: \n{}'.format(key))
            LOG.debug('Value to results folder dict is the output results folder: \n{}'.format(dct[key]))
            LOG.debug('Checking that the results folder exists: ... {}'.format(os.path.isdir(dct[key])))
        return dct
    
    def _parse_data(self):
        '''
        
        '''
        
        PED_dct={}
        LOG.debug('Here is the results folder:\n{}'.format(self.results_folder_dct))
        LOG.debug('The results folder vairable is of type {}'.format(type(self.results_folder_dct)))
#        for i in self._results_folders:
#            print i,self._results_folder[i]
#        print type(self._results_folders)
#        print len(self._results_folders.items())
        for folder in self.results_folder_dct:
            LOG.debug('parsing data from folder')
            LOG.debug('checking results folder exists: {}'.format(os.path.isdir(self.results_folder_dct[folder]),self.results_folder_dct[folder]))
            PED_dct[folder]=ParsePEData(self.results_folder_dct[folder])
            
        LOG.info('data successfully parsed from {} models into Python'.format(len(self.results_folder_dct.items())))
        return PED_dct
            
    def _get_GMQ_dct(self):
        '''
        iterate over each model and get the corresponding
        GetModelQuantities class for each. 
        '''
        LOG.debug('Instantiating GetModelQuantities per model')
        GMQ_dct={}
        for model in self.multi_model_fit.sub_cps_dirs:
            LOG.debug('Key:\t{}'.format(model))
            LOG.debug('Value \t{}'.format(self.multi_model_fit.sub_cps_dirs[model]))
            GMQ_dct[self.multi_model_fit.sub_cps_dirs[model]]=pycopi.GetModelQuantities(self.multi_model_fit.sub_cps_dirs[model])
        LOG.debug('GetModelQuantities Instantiated')
        return GMQ_dct
    
    def _get_number_estimated_model_parameters(self):
        '''
        
        '''
        k_dct={}
        for GMQ in self.GMQ_dct:
            LOG.debug( 'model at {} has {} estimated parameters'.format(GMQ,len(self.GMQ_dct[GMQ].get_fit_items().items())))
            k_dct[GMQ]=len(self.GMQ_dct[GMQ].get_fit_items().items())
        return k_dct
            
    def _get_n(self):
        '''
        get number of observed data points for AIC calculation
        '''
        LOG.info('Counting number of observed data points:...')
        LOG.debug('Number of Experiment Files: \t{}'.format(len(self.multi_model_fit.exp_files)))
        n={}
        for exp in self.multi_model_fit.exp_files:
            data=pandas.read_csv(exp,sep='\t')
            l=[]
            for key in data.keys() :
                if key.lower()!='time':
                    if key[-6:]!='_indep':
                        LOG.debug('Dimensions of data at file \n{} is \n{}'.format(exp,data[key].shape))
                        l.append(int(data[key].shape[0]))
            n[exp]=sum(l)
        n=sum(n.values())
        LOG.debug('Final sum of all data files is {}'.format(n))
        return n
        
        
    
    def calculate1AIC(self,RSS,K,n):
        '''
        Calculate the corrected AIC:
            
            AICc = -2*ln(RSS/n) + 2*K + (2*K*(K+1))/(n-K-1) 
                
            or if likelihood function used instead of RSS
                                
            AICc = -2*ln(likelihood) + 2*K + (2*K*(K+1))/(n-K-1)
            
        Where:
            RSS:
                Residual sum of squares for model fit
            n:
                Number of observations collectively in all data files
                
            K:
                Number of model parameters
        '''
        return n*numpy.log((RSS/n))  + 2*K + (2*K*(K+1))/(n-K-1) 
        
    
    def calculate1BIC(self,RSS,K,n):
        '''
        Calculate the bayesian information criteria
            BIC = -2*ln(likelihood) + k*ln(n)
            
                Does this then go to:
                    
            BIC = -2*ln(RSS/n) + k*ln(n)
        '''
        return  (n*numpy.log(RSS/n) ) + K*numpy.log(n)
    
    def calculate_model_selection_criteria(self):
        '''
        
        '''
        LOG.debug('calculating model selection criteria AIC and BIC')
        LOG.debug('self.multi_model_fit.sub_cps_dirs is of type {}'.format(type(self.multi_model_fit.sub_cps_dirs)))
        df_dct={}
        for model_num in range(len(self.multi_model_fit.sub_cps_dirs)):
            keys=self.multi_model_fit.sub_cps_dirs.keys()
            LOG.debug( 'Calculating MSC for model \t{}'.format(keys[model_num]))
            cps_key=self.multi_model_fit.sub_cps_dirs[keys[model_num]]
            k=self.number_model_parameters[cps_key]
            LOG.debug('k is {}'.format(k))
            n=self.number_observations #constant throughout analysis 
            LOG.debug('n is {}'.format(n))
            RSS=self._PED_dct[cps_key].data['RSS']
            LOG.debug(RSS.shape)
            aic_dct={}
            bic_dct={}
            LOG.debug('Full RSS Series')
            LOG.debug(RSS)
            for i in range(len(RSS)):
                LOG.debug('In RSS vector: {},{}'.format(i,RSS.iloc[i]))
                aic=self.calculate1AIC(RSS.iloc[i],k,n)
                bic=self.calculate1BIC(RSS.iloc[i],k,n)
                aic_dct[i]=aic
                bic_dct[i]=bic
                LOG.debug('In idx,RSS,AIC,BIC: {},{},{},{}'.format(i,RSS.iloc[i],aic,bic))
            LOG.debug('RSS for model:\n{}'.format(RSS.to_dict()))
            LOG.debug('AICc calculation produced:\n{}'.format(aic_dct))
            LOG.debug('BIC calculation produced:\n{}'.format(bic_dct))
            LOG.debug('{},{}'.format(i,RSS[i]))
            aic= pandas.DataFrame.from_dict(aic_dct,orient='index')
            RSS= pandas.DataFrame(RSS)
            bic= pandas.DataFrame.from_dict(bic_dct,orient='index')
            LOG.debug(aic)
            LOG.debug(RSS)
            LOG.debug(bic)
            df=pandas.concat([RSS,aic,bic],axis=1)
            df.columns=['RSS','AICc','BIC']
            df.index.name='RSS Rank'
            df_dct[os.path.split(cps_key)[1]]=df
            LOG.debug('\n{}'.format(df))
        df=pandas.concat(df_dct,axis=1)
        LOG.debug(df)
        return df
    
    
    def plot_boxplot(self):
        '''
        
        '''
        data = self.model_selection_data
        
        data = data.unstack()
        data = data.reset_index()
        data = data.rename(columns={'level_0':'Model',
                                    'level_1':'Metric',
                                    0:'Score'})
#        print data
        for metric in data['Metric'].unique():
            plt.figure()
            seaborn.boxplot(data = data[data['Metric']==metric],
                            x='Model',y='Score')
            plt.xticks(rotation='vertical')
            plt.title('{} Scores'.format(metric))
            plt.xlabel(' ')
            if self['savefig']:
                save_dir = os.path.join(self['output_directory'], 'ModelSelectionGraphs')
                if os.path.isdir(save_dir)!=True:
                    os.mkdir(save_dir)
                os.chdir(save_dir)
                fname = os.path.join(save_dir, '{}.png'.format(metric))
                plt.savefig(fname, dpi=self['dpi'], bbox_inches='tight')
  
        
        
        
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
        return dct[0.05]
    
    def call_fit_analysis_script(self,tolerance=0.001):
        '''
        
        '''
        LOG.debug('calling fit analysis script')
        for i in self.multi_model_fit.results_folder_dct:
            LOG.debug('\tKey :\n{}\nValue:\n{}'.format(i,self.multi_model_fit.results_folder_dct[i]))
            self.run_fit_analysis(self.multi_model_fit.results_folder_dct[i])

#    @ipyparallel.dview.remote(block=True)
    def run_fit_analysis(self,results_path,tolerance=0.001):
        '''
        
        '''
        scripts_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),'Scripts')
        fit_analysis_script_name=os.path.join(scripts_folder,'fit_analysis.py')
        LOG.debug('fit analysis script on your computer is at \t\t{}'.format(fit_analysis_script_name))

        return Popen(['python',fit_analysis_script_name,results_path,'-tol', tolerance])
#        
    def compare_sim_vs_exp(self):
        '''
        
        '''
        LOG.info('Visually comparing simulated Versus Experiemntal data.')
        
        for cps, res in self.multi_model_fit.results_folder_dct.items():
            LOG.debug('running current solution statistics PE with:\t {}'.format(cps))
            pycopi.InsertParameters(cps,parameter_path=res, index=0)
            PE=pycopi.ParameterEstimation(cps,self.multi_model_fit.exp_files,
                                       randomize_start_values=False,
                                       method='CurrentSolutionStatistics',
                                       plot=True,savefig=True,
                                       )
            PE.set_up()
            PE.run()
            PE.format_results()
            
            
    def get_best_parameters(self,filename=None):
        '''
        
        '''
        df=pandas.DataFrame()
        for cps, res in self.multi_model_fit.results_folder_dct.items():
            df[os.path.split(cps)[1]]= ParsePEData(res).data.iloc[0]
            
        if filename==None:
            return df
        else:
            df.to_excel(filename)
            return df
        
        
        
    def compare_model_parameters(self,parameter_list,filename=None):
        '''
        Compare all the parameters accross multiple models 
        in a bar chart averaging and STD for a parameter accross
        all models. 
        
        May have a problem with different models have different 
        parameters as they are not directly comparible
        '''
        best_parameters=self.get_best_parameters()
        data= best_parameters.loc[parameter_list].transpose()
        f=seaborn.barplot(data=numpy.log10(data))
        f.set_xticklabels(parameter_list,rotation=90)
        plt.legend(loc=(1,1))
        plt.title('Barplot Comparing Parameter Estimation Results for specific\nParameters accross all models')
        plt.ylabel('log10(parameter_value),Err=SEM')
        if filename!=None:
            plt.savefig(filename,dpi=200,bbox_inches='tight')
#
        
        
if __name__=='__main__':
    execfile('/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/testing_kholodenko_manually.py')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




















