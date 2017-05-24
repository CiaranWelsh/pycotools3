# -*- coding: utf-8 -*-
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


 This file is intended to provide a COPASI user an alternative to 
 using the official python-copasi API. At present support is 
 provided for:
     -running time courses
     -performing parameter estimation
     -performing parameter scans
     -extracting model variables and quantities
     -creating reports (for parameter estimation, 
     profile likelihood and time course)
     -inserting parameters from file, folder of files, pandas dataframe
     or python dictionary
     


 $Author: Ciaran Welsh
 $Date: 12-09-2016 
 Time:  13:33

'''
import time
import threading
import Queue
import shutil
import numpy 
import pandas
import scipy
import os
from lxml import etree
import logging
import os
import subprocess
import re
import pickle
import PEAnalysis,Errors
import matplotlib
import matplotlib.pyplot as plt
from textwrap import wrap
import string
import itertools
from  multiprocessing import Process
import glob
import seaborn as sns
from copy import deepcopy
from subprocess import check_call




LOG=logging.getLogger(__name__)
sns.set_context(context='poster',
                font_scale=3)

#==========================================================================

class CopasiMLParser():
    '''
    Parse a copasi file into xml.etree. 
    The copasiML is availbale as the copasiML attribute.
    
    args:
        copasi_file:
            A full path to a copasi file
        

    '''
    def __init__(self,copasi_file):
        self.copasi_file=copasi_file
        if os.path.isfile(self.copasi_file)!=True:
            raise Errors.FileDoesNotExistError('{} is not a copasi file'.format(self.copasi_file))
        self.copasiMLTree=self._parse_copasiML()
        self.copasiML=self.copasiMLTree.getroot()
        
        
        '''
        Recently changed this class to use lxml built in functions
        rather that pythons standard write and read methods. Hopefully this
        should help some of the performance issues. The below two comments are required for
        the old class. Keep them commented out until you remove the deprecations fully 
        '''
        #self.dir=os.path.dirname(self.copasi_file)
        os.chdir(os.path.dirname(self.copasi_file))
        
        
    def _parse_copasiML_deprecated(self):
        '''
        deprecated in favor of using etree.parse
        '''
        with open(self.copasi_file) as f:
            copasiML_str=f.read()
        return etree.fromstring(copasiML_str)
        


    def write_copasi_file_deprecated(self,copasi_filename,copasiML):
        '''
        Often you need to delete a copasi file and rewrite it
        directly from the string. This function does this.
        
        copasi_filename = a valid .cps file
        copasiML = an xml string. Convert to xml string
        before using this function using etree.fromstring(xml_string)
        '''
        if os.path.isfile(copasi_filename):
            os.remove(copasi_filename)
        with open(copasi_filename,'w') as f:
            f.write(etree.tostring(copasiML,pretty_print=True))    
            
    def _parse_copasiML(self):
        '''
        Parse xml doc with lxml 
        '''
        tree= etree.parse(self.copasi_file)
        LOG.debug('copasi file {} has been parsed into Python'.format(os.path.split(self.copasi_file)[1]))
        return tree
            
    def write_copasi_file(self,copasi_filename,copasiML):
        '''
        write to file with lxml write function

        '''
        #first convert the copasiML to a root element tree
        root=etree.ElementTree(copasiML)
        root.write(copasi_filename)
        LOG.debug('File {} written to \n{}'.format(os.path.split(self.copasi_file)[1],copasi_filename))
            
#==============================================================================

class GetModelQuantities():
    '''
    Positional arguments:
        copasi_file:
            Full path to copasi file
            
            
    keywords:
        Quantitytype:
            either 'concentration' (default) or 'particle_numbers'. 
    '''
    
    def __init__(self,copasi_file,QuantityType='concentration'):
        self.copasi_file=copasi_file
        self.QuantityType=QuantityType

        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML
                
#        self.all_params=self.get_global_quantities_cns().keys()+self.get_IC_cns().keys()+self.get_local_kinetic_parameters_cns().keys()
        assert self.QuantityType in ['concentration','particle_number']
        
    def convert_particles_to_molar(self,particles,mol_unit,compartment_volume):#,vol_unit):
        '''
        Converts particle numbers to Molarity. 
        particles=number of particles you want to convert
        mol_unit=one of, 'fmol, pmol, nmol, umol, mmol or mol'
        '''
        mol_dct={
            'fmol':1e-15,
            'pmol':1e-12,
            'nmol':1e-9,
            u'\xb5mol':1e-6,
            'mmol':1e-3,
            'mol':float(1),
            'dimensionless':float(1),
            '#':float(1)}
        mol_unit_value=mol_dct[mol_unit]
        avagadro=6.02214179e+023
        molarity=float(particles)/(avagadro*mol_unit_value*compartment_volume)
        if mol_unit=='dimensionless':
            molarity=float(particles)
        if mol_unit=='#':
            molarity=float(particles)
        return round(molarity,33)
        
        
        
    def convert_molar_to_particles(self,moles,mol_unit,compartment_volume):
        '''
        Converts particle numbers to Molarity. 
        particles=number of particles you want to convert
        mol_unit=one of, 'fmol, pmol, nmol, umol, mmol or mol'
        '''
        if isinstance(compartment_volume,(float,int))!=True:
            raise Errors.InputError('compartment_volume is the volume of the compartment for species and must be either a float or a int')

        mol_dct={
            'fmol':1e-15,
            'pmol':1e-12,
            'nmol':1e-9,
            u'\xb5mol':1e-6,
            'mmol':1e-3,
            'mol':float(1),
            'dimensionless':1,
            '#':1}
        mol_unit_value=mol_dct[mol_unit]
        avagadro=6.02214179e+023
        particles=float(moles)*avagadro*mol_unit_value*compartment_volume
        if mol_unit=='dimensionless':# or '#':
            particles=float(moles)
        if mol_unit=='#':
            particles=float(moles)
        return particles        

    def get_quantity_units(self):
        '''
        Get model quantity units (nM for example)
        '''
        query="//*[@avogadroConstant]"
        for i in self.copasiML.xpath(query):
            quantity_unit= i.attrib['quantityUnit']
        return quantity_unit
        
    def get_volume_unit(self):
        '''
        get model volume units. ml for example
        '''
        query="//*[@avogadroConstant]"
        for i in self.copasiML.xpath(query):
            vol_unit= i.attrib['volumeUnit']
        return vol_unit
        
    def get_time_unit(self):
        '''
        get model time units
        '''
        query="//*[@avogadroConstant]"
        for i in self.copasiML.xpath(query):
            time_unit= i.attrib['timeUnit']
        return time_unit
        
    def check_ascii(self,string):
        '''
        Non-ascii characters are not currently supported. 
        Check for non-ascii characters
        
        '''
        for i in string:
            if Errors.IncompatibleStringError().is_ascii(i)==False:
                raise Errors.IncompatibleStringError('Your model name contains non-ascii characters which are not currently supported by PyCoTools.')
        return string
        
    def get_model_name(self):
        '''
        get model name
        '''
        query="//*[@avogadroConstant]"
        for i in self.copasiML.xpath(query):
            name= i.attrib['name']
        name=self.check_ascii(name)            
        return name     
        
        


    def get_model_name_cn(self):
        '''
        get reference to model name
        '''
        first= self.get_IC_cns().keys()[0]
        string= self.get_IC_cns()[first]['cn']
        string=self.check_ascii(string)
        return re.findall('Model=(.*),Vector=C',string)[0]
        
    def get_metabolites(self):
        '''
        Deprecated. Use get_ICs_cns() inst
        returns dict of metabolites in the 'species' menu
        '''
        metab_dct={}
        query='//*[@cn="String=Initial Species Values"]'
        for i in self.copasiML.xpath(query):
            for j in list(i):
                match=re.findall('.*Vector=Metabolites\[(.*)\]',j.attrib['cn'])
                                
                if match==[]:
                    return self.copasiML
                else:
                    compartment_match=re.findall('Compartments\[(.*)\],',j.attrib['cn'])
                    
                    comp=re.findall('Compartments\[(.*?)\]',j.attrib['cn'])[0]
                    if self.QuantityType=='concentration':
                        compartment_vol= float(self.get_compartments()[comp]['value'])
                    else:
                        compartment_vol=1
                    metab_dct[match[0]]={}
                    metab_dct[match[0]]['particle_numbers']=j.attrib['value']
                    concentration= self.convert_particles_to_molar(j.attrib['value'],self.get_quantity_units(),compartment_vol)
                    metab_dct[match[0]]['concentration']=concentration
                    metab_dct[match[0]]['compartment']=compartment_match[0]
        if len(metab_dct.keys())==0:
            raise Errors.NoMetabolitesError('There are no metabolites in {}'.format(self.get_model_name()))
        return metab_dct
        

    def get_global_quantities(self):
        '''
        returns a dict of global quantities
        '''
        query='//*[@cn="String=Initial Global Quantities"]'
        model_val_dct={}
        for i in self.copasiML.xpath(query):
            for j in list(i):
                match=re.findall('.*Values\[(.*)\]', j.attrib['cn'])
                if match==[]:
                    return self.copasiML
                else:
                    model_val_dct[match[0]]=j.attrib['value']
        return model_val_dct
#        
                        
    def get_local_parameters(self):
        '''
        return dict of local parameters used in your model
        '''
        query='//*[@cn="String=Kinetic Parameters"]'
        parameters={}
        for i in self.copasiML.xpath(query):
            for j in  list(i):
                for k in list(j):
                    if k.attrib['simulationType']=='fixed':
                        match= re.findall('.*\[(.*)\].*Parameter=(.*)',k.attrib['cn'])
                        if match==[]:
                            return False
                        parameters['({}).{}'.format(match[0][0],match[0][1])]=k.attrib['value']
        return parameters

    def get_compartments(self):
        '''
        returns a dict of compartments in your model
        '''
        d={}
        query='//*[@cn="String=Initial Compartment Sizes"]'
        for i in self.copasiML.xpath(query):
            for j in list(i):
                match=re.findall('Compartments\[(.*)\]', j.attrib['cn'])[0]
                d[match]= j.attrib
        return d
        
        
    def compartment_lookup(self,metab):
        '''
        metab=a single metabolite dict from the get_metabolites method
        look metab up in the compartment definitions 
        and get the name corresponding to it's key
        '''
        m_comp= metab['compartment']
        for i in self.get_compartments().keys():
            for j in  self.get_compartments()[i]:
                if self.get_compartments()[i][j]== m_comp:
                    return self.get_compartments()[i]['name']  

    def get_IC_cns(self):
        '''
        Get the xml segment for initial condition parameters. 
            
        '''
        query='//*[@cn="String=Initial Species Values"]'
        d={}
        for i in self.copasiML.xpath(query):
            for j in list(i):
                match= re.findall('Metabolites\[(.*)\]', j.attrib['cn'])[0]
                assert isinstance(match.encode('utf8'),str),'{} is not a string but a {}'.format(match,type(match))
                assert match !=None
                assert match !=[]  
                d[match]=j.attrib
                comp=re.findall('Compartments\[(.*?)\]',j.attrib['cn'])[0]
                if self.QuantityType=='concentration':
                    compartment_vol= float(self.get_compartments()[comp]['value'])
                else:
                    compartment_vol=1
                molar= self.convert_particles_to_molar(d[match]['value'],self.get_quantity_units(),compartment_vol)
                d[match]['concentration']=str(molar)
                d[match]['compartment']=str(comp)
                d[match]['compartment_volume']=str(compartment_vol)
        return d
        
        
    def get_global_quantities_cns(self):
        '''
        Get the xml segment for global kinetic parameters. 
        
        '''
        query='//*[@cn="String=Initial Global Quantities"]'
        d={}
        for i in self.copasiML.xpath(query):
            for j in list(i):
                match= re.findall('Values\[(.*)\]',j.attrib['cn'])[0]
                assert isinstance(match.encode('utf8'),str),'{} should be a string but is instead a {}'.format(match,type(match))
                assert match !=None
                assert match !=[]                
                d[match]=j.attrib
        return d
        
    def get_local_kinetic_parameters_cns(self,names_only=False):
        '''
        Get the xml segment for local kinetic parameters. 
            
        '''
        query='//*[@cn="String=Kinetic Parameters"]'
        d={}
        for i in self.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['simulationType']=='fixed':
                        match=re.findall('Reactions\[(.*)\].*Parameter=(.*)',k.attrib['cn'])[0]
                        assert isinstance(match,tuple),'get species regex hasn\'t been found. Do you have species in your model?'
                        assert match !=None
                        assert match !=[]                
                        assert len(match)==2
                        match='({}).{}'.format(match[0],match[1])
                        d[match]=k.attrib
        return d

    def get_global_kinetic_parameters_cns(self):
        '''
        Get the xml segment for global parameters that are used as
        kinetic parameters. 
        '''
        query='//*[@cn="String=Kinetic Parameters"]'
        d={}
        for i in self.copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['simulationType']=='assignment':
                        match=re.findall('Reactions\[(.*)\].*Parameter=(.*)',k.attrib['cn'])[0]
                        assert isinstance(match,tuple),'get species regex hasn\'t been found. Do you have species in your model?'
                        assert match !=None
                        assert match !=[]                
                        assert len(match)==2
                        match='({}).{}'.format(match[0],match[1])
                        d[match]=k.attrib
                        for l in list(k):
                            d[match]['mapping']=l.text
        return d
        
    def get_fit_items(self):
        '''
        return all parameters that are present in the fit items of the
        parameter estimation task
        '''
        d={}
        query='//*[@name="FitItem"]'
        for i in self.copasiML.xpath(query):
            for j in list(i):
                if j.attrib['name']=='ObjectCN':
                    match=re.findall('Reference=(.*)',j.attrib['value'])[0]
                    if match=='Value':
                        match2=re.findall('Reactions\[(.*)\].*Parameter=(.*),', j.attrib['value'])[0]
                        match2='({}).{}'.format(match2[0],match2[1])
                    elif match=='InitialValue':
                        match2=re.findall('Values\[(.*)\]', j.attrib['value'])[0]
                    elif match=='InitialConcentration':
                        match2=re.findall('Metabolites\[(.*)\]',j.attrib['value'])[0]
                    d[match2]=j.attrib    
        return d
        

    def get_all_model_variables(self):
        '''
        concatonate the output of the three functions that give model variables
        Return list
        '''
        g= self.get_global_quantities_cns()
        l=self.get_local_kinetic_parameters_cns()
        p= dict(l,**g)
        p=dict(p,**self.get_IC_cns())
        return p
        
    def get_experiment_files(self):
        '''
        Get any parameter estimation data files that are defined 
        within copasi parameter estimation task
        '''
        query='//*[@name="File Name"]'
        files=[]
        for i in self.copasiML.xpath(query):
            files.append(os.path.abspath(i.attrib['value']))
        return files
        
    def get_all_params_dict_deprecated(self):
        '''
        returns dict[parameter_name]=parameter_value for all local, 
        global and IC parameters in copasi_file
        
        Use get_all_model_variables
        '''
        var_dct={}
        d=self.get_all_model_variables()
        pattern='.*Values\[(.*)\]|.*Reactions\[(.*)\].*Parameter=(.*)|.*Metabolites\[(.*)\]'
        for i in d:
            match= re.findall(pattern,d[i]['cn'])
            l=[]
            for j in match[0]:
                if j!='':
                    l.append(j)
#            now format the local parameters
            local=False
            if len(l)==2:
                local=True
                local_param='({}).{}'.format(l[0],l[1])
                
            if local==True:
                var_dct[local_param]=d[i]['value']
            else:
                var_dct[l[0]]=d[i]['value']
        return var_dct
        
        
    def get_all_params_dict_deprecated2(self):
        '''
        returns dict[parameter_name]=parameter_value for all local, 
        global and IC parameters in copasi_file
        
        get_all_model_variables
        
        
        '''
        var_dct={}
        d=self.get_all_model_variables()
        pattern='.*Values\[(.*)\]|.*Reactions\[(.*)\].*Parameter=(.*)|.*Metabolites\[(.*)\]'
        for i in d:
            match= re.findall(pattern,d[i]['cn'])
            l=[]
            for j in match[0]:
                if j!='':
                    l.append(j)
#            now format the local parameters
            local=False
            if len(l)==2:
                local=True
                local_param='({}).{}'.format(l[0],l[1])
                
            if local==True:
                var_dct[local_param]=d[i]['value']
            else:
                if self.QuantityType=='concentration':
                    var_dct[l[0]]=d[i]['concentration']
                else:
                    var_dct[l[0]]=d[i]['value']
        return var_dct

#==============================================================================

class Reports():
    '''
    Creates reports in copasi output specification section. 
    Use: 
        -the ReportType kwarg to specify which type of report you want to make
        -the Metabolites and GlobalQuantities kwargs to specify which parameters
        to include
        
    
    
    args:
        copasi_file:
            The copasi file you want to add a report too
        
    **kwargs:

        ReportType: 
            Which report to write. Options:
                profilelikleihood:
                    - for Pydentify, shouldn't need to manually touch this
                time_course:
                    -a table of time Vs concentrations. Included values are specified to the Metabolites and//or GlobalQuantities arguments
            parameter_estimation:
                    -a table of values from a parameter estimation and the residual sum of squares value for each run. 

    
        Metabolites:
            A list of valid model metabolites you want to include in the report. Default=All metabolites
        
        GlobalQuantities;
            List of valid global quantities that you want to include in the report. Default=All global variables
        
        QuantityType:
            Either 'concentration' or 'particle_number'. Switch between having report output in either concentration of in particle_numbers. 

        ReportName:
            Name of the report. Default depends on kwarg ReportType
        
        Append: 
            'true' or 'false'. Append to report. Default 'false'
        
        ConfirmOverwrite: 
            'true' or 'false'.  Default= 'false'
        
        Save: 
            either 'false','overwrite' or 'duplicate'. 
            false: don't write to file
            overwrite: overwrite copasi_file
            duplicate: write a new file named using the kwarg OutputML
        
        OutputML: 
            When Save set to 'duplicate', this is the name of the file
        
            
        Variable: 
            When ReportType is profilelikelihood, theta is the parameter of interest
    
    '''
    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=GetModelQuantities(self.copasi_file)
        
#        default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_PE_results.txt'
        default_outputML=os.path.split(self.copasi_file)[1][:-4]+'_Duplicate.cps'
        options={#report variables
                 'Metabolites':self.GMQ.get_metabolites().keys(),
                 'GlobalQuantities':self.GMQ.get_global_quantities().keys(),
                 'LocalParameters':self.GMQ.get_local_kinetic_parameters_cns(),
                 'QuantityType':'concentration',
                 'ReportName':None,
                 'Append': 'false', 
                 'ConfirmOverwrite': 'false',
                 'OutputML':default_outputML,
                 'Separator':'\t',
                 #
                 'Save':'overwrite',
                 'UpdateModel':'false',
                 'ReportType':'parameter_estimation',
                 'Variable':self.GMQ.get_metabolites().keys()[0], #only for profile_likelihood
        
                 }
                     
        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for Reports'.format(i)
        options.update( kwargs) 
        self.kwargs=options
        
        if isinstance(self.kwargs.get('Metabolites'),str):
            self.kwargs['Metabolites']=[self.kwargs.get('Metabolites')]

        if isinstance(self.kwargs.get('GlobalQuantities'),str):
            self.kwargs['GlobalQuantities']=[self.kwargs.get('GlobalQuantities')]

        if isinstance(self.kwargs.get('LocalParameters'),str):
            self.kwargs['LocalParameters']=[self.kwargs.get('LocalParameters')]


        if self.kwargs['Append']=='true':
            self.kwargs['Append']=str(1)
        else:
            self.kwargs['Append']=str(0)
            
        if self.kwargs['ConfirmOverwrite']=='true':
            self.kwargs['ConfirmOverwrite']=str(1)
        else:
            self.kwargs['ConfirmOverwrite']=str(0)
                 
                 
        self.report_types=['none','profilelikelihood','time_course','parameter_estimation']
        assert self.kwargs.get('ReportType') in self.report_types,'valid report types include {}'.format(self.report_types)
        
        write_to_file_list=['duplicate','overwrite','false']
        assert self.kwargs.get('Save') in write_to_file_list     
        
        quantity_types=['particle_numbers','concentration']
        assert self.kwargs.get('QuantityType') in quantity_types
        
        if self.kwargs.get('Variable')!=None:
            assert self.kwargs.get('Variable') in self.GMQ.get_all_model_variables().keys(),'{} not in {}'.format(self.kwargs.get('Variable'),self.GMQ.get_all_model_variables().keys())
        
        if self.kwargs.get('ReportName')==None:
            if self.kwargs.get('ReportType')=='profilelikelihood':
                default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_profilelikelihood.txt'
            elif self.kwargs.get('ReportType')=='time_course':
                default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_time_course.txt'
            elif self.kwargs.get('ReportType')=='parameter_estimation':
                default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_parameter_estimation.txt'
            self.kwargs.update({'ReportName':default_report_name})

        self.copasiML=self.clear_all_reports()
        self.copasiML=self.run()
        

#        LOG.debug('setting up a report with the following settings:')
#        for i in self.kwargs:
#            LOG.debug('\t'+str([i, self.kwargs[i]]))
            
        self.copasiML=self.save()
        
        
        
    def save(self):
        if self.kwargs.get('Save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('Save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML
        
    def timecourse(self):
        '''
        creates a report to collect time course results. 
        
        By default all species and all global quantities are used with 
        Time on the left most column. This behavior can be overwritten by passing
        lists of metabolites to the Metabolites keyword or global quantities to the
        global quantities keyword
        '''
        #get existing report keys
        keys=[]
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])              
            if i.attrib['name']=='Time-Course':
                self.copasiML=self.remove_report('time_course')
        
        new_key='Report_30'
        while new_key  in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))
        report_attributes={'precision': '6', 
                           'separator': '\t',
                           'name': 'Time-Course',
                           'key':new_key, 
                           'taskType': 'Time-Course'}
        
        ListOfReports=self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)
        comment=etree.SubElement(report,'Comment') 
        comment=comment #get rid of annoying squiggly line above
        table=etree.SubElement(report,'Table')
        table.attrib['printTitle']=str(1)
        #Objects for the report to report
        time=etree.SubElement(table,'Object')
        #first element always time. 
        time.attrib['cn']='CN=Root,Model={},Reference=Time'.format(self.GMQ.get_model_name_cn())

        '''
        generate more SubElements dynamically
        '''
        #for metabolites
        if self.kwargs.get('Metabolites')!=None:
            for i in self.kwargs.get('Metabolites'):
                if self.kwargs.get('QuantityType')=='concentration':
                    cn= self.GMQ.get_IC_cns()[i]['cn']+',Reference=Concentration'
                elif self.kwargs.get('QuantityType')=='particle_numbers':
                    cn= self.GMQ.get_IC_cns()[i]['cn']+',Reference=ParticleNumber'
            #add to xml
                Object=etree.SubElement(table,'Object')
                Object.attrib['cn']=cn

        #for global quantities 
        if self.kwargs.get('GlobalQuantities')!=None:
            for i in self.kwargs.get('GlobalQuantities'):
                cn= self.GMQ.get_global_quantities_cns()[i]['cn']+',Reference=InitialValue'
                Object=etree.SubElement(table,'Object')
                Object.attrib['cn']=cn
        return self.copasiML
        
    def profile_likelihood(self):
        '''
        Create report of a parameter and best value for a parameter estimation 
        for profile likelihoods
        '''
        #get existing report keys
        keys=[]
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name']=='profilelikelihood':
                self.remove_report('profilelikelihood')
        
        new_key='Report_31'
        while new_key in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))
        report_attributes={'precision': '6', 
                           'separator': '\t',
                           'name': 'profilelikelihood',
                           'key':new_key, 
                           'taskType': 'Scan'}
        
        ListOfReports=self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)
        
        comment=etree.SubElement(report,'Comment') 
        table=etree.SubElement(report,'Table')
        table.attrib['printTitle']=str(1)
        if self.kwargs.get('Variable') in self.kwargs.get('Metabolites'):
            cn= self.GMQ.get_IC_cns()[self.kwargs.get('Variable')]['cn']+',Reference=InitialConcentration'#{}'.format(self.kwargs.get('QuantityType'))
        if self.kwargs.get('Variable') in self.kwargs.get('GlobalQuantities'):
            cn= self.GMQ.get_global_quantities_cns()[self.kwargs.get('Variable')]['cn']+',Reference=InitialValue'#{}'.format(self.kwargs.get('QuantityType'))
        if self.kwargs.get('Variable') in self.GMQ.get_local_kinetic_parameters_cns().keys():
            cn= self.GMQ.get_local_kinetic_parameters_cns()[self.kwargs.get('Variable')]['cn']+',Reference=Value'#{}'.format(self.kwargs.get('QuantityType'))
        etree.SubElement(table,'Object',attrib={'cn':cn})
        etree.SubElement(table,'Object',attrib={'cn':"CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"})
        return self.copasiML        

    def parameter_estimation_with_function_evaluations(self):
        '''
        Define a parameter estimation report and include the progression 
        of the parameter estimation (function evaluations).
        Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the GlobalQuantities, LocalParameters and Metabolites
        keywords. 
        '''
        #get existing report keys
        keys=[]
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])            
            if i.attrib['name']=='parameter_estimation':
                self.copasiML=self.remove_report('parameter_estimation')
        
        new_key='Report_32'
        while new_key  in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))
        report_attributes={'precision': '6', 
                           'separator': '\t',
                           'name': 'parameter_estimation',
                           'key':new_key, 
                           'taskType': 'parameterFitting'}
        
        ListOfReports=self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)
        comment=etree.SubElement(report,'Comment') 
        comment=comment #get rid of annoying squiggly line above
        table=etree.SubElement(report,'Table')
        table.attrib['printTitle']=str(1)
        #Objects for the report to report
#        time=etree.SubElement(table,'Object')

        '''
        generate more SubElements dynamically
        '''
        #for metabolites
        if self.kwargs.get('Metabolites')!=None:
            for i in self.kwargs.get('Metabolites'):
                assert i in self.GMQ.get_IC_cns().keys()
                if self.kwargs.get('QuantityType')=='concentration':
                    cn= self.GMQ.get_IC_cns()[i]['cn']+',Reference=InitialConcentration'
                elif self.kwargs.get('QuantityType')=='particle_numbers':
                    cn= self.GMQ.get_IC_cns()[i]['cn']+',Reference=InitialParticleNumber'
            #add to xml
                Object=etree.SubElement(table,'Object')
                Object.attrib['cn']=cn

        #for global quantities 
        if self.kwargs.get('GlobalQuantities')!=None:
            for i in self.kwargs.get('GlobalQuantities'):
                cn= self.GMQ.get_global_quantities_cns()[i]['cn']+',Reference=InitialValue'
                #add to xml
                Object=etree.SubElement(table,'Object')
                Object.attrib['cn']=cn
                
        #for global quantities 
        if self.kwargs.get('LocalParameters')!=None:
            for i in self.kwargs.get('LocalParameters'):
                cn= self.GMQ.get_local_kinetic_parameters_cns()[i]['cn']+',Reference=Value'
                #add to xml
                Object=etree.SubElement(table,'Object')
                Object.attrib['cn']=cn
                
                
        Object=etree.SubElement(table,'Object')
        Object.attrib['cn']="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"
        return self.copasiML     


    def parameter_estimation_broken(self):
        '''
        IMPORTANT
        THIS FUNCTION GIVES THE ORIGINAL PARAMETER VALUES
        NOT THE RESULTS OF THE PARAMTEER ESTIMATION
        
        Define a parameter estimation report. Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the GlobalQuantities, LocalParameters and Metabolites
        keywords
        '''
        #get existing report keys
        keys=[]
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])            
            if i.attrib['name']=='parameter_estimation':
                self.copasiML=self.remove_report('parameter_estimation')
        
        new_key='Report_33'
        while new_key  in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))
        report_attributes={'precision': '6', 
                           'separator': self.kwargs.get('Separator'),
                           'name': 'parameter_estimation',
                           'key':new_key, 
                           'taskType': 'parameterFitting'}
#        
        ListOfReports=self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)
        comment=etree.SubElement(report,'Comment') 
        comment=comment #get rid of annoying squiggly line above
        header=etree.SubElement(report,'Header')
        body=etree.SubElement(report,'Body')
        footer=etree.SubElement(report,'Footer')

        def add_sep(parent):
            assert isinstance(header,etree._Element),'parent element needs to be an etree element'
            sep=etree.SubElement(parent,'Object')#,attrib={'cn':'Separator={}'.format()})   
            sep.attrib['cn']='Separator={}'.format(self.kwargs.get('Separator'))
            return sep
        
        #for metabolites
        if self.kwargs.get('Metabolites')!=None:
            for i in self.kwargs.get('Metabolites'):
                assert i in self.GMQ.get_IC_cns().keys()
                if self.kwargs.get('QuantityType')=='concentration':
                    head_cn= self.GMQ.get_IC_cns()[i]['cn']+',Reference=InitialConcentration,Property=DisplayName'
                    foot_cn= self.GMQ.get_IC_cns()[i]['cn']+',Reference=InitialConcentration'
                
                elif self.kwargs.get('QuantityType')=='particle_numbers':
                    head_cn= self.GMQ.get_IC_cns()[i]['cn']+',Reference=InitialParticleNumber,Property=DisplayName'
                    foot_cn=self.GMQ.get_IC_cns()[i]['cn']+',Reference=InitialParticleNumber'
                
                #add to xml
                #header
                Object_head=etree.SubElement(header,'Object')
                Object_head.attrib['cn']=head_cn
                add_sep(header)
                #footer    
                Object_foot=etree.SubElement(footer,'Object')
                Object_foot.attrib['cn']=foot_cn
                add_sep(footer)

        #for global quantities 
        if self.kwargs.get('GlobalQuantities')!=None:
            for i in self.kwargs.get('GlobalQuantities'):
                cn_head= self.GMQ.get_global_quantities_cns()[i]['cn']+',Reference=InitialValue,Property=DisplayName'
                cn_foot= self.GMQ.get_global_quantities_cns()[i]['cn']+',Reference=InitialValue'


                #add to xml
                Object_head=etree.SubElement(header,'Object')
                Object_head.attrib['cn']=cn_head
                add_sep(header)
                
                
                Object_foot=etree.SubElement(footer,'Object')
                Object_foot.attrib['cn']=cn_foot
                add_sep(footer)
                
                
        #for global quantities 
        if self.kwargs.get('LocalParameters')!=None:
            for i in self.kwargs.get('LocalParameters'):
                cn_head= self.GMQ.get_local_kinetic_parameters_cns()[i]['cn']+',Reference=Value,Property=DisplayName'
                cn_foot= self.GMQ.get_local_kinetic_parameters_cns()[i]['cn']+',Reference=Value'


                #add to xml
                Object_head=etree.SubElement(header,'Object')
                Object_head.attrib['cn']=cn_head
                add_sep(header)
                Object_foot=etree.SubElement(footer,'Object')
                Object_foot.attrib['cn']=cn_foot
                add_sep(footer)
#                
        best_value_header=etree.SubElement(header,'Object')
        best_value_header.attrib['cn']="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value,Property=DisplayName"
        best_value_foot=etree.SubElement(footer,'Object')
        best_value_foot.attrib['cn']="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"
        return self.copasiML     
        
        
    
    def run(self):
        '''
        Execute code that builds the report defined by the kwargs
        '''
        if self.kwargs.get('ReportType')=='parameter_estimation':
            LOG.debug('created a \'parameter_estimation\' report')
            self.copasiML=self.parameter_estimation_with_function_evaluations()
        elif self.kwargs.get('ReportType')=='profilelikelihood':
            self.copasiML=self.profile_likelihood()
            LOG.debug('created a \'profile_likelihod\' type report')
        elif self.kwargs.get('ReportType')=='time_course':
            self.copasiML=self.timecourse()
            LOG.debug('created a \'time_course\' type report')
        elif self.kwargs.get('ReportType')=='none':
            self.copasiML=self.copasiML
            LOG.debug('created a \'none\' type report')
        return self.copasiML
        
    def remove_report(self,report_name):
        '''
        remove report called report_name
        '''
        assert report_name in self.report_types,'{} not a valid report type. These are valid report types: {}'.format(report_name,self.report_types)
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if report_name=='time_course':
                report_name='time-course'
            if i.attrib['name'].lower()==report_name.lower():
                i.getparent().remove(i)
        return self.copasiML
        
        
    def clear_all_reports(self):
        '''
        Having multile reports defined at once can be really annoying
        and give you unexpected results. Use this function to remove all reports
        before defining a new one to ensure you only have one active report any once. 
        '''
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            for j in list(i):
                if 'target' in j.attrib.keys():
                    j.attrib['target']=''
        return self.copasiML
        

#==============================================================================
class ParsePEDataDeprecated():
    '''
    Deprecated on 28-01-2017. Keep until you know it 
    wont mess up the rest of your code. 
    
    
    parse parameter estimation data from file
    
    Positional args:
        results_path:
            Full path to a results file or folder of files containing 
            parameter estimation results
            
    NOTE: this class is functional but will be replaced by PEAnalysis.ParsePEData
    '''
    def __init__(self,results_path,**kwargs):
        self.results_path=results_path #either file or folder
        self.cwd=os.path.dirname(self.results_path)
        os.chdir(self.cwd)
        self.pickle_path=os.path.join(self.cwd,'PEData.pickle')
        self.pickle_path_log=os.path.join(self.cwd,'PEData_log.pickle')
        options={
                 'FromPickle':False,
                 'OverwritePickle':False}   
        options.update(kwargs)
        self.kwargs= options
        
        assert os.path.exists(self.results_path),'{} does not exist'.format(self.results_path)
        if os.path.isdir(self.results_path):
            self.mode='folder'
        elif os.path.isfile(self.results_path):
            self.mode='file'
            
        
        #main methods of class
        self.data=self.read_data()
        self.data= self.remove_copasi_headers()
        self.data=self.rename_RSS(self.data)
        self.data=self.sort_data(self.data)
        

      
    def remove_copasi_headers(self):
        '''
        Use the PruneCopasiHeaders class to truncate copasi style formatting 
        conventions        
        '''
        n=self.data.shape[1]-1 #We minus 1 to account for not counting the parameter estimation header 3 lines down
        l=[]
        for i in self.data:
            if i !='TaskList[Parameter Estimation].(Problem)Parameter Estimation.Best Value':
                match= re.findall('.*\[(.*)\].*',i)
                l.append(match)
        if n==len(l):
            data=PruneCopasiHeaders(self.data,replace='true').df
            return data
        else:
            return self.data
        
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
        assert ext in ['.txt','.xlsx','.xls','.csv'],'parameter file is not .txt, .xlsx, .xls, .csv'
        if ext=='.txt':
            return pandas.read_csv(self.results_path,sep='\t')
        elif ext=='xlsx' or 'xls':
            return pandas.read_excel(self.results_path)
        elif ext=='.csv':
            return pandas.read_csv(self.results_path)


    def write_pickle(self,data):
        assert isinstance(data,pandas.core.frame.DataFrame)
        if self.kwargs.get('FromPickle')==True:
            if self.kwargs.get('OverwritePickle') == True:     
                if os.path.isfile(self.pickle_path):
                    os.remove(self.pickle_path)
                data.to_pickle(self.pickle_path)
                return True
            elif self.kwargs.get('OverwritePickle')==False:
                return False
        elif self.kwargs.get('FromPickle')==False:
            return False
                
            
    def read_pickle(self):
        assert os.path.isfile(self.pickle_path),'pickle path does\'t exist'
        return pandas.read_pickle(self.pickle_path)
            
    
    def read_data(self):
        if self.kwargs.get('FromPickle')==False:
            if self.mode=='file':
                data=self.read_file()
            elif self.mode=='folder':
                data=self.read_folder()
            self.write_pickle(data)
            return data
        elif self.kwargs.get('FromPickle')==True:
            if os.path.isfile(self.pickle_path)==False:
                self.kwargs['FromPickle']=False
                data=self.read_data()
            else:
                data=self.read_pickle()
        return data
                        


#==============================================================================            
class ExperimentMapper():
    '''
    Class to map variables from a parameter estimation item template which 
    is written using the ParameterEstimation.Write_item_template method, to model 
    variables. Variable names must match exactly. You cannot have more than 
    1 species with the same name, regardless of compartment. Generally
    this class is used within the parameter estimation class so the user doesn't
    need to bother with it.      
    
    args:
        copasi_file: 
            Copasi file path 
        experiment_files:
            list of experiment file paths
            
    See documentation for ParameterEstimation for
    details on each keyword argument
    
    kwargs:
        RowOrientation
        
        ExperimentType
        
        FirstRow
        
        NormalizeWeightsPerExperiment
        
        RowContainingNames
        
        Separator
        
        WeightMethod
        
        Save
        
        OutputML        
             
                 
    '''

    def __init__(self,copasi_file,experiment_files,**kwargs):
        self.copasi_file=copasi_file
        self.experiment_files=experiment_files
        assert isinstance(self.experiment_files,list)
        for i in self.experiment_files:
            assert os.path.isfile(i),'{} is not a real file'.format(i)
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=GetModelQuantities(self.copasi_file)
        default_outputML=os.path.split(self.copasi_file)[1][:-4]+'_Duplicate.cps'

        options={    
                 'RowOrientation':['true']*len(self.experiment_files),
                 'ExperimentType':['timecourse']*len(self.experiment_files),
                 'FirstRow':[str(1)]*len(self.experiment_files),
                 'NormalizeWeightsPerExperiment':['true']*len(self.experiment_files),
                 'RowContainingNames':[str(1)]*len(self.experiment_files),
                 'Separator':['\t']*len(self.experiment_files),
                 'WeightMethod':['mean_squared']*len(self.experiment_files) ,
                 'Save':'overwrite',
                 'OutputML':default_outputML}
        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TimeCourse'.format(i)
        options.update( kwargs) 
        self.kwargs=options

        #assign numberic values to WeightMethod   
        for i in range(len(self.kwargs.get('WeightMethod'))):
            assert self.kwargs.get('WeightMethod')[i] in ['mean','mean_squared','stardard_deviation','value_scaling']
            if self.kwargs.get('WeightMethod')[i]=='mean':
                self.kwargs.get('WeightMethod')[int(i)]=str(1)
            if self.kwargs.get('WeightMethod')[i]=='mean_squared':
                self.kwargs.get('WeightMethod')[int(i)]=str(2)
            if self.kwargs.get('WeightMethod')[i]=='stardard_deviation':
                self.kwargs.get('WeightMethod')[int(i)]=str(3)
            if self.kwargs.get('WeightMethod')[i]=='value_scaling':
                self.kwargs.get('WeightMethod')[int(i)]=str(4) 
        
        l=[]
        assert isinstance(self.kwargs.get('RowOrientation'),list)
        for i in self.kwargs.get('RowOrientation'):
            assert i in ['true','false']
            if i=='true':
                l.append(str(1))
            else:
                l.append(str(0))
        self.kwargs['RowOrientation']=l

        assert isinstance(self.kwargs.get('ExperimentType'),list)
        for i in range(len(self.kwargs.get('ExperimentType'))):
            assert self.kwargs.get('ExperimentType')[i] in ['steadystate','timecourse']
            if self.kwargs.get('ExperimentType')[i]=='steadystate':
                self.kwargs.get('ExperimentType')[i]=str(0)
            else:
                self.kwargs.get('ExperimentType')[i]=str(1)

        assert isinstance(self.kwargs.get('FirstRow'),list)
        l=[]
        for i in self.kwargs.get('FirstRow'):
            assert i!=0 
            assert i!=str(0)
            l.append(str(i))
        self.kwargs['FirstRow']=l
        
        l=[]
        assert isinstance(self.kwargs.get('NormalizeWeightsPerExperiment'),list)
        for i in self.kwargs.get('NormalizeWeightsPerExperiment'):
            assert i in ['true','false'],'{} should be true or false'.format(i)
            if i=='true':
                l.append(str(1))
            else:
                l.append(str(0))
        self.kwargs['NormalizeWeightsPerExperiment']=l

                
        l=[]
        assert isinstance(self.kwargs.get('RowOrientation'),list)
        for i in self.kwargs['RowOrientation']:
            l.append(str(i))
        self.kwargs['RowOrientation']=l

        l=[]
        assert isinstance(self.kwargs.get('RowContainingNames'),list)
        for i in self.kwargs['RowContainingNames']:
            l.append(str(i))
        self.kwargs['RowContainingNames']=l        


        assert isinstance(self.kwargs.get('Separator'),list)
        for i in self.kwargs['Separator']:
            assert isinstance(i,str),'separator should be given asa python list'
        
        assert self.kwargs.get('Save') in ['false','duplicate','overwrite']
        
        #run the experiment mapper        
        self.map_experiments()
        
        #save the copasi file
        if self.kwargs.get('Save')!='false':
            self.save()
        
        
    def get_existing_experiments(self):
        existing_experiment_list=[]
        query='//*[@name="Experiment Set"]'
        for i in self.copasiML.xpath(query):
            for j in list(i):
                existing_experiment_list.append(j)
        return existing_experiment_list

    def remove_experiment(self,experiment_name):
        '''
        name attribute of experiment. usually Experiment_1 or something
        '''
        query='//*[@name="Experiment Set"]'
        for i in self.copasiML.xpath(query):
            for j in list(i):
                if j.attrib['name']==experiment_name:
                    j.getparent().remove(j)
        return self.copasiML
        
    def remove_all_experiments(self):
        for i in self.get_existing_experiments():
            experiment_name= i.attrib['name']
            self.remove_experiment(experiment_name)
        return self.copasiML
        
    
    def create_experiment(self,index):
        '''
        Adds a single experiment set to the parameter estimation task
        exp_file is an experiment filename with exactly matching headers (independent variablies need '_indep' appended to the end)
        since this method is intended to be used in a loop in another function to 
        deal with all experiment sets, the second argument 'i' is the index for the current experiment
        
        i is the exeriment_file index        
        '''
        assert isinstance(index,int)
        data=pandas.read_csv(self.experiment_files[index],sep=self.kwargs.get('Separator')[index])
        #get observables from data. Must be exact match        
        obs=list(data.columns)
        
        #prune any observables that are contained within square brackets (like the outout from copasu)
        for j in range(len(obs)):
            if re.findall('\[(.*)\]',obs[j])!=[]:
                obs[j]=re.findall('\[(.*)\]',obs[j])[0]
        num_rows= str(data.shape[0])
        num_columns=str(data.shape[1]) #plus 1 to account for 0 indexed
        
        
        #if exp_file is in the same directory as copasi_file only use relative path
        if os.path.dirname(self.copasi_file)==os.path.dirname(self.experiment_files[index]):
            exp= os.path.split(self.experiment_files[index])[1]
        else:
            exp=self.experiment_files[index]
                
#        key_value= len(self.get_existing_experiments())+1
        self.key='Experiment_{}'.format(index)
        
        #necessary XML attributes
        Exp=etree.Element('ParameterGroup',attrib={'name':self.key})
        
        RowOrientation={'type': 'bool', 'name': 'Data is Row Oriented', 'value': self.kwargs.get('RowOrientation')[index]}
        ExperimentType={'type': 'unsignedInteger', 'name': 'Experiment Type', 'value': self.kwargs.get('ExperimentType')[index]}
        ExpFile={'type': 'file', 'name': 'File Name', 'value': exp}
        FirstRow={'type': 'unsignedInteger', 'name': 'First Row', 'value': self.kwargs.get('FirstRow')[index]}
        Key={'type': 'key', 'name': 'Key', 'value': self.key}
        LastRow={'type': 'unsignedInteger', 'name': 'Last Row', 'value': str(int(num_rows)+1)} #add 1 to account for 0 indexed python 
        NormalizeWeightsPerExperiment={'type': 'bool', 'name': 'Normalize Weights per Experiment', 'value': self.kwargs.get('NormalizeWeightsPerExperiment')[index]}
        NumberOfColumns={'type': 'unsignedInteger', 'name': 'Number of Columns', 'value': num_columns}
        ObjectMap={'name': 'Object Map'}
        RowContainingNames={'type': 'unsignedInteger', 'name': 'Row containing Names', 'value': self.kwargs.get('RowContainingNames')[index]}
        Separator={'type': 'string', 'name': 'Separator', 'value': self.kwargs.get('Separator')[index]}
        WeightMethod={'type': 'unsignedInteger', 'name': 'Weight Method', 'value': self.kwargs.get('WeightMethod')[index]}

        etree.SubElement(Exp,'Parameter',attrib=RowOrientation)
        etree.SubElement(Exp,'Parameter',attrib=ExperimentType)
        etree.SubElement(Exp,'Parameter',attrib=ExpFile)
        etree.SubElement(Exp,'Parameter',attrib=FirstRow)
        etree.SubElement(Exp,'Parameter',attrib=Key)
        etree.SubElement(Exp,'Parameter',attrib=LastRow)
        etree.SubElement(Exp,'Parameter',attrib=NormalizeWeightsPerExperiment)
        etree.SubElement(Exp,'Parameter',attrib=NumberOfColumns)
        Map=etree.SubElement(Exp,'ParameterGroup',attrib=ObjectMap)
        etree.SubElement(Exp,'Parameter',attrib=RowContainingNames)
        etree.SubElement(Exp,'Parameter',attrib=Separator)
        etree.SubElement(Exp,'Parameter',attrib=WeightMethod)
        
        #get handle to the cn's
        ICs= self.GMQ.get_IC_cns()
        glob= self.GMQ.get_global_quantities_cns()
        loc=self.GMQ.get_local_kinetic_parameters_cns()
        
        #define object role attributes
        TimeRole={'type': 'unsignedInteger', 'name': 'Role', 'value': '3'}
        DepentantVariableRole={'type': 'unsignedInteger', 'name': 'Role', 'value': '2'}
        IndepentantVariableRole={'type': 'unsignedInteger', 'name': 'Role', 'value': '1'}
        
        for i in range(int(num_columns)):
            map_group=etree.SubElement(Map,'ParameterGroup',attrib={'name':(str(i))})
            if self.kwargs.get('ExperimentType')[index]==str(1): #when Experiment type is set to time course it should be 1
                if i==0:
                    etree.SubElement(map_group,'Parameter',attrib=TimeRole)
                else:
                    '''
                    Need to duplicate the below block for ease. Could be more sophisticated 
                    but this is less effort. 
                    '''
                    if obs[i][-6:]=='_indep':
                        if obs[i][:-6] in ICs.keys():
                            cn=ICs[obs[i][:-6]]['cn']+',Reference=InitialConcentration'
                            independent_ICs={'type': 'cn', 'name': 'Object CN', 'value':cn} 
                            etree.SubElement(map_group,'Parameter',attrib=independent_ICs)
                            
                        elif obs[i][:-6] in glob.keys():
                            cn=glob[obs[i][:-6]]['cn']+',Reference=InitialValue'
                            independent_globs={'type': 'cn', 'name': 'Object CN', 'value':cn} 
                            etree.SubElement(map_group,'Parameter',attrib=independent_globs)
    
                        elif obs[i][:-6] in loc.keys():
                            cn=loc[obs[i][:-6]]['cn']+',Reference=Value'
                            independent_locs={'type': 'cn', 'name': 'Object CN', 'value':cn}
                            etree.SubElement(map_group,'Parameter',attrib=independent_locs)
                        else:
                            raise Errors.ExperimentMappingError('{} not in ICs, global vars or local variables'.format(obs[i]))
                        etree.SubElement(map_group,'Parameter',attrib=IndepentantVariableRole)
                        
                    else:
                        if obs[i] in ICs.keys():
                            cn=ICs[obs[i]]['cn']+',Reference=Concentration'
                            dependent_ICs={'type': 'cn', 'name': 'Object CN', 'value':cn}
                            etree.SubElement(map_group,'Parameter',attrib=dependent_ICs)
                            
                        elif obs[i] in glob.keys():
                            cn=glob[obs[i]]['cn']+',Reference=Value'
                            dependent_globs={'type': 'cn', 'name': 'Object CN', 'value':cn} 
                            etree.SubElement(map_group,'Parameter',attrib=dependent_globs)
                            '''
                            Note that you don't ever map data to reaction parameters therefore the commented
                            out block below is not needed. Don't delete until you are sure of it though...
                            '''
                        elif obs[i] in loc.keys():
                            cn=loc[obs[i]['cn']]+',Reference=Value'
                            dependent_locs={'type': 'cn', 'name': 'Object CN', 'value':cn}
                            etree.SubElement(map_group,'Parameter',attrib=dependent_locs)
                            
                        elif obs[i] not in loc.keys() + glob.keys() + ICs.keys():
                            LOG.info('{}not in model and has not been mapped. Please check spelling and try again'.format(obs[i]))

                        else:
                            raise Errors.ExperimentMappingError('''\'{}\' mapping error. In the copasi GUI its possible to have same name for two species provided they are in different compartments. In this API, having non-unique species identifiers leads to errors in mapping experimental to model variables'''.format(obs[i]))
                        etree.SubElement(map_group,'Parameter',attrib=DepentantVariableRole)

            else:
                '''
                Region of duplicated code
                '''
                if obs[i][-6:]=='_indep':
                    if obs[i][:-6] in ICs.keys():
                        cn=ICs[obs[i][:-6]]['cn']+',Reference=InitialConcentration'
                        independent_ICs={'type': 'cn', 'name': 'Object CN', 'value':cn} 
                        etree.SubElement(map_group,'Parameter',attrib=independent_ICs)
                        
                    elif obs[i][:-6] in glob.keys():
                        cn=glob[obs[i][:-6]]['cn']+',Reference=InitialValue'
                        independent_globs={'type': 'cn', 'name': 'Object CN', 'value':cn} 
                        etree.SubElement(map_group,'Parameter',attrib=independent_globs)

                    elif obs[i][:-6] in loc.keys():
                        cn=loc[obs[i][:-6]]['cn']+',Reference=Value'
                        independent_locs={'type': 'cn', 'name': 'Object CN', 'value':cn}
                        etree.SubElement(map_group,'Parameter',attrib=independent_locs)
                    else:
                        raise Errors.ExperimentMappingError('{} not in ICs, global vars or local variables'.format(obs[i]))
                    etree.SubElement(map_group,'Parameter',attrib=IndepentantVariableRole)
                    
                else:
                    if obs[i] in ICs.keys():
                        cn=ICs[obs[i]]['cn']+',Reference=Concentration'
                        dependent_ICs={'type': 'cn', 'name': 'Object CN', 'value':cn}
                        etree.SubElement(map_group,'Parameter',attrib=dependent_ICs)
                        
                    elif obs[i] in glob.keys():
                        cn=glob[obs[i]]['cn']+',Reference=Value'
                        dependent_globs={'type': 'cn', 'name': 'Object CN', 'value':cn} 
                        etree.SubElement(map_group,'Parameter',attrib=dependent_globs)
                        '''
                        Note that you don't ever map data to reaction parameters therefore the commented
                        out block below is not needed. Don't delete until you are sure of it though...
                        '''
                    elif obs[i] in loc.keys():
                        cn=loc[obs[i]['cn']]+',Reference=Value'
                        dependent_locs={'type': 'cn', 'name': 'Object CN', 'value':cn}
                        etree.SubElement(map_group,'Parameter',attrib=dependent_locs)
                    else:
                        raise Errors.ExperimentMappingError('''\'{}\' mapping error. In the copasi GUI its possible to have same name for two species provided they are in different compartments. In this API, having non-unique species identifiers leads to errors in mapping experimental to model variables'''.format(obs[i]))
                    etree.SubElement(map_group,'Parameter',attrib=DepentantVariableRole)
            

        return Exp

    def add_experiment_set(self,experiment_element):
        query='//*[@name="Experiment Set"]'
        for j in self.copasiML.xpath(query):
            j.insert(0,experiment_element)
        return self.copasiML


    def save(self):
        if self.kwargs.get('Save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('Save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML
        
        
    def map_experiments(self):
        self.remove_all_experiments()
        LOG.debug('Removing all pre-existing experiments from copasi mapping interface')
        for i in range(len(self.experiment_files)):
            Experiment=self.create_experiment(i)
            LOG.debug('Mapping experiment {}'.format(self.experiment_files[i]))
            self.copasiML=self.add_experiment_set(Experiment)
            self.save()
        return self.copasiML
        


#==============================================================================
class TimeCourse(object):
    '''
    Run a time course using Copasi. Ensure, you specify the corrent amount
    of time you want simulating. Do this by ensuring that End=StepSize*Intervals.
    Set Plot='true' to automatically plot the results which can be found in a file
    in the same directory as your copasi file in a folder named after your ReportName
    kwarg
    
    NOTE: Space has been left for addition of code to interface with the other
    copasi solvers. Currently only deterministic is supported. 
    
    args:
        copasi_file - the copasi file you want to do a time course on 
        
        
    **kwargs:
        For arguments related to plotting, see the documentation for Plot
        
        Intervals:
            How many intervals between start and end. Default=100
        
        StepSize:
            How big each time increment is. Default='0.01',
        
        Start: 
            Starting point of stimulation. Default=0.0
        
        End: 
            The end point of the time course. Default=1.
        
        #integration options
        RelativeTolerance: 
            Default='1e-6',
        
        AbsoluteTolerance:
            Default='1e-12',
        
        MaxInternalSteps:
            Default='10000',
            
        UpdateModel:
            Not really needed in time course. Do not change. Default='false'

        Metabolites:
            A list of which metabolites to include in output. Default=all
        
        GlobalQuantities: 
            A list of global quantities to include in the output. Default is all global quantities

        QuantityType: 
            Either 'particle_numbers' or 'concentration',

        ReportName: 
            Name of the output report. Default is name of the copasi file with _TimeCourse appended'

        Append: 
            Append to the report, 'true' or 'false' , default='false'

        ConfirmOverwrite:
            Report confirm overwrite , 'true' or 'false' , default='false'

        SimulationType: 
            Either 'stochastic' or 'deterministic'. default='deterministic'. IMPORTANT: stochastic not yet implemented but there is room for it

        OutputEvent: 
            Output event or not, default ='false'

        Scheduled: 
            'true' or 'false'. Enables running the simulation by CopasiSE. Default='true',

        Save: 
            Save the copasi file with the changes. Either 'false','overwrite' or 'duplicate'
        
        PruneHeaders:
            Copasi automatically prints out copasi references to output files. Set
            this to 'true' to  prune the references off leaving just the variable name,
            'true' or 'false', default='true'
        
        #graph options
        Plot:
            Whether to plot the graphs or not
            
        SaveFig:
            Whether to save the figures to file or not
            
        ExtraTitle:
            If SaveFig='true',give the filename an extra identifier
            
        LineWidth:
            Passed to Matplotlib.pyplot.plot. Thickness of the line

        LineColor:
            Passed to Matplotlib.pyplot.plot. Color of the line

        MarkerColor:
            Passed to Matplotlib.pyplot.plot. color of the dots

        LineStyle:
            Passed to Matplotlib.pyplot.plot. Style of line

        MarkerStyle:
            Passed to Matplotlib.pyplot.plot. Style of marker

        DPI:
            Passed to Matplotlib.pyplot.plot. 
            
        XTickRotation:
            Passed to Matplotlib.pyplot.plot. Rotate x labels
            
        TitleWrapSize:
            Number of characters before word wrapping the title
            
    '''
    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=GetModelQuantities(self.copasi_file)
        default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_TimeCourse.txt'
        default_outputML=os.path.join(os.path.dirname(self.copasi_file),'_Duplicate.cps')

        options={'Intervals':'100',
                 'StepSize':'0.01',
                 'End':'1',
                 'RelativeTolerance':'1e-6',
                 'AbsoluteTolerance':'1e-12',
                 'MaxInternalSteps':'10000',
                 'Start':'0.0',
                 'UpdateModel':'false',
                 #report variables
                 'Metabolites':self.GMQ.get_metabolites().keys(),
                 'GlobalQuantities':self.GMQ.get_global_quantities().keys(),
                 'QuantityType':'concentration',
                 'ReportName':default_report_name,
                 'Append': 'false', 
#                 'target': 'cheese.txt', 
                 'ConfirmOverwrite': 'false',
                 'SimulationType':'deterministic',
                 'OutputEvent':'false',
                 'Scheduled':'true',
                 'Save':'overwrite',
                 'OutputML':default_outputML,
                 'PruneHeaders':'true',
                 
                 #graph options
                 'Plot':'false'      ,              
                 'LineWidth':2,
                 'LineColor':'k',
                 'MarkerColor':'r',
                 'LineStyle':'-',
                 'MarkerStyle':'o',
                 'AxisSize':15,
                 'FontSize':22,
                 'XTickRotation':0,
                 'TitleWrapSize':35,
                 'SaveFig':'false',
                 'ExtraTitle':None,
                 'DPI':125,
                 'MarkerSize':5,
                 'GraphDirectory':None,
                 

                     }
        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TimeCourse'.format(i)
#            kwargs[i]=str(kwargs[i]).lower()
#            assert isinstance(kwargs[i],str),'all optional arguments passed shold be lower case strings'
        options.update( kwargs) 
        self.kwargs=options

        '''
        if the below three kwargs are a single entry they can be a string. 
        In this case, put them back into a list to ensure a smooth ride
        '''
        if isinstance(self.kwargs.get('Metabolites'),str):
            self.kwargs['Metabolites']=[self.kwargs.get('Metabolites')]

        if isinstance(self.kwargs.get('GlobalQuantities'),str):
            self.kwargs['GlobalQuantities']=[self.kwargs.get('GlobalQuantities')]

        if isinstance(self.kwargs.get('LocalParameters'),str):
            self.kwargs['LocalParameters']=[self.kwargs.get('LocalParameters')]


        
        #Ensure consistecny for time variables
        assert float(self.kwargs.get('End'))==float(self.kwargs.get('StepSize'))*float(self.kwargs.get('Intervals')),'End should equal Interval Size times Number of Intervals but {}!={}*{}'.format(self.kwargs.get('End'),self.kwargs.get('StepSize'),self.kwargs.get('Intervals'))        

        #make sure Metabolites and ModelValues are lists
        if self.kwargs.get('Metabolites')!=None:
            assert isinstance(self.kwargs.get('Metabolites'),list),'Keyword argument Metabolites should be a Python list'
            for i in self.kwargs.get('Metabolites'):
                assert i in self.GMQ.get_metabolites().keys(),'{} is not a Metabolite in this model. These are Metabolites in this model: {}'.format(i,self.GMQ.get_IC_cns().keys())


        if self.kwargs.get('GlobalQuantities')!=None:
            assert isinstance(self.kwargs.get('GlobalQuantities'),list),'Keyword argument GlobalQuantities should be a Python list'
            for i in self.kwargs.get('GlobalQuantities'):
                assert i in self.GMQ.get_global_quantities().keys(),'{} is not a global variable in this model. These are global variables in this model: {}'.format(i,self.GMQ.get_global_quantities())
            
        #only accept deterministic or stochastic
        assert self.kwargs.get('SimulationType') in ['deterministic','stochastic']

#
        
        #this bit of code helps keep the keyword arguments consistant
        assert self.kwargs.get('QuantityType').lower() in ['concentration','particle_number']
            
        #report arguments
        
        if self.kwargs.get('PruneHeaders') not in ['true','false']:
            raise Errors.InputError('PruneHeaders kwarg must be either \'true\' or \'false\'')


        if self.kwargs.get('Append') not in ['true','false']:
            raise Errors.InputError('Append kwarg must be either \'true\' or \'false\'')

        if self.kwargs.get('ConfirmOverwrite') not in ['true','false']:
            raise Errors.InputError('ConfirmOverwrite kwarg must be either \'true\' or \'false\'')

        if self.kwargs.get('OutputEvent') not in ['true','false']:
            raise Errors.InputError('OutputEvent kwarg must be either \'true\' or \'false\'')

        if self.kwargs.get('Scheduled') not in ['true','false']:
            raise Errors.InputError('Scheduled kwarg must be either \'true\' or \'false\'')

        if self.kwargs.get('Plot') not in ['true','false']:
            raise Errors.InputError('Plot kwarg must be either \'true\' or \'false\'')

        
        self.kwargs['LineWidth']=int(self.kwargs.get('LineWidth'))
        self.kwargs['AxisSize']=int(self.kwargs.get('AxisSize'))
        self.kwargs['AxisSize']=int(self.kwargs.get('AxisSize'))
        self.kwargs['XTickRotation']=int(self.kwargs.get('XTickRotation'))
        self.kwargs['TitleWrapSize']=int(self.kwargs.get('TitleWrapSize'))
        self.kwargs['DPI']=int(self.kwargs.get('DPI'))

        
        if self.kwargs.get('Append')=='true':
            self.kwargs['Append']==str(1)
        else:
            self.kwargs['Append']==str(0)

        if self.kwargs.get('ConfirmOverwrite')=='true':
            self.kwargs['ConfirmOverwrite']==str(1)
        else:
            self.kwargs['ConfirmOverwrite']==str(0)

        if self.kwargs.get('OutputEvent')=='true':
            self.kwargs['OutputEvent']==str(1)
        else:
            self.kwargs['OutputEvent']==str(0)

        if self.kwargs.get('Scheduled')=='true':
            self.kwargs['Scheduled']==str(1)
        else:
            self.kwargs['Scheduled']==str(0)
            
        assert self.kwargs.get('SaveFig') in ['false','true']
        
        #convert some numeric kwargs to str
        
        self.kwargs['Intervals']=str(self.kwargs.get('Intervals'))
        self.kwargs['StepSize']=str(self.kwargs.get('StepSize'))
        self.kwargs['End']=str(self.kwargs.get('End'))
        self.kwargs['RelativeTolerance']=str(self.kwargs.get('RelativeTolerance'))
        self.kwargs['AbsoluteTolerance']=str(self.kwargs.get('AbsoluteTolerance'))
        self.kwargs['MaxInternalSteps']=str(self.kwargs.get('MaxInternalSteps'))
        self.kwargs['Start']=str(self.kwargs.get('Start'))
        
        if isinstance(self.kwargs.get('MarkerSize'),int):
            self.kwargs['MarkerSize']=float(self.kwargs.get('MarkerSize'))
            
        assert isinstance(self.kwargs.get('MarkerSize'),float)
                 
                 
        assert self.kwargs.get('LineStyle') in   ['-' , '--' , '-.' , ':' , 'None' , ' ' , '']
        assert isinstance(self.kwargs.get('LineWidth'),int),'{} is not int'.format(type(self.kwargs.get('LineWidth')))
        
        assert self.kwargs.get('MarkerStyle') in ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd']

        color_dct={'b': 'blue',
                   'g': 'green',
                   'r': 'red',
                   'c': 'cyan',
                   'm': 'magenta',
                   'y': 'yellow',
                   'k': 'black',
                   'w': 'white'}
        assert self.kwargs.get('LineColor') in color_dct.keys()+color_dct.values()
        assert self.kwargs.get('MarkerColor') in color_dct.keys()+color_dct.values()
                 
                 
        self.report_options={}#report variables
        self.report_options['Metabolites']=self.kwargs.get('Metabolites')
        self.report_options['GlobalQuantities']=self.kwargs.get('GlobalQuantities')
        self.report_options['QuantityType']=self.kwargs.get('QuantityType')
        self.report_options['ReportName']=self.kwargs.get('ReportName')
        self.report_options['Append']=self.kwargs.get('Append')
        self.report_options['ConfirmOverwrite']=self.kwargs.get('ConfirmOverwrite')
        self.report_options['OutputML']=self.kwargs.get('OutputML')
        self.report_options['Save']=self.kwargs.get('Save')
        self.report_options['UpdateModel']=self.kwargs.get('UpdateModel')
        self.report_options['ReportType']='time_course'#self.kwargs.get('ReportType')
        
        #other keywords that are non optional for time course
        self.kwargs['ReportType']='time_course'
        matplotlib.rcParams.update({'font.size':self.kwargs.get('AxisSize')})
        '''
        All methods required for time course are 
        called with run
        '''
        self.run()
        self.data=self.read_sim_data()
        if self.kwargs.get('Plot')=='true':
            self.plot()
        


    def save(self):
        if self.kwargs.get('Save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('Save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML        
        
    def set_deterministic(self):
        '''
        set parameters for deterministic timecourse
        '''
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        method_params={'type': 'Deterministic(LSODA)', 'name': 'Deterministic (LSODA)'}
        for i in self.copasiML.xpath(query):
            #make available to coapsiSE
            i.attrib['scheduled']=self.kwargs.get('Scheduled')
            for j in list(i):
                j.attrib['type']=method_params['type']
                j.attrib['name']=method_params['name']
                for k in list(j):
                    if  k.attrib['name']=='Duration':
                        k.attrib['value']=self.kwargs.get('End')
                        
                    if  k.attrib['name']=='StepNumber':
                        k.attrib['value']=self.kwargs.get('Intervals')
                        
                    elif  k.attrib['name']=='StepSize':
                        k.attrib['value']=self.kwargs.get('StepSize')

                    elif  k.attrib['name']=='TimeSeriesRequested':
                        k.attrib['value']='1'                        

                    elif  k.attrib['name']=='OutputStartTime':
                        k.attrib['value']=self.kwargs.get('Start')

                    elif  k.attrib['name']=='Output Event':
                        k.attrib['value']=self.kwargs.get('OutputEvent')

                    elif  k.attrib['name']=='Continue on Simultaneous Events':
                        k.attrib['value']='0'

                    elif  k.attrib['name']=='Integrate Reduced Model':
                        k.attrib['value']='0'

                    elif  k.attrib['name']=='Relative Tolerance':
                        k.attrib['value']=self.kwargs.get('RelativeTolerance')

                    elif  k.attrib['name']=='Absolute Tolerance':
                        k.attrib['value']=self.kwargs.get('AbsoluteTolerance')

                    elif  k.attrib['name']=='MaxInternalSteps':
                        k.attrib['value']=self.kwargs.get('MaxInternalSteps')
        return self.copasiML


    def report_definition(self):
        self.copasiML=Reports(self.copasi_file,**self.report_options).copasiML 
        return self.copasiML
        
    def get_report_key(self):
        '''
        cros reference the timecourse task with the newly created
        time course reort to get the key
        '''
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name']=='Time-Course':
                key=i.attrib['key']
        assert key!=None,'have you ran the report_definition method?'
        return key
                
    def set_report(self):
        '''
        Use the report defined in self.create_report to tell copasi 
        were to put the results
        '''
        self.copasiML=self.report_definition()
        key=self.get_report_key()
        
        arg_dct={'append': self.kwargs.get('Append'), 
                 'target':self.kwargs.get('ReportName'),
                 'reference': key, 
                 'confirmOverwrite': self.kwargs.get('ConfirmOverwrite')}
        query="//*[@name='Time-Course']" and "//*[@type='timeCourse']"
        present=False
#        query='//Report'
        for i in self.copasiML.xpath(query):
            for j in list(i):
                if 'append' and 'target' in j.attrib.keys():
                    present=True
                    j.attrib.update(arg_dct)
            if present==False:
                report=etree.Element('Report',attrib=arg_dct)
                i.insert(0,report)
#        self.save()
        return self.copasiML

    def run(self):
        '''
        Run a time course. Use keyword argument:
            SimulationType='deterministic' #default
            SumulationType='stochastic' #still to be written
        '''
        if self.kwargs.get('SimulationType')=='deterministic':
            self.copasiML=self.report_definition()
            self.copasiML=self.set_report()
            self.copasiML=self.set_deterministic()
            LOG.debug('setting up deterministic time course')
        elif self.kwargs.get('SimulationType')=='stochastic':
            return 'There is space in this class to write code to run a stochastic simulation but it is not yet written'
        #save to duplicate copasi file
        self.save()
        if self.kwargs.get('Save')=='overwrite':
            args=['CopasiSE',self.copasi_file]
        elif self.kwargs.get('Save')=='duplicate':
            args=['CopasiSE',self.kwargs.get('OutputML')]
            
        R=Run(self.copasi_file,Task='time_course')
        LOG.debug('Time course ran')
        return R

        
    def read_sim_data(self):
        data_output=os.path.join(os.path.dirname(self.copasi_file), self.kwargs['ReportName'])
        #trim copasi style headers
        LOG.debug('Reading timecourse')
        if self.kwargs.get('PruneHeaders')=='true':
            LOG.debug('pruning headers of copasi files of COPASI references')    
            PruneCopasiHeaders(data_output,replace='true')
        return pandas.read_csv(data_output,sep='\t') 
        
    def plot(self):
        '''
        
        '''
        LOG.debug('plotting time course')
        ## Create directory for graphs
        if self.kwargs['GraphDirectory']==None:
            dire=os.path.join(os.path.dirname(self.copasi_file),'TimeCourseGraphs')
            if os.path.isdir(dire)!=True:
                os.mkdir(dire)
            os.chdir(dire)
            
        for i in self.data:
            if i.lower()!='time':
                plt.figure()
                ax = plt.subplot(111)
                plt.plot(self.data['Time'],self.data[i],
                         linewidth=self.kwargs.get('LineWidth'),color=self.kwargs.get('LineColor'),
                         linestyle=self.kwargs.get('LineStyle'),marker='o',markerfacecolor=self.kwargs.get('MarkerColor'),markersize=self.kwargs.get('MarkerSize'))
#                plt.plot(self.data['Time'],self.data[i],color=self.kwargs.get('MarkerColor'),marker=self.kwargs.get('MarkerStyle'))

                
                #plot labels
                plt.title('\n'.join(wrap('Time-Course for {}'.format(i),self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))
                if self.kwargs.get('QuantityType')=='concentration':
                    try:
                        plt.ylabel('Concentration ({})'.format(self.GMQ.get_quantity_units().encode('ascii')),fontsize=self.kwargs.get('FontSize'))
                    except UnicodeEncodeError:
                        plt.ylabel('Concentration (micromol)',fontsize=self.kwargs.get('FontSize'))
                if self.kwargs.get('QuantityType')=='particle_number':
                    plt.ylabel('Particle Numbers',fontsize=self.kwargs.get('FontSize'))
                        
                plt.xlabel('Time ({})'.format(self.GMQ.get_time_unit()),fontsize=self.kwargs.get('FontSize'))         
                    
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
                    def replace_non_ascii(st):
                        for j in st:
                            if j  not in string.ascii_letters+string.digits+'_-[]':
                                st=re.sub('\{}'.format(j),'__',st) 
                        return st
                        
                    filename={}
                    name=replace_non_ascii(i)
                    filename[i]=os.path.join(dire,name+'.png')

                    if self.kwargs.get('ExtraTitle') !=None:
                        plt.savefig(name+'_'+self.kwargs.get('ExtraTitle')+'.png',bbox_inches='tight',format='png',dpi=self.kwargs.get('DPI'))
                    else:
                        plt.savefig(filename[i],format='png',bbox_inches='tight',dpi=self.kwargs.get('DPI'))     
                    return filename
        
                if self.kwargs.get('Show')=='true':
                    plt.show()
                    
                #save figure options
                if self.kwargs.get('SaveFig')=='true':
                    os.chdir(os.path.dirname(self.copasi_file))
                    save_plot()
                    
class PhaseSpace(TimeCourse):
    '''
    Inherits from TimeCourse
    
    Use TimeCourse to get data and replot all n choose 2 combinations
    of phase space plot
    '''
    def __init__(self,copasi_file,**kwargs):
        super(PhaseSpace,self).__init__(copasi_file,**kwargs)
        LOG.debug('Plotting all combinations of phase space plot')
        self.new_options={'Plot':'false'}
        self.kwargs.update(self.new_options)
        self.species_data=self.isolate_species()
        self.combinations=self.get_combinations()
        
        if self.kwargs.get('SaveFig')=='true':
            self.phase_dir=self.make_phase_dir()
            os.chdir(self.phase_dir)
        
        self.plot_all_phase()
        
        os.chdir(os.path.dirname(self.copasi_file))
        
            
    def isolate_species(self):
        '''
        Isolate the species from the time course data 
        '''
        metabs= self.GMQ.get_metabolites().keys()
        for i in metabs:
            if i not in self.data.keys():
                raise Errors.IncompatibleStringError(' {} is an incompatible string that is not supported by PyCoTools. Please modify the string and rerun')
        return self.data[metabs]
        
    def get_combinations(self):
        return list(itertools.combinations(self.species_data.keys(),2))
        
    def make_phase_dir(self):
        dire=os.path.join(os.path.dirname(self.copasi_file),'PhasePlots')
        if os.path.isdir(dire)==False:
            os.mkdir(dire)
        return dire
        
        
    def plot1phase(self,x,y):
        if x  not in self.species_data.keys():
            raise Errors.InputError('{} is not in your model species: {}'.format(x,self.species_data.keys()))
            
        if y  not in self.species_data.keys():
            raise Errors.InputError('{} is not in your model species: {}'.format(y,self.species_data.keys()))
               
        x_data=self.species_data[x]
        y_data=self.species_data[y]
        plt.figure()
        ax = plt.subplot(111)
        plt.plot(x_data,y_data,linewidth=self.kwargs.get('LineWidth'),
                    color=self.kwargs.get('LineColor'),
                    linestyle=self.kwargs.get('LineStyle'),
                    marker='o',markerfacecolor=self.kwargs.get('MarkerColor'),
                    markersize=self.kwargs.get('MarkerSize'))
                    
        plt.title('\n'.join(wrap('{} Vs {} Phase Plot'.format(x,y),self.kwargs.get('TitleWrapSize'))),fontsize=self.kwargs.get('FontSize'))
        try:
            plt.ylabel(y+'({})'.format(self.GMQ.get_quantity_units().encode('ascii')),fontsize=self.kwargs.get('FontSize'))
            plt.xlabel(x+'({})'.format(self.GMQ.get_quantity_units().encode('ascii')),fontsize=self.kwargs.get('FontSize'))         
        except UnicodeEncodeError:
            plt.ylabel(y+'({})'.format('micromol'),fontsize=self.kwargs.get('FontSize'))
            plt.xlabel(x+'({})'.format('micromol'),fontsize=self.kwargs.get('FontSize'))         
            
            
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
        if self.kwargs.get('Show')=='true':
            plt.show()
            
        def replace_non_ascii(st):
            for j in st:
                if j  not in string.ascii_letters+string.digits+'_-[]':
                    st=re.sub('\{}'.format(j),'__',st) 
            return st    
            
        y_new=replace_non_ascii(y)
        x_new=replace_non_ascii(x)
        name='{}_Vs_{}_PhasePlot'.format(x_new,y_new)
        
        if self.kwargs.get('SaveFig')=='true':
            if self.kwargs.get('ExtraTitle') !=None:
                plt.savefig(name+'_'+self.kwargs.get('ExtraTitle')+'.png',bbox_inches='tight',format='png',dpi=self.kwargs.get('DPI'))
            else:
                plt.savefig(name+'_'+'.png',format='png',bbox_inches='tight',dpi=self.kwargs.get('DPI'))     
    def plot_all_phase(self):
        for i in self.combinations:
            self.plot1phase(i[0],i[1])
#                                
            
            
#==============================================================================
class ParameterEstimation():
    '''
    Set up and run a parameter estimation in copasi. Since each parameter estimation
    problem is different, this process cannot be done in a single line of code. 
    Instead the user should initialize an instance of the ParameterEstimation 
    class with all the relevant keyword arguments. Subsequently use the 
    write_item_template() method and modify the resulting xlsx in your copasi file
    directory. Save the file then close and run the set_up() method to define your
    optimization problem. When Run is set to 'true', the parameter estimation will
    automatically run in CopasiSE. If Plot is also set to 'true', a plot comparing 
    experimental and simulated profiles are produced. Profiles are saved
    to file with SaveFig='true'
    
    args:
        
        copasi_file: 
            The file path for the copasi file you want to perform parameter estimation on
            
        experiment_files:
            Either a single experiment file path or a list of experiment file paths 
            
    **Kwargs:
        
        Metabolites:
            Which metabolites (ICs) to include in parameter esitmation. Default = all of them. 
            
        GlobalQuantities:
            Which global values to include in the parameter estimation. Default= all
        
        QuantityType:
            either 'concentration' or particle numbers

        ReportName:
            name of the output report
            
        Append:
            Append to report or not,'true' or 'false'

        ConfirmOverwrite:
            'true' or 'false', overwrite report or not
            
        ConfigFilename:
            Filename for the parameter estimation config file
            
        OverwriteConfigFile:,
            'true' or 'false', overwrite the config file each time program is run
            
        UpdateModel:
            Update model parameters after parameter estimation

        RandomizeStartValues:
            'true' or 'false'. Check the randomize start values box or not. Default 'true'

        CreateParameterSets:
            'true' or 'false'. Check the create parameter sets box or not. Default 'false'
        
        CalculateStatistics':str(1),
            'true' or 'false'. Check the calcualte statistics box or not. Default 'false'

        Method:
            Name of one of the copasi parameter estimation algorithms. Valid arguments: 
            ['CurrentSolutionStatistics','DifferentialEvolution','EvolutionaryStrategySR','EvolutionaryProgram',
             'HookeJeeves','LevenbergMarquardt','NelderMead','ParticleSwarm','Praxis',
             'RandomSearch','ScatterSearch','SimulatedAnnealing','SteepestDescent',
             'TruncatedNewton','GeneticAlgorithm','GeneticAlgorithmSR'],
             Default=GeneticAlgorithm

        NumberOfGenerations:
            A parameter for parameter estimation algorithms. Default=200

        PopulationSize:
            A parameter for parameter estimation algorithms. Default=50

        RandomNumberGenerator:
            A parameter for parameter estimation algorithms. Default=1

        Seed:
            A parameter for parameter estimation algorithms. Default=0

        Pf:
            A parameter for parameter estimation algorithms. Default=0.475

        IterationLimit:
            A parameter for parameter estimation algorithms. Default=50

        Tolerance:
            A parameter for parameter estimation algorithms. Default=0.00001

        Rho;
            A parameter for parameter estimation algorithms. Default=0.2

        Scale:
            A parameter for parameter estimation algorithms. Default=10

        SwarmSize:
            A parameter for parameter estimation algorithms. Default=50

        StdDeviation:
            A parameter for parameter estimation algorithms. Default=0.000001

        NumberOfIterations:
            A parameter for parameter estimation algorithms. Default=100000

        StartTemperature:
            A parameter for parameter estimation algorithms. Default=1

        CoolingFactor:
            A parameter for parameter estimation algorithms. Default=0.85

        RowOrientation:
            1 means data is row oriented, 0 means its column oriented
                         
        ExperimentType:
            List with the same number elements as you have experiment files. Each element
            is either 'timecourse' or 'steady_state' and describes the type of 
            data at that element in the experiment_files argument 

        FirstRow:
            List with the same number elements as you have experiment files. Each element
            is the starting line for data as an integer. Default is a list of 1's and this
            rarely needs to be changed.
            
        NormalizeWeightsPerExperiment':['true']*len(self.experiment_files),
            List with the same number elements as you have experiment files. Each element
            is 'true' or 'false' and correlates to ticking the
            normalize wieghts per experiment box in the copasi gui. Default [true]*len(experiments)
            
        RowContainingNames:
            List with the same number elements as you have experiment files. Each element
            is an integer value corresponding to the row in the data containing names. The default
            is 1 for all experiment files [1]*len(experiment_files)
                        

        Separator':['\t']*len(self.experiment_files),
            List with the same number elements as you have experiment files. Each element
            is the separator used in the data files. Defaults to a tab (\\t) for all files 
            though commas are also common
            
        WeightMethod':['mean_squared']*len(self.experiment_files),
            List with the same number elements as you have experiment files. Each element
            is a list of the name of the normalization algorithm to use for that data set. 
            This should probably be the same for each experiment file and defaults to mean_squared. 
            Options are: ['mean','mean_squared','stardard_deviation','value_scaling']
            
        Save: 
            One of 'false','duplicate' or 'overwrite'. If duplicate, use the name in 
            the keyword argument OutputML to save the file.

        OutputML:
            When Save is set to 'duplicate', this is the new name of the cps file
        
        PruneHeaders:
            Copasi uses references to distinguish between variable types. The report
            output usually contains these references in variable names. 'true' removes 
            the references while 'false' leaves them in. 
        Scheduled':'false'
            'true' or 'false'. Check the box called 'executable' in the top right hand
            corner of the Copasi GUI. This tells Copasi to shedule a parameter estimation 
            task when using CopasiSE. This should be 'true' of you are running a parameter
            estimation from the parameter estimation task via the pycopi but 'false' when you 
            want to set up a repeat item in the scan task with the parameter estimation subtask
            
        UseTemplateStartValues:
            Default set to 'false'. Determines whether the starting parameters 
            from within the fitItemTemplate.xlsx are use for starting values
            in the parameter estimation or not
                 
        LowerBound:
            Value of the default lower bound for the FitItemTemplate. Default 0.000001
        
        UpperBound:
            Value of default upper bound for FitItemTemplate. Default=1000000
            
#        Run:
#            Run the parameter estimation using CopasiSE. When running via the parameter
#            estimation task, the output is a matrix of function evaluation progression over
#            time. When running via the scan's repeat task, output is lines of parameter
#            estimation runs
            
        Plot:
            Whether to plot result or not. Defualt='true'
            
        FontSize:
            Control graph label font size

        AxisSize:
            Control graph axis font size

        ExtraTitle:
            When SaveFig='true', given the saved
            file an extra label in the file path

        LineWidth:
            Control graph LineWidth
            
        DotSize:
            How big to plot the dots on the graph

        SaveFig:
            Save graphs to file labelled after the index


        TitleWrapSize:
            When graph titles are long, how many characters to have per 
            line before word wrap. Default=30. 
            
        Show:
            When not using iPython, use Show='true' to display graphs
            
        Ylimit: default==None, restrict amount of data shown on y axis. 
        Useful for honing in on small confidence intervals

        Xlimit: default==None, restrict amount of data shown on x axis. 
        Useful for honing in on small confidence intervals
        
        DPI:
            How big saved figure should be. Default=125
        
        XTickRotation:
            How many degrees to rotate the X tick labels
            of the output. Useful if you have very small or large
            numbers that overlay when plotting. 
            

    '''
    def __init__(self,copasi_file,experiment_files,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.experiment_files=experiment_files
        if isinstance(self.experiment_files,str):
            assert os.path.isfile(self.experiment_files),'{} is not a real file'.format(self.experiment_files)
            self.experiment_files=[self.experiment_files]
        assert isinstance(self.experiment_files,list),'The experiment_files argument needs to be a list'
        self.GMQ=GetModelQuantities(self.copasi_file)
        
        default_report_name=os.path.join(os.path.dirname(self.copasi_file),
                                         os.path.split(self.copasi_file)[1][:-4]+'_PE_results.txt')
        config_file= os.path.join(os.path.dirname(self.copasi_file),'PEConfigFile.xlsx')
        default_outputML=os.path.join(os.path.dirname(self.copasi_file),'_Duplicate.cps')
        options={#report variables
                 'Metabolites':self.GMQ.get_metabolites().keys(),
                 'GlobalQuantities':self.GMQ.get_global_quantities().keys(),
                 'LocalParameters': self.GMQ.get_local_kinetic_parameters_cns().keys(),
                 'QuantityType':'concentration',
                 'ReportName':default_report_name,
                 'Append': 'false', 
                 'SetReport':'true',
                 'ConfirmOverwrite': 'false',
                 'ConfigFilename':config_file,
                 'OverwriteConfigFile':'false',
                 'OutputML':default_outputML,
                 'PruneHeaders':'true',
                 'UpdateModel':'false',
                 'RandomizeStartValues':'true',
                 'CreateParameterSets':'false',
                 'CalculateStatistics':'false',
                 'UseTemplateStartValues':'false',
                 #method options
                 'Method':'GeneticAlgorithm',
                 #'DifferentialEvolution',
                 'NumberOfGenerations':200,
                 'PopulationSize':50,
                 'RandomNumberGenerator':1,
                 'Seed':0,
                 'Pf':0.475,
                 'IterationLimit':50,
                 'Tolerance':0.00001,
                 'Rho':0.2,
                 'Scale':10,
                 'SwarmSize':50,
                 'StdDeviation':0.000001,
                 'NumberOfIterations':100000,
                 'StartTemperature':1,
                 'CoolingFactor':0.85,
                 #experiment definition options
                 #need to include options for defining multiple experimental files at once
                 'RowOrientation':['true']*len(self.experiment_files),
                 'ExperimentType':['timecourse']*len(self.experiment_files),
                 'FirstRow':[str(1)]*len(self.experiment_files),
                 'NormalizeWeightsPerExperiment':['true']*len(self.experiment_files),
                 'RowContainingNames':[str(1)]*len(self.experiment_files),
                 'Separator':['\t']*len(self.experiment_files),
                 'WeightMethod':['mean_squared']*len(self.experiment_files),
                 'Save':'overwrite',  
                 'Scheduled':'false',
                 'Verbose':'false',
                 'LowerBound':0.000001,
                 'UpperBound':1000000,
#                 'Run':'false',
                 'Plot':'false',
                 '''
                 The below arguments get passed to the parameter
                 estimation plotting class
                 '''
                 
                 'LineWidth':4,
                 #graph features
                 'FontSize':22,
                 'AxisSize':15,
                 'ExtraTitle':None,
                 'LineWidth':3,
                 'Show':'false',
                 'SaveFig':'false',
                 'TitleWrapSize':30,
                 'Ylimit':None,
                 'Xlimit':None,
                 'DPI':125,
                 'XTickRotation':35,
                 'DotSize':10,
                 'LegendLoc':(1,0),
                 }
                     
        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for ParameterEstimation'.format(i)
        options.update( kwargs) 
        self.kwargs=options
        #second dict to separate arguments for the experiment mapper
        self.kwargs_experiment={}
        
        self.kwargs_experiment['RowOrientation']=self.kwargs.get('RowOrientation')
        self.kwargs_experiment['ExperimentType']=self.kwargs.get('ExperimentType')
        self.kwargs_experiment['FirstRow']=self.kwargs.get('FirstRow')
        self.kwargs_experiment['NormalizeWeightsPerExperiment']=self.kwargs.get('NormalizeWeightsPerExperiment')
        self.kwargs_experiment['RowContainingNames']=self.kwargs.get('RowContainingNames')
        self.kwargs_experiment['Separator']=self.kwargs.get('Separator')
        self.kwargs_experiment['WeightMethod']=self.kwargs.get('WeightMethod')
        self.kwargs_experiment['Save']=self.kwargs.get('Save')
        self.kwargs_experiment['OutputML']=self.kwargs.get('OutputML')
        
#        for i in self.kwargs_experiment.keys():
#            assert len(self.experiment_files)==len(self.kwargs_experiment.get(i)),'{} is {} and {} is {}'.format(self.experiment_files,len(self.experiment_files),(self.kwargs_experiment.get(i)),len(self.kwargs_experiment.get(i)))

        self.method_list=['CurrentSolutionStatistics','DifferentialEvolution',
                     'EvolutionaryStrategySR','EvolutionaryProgram',
                     'HookeJeeves','LevenbergMarquardt','NelderMead',
                     'ParticleSwarm','Praxis','RandomSearch','ScatterSearch','SimulatedAnnealing',
                     'SteepestDescent','TruncatedNewton','GeneticAlgorithm',
                     'GeneticAlgorithmSR']
        assert self.kwargs.get('Method').lower() in [i.lower() for i in self.method_list],'{} is not a copasi PE Method. Choose one of: {}'.format(self.kwargs.get('Method'),self.method_list)
        assert self.kwargs.get('Verbose') in ['true','false']
        assert self.kwargs.get('Append') in ['true','false']
        assert self.kwargs.get('ConfirmOverwrite') in ['true','false']
        
        if self.kwargs['Append']=='true':
            self.kwargs['Append']=str(1)
        else:
            self.kwargs['Append']=str(0)
            
        if self.kwargs['ConfirmOverwrite']=='true':
            self.kwargs['ConfirmOverwrite']=str(1)
        else:
            self.kwargs['ConfirmOverwrite']=str(0)        
            
        self.kwargs['Method']=self.kwargs.get('Method').lower()
        if self.kwargs['Method']=='currentsolutionstatistics':
            if self.kwargs['RandomizeStartValues']=='true':
                raise Errors.InputError('Cannot run current solution statistics with \'RandomizeStartValues\' set to \'true\'.' )
        write_to_file_list=['duplicate','overwrite','false']
        assert self.kwargs.get('Save') in write_to_file_list  
        
        assert isinstance(self.kwargs.get('LocalParameters'),list)
        for i in self.kwargs.get('LocalParameters'):
            assert i in self.GMQ.get_local_kinetic_parameters_cns().keys()

        assert isinstance(self.kwargs.get('GlobalQuantities'),list)
        for i in self.kwargs.get('GlobalQuantities'):
            assert i in self.GMQ.get_global_quantities().keys()
    

        assert isinstance(self.kwargs.get('Metabolites'),list)
        for i in self.kwargs.get('Metabolites'):
            assert i in self.GMQ.get_IC_cns().keys()

        if self.kwargs['UseTemplateStartValues'] not in ['true','false']:
            raise Errors.InputError(''' Argument to the UseTemplateStartValues must be \'true\' or \'false\' not {}'''.format(self.kwargs['UseTemplateStartValues']))


            
        #determine which Method to use        
        if self.kwargs.get('Method')=='CurrentSolutionStatistics'.lower():
            self.method_name='Current Solution Statistics'
            self.method_type='CurrentSolutionStatistics'

        if self.kwargs.get('Method')=='DifferentialEvolution'.lower():
            self.method_name='Differential Evolution'
            self.method_type='DifferentialEvolution'

        if self.kwargs.get('Method')=='EvolutionaryStrategySR'.lower():
            self.method_name='Evolution Strategy (SRES)'
            self.method_type='EvolutionaryStrategySR'

        if self.kwargs.get('Method')=='EvolutionaryProgram'.lower():
            self.method_name='Evolutionary Programming'
            self.method_type='EvolutionaryProgram'

        if self.kwargs.get('Method')=='HookeJeeves'.lower():
            self.method_name='Hooke &amp; Jeeves'
            self.method_type='HookeJeeves'

        if self.kwargs.get('Method')=='LevenbergMarquardt'.lower():
            self.method_name='Levenberg - Marquardt'
            self.method_type='LevenbergMarquardt'

        if self.kwargs.get('Method')=='NelderMead'.lower():
            self.method_name='Nelder - Mead'
            self.method_type='NelderMead'

        if self.kwargs.get('Method')=='ParticleSwarm'.lower():
            self.method_name='Particle Swarm'
            self.method_type='ParticleSwarm'

        if self.kwargs.get('Method')=='Praxis'.lower():
            self.method_name='Praxis'
            self.method_type='Praxis'

        if self.kwargs.get('Method')=='RandomSearch'.lower():
            self.method_name='Random Search'
            self.method_type='RandomSearch'

        if self.kwargs.get('Method')=='SimulatedAnnealing'.lower():
            self.method_name='Simulated Annealing'
            self.method_type='SimulatedAnnealing'

        if self.kwargs.get('Method')=='SteepestDescent'.lower():
            self.method_name='Steepest Descent'
            self.method_type='SteepestDescent'

        if self.kwargs.get('Method')=='TruncatedNewton'.lower():
            self.method_name='Truncated Newton'
            self.method_type='TruncatedNewton'

        if self.kwargs.get('Method')=='ScatterSearch'.lower():
            self.method_name='Scatter Search'
            self.method_type='ScatterSearch'

        if self.kwargs.get('Method')=='GeneticAlgorithm'.lower():
            self.method_name='Genetic Algorithm'
            self.method_type='GeneticAlgorithm'

        if self.kwargs.get('Method')=='GeneticAlgorithmSR'.lower():
            self.method_name='Genetic Algorithm SR'
            self.method_type='GeneticAlgorithmSR'
    

            
        assert self.kwargs.get('CreateParameterSets') in ['false','true']
        if self.kwargs.get('CreateParameterSets')=='false':
            self.kwargs['CreateParameterSets']=str(0)
        else:
            self.kwargs['CreateParameterSets']=str(1)
            
        assert self.kwargs.get('CalculateStatistics') in ['false','true']
        if self.kwargs.get('CalculateStatistics')=='false':
            self.kwargs['CalculateStatistics']=str(0)
        else:
            self.kwargs['CalculateStatistics']=str(1)

        assert self.kwargs.get('Plot') in ['false','true']



        if isinstance(self.kwargs.get('Metabolites'),str):
            self.kwargs['Metabolites']=[self.kwargs.get('Metabolites')]

        if isinstance(self.kwargs.get('GlobalQuantities'),str):
            self.kwargs['GlobalQuantities']=[self.kwargs.get('GlobalQuantities')]

        if isinstance(self.kwargs.get('LocalParameters'),str):
            self.kwargs['LocalParameters']=[self.kwargs.get('LocalParameters')]




        self.kwargs['NumberOfGenerations']=str(self.kwargs.get('NumberOfGenerations'))
        self.kwargs['PopulationSize']=str(self.kwargs.get('PopulationSize'))
        self.kwargs['RandomNumberGenerator']=str(self.kwargs.get('RandomNumberGenerator'))
        self.kwargs['Seed']=str(self.kwargs.get('Seed'))
        self.kwargs['Pf']=str(self.kwargs.get('Pf'))
        self.kwargs['IterationLimit']=str(self.kwargs.get('IterationLimit'))
        self.kwargs['Tolerance']=str(self.kwargs.get('Tolerance'))
        self.kwargs['Rho']=str(self.kwargs.get('Rho'))
        self.kwargs['Scale']=str(self.kwargs.get('Scale'))
        self.kwargs['Scale']=str(self.kwargs.get('Scale'))
        self.kwargs['SwarmSize']=str(self.kwargs.get('SwarmSize'))
        self.kwargs['StdDeviation']=str(self.kwargs.get('StdDeviation'))
        self.kwargs['NumberOfIterations']=str(self.kwargs.get('NumberOfIterations'))
        self.kwargs['StartTemperature']=str(self.kwargs.get('StartTemperature'))
        self.kwargs['CoolingFactor']=str(self.kwargs.get('CoolingFactor'))
        self.kwargs['LowerBound']=str( self.kwargs.get('LowerBound'))
        self.kwargs['StartValue']=str( self.kwargs.get('StartValue'))
        self.kwargs['UpperBound']=str( self.kwargs.get('UpperBound'))
        
        
        #report specific arguments
        self.report_dict={}
        self.report_dict['Metabolites']=self.kwargs.get('Metabolites')
        self.report_dict['GlobalQuantities']=self.kwargs.get('GlobalQuantities')
        self.report_dict['LocalParameters']=self.kwargs.get('LocalParameters')
        self.report_dict['QuantityType']=self.kwargs.get('QuantityType')
        self.report_dict['ReportName']=self.kwargs.get('ReportName')
        self.report_dict['Append']=self.kwargs.get('Append')
        self.report_dict['ConfirmOverwrite']=self.kwargs.get('ConfirmOverwrite')
        self.report_dict['Save']=self.kwargs.get('Save')
        self.report_dict['OutputML']=self.kwargs.get('OutputML')
        self.report_dict['Variable']=self.kwargs.get('Variable')
        self.report_dict['ReportType']='parameter_estimation'
        
        assert self.kwargs.get('SetReport') in ['false','true']
#        assert self.kwargs.get('Run') in ['true','false']
        
        
        '''
        PlotPEDataKwargs plotting specific kwargs
        '''
        self.PlotPEDataKwargs={}
        self.PlotPEDataKwargs['LineWidth']=self.kwargs.get('LineWidth')
        self.PlotPEDataKwargs['FontSize']=self.kwargs.get('FontSize')
        self.PlotPEDataKwargs['AxisSize']=self.kwargs.get('AxisSize')
        self.PlotPEDataKwargs['ExtraTitle']=self.kwargs.get('ExtraTitle')
        self.PlotPEDataKwargs['Show']=self.kwargs.get('Show')
        self.PlotPEDataKwargs['SaveFig']=self.kwargs.get('SaveFig')
        self.PlotPEDataKwargs['TitleWrapSize']=self.kwargs.get('TitleWrapSize')
        self.PlotPEDataKwargs['Ylimit']=self.kwargs.get('Ylimit')
        self.PlotPEDataKwargs['Xlimit']=self.kwargs.get('Xlimit')
        self.PlotPEDataKwargs['DPI']=self.kwargs.get('DPI')
        self.PlotPEDataKwargs['XTickRotation']=self.kwargs.get('XTickRotation')
        self.PlotPEDataKwargs['DotSize']=self.kwargs.get('DotSize')
        self.PlotPEDataKwargs['LegendLoc']=self.kwargs.get('LegendLoc')
        self.PlotPEDataKwargs['PruneHeaders']=self.kwargs.get('PruneHeaders')
        self.PlotPEDataKwargs['Separator']=self.kwargs.get('Separator')
        
            
        

    def clear_pe(self):
        pass

    def run(self):
        if self.kwargs.get('Plot')=='false':
            LOG.debug('Running ParameterEstimation. Data reported to file: {}'.format(self.kwargs['ReportName']))
            self.copasiML=Run(self.copasi_file,Task='parameter_estimation')
            return self.copasiML
        else:
            ##Run with 'Mode' set to false just unchecks the executable boxes.
            self.copasiML=Run(self.copasi_file,Task='parameter_estimation',Mode='false')
            ## Now run with check_call
            subprocess.check_call('CopasiSE "{}"'.format(self.copasi_file),shell=True)
            self.plot()
        return self.copasiML
        
        
    def convert_to_string(self,num):
        '''
        convert a number to a string        
        '''
        return str(num)
        
    def get_fit_items(self):
        d={}
        query='//*[@name="FitItem"]'
        for i in self.copasiML.xpath(query):
            for j in list(i):
                if j.attrib['name']=='ObjectCN':
                    match=re.findall('Reference=(.*)',j.attrib['value'])[0]
                    if match=='Value':
                        match2=re.findall('Reactions\[(.*)\].*Parameter=(.*),', j.attrib['value'])
                        if match2!=[]:
                            match2='({}).{}'.format(match2[0][0],match2[0][1])
#                    d[match2]=j.attrib
                    elif match=='InitialValue':
                        match2=re.findall('Values\[(.*)\]', j.attrib['value'])
                        if match2!=[]:
                            match2=match2[0]
                    elif match=='InitialConcentration':
                        match2=re.findall('Metabolites\[(.*)\]',j.attrib['value'])
                        if match2!=[]:
                            match2=match2[0]
                    if match2!=[]:
                        d[match2]=j.attrib    
        return d
        
    def remove_fit_item(self,item):
        query='//*[@name="FitItem"]'
        all_items= self.get_fit_items().keys()
        assert item in all_items,'{} is not a fit item. These are the fit items: {}'.format(item,all_items)
        item=self.get_fit_items()[item]
        for i in self.copasiML.xpath(query):
            for j in list(i):
                if j.attrib['name']=='ObjectCN':
                    #locate references
                    #remove local parameters from PE task
                    match=re.findall('Reference=(.*)',j.attrib['value'])[0]
                    if match=='Value':
                        pattern='Reactions\[(.*)\].*Parameter=(.*),Reference=(.*)'
                        match2_copasiML=re.findall(pattern, j.attrib['value'])
                        if match2_copasiML!=[]:
                            match2_item=re.findall(pattern, item['value'])
                            if match2_item!=[]:
                                if match2_item==match2_copasiML:
                                    i.getparent().remove(i)
                    #rempve global parameters from PE task 
                    elif match=='InitialValue':
                        pattern='Values\[(.*)\].*Reference=(.*)'
                        match2_copasiML=re.findall(pattern, j.attrib['value'])
                        if match2_copasiML!=[]:
                            match2_item=re.findall(pattern,item['value'])
                            if match2_item==match2_copasiML:
                                i.getparent().remove(i)
                    #remove IC parameters from PE task
                    elif match=='InitialConcentration' or match=='InitialParticleNumber':
                        pattern='Metabolites\[(.*)\],Reference=(.*)'
                        match2_copasiML=re.findall(pattern,j.attrib['value'])
                        if match2_copasiML!=[]:
                            if match2_copasiML[0][1]=='InitialConcentration' or match2_copasiML[0][1]=='InitialParticleNumber':
                                match2_item=re.findall(pattern,item['value'])
                                if match2_item!=[]:
                                    if match2_item==match2_copasiML:
                                        i.getparent().remove(i)
                    else:
                        raise TypeError('Parameter {} is not a local parameter, initial concentration parameter or a global parameter.initial_value'.format(match2_item))
        return self.copasiML

 
    def remove_all_fit_items(self):
        for i in self.get_fit_items():
            self.copasiML=self.remove_fit_item(i)
        return self.copasiML
        

        
    def write_item_template(self):
        if os.path.isfile(self.kwargs.get('ConfigFilename'))==False or self.kwargs.get('OverwriteConfigFile')=='true':
            self.get_item_template().to_excel(self.kwargs.get('ConfigFilename'))
        return  'writing template. {} set to {} and {} is {}'.format('OverwriteConfigFile',self.kwargs.get('OverwriteConfigFile'),'ConfigFilename',self.kwargs.get('ConfigFilename'))

        
    def read_item_template(self):
        if os.path.isfile(self.kwargs.get('ConfigFilename'))==False:
            self.write_item_template()
        assert os.path.isfile(self.kwargs.get('ConfigFilename'))==True,'ItemTemplate file does not exist. Run \'write_item_template\' method and modify it how you like then rerun this method'
        return pandas.read_excel(self.kwargs.get('ConfigFilename'))
    
    def add_fit_item(self,item):
        '''
        
        need 5 elements, each with their own attributes. Their names are:
            Affected Cross Validation Experiments
            Affected Experiments
            LowerBound
            ObjectCN
            StartValue
            UpperBound
            
        the element name is <ParameterGroup name="FitItem">
        '''
        #initialize new element
        new_element=etree.Element('ParameterGroup',attrib={'name':'FitItem'})
        all_items= self.read_item_template()
        assert item in list(all_items.index),'{} is not in your ItemTemplate. You item template contains: {}'.format(item,list(all_items.index))
        item= all_items.loc[item]
        subA1={'name': 'Affected Cross Validation Experiments'}
        subA2={'name': 'Affected Experiments'}
        subA3={'type': 'cn', 'name': 'LowerBound', 'value': str(item['LowerBound'])}
        if self.kwargs.get('UseTemplateStartValues')=='true':
            subA5={'type': 'float', 'name': 'StartValue', 'value': str(item['StartValue'])}
        
        subA6={'type': 'cn', 'name': 'UpperBound', 'value': str(item['UpperBound'])}
        
        etree.SubElement(new_element,'ParameterGroup',attrib=subA1)
        etree.SubElement(new_element,'ParameterGroup',attrib=subA2)
        etree.SubElement(new_element,'Parameter',attrib=subA3)
        if self.kwargs.get('UseTemplateStartValues')=='true':
            etree.SubElement(new_element,'Parameter',attrib=subA5)
        etree.SubElement(new_element,'Parameter',attrib=subA6)
        
        #for IC parameters
        if item['simulationType']=='reactions' and item['type']=='Species':
            #fill in the attributes
            if self.kwargs.get('QuantityType')=='concentration':
                subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialConcentration'}
            else:
                subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialParticleNumber'}

        elif item['simulationType']=='ode' and item['type']=='Species':
            if self.kwargs.get('QuantityType')=='concentration':
                subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialConcentration'}
            else:
                subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialParticleNumber'}

        elif item['simulationType']=='ode' and item['type']=='ModelValue':
            if self.kwargs.get('QuantityType')=='concentration':
                subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialConcentration'}
            else:
                subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialParticleNumber'}


        elif item['simulationType']=='fixed' and item['type']=='ReactionParameter':
            subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=Value'}

        elif item['simulationType']=='assignment' and item['type']=='ModelValue':
#            logger.info('{} is an assignment and can therefore not be estimated!'.format(list(item.index)))
            return self.copasiML
        elif item['simulationType']=='fixed' and item['type']=='ModelValue':
            subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialValue'}


        elif item['simulationType']=='assignment' and item['type']=='Species':
            return self.copasiML
 
        elif item['simulationType']=='fixed' and item['type']=='Species':
            return self.copasiML           
        else:
            raise Errors.InputError('{} is not a valid parameter for estimation'.format(list(item)))
        etree.SubElement(new_element,'Parameter',attrib=subA4)

        query='//*[@name="OptimizationItemList"]'
        for i in self.copasiML.xpath(query):
            i.append(new_element)
        return self.copasiML

    def insert_all_fit_items(self):
        parameter_list= list(self.read_item_template().index)
        for i in parameter_list:
            assert i!='nan'
            self.copasiML=self.add_fit_item(i)
        return self.copasiML
        
        
    def set_PE_method(self):
        '''
        Choose PE algorithm and set algorithm specific parameters 
        '''
        #Build XML for method. Root=Method for now. Will be merged with CoapsiML later
        method_params={'name':self.method_name, 'type':self.method_type}
        method_element=etree.Element('Method',attrib=method_params)

        #list of attribute dictionaries 
        #Evolutionary strategy parametery
        NumberOfGenerations={'type': 'unsignedInteger', 'name': 'Number of Generations', 'value': self.kwargs.get('NumberOfGenerations')}
        PopulationSize={'type': 'unsignedInteger', 'name': 'Population Size', 'value': self.kwargs.get('PopulationSize')}
        RandomNumberGenerator={'type': 'unsignedInteger', 'name': 'Random Number Generator', 'value': self.kwargs.get('RandomNumberGenerator')}
        Seed={'type': 'unsignedInteger', 'name': 'Seed', 'value': self.kwargs.get('Seed')}
        Pf={'type': 'float', 'name': 'Pf', 'value': self.kwargs.get('Pf')}
        #local method parameters
        IterationLimit={'type': 'unsignedInteger', 'name': 'Iteration Limit', 'value': self.kwargs.get('IterationLimit')}
        Tolerance={'type': 'float', 'name': 'Tolerance', 'value': self.kwargs.get('Tolerance')}
        Rho={'type': 'float', 'name': 'Rho', 'value': self.kwargs.get('Rho')}
        Scale={'type': 'unsignedFloat', 'name': 'Scale', 'value': self.kwargs.get('Scale')}
        #Particle Swarm parmeters
        SwarmSize={'type': 'unsignedInteger', 'name': 'Swarm Size', 'value': self.kwargs.get('SwarmSize')}
        StdDeviation={'type': 'unsignedFloat', 'name': 'Std. Deviation', 'value': self.kwargs.get('StdDeviation')}
        #Random Search parameters
        NumberOfIterations={'type': 'unsignedInteger', 'name': 'Number of Iterations', 'value': self.kwargs.get('NumberOfIterations')}
        #Simulated Annealing parameters
        StartTemperature={'type': 'unsignedFloat', 'name': 'Start Temperature', 'value': self.kwargs.get('StartTemperature')}
        CoolingFactor={'type': 'unsignedFloat', 'name': 'Cooling Factor', 'value': self.kwargs.get('CoolingFactor')}


        #build the appropiate XML, with method at root (for now)
        if self.kwargs.get('Method')=='CurrentSolutionStatistics'.lower():
            pass #no additional parameter elements required

        if self.kwargs.get('Method')=='DifferentialEvolution'.lower():
            etree.SubElement(method_element,'Parameter',attrib=NumberOfGenerations)
            etree.SubElement(method_element,'Parameter',attrib=PopulationSize)
            etree.SubElement(method_element,'Parameter',attrib=RandomNumberGenerator)
            etree.SubElement(method_element,'Parameter',attrib=Seed)

        if self.kwargs.get('Method')=='EvolutionaryStrategySR'.lower():
            etree.SubElement(method_element,'Parameter',attrib=NumberOfGenerations)
            etree.SubElement(method_element,'Parameter',attrib=PopulationSize)
            etree.SubElement(method_element,'Parameter',attrib=RandomNumberGenerator)
            etree.SubElement(method_element,'Parameter',attrib=Seed)
            etree.SubElement(method_element,'Parameter',attrib=Pf)

        if self.kwargs.get('Method')=='EvolutionaryProgram'.lower():
            etree.SubElement(method_element,'Parameter',attrib=NumberOfGenerations)
            etree.SubElement(method_element,'Parameter',attrib=PopulationSize)
            etree.SubElement(method_element,'Parameter',attrib=RandomNumberGenerator)
            etree.SubElement(method_element,'Parameter',attrib=Seed)

        if self.kwargs.get('Method')=='HookeJeeves'.lower():
            etree.SubElement(method_element,'Parameter',attrib=IterationLimit)
            etree.SubElement(method_element,'Parameter',attrib=Tolerance)
            etree.SubElement(method_element,'Parameter',attrib=Rho)

        if self.kwargs.get('Method')=='LevenbergMarquardt'.lower():
            etree.SubElement(method_element,'Parameter',attrib=IterationLimit)
            etree.SubElement(method_element,'Parameter',attrib=Tolerance)
#
        if self.kwargs.get('Method')=='NelderMead'.lower():
            etree.SubElement(method_element,'Parameter',attrib=IterationLimit)
            etree.SubElement(method_element,'Parameter',attrib=Tolerance)
            etree.SubElement(method_element,'Parameter',attrib=Scale)

        if self.kwargs.get('Method')=='ParticleSwarm'.lower():
            etree.SubElement(method_element,'Parameter',attrib=IterationLimit)
            etree.SubElement(method_element,'Parameter',attrib=SwarmSize)
            etree.SubElement(method_element,'Parameter',attrib=StdDeviation)
            etree.SubElement(method_element,'Parameter',attrib=RandomNumberGenerator)
            etree.SubElement(method_element,'Parameter',attrib=Seed)

        if self.kwargs.get('Method')=='Praxis'.lower():
            etree.SubElement(method_element,'Parameter',attrib=Tolerance)

        if self.kwargs.get('Method')=='RandomSearch'.lower():
            etree.SubElement(method_element,'Parameter',attrib=NumberOfIterations)
            etree.SubElement(method_element,'Parameter',attrib=RandomNumberGenerator)
            etree.SubElement(method_element,'Parameter',attrib=Seed)

        if self.kwargs.get('Method')=='SimulatedAnnealing'.lower():
            etree.SubElement(method_element,'Parameter',attrib=StartTemperature)
            etree.SubElement(method_element,'Parameter',attrib=CoolingFactor)
            etree.SubElement(method_element,'Parameter',attrib=Tolerance)
            etree.SubElement(method_element,'Parameter',attrib=RandomNumberGenerator)
            etree.SubElement(method_element,'Parameter',attrib=Seed)
#
        if self.kwargs.get('Method')=='SteepestDescent'.lower():
            etree.SubElement(method_element,'Parameter',attrib=IterationLimit)
            etree.SubElement(method_element,'Parameter',attrib=Tolerance)
#
        if self.kwargs.get('Method')=='TruncatedNewton'.lower():
            #required no additonal paraemters
            pass
#
        if self.kwargs.get('Method')=='ScatterSearch'.lower():
            etree.SubElement(method_element,'Parameter',attrib=NumberOfIterations)


        if self.kwargs.get('Method')=='GeneticAlgorithm'.lower():
            etree.SubElement(method_element,'Parameter',attrib=NumberOfGenerations)
            etree.SubElement(method_element,'Parameter',attrib=PopulationSize)
            etree.SubElement(method_element,'Parameter',attrib=RandomNumberGenerator)
            etree.SubElement(method_element,'Parameter',attrib=Seed)            

        if self.kwargs.get('Method')=='GeneticAlgorithmSR'.lower():
            etree.SubElement(method_element,'Parameter',attrib=NumberOfGenerations)
            etree.SubElement(method_element,'Parameter',attrib=PopulationSize)
            etree.SubElement(method_element,'Parameter',attrib=RandomNumberGenerator)
            etree.SubElement(method_element,'Parameter',attrib=Seed)  
            etree.SubElement(method_element,'Parameter',attrib=Pf)  

        
        tasks=self.copasiML.find('{http://www.copasi.org/static/schema}ListOfTasks')

        method= tasks[5][-1]
        parent=method.getparent()
        parent.remove(method)
        parent.insert(2,method_element)
        return self.copasiML

    def define_report(self):
        return Reports(self.copasi_file,**self.report_dict).copasiML

    def get_report_key(self):
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name'].lower()=='parameter_estimation':
                key=i.attrib['key']
        assert key!=None
        return key
        
    def set_PE_options(self):
        '''

            
        '''
        
        scheluled_attrib={'scheduled': self.kwargs.get('Scheduled'),
                          'updateModel': self.kwargs.get('UpdateModel')}
                          
        report_attrib={'append': self.kwargs.get('Append'),
                       'reference': self.get_report_key(),
                       'target': self.kwargs.get('ReportName'),
                       'confirmOverwrite': self.kwargs.get('ConfirmOverwrite')}

        randomize_start_values={'type': 'bool', 
                                'name': 'Randomize Start Values', 
                                'value': self.kwargs.get('RandomizeStartValues')}
        calculate_stats={'type': 'bool', 'name': 'Calculate Statistics', 'value': self.kwargs.get('CalculateStatistics')}
        create_parameter_sets={'type': 'bool', 'name': 'Create Parameter Sets', 'value': self.kwargs.get('CreateParameterSets')}

        query='//*[@name="Parameter Estimation"]' and '//*[@type="parameterFitting"]'
        for i in self.copasiML.xpath(query):
            i.attrib.update(scheluled_attrib)
            for j in list(i):
                if self.kwargs.get('SetReport')=='true':
                    if self.kwargs.get('ReportName')!=None:
                        if 'append' in j.attrib.keys():
                            j.attrib.update(report_attrib)
                if list(j)!=[]:
                    for k in list(j):
                        if k.attrib['name']=='Randomize Start Values':
                            k.attrib.update(randomize_start_values)
                        elif k.attrib['name']=='Calculate Statistics':
                            k.attrib.update(calculate_stats)
                        elif k.attrib['name']=='Create Parameter Sets':
                            k.attrib.update(create_parameter_sets)
        return self.copasiML
        
      
    def get_item_template(self):
        local_params= self.GMQ.get_local_kinetic_parameters_cns()
        global_params= self.GMQ.get_global_quantities_cns()
        IC_params= self.GMQ.get_IC_cns()
        df_list_local=[]
        df_list_global=[]
        df_list_ICs=[]
        for i in local_params.keys():
            df= pandas.DataFrame.from_dict(local_params[i].values())
            df.index=local_params[i].keys()
            df.columns=[i]
            df=df.transpose()
            df_list_local.append(df)
        
            
        for i in global_params.keys():
            df= pandas.DataFrame.from_dict(global_params[i].values())
            df.index=global_params[i].keys()
            df.columns=[i]
            df=df.transpose()
            df_list_global.append(df)
            
        for i in IC_params.keys():
            df= pandas.DataFrame.from_dict(IC_params[i].values())
            df.index=IC_params[i].keys()
            df.columns=[i]
            df=df.transpose()
            if self.kwargs.get('QuantityType')=='concentration':
                df=df.drop('value',axis=1)
                df=df.rename(columns={'concentration':'value'})
            elif self.kwargs.get('Quantitytype')=='particle_number':
                df=df.drop('concentration',axis=1)
            df_list_ICs.append(df)
        l=df_list_local+df_list_global+df_list_ICs
        assert len(l)!=0,'No ICs, local or global quantities in your model'
        df= pandas.concat(l)
        df=df.rename(columns={'value':'StartValue'})
        df['LowerBound']=[self.kwargs.get('LowerBound')]*df.shape[0]
#        df['startValue']=[self.kwargs.get('StartValue')]*df.shape[0]
        df['UpperBound']=[self.kwargs.get('UpperBound')]*df.shape[0]
        df.index.name='Parameter'
        order=['StartValue','LowerBound','UpperBound','simulationType','type','cn']
        df=df[order]
        return df

    def save(self):
        if self.kwargs.get('Save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('Save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML
            
    def set_up(self):
        EM=ExperimentMapper(self.copasi_file,self.experiment_files,**self.kwargs_experiment)
        self.copasiML=EM.copasiML
        self.copasiML=self.define_report()
        self.copasiML=self.remove_all_fit_items()
        self.copasiML=self.set_PE_method()
        self.copasiML=self.set_PE_options()
        self.copasiML=self.insert_all_fit_items()
        self.copasiML=self.save()
        
    def plot(self):
        '''
        Use the PlotPEData class to plot results 
        '''
#        if self.kwargs.get('UpdateModel')=='true':
#            copasi_file=self.copasi_file
#        else:
#            #copasi_file=self.copasi_file[:-4]+'_temp.cps'
#            shutil.copy(self.copasi_file,copasi_file)
        self.PL=PEAnalysis.PlotPEData(self.copasi_file,self.experiment_files,self.kwargs.get('ReportName'),
                        **self.PlotPEDataKwargs)

#==============================================================================

class Scan():
    '''
    Positional Args:
        copasi_file:
            the copasi file you want to scan

    **kwargs:
        ScanType:
            Which type of scan do you want to set up. 
            Options are ['scan','repeat','random_sampling']

        Metabolites:
            Metabolites to pass to report 
        
        GlobalQuantities:
            global wuantities to pass to report
            
        QuantityType:
            either 'concentration' or 'particle_number'
        
        ReportName:
            Name the output report
            
        Append:
            Check the Append button in copasi scan task.
            Options are ['true' or 'false'], default='false'
            
        ConfirmOverwrite:
            Check the confirm overwrite button in copasi scan.
            Options are ['true' or 'false'], default='false'

        OutputML:
            If Save set to duplicate, this is the name of 
            the duplicated copasi file.Options are ['true' or 'false'], 
            default='false'
            
        UpdateModel:
            Check the update model button in copasi scan task
            Options are ['true' or 'false'], default='false'
        
        SubTask:
            A valid scan subtask. Options are:
            ['steady_state','time_course','metabolic_control_nalysis',
            'lyapunov_exponents','optimiztion','parameter_estimation',
            'sensitivities','linear_noise_approximation','cross_section',
            'time_scale_separation_analysis']
                   
        ReportType:
            Which type of report to use. Options are ['none',
            'profilelikelihood','time_course','parameter_estimation']
            
        OutputInSubtask:
            Check the OutputInSubtask button in copasi scan task
            Options are ['true' or 'false'], default='false'

        AdjustInitialConditions:
            Check the AdjustInitialConditions button in copasi scan task
            Options are ['true' or 'false'], default='false'
            
        NumberOfSteps:
            Corresponds to the Intervals box in Copasi GUI or number
            of repeats in case your using the Task='repeat' option. Default=10. 
            
        Maximum: 
            Corresponds to the Maximum box in Copasi GUI. Default=100. 

        Minimum: 
            Corresponds to the Minimum box in Copasi GUI. Default=0.01. 

        Log: 
            Corresponds to the Log box in Copasi GUI.
            Options are ['true' or 'false'], default='false'.  
            
        DistributionType:
            When ScanType set to 'random_sampling', can be any of
            ['normal','uniform','poisson','gamma']. Default='normal'
            
        Variable:
            The target of the Scan. Must be a valid model entity. 
            Defaults to the first key in the GMQ.get_metabolites() method

        Scheduled: 
            Corresponds to the Scheduled box in Copasi GUI. Default='true'.
            
        Save:
            Can be one of ['duplicate','false','overwrite']. Duplicate
            will copy copasi file to different file name. Default='overwrite'
            
        ClearScans:
            'true' or 'false'. If 'true' will remove all scans present before
            adding scans. If false, will add another scan in addition to any
            scans alredy present.Default='true'
        
        Variable:
            Only used when the report is profile likelihood. Corresponds to 
            parameter of interest. Must be a model entity. Default=None
            
        Run:
            Run Scan task or not. 'true' or 'false' or 'SGE'. Default='false'
            
    '''
    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=GetModelQuantities(self.copasi_file)
        
        default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_PE_results.txt'
        default_outputML=os.path.split(self.copasi_file)[1][:-4]+'_Duplicate.cps'
        options={#report variables
                 'Metabolites':self.GMQ.get_metabolites().keys(),
                 'GlobalQuantities':self.GMQ.get_global_quantities().keys(),
                 'QuantityType':'concentration',
                 'ReportName':default_report_name,
                 'Append': 'false', 
                 'ConfirmOverwrite': 'false',
                 'OutputML':default_outputML,
                 #
                 'UpdateModel':'false',
                 'SubTask':'parameter_estimation',
                 'ReportType':'profilelikelihood',
                 'OutputInSubtask':'false',
                 'AdjustInitialConditions':'false',
                 'NumberOfSteps':10,
                 'Maximum':100,
                 'Minimum':0.01,
                 'Log':'false',
                 'DistributionType':'normal',
                 'ScanType':'scan',
                 #scan object specific (for scan and random_sampling ScanTypes)
                 'Variable':self.GMQ.get_metabolites().keys()[0],
                 'Scheduled':'true',
                 'Save':'overwrite',
                 'ClearScans':'true',#if true, will remove all scans present then add new scan
                 'Run':'false'}
                                  
                 
                     
        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for Scan'.format(i)
        options.update( kwargs) 
        self.kwargs=options
        
        #correct OutputInSubtask and AsjestInitialConditions
        assert self.kwargs.get('OutputInSubtask') in ['false','true']
        assert self.kwargs.get('AdjustInitialConditions') in ['false','true']
        assert self.kwargs.get('Log') in ['false','true'],'{} is not either \'false\' or \'true\''.format(self.kwargs.get('Log'))
        
        if self.kwargs.get('OutputInSubtask')=='false':
            self.kwargs['OutputInSubtask']=str(0)
        else:
            self.kwargs['OutputInSubtask']=str(1)
            
        if self.kwargs.get('AdjustInitialConditions')=='false':
            self.kwargs['AdjustInitialConditions']=str(0)
        else:
            self.kwargs['AdjustInitialConditions']=str(1)
        
        if self.kwargs.get('Log')=='false':
            self.kwargs['Log']=str(0)
        else:
            self.kwargs['Log']=str(1)
            
        
        subtasks=['steady_state','time_course',
                   'metabolic_control_nalysis',
                   'lyapunov_exponents',
                   'optimiztion','parameter_estimation',
                   'sensitivities','linear_noise_approximation',
                   'cross_section','time_scale_separation_analysis']
                   
        report_types=['none','profilelikelihood','time_course','parameter_estimation']
        dist_types=['normal','uniform','poisson','gamma']
        scan_types=['scan','repeat','random_sampling']
        quantity_type_list=['particle_number','concentration']
        
                   
        assert self.kwargs.get('SubTask') in subtasks                   
        assert self.kwargs.get('ReportType') in report_types,'{} is not in {}'.format(self.kwargs.get('ReportType'),report_types)
        assert self.kwargs.get('DistributionType') in dist_types
        assert self.kwargs.get('ScanType') in scan_types
        assert self.kwargs.get('QuantityType') in quantity_type_list
        assert self.kwargs.get('Scheduled') in ['true','false']
        assert self.kwargs.get('ClearScans') in ['true','false']
        assert self.kwargs.get('Run') in ['true','false','SGE']


        #numericify the some keyword arguments
        subtask_numbers=[0,1,6,7,4,5,9,12,11,8]
        for i in zip(subtasks,subtask_numbers):
            if i[0]==self.kwargs.get('SubTask'):
                self.kwargs['SubTask']=str(i[1])
        
        #numericidy type keywork arguments 
        scan_type_numbers=[1,0,2]
        for i in zip(scan_types,scan_type_numbers):
            if i[0]==self.kwargs.get('ScanType'):
                self.kwargs['ScanType']=str(i[1])   
                
        dist_types_numbers=[0,1,2,3]
        for i in zip(dist_types,dist_types_numbers):
            if i[0]==self.kwargs.get('DistributionType'):
                self.kwargs['DistributionType']=str(i[1])    
                
        assert self.kwargs.get('Variable') in self.GMQ.get_IC_cns().keys() or self.GMQ.get_global_quantities_cns().keys() or self.GMQ.get_local_kinetic_parameters_cns()
        
        #convert what needs to be a string to a string
        self.kwargs['OutputInSubtask']=str(self.kwargs['OutputInSubtask'])
        self.kwargs['AdjustInitialConditions']=str(self.kwargs['AdjustInitialConditions'])
        self.kwargs['NumberOfSteps']=str(self.kwargs['NumberOfSteps'])
        self.kwargs['Maximum']=str(self.kwargs['Maximum'])
        self.kwargs['Minimum']=str(self.kwargs['Minimum'])
        self.kwargs['Log']=str(self.kwargs['Log'])

        assert isinstance(self.kwargs.get('NumberOfSteps'),(float,int,str))
        assert isinstance(self.kwargs.get('Maximum'),(float,int,str))
        assert isinstance(self.kwargs.get('Minimum'),(float,int,str))
        
        if isinstance(self.kwargs.get('NumberOfSteps'),(float,int)):
            self.kwargs['NumberOfSteps']=str(self.kwargs.get('NumberOfSteps'))
            
        if isinstance(self.kwargs.get('Maximum'),(float,int)):
            self.kwargs['Maximum']=str(self.kwargs.get('Maximum'))
            
        if isinstance(self.kwargs.get('Minimum'),(float,int)):
            self.kwargs['Minimum']=str(self.kwargs.get('Minimum'))

#        if self.kwargs.get('ReportType')=='time_course':
#            self.kwargs['ReportType']='time-course'
        write_to_file_list=['duplicate','overwrite','false']
        assert self.kwargs.get('Save') in write_to_file_list,'{} not in {}'.format(self.kwargs.get('Save'),write_to_file_list)
        
        if self.kwargs.get('ClearScans')=='true':
            self.copasiML=self.remove_scans()
            self.copasiML=self.save()
        self.copasiML=self.define_report()
        self.copasiML=self.create_scan()
        self.copasiML=self.set_scan_options()
        self.copasiML=self.save()
        self.run()
        
            
#            PruneCopasiHeaders(self.kwargs['ReportName'],replace='true')
            
            
            
        
    def save(self):
        if self.kwargs.get('Save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('Save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML
                
        
    def define_report(self):
        '''
        
        '''
        logging.info('defining report')
        self.report_dict={}
        self.report_dict['Metabolites']=self.kwargs.get('Metabolites')
        self.report_dict['GlobalQuantities']=self.kwargs.get('GlobalQuantities')
        self.report_dict['QuantityType']=self.kwargs.get('QuantityType')
        self.report_dict['ReportName']=self.kwargs.get('ReportName')
        self.report_dict['Append']=self.kwargs.get('Append')
        self.report_dict['ConfirmOverwrite']=self.kwargs.get('ConfirmOverwrite')
        self.report_dict['Save']=self.kwargs.get('Save')
        self.report_dict['OutputML']=self.kwargs.get('OutputML')
        self.report_dict['Variable']=self.kwargs.get('Variable')
        self.report_dict['ReportType']=self.kwargs.get('ReportType')
        
        R= Reports(self.copasi_file,**self.report_dict)
        return R.copasiML
        
        
    def get_report_key(self):
        '''
        
        '''
        #ammend the time course option
        if self.kwargs.get('ReportType').lower()=='time_course':
            self.kwargs['ReportType']='time-course'
        key=None
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name'].lower()==self.kwargs.get('ReportType').lower():
                key=i.attrib['key']
        if key==None:
            raise Errors.ReportDoesNotExistError('Report doesn\'t exist. Check to see if you have either defined the report manually or used the pycopi.Reports class')
        return key
        
    def create_scan(self):
        '''
        need to find a report key which corresponds to the report we want to use
        '''
        #get cn value
        if self.kwargs.get('Variable') in self.GMQ.get_IC_cns().keys():
            if self.kwargs.get('QuantityType')=='concentration':
                cn= self.GMQ.get_IC_cns()[self.kwargs.get('Variable')]['cn']+',Reference=InitialConcentration'
            elif self.kwargs.get('QuantityType')=='particle_number':
                cn= self.GMQ.get_IC_cns()[self.kwargs.get('Variable')]['cn']+',Reference=InitialParticleNumber'
        elif self.kwargs.get('Variable') in self.GMQ.get_global_quantities_cns().keys():
            cn= self.GMQ.get_global_quantities_cns()[self.kwargs.get('Variable')]['cn']+',Reference=InitialValue'
        elif self.kwargs.get('Variable') in self.GMQ.get_local_kinetic_parameters_cns().keys():
            cn =self.GMQ.get_local_kinetic_parameters_cns()[self.kwargs.get('Variable')]['cn']+',Reference=Value'


        number_of_steps_attrib={'type': 'unsignedInteger', 'name': 'Number of steps', 'value': self.kwargs.get('NumberOfSteps')}
        scan_item={'type': 'cn', 'name': 'Object', 'value': cn}
        type_attrib={'type': 'unsignedInteger', 'name': 'Type', 'value': self.kwargs.get('ScanType')}
        maximum_attrib={'type': 'float', 'name': 'Maximum', 'value': self.kwargs.get('Maximum')}
        minimum_attrib={'type': 'float', 'name': 'Minimum', 'value': self.kwargs.get('Minimum')}
        log_attrib={'type': 'bool', 'name': 'log', 'value': self.kwargs.get('Log')}
        dist_type_attrib={'type': 'unsignedInteger', 'name': 'Distribution type', 'value': self.kwargs.get('DistributionType')}

        scanItem_element=etree.Element('ParameterGroup',attrib={'name':'ScanItem'})
        
        if self.kwargs.get('ScanType')=='1':
            etree.SubElement(scanItem_element,'Parameter',attrib=number_of_steps_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=scan_item)
            etree.SubElement(scanItem_element,'Parameter',attrib=type_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=maximum_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=minimum_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=log_attrib)
        elif self.kwargs.get('ScanType')=='0':
            etree.SubElement(scanItem_element,'Parameter',attrib=number_of_steps_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=type_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=scan_item)
        elif self.kwargs.get('ScanType')=='2':
            etree.SubElement(scanItem_element,'Parameter',attrib=number_of_steps_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=type_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=scan_item)
            etree.SubElement(scanItem_element,'Parameter',attrib=minimum_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=maximum_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=log_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=dist_type_attrib)

        query='//*[@name="ScanItems"]'
        for i in self.copasiML.xpath(query):
            i.append(scanItem_element)
        return self.copasiML


    def set_scan_options(self):
        report_attrib={'append': self.kwargs.get('Append'), 
                       'target': self.kwargs.get('ReportName'), 
                       'reference': self.get_report_key(),
                       'confirmOverwrite': self.kwargs.get('ConfirmOverwrite')}
                       
        subtask_attrib={'type': 'unsignedInteger', 'name': 'Subtask', 'value': self.kwargs.get('SubTask')}
        output_in_subtask_attrib={'type': 'bool', 'name': 'Output in subtask', 'value': self.kwargs.get('OutputInSubtask')}
        adjust_initial_conditions_attrib={'type': 'bool', 'name': 'Adjust initial conditions', 'value': self.kwargs.get('AdjustInitialConditions')}
        scheduled_attrib={'scheduled': self.kwargs.get('Scheduled'), 'updateModel': self.kwargs.get('UpdateModel')}
        
        R=etree.Element('Report',attrib=report_attrib)
        query='//*[@name="Scan"]'
        '''
        If scan task already has a report element defined, modify it, 
        otherwise create a new report element directly under the ScanTask 
        element
        '''
        scan_task= self.copasiML.xpath(query)[0]
        if scan_task[0].tag=='{http://www.copasi.org/static/schema}Problem':
            scan_task.insert(0,R)
        elif scan_task[0].tag=='{http://www.copasi.org/static/schema}Report':
            scan_task[0].attrib.update(report_attrib)
        for i in self.copasiML.xpath(query):
            i.attrib.update(scheduled_attrib)
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='Subtask':
                        k.attrib.update(subtask_attrib)
                    if k.attrib['name']=='Output in subtask':
                        k.attrib.update(output_in_subtask_attrib)
                    if k.attrib['name']=='Adjust initial conditions':
                        k.attrib.update(adjust_initial_conditions_attrib)
        return self.copasiML
        
    def remove_scans(self):
        query='//*[@name="ScanItems"]'
        for i in self.copasiML.xpath(query):
            for j in list(i):
                i.remove(j)
#            i.getparent().remove(i)
        return self.copasiML
        
    def run(self):
        R=Run(self.copasi_file,Task='scan',Mode=self.kwargs.get('Run'))
        
        if self.kwargs.get('Run')=='false':
            return None
        elif self.kwargs.get('Run')=='true':
            return R
        elif self.kwargs.get('Run')=='SGE':
            return R
#==============================================================================            
            
class Run():
    '''
    Run a copasi file using CopasiSE. Run will deactivate all tasks from 
    being executable via CopasiSE then activate the task you want to run, 
    then run it. 
    
    copasi_file:
        The copasi file you want to run 
    
    **kwargs:
    
        Task:
            Any valid copasi task. Default=time_course. Options are 
            ['steady_state','time_course','scan','fluxmode','optimization',
            'parameter_estimation','metaboliccontrolanalysis','lyapunovexponents',
            'timescaleseparationanalysis','sensitivities','moieties',
            'crosssection','linearnoiseapproximation']
            
        Save:
            Either 'false','duplicate' or 'overwrite'. Should probably remain 
            on 'overwrite', the default. 
            
        Mode:
            'true', 'false','multiprocess', or 'SGE'. Default is 'true' but can be turned off if you 
            want to uncheck all executable boxes then check the Task executable
            
        MaxTime:
            Default None. Max time in seconds for copasi to be allowed to run
    '''
    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=GetModelQuantities(self.copasi_file)
        self.SGE_job_file=os.path.splitext(self.copasi_file)[0]+'.sh'
        
        options={'Task':'time_course',
                 'Save':'overwrite',
                 'Mode':'true',
                 'MaxTime':None}
                                  
                 
                     
        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for Run'.format(i)
        options.update( kwargs) 
        self.kwargs=options    


        tasks=['steady_state','time_course',
               'scan','fluxmode','optimization',
               'parameter_estimation','metaboliccontrolanalysis',
               'lyapunovexponents','timescaleseparationanalysis',
               'sensitivities','moieties','crosssection',
               'linearnoiseapproximation']
                   
        
                  
        if  self.kwargs.get('Task') not in tasks:
            raise Errors.InputError('{} is not a valid task. Choose from {}'.format(self.kwargs.get('Task'),tasks))
        if self.kwargs.get('MaxTime')!=None:
            if isinstance(self.kwargs.get('MaxTime'),(float,int))!=True:
                raise TypeError('MaxTime argument must be float or int')
        
        if self.kwargs.get('Task')=='time_course':
            self.kwargs['Task']='timecourse'
            
        elif self.kwargs.get('Task')=='parameter_estimation':
            self.kwargs['Task']='parameterfitting'        
            
        elif self.kwargs.get('Task')=='steady_state':
            self.kwargs['Task']='steadystate'        
        
        
        self.copasiML=self.set_task()
        self.save()
        if self.kwargs.get('Mode')=='true':
            try:
                self.run()
            except Errors.CopasiError:
                self.run_linux()
        elif self.kwargs.get('Mode')=='SGE':
            self.submit_copasi_job_SGE()
        elif self.kwargs.get('Mode')=='multiprocess':
            self.multi_run()
            
            

    def multi_run(self):
        def run(x):
            subprocess.Popen('CopasiSE "{}"'.format(x))
        Process(run(self.copasi_file))
        
        

        
    def set_task(self):
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            i.attrib['scheduled']='false' #set all to false
            if self.kwargs.get('Task')== i.attrib['type'].lower():
                i.attrib['scheduled']='true'
                
        return self.copasiML
        
    def run(self):
        '''
        Process the copasi file using CopasiSE
        Must be Copasi version 16
        
        '''
        if self.kwargs.get('MaxTime')==None:
            args=['CopasiSE',"{}".format(self.copasi_file)]
        else:
            args=['CopasiSE','--maxTime',str(self.kwargs.get('MaxTime')),"{}".format(self.copasi_file)]
        p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        output,err= p.communicate()
        d={}
        d['output']=output
        d['error']=err
        if err!='':
            try:
                self.run_linux()
            except:
                raise Errors.CopasiError('Failed with Copasi error: \n\n'+d['error'])
        return d['output']
        
    def run_linux(self):
        os.system('CopasiSE "{}"'.format(self.copasi_file) )
            
        
    def submit_copasi_job_SGE(self):
        '''
        Submit copasi file as job to SGE based job scheduler. 
        '''
        with open(self.SGE_job_file,'w') as f:
            f.write('#!/bin/bash\n#$ -V -cwd\nmodule add apps/COPASI/4.16.104-Linux-64bit\nCopasiSE {}'.format(self.copasi_file))
        ## -N option for job name 
        os.system('qsub {} -N {} '.format(self.SGE_job_file,self.SGE_job_file))
        ## remove .sh file after used. 
        os.remove(self.SGE_job_file)
    
        
    def save(self):
        if self.kwargs.get('Save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('Save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML        


#==============================================================================
        
class InsertParameters():
    '''
    Insert parameters from a file, dictionary or a pandas dataframe into a copasi
    file. 
    
    Positional Arguments:
    
        copasi_file:
            The copasi file you want to enter parameters into
    
    **Kwargs
        Index:
            Index of parameter estimation run to input into the copasi file. 
            The index is ordered by rank of best fit, with 0 being the best.
            Default=0            
            
        QuantityType:
            Either 'particle_number' or 'concentration'. Default='concentration'
            
        ReportName;
            Unused. Delete?
            
        OutputML:
            If Save set to 'duplicate', this is the duplicate filename
            
        Save:
            either 'false','overwrite' or 'duplicate',default=overwrite
                
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
        
    '''
    def __init__(self,copasi_file,**kwargs):
        '''
        coapsi_file = file you want to insert
        kwargs:
            Index: If not specified default to -1
                    can be int or list of ints
        '''
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=GetModelQuantities(self.copasi_file)

        default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_PE_results.txt'
        default_outputML=os.path.split(self.copasi_file)[1][:-4]+'_Duplicate.cps'
        options={#report variables
                 'Metabolites':self.GMQ.get_metabolites().keys(),
                 'GlobalQuantities':self.GMQ.get_global_quantities().keys(),
                 'QuantityType':'concentration',
                 'ReportName':default_report_name,
                 'OutputML':default_outputML,
                 'Save':'overwrite',
                 'Index':0,
                 'ParameterDict':None,
                 'DF':None,
                 'ParameterPath':None,
                 
                 }
                     
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for InsertParameters'.format(i)
        options.update( kwargs) 
        self.kwargs=options
        
#        assert os.path.exists(self.parameter_path),'{} doesn\'t exist'.format(self.parameter_path)
        assert self.kwargs.get('QuantityType') in ['concentration','particle_numbers']
        if self.kwargs.get('ParameterDict') != None:
            if isinstance(self.kwargs.get('ParameterDict'),dict)!=True:
                raise Errors.InputError('Argument to \'ParameterDict\' keyword needs to be of type dict')
            for i in self.kwargs.get('ParameterDict').keys():
                if i not in self.GMQ.get_all_model_variables().keys():
                    raise Errors.InputError('Parameter \'{}\' is not in your model. \n\nThese are in your model:\n{}'.format(i,sorted(self.GMQ.get_all_model_variables().keys())))
                
        if self.kwargs.get('ParameterDict')==None and self.kwargs.get('ParameterPath')==None and self.kwargs.get('DF') is None:
            raise Errors.InputError('You need to give at least one of ParameterDict,ParameterPath or DF keyword arguments')
        
        assert isinstance(self.kwargs.get('Index'),int)
                
            
        #make sure user gives the right number of arguments
        num=0
        if self.kwargs.get('ParameterDict')!=None:
            num+=1
        if self.kwargs.get('DF') is not None:
            num+=1
        if self.kwargs.get('ParameterPath')!=None:
            num+=1
        if num!=1:
            raise Errors.InputError('You need to supply exactly one of ParameterDict,ParameterPath or df keyord argument. You cannot give two or three.')
        
#        self.check_parameter_consistancy()
        self.parameters=self.get_parameters()   
        self.parameters= self.replace_gl_and_lt()
        self.insert_all()
        #change

    def save(self):
        if self.kwargs.get('Save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('Save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML


    def check_parameter_consistancy_deprecated(self):
        '''
        raise an error if no parameters in the PE header match 
        parameters in model
        '''
        model_parameter_names= set(self.GMQ.get_all_model_variables().keys())
        input_parameter_names= set(list(self.get_parameters().keys()))
        intersection=list( model_parameter_names.intersection(input_parameter_names))
        if intersection==[]:
            raise Errors.InputError('''The parameters in your parameter estimation data are not in your model.\
Please check the headers of your PE data are consistent with your model parameter names.''' )
            
    def check_parameter_consistancy(self,df):
        '''
        raise an error if no parameters in the PE header match 
        parameters in model
        
        args:
            df:
                containing parameters to compare with parameters
                in the model
        '''
        model_parameter_names= set(self.GMQ.get_all_model_variables().keys())
        input_parameter_names= set(list(df.keys()))
        intersection=list( model_parameter_names.intersection(input_parameter_names))
        if intersection==[]:
            raise Errors.InputError('''The parameters in your parameter estimation data are not in your model.\
Please check the headers of your PE data are consistent with your model parameter names.''' )            
            
    def get_parameters(self):
        '''
        Get parameters depending on the type of input. 
        Converge on a pandas dataframe. 
        Columns = parameters, rows = parameter sets
        
        Use check parameter consistency to see
        whether headers have been pruned or not. If not try pruning them
        '''
        if self.kwargs.get('ParameterDict')!=None:
            assert isinstance(self.kwargs.get('ParameterDict'),dict),'The ParameterDict argument takes a Python dictionary'
            for i in self.kwargs.get('ParameterDict'):
                assert i in self.GMQ.get_all_model_variables().keys(),'{} is not a parameter. These are your parameters:{}'.format(i,self.GMQ.get_all_model_variables().keys())
            return pandas.DataFrame(self.kwargs.get('ParameterDict'),index=[0])
        
        if self.kwargs.get('ParameterPath')!=None:
            PED=PEAnalysis.ParsePEData(self.kwargs.get('ParameterPath'))
            if isinstance(self.kwargs.get('Index'),int):
                return pandas.DataFrame(PED.data.iloc[self.kwargs.get('Index')]).transpose()
            else: 
                return PED.data.iloc[self.kwargs.get('Index')]
        if self.kwargs.get('DF') is not None:
            df= pandas.DataFrame(self.kwargs.get('DF').iloc[self.kwargs.get('Index')]).transpose()
        try:
            self.check_parameter_consistancy(df)
        except Errors.InputError:
            df=PruneCopasiHeaders(df).prune()
            self.check_parameter_consistancy(df)
        return df

    def insert_locals(self):
        '''
        
        '''
        #first isolate the local parameters 
        local=self.GMQ.get_local_kinetic_parameters_cns().keys()
        for i in local:
            query='//*[@cn="{}"]'.format( self.GMQ.get_local_kinetic_parameters_cns()[i]['cn'])
            for j in self.copasiML.xpath( query):
                if i in self.parameters.keys():
                    j.attrib['value']=str(float(self.parameters[i]))
        return self.copasiML
                    
    def insert_global(self):
        glob= self.GMQ.get_global_quantities_cns().keys()
        for i in glob:
            query='//*[@cn="{}"]'.format( self.GMQ.get_global_quantities_cns()[i]['cn'])
            for j in self.copasiML.xpath(query):
                if i in self.parameters.keys() and j.attrib['simulationType']!='assignment':
                    j.attrib['value']=str(float(self.parameters[i]))
        return self.copasiML

    def insert_ICs(self):
        IC=self.GMQ.get_IC_cns()
        for i in IC:
            query='//*[@cn="{}"]'.format( self.GMQ.get_IC_cns()[i]['cn'])
            for j in self.copasiML.xpath(query):
                if i in self.parameters.keys() and j.attrib['simulationType']=='reactions':
                    if self.kwargs.get('QuantityType')=='concentration':
                        particles=self.GMQ.convert_molar_to_particles(float(self.parameters[i]),self.GMQ.get_quantity_units(),float(IC[i]['compartment_volume']))#,self.GMQ.get_volume_unit())
##                        particles=self.parameters[i]
                    elif self.kwargs.get('QuantityType')=='particle_numbers':
                        particles=self.parameters[i]
                    j.attrib['value']=str(float(particles))
        return self.copasiML



    def insert_fit_items(self):
        '''
        insert parameters into fit items
        '''
        copasiML=self.copasiML
        query="//*[@name='OptimizationItemList']"
        ICs_and_global=None
        reaction=None
        parameter=None
        for i in copasiML.xpath(query):
            for j in list(i):
                for k in list(j):
                    if k.attrib['name']=='ObjectCN':
                        pattern1='Vector=(?!Reactions).*\[(.*)\]'#match global and IC parameters but not local
                        search1= re.findall(pattern1,k.attrib['value'])
                        
                        if search1 !=[]:
                            ICs_and_global=search1[0]
                    if k.attrib['name']=='StartValue':
                        if ICs_and_global !=None:
                            if ICs_and_global in self.parameters.keys():
                                k.attrib['value']=str(float(self.parameters[ICs_and_global]))
                    #now again for local parameters
                    if k.attrib['name']=='ObjectCN':
                        pattern2='Vector=Reactions\[(.*)\].*Parameter=(.*),'
                        search2= re.findall(pattern2,k.attrib['value'])

                        if search2!=[]:
                            reaction,parameter= search2[0]
                            local= '({}).{}'.format(reaction,parameter)
                    if k.attrib['name']=='StartValue':
                        if reaction != None and parameter !=None:
                            if local in self.parameters.keys():
                                k.attrib['value']=str(float(self.parameters[local]))
                            else:
                                continue
        return self.copasiML
        
    def get_current_parameters_deprecated(self):
        '''
        Deprecated. Just use self.GMQ.get_all_model_variables()
        '''
        return self.GMQ.get_all_model_variables()
        


    def replace_gl_and_lt(self):
        '''
        replace greater than and less than symbols for XML purposes
        '''
        l=[]
        for i in self.parameters.keys():
            i= i.replace('<','\<')
            i=i.replace('>','\>')
            l.append(i)
        self.parameters.columns=pandas.Index(l)
        return self.parameters
            
        
    def insert_all(self):
        self.copasiML=self.insert_locals()
#        self.save() 
        self.copasiML=self.insert_global()
#        self.save()
        self.copasiML=self.insert_ICs()
#        self.save()
        self.copasiML=self.insert_fit_items()
        self.save()
#        os.chdir(os.path.dirname(self.copasi_file))
               
#==============================================================================
class PruneCopasiHeaders():
    '''
    COPASI uses references to distinguish model components (like InitialConcentration 
    or InitialParticleNumber). These are printed to file with copasi results and
    its therefore useful to have a way to remove these references, leaving only the 
    model component as it is in the model. 
    
    Args:
        for_pruning: either a full path to the file you want to prune or 
        a pandas dataframe
    
    kwargs:
        replace:
            'true' or 'false', if 'true' will overwrite the filename. If 'false'
            write new file to new_path. If for_pruning a dataframe this argument is
            ignored. 
            
        new_path: 
            When replace='false 'new_path' is the output filename. Ignored when 
            for_pruning is a pandas dataframe.
        

    '''
    def __init__(self,for_pruning,replace='false',new_path=None):
        self.for_pruning=for_pruning
        self.replace=replace
        
#        assert self.mode in ['singlePE','multiPE,'time_course']
        
        if replace not in ['true','false']:
            raise Errors.InputError('\'replace\' keyword should be either \'true\' or \'false\' ')

            
        self.from_file=False
        self.from_df=False
        if isinstance(self.for_pruning,str) and os.path.isfile(self.for_pruning):
            self.from_file=True
        elif isinstance(for_pruning,pandas.core.frame.DataFrame):
            self.from_df=True
                
        if self.from_file:
            if new_path==None:
                self.new_path= os.path.splitext(self.for_pruning)[0]+'_pruned_titles.txt'
            else:
                self.new_path=new_path
        
#        if self.mode=='time_course':
        if self.from_file:
            self.new_path=self.prune()
        elif self.from_df:
            self.df=self.prune()
    
    
    def prune(self):
        '''
        
        '''
        
        '''
        for time course we're using index but for PE were not. Need to make this consistant!
        '''
        if self.from_file==True:
            df=pandas.DataFrame.from_csv(self.for_pruning,sep='\t',index_col=None)
        elif self.from_df==True:
            df=self.for_pruning
        l=list( df.keys())
        new_titles=[] 
        for j in l:
            #match anything between two square brackets with regex
            match= re.findall('.*\[(.*)\]',j)
            #we need the residual sum of squares value to be called 'RSS'
            #and everything else to be an exact match to the corresponding
            #model element
            if match==[]:
                new_titles.append(j)
            elif match[0]=='Parameter Estimation':
                new_titles.append('RSS')
            else:
                new_titles.append(match[0])
        assert len(df.columns)==len(new_titles)
        df.columns=new_titles
        if self.from_file:
            if self.replace=='true':
                os.remove(self.for_pruning)
                self.new_path=self.for_pruning
            df.to_csv(self.new_path,sep='\t',index=False)
            return self.new_path
        elif self.from_df:
            return df
        
class RunMultiplePEs():
    '''
    
    '''
    def __init__(self,copasi_file,experiment_files,**kwargs):
        self.copasi_file=copasi_file
        self.experiment_files=experiment_files
        self.GMQ=GetModelQuantities(self.copasi_file)
        
        if os.path.isfile(self.copasi_file)!=True:
            raise Errors.InputError('{} doesn\'t exist'.format(self.copasi_file))
        LOG.debug('Performing multi parameter fit for model at:\n{}'.format(self.copasi_file))
        
        ## Pickle file to store directories of sub copasi files
        self.copasi_file_pickle=os.path.join(os.path.dirname(self.copasi_file),'sub_copasi_file.pickle')
        options={'Run':'multiprocess',
                 'OutputDir':None,
                 'CopyNumber':1,
                 'NumberOfPEs':3,
                 'ReportName':None,
                 'Metabolites':self.GMQ.get_metabolites().keys(),
                 'GlobalQuantities':self.GMQ.get_global_quantities().keys(),
                 'LocalParameters': self.GMQ.get_local_kinetic_parameters_cns().keys(),
                 'QuantityType':'concentration',
                 'Append': 'false', 
                 'SetReport':'true',
                 'ConfirmOverwrite': 'false',
                 'ConfigFilename':None,
                 'OverwriteConfigFile':'false',
                 'PruneHeaders':'true',
                 'UpdateModel':'false',
                 'RandomizeStartValues':'true',
                 'CreateParameterSets':'false',
                 'CalculateStatistics':'false',
                 'UseTemplateStartValues':'false',
                 #method options
                 'Method':'GeneticAlgorithm',
                 #'DifferentialEvolution',
                 'NumberOfGenerations':200,
                 'PopulationSize':50,
                 'RandomNumberGenerator':1,
                 'Seed':0,
                 'Pf':0.475,
                 'IterationLimit':50,
                 'Tolerance':0.00001,
                 'Rho':0.2,
                 'Scale':10,
                 'SwarmSize':50,
                 'StdDeviation':0.000001,
                 'NumberOfIterations':100000,
                 'StartTemperature':1,
                 'CoolingFactor':0.85,
                 #experiment definition options
                 #need to include options for defining multiple experimental files at once
                 'RowOrientation':['true']*len(self.experiment_files),
                 'ExperimentType':['timecourse']*len(self.experiment_files),
                 'FirstRow':[str(1)]*len(self.experiment_files),
                 'NormalizeWeightsPerExperiment':['true']*len(self.experiment_files),
                 'RowContainingNames':[str(1)]*len(self.experiment_files),
                 'Separator':['\t']*len(self.experiment_files),
                 'WeightMethod':['mean_squared']*len(self.experiment_files),
                 'Save':'overwrite',  
                 'Scheduled':'false',
                 'Verbose':'false',
                 'LowerBound':0.000001,
                 'UpperBound':1000000,
#                 'Run':'false',
                 'Plot':'false',
                 '''
                 The below arguments get passed to the parameter
                 estimation plotting class
                 '''
                 
                 'LineWidth':4,
                 #graph features
                 'FontSize':22,
                 'AxisSize':15,
                 'ExtraTitle':None,
                 'LineWidth':3,
                 'Show':'false',
                 'SaveFig':'false',
                 'TitleWrapSize':30,
                 'Ylimit':None,
                 'Xlimit':None,
                 'DPI':125,
                 'XTickRotation':35,
                 'DotSize':4,
                 'LegendLoc':'best'}
                 
                 
                 
        
        for key in kwargs.keys():
            if key not in options.keys():
                raise Errors.InputError('{} is not a keyword argument for RunMutliplePEs'.format(key))
        options.update( kwargs) 
        self.kwargs=options           
        self._do_checks()
        self._create_defaults()
        self._create_output_directory()
        
#        dire,fle=os.path.split(self.kwargs['ReportName']) ## for making sub-result directories
#        self.output_dir=os.path.join(dire,'MultiplePEResults')

#        self.PE_dct={'ReportName':self.kwargs['ReportName'],
#                     'Plot':self.kwargs['Plot'],
#                     'RandomizeStartValues':self.kwargs['RandomizeStartValues'],
#                     'ConfigFilename':self.kwargs['ConfigFilename'],
#                     'NumberOfGenerations':self.kwargs['NumberOfGenerations'],
#                     'RandomNumberGenerator':self.kwargs['RandomNumberGenerator'],
#                     'Seed':self.kwargs['Seed'],
#                     'Pf':self.kwargs['Pf'],
#                     'IterationLimit':self.kwargs['IterationLimit'],
#                     'Tolerance':self.kwargs['Tolerance'],
#                     'Rho':self.kwargs['Rho'],
#                     'Scale':self.kwargs['Scale'],
#                     'SwarmSize':self.kwargs['SwarmSize'],
#                     'StdDeviation':self.kwargs['StdDeviation'],
#                     'NumberOfIterations':self.kwargs['NumberOfIterations'],
#                     'StartTemperature':self.kwargs['StartTemperature'],
#                     'CoolingFactor':self.kwargs['CoolingFactor'],
#                     'PopulationSize':self.kwargs['PopulationSize'],
#                     'Method':self.kwargs['Method'] }
        self.PE_dct=deepcopy(self.kwargs)
        del self.PE_dct['OutputDir']
        del self.PE_dct['CopyNumber']
        del self.PE_dct['NumberOfPEs']
        del self.PE_dct['Run']
        
        
        self.report_files=self.enumerate_PE_output()
        LOG.debug('Create an instance of ParameterEstimation')
        self.PE=ParameterEstimation(self.copasi_file,self.experiment_files,**self.PE_dct)
        
        
    def set_up(self):
        '''
        Analogous to the set_up method of the ParameterEstimation class but this time
        setup both the PE and Scan tasks       
        '''

        self.PE.set_up()
        self.sub_copasi_files=self.copy_copasi()
        self._setup_scan()
    
#        if os.path.isfile(self.config_filename)!=True:
#            self.PE.write_item_template()
#        LOG.debug('calling the set_up method of the ParameterEstimation class')
 
    def run(self):
        '''
        If Run=mutliprocess:
        '''
        ##load cps from pickle in case run not being use straignt after set_up
        if self.kwargs['Run']=='SGE':
            try:
                check_call('qhost')
            except Errors.NotImplementedError:
                LOG.warning('Attempting to run in SGE mode but SGE specific commands are unavailable. Switching to \'multiprocess\' mode')
                self.kwargs['Run']='multiprocess'
        if os.path.isfile(self.copasi_file_pickle):
            with open(self.copasi_file_pickle) as f:
                self.sub_copasi_files=pickle.load(f)
        for i in self.sub_copasi_files:
            LOG.info('Running model: {}'.format(i))
            if self.kwargs['Run']=='multiprocess':
                Run(self.sub_copasi_files[i],Mode='multiprocess',Task='scan')
            elif self.kwargs['Run']=='SGE':
                Run(self.sub_copasi_files[i],Mode='SGE',Task='scan')
                    
                
            
    def write_config_template(self):
        '''
        
        '''
        LOG.info('writing PE config template for model: {}'.format(self.copasi_file))
        LOG.debug('ConfigFilename is {}'.format(self.PE.kwargs['ConfigFilename']))
        self.PE.write_item_template()
        
        
    def _setup_scan2(self):
        '''
        Set up n repeat items with NumberOfSteps repeats of parameter estimation
        Set run to false as we want to use the multiprocess mode of the Run class
        to process all m files at once in CopasiSE
        
        Remember scan needs iterating over because each file needs an unique report
        name
        '''
        import time
        for num in range(self.kwargs['CopyNumber']):
            LOG.info('setting up scan for model number {}'.format(num))
            start=time.time()
            Scan(self.sub_copasi_files[num],
                 ScanType='repeat', #set up repeat item under scan. 
                 NumberOfSteps=self.kwargs['NumberOfPEs'], #Run the parameter estimation task 3 times
                 SubTask='parameter_estimation', #this is the default, but included here for demonstration anyway
                 ReportType='parameter_estimation', ## report automatically set up within copasi. 
                 ReportName=self.report_files[num],
                 Run='false') #run the scan task automatically in the background
            LOG.info('Setup Took {} seconds'.format(time.time() - start))    
        
    ##void    
    def _setup_scan(self):
        '''
        Set up n repeat items with NumberOfSteps repeats of parameter estimation
        Set run to false as we want to use the multiprocess mode of the Run class
        to process all m files at once in CopasiSE
        
        Remember scan needs iterating over because each file needs an unique report
        name
        '''

        q=Queue.Queue()
        for num in range(self.kwargs['CopyNumber']):
            LOG.info('setting up scan for model : {}'.format(self.sub_copasi_files[num]))
            t=threading.Thread(target=self._setup1scan,
                               args =  (q,self.sub_copasi_files[num] , self.report_files[num])  )
            t.daemon=True
            t.start()
            time.sleep(0.1)
            
        s=q.get()
        LOG.info(str(s))

            
    ## void
    def _setup1scan(self,q,cps,report):
        '''
        
        '''
#        LOG.info('setting up scan for model number {}'.format(num))
        start=time.time()
        q.put(Scan(cps,
             ScanType='repeat', #set up repeat item under scan. 
             NumberOfSteps=self.kwargs['NumberOfPEs'], #Run the parameter estimation task 3 times
             SubTask='parameter_estimation', #this is the default, but included here for demonstration anyway
             ReportType='parameter_estimation', ## report automatically set up within copasi. 
             ReportName=report,
             Run='false') )#run the scan task automatically in the background
        LOG.info('Setup Took {} seconds'.format(time.time() - start))      
        
        
    ##void
    def _create_defaults(self):
        '''
        
        '''
        default_report_name=os.path.join(os.path.dirname(self.copasi_file),'ParameterFit.txt')
        if self.kwargs['ReportName']==None:
            LOG.debug('Using default report name:\n{}'.format(default_report_name))
            self.kwargs['ReportName']=default_report_name
                       
        output_dir_default=os.path.join(os.path.dirname(self.copasi_file),'MultiplePEResults')
        if self.kwargs['OutputDir']==None:
            LOG.debug('Using default OutputDir:\n{}'.format(output_dir_default))
            self.kwargs['OutputDir']=output_dir_default        
                       
        if self.kwargs['ConfigFilename']==None:
            LOG.debug('ConfigFilename is None. Reassigning ConfigFilename')
            self.kwargs['ConfigFilename']=os.path.join(os.path.dirname(self.copasi_file),'PEConfigFile.xlsx')
        
        if self.kwargs['ConfigFilename']!=None:
            if os.path.isabs(self.kwargs['ConfigFilename'])==False:
                self.kwargs['ConfigFilename']=os.path.join(os.path.dirname(self.copasi_file),self.kwargs['ConfigFilename'])
                
                       

    
    ##void             
    def _do_checks(self):
        '''
        
        '''
        run_arg_list=['multiprocess','SGE']
        if self.kwargs['Run'] not in run_arg_list:
            raise Errors.InputError('Run needs to be one of {}'.format(run_arg_list))
        if isinstance(self.kwargs['CopyNumber'],int)!=True:
            raise Errors.InputError('CopyNumber argument is of type int')
            
        if isinstance(self.kwargs['NumberOfPEs'],int)!=True:
            raise Errors.InputError('NumberOfPEs argument is of type int')    
            
        if self.kwargs['OutputDir']==None:
            self.kwargs['OutputDir']='MultipleParameterEsimationAnalysis'
        self.kwargs['OutputDir']=os.path.abspath(self.kwargs['OutputDir'])
            
    
    def copy_copasi(self):
        '''
        Copy copasi files m times to run separetly on a single 
        computer
        
        returns:
            dict[model_number]=cps_file
        '''
        LOG.info('Copying copasi file {} times'.format(self.kwargs['CopyNumber']))
        sub_copasi_files_dct={}
        copasi_path,copasi_filename=os.path.split(self.copasi_file)
        for i in range(self.kwargs['CopyNumber']):
            new_cps=os.path.join(copasi_path,copasi_filename[:-4]+'{}.cps'.format(str(i)))
            shutil.copy(self.copasi_file,new_cps)
            sub_copasi_files_dct[i]= new_cps
        
        with open(self.copasi_file_pickle,'w')as f:
            pickle.dump(sub_copasi_files_dct,f)
            
        return sub_copasi_files_dct
    
    def _create_output_directory(self):
        '''
        
        '''
        LOG.info('creating a directory for analysis in : \n\n{}'.format(self.kwargs['OutputDir']))
        if os.path.isdir(self.kwargs['OutputDir'])!=True:
            os.mkdir(self.kwargs['OutputDir'])
                
            
    
    def enumerate_PE_output(self):
        '''
        Create a filename for each file to collect PE results
        
        Returns:
            dct['model_copy_number]=enumerated_report_name
        '''
        LOG.debug('Enumerating PE report files')
        dct={}
        dire,fle=os.path.split(self.kwargs['ReportName'])
        for i in range(self.kwargs['CopyNumber']):
            new_file=os.path.join(self.kwargs['OutputDir'],
                                  fle[:-4]+'{}.txt'.format(str(i)))
            dct[i]=new_file
        return dct
    


class MultiModelFit():
    '''
    Take a project directory containing all copasi files
    and data files that you want to fit simultaneously and 
    

    '''
    def __init__(self,project_config,outdir,**kwargs):
        self.outdir=outdir
        self.project_dir=project_config
#        self.config_filename=config_filename
        self.do_checks()
        self.cps_files,self.exp_files=self.read_fit_config()
        
#        if self.config_filename==None:
#            self.config_filename=os.path.join(self.project_dir,'PEConfigFile.xlsx')
        
        options={'Run':'multiprocess',
                 'CopyNumber':1,
                 'NumberOfPEs':3,
                 'ReportName':None,
                 'OutputDir':None,
                 ##default parameters for ParameterEstimation
                 'Method':'GeneticAlgorithm',
                 'Plot':'false',
                 'QuantityType':'concentration',
                 'Append': 'false', 
                 'SetReport':'true',
                 'ConfirmOverwrite': 'false',
                 'ConfigFilename':'PEConfigFile.xlsx',
                 'OverwriteConfigFile':'false',
                 'PruneHeaders':'true',
                 'UpdateModel':'false',
                 'RandomizeStartValues':'true',
                 'CreateParameterSets':'false',
                 'CalculateStatistics':'false',
                 'UseTemplateStartValues':'false',
                 #method options
                 'Method':'GeneticAlgorithm',
                 #'DifferentialEvolution',
                 'NumberOfGenerations':200,
                 'PopulationSize':50,
                 'RandomNumberGenerator':1,
                 'Seed':0,
                 'Pf':0.475,
                 'IterationLimit':50,
                 'Tolerance':0.0001,
                 'Rho':0.2,
                 'Scale':10,
                 'SwarmSize':50,
                 'StdDeviation':0.000001,
                 'NumberOfIterations':100000,
                 'StartTemperature':1,
                 'CoolingFactor':0.85,
                 #experiment definition options
                 #need to include options for defining multiple experimental files at once
                 'RowOrientation':['true']*len(self.exp_files),
                 'ExperimentType':['timecourse']*len(self.exp_files),
                 'FirstRow':[str(1)]*len(self.exp_files),
                 'NormalizeWeightsPerExperiment':['true']*len(self.exp_files),
                 'RowContainingNames':[str(1)]*len(self.exp_files),
                 'Separator':['\t']*len(self.exp_files),
                 'WeightMethod':['mean_squared']*len(self.exp_files),
                 'Save':'overwrite',  
                 'Scheduled':'false',
                 'Verbose':'false',
                 'LowerBound':0.000001,
                 'UpperBound':1000000,
#                 'Run':'false',
                 'Plot':'false'}
        
        for key in kwargs.keys():
            if key not in options.keys():
                raise Errors.InputError('{} is not a keyword argument for MultiModelFit'.format(key))
        options.update( kwargs) 
        self.kwargs=options    
        
        
        
        self.sub_cps_dirs=self.create_workspace()
        self.RMPE_dct=self.instantiate_run_multi_PEs_class()
        self.results_folder_dct=self.get_output_directories()
        
    def instantiate_run_multi_PEs_class(self):
        '''
        pass correct arguments to the RunMultiplePEs class in order
        to instantiate a RunMultiplePEs instance for each model. 
        
        Reutrns:
            dict[model_filename]=RunMultiplePEs_instance
        '''
        LOG.debug('instantiating an instance of RunMultiplePEs for each model')
        dct={}
#        run_multiple_pes_kwargs=self.kwargs
#        del run_multiple_pes_kwargs['Method']
#        if self.kwargs['ConfigFilename']==None:
#            self.kwargs['ConfigFilename']='PEConfigFile.xlsx'
            
        for cps_dir in self.sub_cps_dirs:
            os.chdir(cps_dir)
            if os.path.isabs(self.kwargs['ConfigFilename']):
                self.kwargs['ConfigFilename']=os.path.split(self.kwargs['ConfigFilename'])[1]
#            LOG.debug('ConfigFilename is {}'.format(self.kwargs['ConfigFilename']))
#            self.kwargs['ConfigFilename']=os.path.join(cps_dir,self.kwargs['ConfigFilename'])
#            LOG.debug('config filename after modification is: {}'.format(self.kwargs['ConfigFilename']))
            dct[self.sub_cps_dirs[cps_dir]]=RunMultiplePEs(self.sub_cps_dirs[cps_dir],
                                                           self.exp_files,**self.kwargs)
            
        LOG.debug('Each instance of RunMultiplePEs is being held in a dct:\n{}'.format(dct))
        return dct

    def get_output_directories(self):
        '''
        Returns the location of the parameter estimation output files
        produced from the analysis. 
        '''
        LOG.debug('getting output directories')
        output_dct={}
        for RMPE in self.RMPE_dct:
            LOG.debug('output directory for model \n{}:'.format(RMPE))
            LOG.debug('\t\t'+self.RMPE_dct[RMPE].kwargs['OutputDir'])
            output_dct[RMPE]=self.RMPE_dct[RMPE].kwargs['OutputDir']
        return output_dct
    
    #void
    def write_config_template(self):
        '''
        A class to write a config file template for each 
        model in the analysis. Calls the corresponding
        write_config_template from the RunMultiplePEs class
        '''
        for RMPE in self.RMPE_dct:
            self.RMPE_dct[RMPE].write_config_template()
            
        
    def set_up(self):
        '''
        A user interface class which calls the corresponding
        method (set_up) from the RunMultiplePEs class per model. 
        Perform the ParameterEstimation.set_up() method on each model. 
        
        '''
        for RMPE in self.RMPE_dct:
            self.RMPE_dct[RMPE].set_up()


    def run(self):
        '''
        A user interface class which calls the corresponding
        method (run) from the RunMultiplePEs class per model. 
        Perform the ParameterEstimation.run() method on each model. 
        '''
        for RMPE in self.RMPE_dct:
            self.RMPE_dct[RMPE].run()
        

    def do_checks(self):
        '''
        Function to check the integrity of the input given by user
        '''
        pass
    
        
    def create_workspace(self):
        '''
        Creates a workspace from cps and experiment files in self.project_dir
        
        i.e. 
            --project_dir
            ----model1_dir
            ------model1.cps
            ------exp_data.txt
            ----model2_dir
            ------model2.cps
            ------exp_data.txt
        
        returns:
            Dictionary[cps_filename]=DirectoryForCpsAnalysis
        '''
        LOG.info('Creating workspace from project_dir')
        LOG.debug('Creating Workspace from files in: \n{}'.format(self.project_dir))
        ## Create entire working directory for analysis
        self.wd=os.path.join(self.project_dir,self.outdir)
        
        LOG.debug('New Working directory is:\n{}'.format(self.wd))
        if os.path.isdir(self.wd)!=True:
            LOG.debug('{} doesn\' already exist. Creating {}'.format(self.wd,self.wd))
            os.mkdir(self.wd)
        os.chdir(self.project_dir)
        LOG.debug('changing directory to project_dir: \n({}) to read relevent .cps and exp files'.format(self.wd))
        LOG.debug('Creating a directory in working directory for each of the model files')
        
        cps_dirs={}
        
        for cps in self.cps_files:
            cps_abs=os.path.abspath(cps)
            cps_filename=os.path.split(cps_abs)[1]
            sub_cps_dir=os.path.join(self.wd,cps_filename[:-4])
            if os.path.isdir(sub_cps_dir)!=True:
                os.mkdir(sub_cps_dir)
            sub_cps_abs=os.path.join(sub_cps_dir,cps_filename)
            shutil.copy(cps_abs,sub_cps_abs)
            if os.path.isfile(sub_cps_abs)!=True:
                raise Exception ('Error in copying copasi file to sub directories')
            cps_dirs[sub_cps_dir]=sub_cps_abs
        LOG.info('Workspace created')
        return cps_dirs
#                

    def read_fit_config(self):
        '''
        The recommed way to use this class: 
            Put all .cps files you want to fit in a folder with meaningful names (pref with no spaces)
            Put all data files for fitting in the same folder. 
                Make sure all data files have left most column as Time (with consistent units)
                and all other columns corresponding exactly (no trailing white spaces) to model variables. 
                Any independent variables should have the '_indep' suffix
        This function will read this multifit config and produce a directory tree for subsequent analysis
        '''
        LOG.debug('Reading fit configuration')
        if self.project_dir==None:
            raise Errors.InputError('Cannot read multifit confuration as no Project kwarg is provided')
        ##make sure we're in the right directory
        os.chdir(self.project_dir)
        cps_list=[]
        LOG.debug('These are the cps files in your fit config:')
        for cps_file in glob.glob('*.cps'):
            LOG.debug('''{}'''.format(cps_file))
            cps_list.append(cps_file)
            
        LOG.debug('These are the experiment files in your fit config:')
        exp_list=[]
        exp_file_types=('*.csv','*.txt')
        for typ in exp_file_types:
            for exp_file in glob.glob(typ):
                LOG.debug('''{}'''.format(exp_file))
                exp_list.append(os.path.abspath(exp_file))
                
        if cps_list==[]:
            raise Errors.InputError('No cps files in your project')
        if exp_list==[]:
            raise Errors.InputError('No experiment files in your project')
        return cps_list,exp_list
        
        
        
#==============================================================================

            
        
            
if __name__=='__main__':
    class FilePaths():
        def __init__(self):
            self.dire=r'/home/b3053674/Documents/Models/MinimalTGFbetaModel/Fit3'
    #        self.dire='/sharedlustre/users/a8021862/Ciaran/MinimalTGFbetaModel/Fit2'
            self.copasi_file=os.path.join(self.dire,'M3.cps')
            self.data_file=os.path.join(self.dire,'FittingData.csv')
            self.pSmad3_data_file=os.path.join(self.dire,'pSmad3data.csv')
            self.PEData=os.path.join(self.dire,'MultipleParameterEsimationAnalysis')
            self.parameter_file=os.path.join(self.dire,'MultipleParameterEsimationAnalysis/Fit30.txt')
        
    F=FilePaths()
    #
    config=r'M3.ConfigFile.xlsx'
    
#    PE=pycopi.ParameterEstimation(F.copasi_file,[F.data_file,F.pSmad3_data_file],
#                                         Method='CurrentSolutionStatistics',
#                                         RandomizeStartValues='false',
#                                         Plot='true',
#                                         )
#    PE.set_up()
#    PE.run()


#    G=pycopi.GetModelQuantities(F.copasi_file)
#    for i in G.get_all_model_variables():
#        print i,G.get_all_model_variables()[i]['value']
#    I=pycopi.InsertParameters(F.copasi_file,ParameterPath=F.parameter_file,Index=0)
#    print I.parameters
    

#    TC=TimeCourse(F.copasi_file,End=50,StepSize=1,Intervals=50,
#                         ReportName=os.path.join(F.dire,'TimeCourseReport.txt'),
#                         Plot='true')
#    for i in dir(TC):
#        print i
#        
#        
#        
#    for i in TC.data:
#        plt.figure()
#        plt.plot(TC.data['Time'],TC.data[i])
#        
        
#    PlotPEData(F.copasi_file,[F.data_file,F.pSmad3_data_file],
#               F.parameter_file,Plot='true')
    





























