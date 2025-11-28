# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 13:34:13 2025

@author: Bruger
"""

import requests
from bs4 import BeautifulSoup

link = 'https://millercenter.org/the-presidency/presidential-speeches'

res = requests.get(link)
soup = BeautifulSoup(res.text, 'html.parser')
soup.find_all("field-content")


!pip install selenium
from selenium import webdriver
webdriver.Chrome()
