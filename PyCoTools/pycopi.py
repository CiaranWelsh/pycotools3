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
import PEAnalysis,Errors, Misc, _base
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


class CopasiMLParser():

    """
    Parse a copasi file into xml.etree.
    The copasiML is availbale as the copasiML attribute.

    args:
        copasi_file:
            A full path to a copasi file


    """
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
            
    def _parse_copasiML(self):
        '''
        Parse xml doc with lxml 
        '''
        tree= etree.parse(self.copasi_file)
        return tree

    def write_copasi_file(self,copasi_filename, copasiML):
        '''
        write to file with lxml write function
        '''
        #first convert the copasiML to a root element tree
        root=etree.ElementTree(copasiML)
        root.write(copasi_filename)
        LOG.debug('model written to {}'.format(copasi_filename))




#==============================================================================
class Model():
    """
    This class is the replacement for GetModelQuantities. Currently supporting
    'getters' for model quantities. There is space for the 'setters' but this 
    is not implemented yet. 
    """
    def __init__(self, copasi_file):
        self.copasi_file = copasi_file
        self.copasiML = CopasiMLParser(self.copasi_file).copasiML
        
        
    def get_time_unit(self):
        """
        
        """
        
        query =  '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.copasiML.xpath(query)[0].attrib['timeUnit']    
    
    def get_model_name(self):
        """
        
        """
        query =  '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.copasiML.xpath(query)[0].attrib['name']            

    def get_volume_unit(self):
        query =  '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.copasiML.xpath(query)[0].attrib['volumeUnit']
    
    def get_quantity_unit(self):
        query =  '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.copasiML.xpath(query)[0].attrib['quantityUnit']  
    
    def get_area_unit(self):
        query =  '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.copasiML.xpath(query)[0].attrib['areaUnit']  
    
    def get_length_unit(self):
        query =  '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.copasiML.xpath(query)[0].attrib['lengthUnit']  
    
    def get_avagadro(self):
        query =  '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return float(self.copasiML.xpath(query)[0].attrib['avogadroConstant'] ) 
    
    
    def get_model_key(self):
        """
        Get the model reference - the 'key' from self.get_model_units
        """
        query =  '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.copasiML.xpath(query)[0].attrib['key']  
    
    def get_compartments(self):
        """
        Get dict of compartments. dict[compartment_name] = corresponding xml code as nested dict
        """
        collection= {}
        for i in self.copasiML.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfCompartments':
                df_list = []
                for j in i:
                    values = j.attrib.values()
                    df_list.append(pandas.DataFrame(values, index=['ID','Name','SimulationType','Value']).transpose()  )
        df = pandas.concat(df_list)
        df = df.set_index('Name')
        df['Value'] = [int(i) for i in df['Value']]
        return df
#                    if attribute==None:
#                    collection[j.attrib['key']] = pandas.DataFrame(j.attrib)
#                    print collection
#                    print pandas.DataFrame(collection)

                    
#                    else:
#                        collection[j.attrib['key']] = j.attrib[attribute]
#        return collection
    
        
    def get_global_quantities(self):
        """

        ===returns===
        pandas.DataFrame containing name, value, key and reference
        for global variables.
        """

        def get_global_quantities_key2name_mapping():
            """
            Get the model reference - the 'key' from self.get_model_units
            """
            collection = {}
            for i in self.copasiML.iter():
                if i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                    for j in i:
                            collection[j.attrib['key']] = j.attrib['name']
            return collection

        # print get_global_quantities_key2name_mapping()

        print self.get_initial_state_global_quantities()
       # collection= {}
       #
       #Dont take conc or from here
       # for i in self.copasiML.iter():
       #     if  i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
       #         for j in i:
       #              collection[j.attrib['key']] = j.attrib
       # return collection
    
    

    def get_local_parameters(self):
        """
        Get local parameters from the model. 
        
        ====returns===
        DataFrame containing name, value, key and reference for 
        local parmeters
        """
        def get_local_parameter_reference_df():
            
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
                            d[match]=k.attrib['cn']

            reference_df = pandas.DataFrame(d, index=['Reference']).transpose()
            return reference_df
        
        reference_df = get_local_parameter_reference_df()
        
        collection = {}
        for i in self.copasiML.iter() :
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                reaction_name = i.getparent().attrib['name']
                for j in i:
                    collection[j.attrib['key']] = (reaction_name, j.attrib['name'], float(j.attrib['value']) )                    
        df = pandas.DataFrame(collection, index=['Reaction','Parameter', 'Value']).transpose()
        
        reaction_parameter_name = []
        for i in range(df.shape[0]):
            reaction_parameter_name .append('({}).{}'.format(df['Reaction'].iloc[i], df['Parameter'].iloc[i])  )
        df.index.name='ParameterKey'
        df['ReactionParameterID'] = reaction_parameter_name
        df = df.reset_index()
        df = df.set_index('ReactionParameterID')
        
        '''
        Here I've chosen to merge the reference and df frames using
        'inner' because this way it seems to filter out the local
        parmeters which are assigned to global variables. Using how='outer'
        will return all parameters instead. 
        '''
        return  df.merge(reference_df, left_index=True, right_index=True, how='inner')
    
#    def get_reactions(self, attribute=None):
#        """
#        
#        """
#        key_list = [None,'key', 'name', 'reversible', 'fast']
#        if attribute not in key_list:
#            raise Errors.InputError('{} not in {}'.format(attribute, key_list))
#            
#        collection={}
#        for i in self.copasiML.iter():
#            if i.tag=='{http://www.copasi.org/static/schema}ListOfReactions':
#                for j in i:
#                    if attribute == None:
#                        collection[j.attrib['key']] = j.attrib
#                    else:
#                        collection[j.attribute['key']] = j.attrib[attribute]
#        return collection
#    
#    def get_state_template(self):
#        """
#
#        """
#        collection= []
#        for i in self.copasiML.iter():
#            if  i.tag == '{http://www.copasi.org/static/schema}StateTemplate':
#                for j in i:
#                    collection.append(j.attrib['objectReference'])
#        return collection     

    def get_state_template(self):
        """
        Get states (metabolites and globals) in the order they are read by Copasi
        from the StateTemplate element.
        
        ===Returns===
        list. 
        """
        collection= []
        for i in self.copasiML.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}StateTemplate':
                for j in i:
                    collection.append(j.attrib['objectReference'])
        return collection   
    
    def get_metabolites(self):
        '''

        '''
            
        def get_metabolites_key2name_mapping():
            """
                Get the model reference - the 'key' from self.get_model_units7
                Only needed by get_metabolites() so hide scope from outer class
            """
            collection= {}
            for i in self.copasiML.iter():
                if  i.tag == '{http://www.copasi.org/static/schema}ListOfMetabolites':
                    for j in i:
                        collection[j.attrib['key']] = j.attrib['name']
            return collection

        def get_reference():
            """
            Get copasi references for transient metabolite quantities.
            These are strings begining with cn in the xml
            :return:
            pandas.DataFrame
            """

            query='//*[@cn="String=Initial Species Values"]'
            d={}
            for i in self.copasiML.xpath(query):
                for j in list(i):
                    match= re.findall('Metabolites\[(.*)\]', j.attrib['cn'])[0]
                    assert isinstance(match.encode('utf8'),str),'{} is not a string but a {}'.format(match,type(match))
                    assert match is not  None
                    assert match !=[]
                    d[match]=j.attrib['cn']
            return d #pandas.DataFrame(d, index=[0]).transpose()

        metab_dct={}
        query='//*[@cn="String=Initial Species Values"]'
        for i in self.copasiML.xpath(query):
            for j in list(i):
                match=re.findall('.*Vector=Metabolites\[(.*)\]',j.attrib['cn'])
                if match==[]:
                    return self.copasiML
                else:
                    
                    comp=re.findall('Compartments\[(.*?)\]',j.attrib['cn'])[0]
                    compartment_vol = self.get_compartments().loc[comp]['Value']
                    metab_dct[match[0]]={}
                    metab_dct[match[0]][comp]={}

        if len(metab_dct.keys())==0:
            raise Errors.NometabolitesError('There are no metabolites in {}'.format(self.get_model_name()))
        query = '//*[@type="initialState"]'
        for i in self.copasiML.xpath(query):
            state_values = i.text
        state_values = state_values.strip()
        state_values = state_values.split(' ')
        state_values = [ i for i in state_values if i not in ['',' ','\n','\t']]
        mapping =  get_metabolites_key2name_mapping()
        dct = dict(zip(self.get_state_template(), state_values))
        particle_numbers = {j:dct[i] for (i,j) in mapping.items() if i in dct.keys()}

        part = []
        conc = []
        ref = []
        m = []
        c = []
        for metab in metab_dct:
            m.append(metab)
            for comp in metab_dct[metab]:
                c.append(comp)
                part.append(float(particle_numbers[metab]) )

                conc.append(Misc.convert_particles_to_molar(float(particle_numbers[metab]),
                                                      self.get_quantity_unit(),
                                                      self.get_compartments().loc[comp]['Value'])  )
                ref.append(get_reference()[metab]  )

        df = pandas.DataFrame([m,c, part, conc, ref],
                               index=['Metabolite', 'Compartment',
                                      'Particles', 'Concentration',
                                      'Reference']).transpose()
        return df.set_index('Metabolite')

    def get_initial_state_global_quantities(self):
        query = '//*[@type="initialState"]'
        for i in self.copasiML.xpath(query):
            state_values = i.text
        state_values = state_values.split(' ')
        mapping =  self.get_global_quantities_key2name_mapping()
        dct = dict(zip(self.get_state_template(), state_values))
        return {j:dct[i] for (i,j) in mapping.items() if i in dct.keys()}



class GetModelQuantities():
    '''
    Positional arguments:
        copasi_file:
            Full path to copasi file
            
            
    keywords:
        quantity_type:
            either 'concentration' (default) or 'particle_numbers'. 
    '''
    
    def __init__(self,copasi_file,quantity_type='concentration'):
        self.copasi_file=copasi_file
        self.quantity_type=quantity_type

        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML
                
#        self.all_params=self.get_global_quantities_cns().keys()+self.get_IC_cns().keys()+self.get_local_kinetic_parameters_cns().keys()
        assert self.quantity_type in ['concentration','particle_number']


    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]

    def __setitem__(self,key,value):
        self.kwargs[key] = value
        
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
        
    def get_model_units(self):
        '''
        get model reference
        '''
        query =  '//*[@timeUnit]' and '//*[@volumeUnit]' and '//*[@areaUnit]'
        return self.copasiML.xpath(query)[0].attrib
    
    def get_model_object_reference(self):
        """
        Get the model reference - the 'key' from self.get_model_units
        """
        return self.get_model_units()['key']
    
    def get_metabolites_object_reference(self):
        """
        Get the model reference - the 'key' from self.get_model_units
        """
        collection= {}
        for i in self.copasiML.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfMetabolites':
                for j in i:
                    collection[j.attrib['key']] = j.attrib['name']
        return collection

    def get_metabolites_key2name_mapping(self):
        """
        Get the model reference - the 'key' from self.get_model_units
        """
        collection= {}
        for i in self.copasiML.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfMetabolites':
                for j in i:
                    collection[j.attrib['key']] = j.attrib['name']
        return collection


    def get_global_object_reference(self):
        """
        Get the model reference - the 'key' from self.get_model_units
        """
        collection= {}
        for i in self.copasiML.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                for j in i:
                    collection[j.attrib['key']] = j.attrib['name']
        return collection
    
    def get_global_quantities_key2name_mapping(self):
        """
        Get the model reference - the 'key' from self.get_model_units
        """
        collection= {}
        for i in self.copasiML.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfModelValues':
                for j in i:
                    collection[j.attrib['key']] = j.attrib['name']
        return collection
    
    def get_compartment_object_reference(self):
        """
        Get the model reference - the 'key' from self.get_model_units
        """
        collection= {}
        for i in self.copasiML.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfCompartments':
                for j in i:
                    collection[j.attrib['key']] = j.attrib['name']
        return collection

    def get_list_of_constants(self):
        """
        Get the model reference - the 'key' from self.get_model_units
        """
        collection= {}
        for i in self.copasiML.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                for j in i:
                    collection[j.attrib['name']] = {}
                for j in i:
                    collection[j.attrib['name']][j.attrib['key']] = j.attrib['value']
        return collection    
    
    def get_reactions_object_reference(self):
        """
        
        """
        collection={}
        for i in self.copasiML.iter():
            if i.tag=='{http://www.copasi.org/static/schema}ListOfReactions':
                for j in i:
                    collection[j.attrib['name']] = j.attrib['key']
        return collection
            
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
                    if self.quantity_type=='concentration':
                        compartment_vol= float(self.get_compartments()[comp]['value'])
                    else:
                        compartment_vol=1
                    metab_dct[match[0]]={}
                    metab_dct[match[0]]['particle_numbers']=j.attrib['value']
                    concentration= self.convert_particles_to_molar(j.attrib['value'],self.get_quantity_units(),compartment_vol)
                    metab_dct[match[0]]['concentration']=concentration
                    metab_dct[match[0]]['compartment']=compartment_match[0]
        if len(metab_dct.keys())==0:
            raise Errors.NometabolitesError('There are no metabolites in {}'.format(self.get_model_name()))
        
        
        return metab_dct
    
    def get_initial_state_metabolites(self):
        query = '//*[@type="initialState"]'
        for i in self.copasiML.xpath(query):
            state_values = i.text
        state_values = state_values.split(' ')
        mapping =  self.get_metabolites_key2name_mapping()
        dct = dict(zip(self.get_state_template(), state_values))
        return {j:dct[i] for (i,j) in mapping.items() if i in dct.keys()}

    def get_initial_state_global_quantities(self):
        query = '//*[@type="initialState"]'
        for i in self.copasiML.xpath(query):
            state_values = i.text
        state_values = state_values.split(' ')
        mapping =  self.get_global_quantities_key2name_mapping()
        dct = dict(zip(self.get_state_template(), state_values))
        return {j:dct[i] for (i,j) in mapping.items() if i in dct.keys()}
    
    
    def get_metabolites2(self):
        '''
        Deprecated. Use get_ICs_cns() inst
        returns dict of metabolites in the 'species' menu
        '''
        metab_dct={}
        query='//*[@cn="String=Initial Species Values"]'
        for i in self.copasiML.xpath(query):
            print self.get_state_template()
#            for j in list(i):
#                match=re.findall('.*Vector=Metabolites\[(.*)\]',j.attrib['cn'])
#                                
#                if match==[]:
#                    return self.copasiML
#                else:
#                    compartment_match=re.findall('Compartments\[(.*)\],',j.attrib['cn'])
#                    
#                    comp=re.findall('Compartments\[(.*?)\]',j.attrib['cn'])[0]
#                    if self.quantity_type=='concentration':
#                        compartment_vol= float(self.get_compartments()[comp]['value'])
#                    else:
#                        compartment_vol=1
#                    metab_dct[match[0]]={}
#                    metab_dct[match[0]]['particle_numbers']=j.attrib['value']
#                    concentration= self.convert_particles_to_molar(j.attrib['value'],self.get_quantity_units(),compartment_vol)
#                    metab_dct[match[0]]['concentration']=concentration
#                    metab_dct[match[0]]['compartment']=compartment_match[0]
#        if len(metab_dct.keys())==0:
#            raise Errors.NometabolitesError('There are no metabolites in {}'.format(self.get_model_name()))
        return metab_dct
    
    def get_metabolites3(self, attribute=None):
        """

        """
        key_list = [None, 'key', 'name', 'simulationType', 'compartment']
        if attribute not in key_list:
            raise Errors.InputError('{} not in {}'.format(attribute, key_list))
        collection= {}
        for i in self.copasiML.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}ListOfMetabolites':
                for j in i:
                    if attribute==None:
                        collection[j.attrib['key']] = j.attrib
                    else:
                        collection[j.attrib['key']] = j.attrib[attribute]
        return collection     
        
    def get_state_template(self):
        """

        """
        collection= []
        for i in self.copasiML.iter():
            if  i.tag == '{http://www.copasi.org/static/schema}StateTemplate':
                for j in i:
                    collection.append(j.attrib['objectReference'])
        return collection        

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
                        
    def get_local_parameters_dep(self):
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

    def get_local_parameters(self):
        '''
        return dict of local parameters used in your model
        '''
        global_kinetic_parameters = self.get_global_kinetic_parameters_cns().keys()
#        query='//*[@cn="String=Kinetic Parameters"]'
        query = 'Reaction'
        parameters={}
        count=0
        for i in self.copasiML.iter():
            if i.tag == '{http://www.copasi.org/static/schema}Constant':
#                print i.getparent().getparent().attrib
                reaction_name = i.getparent().getparent().attrib['name']
                parameter_name = i.attrib['name']
                key2 = "({}).{}".format(reaction_name, parameter_name)
                if key2 in global_kinetic_parameters:
                    continue
                parameters[key2] = {}
                parameters[key2] = float(i.attrib['value'])
                count+=1
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
        metab=a single metabolite dict from the get_IC_cns method
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
                if self.quantity_type=='concentration':
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
    
    def get_fit_item_order(self):
        '''
        return all parameters that are present in the fit items of the
        parameter estimation task
        '''
        lst =[]
        query='//*[@name="FitItem"]'
        for i in self.copasiML.xpath(query):
            for j in list(i):
                if j.attrib['name']=='ObjectCN':
                    match=re.findall('Reference=(.*)',j.attrib['value'])[0]
                    if match=='Value':
                        match2=re.findall('Reactions\[(.*)\].*Parameter=(.*),', j.attrib['value'])[0]
                        match2='({}).{}'.format(match2[0],match2[1])
                        lst.append(match2)
                    elif match=='InitialValue':
                        match2=re.findall('Values\[(.*)\]', j.attrib['value'])[0]
                        lst.append(match2)
                    elif match=='InitialConcentration':
                        match2=re.findall('Metabolites\[(.*)\]',j.attrib['value'])[0]
                        lst.append(match2)
        return lst

    def get_all_model_variables(self):
        '''
        concatonate the output of the three functions that give model variables
        Return list
        '''
        g= self.get_global_quantities_cns()
        l=self.get_local_kinetic_parameters_cns()
        p= dict(l,**g)
        p=dict(p,**self.get_IC_cns())
        p=dict(p,**self.get_compartments())
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
        


#==============================================================================

class Reports():
    '''
    Creates reports in copasi output specification section. 
    Use: 
        -the report_type kwarg to specify which type of report you want to make
        -the metabolites and global_quantities kwargs to specify which parameters
        to include
        
    
    
    args:
        copasi_file:
            The copasi file you want to add a report too
        
    **kwargs:

        report_type: 
            Which report to write. Options:
                profilelikleihood:
                    - for Pydentify, shouldn't need to manually touch this
                time_course:
                    -a table of time Vs concentrations. Included values are specified to the metabolites and//or global_quantities arguments
            parameter_estimation:
                    -a table of values from a parameter estimation and the residual sum of squares value for each run. 

    
        metabolites:
            A list of valid model metabolites you want to include in the report. Default=All metabolites
        
        global_quantities;
            List of valid global quantities that you want to include in the report. Default=All global variables
        
        quantity_type:
            Either 'concentration' or 'particle_number'. Switch between having report output in either concentration of in particle_numbers. 

        report_name:
            Name of the report. Default depends on kwarg report_type
        
        append: 
            True or False. append to report. Default False
        
        confirm_overwrite: 
            True or False.  Default= False
        
        save: 
            either False,'overwrite' or 'duplicate'. 
            false: don't write to file
            overwrite: overwrite copasi_file
            duplicate: write a new file named using the kwarg OutputML

            
        variable:
            When report_type is profilelikelihood, theta is the parameter of interest
    
    '''
    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=GetModelQuantities(self.copasi_file)
        
