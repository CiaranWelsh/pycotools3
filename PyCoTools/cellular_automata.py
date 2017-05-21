#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:40:48 2017

@author: b3053674
"""
import Errors
import logging
import pandas
import numpy
from contextlib import contextmanager
import re
from random import randint

LOG=logging.getLogger(__file__)




class State(object):
    '''
    A cell can be in a state which is defined using this class
    
    args:
        label:
            symbolic representation of a state
    '''
    def __init__(self,label):
        self.label=label
    
    def __repr__(self):
        return str(self.label)
    
    
    
    
class Rule(object):
    '''
    Use compas NESW... for navigation. 
    Does it extend to 3D? 
    '''
    def __init__(self,a,b):
        self.a=a
        self.b=b
        self.type=''
        
        self.interpret_rule()
        
        if self.type=='':
            raise Errors.InputError('type attribute has not been set')
        
        
    def interpret_rule(self):
        square_brackets= re.findall('\[(.*\])',self.a)
        if square_brackets==[]:
            self.type='C'
            
        elif square_brackets!=[]:
            self.type= re.findall('\((.*)\)',square_brackets[0])[0]
            self.type=list(self.type)
            self.qualifier=re.findall('(.*)\(',square_brackets[0])[0]
            
            
            
    
            
            
    def set_type(self):
        '''
        
        '''
        pass
    
    

        
        
        

        
        
    
    
class Cell(object):
    '''
    Cell objects are components of the lattice
    
    args:
        state:
            Symbolic representation of cell state
    kwargs:
        x: 
            x coordinate. Defuault=None
        y:
            y coordinate. Default=None
        z: 
            z coordinate. Devault=None
            
    ===================
    Additional attributes:
        coordinates:
            tuple containing (x,y,z), the position of the cell
        
    '''
    def __init__(self,state,x=None,y=None,z=None):
        self.state=state
        self.x=x
        self.y=y
        self.z=z
        self.coordinates=(self.x,self.y,self.z)
        
    def set_state(self,state):
        '''
        
        '''
        if isinstance(state,State)!=True:
            raise TypeError('{} not State'.format(type(state)))
        return State(state)
    
    def get_state(self):
        return self.state
    
    def __repr__(self):
        return str(self.coordinates)

    def __getitem__(self,idx):
        return self.coordinate[idx]
    
    def __setitem__(self,idx,item):
        self.geometry[idx]=item
                     
                     
    def neighbours(self):
        pass
    
class Cell(object):
    '''
    Cell objects are components of the lattice
    
    args:
        state:
            Symbolic representation of cell state
    kwargs:
        x: 
            x coordinate. Defuault=None
        y:
            y coordinate. Default=None
        z: 
            z coordinate. Devault=None
            
    ===================
    Additional attributes:
        coordinates:
            tuple containing (x,y,z), the position of the cell
        
    '''
    def __init__(self,state,x=None,y=None,z=None):
        self.state=state
        self.x=x
        self.y=y
        self.z=z
        self.coordinates=(self.x,self.y,self.z)
        
    def set_state(self,state):
        '''
        
        '''
        if isinstance(state,State)!=True:
            raise TypeError('{} not State'.format(type(state)))
        return State(state)
    
    def get_state(self):
        return self.state
    
    def __repr__(self):
        return str(self.coordinates)

    def __getitem__(self,idx):
        return self.coordinate[idx]
    
    def __setitem__(self,idx,item):
        self.geometry[idx]=item
                     
                     
    def neighbours(self):
        pass        
    
    
    '''
    get item and set item are used in dicts for mattping keys to values
    which is why I cannot yse the list like lattice in the model object. 
    modify!
    
    Create a dictionary type lattice with coordinates corresponding
    to grid locations and value containing the Cell(State) object
    '''   
    
class Lattice(object):
    '''
    A structure for containing cells that are associated with 
    a state. 
    
    kwargs:
        dimensions:
            lattice can be 1, 2 or 3 dimensional
        x:
            size of lattice in x dimension
        y:
            size of lattice in y dimension. Only 
            used when dimensions=2 or 3
        z:
            size of lattice in z dimension.
            Only used when dimensions=3
    ==================
    Other Attributes:
        index:
            Used for iterating over the lattice
            
        geometry:
            name used for accessing cells in the lattice
            
        
    '''
    def __init__(self,dimensions=1, x=64,y=64,z=64):
        self.dimensions=dimensions
        self.x=x
        self.y=y
        self.z=z
        self.index=0
        self.geometry=self.create()
        
        
    def __iter__(self):
        for i in self.geometry:
            yield i
    
    def __getitem__(self, index):
        return self.geometry[index]
    
    def __setitem__(self,key,item):
        self.geometry[key]=item

    def __repr__(self):
        return str(self.geometry.values())
#        if self.dimensions==1:
#            for i in self.geometry:
                
#            l=numpy.array()
#            for i in self.geometry.values():
#                l.append(i.state)
#            return str(l)
        
        
    
    def create(self):
        '''
        
        '''
        if self.dimensions==1:
            LOG.debug('creating lattice in 1D')
            cells={}
            for i in range(self.x):
                cells[i]=Cell(State('Empty'),x=i)
            return cells
        
        elif self.dimensions==2:
            LOG.debug('creating lattice in 2D')
            cells={}
            for i in range(self.x):
                cells[i]={}
                for j in range(self.y):
                    cells[i][j]=Cell(State('Empty'),x=i,y=j)
            return cells
        
        elif self.dimensions==3:
            LOG.debug('creating lattice in 3D')
            cells={}
            for i in range(self.x):
                cells[i]={}
                for j in range(self.y):
                    cells[i][j]={}
                    for k in range(self.z):
                        cells[i][j][k]=Cell(State('Empty'),x=i,y=j,z=k)
            return cells
    
class Model(object):
    '''
    Need syntax for determining the default background state
    '''
    def __init__(self,transitions,lattice,states):
        self.transitions=transitions
        self.lattice=lattice
        self.transitions=self.read_transitions()
        self.num_transitions= len(self.transitions)
        self.states=states
        self.operators=['->','=']
        self.environment='Empty'
        self.environment=self.interpret_environment()
#        self.interpret_transitions()
        
        self.seed()
        
#        print self.lattice[0]
        
        
        
    def add_state(self,state):
        self.state_types=[]
        return self.state_types.append(state)
        
    
    
    def read_transitions(self):
        '''
        Convert transition string into list of transitions/reactions
        This may be best implemented in some other way. 
        Try and copy the with approach from ecell4
        '''
        self.transitions= self.transitions.split('\n')
        self.transitions= [self.transitions[i].strip() for i in range(len(self.transitions))]
        self.transitions=[i for i in self.transitions if i!='']
        return self.transitions
    
    def interpret_transitions(self):
        '''
        
        '''
        rules=[]
        for transition in self.transitions:
            if '->' in transition:
                a,b= re.findall('(.*) -> (.*)', transition)[0]
                rules.append(Rule(a,b))
        return [i.type for i in rules]
    
    def interpret_environment(self):
        '''
        Read model specification begining with 'Environment'
        and convert all cells to the clause in the square brackets. 
        i.e. detect Environment[White] and set all Cells to State White
        '''
        for transition in self.transitions:
            if 'Environment' in transition:
                environment=re.findall('\[(.*)\]',transition)[0]
        return environment
            
            
    def seed(self):
        for cell in self.lattice:
            self.lattice[cell]=Cell(self.environment)
            
        self.lattice[32]=Cell(self.states[0])    
    
class Automaton(object):
    '''
    
    '''
    def __init__(self):
        pass
    
        



if __name__=='__main__':
    
    trans='''
    Environment[White]
    Black -> White
    White[Black(WE)] -> Black
    '''
    
    
    
#    L=Lattice(dimensions=1)
#    black=State('Black')
#    white=State('White')
#    M=Model(trans,L,[black,white])



    black=State('Black')
    cell=Cell(black,x=1,y=None,z=None)
    print cell

#    L=Lattice(dimensions=1,x=4,y=4)
#    print L

#    print L[0].coordinate
#    for i in M.lattice:
#        print M.lattice[i].coordinate
        
#    for i in L:
#        print i
#    print L
#    print [Cell(1),Cell(2)]

    
#    Cell objects shold have a key which is the state ad
#    the coordinates




























































