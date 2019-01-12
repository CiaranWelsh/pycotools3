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
from collections import OrderedDict
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
    def __init__(self,label,behaviour=None):
        self.label=self.set_label(label)
        self.behaviour=behaviour
    
    def __repr__(self):
        return str(self.label)
    
    def set_label(self,label):
        self.label=label
        return self.label
    
    def get_label(self):
        return self.label
    
    def set_behaviour(self,type):
        return Behaviour.factory(type)
    
    def get_behaviour(self):
        pass
            
    
class Behaviour(object):
    '''
    Base class of behaviour. Read and interpret rules from a string.
    Firstly Behaviour differentiates between the preamble and the actual rules 
    which determine behaviour. 
    
    Collect subclasses using the BehaviourFactory.__subclasses__() function
    
    '''
        
    @staticmethod
    def factory(args,rule):

        if rule=='constant_production':
            return ConstantProduction(args)
        elif rule=='transition':
            return Transition(args)
        else:
            raise TypeError('{} not a valid type'.format(rule))
        
        
        
class Transition(Behaviour):
    
    def __init__(self,args1):
        self.args1=args1
        
    def update(self,cell):
        pattern= '(.*) -> (.*)'
        A,B=re.findall(pattern,self.args1)[0]
        if cell.state.label==A:
            return State(B.strip())
        else:
            return cell.state.label.strip()
        
    def __str__(self):
        return '<class Transition>'
        
#            elif i=='Black -> White : transition':
#                if self.state.label == 'Black':
#                    self.state=State('White')            
            

    
    
class ConstantProduction(Behaviour):
    '''
    Describes production of the type:
        
        -> A<index>
    
    Where A is constantly produced at a location given in index. This
    is essentially a zeroth order reaction.
    '''
    def __init__(self,args):
        self.args=args
        
        
    def update(self,cell):
        pattern='-> (\D+)<(\d)>|-> (\D+)<(\d,\d)>|-> (\D+)<(\d,\d,\d)>'
        match=re.findall(pattern,self.args)[0]
        A,index= [i for i in match if i!='']
        if cell.coordinates==int(index):
            return State(A.strip())
        else:
            return cell.state
        
    def __str__(self):
        return '<class ConstantProduction>'
        
        
    
    
    

        
        
    
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
    def __init__(self,state,x=None,y=None,z=None,behaviours=[]):
        self.state=state
        self.state=self.set_state(state)
        self.x=x
        self.y=y
        self.z=z
        self.behaviours=behaviours
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
        return str('Cell({})'.format(self.state))

    def __getitem__(self,idx):
        return self.coordinates[idx]
    
    def __setitem__(self,idx,item):
        self.coordinates[idx]=item
        
        
    def update2(self):
        for i in self.behaviours:
            if i=='-> White<5> : constant_production':
                if self.coordinates == 5:
                    self.state=State('White')
                    
            elif i=='Black -> White : transition':
                if self.state.label == 'Black':
                    self.state=State('White')
                    
    def update(self):
        for i in self.behaviours:
            LOG.debug('Current State = {}'.format(self.state))
            LOG.debug('Updating behaviour "{}"'.format(i))
            args,rule=i.split(':')
            behaviour= Behaviour.factory(args,rule.strip())
            LOG.debug('Behaviour determined to be {}'.format(behaviour))
            self.state=behaviour.update(self)
            LOG.debug('New state is: {}'.format(self.state))

    
