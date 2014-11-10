# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 21:48:06 2014

@author: Alex
"""

from sklearn import tree

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
    
    def __init__(self):
        self.age = 0
        self.total_score = 0
        self.alg = tree.DecisionTreeClassifier()
    
    def train(self, past_data, past_performance):
        self.alg = self.alg.fit(past_data, past_performance)
    
    def pick(self, current_data):
        self.age += 1
        self.current_pick = self.alg.predict(current_data)
        return self.current_pick
    
    def evaluate_current_pick(self, new_data):
        self.current_score = None
        self.total_score = (self.total_score * (self.age - 1) + self.current_score) / self.age
    
    def get_current_score(self):
        return self.current_score
    
    def get_total_score(self):
        return self.total_score

class DecisionTreeColony():
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
    
    def evaluate_pickers(self):
        None
    
    def cull(self):
        for picker in self.pickers:
            if picker.get_total_score < 0:
                self.pickers.remove(picker)
                
    def breed(self):
        # don't forget to train new pickers        
        None