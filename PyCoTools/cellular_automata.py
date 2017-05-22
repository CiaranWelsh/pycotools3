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
import os

LOG=logging.getLogger(__name__)




class State(object):
    '''
    A cell can be in a state which is defined using this class
    
    args:
        label:
            symbolic representation of a state
    '''
    def __init__(self,label,rule=None):
        self.label=self.set_label(label)
        self.rule=rule
    
    def __repr__(self):
        return str(self.label)
    
    def set_label(self,label):
        self.label=label
        return self.label
    
    def get_label(self):
        return self.label
    
    def set_rule(self,rule):
        if isinstance(rule,Rule)!=True:
            raise TypeError('{} is not of type Rule'.format(rule))
        self.rule=rule
        return rule
    
    def get_rule(self):
        return self.rule
    
class ZerothOrderReaction(object):
    def __init__(self,A):
        self.A=A
    
    
class FirstOrderReaction(object):
    def __init__(self):
        pass
    
    
class SecondOrderReaction(object):
    def __init__(self):
        pass
    
    
    
class Rule(object):
    '''
    Use compas NESW... for navigation. 
    Does it extend to 3D? 
    
    0, first second ,third order reations
    Diffusion
    
    
    Need:
        Static reaction
            A Cell converts to another cell type (i.e. different state)
            but stays at current location. Is this just a first order 
            reaction
            
        second order reaction:
            A cell 'reacts' with another cell if they are next to eachother
            in the appropiate stoiciometry
            
        Movement:
            Diffusion? A cell moves but remains unchanged
            
        Proliferation == 1st order reaction with two products .
        
        
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
        self.state=self.set_state(state)
        self.x=x
        self.y=y
        self.z=z
        self.coordinates=[]
        
        if self.x==None:
            raise TypeError('x cannot be None')
        
        if self.y== None and self.z==None:
            self.coordinates=self.x#]=state
                            
        elif self.z==None:
            self.coordinates=(self.x,self.y)#=state
        
        elif self.x!=None and self.y!=None and self.z!=None:
            self.coordinates=(self.x,self.y,self.z)#]=state
                             
        self.dimensions=self.get_num_dimensions()
                             
        self.neighbours=self.define_neighbours()
        
    def get_num_dimensions(self):
        boolean= [isinstance(i,int) for i in [self.x,self.y,self.z]]
        if boolean ==[False,False,False]:
            raise Errors.InputError('Need to specific at least an x dimension')            
        elif boolean == [True,False,False]:
            return 1
        elif boolean == [True,True,False]:
            return 2
        elif boolean == [True,True,True]:
            return 3
        else:
            LOG.critical('Something has gone badly wrong')
            raise Exception('Something is wrong (I like to be helpful)')
        
        
                             
                             
    def define_neighbours(self):
        neighbours={}
        if self.dimensions==1:
            neighbours['W']=self.x-1
            neighbours['E']=self.x+1
        elif self.dimensions==2:
            neighbours['NW']= (self.x-1,self.y-1)
            neighbours['N']=(self.x,self.y-1)
            neighbours['NE']=(self.x+1,self.y-1)
            neighbours['E']=(self.x-1,self.y)
            neighbours['SE']=(self.x+1,self.y)
            neighbours['S']=(self.x-1,self.y+1)
            neighbours['SW']=(self.x,self.y+1)
            neighbours['E']=(self.x+1,self.y+1)
        elif self.dimensions==3:
            neighbours['FNW']= (self.x-1,self.y-1,self.z+1)
            neighbours['FN']=(self.x,self.y-1,self.z+1)
            neighbours['FNE']=(self.x+1,self.y-1,self.z+1)
            neighbours['FE']=(self.x-1,self.y,self.z+1)
            neighbours['FSE']=(self.x+1,self.y,self.z+1)
            neighbours['FS']=(self.x-1,self.y+1,self.z+1)
            neighbours['FSW']=(self.x,self.y+1,self.z+1)
            neighbours['FE']=(self.x+1,self.y+1,self.z+1)
            neighbours['F']=(self.x,self.y,self.z+1)
            
            neighbours['MNW']= (self.x-1,self.y-1,self.z)
            neighbours['MN']=(self.x,self.y-1,self.z)
            neighbours['MNE']=(self.x+1,self.y-1,self.z)
            neighbours['ME']=(self.x-1,self.y,self.z)
            neighbours['MSE']=(self.x+1,self.y,self.z)
            neighbours['MS']=(self.x-1,self.y+1,self.z)
            neighbours['MSW']=(self.x,self.y+1,self.z)
            neighbours['ME']=(self.x+1,self.y+1,self.z)
            
            neighbours['BNW']= (self.x-1,self.y-1,self.z-1)
            neighbours['BN']=(self.x,self.y-1,self.z-1)
            neighbours['BNE']=(self.x+1,self.y-1,self.z-1)
            neighbours['BE']=(self.x-1,self.y,self.z-1)
            neighbours['BSE']=(self.x+1,self.y,self.z-1)
            neighbours['BS']=(self.x-1,self.y+1,self.z-1)
            neighbours['BSW']=(self.x,self.y+1,self.z-1)
            neighbours['BE']=(self.x+1,self.y+1,self.z-1)
        else:
            LOG.critical('Not 1,2 or 3 dimesions. Something is seriously wrong')
        return neighbours
        
    def set_state(self,state):
        '''
        
        '''
        return State(state)
    
    def get_state(self):
        return self.state
    
    def __repr__(self):
        return str('Cell({},{})'.format(self.coordinates,self.state))

    def __getitem__(self,idx):
        return self.coordinates[idx]
    
    def __setitem__(self,idx,item):
        self.coordinates[idx]=item
                        
#    def keys(self):
#        return self.coordinates.keys()[0]
#                     
#    def values(self):
#       return self.coordinates.values()[0]
                    
    
    
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
    def __init__(self, x=64,y=None,z=None):
        self.x=x
        self.y=y
        self.z=z
        self.index=0
        self.dimensions=self.get_num_dimensions()
        self.cells=self.create()
        self.filter_cell_neighbours()
        
        
    def filter_cell_neighbours(self):
        '''
        Remove neighbours from each cell which 
        violate boundaries of the automata dimensions
        '''
        if self.dimensions==1:
            for cell in self.cells:
                for direction,x in self.cells[cell].neighbours.items():
                    if x not in range(self.x):
                        del self.cells[cell].neighbours[direction]
        if self.dimensions==2:
            for cell in self.cells:
                for direction,(x,y) in self.cells[cell].neighbours.items():
                    if x not in range(self.x):# direction,x,y
                        del self.cells[cell].neighbours[direction]
                for direction,(x,y) in self.cells[cell].neighbours.items():
                    if y not in range(self.y):
                        del self.cells[cell].neighbours[direction]
                        
        if self.dimensions==3:
            for cell in self.cells:
                for direction,(x,y,z) in self.cells[cell].neighbours.items():
                    if x not in range(self.x):# direction,x,y
                        del self.cells[cell].neighbours[direction]
                for direction,(x,y,z) in self.cells[cell].neighbours.items():
                    if y not in range(self.y):
                        del self.cells[cell].neighbours[direction]
                for direction,(x,y,z) in self.cells[cell].neighbours.items():
                    if z not in range(self.y):
                        del self.cells[cell].neighbours[direction]
        
    def get_num_dimensions(self):
        boolean= [isinstance(i,int) for i in [self.x,self.y,self.z]]
        if boolean ==[False,False,False]:
            raise Errors.InputError('Need to specific at least an x dimension')            
        elif boolean == [True,False,False]:
            return 1
        elif boolean == [True,True,False]:
            return 2
        elif boolean == [True,True,True]:
            return 3
        else:
            LOG.critical('Something has gone badly wrong')
            raise Exception('Something is wrong (I like to be helpful)')
        
            
        
        
    def __iter__(self):
        for i in self.cells:
            yield i
    
    def __getitem__(self, index):
        return self.cells[index]
#    
    def __setitem__(self,key,item):
        self.cells[key]=item

    def __repr__(self):
        return str(self.cells)
    
    def update_cell(self,cell,value):
        self.cells[cell]=value
        
    
    def create(self):
        '''
        
        '''
        if self.dimensions==1:
            LOG.debug('creating lattice in 1D')
            cells={}
            for i in range(self.x):
                cell=Cell('Empty',x=i)
                cells[cell.coordinates]=cell
            return cells
                
        elif self.dimensions==2:
            LOG.debug('creating lattice in 2D')
            cells={}
            for i in range(self.x):
                for j in range(self.y):
                    cell=Cell('Empty',x=i,y=j)
                    cells[cell.coordinates]=cell
            return cells
        
        elif self.dimensions==3:
            LOG.debug('creating lattice in 3D')
            cells={}
            for i in range(self.x):
                for j in range(self.y):
                    for k in range(self.z):
                        cell=Cell('Empty',x=i,y=j,z=k)
                        cells[cell.coordinates]=cell
            return cells
    
class Automaton(object):
    '''
    Need syntax for determining the default background state
    '''
    def __init__(self,rules,lattice,initial,generations=10):
        self.rules = rules
        self.initial = initial
        self.lattice = lattice
        self.preamble,self.rules = self.read_rules()
        
        self.num_rules= len(self.rules)
#        print self.rules
        self.environment='Empty'
        self.enviornment,self.seeds = self.interpret_preamble()
        self.set_environment()
        self.set_seeds()
#        self.environment=self.interpret_environment()
        
#        print self.environment
#        self.states=self.get_states()
#        self.seed()
#        self.turn()
        
#        print self.lattice[0]
        
        
    def get_states(self):
        states=[]
        for rule in self.rules:
            if '->' in rule:
                a,b= re.findall('(.*) -> (.*)',rule)[0]
                c= re.search('\[',a)
                if not c:
                    states.append(a) 
#                states.append(a)
                states.append(b)
        for state in states:
            match=re.findall('.*\[(.*)\(.*\)\]', state)
            if match != []:
                states=states+match
        return list(set(states))
                
    
    def read_rules(self):
        '''
        Convert rule string into list of rules/reactions
        This may be best implemented in some other way. 
        Try and copy the with approach from ecell4
        '''
        rules= self.rules.split('\n')
        rules= [rules[i].strip() for i in range(len(rules))]
        rules=[i for i in rules if i!='' ]
        preamble=[]
        new_rules=[]
        for i in range(len(rules)):
            if rules[i][:2]=='%%':
                preamble.append(rules[i])
            else:
                new_rules.append(rules[i])
        LOG.debug('\n\nThis is your preamble:\n\t\t{}\n\n\nThese are your rules\n\t\t{}'.format(preamble,new_rules))
        return preamble,new_rules
    
    def interpret_rules(self):
        '''
        
        '''
        rules=[]
        for rule in self.rules:
            if '->' in rule:
                a,b= re.findall('(.*) -> (.*)', rule)[0]
                rules.append(Rule(a,b))
        return rules
    
    def interpret_preamble(self):
        '''
        Read model specification begining with 'Environment'
        and convert all cells to the clause in the square brackets. 
        i.e. detect Environment[White] and set all Cells to State White
        '''
        preamble_id=None
        environment_id=None
        seeds=None
        for rule in self.preamble:
            rule=rule[2:]
            try:
                preamble_id= re.findall('^(\w+)',rule)[0]
            
                if preamble_id=='Environment':
                    environment_id=re.findall('(\w+)$',rule)[0]
                elif preamble_id=='Seed':
                    seeds=re.findall('= (.*)',rule)[0]
                    
            except IndexError:
                LOG.warning('No Enviornment or Seed set. Default enviornment (Empty) is being used without any initial conditions')
        
        if preamble_id==0:
            return None
        
        if environment_id==None:
            LOG.warning('No Enviornment specified. Using default (Empty)')
        
        if seeds==None:
            LOG.warning('No Seed set. Initial conditions are black')
            
        return environment_id,seeds
        
    def set_environment(self):
        for cell in self.lattice:
            self.lattice[cell]=self.environment            
            
    def set_seeds(self):
        d={}
        pattern=re.findall(r'(\w+)<([^<>]+)>',self.seeds)
        for i in range(len(pattern)):
            d[i]={}
        for i in range(len(pattern)):
            d[i][pattern[i][0]]= map(int,pattern[i][1].split(','))
            
        LOG.debug('Seeding {}:\n\nSeed Dict=\n\t{}'.format(self.seeds,d))
        for seed in d:
            self.lattice[ d[seed].values()[0][0]] = d[seed].keys()[0]
        return d
    
    def turn(self):
        '''
        '''
        print self.interpret_rules()



if __name__=='__main__':
    
    rules='''
    %%Environment = White
    %%Seed = Black<5,4>, Black<9,4>
    Black -> White
    White + Black -> Black  ##comments are possible. 
    Black + White -> Black
    '''
    rules='''
    %%Environment = White
    %%Seed = Black<5>, Black<9>
    Black -> White
    '''    
    
    
    L=Lattice(x=11)#,y=11,z=11)
#    print L.cells[0,0,0].neighbours
#    black=State('Black')
##    white=State('White')
#    initial={5:'Black'}
    A=Automaton(rules,L,initial)
#    print A.lattice
    
#    print A
#    print M.lattice
#    for cell in L:
#        print type(cell)


#    cell=Cell('black',x=6,y=6,z=None)
##    print cell
#    print cell.neighbours
    
#    print cell.values()
#    cell[(1,None,None)]='white'
    
    #[(1,None,None)]

#    L=Lattice(dimensions=1,x=4,y=4)
#    L.update_cell(0,'new')
#    print L
##    print L[0]['Empty']

#    print L[0].coordinate
#    for i in M.lattice:
#        print M.lattice[i].coordinate
        
#    for i in L:
#        print i
#    print L
#    print [Cell(1),Cell(2)]

    
#    Cell objects shold have a key which is the state ad
#    the coordinates




























































