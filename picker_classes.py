# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 21:48:06 2014

@author: Alex
"""

import random
from sklearn import tree

class Picker():
    """Superclass for all pickers."""
    
    def __init__(self):
        None
    
    def pick(self):
        None

class DecisionTreePicker(Picker()):
    """Picker implementing simple decision tree classifier.  May be created
    from two parents, from a string, or randomly."""
    
    def __init__(self, past_data):
        self.alg = tree.DecisionTreeClassifier()
        self.alg = self.alg.fit(past_data)
    
    def pick(self, current_data):
        self.current_pick = self.alg.predict(current_data)
        return self.current_pick
    
    def evaluate_current_pick(self, new_data):
        self.current_score = None