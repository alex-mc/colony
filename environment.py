# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 13:39:02 2014

@author: Alex
"""

from values import symbol_list
import ystockquote as ys

def get_morning_data():
    """Retrieve all data available from ystockquote for each known symbol. This
    data is classified by pickers and added to past data once evening prices
    are obtained.  This method should be run in the morning to allow pickers
    to make their picks."""
    current_data = {}
    for symbol in symbol_list:
        current_data[symbol] = ys.get_all(symbol)
    return current_data

def get_evening_prices():
    """Retrieve price for each symbol.  This method should be run in the
    evening so that picker's picks can be evaluated."""
    new_data = {}
    for symbol in symbol_list:
        new_data[symbol] = ys.get_price(symbol)
    return new_data

def evaluate_symbols(current_data, new_data):
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
        morning_price = current_data[symbol][price]
        evening_price = new_data[symbol]
        price_change = (evening_price - morning_price) / morning_price
        if price_change > 0.05:
            performance = 2
        elif price_change > 0.005:
            performance = 1
        elif price_change > 0.005:
            performance = 0
        elif price_change >= 0.025:
            performance = -1
        elif price_change < 0.025:
            performance = -2
        symbol_performances[symbol] = performance
    return symbol_performances

def update_past_data(current_data, symbol_performances):
    """Append current day's data and performance to past data.  Past data
    represents training data."""
    past_data = open('past_data.txt', 'a')
    for symbol in symbol_list:
        for k, v in current_data[symbol]:
            past_data.write(k)
            past_data.write(',')
            past_data.write(v)
            past_data.write(';')
        past_data.write('performance,')
        past_data.write(symbol_performances[symbol])
        past_data.write('\n')
    past_data.close()

def get_past_data():
    """Read past data from file into feature and class lists for training."""
    training_data = []
    past_data = open('past_data.txt', 'a')
    for line in past_data:
        line = line.split(';')
        symbol_data = []
        performance_data = []
        for data_element in line:
            data_element = data_element.split(',')
            value = data_element[1]
            symbol_data.append(value)
        
        # move performance value (last value on line) from symbol data to
        # performance data
        performance_data.append(symbol_data.pop())
        training_data.append(symbol_data)
    return training_data, performance_data