#        default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_PE_results.txt'
        options={#report variables
                 'metabolites':self.GMQ.get_IC_cns().keys(),
                 'global_quantities':self.GMQ.get_global_quantities().keys(),
                 'local_parameters':self.GMQ.get_local_kinetic_parameters_cns(),
                 'quantity_type':'concentration',
                 'report_name':None,
                 'append': False, 
                 'confirm_overwrite': False,
                 'separator':'\t',
                 #
                 'save':'overwrite',
                 'update_model':False,
                 'report_type':'parameter_estimation',
                 'variable':self.GMQ.get_IC_cns().keys()[0], #only for profile_likelihood
        
                 }
                     
        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for Reports'.format(i)
        options.update( kwargs) 
        self.kwargs=options
        
        if isinstance(self.kwargs.get('metabolites'),str):
            self.kwargs['metabolites']=[self.kwargs.get('metabolites')]

        if isinstance(self.kwargs.get('global_quantities'),str):
            self.kwargs['global_quantities']=[self.kwargs.get('global_quantities')]

        if isinstance(self.kwargs.get('local_parameters'),str):
            self.kwargs['local_parameters']=[self.kwargs.get('local_parameters')]


        if self.kwargs['append']==True:
            self.kwargs['append']=str(1)
        else:
            self.kwargs['append']=str(0)
            
        if self.kwargs['confirm_overwrite']==True:
            self.kwargs['confirm_overwrite']=str(1)
        else:
            self.kwargs['confirm_overwrite']=str(0)
                 
                 
        self.report_types=[None,'profilelikelihood', 'profilelikelihood2',
                           'time_course','parameter_estimation', 'multi_parameter_estimation']
        assert self.kwargs.get('report_type') in self.report_types,'valid report types include {}'.format(self.report_types)
        
        write_to_file_list=['duplicate','overwrite',False]
        assert self.kwargs.get('save') in write_to_file_list     
        
        quantity_types=['particle_numbers','concentration']
        assert self.kwargs.get('quantity_type') in quantity_types
        
        if self.kwargs.get('variable')!=None:
            assert self.kwargs.get('variable') in self.GMQ.get_all_model_variables().keys(),'{} not in {}'.format(self.kwargs.get('variable'),self.GMQ.get_all_model_variables().keys())
        
        if self.kwargs.get('report_name')==None:
            if self.kwargs.get('report_type')=='profilelikelihood':
                default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_profilelikelihood.txt'
            elif self.kwargs.get('report_type')=='profilelikelihood2':
                default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_profilelikelihood2.txt'

            elif self.kwargs.get('report_type')=='time_course':
                default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_time_course.txt'
            elif self.kwargs.get('report_type')=='parameter_estimation':
                default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_parameter_estimation.txt'
            elif self['report_type'] == 'multi_parameter_estimation':
                default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_multi_parameter_estimation.txt'
            self.kwargs.update({'report_name':default_report_name})

        self.kwargs = Bool2Str(self.kwargs).convert_dct()

        self.copasiML=self.clear_all_reports()
        self.copasiML=self.run()
        
            
        self.copasiML=self.save()
        
        


    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]

    def __setitem__(self,key,value):
        self.kwargs[key] = value
        
    def save(self):
        self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML
        
    def save_dep(self):
        if self.kwargs.get('save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML
        
    def timecourse(self):
        '''
        creates a report to collect time course results. 
        
        By default all species and all global quantities are used with 
        Time on the left most column. This behavior can be overwritten by passing
        lists of metabolites to the metabolites keyword or global quantities to the
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
        if self.kwargs.get('metabolites')!=None:
            for i in self.kwargs.get('metabolites'):
                if self.kwargs.get('quantity_type')=='concentration':
                    cn= self.GMQ.get_IC_cns()[i]['cn']+',Reference=Concentration'
                elif self.kwargs.get('quantity_type')=='particle_numbers':
                    cn= self.GMQ.get_IC_cns()[i]['cn']+',Reference=ParticleNumber'
            #add to xml
                Object=etree.SubElement(table,'Object')
                Object.attrib['cn']=cn

        #for global quantities 
        if self.kwargs.get('global_quantities')!=None:
            for i in self.kwargs.get('global_quantities'):
                cn= self.GMQ.get_global_quantities_cns()[i]['cn']+',Reference=Value'
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
        if self.kwargs.get('variable') in self.kwargs.get('metabolites'):
            cn= self.GMQ.get_IC_cns()[self.kwargs.get('variable')]['cn']+',Reference=InitialConcentration'#{}'.format(self.kwargs.get('quantity_type'))
        if self.kwargs.get('variable') in self.kwargs.get('global_quantities'):
            cn= self.GMQ.get_global_quantities_cns()[self.kwargs.get('variable')]['cn']+',Reference=InitialValue'#{}'.format(self.kwargs.get('quantity_type'))
        if self.kwargs.get('variable') in self.GMQ.get_local_kinetic_parameters_cns().keys():
            cn= self.GMQ.get_local_kinetic_parameters_cns()[self.kwargs.get('variable')]['cn']+',Reference=Value'#{}'.format(self.kwargs.get('quantity_type'))
        etree.SubElement(table,'Object',attrib={'cn':cn})
        etree.SubElement(table,'Object',attrib={'cn':"CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"})
        return self.copasiML
    
    
    def profile_likelihood2(self):
        '''
        Create report of a parameter and best value for a parameter estimation 
        for profile likelihoods
        '''
        #get existing report keys
        keys=[]
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name']=='profilelikelihood2':
                self.remove_report('profilelikelihood2')
        
        new_key='Report_31'
        while new_key in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))
        
        report_attributes={'precision': '6', 
                           'separator': '\t',
                           'name': 'profilelikelihood2',
                           'key':new_key, 
                           'taskType': 'Scan'}
        
        ListOfReports=self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)
        
        comment=etree.SubElement(report,'Comment') 
        table=etree.SubElement(report,'Table')
        table.attrib['printTitle']=str(1)
        if self.kwargs.get('variable') in self.kwargs.get('metabolites'):
            cn= self.GMQ.get_IC_cns()[self.kwargs.get('variable')]['cn']+',Reference=InitialConcentration'#{}'.format(self.kwargs.get('quantity_type'))
        if self.kwargs.get('variable') in self.kwargs.get('global_quantities'):
            cn= self.GMQ.get_global_quantities_cns()[self.kwargs.get('variable')]['cn']+',Reference=InitialValue'#{}'.format(self.kwargs.get('quantity_type'))
        if self.kwargs.get('variable') in self.GMQ.get_local_kinetic_parameters_cns().keys():
            cn= self.GMQ.get_local_kinetic_parameters_cns()[self.kwargs.get('variable')]['cn']+',Reference=Value'#{}'.format(self.kwargs.get('quantity_type'))
        etree.SubElement(table,'Object',attrib={'cn':cn})
        etree.SubElement(table,'Object',attrib={'cn':"CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"})
        etree.SubElement(table,'Object',attrib={'cn':"CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"})
        return self.copasiML
    
    

    def parameter_estimation_with_function_evaluations2(self):
        '''
        Define a parameter estimation report and include the progression
        of the parameter estimation (function evaluations).
        Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the global_quantities, LocalParameters and metabolites
        keywords.
        '''
        # get existing report keys
        keys = []
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])
            if i.attrib['name'] == 'parameter_estimation':
                self.copasiML = self.remove_report('parameter_estimation')

        new_key = 'Report_32'
        while new_key in keys:
            new_key = 'Report_{}'.format(numpy.random.randint(30, 100))
        report_attributes = {'precision': '6',
                             'separator': '\t',
                             'name': 'parameter_estimation',
                             'key': new_key,
                             'taskType': 'parameterFitting'}

        ListOfReports = self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports')
        report = etree.SubElement(ListOfReports, 'Report')
        report.attrib.update(report_attributes)
        comment = etree.SubElement(report, 'Comment')
        comment = comment  # get rid of annoying squiggly line above
        table = etree.SubElement(report, 'Table')
        table.attrib['printTitle'] = str(1)

        '''
        generate more SubElements dynamically
        '''
        # for metabolites
        if self.kwargs.get('metabolites') != None:
            for i in self.kwargs.get('metabolites'):
                assert i in self.GMQ.get_IC_cns().keys()
                if self.kwargs.get('quantity_type') == 'concentration':
                    cn = self.GMQ.get_IC_cns()[i]['cn'] + ',Reference=InitialConcentration'
                elif self.kwargs.get('quantity_type') == 'particle_numbers':
                    cn = self.GMQ.get_IC_cns()[i]['cn'] + ',Reference=InitialParticleNumber'
                    # add to xml
                Object = etree.SubElement(table, 'Object')
                Object.attrib['cn'] = cn

        # for global quantities
        if self.kwargs.get('global_quantities') != None:
            for i in self.kwargs.get('global_quantities'):
                cn = self.GMQ.get_global_quantities_cns()[i]['cn'] + ',Reference=InitialValue'
                # add to xml
                Object = etree.SubElement(table, 'Object')
                Object.attrib['cn'] = cn

        # for local quantities
        if self.kwargs.get('local_parameters') != None:
            for i in self.kwargs.get('local_parameters'):
                cn = self.GMQ.get_local_kinetic_parameters_cns()[i]['cn'] + ',Reference=Value'
                # add to xml
                Object = etree.SubElement(table, 'Object')
                Object.attrib['cn'] = cn

        Object = etree.SubElement(table, 'Object')
        Object.attrib[
            'cn'] = "CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"
        LOG.debug('Reports PE setup copasiML {}'.format(self.copasiML))

        return self.copasiML

    def set_parameter_estimation_report(self):
        '''
        Define a parameter estimation report and include the progression 
        of the parameter estimation (function evaluations).
        Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the global_quantities, LocalParameters and metabolites
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
                           'key': new_key,
                           'taskType': 'parameterFitting'}
        
        ListOfReports=self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)
        comment=etree.SubElement(report,'Comment') 
        footer=etree.SubElement(report,'Footer')
        Object=etree.SubElement(footer,'Object')
        Object.attrib['cn']="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"
        Object=etree.SubElement(footer,'Object')
        Object.attrib['cn']="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"
        LOG.debug('Reports PE setup copasiML {}'.format(self.copasiML))
        return self.copasiML     
    
    def set_multi_parameter_estimation_report(self):
        '''
        Define a parameter estimation report and include the progression 
        of the parameter estimation (function evaluations).
        Defaults to including all
        metabolites, global variables and local variables with the RSS best value
        These can be over-ridden with the global_quantities, LocalParameters and metabolites
        keywords. 
        '''
        #get existing report keys
        keys=[]
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            keys.append(i.attrib['key'])            
            if i.attrib['name']=='multi_parameter_estimation':
                self.copasiML=self.remove_report('multi_parameter_estimation')
        
        new_key='Report_32'
        while new_key  in keys:
            new_key='Report_{}'.format(numpy.random.randint(30,100))
        report_attributes={'precision': '6', 
                           'separator': '\t',
                           'name': 'multi_parameter_estimation',
                           'key': new_key,
                           'taskType': 'parameterFitting'}
        
        ListOfReports=self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports')
        report=etree.SubElement(ListOfReports,'Report')
        report.attrib.update(report_attributes)
        comment=etree.SubElement(report,'Comment') 
        table=etree.SubElement(report,'Table')
        table.attrib['printTitle']=str(1)
        etree.SubElement(table,'Object',attrib={'cn':"CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"})
        etree.SubElement(table,'Object',attrib={'cn':"CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"})
        return self.copasiML
    
    

    def run(self):
        '''
        Execute code that builds the report defined by the kwargs
        '''
        if self.kwargs.get('report_type')=='parameter_estimation':
            LOG.debug('created a \'parameter_estimation\' report')
            self.copasiML=self.set_parameter_estimation_report()        
            
        elif self['report_type']=='multi_parameter_estimation':
            LOG.debug('created a \'parameter_estimation\' report')
            self.copasiML=self.set_multi_parameter_estimation_report()
            
        elif self.kwargs.get('report_type')=='profilelikelihood':
            self.copasiML=self.profile_likelihood()
            LOG.debug('created a \'profile_likelihod\' type report')
            
        elif self.kwargs.get('report_type')=='profilelikelihood2':
            self.copasiML=self.profile_likelihood2()
            LOG.debug('created a \'profile_likelihod2\' type report')
            
        elif self.kwargs.get('report_type')=='time_course':
            self.copasiML=self.timecourse()
            LOG.debug('created a \'time_course\' type report')
            
        elif self.kwargs.get('report_type')==None:
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
        

class Bool2Str():
    """
    copasiML expects strings and we pythoners want to use python booleans not strings
    This class quickly converts between them
    """
    def __init__(self,dct):
        self.dct = dct
        if isinstance(self.dct,dict)!=True:
            raise Errors.InputError('Input must be dict')
        
        self.acceptable_kwargs = ['append','confirm_overwrite','update_model',
                                  'output_in_subtask','adjust_initial_conditions',
                                  'randomize_start_values','log10','scheduled','output_event']
    
    def convert(self,boolean):
        if boolean == True:
            return "true"
        elif boolean == False:
            return "false"
        else:
            raise Errors.InputError('Input should be boolean not {}'.format(isinstance(boolean)))
            
    def convert_dct(self):
        """
        
        ----
        return 
        """
        for kwarg in self.dct.keys():
            if kwarg in self.acceptable_kwargs:
                if self.dct[kwarg]==True:
                    self.dct.update({kwarg:"true"})
                else:
                    self.dct.update({kwarg:"false"})
#                
        return self.dct
            
    

