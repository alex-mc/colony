# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 16:30:50 2014

@author: Alex
"""

import environment_methods as em
import picker_classes as pc
import ystockquote as ys
from time import sleep
from values import symbol_list

class Environment():
    
    def __init__(self, dirnames=None, colonies=[['DecisionTreeColony', 100]]):
        self.colonies = []
        if dirnames:
            for dirname in dirnames:
                colony_type = dirname.split('_')[0]
                if colony_type == 'DTC':
                    self.colonies.append(pc.DecisionTreeColony(dirname.split('_')[1], saved_colony_dirname=dirname))
        else:
            for colony in colonies:
                if colony[0] == 'DecisionTreeColony':
                    self.colonies.append(pc.DecisionTreeColony(colony[1]))
                else:
                    print("Invalid colony type:", colony[0])
    
    def run(self, hours=8):
        self.get_morning_data()
        for colony in self.colonies:
            print(colony.pick())
        #sleep(hours * 3600)
        self.get_evening_prices()
        self.evaluate_symbols()
        #evolve
        self.update_past_data()
        self.save()
    
    def save(self):
        for colony in self.colonies:
            colony.save()
    
    def get_morning_data(self):
        """Retrieve all data available from ystockquote for each known symbol. This
        data is classified by pickers and added to past data once evening prices
        are obtained.  This method should be run in the morning to allow pickers
        to make their picks."""
        current_data = {}
        for symbol in symbol_list:
            print(symbol)
            while True:
                try:
                    current_data[symbol] = ys.get_all(symbol)
                    break
                except:
                    sleep(1)
        self.current_data = current_data
    
    def get_evening_prices(self):
        """Retrieve price for each symbol.  This method should be run in the
        evening so that picker's picks can be evaluated."""
        new_data = {}
        for symbol in symbol_list:
            print(symbol)
            while True:
                try:
                    new_data[symbol] = ys.get_price(symbol)
                    break
                except:
                    sleep(1)
        self.new_data = new_data
    
    def evaluate_symbols(self):
        """Assign a number from -2 to 2 to each symbol depending on its
        performance from the past day.
        
        2   -  better than 5% gain
        1   -  0.5 to 5% gain
        0   -  0.5% loss to 0.5% gain
        -1  -  2.5% to 0.5% loss
        -2  -  worse than 2.5% loss  
        
        """
        symbol_performances = {}
        for symbol in symbol_list:
            morning_price = float(self.current_data[symbol]['price'])
            evening_price = float(self.new_data[symbol])
            try:
                price_change = (evening_price - morning_price) / morning_price
            except:
                price_change = 0.0
            if price_change >= 0.05:
                performance = 2
            elif price_change >= 0.005:
                performance = 1
            elif price_change >= 0.0:
                performance = 0
            elif price_change >= -0.025:
                performance = -1
            elif price_change < -0.025:
                performance = -2
            symbol_performances[symbol] = performance
        self.symbol_performances = symbol_performances
    
    def update_past_data(self):
        """Append current day's data and performance to past data.  Past data
        represents training data."""
        past_data = open('past_data.txt', 'a')
        for symbol in symbol_list:
            for k, v in self.current_data[symbol].items():
                v = em.return_data_value_as_number(v)
                past_data.write(k)
                past_data.write(',')
                past_data.write(str(v))
                past_data.write(';')
            past_data.write('performance,')
            past_data.write(str(self.symbol_performances[symbol]))
            past_data.write('\n')
        past_data.close()
    
    def get_past_data(self):
        """Read past data from file into feature and class lists for training."""
        training_data = []
        performance_data = []
        past_data = open('past_data.txt', 'r')
        for line in past_data:
            line = line.split(';')
            symbol_data = []
            for data_element in line:
                data_element = data_element.split(',')
                value = data_element[1]
                try:
                    value = int(value)
                except:
                    continue
                symbol_data.append(value)
            
            # move performance value (last value on line) from symbol data to
            # performance data
            performance_data.append(int(symbol_data.pop()))
            training_data.append(symbol_data)
        past_data.close()
        return training_data, performance_data
    
    def add_colony(self):
        None