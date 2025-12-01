# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 16:42:47 2025

@author: Bruger
"""

c = 0

# Opening our text file in read only mode
with open(r'SampleFile.txt','r') as file:

    data = file.read()
    
    w = data.split()
    
    c += len(w)

print(c)