class TimeCourse(object):
        '''
        run a time course using Copasi. Ensure, you specify the corrent amount
        of time you want simulating. Do this by ensuring that end=step_size*intervals.
        Set plot=True to automatically plot the results which can be found in a file
        in the same directory as your copasi file in a folder named after your report_name
        kwarg

        NOTE: Space has been left for addition of code to interface with the other
        copasi solvers. Currently only deterministic is supported.

        args:
            copasi_file - the copasi file you want to do a time course on


        **kwargs:
            For arguments related to plotting, see the documentation for plot

            intervals:
                How many intervals between start and end. Default=100

            step_size:
                How big each time increment is. Default='0.01',

            start:
                starting point of stimulation. Default=0.0

            end:
                The end point of the time course. Default=1.

            #integration options
            relative_tolerance:
                Default='1e-6',

            absolute_tolerance:
                Default='1e-12',

            max_internal_steps:
                Default='10000',

            update_model:
                Not really needed in time course. Do not change. Default=False

            metabolites:
                A list of which metabolites to include in output. Default=all

            global_quantities:
                A list of global quantities to include in the output. Default is all global quantities

            quantity_type:
                Either 'particle_numbers' or 'concentration',

            report_name:
                Name of the output report. Default is name of the copasi file with _TimeCourse appended'

            append:
                append to the report, True or False , default=False

            confirm_overwrite:
                Report confirm overwrite , True or False , default=False

            simulation_type:
                Either 'stochastic' or 'deterministic'. default='deterministic'. IMPORTANT: stochastic not yet implemented but there is room for it

            OutputEvent:
                Output event or not, default =False

            scheduled:
                True or False. Enables running the simulation by CopasiSE. Default=True,

            save:
                save the copasi file with the changes. Either False,'overwrite' or 'duplicate'

            prune_headers:
                Copasi automatically prints out copasi references to output files. Set
                this to True to  prune the references off leaving just the variable name,
                True or False, default=True

            #graph options
            plot:
                Whether to plot the graphs or not

            savefig:
                Whether to save the figures to file or not

            extra_title:
                If savefig=True,give the filename an extra identifier

            line_width:
                Passed to Matplotlib.pyplot.plot. Thickness of the line

            line_color:
                Passed to Matplotlib.pyplot.plot. color of the line

            marker_color:
                Passed to Matplotlib.pyplot.plot. color of the dots

            line_style:
                Passed to Matplotlib.pyplot.plot. Style of line

            marker_style:
                Passed to Matplotlib.pyplot.plot. Style of marker

            dpi:
                Passed to Matplotlib.pyplot.plot.

            xtick_rotation:
                Passed to Matplotlib.pyplot.plot. Rotate x labels

            title_wrap_size:
                Number of characters before word wrapping the title

        '''

        def __init__(self, copasi_file, **kwargs):
            self.copasi_file = copasi_file
            self.CParser = CopasiMLParser(self.copasi_file)
            self.copasiML = self.CParser.copasiML
            LOG.debug('CopasiML: {}'.format(self.copasiML))
            self.GMQ = GetModelQuantities(self.copasi_file)
            default_report_name = os.path.join(os.path.dirname(self.copasi_file),'{}_TimeCourse.txt'.format(os.path.split(self.copasi_file)[1][:-4]))
            options = {'intervals': '100',
                       'step_size': '0.01',
                       'end': '1',
                       'relative_tolerance': '1e-6',
                       'absolute_tolerance': '1e-12',
                       'max_internal_steps': '10000',
                       'start': '0.0',
                       'update_model': False,
                       # report variables
                       'metabolites': self.GMQ.get_IC_cns().keys(),
                       'global_quantities': self.GMQ.get_global_quantities().keys(),
                       'quantity_type': 'concentration',
                       'report_name': default_report_name,
                       'append': False,
                       #                 'target': 'cheese.txt',
                       'confirm_overwrite': False,
                       'simulation_type': 'deterministic',
                       'output_event': False,
                       'scheduled': True,
                       'save': 'overwrite',
                       'prune_headers': True,

                       # graph options
                       'plot': False,
                       'line_width': 2,
                       'line_color': 'k',
                       'marker_color': 'r',
                       'line_style': '-',
                       'marker_style': 'o',
                       'axis_size': 15,
                       'font_size': 22,
                       'xtick_rotation': 0,
                       'title_wrap_size': 35,
                       'savefig': False,
                       'extra_title': None,
                       'dpi': 125,
                       'marker_size': 5,
                       'graph_directory': None,
                       }
            # values need to be lower case for copasiML
            for i in kwargs.keys():
                assert i in options.keys(), '{} is not a keyword argument for TimeCourse'.format(i)
                #            kwargs[i]=str(kwargs[i]).lower()
                #            assert isinstance(kwargs[i],str),'all optional arguments passed shold be lower case strings'
            options.update(kwargs)
            
            self.kwargs = options

            '''
            if the below three kwargs are a single entry they can be a string. 
            In this case, put them back into a list to ensure a smooth ride
            '''
            if isinstance(self.kwargs.get('metabolites'), str):
                self.kwargs['metabolites'] = [self.kwargs.get('metabolites')]

            if isinstance(self.kwargs.get('global_quantities'), str):
                self.kwargs['global_quantities'] = [self.kwargs.get('global_quantities')]

            if isinstance(self.kwargs.get('local_parameters'), str):
                self.kwargs['local_parameters'] = [self.kwargs.get('local_parameters')]

            # Ensure consistecny for time variables
            assert float(self.kwargs.get('end')) == float(self.kwargs.get('step_size')) * float(self.kwargs.get(
                'intervals')), 'end should equal Interval Size times Number of intervals but {}!={}*{}'.format(
                self.kwargs.get('end'), self.kwargs.get('step_size'), self.kwargs.get('intervals'))

            # make sure metabolites and modelValues are lists
            if self.kwargs.get('metabolites') != None:
                assert isinstance(self.kwargs.get('metabolites'),
                                  list), 'Keyword argument metabolites should be a Python list'
                for i in self.kwargs.get('metabolites'):
                    assert i in self.GMQ.get_IC_cns().keys(), '{} is not a Metabolite in this model. These are metabolites in this model: {}'.format(
                        i, self.GMQ.get_IC_cns().keys())

            if self.kwargs.get('global_quantities') != None:
                assert isinstance(self.kwargs.get('global_quantities'),
                                  list), 'Keyword argument global_quantities should be a Python list'
                for i in self.kwargs.get('global_quantities'):
                    assert i in self.GMQ.get_global_quantities().keys(), '{} is not a global variable in this model. These are global variables in this model: {}'.format(
                        i, self.GMQ.get_global_quantities())

            # only accept deterministic or stochastic
            assert self.kwargs.get('simulation_type') in ['deterministic', 'stochastic']

            #

            # this bit of code helps keep the keyword arguments consistant
            assert self.kwargs.get('quantity_type').lower() in ['concentration', 'particle_number']

            # report arguments

            if self.kwargs.get('prune_headers') not in [True, False,'true','false']:
                raise Errors.InputError('prune_headers kwarg must be either \'true\' or \'false\'')

            if self.kwargs.get('append') not in [True, False,'true','false']:
                raise Errors.InputError('append kwarg must be either \'true\' or \'false\'')

            if self.kwargs.get('confirm_overwrite') not in [True, False,'true','false']:
                raise Errors.InputError('confirm_overwrite kwarg must be either \'true\' or \'false\'')

            if self.kwargs.get('output_event') not in [True, False,'true','false']:
                raise Errors.InputError('OutputEvent kwarg must be either \'true\' or \'false\'')

            if self.kwargs.get('scheduled') not in [True, False,'true','false']:
                raise Errors.InputError('scheduled kwarg must be either \'true\' or \'false\'')

            if self.kwargs.get('plot') not in [True, False,'true','false']:
                raise Errors.InputError('plot kwarg must be either \'true\' or \'false\'')

            self.kwargs['line_width'] = int(self.kwargs.get('line_width'))
            self.kwargs['axis_size'] = int(self.kwargs.get('axis_size'))
            self.kwargs['axis_size'] = int(self.kwargs.get('axis_size'))
            self.kwargs['xtick_rotation'] = int(self.kwargs.get('xtick_rotation'))
            self.kwargs['title_wrap_size'] = int(self.kwargs.get('title_wrap_size'))
            self.kwargs['dpi'] = int(self.kwargs.get('dpi'))

            if self.kwargs.get('append') == True:
                self.kwargs['append'] == str(1)
            else:
                self.kwargs['append'] == str(0)

            if self.kwargs.get('confirm_overwrite') == True:
                self.kwargs['confirm_overwrite'] == str(1)
            else:
                self.kwargs['confirm_overwrite'] == str(0)

            if self.kwargs.get('output_event') == True:
                self.kwargs['output_event'] == str(1)
            else:
                self.kwargs['output_event'] == str(0)

            if self.kwargs.get('scheduled') == True:
                self.kwargs['scheduled'] == str(1)
            else:
                self.kwargs['scheduled'] == str(0)

            assert self.kwargs.get('savefig') in [False, True]

            # convert some numeric kwargs to str
            self.kwargs = Bool2Str(self.kwargs).convert_dct()
            self.kwargs['intervals'] = str(self.kwargs.get('intervals'))
            self.kwargs['step_size'] = str(self.kwargs.get('step_size'))
            self.kwargs['end'] = str(self.kwargs.get('end'))
            self.kwargs['relative_tolerance'] = str(self.kwargs.get('relative_tolerance'))
            self.kwargs['absolute_tolerance'] = str(self.kwargs.get('absolute_tolerance'))
            self.kwargs['max_internal_steps'] = str(self.kwargs.get('max_internal_steps'))
            self.kwargs['start'] = str(self.kwargs.get('start'))

            if isinstance(self.kwargs.get('marker_size'), int):
                self.kwargs['marker_size'] = float(self.kwargs.get('marker_size'))

            assert isinstance(self.kwargs.get('marker_size'), float)

            assert self.kwargs.get('line_style') in ['-', '--', '-.', ':', 'None', ' ', '']
            assert isinstance(self.kwargs.get('line_width'), int), '{} is not int'.format(
                type(self.kwargs.get('line_width')))

            assert self.kwargs.get('marker_style') in ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd']

            color_dct = {'b': 'blue',
                         'g': 'green',
                         'r': 'red',
                         'c': 'cyan',
                         'm': 'magenta',
                         'y': 'yellow',
                         'k': 'black',
                         'w': 'white'}
            assert self.kwargs.get('line_color') in color_dct.keys() + color_dct.values()
            assert self.kwargs.get('marker_color') in color_dct.keys() + color_dct.values()

            self.report_options = {}  # report variables
            self.report_options['metabolites'] = self.kwargs.get('metabolites')
            self.report_options['global_quantities'] = self.kwargs.get('global_quantities')
            self.report_options['quantity_type'] = self.kwargs.get('quantity_type')
            self.report_options['report_name'] = self.kwargs.get('report_name')
            self.report_options['append'] = self.kwargs.get('append')
            self.report_options['confirm_overwrite'] = self.kwargs.get('confirm_overwrite')
            self.report_options['save'] = self.kwargs.get('save')
            self.report_options['update_model'] = self.kwargs.get('update_model')
            self.report_options['report_type'] = 'time_course'  # self.kwargs.get('report_type')

            # other keywords that are non optional for time course
            self.kwargs['report_type'] = 'time_course'
            matplotlib.rcParams.update({'font.size': self.kwargs.get('axis_size')})
            '''
            All methods required for time course are 
            called with run
            '''
            
            self.save()
            self.run()
            if self.kwargs['plot'] == True:
                self.data = self.read_sim_data()
                self.plot()

        def __getitem__(self,key):
            if key not in self.kwargs.keys():
                raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
            return self.kwargs[key]
    
        def __setitem__(self,key,value):
            self.kwargs[key] = value
        
        def _do_checks(self):
            """
            
            """
            

        def save(self):
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
            return self.copasiML

        def save_dep(self):
            if self.kwargs.get('save') == 'duplicate':
                self.CParser.write_copasi_file(self.kwargs.get('OutputML'), self.copasiML)
            elif self.kwargs.get('save') == 'overwrite':
                self.CParser.write_copasi_file(self.copasi_file, self.copasiML)
            return self.copasiML

        def set_deterministic(self):
            '''
            set parameters for deterministic timecourse
            '''
            query = "//*[@name='Time-Course']" and "//*[@type='timeCourse']"
            method_params = {'type': 'Deterministic(LSODA)', 'name': 'Deterministic (LSODA)'}
            for i in self.copasiML.xpath(query):
                # make available to coapsiSE
                i.attrib['scheduled'] = self.kwargs.get('scheduled')
                for j in list(i):
                    j.attrib['type'] = method_params['type']
                    j.attrib['name'] = method_params['name']
                    for k in list(j):
                        if k.attrib['name'] == 'Duration':
                            k.attrib['value'] = self.kwargs.get('end')

                        if k.attrib['name'] == 'StepNumber':
                            k.attrib['value'] = self.kwargs.get('intervals')

                        elif k.attrib['name'] == 'StepSize':
                            k.attrib['value'] = self.kwargs.get('step_size')

                        elif k.attrib['name'] == 'TimeSeriesRequested':
                            k.attrib['value'] = '1'

                        elif k.attrib['name'] == 'OutputStartTime':
                            k.attrib['value'] = self.kwargs.get('start')

                        elif k.attrib['name'] == 'Output Event':
                            k.attrib['value'] = self.kwargs.get('output_event')

                        elif k.attrib['name'] == 'Continue on Simultaneous Events':
                            k.attrib['value'] = '0'

                        elif k.attrib['name'] == 'Integrate Reduced Model':
                            k.attrib['value'] = '0'

                        elif k.attrib['name'] == 'Relative Tolerance':
                            k.attrib['value'] = self.kwargs.get('relative_tolerance')

                        elif k.attrib['name'] == 'Absolute Tolerance':
                            k.attrib['value'] = self.kwargs.get('absolute_tolerance')

                        elif k.attrib['name'] == 'MaxInternalSteps':
                            k.attrib['value'] = self.kwargs.get('max_internal_steps')
            return self.copasiML

        def report_definition(self):
            return Reports(self.copasi_file, **self.report_options).copasiML

        def get_report_key(self):
            '''
            cros reference the timecourse task with the newly created
            time course reort to get the key
            '''
            LOG.debug('getting report key')
            for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
                if i.attrib['name'] == 'Time-Course':
                    key = i.attrib['key']
            assert key != None, 'have you ran the report_definition method?'
            return key

        def set_report(self):
            '''
            Use the report defined in self.create_report to tell copasi
            were to put the results
            '''
            key = self.get_report_key()

            arg_dct = {'append': self.kwargs.get('append'),
                       'target': self.kwargs.get('report_name'),
                       'reference': key,
                       'confirmOverwrite': self.kwargs.get('confirm_overwrite')}
            query = "//*[@name='Time-Course']" and "//*[@type='timeCourse']"
            present = False
            #        query='//Report'
            for i in self.copasiML.xpath(query):
                for j in list(i):
                    if 'append' and 'target' in j.attrib.keys():
                        present = True
                        j.attrib.update(arg_dct)
                if present == False:
                    report = etree.Element('Report', attrib=arg_dct)
                    i.insert(0, report)
                    self.save()   #This save is needed in order to save the report befor euse
            return self.copasiML

        def run(self):
            '''
            run a time course. Use keyword argument:
                simulation_type='deterministic' #default
                SumulationType='stochastic' #still to be written
            '''
            if self.kwargs.get('simulation_type') == 'deterministic':
                self.copasiML = self.report_definition()
                self.copasiML = self.set_report()
                self.copasiML = self.set_deterministic()
                LOG.debug('setting up deterministic time course')
            elif self.kwargs.get('simulation_type') == 'stochastic':
                raise Errors.NotImplementedError('There is space in this class to write code to Run a stochastic simulation but it is not yet written')
##                
#            # save to duplicate copasi file
            self.save()
            R = Run(self.copasi_file, task='time_course')
            LOG.debug('Time course ran')
            return R

        def read_sim_data(self):
            data_output = os.path.join(os.path.dirname(self.copasi_file), self.kwargs['report_name'])
            # trim copasi style headers
            LOG.debug('Reading timecourse')
            if self.kwargs.get('prune_headers') == True:
                LOG.debug('pruning headers of copasi files of COPASI references')
                PruneCopasiHeaders(data_output, replace=True)
            return pandas.read_csv(data_output, sep='\t')

        def plot(self):
            '''

            '''
            LOG.debug('plotting time course')
            ## Create directory for graphs
            if self.kwargs['graph_directory'] == None:
                dire = os.path.join(os.path.dirname(self.copasi_file), 'TimeCourseGraphs')
                if os.path.isdir(dire) != True:
                    os.mkdir(dire)
                os.chdir(dire)

            for i in self.data:
                if i.lower() != 'time':
                    plt.figure()
                    ax = plt.subplot(111)
                    plt.plot(self.data['Time'], self.data[i],
                             linewidth=self.kwargs.get('line_width'), color=self.kwargs.get('line_color'),
                             linestyle=self.kwargs.get('line_style'), marker='o',
                             markerfacecolor=self.kwargs.get('marker_color'), markersize=self.kwargs.get('marker_size'))
                    #                plt.plot(self.data['Time'],self.data[i],color=self.kwargs.get('marker_color'),marker=self.kwargs.get('marker_style'))


                    # plot labels
                    plt.title('\n'.join(wrap('Time-Course for {}'.format(i), self.kwargs.get('title_wrap_size'))),
                              fontsize=self.kwargs.get('font_size'))
                    if self.kwargs.get('quantity_type') == 'concentration':
                        try:
                            plt.ylabel('Concentration ({})'.format(self.GMQ.get_quantity_units().encode('ascii')),
                                       fontsize=self.kwargs.get('font_size'))
                        except UnicodeEncodeError:
                            plt.ylabel('Concentration (micromol)', fontsize=self.kwargs.get('font_size'))
                    if self.kwargs.get('quantity_type') == 'particle_number':
                        plt.ylabel('Particle Numbers', fontsize=self.kwargs.get('font_size'))

                    plt.xlabel('Time ({})'.format(self.GMQ.get_time_unit()), fontsize=self.kwargs.get('font_size'))

                    # pretty stuff

                    ax.spines['right'].set_color('none')
                    ax.spines['top'].set_color('none')
                    ax.xaxis.set_ticks_position('bottom')
                    ax.yaxis.set_ticks_position('left')
                    ax.spines['left'].set_smart_bounds(True)
                    ax.spines['bottom'].set_smart_bounds(True)

                    # xtick rotation
                    plt.xticks(rotation=self.kwargs.get('xtick_rotation'))

                    # options for changing the plot axis
                    if self.kwargs.get('ylimit') != None:
                        ax.set_ylim(self.kwargs.get('ylimit'))
                    if self.kwargs.get('xlimit') != None:
                        ax.set_xlim(self.kwargs.get('xlimit'))

                    def save_plot():
                        def replace_non_ascii(st):
                            for j in st:
                                if j not in string.ascii_letters + string.digits + '_-[]':
                                    st = re.sub('\{}'.format(j), '__', st)
                            return st

                        filename = {}
                        name = replace_non_ascii(i)
                        filename[i] = os.path.join(dire, name + '.png')

                        if self.kwargs.get('extra_title') != None:
                            plt.savefig(name + '_' + self.kwargs.get('extra_title') + '.png', bbox_inches='tight',
                                        format='png', dpi=self.kwargs.get('dpi'))
                        else:
                            plt.savefig(filename[i], format='png', bbox_inches='tight', dpi=self.kwargs.get('dpi'))
                        return filename

                    if self.kwargs.get('show') == True:
                        plt.show()

                    # save figure options
                    if self.kwargs.get('savefig') == True:
                        os.chdir(os.path.dirname(self.copasi_file))
                        save_plot()