class Lattice(OrderedDict):
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
        pass            
        
    '''
    def __init__(self,cell, x=64,y=None,z=None,):
        super(Lattice,self).__init__(x=64,y=None,z=None)
        self.cell=cell
        self.x=x
        self.y=y
        self.z=z
        
        self.dimensions=self._get_num_dimensions()
        self._create()
        self._remove_coordinates()
        self._filter_cell_neighbours()
#        self.update()
    
    ##private, void
    def _remove_coordinates(self):
        '''
        OrderedDict automatically puts the x,y and z values into the dict. 
        This method removes these from the dict
        '''
#        for i in range(3):
        self.popitem(last=False)
        self.popitem(last=False)
        self.popitem(last=False)
            
    ##private, void
    def _filter_cell_neighbours(self):
        '''
        Remove neighbours from each cell which 
        violate boundaries of the automata dimensions
        '''
        if self.dimensions==1:
            for cell in self:
                for direction,x in list(self[cell].neighbours.items()):
                    if x not in list(range(self.x)):
                        del self[cell].neighbours[direction]
        if self.dimensions==2:
            for cell in self:
                for direction,(x,y) in list(self[cell].neighbours.items()):
                    if x not in list(range(self.x)):# direction,x,y
                        del self[cell].neighbours[direction]
                for direction,(x,y) in list(self[cell].neighbours.items()):
                    if y not in list(range(self.y)):
                        del self[cell].neighbours[direction]
                        
        if self.dimensions==3:
            for cell in self:
                for direction,(x,y,z) in list(self[cell].neighbours.items()):
                    if x not in list(range(self.x)):# direction,x,y
                        del self[cell].neighbours[direction]
                for direction,(x,y,z) in list(self[cell].neighbours.items()):
                    if y not in list(range(self.y)):
                        del self[cell].neighbours[direction]
                for direction,(x,y,z) in list(self[cell].neighbours.items()):
                    if z not in list(range(self.y)):
                        del self[cell].neighbours[direction]
    
    ##private
    def _get_num_dimensions(self):
        '''
        returns 1, 2 or 3 dependinging on arguments to x,y and z kwargs
        '''
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
        
    ##private,void
    def _create(self):
        '''
        
        '''
        if self.dimensions==1:
            LOG.debug('creating lattice in 1D')
            for i in range(self.x):
                cell=Cell('Empty',x=i)
                cell.state=self.cell.state
                self[cell.coordinates]=cell
            return self#cells
                
        elif self.dimensions==2:
            LOG.debug('creating lattice in 2D')
            for i in range(self.x):
                for j in range(self.y):
                    cell=Cell('Empty',x=i,y=j)
                    cell.state=self.cell.state

                    self[cell.coordinates]=cell
            return self
        
        elif self.dimensions==3:
            LOG.debug('creating lattice in 3D')
            for i in range(self.x):
                for j in range(self.y):
                    for k in range(self.z):
                        cell=Cell('Empty',x=i,y=j,z=k)
                        cell.state=self.cell.state
                        self[cell.coordinates]=cell
            return self
        
#    def update(self):
#        for cell in self:
#            print self[cell].update()


class Automaton(object):
    '''
    Need syntax for determining the default background state
    What is my strategy for the automaton?
    
    1) read th rules and interpret them. 
    2) for each rule
    '''
    def __init__(self,rules,lattice,initial,generations=10):
        self.rules = rules
        self.initial = initial
        self.lattice = lattice
        self.preamble,self.rules = self.read_rules()
        self.states=[]
        
        self.num_rules= len(self.rules)
#        print self.rules
        self.environment,self.seeds = self.interpret_preamble()
        self.set_environment()
        self.set_seeds()
        self.behaviours=self.get_behaviours()
        print((self.turn()))
        
    def turn(self):
        lattice2=self.lattice
        for i in self.lattice:
            print((lattice2[i]))
                
    def get_behaviours(self):
        '''
        
        '''
        b={}
        for line in self.rules:
            args, rule = line.split(':')
            behaviour = Behaviour.factory(args,rule.strip())
            b[line]=behaviour
        return b
            
            
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
                    self.states.append(environment_id)
                elif preamble_id=='seed':
                    seeds=re.findall('= (.*)',rule)[0]
                    
            except indexError:
                LOG.warning('No Enviornment or seed set. Default enviornment (Empty) is being used without any initial conditions')
        
        if preamble_id==0:
            return None
        
        if environment_id==None:
            LOG.warning('No Enviornment specified. Using default (Empty)')
        
        if seeds==None:
            LOG.warning('No seed set. Initial conditions are black')
            
        return environment_id,seeds
        
    def set_environment(self):
        for cell in self.lattice:
            if isinstance(cell,int):
                self.lattice[cell]=Cell(self.environment,cell)
            elif isinstance(cell,tuple):
                self.lattice[cell]=Cell(self.environment,*cell)
        return self.lattice
            
    def set_seeds(self):
        d={}
        pattern=re.findall(r'(\w+)<([^<>]+)>',self.seeds)
        for i in range(len(pattern)):
            d[i]={}
        for i in range(len(pattern)):
            d[i][pattern[i][0]]= list(map(int,pattern[i][1].split(',')))
            
        LOG.debug('seeding {}:\n\nseed Dict=\n\t{}'.format(self.seeds,d))
        for seed in d:
            self.lattice[ list(d[seed].values())[0][0]] = Cell(list(d[seed].keys())[0],x=list(d[seed].values())[0][0])
        return d

        
    

if __name__=='__main__':
    
    rules='''
    %%Environment = White
    %%seed = Black<5,4>, Black<9,4>
    Black -> White
    White + Black -> Black  ##comments are possible. 
    Black + White -> Black
    Black -> White : transition

    '''
    rules='''
    %%Environment = White
    %%seed = Black<5>, Black<9>
    -> Black<5> : constant_production
    '''    
    
    
    '''
    To make a system with two states
    the background and black state, 
    associate the states with cells
    
    '''
    
    
    c=Cell('Black',x=4,behaviours=['-> White<4> : constant_production',
                                   'Black-> White : transition'])
    print(c)
    c.update()
    print(c)
#    L=Lattice(c,x=20)
#    print L

























































