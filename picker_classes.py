# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 21:48:06 2014

@author: Alex
"""

from sklearn import tree
from sklearn.externals import joblib
from time import clock
from environment_methods import random_string
import random


class Picker():
    """Superclass for all pickers."""
    
    def __init__(self):
        None
    
    def pick(self):
        None
    
    def save(self):
        joblib.dump(self.algorithm, self.name + ".pkl")
        

class Colony():
    """Superclass for all colonies."""
    
    def __init__(self):
        None
    
    def save(self):
       None 

class DecisionTreePicker(Picker):
    """Picker implementing simple decision tree classifier.  May be created
    from two parents, from a string, or randomly."""
    
    def __init__(self, criterion=None, splitter=None, max_features=None, max_depth=None, 
                 min_samples_split=None, min_samples_leaf=None, max_leaf_nodes=None, 
                 random_state=None, alg_filename=None):
        
        if alg_filename:
            self.alg = joblib.load(alg_filename)
        else:
            if criterion == None:
                criterion = random.choice(('gini', 'entropy'))
            
            if splitter == None:
                splitter = random.choice(('best', 'random'))
            
            if max_features == None:
                max_features = random.choice(('int', 'float', 'auto', 'sqrt', 'log2', None))
                if max_features == 'int':
                    max_features = random.randint(0, 100)
                elif max_features == 'float':
                    max_features = random.random()
            
            if max_depth == None:
                max_depth = random.choice(('int', None))
                if max_depth == 'int':
                    max_depth = random.randint(1, 100)
            
            if min_samples_split == None:
                min_samples_split = random.choice(('int', None))
                if min_samples_split == 'int':
                    min_samples_split = random.randint(0, 10)
            
            if min_samples_leaf == None:
                min_samples_leaf = random.choice(('int', None))
                if min_samples_leaf == 'int':
                    min_samples_leaf = random.randint(0, 10)
                
            if max_leaf_nodes == None:
                max_leaf_nodes = random.choice(('int', None))
                if max_leaf_nodes == 'int':
                    max_leaf_nodes = random.randint(0, 100)
            
            if random_state == None:
                random_state = random.choice(('int', None))
                if random_state == 'int':
                    random_state = random.randint(0, 100000)
            
            self.alg = tree.DecisionTreeClassifier(criterion, 
                                                   splitter, 
                                                   max_features, 
                                                   max_depth, 
                                                   min_samples_split, 
                                                   min_samples_leaf, 
                                                   max_leaf_nodes, 
                                                   random_state)
                                               
        self.age = 0
        self.speed = 0.0
        self.current_pick = None
        self.last_pick = None
        self.average_return = 0
        self.last_return = 0
        self.strength = 0
        self.name = random_string(20)
        
    def train(self, past_data, past_performance):
        self.alg = self.alg.fit(past_data, past_performance)
    
    def pick(self, current_data):
        start = clock()
        self.age += 1
        self.current_pick = self.alg.predict(current_data)
        self.speed = clock() - start
        return self.current_pick
        
    def set_strength(self, strength):
        self.strength = strength
    
    def get_age(self):
        return self.age
        
    def get_speed(self):
        return self.speed
    
    def get_current_pick(self):
        return self.current_pick
        
    def get_last_pick(self):
        return self.last_pick
        
    def get_average_return(self):
        return self.average_return
        
    def get_last_return(self):
        return self.last_return
        
    def get_strength(self):
        return self.strength

class DecisionTreeColony(Colony):
    """fill in later"""
    
    def __init__(self, size, past_data, past_performance, saved_colony_filename=None):
        self.pickers = []
        if saved_colony_filename:
            saved_colony = open(saved_colony_filename, 'r')
            for line in saved_colony:
                self.pickers.append(DecisionTreePicker(alg_filename=line))
        else:
            for i in range(size):
                picker = DecisionTreePicker()
                picker.train(past_data, past_performance)
                self.pickers.append(picker)
    
    def pick(self, current_data):
        picks = []
        for picker in self.pickers:
            picks.append(picker.pick(current_data))
    
    def evaluate(self):
        None
    
    def cull(self):
        None
                
    def breed(self):    
        None
    
    def train(self, past_data, past_performance):
        for picker in self.pickers:
            if picker.get_age() == 0:
                picker.train(past_data, past_performance)