#==============================================================================            
class ExperimentMapper():
    '''
    Class to map variables from a parameter estimation item template which 
    is written using the ParameterEstimation.Write_item_template method, to model 
    variables. variable names must match exactly. You cannot have more than 
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
        row_orientation
        
        experiment_type
        
        first_row
        
        normalize_weights_per_experiment
        
        row_containing_names
        
        separator
        
        weight_method
        
        save
        

                 
    '''

    def __init__(self,copasi_file,experiment_files,**kwargs):
        self.copasi_file=copasi_file
        self.experiment_files=experiment_files
        if isinstance(self.experiment_files,str)==True:
            self.experiment_files = [self.experiment_files]
        assert isinstance(self.experiment_files,list)
        for i in self.experiment_files:
            assert os.path.isfile(i),'{} is not a real file'.format(i)
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=GetModelQuantities(self.copasi_file)

        options={    
                 'row_orientation':[True]*len(self.experiment_files),
                 'experiment_type':['timecourse']*len(self.experiment_files),
                 'first_row':[str(1)]*len(self.experiment_files),
                 'normalize_weights_per_experiment':[True]*len(self.experiment_files),
                 'row_containing_names':[str(1)]*len(self.experiment_files),
                 'separator':['\t']*len(self.experiment_files),
                 'weight_method':['mean_squared']*len(self.experiment_files) ,
                 'save':'overwrite'}
        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for TimeCourse'.format(i)
        options.update( kwargs) 
        self.kwargs=options

        weight_method_string = ['mean','mean_squared','stardard_deviation','value_scaling']
        weight_method_numbers = [str(i) for i in [1,2,3,4] ]
        weight_method_dict = dict(zip(weight_method_string, weight_method_numbers))
        self['weight_method'] = [weight_method_dict[i] for i in self['weight_method']  ]


        experiment_type_string = ['steadystate','timecourse']
        experiment_type_numbers = [str(i) for i in [0,1] ]
        experiment_type_dict = dict(zip(experiment_type_string, experiment_type_numbers))
        self['experiment_type'] = [experiment_type_dict[i] for i in self['experiment_type']]
                
        l=[]
        assert isinstance(self.kwargs.get('row_orientation'),list)
        for i in self.kwargs.get('row_orientation'):
            assert i in [True,False,'true','false']
            if i==True:
                l.append(str(1))
            else:
                l.append(str(0))
        self.kwargs['row_orientation']=l

        assert isinstance(self.kwargs.get('first_row'),list)
        l=[]
        for i in self.kwargs.get('first_row'):
            assert i!=0 
            assert i!=str(0)
            l.append(str(i))
        self.kwargs['first_row']=l
        
        l=[]
        assert isinstance(self.kwargs.get('normalize_weights_per_experiment'),list)
        for i in self.kwargs.get('normalize_weights_per_experiment'):
            assert i in [True,False,'true','false'],'{} should be true or false'.format(i)
            if i==True:
                l.append(str(1))
            else:
                l.append(str(0))
        self.kwargs['normalize_weights_per_experiment']=l

                
        l=[]
        assert isinstance(self.kwargs.get('row_orientation'),list)
        for i in self.kwargs['row_orientation']:
            l.append(str(i))
        self.kwargs['row_orientation']=l

        l=[]
        assert isinstance(self.kwargs.get('row_containing_names'),list)
        for i in self.kwargs['row_containing_names']:
            l.append(str(i))
        self.kwargs['row_containing_names']=l        


        assert isinstance(self.kwargs.get('separator'),list)
        for i in self.kwargs['separator']:
            assert isinstance(i,str),'separator should be given asa python list'
        
        assert self.kwargs.get('save') in [False,'duplicate','overwrite']
        
        self.kwargs = Bool2Str(self.kwargs).convert_dct()

        
        #run the experiment mapper        
        self.map_experiments()
        
        #save the copasi file
        if self.kwargs.get('save')!=False:
            self.save()
        
    def __getitem__(self, key):
        if key not in self.kwargs:
            raise Errors.InputError('{} not in {}'.format(key, self.kwargs))
        return self.kwargs[key]
    
    def __setitem__(self,key, value):
        self.kwargs[key] = value
        
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
        data=pandas.read_csv(self.experiment_files[index],sep=self.kwargs.get('separator')[index])
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
        
        #necessary xML attributes
        Exp=etree.Element('ParameterGroup',attrib={'name':self.key})
        
        row_orientation={'type': 'bool', 'name': 'Data is Row Oriented', 'value': self.kwargs.get('row_orientation')[index]}
        experiment_type={'type': 'unsignedInteger', 'name': 'Experiment Type', 'value': self.kwargs.get('experiment_type')[index]}
        ExpFile={'type': 'file', 'name': 'File Name', 'value': exp}
        first_row={'type': 'unsignedInteger', 'name': 'First Row', 'value': self.kwargs.get('first_row')[index]}
        Key={'type': 'key', 'name': 'Key', 'value': self.key}
        LastRow={'type': 'unsignedInteger', 'name': 'Last Row', 'value': str(int(num_rows)+1)} #add 1 to account for 0 indexed python 
        normalize_weights_per_experiment={'type': 'bool', 'name': 'Normalize Weights per Experiment', 'value': self.kwargs.get('normalize_weights_per_experiment')[index]}
        NumberOfColumns={'type': 'unsignedInteger', 'name': 'Number of Columns', 'value': num_columns}
        ObjectMap={'name': 'Object Map'}
        row_containing_names={'type': 'unsignedInteger', 'name': 'Row containing Names', 'value': self.kwargs.get('row_containing_names')[index]}
        separator={'type': 'string', 'name': 'separator', 'value': self.kwargs.get('separator')[index]}
        weight_method={'type': 'unsignedInteger', 'name': 'Weight Method', 'value': self['weight_method'][index]}

        etree.SubElement(Exp,'Parameter',attrib=row_orientation)
        etree.SubElement(Exp,'Parameter',attrib=experiment_type)
        etree.SubElement(Exp,'Parameter',attrib=ExpFile)
        etree.SubElement(Exp,'Parameter',attrib=first_row)
        etree.SubElement(Exp,'Parameter',attrib=Key)
        etree.SubElement(Exp,'Parameter',attrib=LastRow)
        etree.SubElement(Exp,'Parameter',attrib=normalize_weights_per_experiment)
        etree.SubElement(Exp,'Parameter',attrib=NumberOfColumns)
        Map=etree.SubElement(Exp,'ParameterGroup',attrib=ObjectMap)
        etree.SubElement(Exp,'Parameter',attrib=row_containing_names)
        etree.SubElement(Exp,'Parameter',attrib=separator)
        etree.SubElement(Exp,'Parameter',attrib=weight_method)
        
        #get handle to the cn's
        ICs= self.GMQ.get_IC_cns()
        glob= self.GMQ.get_global_quantities_cns()
        loc=self.GMQ.get_local_kinetic_parameters_cns()
        
        #define object role attributes
        TimeRole={'type': 'unsignedInteger', 'name': 'Role', 'value': '3'}
        DepentantvariableRole={'type': 'unsignedInteger', 'name': 'Role', 'value': '2'}
        IndepentantvariableRole={'type': 'unsignedInteger', 'name': 'Role', 'value': '1'}
        IgnoredvariableRole={'type': 'unsignedInteger', 'name': 'Role', 'value': '0'}
        
        for i in range(int(num_columns)):
            map_group=etree.SubElement(Map,'ParameterGroup',attrib={'name':(str(i))})
            if self.kwargs.get('experiment_type')[index]==str(1): #when Experiment type is set to time course it should be 1
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
                        etree.SubElement(map_group,'Parameter',attrib=IndepentantvariableRole)
                        
                    elif obs[i][:-6]!='indep':
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
                            LOG.warning('{}not in model and has not been mapped. Please check spelling and try again'.format(obs[i]))

                        else:
                            raise Errors.ExperimentMappingError('''\'{}\' mapping error. In the copasi GUI its possible to have same name for two species provided they are in different compartments. In this API, having non-unique species identifiers leads to errors in mapping experimental to model variables'''.format(obs[i]))
                        etree.SubElement(map_group,'Parameter',attrib=DepentantvariableRole)
                        
                        
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
                            LOG.warning('{}not in model and has not been mapped. Please check spelling and try again'.format(obs[i]))

                        else:
                            raise Errors.ExperimentMappingError('''\'{}\' mapping error. In the copasi GUI its possible to have same name for two species provided they are in different compartments. In this API, having non-unique species identifiers leads to errors in mapping experimental to model variables'''.format(obs[i]))
                        etree.SubElement(map_group,'Parameter',attrib=IgnoredvariableRole)


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
                    etree.SubElement(map_group,'Parameter',attrib=IndepentantvariableRole)
                    
                elif obs[i][-6:]!='_indep':
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
                    etree.SubElement(map_group,'Parameter',attrib=IgnoredvariableRole)
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
                    etree.SubElement(map_group,'Parameter',attrib=DepentantvariableRole)
            

        return Exp

    def add_experiment_set(self,experiment_element):
        query='//*[@name="Experiment Set"]'
        for j in self.copasiML.xpath(query):
            j.insert(0,experiment_element)
        return self.copasiML

    def save(self):
        self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML

    def save_deg(self):
        if self.kwargs.get('save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('save')=='overwrite':
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

class PhaseSpace(TimeCourse):
    '''
    Inherits from TimeCourse
    
    Use TimeCourse to get data and replot all n choose 2 combinations
    of phase space plot
    '''
    def __init__(self,copasi_file,**kwargs):
        super(PhaseSpace,self).__init__(copasi_file,**kwargs)
        LOG.debug('plotting all combinations of phase space plot')
        self.new_options={'plot':False}
        self.kwargs.update(self.new_options)
        self.species_data=self.isolate_species()
        self.combinations=self.get_combinations()
        
        if self.kwargs.get('savefig')==True:
            self.phase_dir=self.make_phase_dir()
            os.chdir(self.phase_dir)
        
        self.plot_all_phase()
        
        os.chdir(os.path.dirname(self.copasi_file))
        
            
    def isolate_species(self):
        '''
        Isolate the species from the time course data 
        '''
        metabs= self.GMQ.get_IC_cns().keys()
        for i in metabs:
            if i not in self.data.keys():
                raise Errors.IncompatibleStringError(' {} is an incompatible string that is not supported by PyCoTools. Please modify the string and rerun')
        return self.data[metabs]
        
    def get_combinations(self):
        return list(itertools.combinations(self.species_data.keys(),2))
        
    def make_phase_dir(self):
        dire=os.path.join(os.path.dirname(self.copasi_file),'Phaseplots')
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
        plt.plot(x_data,y_data,linewidth=self.kwargs.get('line_width'),
                    color=self.kwargs.get('line_color'),
                    linestyle=self.kwargs.get('line_style'),
                    marker='o',markerfacecolor=self.kwargs.get('marker_color'),
                    markersize=self.kwargs.get('marker_size'))
                    
        plt.title('\n'.join(wrap('{} Vs {} Phase plot'.format(x,y),self.kwargs.get('title_wrap_size'))),fontsize=self.kwargs.get('font_size'))
        try:
            plt.ylabel(y+'({})'.format(self.GMQ.get_quantity_units().encode('ascii')),fontsize=self.kwargs.get('font_size'))
            plt.xlabel(x+'({})'.format(self.GMQ.get_quantity_units().encode('ascii')),fontsize=self.kwargs.get('font_size'))         
        except UnicodeEncodeError:
            plt.ylabel(y+'({})'.format('micromol'),fontsize=self.kwargs.get('font_size'))
            plt.xlabel(x+'({})'.format('micromol'),fontsize=self.kwargs.get('font_size'))         
            
            
        #pretty stuff
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
        if self.kwargs.get('show')==True:
            plt.show()
            
        def replace_non_ascii(st):
            for j in st:
                if j  not in string.ascii_letters+string.digits+'_-[]':
                    st=re.sub('\{}'.format(j),'__',st) 
            return st    
            
        y_new=replace_non_ascii(y)
        x_new=replace_non_ascii(x)
        name='{}_Vs_{}_Phaseplot'.format(x_new,y_new)
        
        if self.kwargs.get('savefig')==True:
            if self.kwargs.get('extra_title') !=None:
                plt.savefig(name+'_'+self.kwargs.get('extra_title')+'.png',bbox_inches='tight',format='png',dpi=self.kwargs.get('dpi'))
            else:
                plt.savefig(name+'_'+'.png',format='png',bbox_inches='tight',dpi=self.kwargs.get('dpi'))     
    def plot_all_phase(self):
        for i in self.combinations:
            self.plot1phase(i[0],i[1])

class FormatPEData():
    def __init__(self,copasi_file,report_name, report_type='parameter_estimation'):
        self.copasi_file = copasi_file
        self.report_type = report_type
        self.GMQ = GetModelQuantities(self.copasi_file)
        self.report_name = report_name
        
        available_report_types = ['parameter_estimation','multi_parameter_estimation']
        if self.report_type not in available_report_types:
            raise Errors.InputError('{} not in {}'.format(self.report_type,available_report_types))
            
#        if os.path.isdir(self.report_name):
#            for i in os.listdir(self.report_name):
                
#        if os.path.isfile(self.report_name)!=True:
#            raise Errors.InputError('file {} does not exist'.format(self.report_name))
        
        if self.report_type=='parameter_estimation':
            try:
                self.format = self.format_results()
            except IOError:
                raise Errors.FileIsEmptyError('{} is empty and therefore cannot be read by pandas. Make sure you have waited until there is data in the parameter estimation file before formatting parameter estimation output')
            except pandas.parser.CParserError:
                raise Errors.InputError('Pandas cannot read data file. Ensure you are using report_type=\'multi_parameter_estimation\' for multiple parameter estimation classes')
        elif self.report_type=='multi_parameter_estimation':
            try:
                self.format = self.format_multi_results()
            except IOError:
                raise Errors.FileIsEmptyError('{} is empty and therefore cannot be read by pandas. Make sure you have waited until there is data in the parameter estimation file before formatting parameter estimation output')
        
        
    def format_results(self):
        """
        Results come without headers - parse the results
        give them the proper headers then overwrite the file again
        :return:
        """
        data = pandas.read_csv(self.report_name, sep='\t', header=None)
        data = data.drop(data.columns[0], axis=1)
        LOG.debug('Shape of estimated parameters: {}'.format(data.shape))
        width = data.shape[1]
        ## remove the extra bracket
        data[width] = data[width].str[1:]
#        num = data.shape[0]
        names = self.GMQ.get_fit_item_order()+['RSS']
        data.columns = names
        os.remove(self.report_name)
        data.to_csv(self.report_name,sep='\t',index=False)
        return data
    
    def format_multi_results(self):
        """
        Results come without headers - parse the results
        give them the proper headers then overwrite the file again
        :return:
        """
        try:
            data = pandas.read_csv(self.report_name, sep='\t', header=None, skiprows=[0])
        except:
            LOG.warning('No Columns to parse from file. {} is empty. Returned None'.format(self.report_name))
            return None
        bracket_columns = data[data.columns[[0,-2]]]
        if bracket_columns.iloc[0].iloc[0] != '(':
            data = pandas.read_csv(self.report_name, sep='\t')
            return data
        else:
            data = data.drop(data.columns[[0,-2]], axis=1)
            data.columns = range(data.shape[1])
            LOG.debug('Shape of estimated parameters: {}'.format(data.shape))
            ### parameter of interest has been removed. 
            names = self.GMQ.get_fit_item_order()+['RSS']
            if self.GMQ.get_fit_item_order() == []:
                raise Errors.SomethingWentHorriblyWrongError('Parameter Estimation task is empty')
            if len(names) != data.shape[1]:
                raise Errors.SomethingWentHorriblyWrongError('length of parameter estimation data does not equal number of parameters estimated')
                
            if os.path.isfile(self.report_name):
                os.remove(self.report_name)
            data.columns = names
            data.to_csv(self.report_name, sep='\t', index=False)
            return self.report_name
    
    @staticmethod
    def format_folder(copasi_file, folder, report_type='multi_parameter_estimation'):
        """
        Format entire folder of similar PE data files
        """
        for i in glob.glob(os.path.join(folder, '*.txt')):
            FormatPEData(copasi_file, i, report_type=report_type)
            
        
        
    


class ParameterEstimation():
    '''
    Set up and run a parameter estimation in copasi. Since each parameter estimation
    problem is different, this process cannot be done in a single line of code. 
    Instead the user should initialize an instance of the ParameterEstimation 
    class with all the relevant keyword arguments. Subsequently use the 
    write_item_template() method and modify the resulting xlsx in your copasi file
    directory. save the file then close and run the setup()() method to define your
    optimization problem. When run is set to True, the parameter estimation will
    automatically run in CopasiSE. If plot is also set to True, a plot comparing 
    experimental and simulated profiles are produced. Profiles are saved
    to file with savefig=True
    
    args:
        
        copasi_file: 
            The file path for the copasi file you want to perform parameter estimation on
            
        experiment_files:
            Either a single experiment file path or a list of experiment file paths 
            
    **Kwargs:
        
        metabolites:
            Which metabolites (ICs) to include in parameter esitmation. Default = all of them. 
            
        global_quantities:
            Which global values to include in the parameter estimation. Default= all
        
        quantity_type:
            either 'concentration' or particle numbers

        report_name:
            name of the output report
            
        append:
            append to report or not,True or False

        confirm_overwrite:
            True or False, overwrite report or not
            
        config_filename:
            Filename for the parameter estimation config file
            
        overwrite_config_file:,
            True or False, overwrite the config file each time program is run
            
        update_model:
            Update model parameters after parameter estimation

        randomize_start_values:
            True or False. Check the randomize start values box or not. Default True

        create_parameter_sets:
            True or False. Check the create parameter sets box or not. Default False
        
        calculate_statistics':str(1),
            True or False. Check the calcualte statistics box or not. Default False

        method:
            Name of one of the copasi parameter estimation algorithms. Valid arguments: 
            ['CurrentSolutionStatistics','DifferentialEvolution','EvolutionaryStrategySR','EvolutionaryProgram',
             'HookeJeeves','LevenbergMarquardt','NelderMead','ParticleSwarm','Praxis',
             'RandomSearch','ScatterSearch','SimulatedAnnealing','SteepestDescent',
             'TruncatedNewton','GeneticAlgorithm','GeneticAlgorithmSR'],
             Default=GeneticAlgorithm

        number_of_generations:
            A parameter for parameter estimation algorithms. Default=200

        population_size:
            A parameter for parameter estimation algorithms. Default=50

        random_number_generator:
            A parameter for parameter estimation algorithms. Default=1

        seed:
            A parameter for parameter estimation algorithms. Default=0

        pf:
            A parameter for parameter estimation algorithms. Default=0.475

        iteration_limit:
            A parameter for parameter estimation algorithms. Default=50

        tolerance:
            A parameter for parameter estimation algorithms. Default=0.00001

        rho;
            A parameter for parameter estimation algorithms. Default=0.2

        scale:
            A parameter for parameter estimation algorithms. Default=10

        swarm_size:
            A parameter for parameter estimation algorithms. Default=50

        std_deviation:
            A parameter for parameter estimation algorithms. Default=0.000001

        number_of_iterations:
            A parameter for parameter estimation algorithms. Default=100000

        start_temperature:
            A parameter for parameter estimation algorithms. Default=1

        cooling_factor:
            A parameter for parameter estimation algorithms. Default=0.85

        row_orientation:
            1 means data is row oriented, 0 means its column oriented
                         
        experiment_type:
            List with the same number elements as you have experiment files. Each element
            is either 'timecourse' or 'steady_state' and describes the type of 
            data at that element in the experiment_files argument 

        first_row:
            List with the same number elements as you have experiment files. Each element
            is the starting line for data as an integer. Default is a list of 1's and this
            rarely needs to be changed.
            
        normalize_weights_per_experiment':[True]*len(self.experiment_files),
            List with the same number elements as you have experiment files. Each element
            is True or False and correlates to ticking the
            normalize wieghts per experiment box in the copasi gui. Default [true]*len(experiments)
            
        row_containing_names:
            List with the same number elements as you have experiment files. Each element
            is an integer value corresponding to the row in the data containing names. The default
            is 1 for all experiment files [1]*len(experiment_files)
                        

        separator':['\t']*len(self.experiment_files),
            List with the same number elements as you have experiment files. Each element
            is the separator used in the data files. Defaults to a tab (\\t) for all files 
            though commas are also common
            
        weight_method':['mean_squared']*len(self.experiment_files),
            List with the same number elements as you have experiment files. Each element
            is a list of the name of the normalization algorithm to use for that data set. 
            This should probably be the same for each experiment file and defaults to mean_squared. 
            Options are: ['mean','mean_squared','stardard_deviation','value_scaling']
            
        save: 
            One of False,'duplicate' or 'overwrite'. If duplicate, use the name in 
            the keyword argument OutputML to save the file.


        prune_headers:
            Copasi uses references to distinguish between variable types. The report
            output usually contains these references in variable names. True removes 
            the references while False leaves them in. 
        scheduled':False
            True or False. Check the box called 'executable' in the top right hand
            corner of the Copasi GUI. This tells Copasi to shedule a parameter estimation 
            task when using CopasiSE. This should be True of you are running a parameter
            estimation from the parameter estimation task via the pycopi but False when you 
            want to set up a repeat item in the scan task with the parameter estimation subtask
            
        use_config_start_values:
            Default set to False. Determines whether the starting parameters 
            from within the fitItemTemplate.xlsx are use for starting values
            in the parameter estimation or not
                 
        lower_bound:
            Value of the default lower bound for the FitItemTemplate. Default 0.000001
        
        upper_bound:
            Value of default upper bound for FitItemTemplate. Default=1000000
            
#        run:
#            run the parameter estimation using CopasiSE. When running via the parameter
#            estimation task, the output is a matrix of function evaluation progression over
#            time. When running via the scan's repeat task, output is lines of parameter
#            estimation runs
            
        plot:
            Whether to plot result or not. Defualt=True
            
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

        savefig:
            save graphs to file labelled after the index


        title_wrap_size:
            When graph titles are long, how many characters to have per 
            line before word wrap. Default=30. 
            
        show:
            When not using iPython, use show=True to display graphs
            
        ylimit: default==None, restrict amount of data shown on y axis. 
        Useful for honing in on small confidence intervals

        xlimit: default==None, restrict amount of data shown on x axis. 
        Useful for honing in on small confidence intervals
        
        dpi:
            How big saved figure should be. Default=125
        
        xtick_rotation:
            How many degrees to rotate the x tick labels
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
        options={#report variables
                 'metabolites':self.GMQ.get_IC_cns().keys(),
                 'global_quantities':self.GMQ.get_global_quantities().keys(),
                 'local_parameters': self.GMQ.get_local_kinetic_parameters_cns().keys(),
                 'quantity_type':'concentration',
                 'report_name':default_report_name,
                 'append': False, 
                 'confirm_overwrite': False,
                 'config_filename':config_file,
                 'overwrite_config_file':False,
                 'prune_headers':True,
                 'update_model':False,
                 'randomize_start_values':True,
                 'create_parameter_sets':False,
                 'calculate_statistics':False,
                 'use_config_start_values':False,
                 #method options
                 'method':'GeneticAlgorithm',
                 #'DifferentialEvolution',
                 'number_of_generations':200,
                 'population_size':50,
                 'random_number_generator':1,
                 'seed':0,
                 'pf':0.475,
                 'iteration_limit':50,
                 'tolerance':0.00001,
                 'rho':0.2,
                 'scale':10,
                 'swarm_size':50,
                 'std_deviation':0.000001,
                 'number_of_iterations':100000,
                 'start_temperature':1,
                 'cooling_factor':0.85,
                 #experiment definition options
                 #need to include options for defining multiple experimental files at once
                 'row_orientation':[True]*len(self.experiment_files),
                 'experiment_type':['timecourse']*len(self.experiment_files),
                 'first_row':[str(1)]*len(self.experiment_files),
                 'normalize_weights_per_experiment':[True]*len(self.experiment_files),
                 'row_containing_names':[str(1)]*len(self.experiment_files),
                 'separator':['\t']*len(self.experiment_files),
                 'weight_method':['mean_squared']*len(self.experiment_files),
                 'save':'overwrite',  
                 'scheduled':False,
                 'lower_bound':0.000001,
                 'upper_bound':1000000,
                 'plot':False,
                 'results_directory':os.path.join(os.path.dirname(self.copasi_file), 'ParameterEstimationPlots'),
                 'font_size':22,
                 'axis_size':15,
                 'extra_title':None,
                 'line_width':3,
                 'show':False,
                 'savefig':False,
                 'title_wrap_size':30,
                 'ylimit':None,
                 'xlimit':None,
                 'dpi':125,
                 'xtick_rotation':35,
                 'marker_size':10,
                 'legend_loc':(1,0),
                 }
                     
        #values need to be lower case for copasiML
        for i in kwargs.keys():
            if i not in options.keys():
                raise Errors.InputError('{} is not a keyword argument for ParameterEstimation'.format(i) )
        options.update( kwargs) 
        self.kwargs=options
        #second dict to separate arguments for the experiment mapper
        self.kwargs_experiment={}
        
        self.kwargs_experiment['row_orientation']=self.kwargs.get('row_orientation')
        self.kwargs_experiment['experiment_type']=self.kwargs.get('experiment_type')
        self.kwargs_experiment['first_row']=self.kwargs.get('first_row')
        self.kwargs_experiment['normalize_weights_per_experiment']=self.kwargs.get('normalize_weights_per_experiment')
        self.kwargs_experiment['row_containing_names']=self.kwargs.get('row_containing_names')
        self.kwargs_experiment['separator']=self.kwargs.get('separator')
        self.kwargs_experiment['weight_method']=self.kwargs.get('weight_method')
        self.kwargs_experiment['save']=self.kwargs.get('save')
        
#        for i in self.kwargs_experiment.keys():
#            assert len(self.experiment_files)==len(self.kwargs_experiment.get(i)),'{} is {} and {} is {}'.format(self.experiment_files,len(self.experiment_files),(self.kwargs_experiment.get(i)),len(self.kwargs_experiment.get(i)))

        self.method_list=['CurrentSolutionStatistics','DifferentialEvolution',
                     'EvolutionaryStrategySR','EvolutionaryProgram',
                     'HookeJeeves','LevenbergMarquardt','NelderMead',
                     'ParticleSwarm','Praxis','RandomSearch','ScatterSearch','SimulatedAnnealing',
                     'SteepestDescent','TruncatedNewton','GeneticAlgorithm',
                     'GeneticAlgorithmSR']
        assert self.kwargs.get('method').lower() in [i.lower() for i in self.method_list],'{} is not a copasi PE method. Choose one of: {}'.format(self.kwargs.get('method'),self.method_list)
        assert self.kwargs.get('append') in [True,False,'true','false']
        assert self.kwargs.get('confirm_overwrite') in [True,False,'true','false']
        
        if self.kwargs['append']==True:
            self.kwargs['append']=str(1)
        else:
            self.kwargs['append']=str(0)
            
        if self.kwargs['confirm_overwrite']==True:
            self.kwargs['confirm_overwrite']=str(1)
        else:
            self.kwargs['confirm_overwrite']=str(0)        
            
        self.kwargs['method']=self.kwargs.get('method').lower()
        if self.kwargs['method']=='currentsolutionstatistics':
            if self.kwargs['randomize_start_values']==True:
                raise Errors.InputError('Cannot run current solution statistics with \'randomize_start_values\' set to \'true\'.' )
        write_to_file_list=['duplicate','overwrite',False]
        assert self.kwargs.get('save') in write_to_file_list  
        
        assert isinstance(self.kwargs.get('local_parameters'),list)
        for i in self.kwargs.get('local_parameters'):
            assert i in self.GMQ.get_local_kinetic_parameters_cns().keys()

        assert isinstance(self.kwargs.get('global_quantities'),list)
        for i in self.kwargs.get('global_quantities'):
            assert i in self.GMQ.get_global_quantities().keys()
    

        assert isinstance(self.kwargs.get('metabolites'),list)
        for i in self.kwargs.get('metabolites'):
            assert i in self.GMQ.get_IC_cns().keys()

        if self.kwargs['use_config_start_values'] not in [True,False,'true','false']:
            raise Errors.InputError(''' Argument to the use_config_start_values must be \'true\' or \'false\' not {}'''.format(self.kwargs['use_config_start_values']))


            
        #determine which method to use        
        if self.kwargs.get('method')=='CurrentSolutionStatistics'.lower():
            self.method_name='Current Solution Statistics'
            self.method_type='CurrentSolutionStatistics'

        if self.kwargs.get('method')=='DifferentialEvolution'.lower():
            self.method_name='Differential Evolution'
            self.method_type='DifferentialEvolution'

        if self.kwargs.get('method')=='EvolutionaryStrategySR'.lower():
            self.method_name='Evolution Strategy (SRES)'
            self.method_type='EvolutionaryStrategySR'

        if self.kwargs.get('method')=='EvolutionaryProgram'.lower():
            self.method_name='Evolutionary Programming'
            self.method_type='EvolutionaryProgram'

        if self.kwargs.get('method')=='HookeJeeves'.lower():
            self.method_name='Hooke &amp; Jeeves' 
            self.method_type='HookeJeeves'

        if self.kwargs.get('method')=='LevenbergMarquardt'.lower():
            self.method_name='Levenberg - Marquardt'
            self.method_type='LevenbergMarquardt'

        if self.kwargs.get('method')=='NelderMead'.lower():
            self.method_name='Nelder - Mead'
            self.method_type='NelderMead'

        if self.kwargs.get('method')=='ParticleSwarm'.lower():
            self.method_name='Particle Swarm'
            self.method_type='ParticleSwarm'

        if self.kwargs.get('method')=='Praxis'.lower():
            self.method_name='Praxis'
            self.method_type='Praxis'

        if self.kwargs.get('method')=='RandomSearch'.lower():
            self.method_name='Random Search'
            self.method_type='RandomSearch'

        if self.kwargs.get('method')=='SimulatedAnnealing'.lower():
            self.method_name='Simulated Annealing'
            self.method_type='SimulatedAnnealing'

        if self.kwargs.get('method')=='SteepestDescent'.lower():
            self.method_name='Steepest Descent'
            self.method_type='SteepestDescent'

        if self.kwargs.get('method')=='TruncatedNewton'.lower():
            self.method_name='Truncated Newton'
            self.method_type='TruncatedNewton'

        if self.kwargs.get('method')=='ScatterSearch'.lower():
            self.method_name='Scatter Search'
            self.method_type='ScatterSearch'

        if self.kwargs.get('method')=='GeneticAlgorithm'.lower():
            self.method_name='Genetic Algorithm'
            self.method_type='GeneticAlgorithm'

        if self.kwargs.get('method')=='GeneticAlgorithmSR'.lower():
            self.method_name='Genetic Algorithm SR'
            self.method_type='GeneticAlgorithmSR'
    

            
        assert self.kwargs.get('create_parameter_sets') in [False,True,'false','true']
        if self.kwargs.get('create_parameter_sets')==False:
            self.kwargs['create_parameter_sets']=str(0)
        else:
            self.kwargs['create_parameter_sets']=str(1)
            
        assert self.kwargs.get('calculate_statistics') in [False,True,'false','true']
        if self.kwargs.get('calculate_statistics')==False:
            self.kwargs['calculate_statistics']=str(0)
        else:
            self.kwargs['calculate_statistics']=str(1)

        assert self.kwargs.get('plot') in [False,True,'false','true']



        if isinstance(self.kwargs.get('metabolites'),str):
            self.kwargs['metabolites']=[self.kwargs.get('metabolites')]

        if isinstance(self.kwargs.get('global_quantities'),str):
            self.kwargs['global_quantities']=[self.kwargs.get('global_quantities')]

        if isinstance(self.kwargs.get('local_parameters'),str):
            self.kwargs['local_parameters']=[self.kwargs.get('local_parameters')]


        self.kwargs = Bool2Str(self.kwargs).convert_dct()

        self.kwargs['number_of_generations']=str(self.kwargs.get('number_of_generations'))
        self.kwargs['population_size']=str(self.kwargs.get('population_size'))
        self.kwargs['random_number_generator']=str(self.kwargs.get('random_number_generator'))
        self.kwargs['seed']=str(self.kwargs.get('seed'))
        self.kwargs['pf']=str(self.kwargs.get('pf'))
        self.kwargs['iteration_limit']=str(self.kwargs.get('iteration_limit'))
        self.kwargs['tolerance']=str(self.kwargs.get('tolerance'))
        self.kwargs['rho']=str(self.kwargs.get('rho'))
        self.kwargs['scale']=str(self.kwargs.get('scale'))
        self.kwargs['scale']=str(self.kwargs.get('scale'))
        self.kwargs['swarm_size']=str(self.kwargs.get('swarm_size'))
        self.kwargs['std_deviation']=str(self.kwargs.get('std_deviation'))
        self.kwargs['number_of_iterations']=str(self.kwargs.get('number_of_iterations'))
        self.kwargs['start_temperature']=str(self.kwargs.get('start_temperature'))
        self.kwargs['cooling_factor']=str(self.kwargs.get('cooling_factor'))
        self.kwargs['lower_bound']=str( self.kwargs.get('lower_bound'))
        self.kwargs['start_value']=str( self.kwargs.get('start_value'))
        self.kwargs['upper_bound']=str( self.kwargs.get('upper_bound'))
        
        
        #report specific arguments
        self.report_dict={}
        self.report_dict['metabolites']=self.kwargs.get('metabolites')
        self.report_dict['global_quantities']=self.kwargs.get('global_quantities')
        self.report_dict['local_parameters']=self.kwargs.get('local_parameters')
        self.report_dict['quantity_type']=self.kwargs.get('quantity_type')
        self.report_dict['report_name']=self.kwargs.get('report_name')
        self.report_dict['append']=self.kwargs.get('append')
        self.report_dict['confirm_overwrite']=self.kwargs.get('confirm_overwrite')
        self.report_dict['save']=self.kwargs.get('save')
        self.report_dict['variable']=self.kwargs.get('variable')
        self.report_dict['report_type']='parameter_estimation'
        
        
        
        '''
        PlotPEDataKwargs plotting specific kwargs
        '''
        self.PlotPEDataKwargs={}
        self.PlotPEDataKwargs['line_width']=self.kwargs.get('line_width')
        self.PlotPEDataKwargs['font_size']=self.kwargs.get('font_size')
        self.PlotPEDataKwargs['axis_size']=self.kwargs.get('axis_size')
        self.PlotPEDataKwargs['extra_title']=self.kwargs.get('extra_title')
        self.PlotPEDataKwargs['show']=self.kwargs.get('show')
        self.PlotPEDataKwargs['savefig']=self.kwargs.get('savefig')
        self.PlotPEDataKwargs['title_wrap_size']=self.kwargs.get('title_wrap_size')
        self.PlotPEDataKwargs['ylimit']=self.kwargs.get('ylimit')
        self.PlotPEDataKwargs['xlimit']=self.kwargs.get('xlimit')
        self.PlotPEDataKwargs['dpi']=self.kwargs.get('dpi')
        self.PlotPEDataKwargs['xtick_rotation']=self.kwargs.get('xtick_rotation')
        self.PlotPEDataKwargs['marker_size']=self.kwargs.get('marker_size')
        self.PlotPEDataKwargs['legend_loc']=self.kwargs.get('legend_loc')
        self.PlotPEDataKwargs['prune_headers']=self.kwargs.get('prune_headers')
        self.PlotPEDataKwargs['separator']=self.kwargs.get('separator')
        self.PlotPEDataKwargs['results_directory']=self.kwargs.get('results_directory')

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,sorted(self.kwargs.keys())))
        return self.kwargs[key]

    def __setitem__(self,key,value):
        self.kwargs[key] = value
        
    def run(self):
        if self.kwargs.get('plot')==False:
            LOG.debug('running ParameterEstimation. Data reported to file: {}'.format(self.kwargs['report_name']))
            self.copasiML = Run(self.copasi_file, task='parameter_estimation')
            self.format_results()
            return self.copasiML
        else:
            ##Run with 'mode' set to false just unchecks the executable boxes.
            self.copasiML=Run(self.copasi_file,task='parameter_estimation',mode=False)
            ## Now run with check_call
            os.system('CopasiSE "{}"'.format(self.copasi_file))
            self.format_results()
            self.plot()
        return self.copasiML

    def format_results(self):
        """
        Results come without headers - parse the results
        give them the proper headers then overwrite the file again
        :return:
        """
        FormatPEData(self.copasi_file, self['report_name'], report_type='parameter_estimation')


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
        LOG.warning('write_item_template is deprecated. It will work but please use write_config_template instead')
        if os.path.isfile(self.kwargs.get('config_filename'))==False or self.kwargs.get('overwrite_config_file')==True:
            self.get_item_template().to_excel(self.kwargs.get('config_filename'))
        return  'writing template. {} set to {} and {} is {}'.format('overwrite_config_file',self.kwargs.get('overwrite_config_file'),'config_filename',self.kwargs.get('config_filename'))

    def write_config_template(self):
        if os.path.isfile(self.kwargs.get('config_filename'))==False or self.kwargs.get('overwrite_config_file')==True:
            self.get_item_template().to_excel(self.kwargs.get('config_filename'))
            LOG.debug(  'writing config template. {} set to {} and {} is {}'.format('overwrite_config_file',self.kwargs.get('overwrite_config_file'),'config_filename',self.kwargs.get('config_filename')))

        
    def read_item_template(self):
        if os.path.isfile(self.kwargs.get('config_filename'))!=True:
            raise Errors.InputError('ConfigFile does not exist. run \'write_config_template\' method and modify it how you like then run the setup()  method again.')
        df = pandas.read_excel(self.kwargs.get('config_filename'))
        parameter_names = list(df[df.columns[0]])
        
        model_parameters = self.GMQ.get_all_model_variables().keys()
        for parameter in parameter_names:
            if parameter not in model_parameters:
                raise Errors.InputError('{} not in {}\n\n Ensure you are using the correct PE config file!'.format(parameter, model_parameters))
        return df 
    
    def add_fit_item(self,item):
        '''
        
        need 5 elements, each with their own attributes. Their names are:
            Affected Cross Validation Experiments
            Affected Experiments
            lower_bound
            ObjectCN
            startValue
            upper_bound
            
        the element name is <ParameterGroup name="FitItem">
        '''
        #initialize new element
        new_element=etree.Element('ParameterGroup',attrib={'name':'FitItem'})
        all_items= self.read_item_template()
        assert item in list(all_items.index),'{} is not in your ItemTemplate. You item template contains: {}'.format(item,list(all_items.index))
        item= all_items.loc[item]
        subA1={'name': 'Affected Cross Validation Experiments'}
        subA2={'name': 'Affected Experiments'}
        subA3={'type': 'cn', 'name': 'LowerBound', 'value': str(item['lower_bound'])}
        if self.kwargs.get('use_config_start_values')==True:
            subA5={'type': 'float', 'name': 'StartValue', 'value': str(item['startValue'])}
        
        subA6={'type': 'cn', 'name': 'UpperBound', 'value': str(item['upper_bound'])}
        
        etree.SubElement(new_element,'ParameterGroup',attrib=subA1)
        etree.SubElement(new_element,'ParameterGroup',attrib=subA2)
        etree.SubElement(new_element,'Parameter',attrib=subA3)
        if self.kwargs.get('use_config_start_values')==True:
            etree.SubElement(new_element,'Parameter',attrib=subA5)
        etree.SubElement(new_element,'Parameter',attrib=subA6)
        
        #for IC parameters
        if item['simulationType']=='reactions' and item['type']=='Species':
            #fill in the attributes
            if self.kwargs.get('quantity_type')=='concentration':
                subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialConcentration'}
            else:
                subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialParticleNumber'}

        elif item['simulationType']=='ode' and item['type']=='Species':
            if self.kwargs.get('quantity_type')=='concentration':
                subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialConcentration'}
            else:
                subA4={'type': 'cn', 'name': 'ObjectCN', 'value': str(item['cn'])+',Reference=InitialParticleNumber'}

        elif item['simulationType']=='ode' and item['type']=='ModelValue':
            if self.kwargs.get('quantity_type')=='concentration':
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
        #Build xML for method. Root=method for now. Will be merged with CoapsiML later
        method_params={'name':self.method_name, 'type':self.method_type}
        method_element=etree.Element('Method',attrib=method_params)

        #list of attribute dictionaries 
        #Evolutionary strategy parametery
        number_of_generations={'type': 'unsignedInteger', 'name': 'Number of Generations', 'value': self.kwargs.get('number_of_generations')}
        population_size={'type': 'unsignedInteger', 'name': 'Population Size', 'value': self.kwargs.get('population_size')}
        random_number_generator={'type': 'unsignedInteger', 'name': 'Random Number Generator', 'value': self.kwargs.get('random_number_generator')}
        seed={'type': 'unsignedInteger', 'name': 'Seed', 'value': self.kwargs.get('seed')}
        pf={'type': 'float', 'name': 'Pf', 'value': self.kwargs.get('pf')}
        #local method parameters
        iteration_limit={'type': 'unsignedInteger', 'name': 'Iteration Limit', 'value': self.kwargs.get('iteration_limit')}
        tolerance={'type': 'float', 'name': 'Tolerance', 'value': self.kwargs.get('tolerance')}
        rho={'type': 'float', 'name': 'Rho', 'value': self.kwargs.get('rho')}
        scale={'type': 'unsignedFloat', 'name': 'Scale', 'value': self.kwargs.get('scale')}
        #Particle Swarm parmeters
        swarm_size={'type': 'unsignedInteger', 'name': 'Swarm Size', 'value': self.kwargs.get('swarm_size')}
        std_deviation={'type': 'unsignedFloat', 'name': 'Std. Deviation', 'value': self.kwargs.get('std_deviation')}
        #Random Search parameters
        number_of_iterations={'type': 'unsignedInteger', 'name': 'Number of Iterations', 'value': self.kwargs.get('number_of_iterations')}
        #Simulated Annealing parameters
        start_temperature={'type': 'unsignedFloat', 'name': 'Start Temperature', 'value': self.kwargs.get('start_temperature')}
        cooling_factor={'type': 'unsignedFloat', 'name': 'Cooling Factor', 'value': self.kwargs.get('cooling_factor')}


        #build the appropiate xML, with method at root (for now)
        if self.kwargs.get('method')=='CurrentSolutionStatistics'.lower():
            pass #no additional parameter elements required

        if self.kwargs.get('method')=='DifferentialEvolution'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_generations)
            etree.SubElement(method_element,'Parameter',attrib=population_size)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)

        if self.kwargs.get('method')=='EvolutionaryStrategySR'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_generations)
            etree.SubElement(method_element,'Parameter',attrib=population_size)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)
            etree.SubElement(method_element,'Parameter',attrib=pf)

        if self.kwargs.get('method')=='EvolutionaryProgram'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_generations)
            etree.SubElement(method_element,'Parameter',attrib=population_size)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)

        if self.kwargs.get('method')=='HookeJeeves'.lower():
            etree.SubElement(method_element,'Parameter',attrib=iteration_limit)
            etree.SubElement(method_element,'Parameter',attrib=tolerance)
            etree.SubElement(method_element,'Parameter',attrib=rho)

        if self.kwargs.get('method')=='LevenbergMarquardt'.lower():
            etree.SubElement(method_element,'Parameter',attrib=iteration_limit)
            etree.SubElement(method_element,'Parameter',attrib=tolerance)
