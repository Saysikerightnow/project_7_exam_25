# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 15:14:44 2025

@author: Bruger
"""

import requests

url = 'https://millercenter.org/the-presidency/presidential-speeches/september-30-2025-remarks-military-leaders'
html_output_name = 'test3.html'

req = requests.get(url, 'html.parser', headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'})

with open(html_output_name, 'w') as f:
    f.write(req.text)
    f.close()
