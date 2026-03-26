# -*- coding: utf-8 -*-
"""
Calculate and expansion of (x+1)^n, in part or in full

Created on Wed Feb 20 19:39:43 2019

@author: nas03132
"""

import coefficients as co

n=int(input('Enter integer power of (x+1): '))
# Set up dummy value of c to get into the loop
term=-2
while term<-1 or term>n:
    term=input('Enter term number, staring at 0 (or "all"): ')
    if term=='all':
        # Translate at once to special integer before testing loop condition
        term=-1
    else:
        term=int(term)
    
print()
if term!=-1:
    coeff=co.calc_coeff(n,term)
    # print the common part of the output
    print ('Term ',term,' of the expansion of (x+1)^',n,' is ',sep='',end='' )
    co.print_coeff(term,coeff)
    print()
        
else:
    print("executes")
    term=n
    print ('Expansion is ',end='')
    while term>0:
        coeff=co.calc_coeff(term,n)
        co.print_coeff(term,coeff)
        if term>0:
            print(' + ',end='')
        term=term-1
    print()
    