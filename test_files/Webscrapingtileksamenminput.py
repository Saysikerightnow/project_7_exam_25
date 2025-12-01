# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 13:39:14 2025

@author: Bruger
"""


import requests
from bs4 import BeautifulSoup

url = input("Insert https-adress")
response = requests.get(url)
print(response.status_code)
print(response.content)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
print (soup.prettify())
s = soup.find('div', class_='view-transcript')