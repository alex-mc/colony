# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 13:19:12 2014

@author: Alex
"""

import re

nasdaq_symbols = []
nasdaq_listed = open('nasdaqlisted.txt', 'r')

for line in nasdaq_listed:
    line = line.split('|')
    if not '.' in line[0] and not ':' in line[0]:
        nasdaq_symbols.append(line[0])

print(nasdaq_symbols)