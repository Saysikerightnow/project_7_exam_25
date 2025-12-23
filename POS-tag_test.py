# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 16:15:23 2025

@author: Bruger
"""

import nltk
from nltk.tokenize import word_tokenize

text = word_tokenize("And now for something completely different")
nltk.pos_tag(text)
[('And', 'CC'), ('now', 'RB'), ('for', 'IN'), ('something', 'NN'),
('completely', 'RB'), ('different', 'JJ')]
text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
#Comparing words in text, fx. woman -man, child
text.similar('woman')
