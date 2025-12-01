

# Den virker nu og virker baseret på url, class name og inner tag

import requests
from bs4 import BeautifulSoup

def content_scraper():
    # Fetch and parse the page
    url = input("Insert url for desired content \n")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def get_desired_data(soup):
    # Empty list to hold the fetched content later on
    scraped_data = []

    # Stores input in variables for clarity sake
    element = input("enter the element tag fx. div \n")
    class_name = input("enter the class name fx. view-transcript \n")
    inner_tag = input("enter the inner tag to search for fx. p or h2\n")

    # Fetches the desired content from the page
    content_fetch = soup.find(element, class_=class_name)

    # For loop to fetch the desired HTML element inside the fetched content
    if content_fetch:
        if inner_tag == "p":
            for item in content_fetch.find_all("p"):
                scraped_data.append(item.text.strip())
        else:
            # Otherwise, scrape the specified inner_tag ex. h2
            for item in content_fetch.find_all(inner_tag):
                # find the desired element and adds it to the empty scraped_data list.
                scraped_data.append(item.text.strip())

    if scraped_data:
        # Loops through the content and prints each paragraf in the original format
        for i, paragraph in enumerate(scraped_data, 1):
            print (f"{paragraph} \n")
    else:
    # Loop break in case of no content found within the parametres
        print("No content found.") 

soup = content_scraper()
get_desired_data(soup)



    