#
        if self.kwargs.get('method')=='NelderMead'.lower():
            etree.SubElement(method_element,'Parameter',attrib=iteration_limit)
            etree.SubElement(method_element,'Parameter',attrib=tolerance)
            etree.SubElement(method_element,'Parameter',attrib=scale)

        if self.kwargs.get('method')=='ParticleSwarm'.lower():
            etree.SubElement(method_element,'Parameter',attrib=iteration_limit)
            etree.SubElement(method_element,'Parameter',attrib=swarm_size)
            etree.SubElement(method_element,'Parameter',attrib=std_deviation)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)

        if self.kwargs.get('method')=='Praxis'.lower():
            etree.SubElement(method_element,'Parameter',attrib=tolerance)

        if self.kwargs.get('method')=='RandomSearch'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_iterations)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)

        if self.kwargs.get('method')=='SimulatedAnnealing'.lower():
            etree.SubElement(method_element,'Parameter',attrib=start_temperature)
            etree.SubElement(method_element,'Parameter',attrib=cooling_factor)
            etree.SubElement(method_element,'Parameter',attrib=tolerance)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)
#
        if self.kwargs.get('method')=='SteepestDescent'.lower():
            etree.SubElement(method_element,'Parameter',attrib=iteration_limit)
            etree.SubElement(method_element,'Parameter',attrib=tolerance)
