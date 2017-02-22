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


'''
import string
import pandas 
import matplotlib.pyplot as plt
import scipy 
import numpy 
import os
import matplotlib
from textwrap import wrap
import itertools
import unittest
import pycopi,Errors
import re
import logging
#import math


class ParsePEData():
    '''
    parse parameter estimation data from file
    
    Args:
        results_path: 
            Absolute path to file or folder of files containing parameter
            estimation data. 
            
    kwargs:
        UsePickle:
            Allow one to overwrite the pickle file automatically
            produced for speed. Default='false'
    '''
    def __init__(self,results_path,UsePickle='false',OverwritePickle='true',
                 RemoveInfiniteRSS='false',PicklePath=None):
        #input argument variables
        self.results_path=results_path #either file or folder
        self.RemoveInfiniteRSS=RemoveInfiniteRSS
        #assertions
#        assert os.path.isfile(self.copasi_file),'{} is not a real file'.format(self.copasi_file)
        #change directory
        self.cwd=os.path.dirname(self.results_path)
        os.chdir(self.cwd)
        self.pickle_path=PicklePath
        if self.pickle_path==None:
            self.pickle_path=os.path.join(self.cwd,'PEData.pickle')
            self.pickle_path_log=os.path.join(self.cwd,'PEData_log.pickle')
        else:
            self.pickle_path_log=os.path.join(os.path.dirname(self.pickle_path),os.path.splitext(self.pickle_path)[0][:6]+'_log.pickle')
#        self.FromPickle=True
        self.UsePickle=UsePickle
        self.OverwritePickle=OverwritePickle
        
        assert os.path.exists(self.results_path),'{} does not exist'.format(self.results_path)
        if os.path.isdir(self.results_path):
            self.mode='folder'
        elif os.path.isfile(self.results_path):
            self.mode='file'
            
        if self.UsePickle not in ['true','false']:
            raise Errors.InputError('The argument UsePickle only accepts \'true\' or \'false\'')

        if self.OverwritePickle not in ['true','false']:
            raise Errors.InputError('The argument OverwritePickle only accepts \'true\' or \'false\'')

        if self.RemoveInfiniteRSS not in ['true','false']:
            raise Errors.InputError('The argument OverwritePickle only accepts \'true\' or \'false\'')            
        
        self.data=self.read_data()
        if self.data.empty==True:
            raise Errors.InputError('DataFrame is empty. Your PE data has not been read.')
        self.data=self.rename_RSS(self.data)
        self.data=self.sort_data(self.data)
#        self.data=self.prune_headers()
        self.data=self.filter_constants(self.data)
        self.data=self.remove_infinite_RSS()
        self.data=pycopi.PruneCopasiHeaders(self.data).prune()
        try:
            self.log_data=self.log10_conversion()
        except AttributeError:
            raise TypeError('Could not convert to log10 scale. Chances are this is because you have infinite RSS values in your parameter estimation data. Try changing the optimization settings')
            



    def remove_infinite_RSS(self):
        for i in self.data['RSS']:
            if i=='1.#INF' :
                logging.log(logging.INFO,'Your PE data contains infinite RSS values. These data will be removed''')
                self.RemoveInfiniteRSS='true'
        if self.RemoveInfiniteRSS=='true':
            return self.data[self.data['RSS']!='1.#INF'].reset_index(drop=True)
        else:
            return self.data
        
        
    def filter_constants(self,df):
        if self.data.shape[0]==1:
            return self.data
        else:
            return df.loc[:, (df != df.ix[0]).any()] 
        
    def read_folder(self):
        '''
        read folder of tab separated csv files i.e. the output from copasi
        '''
        assert os.path.isdir(self.results_path),'{} is not a real directory'.format(self.results_path)
        df_list=[]
        for i in os.listdir(self.results_path):
            path=os.path.join(self.results_path,i)
            if os.path.splitext(path)[1]=='.txt':
                df=pandas.read_csv(path,sep='\t')
                df_list.append(df)
        return pandas.concat(df_list)
                
    def rename_RSS(self,data):
        '''
        change the RSS from copasi output to RSS
        '''
        b='TaskList[Parameter Estimation].(Problem)Parameter Estimation.Best Value'
        if b in data.keys():
            data=data.rename(columns={b:'RSS'})
        return data

        
    def sort_data(self,data):
        '''
        sort data in order of increasing RSS
        '''
        data.sort_values('RSS',inplace=True)
        data.reset_index(drop=True,inplace=True)
        return data

        
    def read_file(self):
        assert self.mode=='file','mode not file'
        _,ext=os.path.splitext(self.results_path)
        assert ext in ['.txt','.xlsx','.xls','.csv','.pickle'],'parameter file is not .pickle, .txt, .xlsx, .xls, .csv'
        if ext=='.txt':
            return pandas.read_csv(self.results_path,sep='\t')
        elif ext=='xlsx' or ext=='xls':
            return pandas.read_excel(self.results_path)
        elif ext=='.csv':
            return pandas.read_csv(self.results_path)
        elif ext=='.pickle':
            return pandas.read_pickle(self.results_path)
            
    def read_pickle(self):
        if os.path.isfile(self.pickle_path)!=True:
            raise Errors.InputError('Pickle path does not exist')
        return pandas.read_pickle(self.pickle_path)
 

    def read_data(self):
        '''
        Read data. The self.for_testing variable only exists for
        sign posting the tests for this class
        '''
        self.for_testing=None
        def read():
            if self.mode=='file':
                return self.read_file()
            elif self.mode=='folder':
                return self.read_folder()
                
                
        if self.UsePickle=='false':
            self.for_testing='pickle_false'
            data=read()
            data.to_pickle(self.pickle_path)
            return data

        if self.UsePickle=='true':
            if self.OverwritePickle=='false':
                self.for_testing='pickle_true_overwrite_false'
                return self.read_pickle()

            elif self.OverwritePickle=='true':
                self.for_testing='pickle_true_overwrite_true'
                if os.path.isfile(self.pickle_path):
                    os.remove(self.pickle_path)
                self.UsePickle=='false'
                data=read()
                data.to_pickle(self.pickle_path)
                return data 

    def log10_conversion(self):
        return numpy.log10(self.data)

#==============================================================================

