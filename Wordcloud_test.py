# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 15:27:03 2025

@author: Bruger
"""
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import sys, os
#Specify directory, not necessary
os.chdir(sys.path[0])

# Read text
text = open("test.txt", mode= "r", encoding="utf-8").read()
stopwords = STOPWORDS

wc= WordCloud(
    background_color="white",
    stopwords=stopwords,
    height=600,
    width=400
    )

wc.generate(text)

#Save as a file
wc.to_file("wordcloud_output.png")