#
        if self.kwargs.get('method')=='TruncatedNewton'.lower():
            #required no additonal paraemters
            pass
#
        if self.kwargs.get('method')=='ScatterSearch'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_iterations)


        if self.kwargs.get('method')=='GeneticAlgorithm'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_generations)
            etree.SubElement(method_element,'Parameter',attrib=population_size)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)            

        if self.kwargs.get('method')=='GeneticAlgorithmSR'.lower():
            etree.SubElement(method_element,'Parameter',attrib=number_of_generations)
            etree.SubElement(method_element,'Parameter',attrib=population_size)
            etree.SubElement(method_element,'Parameter',attrib=random_number_generator)
            etree.SubElement(method_element,'Parameter',attrib=seed)  
            etree.SubElement(method_element,'Parameter',attrib=pf)  

        
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
        
        scheluled_attrib={'scheduled': self.kwargs.get('scheduled'),
                          'updateModel': self.kwargs.get('update_model')}
                          
        report_attrib={'append': self.kwargs.get('append'),
                       'reference': self.get_report_key(),
                       'target': self.kwargs.get('report_name'),
                       'confirmOverwrite': self.kwargs.get('confirm_overwrite')}


        randomize_start_values={'type': 'bool', 
                                'name': 'Randomize Start Values',
                                'value': self.kwargs.get('randomize_start_values')}

        calculate_stats={'type': 'bool', 'name': 'Calculate Statistics', 'value': self.kwargs.get('calculate_statistics')}
        create_parameter_sets={'type': 'bool', 'name': 'Create Parameter Sets', 'value': self.kwargs.get('create_parameter_sets')}

        query='//*[@name="Parameter Estimation"]' and '//*[@type="parameterFitting"]'
        for i in self.copasiML.xpath(query):
            i.attrib.update(scheluled_attrib)
            for j in list(i):
                if self.kwargs.get('report_name')!=None:
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
        '''
         'metabolites':self.GMQ.get_IC_cns().keys(),
         'global_quantities':self.GMQ.get_global_quantities().keys(),
         'local_parameters': self.GMQ.get_local_kinetic_parameters_cns().keys(),
        '''        
        local_params= self.GMQ.get_local_kinetic_parameters_cns()
        
        for key in local_params.keys():
            if key not in self['local_parameters']:
                del local_params[key]
                
        LOG.debug(local_params)
        global_params= self.GMQ.get_global_quantities_cns()
        
        for key in global_params.keys():
            if key not in self['global_quantities']:
                del global_params[key]
                
        IC_params= self.GMQ.get_IC_cns()
        
        for key in IC_params.keys():
            if key not in self['metabolites']:
                del IC_params[key]
                
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
            if self.kwargs.get('quantity_type')=='concentration':
                df=df.drop('value',axis=1)
                df=df.rename(columns={'concentration':'value'})
            elif self.kwargs.get('quantity_type')=='particle_number':
                df=df.drop('concentration',axis=1)
            df_list_ICs.append(df)
        l=df_list_local+df_list_global+df_list_ICs
        assert len(l)!=0,'No ICs, local or global quantities in your model. This is a problem'
        df= pandas.concat(l)
        df=df.rename(columns={'value':'start_value'})
        df['lower_bound']=[self.kwargs.get('lower_bound')]*df.shape[0]
        df['upper_bound']=[self.kwargs.get('upper_bound')]*df.shape[0]
        df.index.name='parameter'
        order=['start_value','lower_bound','upper_bound','simulationType','type','cn']
        df=df[order]
        return df

    def save(self):
        """
        
        """
        self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML

    def setup(self):
        EM=ExperimentMapper(self.copasi_file,self.experiment_files,**self.kwargs_experiment)
        self.copasiML=EM.copasiML
        self.copasiML=self.define_report()
        self.copasiML=self.remove_all_fit_items()
        self.copasiML=self.set_PE_method()
        self.copasiML=self.set_PE_options()
        self.copasiML=self.insert_all_fit_items()
        self.copasiML=self.save()
        
            
    def set_up(self):
        LOG.warning('The set_up method is deprecated. Use setup() method instead')
        EM=ExperimentMapper(self.copasi_file,self.experiment_files,**self.kwargs_experiment)
        self.copasiML=EM.copasiML
        self.copasiML=self.define_report()
        self.copasiML=self.remove_all_fit_items()
        self.copasiML=self.set_PE_method()
        self.copasiML=self.set_PE_options()
        self.copasiML=self.insert_all_fit_items()
        self.copasiML=self.save()
        
    def plot(self):
        self.PL=PEAnalysis.PlotPEData(self.copasi_file,self.experiment_files,self.kwargs.get('report_name'),
                        **self.PlotPEDataKwargs)

#==============================================================================

class Scan():
    '''
    Positional Args:
        copasi_file:
            the copasi file you want to scan

    **kwargs:
        scan_type:
            Which type of scan do you want to set up. 
            Options are ['scan','repeat','random_sampling']

        metabolites:
            metabolites to pass to report 
        
        global_quantities:
            global wuantities to pass to report
            
        quantity_type:
            either 'concentration' or 'particle_number'
        
        report_name:
            Name the output report
            
        append:
            Check the append button in copasi scan task.
            Options are [True or False], default=False
            
        confirm_overwrite:
            Check the confirm overwrite button in copasi scan.
            Options are [True or False], default=False
            
        update_model:
            Check the update model button in copasi scan task
            Options are [True or False], default=False
        
        subtask:
            A valid scan subtask. Options are:
            ['steady_state','time_course','metabolic_control_nalysis',
            'lyapunov_exponents','optimiztion','parameter_estimation',
            'sensitivities','linear_noise_approximation','cross_section',
            'time_scale_separation_analysis']
                   
        report_type:
            Which type of report to use. Options are ['none',
            'profilelikelihood','time_course','parameter_estimation']
            
        output_in_subtask:
            Check the output_in_subtask button in copasi scan task
            Options are [True or False], default=False

        adjust_initial_conditions:
            Check the adjust_initial_conditions button in copasi scan task
            Options are [True or False], default=False
            
        number_of_steps:
            Corresponds to the intervals box in Copasi GUI or number
            of repeats in case your using the task='repeat' option. Default=10.
            
        maximum: 
            Corresponds to the maximum box in Copasi GUI. Default=100. 

        minimum: 
            Corresponds to the minimum box in Copasi GUI. Default=0.01. 

        log10: 
            Corresponds to the log10 box in Copasi GUI.
            Options are [True or False], default=False.  
            
        distribution_type:
            When scan_type set to 'random_sampling', can be any of
            ['normal','uniform','poisson','gamma']. Default='normal'
            
        variable:
            The target of the Scan. Must be a valid model entity. 
            Defaults to the first key in the GMQ.get_IC_cns() method

        scheduled: 
            Corresponds to the scheduled box in Copasi GUI. Default=True.
            
        save:
            Can be one of ['duplicate',False,'overwrite']. Duplicate
            will copy copasi file to different file name. Default='overwrite'
            
        clear_scans:
            True or False. If True will remove all scans present before
            adding scans. If false, will add another scan in addition to any
            scans alredy present.Default=True
            
        run:
            run Scan task or not. True or False or 'SGE'. Default=False
            
    '''
    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=GetModelQuantities(self.copasi_file)
        
        default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_PE_results.txt'
        #default_outputML=os.path.split(self.copasi_file)[1][:-4]+'_Duplicate.cps'
        options={#report variables
                 'metabolites':self.GMQ.get_IC_cns().keys(),
                 'global_quantities':self.GMQ.get_global_quantities().keys(),
                 'quantity_type':'concentration',
                 'report_name':default_report_name,
                 'append': False, 
                 'confirm_overwrite': False,
                 'update_model':False,
                 'subtask':'parameter_estimation',
                 'report_type':'profilelikelihood',
                 'output_in_subtask':False,
                 'adjust_initial_conditions':False,
                 'number_of_steps':10,
                 'maximum':100,
                 'minimum':0.01,
                 'log10':False,
                 'distribution_type':'normal',
                 'scan_type':'scan',
                 #scan object specific (for scan and random_sampling scan_types)
                 'variable':self.GMQ.get_IC_cns().keys()[0],
                 'scheduled':True,
                 'save':'overwrite',
                 'clear_scans':True,#if true, will remove all scans present then add new scan
                 'run':False}
                                  
                 
                     
        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for Scan'.format(i)
        options.update( kwargs) 
        self.kwargs=options
        
        
        #correct output_in_subtask and AsjestInitialConditions
        assert self.kwargs.get('output_in_subtask') in [False,True,'false','true']
        assert self.kwargs.get('adjust_initial_conditions') in [False,True,'false','true']
        assert self.kwargs.get('log10') in [False,True,'false','true'],'{} is not either \'false\' or \'true\''.format(self.kwargs.get('log10'))
        
        if self.kwargs.get('output_in_subtask')==False:
            self.kwargs['output_in_subtask']=str(0)
        else:
            self.kwargs['output_in_subtask']=str(1)
            
        if self.kwargs.get('adjust_initial_conditions')==False:
            self.kwargs['adjust_initial_conditions']=str(0)
        else:
            self.kwargs['adjust_initial_conditions']=str(1)
        
        if self.kwargs.get('log10')==False:
            self.kwargs['log10']=str(0)
        else:
            self.kwargs['log10']=str(1)
            
            
        self.kwargs = Bool2Str(self.kwargs).convert_dct()
        
        subtasks=['steady_state','time_course',
                   'metabolic_control_nalysis',
                   'lyapunov_exponents',
                   'optimiztion','parameter_estimation',
                   'sensitivities','linear_noise_approximation',
                   'cross_section','time_scale_separation_analysis']
                   
        report_types=[None,'profilelikelihood','time_course','parameter_estimation', 
                      'multi_parameter_estimation', 'profilelikelihood2']
        dist_types=['normal','uniform','poisson','gamma']
        scan_types=['scan','repeat','random_sampling']
        quantity_type_list=['particle_number','concentration']
        
                   
        assert self.kwargs.get('subtask') in subtasks                   
        assert self.kwargs.get('report_type') in report_types,'{} is not in {}'.format(self['report_type'],report_types)
        assert self.kwargs.get('distribution_type') in dist_types
        assert self.kwargs.get('scan_type') in scan_types
        assert self.kwargs.get('quantity_type') in quantity_type_list
        assert self.kwargs.get('scheduled') in [True,False,'true','false']
        assert self.kwargs.get('clear_scans') in [True,False,'true','false']
        assert self.kwargs.get('run') in [True,False,'true','false','SGE']


        #numericify the some keyword arguments
        subtask_numbers=[0,1,6,7,4,5,9,12,11,8]
        for i in zip(subtasks,subtask_numbers):
            if i[0]==self.kwargs['subtask']:
                self.kwargs['subtask']=str(i[1])
        
        #numericidy type keywork arguments 
        scan_type_numbers=[1,0,2]
        LOG.debug('kwargs[scan_type is: {}'.format(self.kwargs['scan_type']))
        for i in zip(scan_types,scan_type_numbers):
            LOG.debug('scan type to number tuple: {}'.format(i))
            if i[0]==self.kwargs['scan_type']:
                self.kwargs['scan_type']=str(i[1])   
                
        dist_types_numbers=[0,1,2,3]
        for i in zip(dist_types,dist_types_numbers):
            if i[0]==self.kwargs['distribution_type']:
                self.kwargs['distribution_type']=str(i[1])    
                
        assert self.kwargs.get('variable') in self.GMQ.get_IC_cns().keys() or self.GMQ.get_global_quantities_cns().keys() or self.GMQ.get_local_kinetic_parameters_cns()
        
        #convert what needs to be a string to a string
        self.kwargs['output_in_subtask']=str(self.kwargs['output_in_subtask'])
        self.kwargs['adjust_initial_conditions']=str(self.kwargs['adjust_initial_conditions'])
        self.kwargs['number_of_steps']=str(self.kwargs['number_of_steps'])
        self.kwargs['maximum']=str(self.kwargs['maximum'])
        self.kwargs['minimum']=str(self.kwargs['minimum'])
        self.kwargs['log10']=str(self.kwargs['log10'])

        assert isinstance(self.kwargs.get('number_of_steps'),(float,int,str))
        assert isinstance(self.kwargs.get('maximum'),(float,int,str))
        assert isinstance(self.kwargs.get('minimum'),(float,int,str))
        
        if isinstance(self.kwargs.get('number_of_steps'),(float,int)):
            self.kwargs['number_of_steps']=str(self.kwargs.get('number_of_steps'))
            
        if isinstance(self.kwargs.get('maximum'),(float,int)):
            self.kwargs['maximum']=str(self.kwargs.get('maximum'))
            
        if isinstance(self.kwargs.get('minimum'),(float,int)):
            self.kwargs['minimum']=str(self.kwargs.get('minimum'))

#        if self.kwargs.get('report_type')=='time_course':
#            self.kwargs['report_type']='time-course'
        write_to_file_list=['duplicate','overwrite',False]
        assert self.kwargs.get('save') in write_to_file_list,'{} not in {}'.format(self.kwargs.get('save'),write_to_file_list)
        
        if self.kwargs.get('clear_scans')==True:
            self.copasiML=self.remove_scans()
            self.copasiML=self.save()    ##extra save - is this needed. Yes, I've checked - do not remove!
        self.copasiML=self.define_report()
        self.copasiML=self.create_scan()
        self.copasiML=self.set_scan_options()
        self.copasiML=self.save()
        self.run()
        
    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]

    def __setitem__(self,key,value):
        self.kwargs[key] = value
            
    def save(self):
        self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML
                
        
    def define_report(self):
        '''
        
        '''
        logging.debug('defining report')
        self.report_dict={}
        self.report_dict['metabolites']=self.kwargs.get('metabolites')
        self.report_dict['global_quantities']=self.kwargs.get('global_quantities')
        self.report_dict['quantity_type']=self.kwargs.get('quantity_type')
        self.report_dict['report_name']=self.kwargs.get('report_name')
        self.report_dict['append']=self.kwargs.get('append')
        self.report_dict['confirm_overwrite']=self.kwargs.get('confirm_overwrite')
        self.report_dict['save']=self.kwargs.get('save')
        self.report_dict['variable']=self.kwargs.get('variable')
        self.report_dict['report_type']=self.kwargs.get('report_type')
        R= Reports(self.copasi_file,**self.report_dict)

        return R.copasiML
        
        
    def get_report_key(self):
        '''
        
        '''
        #ammend the time course option
        if self.kwargs.get('report_type').lower()=='time_course':
            self.kwargs['report_type']='time-course'
        key=None
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfReports'):
            if i.attrib['name'].lower()==self.kwargs.get('report_type').lower():
                key=i.attrib['key']
        if key==None:
            raise Errors.ReportDoesNotExistError('Report doesn\'t exist. Check to see if you have either defined the report manually or used the pycopi.Reports class')
        return key
    
    def create_scan(self):
        '''
        need to find a report key which corresponds to the report we want to use
        '''
        #get cn value
        if self.kwargs.get('variable') in self.GMQ.get_IC_cns().keys():
            if self.kwargs.get('quantity_type')=='concentration':
                cn= self.GMQ.get_IC_cns()[self.kwargs.get('variable')]['cn']+',Reference=InitialConcentration'
            elif self.kwargs.get('quantity_type')=='particle_number':
                cn= self.GMQ.get_IC_cns()[self.kwargs.get('variable')]['cn']+',Reference=InitialParticleNumber'
        elif self.kwargs.get('variable') in self.GMQ.get_global_quantities_cns().keys():
            cn= self.GMQ.get_global_quantities_cns()[self.kwargs.get('variable')]['cn']+',Reference=InitialValue'
        elif self.kwargs.get('variable') in self.GMQ.get_local_kinetic_parameters_cns().keys():
            cn =self.GMQ.get_local_kinetic_parameters_cns()[self.kwargs.get('variable')]['cn']+',Reference=Value'

        
        number_of_steps_attrib={'type': 'unsignedInteger', 'name': 'Number of steps', 'value': self.kwargs['number_of_steps']}
        scan_item_attrib={'type': 'cn', 'name': 'Object', 'value': cn}
        type_attrib={'type': 'unsignedInteger', 'name': 'Type', 'value': self.kwargs['scan_type']}
        maximum_attrib={'type': 'float', 'name': 'Maximum', 'value': self.kwargs['maximum']}
        minimum_attrib={'type': 'float', 'name': 'Minimum', 'value': self.kwargs['minimum']}
        log_attrib={'type': 'bool', 'name': 'log', 'value': self.kwargs['log10']}
        dist_type_attrib={'type': 'unsignedInteger', 'name': 'Distribution type', 'value': self.kwargs['distribution_type']}
        scanItem_element=etree.Element('ParameterGroup',attrib={'name':'ScanItem'})
        
        ## regular scan
        if self.kwargs['scan_type']=='1':
            etree.SubElement(scanItem_element,'Parameter',attrib=number_of_steps_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=scan_item_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=type_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=maximum_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=minimum_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=log_attrib)
        ## repeat scan 
        elif self.kwargs['scan_type']=='0':
            etree.SubElement(scanItem_element,'Parameter',attrib=number_of_steps_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=type_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=scan_item_attrib)
        ## distribution scan
        elif self.kwargs['scan_type']=='2':
            etree.SubElement(scanItem_element,'Parameter',attrib=number_of_steps_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=type_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=scan_item_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=minimum_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=maximum_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=log_attrib)
            etree.SubElement(scanItem_element,'Parameter',attrib=dist_type_attrib)
        query='//*[@name="ScanItems"]'
        for i in self.copasiML.xpath(query):
            i.append(scanItem_element)
        return self.copasiML


        
    def set_scan_options(self):
        report_attrib={'append': self.kwargs.get('append'), 
                       'target': self.kwargs.get('report_name'), 
                       'reference': self.get_report_key(),
                       'confirmOverwrite': self.kwargs.get('confirm_overwrite')}
        
        LOG.debug('output during subtask value is: {}'.format(self.kwargs['output_in_subtask']))
#        LOG.debug()
        subtask_attrib={'type': 'unsignedInteger', 'name': 'Subtask', 'value': self.kwargs.get('subtask')}
        output_in_subtask_attrib={'type': 'bool', 'name': 'Output in subtask', 'value': self.kwargs['output_in_subtask']}
        adjust_initial_conditions_attrib={'type': 'bool', 'name': 'Adjust initial conditions', 'value': self.kwargs.get('adjust_initial_conditions')}
        scheduled_attrib={'scheduled': self.kwargs.get('scheduled'), 'updateModel': self.kwargs.get('update_model')}

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
        R=Run(self.copasi_file,task='scan',mode=self.kwargs.get('run'))
        #
        # if self.kwargs.get('run')==False:
        #     return None
        # elif self.kwargs.get('run')==True:
        #     return R
        # elif self.kwargs.get('run')=='SGE':
        #     return R
