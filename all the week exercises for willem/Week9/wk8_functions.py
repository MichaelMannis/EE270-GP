# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 07:13:25 2019

@author: nas03132
"""

import math

# Calculate price of tree. Returns -1 for trees too short to be sold
# Inputs: height (real number) - height of tree sold
# Outputs: Price of tree
def calculate_price(height):
    if height > 0.6:
           # Calculate in 25cm units, rounding down
        unitheight=height//0.25
        # Add 1 for any part-25-cm units
        if height%0.25>0:
            unitheight=unitheight+1
        price=5.5+2.2*unitheight
        if height > 2.5:
            price=price+3.25
        return price
    else:
        return -1
        
# Update running totals following sale of a tree
# Inputs: price (real number) - price of tree sold
#         totals (list) - running totals [number sold, total height, total money]
def update_totals(price,height,totals):
    if price >= 0:
        totals[0]=totals[0]+1
        totals[1]=totals[1]+price
        totals[2]=totals[2]+height
    return totals

# Update running totals following sale of a tree
# Inputs: price (real number) - price of tree sold
def display_price(price):
    if price >= 0:
        print('Price of tree: £',price)
    elif price == -1:
        print ('That tree is too tall to be sold')
    elif price == -2:
        print ('That tree is too short to be sold')
        
# Inputs: totals (list) - running totals [number sold, total height, total money]
# Outputs: list: [average height, average price]
def calc_averages(totals):
    averages=[]
    
    av_height=totals[1]/totals[0]
    averages.append(math.floor(av_height*10)/10)
    
    av_price=totals[2]/totals[0]
    averages.append(math.floor(av_price*100)/100)
    
    return averages