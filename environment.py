# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 16:30:50 2014

@author: Alex
"""

import environment_methods as em
import picker_classes as pc
from time import clock, sleep

class Environment():
    
    def __init__(self, filename=None, colonies=[['DecisionTreeColony', 100]]):
        self.colonies = []
        if filename:
            None
        else:
            for colony in colonies:
                if colony[0] == 'DecisionTreeColony':
                    self.colonies.append(pc.DecisionTreeColony(colony[1]))
                else:
                    print("Invalid colony type:", colony[0])
    
    def run(self, hours=8):
        #self.get_morning_data()
        #sleep(hours * 3600)
        #self.get_evening_prices()
        #self.evaluate_symbols()
        #self.update_past_data()
        self.save()
    
    def save(self):
        for colony in self.colonies:
            colony.save()
    
    def load(self):
        None
    
    def get_morning_data(self):
        None
    
    def get_evening_prices(self):
        None
    
    def evaluate_symbols(self):
        None
    
    def update_past_data(self):
        None
    
    def get_past_data(self):
        None
    
    def add_colony(self):
        None