#==============================================================================            
class Run():
    '''
    run a copasi file using CopasiSE. run will deactivate all tasks from 
    being executable via CopasiSE then activate the task you want to run, 
    then run it. 
    
    copasi_file:
        The copasi file you want to run 
    
    **kwargs:
    
        task:
            Any valid copasi task. Default=time_course. Options are 
            ['steady_state','time_course','scan','fluxmode','optimization',
            'parameter_estimation','metaboliccontrolanalysis','lyapunovexponents',
            'timescaleseparationanalysis','sensitivities','moieties',
            'crosssection','linearnoiseapproximation']
            
        save:
            Either False,'duplicate' or 'overwrite'. Should probably remain 
            on 'overwrite', the default. 
            
        mode:
            True, False,'multiprocess', or 'SGE'. Default is True but can be turned off if you 
            want to uncheck all executable boxes then check the task executable
            
        max_time:
            Default None. Max time in seconds for copasi to be allowed to run
    '''
    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML
        self.GMQ=GetModelQuantities(self.copasi_file)
        self.SGE_job_file=os.path.splitext(self.copasi_file)[0]+'.sh'

        options={'task':'time_course',
                 'save':'overwrite',
                 'mode':True,
                 'max_time':None}



        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for run'.format(i)
        options.update( kwargs)
        self.kwargs=options
        self.kwargs = Bool2Str(self.kwargs).convert_dct()


        tasks=['steady_state','time_course',
               'scan','fluxmode','optimization',
               'parameter_estimation','metaboliccontrolanalysis',
               'lyapunovexponents','timescaleseparationanalysis',
               'sensitivities','moieties','crosssection',
               'linearnoiseapproximation']



        if  self.kwargs.get('task') not in tasks:
            raise Errors.InputError('{} is not a valid task. Choose from {}'.format(self.kwargs.get('task'),tasks))
        if self.kwargs.get('max_time')!=None:
            if isinstance(self.kwargs.get('max_time'),(float,int))!=True:
                raise TypeError('max_time argument must be float or int')

        if self.kwargs.get('task')=='time_course':
            self.kwargs['task']='timecourse'

        elif self.kwargs.get('task')=='parameter_estimation':
            self.kwargs['task']='parameterfitting'

        elif self.kwargs.get('task')=='steady_state':
            self.kwargs['task']='steadystate'

        if os.path.isfile(self.copasi_file)!=True:
            raise Errors.FileDoesNotExistError('{} is not a file'.format(self.copasi_file))


        self.copasiML=self.set_task()
        self.save()
        if self.kwargs.get('mode')==True:
            try:
                self.run()
            except Errors.CopasiError:
                self.run_linux()
        elif self.kwargs.get('mode')=='SGE':
            self.submit_copasi_job_SGE()
        elif self.kwargs.get('mode')=='multiprocess':
            self.multi_run()



    def multi_run(self):
        def run(x):
            if os.path.isfile(x)!=True:
                raise Errors.FileDoesNotExistError('{} is not a file'.format(self.copasi_file))
            subprocess.Popen(['CopasiSE',self.copasi_file])
        Process(run(self.copasi_file))




    def set_task(self):
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            i.attrib['scheduled']="false" #set all to false
            if self.kwargs.get('task')== i.attrib['type'].lower():
                i.attrib['scheduled']="true"

        return self.copasiML

    def run(self):
        '''
        Process the copasi file using CopasiSE
        Must be Copasi version 16
        
        '''
        args=['CopasiSE',"{}".format(self.copasi_file)]
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
#        os.remove(self.SGE_job_file)
        
    def save(self):
        self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML


    def save_dep(self):
        if self.kwargs.get('save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML


        
class Run2():
    '''
    run a copasi file using CopasiSE. run will deactivate all tasks from 
    being executable via CopasiSE then activate the task you want to run, 
    then run it. 
    
    copasi_file:
        The copasi file you want to run 
    
    **kwargs:
    
        task:
            Any valid copasi task. Default=time_course. Options are 
            ['steady_state','time_course','scan','fluxmode','optimization',
            'parameter_estimation','metaboliccontrolanalysis','lyapunovexponents',
            'timescaleseparationanalysis','sensitivities','moieties',
            'crosssection','linearnoiseapproximation']
            
        save:
            Either False,'duplicate' or 'overwrite'. Should probably remain 
            on 'overwrite', the default. 
            
        mode:
            True, False,'multiprocess', or 'SGE'. Default is True but can be turned off if you 
            want to uncheck all executable boxes then check the task executable
            
        max_time:
            Default None. Max time in seconds for copasi to be allowed to run
    '''
    def __init__(self,copasi_file,**kwargs):
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML
        self.GMQ=GetModelQuantities(self.copasi_file)
        self.SGE_job_file=os.path.splitext(self.copasi_file)[0]+'.sh'

        options={'task':'time_course',
                 'save':'overwrite',
                 'mode':True,
                 'max_time':None}



        #values need to be lower case for copasiML
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for run'.format(i)
        options.update( kwargs)
        self.kwargs=options
        self.kwargs = Bool2Str(self.kwargs).convert_dct()



        tasks=['steady_state','time_course',
               'scan','fluxmode','optimization',
               'parameter_estimation','metaboliccontrolanalysis',
               'lyapunovexponents','timescaleseparationanalysis',
               'sensitivities','moieties','crosssection',
               'linearnoiseapproximation']



        if  self.kwargs.get('task') not in tasks:
            raise Errors.InputError('{} is not a valid task. Choose from {}'.format(self.kwargs.get('task'),tasks))
        if self.kwargs.get('max_time')!=None:
            if isinstance(self.kwargs.get('max_time'),(float,int))!=True:
                raise TypeError('max_time argument must be float or int')

        if self.kwargs.get('task')=='time_course':
            self.kwargs['task']='timecourse'

        elif self.kwargs.get('task')=='parameter_estimation':
            self.kwargs['task']='parameterfitting'

        elif self.kwargs.get('task')=='steady_state':
            self.kwargs['task']='steadystate'

        if os.path.isfile(self.copasi_file)!=True:
            raise Errors.FileDoesNotExistError('{} is not a file'.format(self.copasi_file))


        self.copasiML=self.set_task()
        self.save()
        if self.kwargs.get('mode')==True:
            try:
                self.run()
            except Errors.CopasiError:
                self.run_linux()
        elif self.kwargs.get('mode')=='SGE':
            self.submit_copasi_job_SGE()
        elif self.kwargs.get('mode')=='multiprocess':
            self.multi_run()

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]

    def __setitem__(self,key,value):
        self.kwargs[key] = value
        
        
    def multi_run(self):
        def run(x):
            if os.path.isfile(x)!=True:
                raise Errors.FileDoesNotExistError('{} is not a file'.format(x))
            subprocess.Popen(['CopasiSE',x])
            os.system('CopasiSE {}'.format(x))
        Process(run(self.copasi_file))


    def set_task(self):
        for i in self.copasiML.find('{http://www.copasi.org/static/schema}ListOfTasks'):
            i.attrib['scheduled']="false" #set all to false
            if self.kwargs.get('task')== i.attrib['type'].lower():
                i.attrib['scheduled']="true"

        return self.copasiML

    def run(self):
        '''
        Process the copasi file using CopasiSE
        Must be Copasi version 16
        
        '''
        try:
            LOG.info('Running... {}'.format(self.copasi_file))
            args=["CopasiSE","{}".format(self.copasi_file)]
            p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
            output,err= p.communicate()
            d={}
            d['output']=output
            d['error']=err
            if err!='':
               raise Errors.CopasiError('Failed with Copasi error: \n\n'+d['error'])
            return d['output']
        except Errors.CopasiError:
            LOG.warning('Failed to run using subprocess.Popen(). Trying with os.system')
            self.run_with_os_system()

    def run_with_check_call(self):
        print self.copasi_file
        subprocess.check_call(["CopasiSE",r"{}".format(self.copasi_file) ])

    def run_with_os_system(self):
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
        self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML


    def save_dep(self):
        if self.kwargs.get('save')=='duplicate':
            self.CParser.write_copasi_file(self.kwargs.get('OutputML'),self.copasiML)
        elif self.kwargs.get('save')=='overwrite':
            self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML

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
            True or False, if True will overwrite the filename. If False
            write new file to new_path. If for_pruning a dataframe this argument is
            ignored. 
            
        new_path: 
            When replace='false 'new_path' is the output filename. Ignored when 
            for_pruning is a pandas dataframe.
        

    '''
    def __init__(self,for_pruning,replace=False,new_path=None):
        self.for_pruning=for_pruning
        self.replace=replace
        
#        assert self.mode in ['singlePE','multiPE,'time_course']
        
        if replace not in [True,False,'true','false']:
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
            if self.replace==True:
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
        
        if isinstance(self.experiment_files, str):
            self.experiment_files = [self.experiment_files]
        
        
        ## Pickle file to store directories of sub copasi files
        self.copasi_file_pickle=os.path.join(os.path.dirname(self.copasi_file),'sub_copasi_file.pickle')
        default_results_directory = os.path.join(os.path.dirname(self.copasi_file),'MultipleParameterEstimationResults')
        options={'run':'multiprocess',
                 'results_directory':default_results_directory,
                 'copy_number':1,
                 'pe_number':3,
                 'report_name':None,
                 'metabolites':self.GMQ.get_IC_cns().keys(),
                 'global_quantities':self.GMQ.get_global_quantities().keys(),
                 'local_parameters': self.GMQ.get_local_kinetic_parameters_cns().keys(),
                 'quantity_type':'concentration',
                 'append': False, 
                 'confirm_overwrite': False,
                 'config_filename':None,
                 'overwrite_config_file':False,
                 'prune_headers':True,
                 'update_model':False,
                 'randomize_start_values':True,
                 'create_parameter_sets':False,
                 'calculate_statistics':False,
                 'use_config_start_values':False,
                 #method options
                 'method':'GeneticAlgorithm',
                 #'DifferentialEvolution',
                 'number_of_generations':200,
                 'population_size':50,
                 'random_number_generator':1,
                 'seed':0,
                 'pf':0.475,
                 'iteration_limit':50,
                 'tolerance':0.00001,
                 'rho':0.2,
                 'scale':10,
                 'swarm_size':50,
                 'std_deviation':0.000001,
                 'number_of_iterations':100000,
                 'start_temperature':1,
                 'cooling_factor':0.85,
                 #experiment definition options
                 #need to include options for defining multiple experimental files at once
                 'row_orientation':[True]*len(self.experiment_files),
                 'experiment_type':['timecourse']*len(self.experiment_files),
                 'first_row':[str(1)]*len(self.experiment_files),
                 'normalize_weights_per_experiment':[True]*len(self.experiment_files),
                 'row_containing_names':[str(1)]*len(self.experiment_files),
                 'separator':['\t']*len(self.experiment_files),
                 'weight_method':['mean_squared']*len(self.experiment_files),
                 'save':'overwrite',  
                 'scheduled':False,
                 'lower_bound':0.000001,
                 'upper_bound':1000000,
                 'plot':False,
                 'output_in_subtask':False,
                 'line_width':4,
                 #graph features
                 'font_size':22,
                 'axis_size':15,
                 'extra_title':None,
                 'show':False,
                 'savefig':False,
                 'title_wrap_size':30,
                 'ylimit':None,
                 'xlimit':None,
                 'dpi':125,
                 'xtick_rotation':35,
                 'marker_size':4,
                 'legend_loc':'best'}
                 
                 
                 
        
        for key in kwargs.keys():
            if key not in options.keys():
                raise Errors.InputError('{} is not a keyword argument for RunMutliplePEs'.format(key))
        options.update( kwargs) 
        self.kwargs=options       
#        self.kwargs = Bool2Str(self.kwargs).convert_dct()
        self._do_checks()
        self._create_defaults()
        self._create_output_directory()
        
        ## create copy of kwargs and remove those that we do not wnt to pass to ParameterEstimation
        self.PE_dct=deepcopy(self.kwargs)
        del self.PE_dct['results_directory']
        del self.PE_dct['copy_number']
        del self.PE_dct['pe_number']
        del self.PE_dct['run']
        del self.PE_dct['output_in_subtask']


        self.report_files=self.enumerate_PE_output()
        LOG.debug('Create an instance of ParameterEstimation')
        self.PE=ParameterEstimation(self.copasi_file,self.experiment_files,**self.PE_dct)

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]

    def __setitem__(self,key,value):
        self.kwargs[key] = value
        
    def format_results(self):
        """
        Copasi output does not have headers. This function 
        gives PE data output headers
        """
        try:
            cps_keys = self.sub_copasi_files.keys()
        except AttributeError:
            self.setup()
            cps_keys = self.sub_copasi_files.keys()
        report_keys = self.report_files.keys()
        for i in range(len(self.report_files)):
            try:
                FormatPEData(self.sub_copasi_files[cps_keys[i]], self.report_files[report_keys[i]],
                         report_type='multi_parameter_estimation')
            except Errors.InputError:
                LOG.warning('{} is empty. Cannot parse. Skipping this file'.format(self.report_files[report_keys[i]]))
                continue
        return self.report_files

    def setup(self):
        '''
        Analogous to the set_up method of the ParameterEstimation class but this time
        setup both the PE and Scan tasks       
        '''
        
        self.PE.setup()
        self.sub_copasi_files=self.copy_copasi()
        self._setup_scan()
    

        
    def set_up_dep(self):
        '''
        Analogous to the set_up method of the ParameterEstimation class but this time
        setup both the PE and Scan tasks       
        '''
        LOG.warning('set_up method is deprecated. Use setup() method instead')
        self.PE.set_up()
        self.sub_copasi_files=self.copy_copasi()
        self._setup_scan()
 
    def run(self):
        '''
        '''
        ##load cps from pickle in case run not being use straignt after set_up
        if self.kwargs['run']=='SGE':
            try:
                check_call('qhost')
            except Errors.NotImplementedError:
                LOG.warning('Attempting to run in SGE mode but SGE specific commands are unavailable. Switching to \'multiprocess\' mode')
                self.kwargs['run']='multiprocess'
        if os.path.isfile(self.copasi_file_pickle):
            with open(self.copasi_file_pickle) as f:
                self.sub_copasi_files=pickle.load(f)
        for i in self.sub_copasi_files:
            LOG.info('running model: {}'.format(i))
            Run(self.sub_copasi_files[i],mode=self.kwargs['run'],task='scan')
                    
    def copy_copasi(self):
        '''
        Copy copasi files m times to run separetly on a single 
        computer
        
        returns:
            dict[model_number]=cps_file
        '''
        LOG.debug('Copying copasi file {} times'.format(self.kwargs['copy_number']))
        sub_copasi_files_dct={}
        copasi_path,copasi_filename=os.path.split(self.copasi_file)
        for i in range(1,self.kwargs['copy_number']):
            new_cps=os.path.join(copasi_path,copasi_filename[:-4]+'_{}.cps'.format(str(i)))
            shutil.copy(self.copasi_file,new_cps)
            sub_copasi_files_dct[i]= new_cps
        sub_copasi_files_dct[0]=self.copasi_file
        
        with open(self.copasi_file_pickle,'w')as f:
            pickle.dump(sub_copasi_files_dct,f)
            
        return sub_copasi_files_dct                
            
    def write_config_template(self):
        '''
        
        '''
        LOG.debug('writing PE config template for model: {}'.format(self.copasi_file))
        LOG.debug('config_filename is {}'.format(self.PE.kwargs['config_filename']))
        self.PE.write_config_template()
        return self.PE['config_filename']
        
        
    ##void    
    def _setup_scan(self):
        '''
        Set up n repeat items with number_of_steps repeats of parameter estimation
        Set run to false as we want to use the multiprocess mode of the run class
        to process all m files at once in CopasiSE
        
        Remember scan needs iterating over because each file needs an unique report
        name
        '''

        q=Queue.Queue()
        for num in range(self.kwargs['copy_number']):
            LOG.debug('setting up scan for model : {}'.format(self.sub_copasi_files[num]))
            t=threading.Thread(target=self._setup1scan,
                               args =  (q,self.sub_copasi_files[num] , self.report_files[num])  )
            t.daemon=True
            t.start()
            time.sleep(0.1)
            
        s=q.get()
        ## Since this is being executed in parallel sometimes
        ## we get process clashes. Not sure exactly whats going on
        ## but introducing a small delay seems to fix
        time.sleep(0.1)


            
    ## void
    def _setup1scan(self,q,cps,report):
        '''
        
        '''
#        LOG.info('setting up scan for model number {}'.format(num))
        start=time.time()
        q.put(Scan(cps,
             scan_type='repeat', #set up repeat item under scan. 
             number_of_steps=self.kwargs['pe_number'], #run the parameter estimation task 3 times
             subtask='parameter_estimation', #this is the default, but included here for demonstration anyway
             report_type='multi_parameter_estimation', ## report automatically set up within copasi. 
             report_name=report,
             run=False,#run the scan task automatically in the background
             append = self.kwargs['append'],
             confirm_overwrite = self.kwargs['confirm_overwrite'],
             output_in_subtask = self.kwargs['output_in_subtask']) )
        LOG.debug('Setup Took {} seconds'.format(time.time() - start))

    ##void
    def _create_defaults(self):
        '''
        
        '''
        default_report_name=os.path.join(os.path.dirname(self.copasi_file),'ParameterFit.txt')
        if self.kwargs['report_name']==None:
            LOG.debug('Using default report name:\n{}'.format(default_report_name))
            self.kwargs['report_name']=default_report_name
                       
        results_directory_default=os.path.join(os.path.dirname(self.copasi_file),'MultiplePEResults')
        if self.kwargs['results_directory']==None:
            LOG.debug('Using default results_directory:\n{}'.format(results_directory_default))
            self.kwargs['results_directory']=results_directory_default        
                       
        if self.kwargs['config_filename']==None:
            LOG.debug('config_filename is None. Reassigning config_filename')
            self.kwargs['config_filename']=os.path.join(os.path.dirname(self.copasi_file),'PEConfigFile.xlsx')
        
        if self.kwargs['config_filename']!=None:
            if os.path.isabs(self.kwargs['config_filename'])==False:
                self.kwargs['config_filename']=os.path.join(os.path.dirname(self.copasi_file),self.kwargs['config_filename'])
                
                       

    
    ##void             
    def _do_checks(self):
        '''
        
        '''
        run_arg_list=['multiprocess','SGE']
        if self.kwargs['run'] not in run_arg_list:
            raise Errors.InputError('run needs to be one of {}'.format(run_arg_list))
        if isinstance(self.kwargs['copy_number'],int)!=True:
            raise Errors.InputError('copy_number argument is of type int')
            
        if isinstance(self.kwargs['pe_number'],int)!=True:
            raise Errors.InputError('pe_number argument is of type int')    
            
        if self.kwargs['results_directory']==None:
            self.kwargs['results_directory']='MultipleParameterEsimationAnalysis'
        self.kwargs['results_directory']=os.path.abspath(self.kwargs['results_directory'])
            
    
    def _create_output_directory(self):
        '''
        
        '''
        LOG.debug('creating a directory for analysis in : \n\n{}'.format(self.kwargs['results_directory']))
        if os.path.isdir(self.kwargs['results_directory'])!=True:
            os.mkdir(self.kwargs['results_directory'])
                
            
    
    def enumerate_PE_output(self):
        '''
        Create a filename for each file to collect PE results
        
        Returns:
            dct['model_copy_number]=enumerated_report_name
        '''
        LOG.debug('Enumerating PE report files')
        dct={}
        dire,fle=os.path.split(self.kwargs['report_name'])
        for i in range(self.kwargs['copy_number']):
            new_file=os.path.join(self.kwargs['results_directory'],
                                  fle[:-4]+'{}.txt'.format(str(i)))
            dct[i]=new_file
        return dct
    


class MultiModelFit():
    '''
    Coordinate a systematic multi model fitting parameter estimation and 
    compare results using AIC/BIC. 
    
    Usage: 
        1):
            Setup a new folder containing all models that you would like to fit
            and all data you would like to fit to the model. Do not have any 
            other text or csv files in this folder as python will try and setup
            fits for them. Data files must have 'Time' in the left column
            and each subsequent column must be titled with a variable name mapping 
            to a model entity exactly (watch out for trailing spaces). It is 
            reccommended to supply a plain text file detailing the common 
            component between the models and what is different between each model. 
            This however should not be saved as a .txt file or python will 
            try and map it to the models. Just save the 'ReadMe' without an extention
            to avoid this problem.
            
                i.e.:
                    ./project_dir
                        --Exp data 1
                        --Exp data n
                        --model1.cps
                        --model2.cps

        2):
            Instantiate instance of the MultimodelFit class with all relevant 
            keywords. Relevant keywords are described in the ParameterEstimation
            or runMultiplePEs classes. As non-optional arguments this takes the absolute path 
            to the project directory that you created in step 1. 
            Python automatically creates subdirectories  for each model in your 
            model selection problem and maps all data files in the main directory 
            to each of the models. 
        3):
            Use the write_item_template() method to create a spreadsheet containing
            your a config file with it instructions. By default, all ICs and all kinetic (global or local)
            parameters are included. Delete entries that you would like to keep fixed. Do not 
            modify the last columns which contain xml code for that variable. 
        4): 
            Once each model folder has a config file specific for that model
            use the setup()() method. Then open one of the child copasi files
            in order to check that things are configured how you'd like them before 
            using the run() method. 
            
            
        **kwargs:
            copy_number:
                Default = 1. This is how many times to copy a copasi file before
                running the parameter estimation on each model. 
            pe_number:
                Default = 3. How many parameter estimations to perform in one model. 
                i.e. a repeat scan task is automatically configured. 
                
            All other kwargs are described in runMultiplePEs or ParameterEstimation
    '''
    def __init__(self,project_config,**kwargs):
        self.project_dir=project_config
#        self.config_filename=config_filename
        self.do_checks()
        self.cps_files,self.exp_files=self.read_fit_config()
        
#        if self.config_filename==None:
#            self.config_filename=os.path.join(self.project_dir,'PEConfigFile.xlsx')
        
        options={'run':'multiprocess',
                 'copy_number':1,
                 'pe_number':3,
                 'report_name':None,
                 'results_directory':None,
                 ##default parameters for ParameterEstimation
                 'method':'GeneticAlgorithm',
                 'plot':False,
                 'quantity_type':'concentration',
                 'append': False, 
                 'confirm_overwrite': False,
                 'config_filename':'PEConfigFile.xlsx',
                 'overwrite_config_file':False,
                 'prune_headers':True,
                 'update_model':False,
                 'randomize_start_values':True,
                 'create_parameter_sets':False,
                 'calculate_statistics':False,
                 'use_config_start_values':False,
                 #method options
                 #'DifferentialEvolution',
                 'number_of_generations':200,
                 'population_size':50,
                 'random_number_generator':1,
                 'seed':0,
                 'pf':0.475,
                 'iteration_limit':50,
                 'tolerance':0.0001,
                 'rho':0.2,
                 'scale':10,
                 'swarm_size':50,
                 'std_deviation':0.000001,
                 'number_of_iterations':100000,
                 'start_temperature':1,
                 'cooling_factor':0.85,
                 #experiment definition options
                 #need to include options for defining multiple experimental files at once
                 'row_orientation':[True]*len(self.exp_files),
                 'experiment_type':['timecourse']*len(self.exp_files),
                 'first_row':[str(1)]*len(self.exp_files),
                 'normalize_weights_per_experiment':[True]*len(self.exp_files),
                 'row_containing_names':[str(1)]*len(self.exp_files),
                 'separator':['\t']*len(self.exp_files),
                 'weight_method':['mean_squared']*len(self.exp_files),
                 'save':'overwrite',  
                 'scheduled':False,
                 'lower_bound':0.000001,
                 'upper_bound':1000000}
        
        for key in kwargs.keys():
            if key not in options.keys():
                raise Errors.InputError('{} is not a keyword argument for MultiModelFit'.format(key))
        options.update( kwargs) 
        self.kwargs=options    
        
        
        self.sub_cps_dirs=self.create_workspace()
        self.RMPE_dct=self.instantiate_run_multi_PEs_class()
        self.results_folder_dct=self.get_output_directories()

    def __getitem__(self,key):
        if key not in self.kwargs.keys():
            raise TypeError('{} not in {}'.format(key,self.kwargs.keys()))
        return self.kwargs[key]

    def __setitem__(self,key,value):
        self.kwargs[key] = value
        
    def instantiate_run_multi_PEs_class(self):
        '''
        pass correct arguments to the runMultiplePEs class in order
        to instantiate a runMultiplePEs instance for each model. 
        
        Reutrns:
            dict[model_filename]=runMultiplePEs_instance
        '''
        LOG.debug('instantiating an instance of runMultiplePEs for each model')
        dct={}
            
        for cps_dir in self.sub_cps_dirs:
            os.chdir(cps_dir)
            if os.path.isabs(self.kwargs['config_filename']):
                self.kwargs['config_filename']=os.path.split(self.kwargs['config_filename'])[1]
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
            LOG.debug('\t\t'+self.RMPE_dct[RMPE].kwargs['results_directory'])
            output_dct[RMPE]=self.RMPE_dct[RMPE].kwargs['results_directory']
        return output_dct
    
    #void
    def write_config_template(self):
        '''
        A class to write a config file template for each 
        model in the analysis. Calls the corresponding
        write_config_template from the runMultiplePEs class
        ===returns=== 
        list of config files
        '''
        conf_list=[]
        for RMPE in self.RMPE_dct:
            f = self.RMPE_dct[RMPE].write_config_template()
            conf_list.append(f)
        return conf_list 
    
    def setup(self):
        '''
        A user interface class which calls the corresponding
        method (setup) from the runMultiplePEs class per model. 
        Perform the ParameterEstimation.setup() method on each model. 
        
        '''
        for RMPE in self.RMPE_dct:
            self.RMPE_dct[RMPE].setup()
            
    def set_up_dep(self):
        '''
        A user interface class which calls the corresponding
        method (set_up) from the runMultiplePEs class per model. 
        Perform the ParameterEstimation.set_up() method on each model. 
        
        '''
        LOG.warning('The set_up method is deprecated. Use setup() method instead')
        for RMPE in self.RMPE_dct:
            self.RMPE_dct[RMPE].set_up()


    def run(self):
        '''
        A user interface class which calls the corresponding
        method (run) from the runMultiplePEs class per model. 
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
        self.wd=self.project_dir
        
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
    
    
    def format_data(self):
        """
        Method for giving appropiate headers to parameter estimation data
        """
        for RMPE in self.RMPE_dct:
            self.RMPE_dct[RMPE].format_results()
