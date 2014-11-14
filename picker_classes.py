# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 21:48:06 2014

@author: Alex
"""

from sklearn import tree
from time import clock

class Picker():
    """Superclass for all pickers."""
    
    def __init__(self):
        self.total_score = 0
    
    def pick(self):
        None

class Colony():
    """Superclass for all colonies."""

class DecisionTreePicker(Picker):
    """Picker implementing simple decision tree classifier.  May be created
    from two parents, from a string, or randomly."""
    
    def __init__(self, criterion, splitter, max_features, max_depth, 
                 min_samples_split, min_samples_leaf, max_leaf_nodes, 
                 random_state):
                     
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
    
    def __init__(self, size, past_data, past_performance):
        self.pickers = []
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