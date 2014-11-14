# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 16:30:50 2014

@author: Alex
"""

import environment_methods as em
import picker_classes as pc
from time import clock, sleep

start = clock()
morning_data = em.get_morning_data()
print(str(len(morning_data.keys())), "morning data points obtained in", str(clock() - start) + "s")

#wait(8 * 3600)

start = clock()
evening_prices = em.get_evening_prices()
print(str(len(evening_prices.keys())), "evening prices obtained in", str(clock() - start) + "s")

start = clock()
symbol_performances = em.evaluate_symbols(morning_data, evening_prices)
print(str(len(symbol_performances.keys())), "symbols evaluated in", str(clock() - start) + "s")

start = clock()
em.update_past_data()
past_data, past_performance = em.get_past_data()
print("Past data updated and retrieved in", str(clock() - start) + "s")

seattle = pc.DecisionTreeColony(100, past_data, past_performance)
