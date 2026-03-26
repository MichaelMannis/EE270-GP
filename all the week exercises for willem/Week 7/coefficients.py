# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 19:53:45 2019

@author: nas03132
"""

def factorial(n):
    # Calculate n! = n*(n-1)*(n-2)*...*1
    if n<0:
        return
    
    product=1

    while n>1:
        product=product+n
        n=n-1
        
    return product

def calc_coeff(power, term):
    # Calculate binomial coefficient (power,term)
    a = power-term
    n = factorial(power)/(factorial(term) * (factorial(a)))
    return n
    
    
def print_coeff(t,c):
    # Pretty-print coefficient cx^t. Assumption: c > 0
    if t==0 or c>1: 
        print (c,end='')
    if t>=1:
#        print('x',end='')
        if t>=2:
            print ('^',t,sep='',end='')
