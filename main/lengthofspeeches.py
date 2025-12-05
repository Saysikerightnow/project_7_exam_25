# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 11:13:18 2025

@author: Bruger
"""

import os

def counter(fname):
    
    # variable to store total word count
    num_words = 0
    
    # variable to store total line count
    num_lines = 0
    
    # variable to store total character count
    num_charc = 0
    
    # variable to store total space count
    num_spaces = 0
    
    # opening file using with() method
    # so that file gets closed
    # after completion of work
    with open(fname, 'r') as f:
        
        # loop to iterate file
        # line by line
        for line in f:
            
            # separating a line from \n character
            # and storing again in line
            line = line.strip(os.linesep)
            
            # splitting the line
            wordslist = line.split()
            
            # incrementing value of num_lines
            num_lines = num_lines + 1
            
            # incrementing value of num_word
            num_words = num_words + len(wordslist)
            
            # incrementing value of num_char
            num_charc = num_charc + sum(1 for c in line
                        if c not in (os.linesep, ' '))
            
            # incrementing value of num_space
            num_spaces = num_spaces + sum(1 for s in line
                                if s in (os.linesep, ' '))
    
    # printing total word count
    print("Number of words in text file: ",
          num_words)
    
    # printing total line count
    print("Number of lines in text file: ",
          num_lines)
    
    # printing total character count
    print("Number of characters in text file: ",
          num_charc)
    
    # printing total space count
    print("Number of spaces in text file: ",
          num_spaces)

# Driver Code:
if __name__ == '__main__':
    fname = 'test.txt'
    try:
        counter(fname)
    except:
        print('File not found')