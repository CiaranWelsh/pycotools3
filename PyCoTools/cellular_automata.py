#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:40:48 2017

@author: b3053674
"""
import logging
import pandas
from contextlib import contextmanager


LOG=logging.getLogger(__file__)





class Rule():
    '''
    
    '''
    def __init__(self,definition):
        self.definition=definition
        
    def read_definition(self):
        print self.definition
    
    
    
class State():
    '''
    
    '''
    def __init__(self,label):
        self.label=label
    
    def set_rule(self,Rule):
        pass
        
        
        
class Model():
    '''
    
    '''
    def __init__(self,transitions):
        self.transitions=transitions
        print self.read_transitions()
    
    
    def read_transitions(self):
        self.transitions= self.transitions.split('\n')
        self.transitions= [self.transitions[i].strip() for i in range(len(self.transitions))]
        self.transitions=[i for i in self.transitions if i!='']
        print self.transitions
    
    
    
class Cell():
    '''
    
    '''
    def __init__(self):
        pass
    
    
    
class Lattice():
    '''
    
    '''
    def __init__(self):
        pass
    
    
    
class Automaton():
    '''
    
    '''
    def __init__(self):
        pass
    
        



if __name__=='__main__':
    state1=State('State1')
    bool_rule=Rule('boolean')
    
    trans='''
    s1 -> s2
    s3{1} -> s4
    '''
    M=Model(trans)
    
    






























































