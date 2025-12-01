# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 11:07:33 2025

@author: Bruger
"""

import requests
from bs4 import BeautifulSoup
url = 'https://millercenter.org/the-presidency/presidential-speeches'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
soup.find_all("views-row")

# Selenium setup
from selenium import webdriver
driver = webdriver.Chrome()
from selenium.webdriver.common.by import By
driver.get('https://millercenter.org/the-presidency/presidential-speeches')



