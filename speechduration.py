# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 10:47:29 2025

@author: Bruger
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def pageLoad(url):
    dr = webdriver.Chrome()
    dr.get(pageUrl)
    wait = 5
    try:
      	#Checking our desired element is loaded or not
        element = WebDriverWait(dr, wait).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 
                                            '#block-mainpagecontent > article > div > div.presidential-speeches--body-wrapper > div.audio-player-wrapper > div > div.controls > span')))
        print("You can procced to scrape the data.....\n")

        #We are now performing actions with our desired element
        c=1
        print("Our Web Dev Courses :-")
        for i in dr.find_elements(By.CSS_SELECTOR,
                                  '#block-mainpagecontent > article > div > div.presidential-speeches--body-wrapper > div.audio-player-wrapper > div > div.controls > span'):
          print(str(c)+". ",i.text)
          c += 1
    except TimeoutException:
      	#If our desired element is not found
        print("An ERROR Occured!!!!")

    dr.quit()

if __name__ == "__main__":
    
    #our url in which we want to visit and perform actions
    pageUrl = "https://millercenter.org/the-presidency/presidential-speeches"
    pageLoad(pageUrl)