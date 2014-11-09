# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 16:30:50 2014

@author: Alex
"""

from environment_methods import *
from picker_classes import *

try:
    past_data, past_performance = get_past_data()
except:
    morning_data = get_morning_data()
    evening_prices = get_evening_prices()
    symbol_performances = evaluate_symbols(morning_data, evening_prices)
    update_past_data()
    past_data, past_performance = get_past_data()

seattle = DecisionTreeColony(100, past_data, past_performance)