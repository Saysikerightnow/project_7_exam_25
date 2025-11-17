

import requests
from bs4 import BeautifulSoup

# Fetch and parse the page
response = requests.get("https://millercenter.org/the-presidency/presidential-speeches/april-30-1789-first-inaugural-address")
soup = BeautifulSoup(response.content, "html.parser")

# Find the main content container
content_div = soup.find("div", class_="view-transcript")
if content_div:
    for para in content_div.find_all("p"):
        print(para.text.strip())
else:
    print("No article content found.")   
    
    Jeg er verden 