# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 07:32:30 2019

@author: nas03132
"""

import wk8_functions as f

totals=[0,0,0]
height=float(input('Enter height of tree: '))

while height >=0:
    price=f.calculate_price(height)
    totals=f.update_totals(price,height,totals)
    f.display_price(price)
    height=float(input('Enter height of tree: '))
    
averages=f.calc_averages(totals)
print ('Total number of trees sold:',totals[0])
print ('Average height of trees sold:',averages[0])
print ('Total amount of money taken: £',totals[2],sep='')
print ('Average price of trees sold: £',averages[1],sep='')