class WritePEData():
    '''
    Write the sorted parameter estimation data as a flat xlsx file
    Args
        results_path:
            The path to the results file or folder of files with parameter
            estimation data in
    **kwargs 
        Log10:
    '''
    def __init__(self,results_path,**kwargs):
        self.results_path=results_path
        self.PED=ParsePEData(self.results_path)
        
        
        options={'Log10':'false',
                 
                     }
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TruncateData'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        
        if self.kwargs.get('Log10')=='true':
            self.data=numpy.Log10(self.PED.data)
            self.data_file=os.path.join(os.path.dirname(self.results_path),'PE_Data_log.xlsx')

        else:
            self.data=self.PED.data
            self.data_file=os.path.join(os.path.dirname(self.results_path),'PE_Data.xlsx')
            
        if os.path.isfile(self.data_file):
            os.remove(self.data_file)
        
        self.data= self.prune_headers()
        self.write_to_xlsx()
        
    def prune_headers(self):
        return pycopi.PruneCopasiHeaders(self.data).df
    
    def write_to_xlsx(self):
        if self.kwargs.get('Log10')=='true':
            self.data.to_excel(self.data_file)
        else:
            self.data.to_excel(self.data_file)
    
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
        TruncateMode:
            Two modes accepted. When set to 'percent' take Xth percentile of 
            data. when set to 'below_x', truncate data below the value X. Pay
            attention to whether you are in Log10 mode or not. 
            
        X:
            Either Xth percentive or value to truncate data below. 
    '''
    def __init__(self,data,TruncateMode='percent',X=100):
        self.data=data
        self.TruncateMode=TruncateMode        
        self.X=X
        assert isinstance(self.data,pandas.core.frame.DataFrame)
        assert self.TruncateMode in ['below_x','percent']
        
        self.data=self.truncate()
        
    def below_x(self):
        assert self.data.shape[0]!=0,'There are no data with RSS below {}. Choose a higher number'.format(self.X)
        return self.data[self.data['RSS']<self.X]
        
            
    def top_x_percent(self):
        '''
        get top X percent data. 
        Defulat= 100 = all data
        '''
        if self.X>100 or self.X<1:
            raise Errors.InputError('{} should be between 0 and 100')
        x_quantile= int(numpy.round(self.data.shape[0]*(float(self.X)/100.0)))
        return self.data.iloc[:x_quantile]
            
    def truncate(self):
        if self.TruncateMode=='below_x':
            return self.below_x()#self.data
        elif self.TruncateMode=='percent':
            return self.top_x_percent()
        

#==============================================================================
class PlotHistogram():
    '''
    Plot parameter estimation results as histogram
    Args:
        results_path:
            Path to file or folder of files containing parameter estimation data
            to plot
    **kwargs:
         TruncateMode:
             'below_x', #either 'below_x' or 'percent' for method of truncation. 
         Log10:
             'false',
         X:
             100,           #if below_x: this is the X boundary. If percent: this is the percent of data to keep
    **kwargs which correspond to matplotlib.pyplot.hist keyword arguments. 
    More information about these can be found in the matplotlib documentation 
         Bins:
             Number of bins to use. Default=100,
         AxisSize:
             Font size for the axis. Default=15
         FontSize:
             Font size for the graph labels. Default=22
         Normed:
             'true' or 'false. Whether to make the plot integrate to 1. 
             Default='false'
         Color:
             Plot colour. Default='red',     
         XRotation:
             25,   #rotation for X tick axis
         TitleWrapSize:
             Number of characters to use before word wrapping the title. Default=35  
         Orientation:
             'horizontal' or 'vertical', default='vertical'
         SaveFig:
             'true' or 'false'. Save to a folder called histograms in results directory. 
             Default='false'
         DPI:
             Resolution to use when SaveFig='true'. The larger this value the 
             higher the resolution. Default=125. 
         ExtraTitle:
             When SaveFig='true', save with ExtraTitle appended to the filepath. 
             Default=None
         Show:
             'true' or 'false'. When not using iPython and graphs are not automatically 
             displayed in shell, this determines whether the plots are opened in a
             window or not. Default='false'
        
         ResultsDirectory:
             Name of the directory to store parameter estimation results. 
             Default= 'Histograms'
                     
                 
    '''
    def __init__(self,results_path,**kwargs):
        #arguments
#        self.copasi_file=copasi_file
        self.results_path=results_path
        #keywrod arguments
        options={'FromPickle':'false',
                 'TruncateMode':'percent', #either 'below_x' or 'percent' for method of truncation. 
                 'Log10':'false',
                 'X':100,           #if below_x: this is the X boundary. If percent: this is the percent of data to keep
                 'Bins':100,
                 'AxisSize':15,
                 'FontSize':22,
                 'Normed':'false',
                 'Color':'red',
                 'XRotation':25,
                 'TitleWrapSize':35,
                 'Orientation':'vertical',
                 'SaveFig':'false',
                 'DPI':125,
                 'ExtraTitle':None,
                 'Log10':'false',
                 'Show':'false',
                 'Variable':None,
                 'ResultsDirectory':None,
                 'ColourMap':'plasma',
                 }
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TruncateData'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        assert self.kwargs.get('TruncateMode') in ['below_x','percent']
        
        #Other 
        self.PED=ParsePEData(self.results_path)

        #create a directory and change to it
        if self.kwargs.get('ResultsDirectory')==None:
            self.results_dir=os.path.join(os.path.dirname(self.results_path),'Histograms')
        else:
            self.results_dir=self.kwargs.get('ResultsDirectory')
        if self.kwargs.get('SaveFig')=='true':
            if os.path.isdir(self.results_dir)!=True:
                os.mkdir(self.results_dir)
            os.chdir(self.results_dir)
        
        #attributes
        self.data=self.PED.data.dropna()
        self.log_data=self.PED.log_data.dropna()
        self.truncated_data=self.truncate_data()
        #main method
        self.testing_variable=self.plot_all() #only assigned to variable for testing purposes
        os.chdir('..')
        
    def list_parameters(self):
        return self.data.keys()
    
    def truncate_data(self):
        if self.kwargs.get('Log10')=='false':
#            print '1'
            TC=TruncateData(self.data,TruncateMode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
        elif self.kwargs.get('Log10')=='true':
#            print '2'
            TC=TruncateData(self.log_data,TruncateMode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
        
    def plot1(self,variable='RSS'):
        '''
        variable: variable to plot. Default= 'RSS'
        '''
        matplotlib.rcParams.update({'font.size': 22})
        assert variable in self.truncated_data.keys(),'{} is not in your PE results: {}'.format(variable,self.truncated_data.keys())
        data= self.truncated_data[variable]
        plt.figure()
        plt.hist(data,
                 bins=self.kwargs.get('Bins'),
                 color=self.kwargs.get('Color'),
                 normed=self.kwargs.get('Normed'),
                 orientation=self.kwargs.get('Orientation'))
        
        #pretty stuff
        ax=plt.subplot(1,1,1)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        
        #labels
#        plt.title('\n'.join(wrap('{},n={}'.format(variable,self.data.shape[1])) ),35  )
        plt.title('\n'.join(wrap('{},n={}'.format(variable,data.shape[0]),
                                 self.kwargs.get('TitleWrapSize'))),
                                 fontsize=self.kwargs.get('FontSize'))
        plt.ylabel('Frequency in bin')
        plt.xticks(rotation=self.kwargs.get('XRotation'))
        if self.kwargs.get('Log10')=='true':
            plt.xlabel('Parameter Value(Log10)',fontsize=self.kwargs.get('FontSize'))
        else:
            plt.xlabel('Parameter Value',fontsize=self.kwargs.get('FontSize'))
        
        #SaveFig options
        if self.kwargs.get('SaveFig')=='true':
            if self.kwargs.get('ExtraTitle')!=None:
                assert isinstance(self.kwargs.get('ExtraTitle'),str),'extra title should be a string'
                plt.savefig(variable+'_'+self.kwargs.get('ExtraTitle')+'.jpeg',bbox_inches='tight',format='jpeg',dpi=self.kwargs.get('DPI'))
            else:
                plt.savefig(variable+'.jpeg',format='jpeg',bbox_inches='tight',dpi=self.kwargs.get('DPI'))
        if self.kwargs.get('Show')=='true':
            plt.show()
    
    def plot_all(self):
        for i in self.truncated_data:
            self.plot1(i)
        return True


        
#==============================================================================            
class PlotScatters():
    '''
    Plot all possible combinations of scatter graph
    '''
    def __init__(self,results_path,**kwargs):
        self.results_path=results_path
        #keywrod arguments
        options={'FromPickle':'false',
                 'TruncateMode':'percent', #either 'below_x' or 'percent' for method of truncation. 
                 'Log10':'false',
                 'X':100,           #if below_x: this is the X boundary. If percent: this is the percent of data to keep
                 'AxisSize':15,
                 'FontSize':22,
                 'Color':'red',
                 'XRotation':25,
                 'TitleWrapSize':35,
                 'SaveFig':'false',
                 'DPI':125,
                 'ExtraTitle':None,
                 'Log10':'false',
                 'Show':'false',
                 'ColourMap':'inferno',
                 'ResultsDirectory':None,
                 
                     }
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TruncateData'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        assert self.kwargs.get('TruncateMode') in ['below_x','percent']
        
        #Other classes
        self.PED=ParsePEData(self.results_path)
        
        #create a directory and change to it
        if self.kwargs['ResultsDirectory']==None:
            self.results_dir=os.path.join(os.path.dirname(self.results_path),'Scatters')
        else:
            self.results_dir=self.kwargs['ResultsDirectory']
            
        if self.kwargs.get('SaveFig')=='true':
            if os.path.isdir(self.results_dir)!=True:
                os.mkdir(self.results_dir)
            os.chdir(self.results_dir)
        
        
        #attributes
        self.data=self.PED.data
        self.log_data=self.PED.log_data.dropna()
        self.truncated_data=self.truncate_data()
        self.testing_variable=self.plot_scatters()

    def list_parameters(self):
        return self.data.keys()
    
        
    def truncate_data(self):
        if self.kwargs.get('Log10')=='false':
            TC=TruncateData(self.data,TruncateMode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
        else:
            TC=TruncateData(self.log_data,TruncateMode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
            
    def plot1_scatter(self,x_specie,y_specie,data):
        assert x_specie in self.truncated_data.keys(),'x_specie is not in your PE data set'
        assert y_specie in self.truncated_data.keys(),'y_specie is not in your PE data set'
        matplotlib.rcParams.update({'font.size':self.kwargs.get('AxisSize')})   
        x_data=self.truncated_data[x_specie]
        y_data=self.truncated_data[y_specie]
        plt.figure()
        plt.scatter(x_data,y_data,c=self.truncated_data['RSS'],cmap=self.kwargs['ColourMap'])
        cb=plt.colorbar()
        cb.set_label('RSS')
        #pretty stuff
        ax=plt.subplot(1,1,1)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        
        #labels
#        plt.title('\n'.join(wrap('{},n={}'.format(variable,self.data.shape[1])) ),35  )
        plt.title('\n'.join(wrap('n={},Log10={}'.format(x_data.shape[0],self.kwargs.get('Log10')),
                                 self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))
        plt.ylabel('\n'.join(wrap(y_specie,self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))
        plt.xticks(rotation=self.kwargs.get('XRotation'))
        if self.kwargs.get('Log10')=='true':
            plt.xlabel(x_specie,fontsize=self.kwargs.get('FontSize'))
        else:
            plt.xlabel(x_specie,fontsize=self.kwargs.get('FontSize'))
        
        x_specie=x_specie.replace('(','')
        x_specie=x_specie.replace(')','')
        y_specie=y_specie.replace('(','')
        y_specie=y_specie.replace(')','')
#        SaveFig options
        if self.kwargs.get('SaveFig')=='true':
            if self.kwargs.get('ExtraTitle')!=None:
                assert isinstance(self.kwargs.get('ExtraTitle'),str),'extra title should be a string'
                plt.savefig('{}_vs_{}'.format(x_specie,y_specie)+'_'+self.kwargs.get('ExtraTitle')+'.jpeg',bbox_inches='tight',format='jpeg',dpi=self.kwargs.get('DPI'))
            else:
                plt.savefig('{}_vs_{}'.format(x_specie,y_specie)+'.jpeg',format='jpeg',bbox_inches='tight',dpi=self.kwargs.get('DPI'))
        if self.kwargs.get('Show')=='true':
            plt.show()
        else:
            plt.close()
#            
            
    def binomial_coefficient(self,n,k):
        assert isinstance(n,int)
        assert isinstance(k,int)
        from scipy.misc import factorial
        return factorial(n)/(factorial(k)*factorial(n-k))
        
        
    def get_combinations(self):
        comb=itertools.combinations(self.truncated_data.keys(),2)
#        comb=[i for i in comb]
        return comb
        
    def plot_scatters(self):
        '''
        
        '''
        comb=self.get_combinations()
        for X,y in comb:
            self.plot1_scatter(X,y,self.truncated_data)
        return True

class PlotHexMap():
    '''
    Plot all possible combinations of scatter graph
    '''
    def __init__(self,results_path,**kwargs):
        self.results_path=results_path
        #keywrod arguments
        options={'FromPickle':'false',
                 'TruncateMode':'percent', #either 'below_x' or 'percent' for method of truncation. 
                 'Log10':'false',
                 'GridSize':25,
                 'X':100,           #if below_x: this is the X boundary. If percent: this is the percent of data to keep
                 'AxisSize':15,
                 'FontSize':22,
                 'Bins':'log',
                 'ColorMap':'inferno',
                 'XRotation':25,
                 'TitleWrapSize':25,
                 'SaveFig':'false',
                 'DPI':125,
                 'ExtraTitle':None,
                 'Log10':'false',
                 'Show':'false',
                 'Mode':'counts',
                 'Marginals':'false',
                 'ColourMap':'inferno',
                 'ResultsDirectory':None,
                 
                     }
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for PlotHexMap'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        assert self.kwargs.get('TruncateMode') in ['below_x','percent']
        if self.kwargs['Mode'] not in ['counts','RSS']:
            raise Errors.InputError('{} not in {}'.format(self.kwargs['Mode'],['counts','RSS']))        
        
        if self.kwargs['Marginals'] not in ['true','false']:
            raise Errors.InputError('{} not argument for Marginals'.format(self.kwargs['Marginals']))
            
        if self.kwargs['Marginals']=='true':
            self.kwargs['Marginals']=True
        else:
            self.kwargs['Marginals']=False
        self.PED=ParsePEData(self.results_path)
        
        #create a directory and change to it
        if self.kwargs['ResultsDirectory']==None:
            if self.kwargs['Mode']=='RSS':
                self.results_dir=os.path.join(os.path.dirname(self.results_path),'HexPlotsByRSS')
            else:
                self.results_dir=os.path.join(os.path.dirname(self.results_path),'HexPlotsByCounts')
        if self.kwargs.get('SaveFig')=='true':
            if os.path.isdir(self.results_dir)!=True:
                os.mkdir(self.results_dir)
            os.chdir(self.results_dir)
            

        
        
        #attributes
        self.data=self.PED.data
        self.log_data=self.PED.log_data.dropna()
        self.truncated_data=self.truncate_data()
        self.testing_variable=self.plot_hex_maps()

    def list_parameters(self):
        return self.data.keys()
    
        
    def truncate_data(self):
        if self.kwargs.get('Log10')=='false':
            TC=TruncateData(self.data,TruncateMode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
        else:
            TC=TruncateData(self.log_data,TruncateMode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
            
    def plot1_hex(self,x_specie,y_specie,data):
        assert x_specie in self.truncated_data.keys(),'x_specie is not in your PE data set'
        assert y_specie in self.truncated_data.keys(),'y_specie is not in your PE data set'
        matplotlib.rcParams.update({'font.size':self.kwargs.get('AxisSize')})   
        
        
        x_data=self.truncated_data[x_specie]
        y_data=self.truncated_data[y_specie]
        plt.figure()
        if self.kwargs['Mode']=='RSS':
            plt.hexbin(x_data,y_data,cmap=self.kwargs['ColourMap'],C=self.truncated_data['RSS'],bins=self.kwargs['Bins'],gridsize=self.kwargs['GridSize'])
            cb=plt.colorbar()
            if self.kwargs['Bins']=='log':
                cb.set_label('RSS(log)')   
            else:
                cb.set_label('RSS')
        else:
            plt.hexbin(x_data,y_data,cmap=self.kwargs['ColourMap'],gridsize=self.kwargs['GridSize'],bins=self.kwargs['Bins'])
            cb=plt.colorbar()
            if self.kwargs['Bins']=='log':
                cb.set_label('Counts (log)')        
            else:
                cb.set_label('Counts')

        #pretty stuff
        ax=plt.subplot(1,1,1)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
#        
        #labels
        plt.title('\n'.join(wrap('n={},Log10={},Bins={},GridSize={}'.format(x_data.shape[0],self.kwargs.get('Log10'),self.kwargs['Bins'],self.kwargs['GridSize']),
                                 self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))
        plt.ylabel('\n'.join(wrap(y_specie,self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))
        plt.xticks(rotation=self.kwargs.get('XRotation'))
        if self.kwargs.get('Log10')=='true':
            plt.xlabel(x_specie,fontsize=self.kwargs.get('FontSize'))
        else:
            plt.xlabel(x_specie,fontsize=self.kwargs.get('FontSize'))
        
        
        x_specie=x_specie.replace('(','')
        x_specie=x_specie.replace(')','')
        y_specie=y_specie.replace('(','')
        y_specie=y_specie.replace(')','')
#        SaveFig options
        if self.kwargs.get('SaveFig')=='true':
            if self.kwargs.get('ExtraTitle')!=None:
                assert isinstance(self.kwargs.get('ExtraTitle'),str),'extra title should be a string'
                plt.savefig('{}_vs_{}'.format(x_specie,y_specie)+'_'+self.kwargs.get('ExtraTitle')+'.jpeg',bbox_inches='tight',format='jpeg',dpi=self.kwargs.get('DPI'))
            else:
                plt.savefig('{}_vs_{}'.format(x_specie,y_specie)+'.jpeg',format='jpeg',bbox_inches='tight',dpi=self.kwargs.get('DPI'))
        if self.kwargs.get('Show')=='true':
            plt.show()
        else:
            plt.close()
#            
            
    def binomial_coefficient(self,n,k):
        assert isinstance(n,int)
        assert isinstance(k,int)
        from scipy.misc import factorial
        return factorial(n)/(factorial(k)*factorial(n-k))
        
        
    def get_combinations(self):
        comb=itertools.combinations(self.truncated_data.keys(),2)
#        comb=[i for i in comb]
        return comb
        
    def plot_hex_maps(self):
        '''
        
        '''
        comb=self.get_combinations()
        for x,y in comb:
            self.plot1_hex(x,y,self.truncated_data)
        return True
#==============================================================================
class PlotBoxplot():
    '''
    Visualize your PE data as boxplots. 
    
    args:
        results_path:
            A parameter esitmation results file or a folder of parameter 
            estimation results files. 
            
    **kwargs:
         NumPerPlot:
            How many parameters to include in a box plot before producing 
            multiple figure. Default=None -  means all will be in one figure. 
    
         TruncateMode:
             'below_x', #either 'below_x' or 'percent' for method of truncation. 
         Log10:
             'false',
         X:
             Corresponding parameter for TruncateMode. See entry for
             the TruncateData class. Default=100           
    kwargs which correspond to matplotlib.pyplot.hist keyword arguments. 
    More information about these can be found in the matplotlib documentation 
         AxisSize:
             Font size for the axis. Default=15
         FontSize:
             Font size for the graph labels. Default=22
         Normed:
             'true' or 'false. Whether to make the plot integrate to 1. 
             Default='false'
         Color:
             Plot colour. Default='red',     
         XRotation:
             25,   #rotation for X tick axis
         TitleWrapSize:
             Number of characters to use before word wrapping the title. Default=35  
         Orientation:
             'horizontal' or 'vertical', default='vertical'
         SaveFig:
             'true' or 'false'. Save to a folder called boxplots in results directory. 
             Default='false'
         DPI:
             Resolution to use when SaveFig='true'. The larger this value the 
             higher the resolution. Default=125. 
         ExtraTitle:
             When SaveFig='true', save with ExtraTitle appended to the filepath. 
             Default=None
         Show:
             'true' or 'false'. When not using iPython and graphs are not automatically 
             displayed in shell, this determines whether the plots are opened in a
             window or not. Default='false'
    
    '''
    def __init__(self,results_path,**kwargs):
        self.results_path=results_path
        #keywrod arguments
        options={#parse data options
                 'TruncateMode':'percent', #either 'below_x' or 'percent' for method of truncation. 
                 'Log10':'true',
                 'parse_mode':'folder',
                 'FromPickle':'true',
                 #truncate data options
                 'X':100,           #if below_x: this is the X boundary. If percent: this is the percent of data to keep
                 #graph options
                 'AxisSize':15,
                 'Show':'false',
                 'FontSize':22,
                 'Color':'red',
                 'XRotation':90,
                 'TitleWrapSize':35,
                 'SaveFig':'false',
                 'DPI':125,
                 'ExtraTitle':None,
                 'CustomTitle':None,
                 #boxplot specific options
                 'NumPerPlot':None,
                 'ResultsDirectory':None,
                 
                     }
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TruncateData'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        assert self.kwargs.get('TruncateMode') in ['below_x','percent']
        
        if self.kwargs.get('CustomTitle')!=None:
            assert isinstance(self.kwargs.get('CustomTitle'),str)
        #Other classes
        self.PED=ParsePEData(self.results_path)
        #create a directory and change to it
        if self.kwargs['ResultsDirectory']==None:
            self.results_dir=os.path.join(os.path.dirname(self.results_path),'Boxplots')
        else:
            self.results_dir=self.kwargs['ResultsDirectory']
        if os.path.isdir(self.results_dir)!=True:
            os.mkdir(self.results_dir)
        os.chdir(self.results_dir)
        
        #attributes
        self.data=self.PED.data
        self.log_data=self.PED.log_data
        self.truncated_data=self.truncate_data()
        if self.kwargs.get('NumPerPlot')==None:
            self.kwargs['NumPerPlot']=self.truncated_data.shape[1]
        self.boxplot()

    def list_parameters(self):
        return self.data.keys()
    
        
    def truncate_data(self):
        if self.kwargs.get('Log10')=='false':
            TC=TruncateData(self.data,mode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
        elif self.kwargs.get('Log10')=='true':
            TC=TruncateData(self.log_data,TruncateMode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
            
    def divide_data(self):
        n_vars=len(self.truncated_data.keys())
        n_per_plot= self.kwargs.get('NumPerPlot')
#        assert n_per_plot<n_vars,'number of variables per plot must be smaller than the number of variables'
        int_division= n_vars//n_per_plot
        remainder=n_vars-(n_per_plot*int_division)
        l=[]
        for i in range(int_division):
            l.append(self.truncated_data.keys()[i*n_per_plot:(i+1)*n_per_plot])
        l.append(self.truncated_data.keys()[-remainder:])
        return [list(i) for i in l]
        

    def boxplot(self):
        '''
        
        '''
        matplotlib.rcParams.update({'font.size':self.kwargs.get('AxisSize')}) 
        labels=self.divide_data()
        for i in range(len(labels)):
            plt.figure()
#            data= self.truncated_data[labels[i]]
            self.truncated_data[labels[i]].boxplot(rot=self.kwargs.get('XRotation'),return_type='axes')
            #pretty stuff
            ax=plt.subplot(1,1,1)
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            ax.spines['left'].set_smart_bounds(True)
            ax.spines['bottom'].set_smart_bounds(True)
            
            #labels
            if self.kwargs.get('CustomTitle')==None:
                plt.title('\n'.join(wrap('Distribution of parameter values from {} PE runs'.format(self.truncated_data.shape[0]),
                                     self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))
            else:
                plt.title('\n'.join(wrap(self.kwargs.get('CustomTitle'),self.truncated_data.shape[0]),
                                         self.kwargs.get('TitleWrapSize')),fontsize=self.kwargs.get('FontSize'))

            if self.kwargs.get('Log10')=='true':
                plt.ylabel('Parameter Values (Log10)',fontsize=self.kwargs.get('FontSize'))
            else:
                plt.ylabel('Parameter Values',fontsize=self.kwargs.get('FontSize'))

            plt.xticks(rotation=self.kwargs.get('XRotation'))
            
    #        SaveFig options
            if self.kwargs.get('SaveFig')=='true':
                if self.kwargs.get('ExtraTitle')!=None:
                    assert isinstance(self.kwargs.get('ExtraTitle'),str),'extra title should be a string'
                    plt.savefig('boxplot_{}'.format(i)+'_'+self.kwargs.get('ExtraTitle')+'.jpeg',bbox_inches='tight',format='jpeg',dpi=self.kwargs.get('DPI'))
                else:
                    plt.savefig('boxplot_{}'.format(i)+'.jpeg',format='jpeg',bbox_inches='tight',dpi=self.kwargs.get('DPI'))
            if self.kwargs.get('Show')=='true':
                plt.show()
                


                
#==============================================================================    
class PlotHeatMap():
    '''
    Plot Pearsons correlation as heat map. Still under development. 
    '''
    def __init__(self,copasi_file,results_path,**kwargs):
        self.copasi_file=copasi_file
        self.results_path=results_path
        #keywrod arguments
        options={#parse data options
                 'FromPickle':'false',
                 'TruncateMode':'below_x', #either 'below_x' or 'percent' for method of truncation. 
                 'Log10':'true',
                 'parse_mode':'folder',
                 #truncate data options
                 'X':100,           #if below_x: this is the X boundary. If percent: this is the percent of data to keep
                 #graph options
                 'AxisSize':8,
                 'Show':'false',
                 'FontSize':22,
                 'Color':'red',
                 'XRotation':90,
                 'TitleWrapSize':35,
                 'SaveFig':'false',
                 'DPI':300,
                 'ExtraTitle':None,
                 #boxplot specific options
                 'sym':'true',
                 'grid':'true',
                 
                     }
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TruncateData'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        assert self.kwargs.get('TruncateMode') in ['below_x','percent']
        
        #Other classes
        self.PED=ParsePEData(self.copasi_file,self.results_path,
                             mode=self.kwargs.get('parse_mode'),
                             FromPickle=self.kwargs.get('FromPickle'),
                             Log10=self.kwargs.get('Log10'))
        #create a directory and change to it
        self.cwd=self.PED.cwd
        self.results_dir=os.path.join(self.cwd,'HeatMaps')
        if os.path.isdir(self.results_dir)!=True:
            os.mkdir(self.results_dir)
        os.chdir(self.results_dir)
        



        #attributes
        self.data=self.PED.data
        self.log_data=self.PED.log_data
        self.truncated_data=self.truncate_data()
        if self.kwargs.get('NumPerPlot')==None:
            self.kwargs['NumPerPlot']=self.truncated_data.shape[1]
        self.boxplot()

    def list_parameters(self):
        return self.data.keys()
    
        
    def truncate_data(self):
        if self.kwargs.get('Log10')=='false':
            TC=TruncateData(self.data,mode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
        elif self.kwargs.get('Log10')=='true':
            TC=TruncateData(self.log_data,TruncateMode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
            
    def divide_data(self):
        n_vars=len(self.truncated_data.keys())
        n_per_plot= self.kwargs.get('NumPerPlot')
#        assert n_per_plot<n_vars,'number of variables per plot must be smaller than the number of variables'
        int_division= n_vars//n_per_plot
        remainder=n_vars-(n_per_plot*int_division)
        l=[]
        for i in range(int_division):
            l.append(self.truncated_data.keys()[i*n_per_plot:(i+1)*n_per_plot])
        l.append(self.truncated_data.keys()[-remainder:])
        return [list(i) for i in l]



    def get_variance(self):
        print 







            
class GetCovarianceMatrix():
    '''
    Might be useful somewhere but still under development. 
    '''
    def __init__(self,copasi_file,results_path,**kwargs):
        self.copasi_file=copasi_file
        self.results_path=results_path
        #keywrod arguments
        options={#parse data options
                 'FromPickle':'false',
                 'TruncateMode':'below_x', #either 'below_x' or 'percent' for method of truncation. 
                 'Log10':'true',
                 'parse_mode':'folder',
                 #truncate data options
                 'X':100,           #if below_x: this is the X boundary. If percent: this is the percent of data to keep
                     }
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TruncateData'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        assert self.kwargs.get('parse_mode') in ['folder','file']
        
#        Other classes
        self.PED=ParsePEData(self.copasi_file,self.results_path,
                             mode=self.kwargs.get('parse_mode'),
                             FromPickle=self.kwargs.get('FromPickle'),
                             Log10=self.kwargs.get('Log10'))
#                             
    def get_covariance(self):
        print self.PED

class EvaluateOptimizationPerformance():
    '''
    Plot your data RSS Vs Rank of best fit as evaluated by RSS value. This should
    highlight whether your optimization is finding a minimum and also help map 
    your local and (apparant) global minimum.
    
    Args:
        results_path. File or folder of files containing parameter estimation 
        data
        
    **kwargs: 
        Same as for the other classes in PEAnalaysis
    '''
    def __init__(self,results_path,**kwargs):
        self.results_path=results_path
        #keywrod arguments
        options={#parse data options
                 'TruncateMode':'percent', #either 'below_x' or 'percent' for method of truncation. 
                 'Log10':'true',
                 #truncate data options
                 'X':100,           #if below_x: this is the X boundary. If percent: this is the percent of data to keep
                 #graph options
                 'AxisSize':15,
                 'Show':'false',
                 'FontSize':22,
                 'Color':'red',
                 'XRotation':90,
                 'TitleWrapSize':35,
                 'SaveFig':'false',
                 'DPI':300,
                 'ExtraTitle':None,
                 'CustomTitle':None,
                 'ResultsDirectory':None,
                 
                     }
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TruncateData'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        assert self.kwargs.get('TruncateMode') in ['below_x','percent']
        
        
        #Other classes
        self.PED=ParsePEData(self.results_path)
        
        #create a directory and change to it
        if self.kwargs['ResultsDirectory']==None:
            self.results_dir=os.path.join(os.path.dirname(self.results_path),'OptimizationPerformanceGraph')
        else:
            self.results_dir=self.kwargs['ResultsDirectory']
        if os.path.isdir(self.results_dir)!=True:
            os.mkdir(self.results_dir)
        os.chdir(self.results_dir)
        
        ## Set size of axes font
        matplotlib.rcParams.update({'font.size':self.kwargs.get('AxisSize')})
        
        
        self.plot_rss()
        os.chdir(os.path.dirname(self.results_path))
                             
    def plot_rss(self):

        if self.kwargs.get('Log10')=='true':
            data=TruncateData(self.PED.log_data,TruncateMode=self.kwargs['TruncateMode'],X=self.kwargs['X']).data
            rss=data['RSS']
            iterations=numpy.log10(range(len(rss)))
        else:
            data=TruncateData(self.PED.data,TruncateMode=self.kwargs['TruncateMode'],X=self.kwargs['X']).data
            rss= data['RSS']
            iterations=range(len(rss))

            
        plt.figure()
        plt.plot(iterations,rss)
        
        #pretty stuff
        ax=plt.subplot(1,1,1)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_smart_bounds(True)
        ax.spines['bottom'].set_smart_bounds(True)
        
        #labels
        if self.kwargs.get('CustomTitle')==None:
            plt.title('\n'.join(wrap('RSS values for {} iterations'.format(len(rss)),
                                 self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))
        else:
            plt.title('\n'.join(wrap(self.kwargs.get('CustomTitle'),self.truncated_data.shape[0]),
                                     self.kwargs.get('TitleWrapSize')),fontsize=self.kwargs.get('FontSize'))

        if self.kwargs.get('Log10')=='true':
            plt.ylabel('RSS Values (Log10)',fontsize=self.kwargs.get('FontSize'))
            plt.xlabel('Rank of Best Fit (Log10)',fontsize=self.kwargs.get('FontSize'))
        else:
            plt.ylabel('Optimization Iteration',fontsize=self.kwargs.get('FontSize'))
            plt.xlabel('Rank of Best Fit',fontsize=self.kwargs.get('FontSize'))
            
        plt.xticks(rotation=self.kwargs.get('XRotation'))
        
        if self.kwargs['Log10']=='true':
            self.kwargs['ExtraTitle']='(Log10)'
        
#        SaveFig options
        if self.kwargs.get('SaveFig')=='true':
            if self.kwargs.get('ExtraTitle')!=None:
                if isinstance(self.kwargs.get('ExtraTitle'),str)==False:
                    raise Errors.InputError('extra title should be a string')
                plt.savefig('RSSVsITerations'+'_'+self.kwargs.get('ExtraTitle')+'.jpeg',bbox_inches='tight',format='jpeg',dpi=self.kwargs.get('DPI'))
            else:
                plt.savefig('RSSVsITerations'+'.jpeg',format='jpeg',bbox_inches='tight',dpi=self.kwargs.get('DPI'))
        if self.kwargs.get('Show')=='true':
            plt.show()

#==============================================================================


class PlotPEData():
    '''
    Plot a parameter estimation run against experimental data. 
    Suport currently only exists for time course experiments. In future versions
    a SteadyState Task will be introduced and then we can build a plotting feature
    for fitting steady state experiments
    
    Positional Arguments:
    
        copasi_file:
            The copasi file you want to enter parameters into
            
        experiment_files
        
        PE_result_files
    
    **Kwargs
        Index:
            Index of parameter estimation run to input into the copasi file. 
            The index is ordered by rank of best fit, with 0 being the best.
            Default=0            
            
        PruneHeaders:
            Prune copasi variable names of Copasi references. 'true' or 'false'
            
        QuantityType:
            Either 'particle_number' or 'concentration'. Default='concentration'
            
        OutputML:
            If Save set to 'duplicate', this is the duplicate filename. 
            
        Save:
            either 'false','overwrite' or 'duplicate'
            
        ParameterDict:
            A python dictionary with keys correponding to parameters in the model
            and values the parameters (dict[parameter_name]=parameter value). 
            Default=None
            
        DF:
            A pandas dataframe with parameters being column names matching 
            parameters in your model and RSS values and rows being individual 
            parameter estimationruns. In this case, ensure you have set the 
            Index parameter to the index you want to use. Dataframes are 
            automatically sorted by the RSS column. 
            
        ParameterPath:
            Full path to a parameter estimation file ('.txt','.xls','.xlsx' or 
            '.csv') or a folder containing parameter estimation files. 
            
        OutputDirectory:
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
                 'ReportName':default_report_name,
                 'OutputML':default_outputML,
                 'Save':'overwrite',
                 'Index':0,
                 'LineWidth':4,
                 'PruneHeaders':'true',
                 
                 #graph features
                 'FontSize':22,
                 'AxisSize':15,
                 'ExtraTitle':None,
                 'Show':'false',
                 'MultiPlot':'false',
                 'SaveFig':'false',
                 'TitleWrapSize':30,
                 'Ylimit':None,
                 'Xlimit':None,
                 'DPI':125,
                 'XTickRotation':35,
                 'DotSize':4,
                 'LegendLoc':'best',
                 'OutputDirectory':os.path.join(os.path.dirname(self.copasi_file),'ParameterEstimationPlots'),
                 'Plot':'true',                 
                 
                 }
                 
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for Plot'.format(i)
        options.update( kwargs) 
        self.kwargs=options       
        
        
        if self.kwargs.get('Plot') not in ['false','true']:
            raise Errors.InputError('The Plot kwarg takes only \'false\' or \'true\'')
        #limit parameters
        if self.kwargs.get('Ylimit')!=None:
            assert isinstance(self.kwargs.get('Ylimit'),list),'Ylimit is a list of coordinates for y axis,i.e. [0,10]'
            assert len(self.kwargs.get('Ylimit'))==2,'length of the Ylimit list must be 2'
        
        if self.kwargs.get('Xlimit')!=None:
            assert isinstance(self.kwargs.get('Xlimit'),list),'Xlimit is a list of coordinates for X axis,i.e. [0,10]'
            assert len(self.kwargs.get('Xlimit'))==2,'length of the Xlimit list must be 2'
        
        assert isinstance(self.kwargs.get('XTickRotation'),int),'XTickRotation parameter should be a Python integer'

        
        if self.kwargs.get('ExtraTitle')!=None:
            assert isinstance(self.kwargs.get('ExtraTitle'),str)
        assert isinstance(self.kwargs.get('FontSize'),int)
        assert isinstance(self.kwargs.get('AxisSize'),int)
        assert isinstance(self.kwargs.get('LineWidth'),int)

        assert isinstance(self.kwargs.get('TitleWrapSize'),int)

        if self.kwargs.get('Ylimit')!=None:
            assert isinstance(self.kwargs.get('Ylimit'),str)
            
        if self.kwargs.get('Xlimit')!=None:
            assert isinstance(self.kwargs.get('Xlimit'),str)
            
            
        assert isinstance(self.kwargs.get('DPI'),int)
        assert isinstance(self.kwargs.get('XTickRotation'),int)
    
        assert self.kwargs.get('Show') in ['false','true']
        assert self.kwargs.get('SaveFig') in ['false','true']
        assert self.kwargs.get('MultiPlot') in ['false','true']                
                     
        assert self.kwargs.get('PruneHeaders') in ['false','true']                
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
        
        matplotlib.rcParams.update({'font.size':self.kwargs.get('AxisSize')})
        
        self.experiment_data=self.parse_experimental_files()
