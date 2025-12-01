

import requests
from bs4 import BeautifulSoup

# Fetch and parse the page
response = requests.get("https://millercenter.org/the-presidency/presidential-speeches/april-30-1789-first-inaugural-address")
soup = BeautifulSoup(response.content, "html.parser")

# Fetch the desired content from the page
content_fetch = soup.find("div", class_="view-transcript")
scraped_data = []

# For loop to fetch the desired HTML element inside the fetched content
if content_fetch:
    for para in content_fetch.find_all("p"):
        # find the desired element and adds it to the empty scraped_data list. also removes spaces
        scraped_data.append(para.text.strip())
    if scraped_data:
        # Loops through the content and prints each paragraf in the original format
        for i, paragraph in enumerate(scraped_data, 1):
            print (f"{paragraph} \n")
else:
    # Loop break in case of no content found within the parametres
    print("No content found.")   



