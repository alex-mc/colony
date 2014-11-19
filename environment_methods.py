# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 13:39:02 2014

@author: Alex
"""

from values import symbol_list
import ystockquote as ys
from time import sleep
import random
import string

def get_morning_data():
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
    return current_data

def get_evening_prices():
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
        morning_price = float(current_data[symbol]['price'])
        evening_price = float(new_data[symbol])
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
    return symbol_performances

def update_past_data(current_data, symbol_performances):
    """Append current day's data and performance to past data.  Past data
    represents training data."""
    past_data = open('past_data.txt', 'a')
    for symbol in symbol_list:
        for k, v in current_data[symbol].items():
            v = return_data_value_as_number(v)
            past_data.write(k)
            past_data.write(',')
            past_data.write(str(v))
            past_data.write(';')
        past_data.write('performance,')
        past_data.write(str(symbol_performances[symbol]))
        past_data.write('\n')
    past_data.close()

def get_past_data():
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

def return_data_value_as_number(data_value):
    try:
        data_value = float(data_value)
    except:
        data_value = str(data_value)
        if data_value.endswith('M'):
            data_value = data_value.strip('M')
            data_value = float(data_value) * (1000 ** 2)
        elif data_value.endswith('B'):
            data_value = data_value.strip('B')
            data_value = float(data_value) * (1000 ** 3)
        else:
            data_value = 0.0
    return data_value
    
def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))