#        print self.experiment_data
        self.exp_times=self.get_experiment_times()
        self.parameters=self.parse_parameters()
        self.insert_parameters()
        self.sim_data=self.simulate_time_course()
##        '''
##        Only change directory before doing the actual plotting. 
##        You want to be in the model directory for all the while your collecting
##        data then move on over to the results directory when plotting. 
##        '''
        if self.kwargs.get('Plot')=='true':
            self.change_directory()
            self.plot()
        os.chdir(os.path.dirname(self.copasi_file))
        
        
    def change_directory(self):
        dire=os.path.join(os.path.dirname(self.copasi_file),'ParameterEstimationPlots')
        if os.path.isdir(dire)==False:
            os.mkdir(dire)
        os.chdir(dire)
        return dire
        
        
    def parse_experimental_files(self):
        df_dct={}
        for i in self.experiment_files:
            df=pandas.read_csv(i,sep='\t')
            df_dct[i]=df
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
            times[i]['Start']=d[i].iloc[0]
            times[i]['End']=d[i].iloc[-1]
            times[i]['StepSize']=d[i].iloc[1]-d[i].iloc[0]
            '''
            subtract 1 from intervals to account for header
            '''
            times[i]['Intervals']=int(d[i].shape[0])-1
        return times
        
    def parse_parameters(self):
        if self.kwargs.get('PruneHeaders')=='true':
            pycopi.PruneCopasiHeaders(self.PE_result_file,replace='true')
        df= pandas.read_csv( self.PE_result_file,sep='\t')
        df=ParsePEData(self.PE_result_file)
        df= df.data
        print self.PE_result_file
        return pandas.DataFrame(df.iloc[-1]).transpose()
    
    def insert_parameters(self):
        pycopi.InsertParameters(self.copasi_file,DF=self.parameters,Save='overwrite')
        return self.copasi_file
        
        
    def simulate_time_course(self):
        data_dct={}
        for i in self.exp_times:
            '''
            need to subtract 1 from the intervals
            '''
            TC=pycopi.TimeCourse(self.copasi_file,Start=self.exp_times[i]['Start'],
                          End=self.exp_times[i]['End'],
                          Intervals=self.exp_times[i]['Intervals'],
                          StepSize=self.exp_times[i]['StepSize'],Plot='false')
            P=pycopi.PruneCopasiHeaders(TC.data,replace='true')
            data_dct[i]=P.df
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
#                          StepSize=1,Plot='false')
#            P=pycopi.PruneCopasiHeaders(TC.data,replace='true')
#            data_dct[i]=P.df
#        return data_dct
        
        
                            
    def plot1(self,fle,parameter):
        '''
        Plot one parameter of one experiment. for iterating over in 
        other functions
        '''
        if fle not in self.experiment_files:
            raise Errors.InputError('{} not in {}'.format(fle,self.exp_times))
        if parameter not in self.sim_data[fle].keys() and parameter not in self.experiment_data[fle].keys():
            raise Errors.InputError('{} not in {} or {}'.format(parameter,self.sim_data[fle.keys()],self.experiment_data[fle].keys()))
        sim= self.sim_data[fle][parameter]
        exp= self.experiment_data[fle][parameter]
        time=self.sim_data[fle]['Time']
        plt.figure()
        ax = plt.subplot(111)
        plt.plot(time,sim,'k-',label='simulated',linewidth=self.kwargs.get('LineWidth'))
        plt.plot(time,exp,'ro',label='experimental',markersize=self.kwargs.get('DotSize'))
        plt.legend(loc=self.kwargs.get('LegendLoc'))


   
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
        
        plt.title('\n'.join(wrap('{}'.format(parameter),self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))
        try:
            plt.ylabel('Quantity Unit ({})'.format(self.GMQ.get_quantity_units().encode('ascii')),fontsize=self.kwargs.get('FontSize'))
        except UnicodeEncodeError:
            plt.ylabel('Quantity Unit (micromol)',fontsize=self.kwargs.get('FontSize'))
                        
        plt.xlabel('Time ({})'.format(self.GMQ.get_time_unit()),fontsize=self.kwargs.get('FontSize'))  


        for j in parameter:
            if j not in string.ascii_letters+string.digits+'_-[]':
                parameter=parameter.replace(j,'_')
                
#        parameter=re.sub(p,'_',parameter) 
                                
                                
                                
        if self.kwargs.get('SaveFig')=='true':
            if self.kwargs.get('ExtraTitle')!=None:
                assert isinstance(self.kwargs.get('ExtraTitle'),str),'extra title should be a string'
                fle=os.path.join(self.kwargs.get('OutputDirectory'),'{}_{}.jpeg'.format(parameter,self.kwargs.get('ExtraTitle')))                
            else:
                fle=os.path.join(self.kwargs.get('OutputDirectory'),'{}.jpeg'.format(parameter))
            plt.savefig(fle,dpi=self.kwargs.get('DPI'),bbox_inches='tight')

        if self.kwargs.get('Show')=='true':
            plt.show()             
        
        
    def plot1file(self,fle):
        '''
        plot only parameters from a single experiment file
        (for the event that the user has multiple time course
        experiments)
        '''
        for parameter in  self.experiment_data[fle]:
            if parameter !='Time':
                self.plot1(fle,parameter)
        
    def plot(self):
        '''
        Plot all parameters
        '''
        for f in self.experiment_files:
            dire,p= os.path.split(f)
            fle=os.path.splitext(p)[0]
            self.plot1file(f)
            
            
            
class PlotHistogram3D():
    '''
    Not functional 
    
    
    
    
    Plot parameter estimation results as histogram
    Args:
        results_path:
            Path to file or folder of files containing parameter estimation data
            to plot
    **kwargs:
         TruncateMode:
             'below_x', #either 'below_x' or 'percent' for method of truncation. 
         Log10:
             'false',
         X:
             100,           #if below_x: this is the X boundary. If percent: this is the percent of data to keep
    **kwargs which correspond to matplotlib.pyplot.hist keyword arguments. 
    More information about these can be found in the matplotlib documentation 
         Bins:
             Number of bins to use. Default=100,
         AxisSize:
             Font size for the axis. Default=15
         FontSize:
             Font size for the graph labels. Default=22
         Normed:
             'true' or 'false. Whether to make the plot integrate to 1. 
             Default='false'
         Color:
             Plot colour. Default='red',     
         XRotation:
             25,   #rotation for X tick axis
         TitleWrapSize:
             Number of characters to use before word wrapping the title. Default=35  
         Orientation:
             'horizontal' or 'vertical', default='vertical'
         SaveFig:
             'true' or 'false'. Save to a folder called histograms in results directory. 
             Default='false'
         DPI:
             Resolution to use when SaveFig='true'. The larger this value the 
             higher the resolution. Default=125. 
         ExtraTitle:
             When SaveFig='true', save with ExtraTitle appended to the filepath. 
             Default=None
         Show:
             'true' or 'false'. When not using iPython and graphs are not automatically 
             displayed in shell, this determines whether the plots are opened in a
             window or not. Default='false'
                     
                 
    '''
    def __init__(self,results_path,**kwargs):
        #arguments
#        self.copasi_file=copasi_file
        self.results_path=results_path
        #keywrod arguments
        options={'FromPickle':'false',
                 'TruncateMode':'percent', #either 'below_x' or 'percent' for method of truncation. 
                 'Log10':'false',
                 'X':100,           #if below_x: this is the X boundary. If percent: this is the percent of data to keep
                 'Bins':100,
                 'AxisSize':15,
                 'FontSize':22,
                 'Normed':'false',
                 'Color':'red',
                 'XRotation':25,
                 'TitleWrapSize':35,
                 'Orientation':'vertical',
                 'SaveFig':'false',
                 'DPI':125,
                 'ExtraTitle':None,
                 'Log10':'false',
                 'Show':'false',
                 'Variable':None,
                 
                     }
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TruncateData'.format(i)
        options.update( kwargs)  
        self.kwargs=options
        assert self.kwargs.get('TruncateMode') in ['below_x','percent']
        
        #Other classes
        self.PED=ParsePEData(self.results_path)

        #create a directory and change to it
        self.results_dir=os.path.join(os.path.dirname(self.results_path),'Histograms')
        if self.kwargs.get('SaveFig')=='true':
            if os.path.isdir(self.results_dir)!=True:
                os.mkdir(self.results_dir)
            os.chdir(self.results_dir)
        
        #attributes
        self.data=self.PED.data.dropna()
        self.log_data=self.PED.log_data.dropna()
        self.truncated_data=self.truncate_data()
        #main method
        print self.list_parameters()
        self.plot1()
#        self.testing_variable=self.plot_all() #only assigned to variable for testing purposes
#        os.chdir(os.path.dirname(self.results_dir))
            
    def list_parameters(self):
        return self.data.keys()
    
    def truncate_data(self):
        if self.kwargs.get('Log10')=='false':
#            print '1'
            TC=TruncateData(self.data,TruncateMode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
        elif self.kwargs.get('Log10')=='true':
#            print '2'
            TC=TruncateData(self.log_data,TruncateMode=self.kwargs.get('TruncateMode'),X=self.kwargs.get('X'))
            return TC.data
        
    def plot1(self,variable='RSS'):
        '''
        variable: variable to plot. Default= 'RSS'
        '''
        matplotlib.rcParams.update({'font.size': 22})
        assert variable in self.truncated_data.keys(),'{} is not in your PE results: {}'.format(variable,self.truncated_data.keys())
        data= self.truncated_data[variable]
        fig=plt.figure()
        Axes3D.plot_surface()
        
#        plt.hist(data,
#                 bins=self.kwargs.get('Bins'),
#                 color=self.kwargs.get('Color'),
#                 normed=self.kwargs.get('Normed'),
#                 orientation=self.kwargs.get('Orientation'))
#        
#        #pretty stuff
#        ax=plt.subplot(1,1,1)
#        ax.spines['right'].set_color('none')
#        ax.spines['top'].set_color('none')
#        ax.xaxis.set_ticks_position('bottom')
#        ax.yaxis.set_ticks_position('left')
#        ax.spines['left'].set_smart_bounds(True)
#        ax.spines['bottom'].set_smart_bounds(True)
#        
#        #labels
##        plt.title('\n'.join(wrap('{},n={}'.format(variable,self.data.shape[1])) ),35  )
#        plt.title('\n'.join(wrap('{},n={}'.format(variable,data.shape[0]),
#                                 self.kwargs.get('TitleWrapSize'))),
#                                 fontsize=self.kwargs.get('FontSize'))
#        plt.ylabel('Frequency in bin')
#        plt.xticks(rotation=self.kwargs.get('XRotation'))
#        if self.kwargs.get('Log10')=='true':
#            plt.xlabel('Parameter Value(Log10)',fontsize=self.kwargs.get('FontSize'))
#        else:
#            plt.xlabel('Parameter Value',fontsize=self.kwargs.get('FontSize'))
#        
#        #SaveFig options
#        if self.kwargs.get('SaveFig')=='true':
#            if self.kwargs.get('ExtraTitle')!=None:
#                assert isinstance(self.kwargs.get('ExtraTitle'),str),'extra title should be a string'
#                plt.savefig(variable+'_'+self.kwargs.get('ExtraTitle')+'.jpeg',bbox_inches='tight',format='jpeg',dpi=self.kwargs.get('DPI'))
#            else:
#                plt.savefig(variable+'.jpeg',format='jpeg',bbox_inches='tight',dpi=self.kwargs.get('DPI'))
#        if self.kwargs.get('Show')=='true':
#            plt.show()
#    
#    def plot_all(self):
#        for i in self.truncated_data:
#            self.plot1(i)
#        return True


if __name__=='__main__':
    pass
#    current_directory='D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools\PyCoTools\Examples\GoldbetterExample'
#    copasi_file=r'Goldbeter1995_CircClock.cps'
#    goldbetter_model=os.path.join(current_directory,copasi_file)
#    report=os.path.join(current_directory,'TimeCourseOutput.txt')
#    noisy_report=os.path.join(current_directory,'NoisyTimeCourseOutput.txt')
#    
#    EvaluateOptimizationPerformance(noisy_report)
#    PEData_report=os.path.join(current_directory,'PEData.txt')
    
    
#    print ParsePEData(PEData_report).data





