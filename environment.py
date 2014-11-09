# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 16:30:50 2014

@author: Alex
"""

import environment_methods as em
import picker_classes as pc

try:
    past_data, past_performance = em.get_past_data()
except:
    morning_data = em.get_morning_data()
    evening_prices = em.get_evening_prices()
    symbol_performances = em.evaluate_symbols(morning_data, evening_prices)
    em.update_past_data()
    past_data, past_performance = em.get_past_data()

seattle = pc.DecisionTreeColony(100, past_data, past_performance)