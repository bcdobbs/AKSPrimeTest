4# -*- coding: utf-8 -*-
"""
Main Script for Prime Test
Created on Tue Apr 11 21:19:20 2017
@author: Ben Dobbs

Imports class containing the AKS Prime Algorithm. 
Contained in AKSTest.py
This is where the heart of the code is.
"""

from AKSTest import AKSTest

import sys

InputNumber = 0

#Ask for a number to be entered to test. Catches error if not a number.
while True:
    try:
        InputNumber = int(input('Enter number to test:'))
        break
    
    except ValueError:
        print('You must enter a  number.')
        
    except:
        sys.exit(0)
 
"""
Create a new object based on the AKSTest Class and gives the number
entered as a parameter. The alogrithm runs as soon as object is created.
"""   
objAKS = AKSTest(InputNumber)

"""
Prints out the key outputs from the alorithm
"""

print("Is the number prime? " + str(objAKS.IsPrime()))
print("Answer String: " + objAKS.GetAnswer())
print("Smallest R Value: " + str(objAKS.GetSmallestR()))