#        [RMPE.format_data() for RMPE in self.RMPE_dct[RMPE]]
            
        
        

class InsertParameters():
    '''
    Insert parameters from a file, dictionary or a pandas dataframe into a copasi
    file. 
    
    Positional Arguments:
    
        copasi_file:
            The copasi file you want to enter parameters into
    
    **Kwargs
        index:
            index of parameter estimation run to input into the copasi file. 
            The index is ordered by rank of best fit, with 0 being the best.
            Default=0            
            
        quantity_type:
            Either 'particle_number' or 'concentration'. Default='concentration'
            
        report_name;
            Unused. Delete?
            
        save:
            either False,'overwrite' or 'duplicate',default=overwrite
                
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
        
    '''
    def __init__(self,copasi_file,**kwargs):
        '''
        coapsi_file = file you want to insert
        kwargs:
            index: If not specified default to -1
                    can be int or list of ints
        '''
        self.copasi_file=copasi_file
        self.CParser=CopasiMLParser(self.copasi_file)
        self.copasiML=self.CParser.copasiML 
        self.GMQ=GetModelQuantities(self.copasi_file)

        default_report_name=os.path.split(self.copasi_file)[1][:-4]+'_PE_results.txt'
        options={#report variables
                 'metabolites':self.GMQ.get_IC_cns().keys(),
                 'global_quantities':self.GMQ.get_global_quantities().keys(),
                 'quantity_type':'concentration',
                 'report_name':default_report_name,
                 'save':'overwrite',
                 'index':0,
                 'parameter_dict':None,
                 'df':None,
                 'parameter_path':None,
                 }
                     
        for i in kwargs.keys():
            assert i in options.keys(),'{} is not a keyword argument for InsertParameters'.format(i)
        options.update( kwargs) 
        self.kwargs=options
        self.kwargs = Bool2Str(self.kwargs).convert_dct()
        
        LOG.debug('These are kwargs {}'.format(self.kwargs))
        
#        assert os.path.exists(self.parameter_path),'{} doesn\'t exist'.format(self.parameter_path)
        assert self.kwargs.get('quantity_type') in ['concentration','particle_numbers']
        if self.kwargs.get('parameter_dict') != None:
            if isinstance(self.kwargs.get('parameter_dict'),dict)!=True:
                raise Errors.InputError('Argument to \'parameter_dict\' keyword needs to be of type dict')
            for i in self.kwargs.get('parameter_dict').keys():
                if i not in self.GMQ.get_all_model_variables().keys():
                    raise Errors.InputError('Parameter \'{}\' is not in your model. \n\nThese are in your model:\n{}'.format(i,sorted(self.GMQ.get_all_model_variables().keys())))
                
        if self.kwargs.get('parameter_dict')==None and self.kwargs.get('parameter_path')==None and self.kwargs.get('df') is None:
            raise Errors.InputError('You need to give at least one of parameter_dict,parameter_path or df keyword arguments')
        
        assert isinstance(self.kwargs.get('index'),int)
                
            
        #make sure user gives the right number of arguments
        num=0
        if self.kwargs.get('parameter_dict')!=None:
            num+=1
        if self.kwargs.get('df') is not None:
            num+=1
        if self.kwargs.get('parameter_path')!=None:
            num+=1
        if num!=1:
            raise Errors.InputError('You need to supply exactly one of parameter_dict,parameter_path or df keyord argument. You cannot give two or three.')
        
        self.parameters=self.get_parameters()
        self.parameters= self.replace_gl_and_lt()
#        self.insert_locals()
        self.insert_all()
        #change

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
            raise Errors.ParameterInputError('''The parameters in your parameter estimation data are not in your model.\
Please check the headers of your PE data are consistent with your model parameter names.''' )            

    def get_parameters(self):
        '''
        Get parameters depending on the type of input. 
        Converge on a pandas dataframe. 
        Columns = parameters, rows = parameter sets
        
        Use check parameter consistency to see
        whether headers have been pruned or not. If not try pruning them
        '''
        if self.kwargs.get('parameter_dict')!=None:
            assert isinstance(self.kwargs.get('parameter_dict'),dict),'The parameter_dict argument takes a Python dictionary'
            for i in self.kwargs.get('parameter_dict'):
                assert i in self.GMQ.get_all_model_variables().keys(),'{} is not a parameter. These are your parameters:{}'.format(i,self.GMQ.get_all_model_variables().keys())
            return pandas.DataFrame(self.kwargs.get('parameter_dict'),index=[0])
        
        if self.kwargs.get('parameter_path')!=None:
            PED=PEAnalysis.ParsePEData(self.kwargs.get('parameter_path'))
            if isinstance(self.kwargs.get('index'),int):
                return pandas.DataFrame(PED.data.iloc[self.kwargs.get('index')]).transpose()
            else: 
                return PED.data.iloc[self.kwargs.get('index')]
        if self.kwargs.get('df') is not None:
            df= pandas.DataFrame(self.kwargs.get('df').iloc[self.kwargs.get('index')]).transpose()
            self.check_parameter_consistancy(df)
        # except Errors.ParameterInputError:
        #     df=PruneCopasiHeaders(df).prune()
        #     self.check_parameter_consistancy(df)
        return df

    def insert_locals(self):
        '''
        
        '''
        ## get local parameters
        local=sorted(self.GMQ.get_local_kinetic_parameters_cns().keys())
        ## remove local parameters from complete list depending on whether
        ## user wants to insert anything for that parameter or not
        local= [i for i in self.parameters if i in local]
        LOG.debug('Local parameters being inserted into model: {}'.format(local))
        ## create a dict[parameter]=reactiontype dict to help
        ## navidate the xml
        local_dct={}
        for full_param in local:
            local_dct[full_param]={}
            k,v = re.findall(  '\((.*)\)\.(.*)', full_param ) [0]
            local_dct[full_param][k] = v
            
        LOG.debug('Constructing a dict of reaction:parameter for local parameters: {}'.format(local_dct))
        
        ## Iterate over all local parameters that we want to insert
        ## Identify the list of reactions ,match for the current reaction
        ## bore into that reaction to locate the locally defined rate constant
        ## match with the parameter then insert the str(float(*.)) representation
        ## of the parameter value into the value attribute for the constant
        ## element
        for key in local_dct:
            for reaction_name, parameter_name in local_dct[key].items():
                for element_tags in self.copasiML.iter():
                    if  element_tags.tag == '{http://www.copasi.org/static/schema}ListOfReactions':
                        for reaction in element_tags:
                            if reaction.attrib['name'] == reaction_name:
                                for reaction_element in reaction:
                                    if reaction_element.tag == '{http://www.copasi.org/static/schema}ListOfConstants':
                                        for constant_xml in reaction_element:
                                            if constant_xml.attrib['name'] == parameter_name:
                                                constant_xml.attrib['value'] = str(float(self.parameters['({}).{}'.format(reaction_name,parameter_name)]))
        return self.copasiML
    
    def assemble_state_values(self):
        """
        
        """
        LOG.debug('States:\t {}'.format( self.GMQ.get_state_template()))
        state_values = []
        count = 0
        for state in self.GMQ.get_state_template():
            #LOG.debug('assembling parameter {} out of {}'.format(count,len(self.GMQ.get_state_template())))
            count+=1
            model = re.findall('(Model)_',state)
            metab = re.findall('Metabolite',state)
            mod_value = re.findall('ModelValue',state)
            compartment = re.findall('Compartment',state)
            if model !=[]:
                LOG.debug('State {} is model'.format(state))
                assert metab == []
                assert mod_value == []
                assert compartment ==[]
                state_values.append(str(0))
                LOG.debug('Added 0 for first parameter in sequence')
            elif metab !=[]:
                LOG.debug('State {} is metab'.format(state))
                assert model == []
                assert mod_value == []
                assert compartment == []
                metab_name= self.GMQ.get_metabolites_object_reference()[state]
#                    print self.parameters[metab_name]
                metab =  self.GMQ.get_IC_cns()[metab_name]
                comp_vol = self.GMQ.get_IC_cns()[metab_name]['compartment_volume']
                
                metab_val = self.GMQ.get_IC_cns()[metab_name]['value']
                #LOG.debug('Metab dict for {}, \n\n{}'.format(state,self.GMQ.get_IC_cns()[metab_name]))
                
                if metab_name in self.parameters:
                    metab_val =  self.GMQ.convert_molar_to_particles(float(self.parameters[metab_name]),
                                                          self.GMQ.get_quantity_units(),
                                                          float(comp_vol))
                state_values.append(str(float(metab_val)))

            elif mod_value !=[]:
                LOG.debug('State {} is Global variable'.format(state))

                assert model == []
                assert metab == []
                assert compartment == []
                mod_value_name = self.GMQ.get_global_object_reference()[state]
                mod_value_value = self.GMQ.get_global_quantities()[mod_value_name]
                if mod_value_name in self.parameters.keys():
                    mod_value_value=str(float(self.parameters[mod_value_name]))
                state_values.append(mod_value_value)
                
            elif compartment != []:
                '''
                Warning: A potential bug may exist where if some metabolites are
                calculated before the compartment is changed then other after, 
                we'll get metabolites with inconsident volumes. This will be 
                rare as I don't generally estimate the compartment volumes 
                but if you are then this could be a problem. 
                '''
                assert model ==[]
                assert metab == []
                assert mod_value == []
                compartment_name = self.GMQ.get_compartment_object_reference()[state]
                compartment_value = self.GMQ.get_compartments()[compartment_name]['value']
                if compartment_name in self.parameters.keys():
                    compartment_value = str(float(self.parameters[compartment_name]))
                state_values.append(compartment_value)
                    
#        if len(state_values)!=len(self.GMQ.get_state_template()):
#            raise Exception('For some reason the number of state values does not equal the number of global + IC parameters in yoru model')
        return state_values

    def insert_ICs(self):
        IC=self.GMQ.get_IC_cns()
        for i in IC:
            query='//*[@cn="{}"]'.format( self.GMQ.get_IC_cns()[i]['cn'])
            for j in self.copasiML.xpath(query):
                if i in self.parameters.keys() and j.attrib['simulationType']=='reactions':
                    if self.kwargs.get('quantity_type')=='concentration':
                        particles=self.GMQ.convert_molar_to_particles(float(self.parameters[i]),self.GMQ.get_quantity_units(),float(IC[i]['compartment_volume']))#,self.GMQ.get_volume_unit())
##                        particles=self.parameters[i]
                    elif self.kwargs.get('quantity_type')=='particle_numbers':
                        particles=self.parameters[i]
                    j.attrib['value']=str(float(particles))
        return self.copasiML
    
    def insert_global_and_ICs(self):
        """
        
        """
        def reduce_str(y,z):
            return '{} {}'.format(y,z)
        values=reduce(reduce_str,self.assemble_state_values())
        query = '//*[@type="initialState"]'
        for i in self.copasiML.xpath(query):
            i.text = values
        return self.copasiML
                    
    def insert_global(self):
        glob= self.GMQ.get_global_quantities_cns().keys()
        for i in glob:
            query='//*[@cn="{}"]'.format( self.GMQ.get_global_quantities_cns()[i]['cn'])
            for j in self.copasiML.xpath(query):
                if i in self.parameters.keys() and j.attrib['SimulationType']!='assignment':
                    j.attrib['value']=str(float(self.parameters[i]))
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

        


    def replace_gl_and_lt(self):
        '''
        replace greater than and less than symbols for xML purposes
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
        self.copasiML = self.insert_global_and_ICs()
        self.copasiML=self.insert_fit_items()
        self.save()
        
    def save(self):
        self.CParser.write_copasi_file(self.copasi_file,self.copasiML)
        return self.copasiML



class HighThroughputFit():
    """
    The aim of this class is to build a way
    of fitting high throughput data sets to
    a single abstract model.

    The reason this class is being built is
    to model microarray data with an abstract
    model of transcription. In principle this
    idea can be extended to other models and data
    
    Just an idea t the moment. not implemented
    """

    def __init__(self,abstract_model_file):
        self.abstract_model_file = abstract_model_file
        
#==============================================================================

            
        
            
if __name__=='__main__':
    pass
#    execfile('/home/b3053674/Documents/Models/2017/08_Aug/PyCoToolsTests/RunPEs.py')
        #    execfile('/home/b3053674/Documents/PyCoTools/PyCoTools/PyCoToolsTutorial/Test/testing_kholodenko_manually.py')
