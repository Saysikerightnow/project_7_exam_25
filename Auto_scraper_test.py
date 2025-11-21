
# The intended function is to automatically find and print the desired content from any url input based on the assignments variabled

import requests
from bs4 import BeautifulSoup
import csv

def content_scraper():
    # Fetch and parse the page
    url = input("Insert url for desired content \n")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def auto_scraper(soup):
    # Empty list to hold the fetched content later on
    scraped_data = {}

    variables = {
        # Constant variables for the script to search for
    # "transcript": "view-transcript",
        # the transcript minus the word transcript
    "president_name": "president-name",
        # in div class= about this episode on the sidebar
    "speech_title": "presidential-speeches--title",
        # Contains both date and title of the speech. must be spliced before appending
    "speech_date": "episode-date",
        # In the sidebar div class= "about-this-episode--inner"
    "speech_duration": "duration",
        # in div class="audio-player-wrapper"
    "speech_description": "about-sidebar--intro",
        # In the side bar
    "source": "speech-loc"
        # Side bar
        }
    
    # Fetches the desired content from the page
    for key, class_name in variables.items(): 
        content_fetch = soup.find("div", class_=class_name) or soup.find(class_=class_name)
        if content_fetch:
            if key == "speech_title":
                full_text = content_fetch.text.strip()
                if ": " in full_text:
                    parts = full_text.split(": ", 1)
                    title_part = parts[1].strip() if len(parts) > 1 else full_text
                    scraped_data[key] = title_part
                else:
                    scraped_data[key] = full_text
            else:
                scraped_data[key] = content_fetch.text.strip()
    if scraped_data:
        for key, item in scraped_data.items():
            print(f"{key.capitalize().replace("_", " ")}: {item} \n")
    else:
        print("No content found.")

    # Faulty csv export. bad format and keeps key in before content. 
    if scraped_data:
        with open("scraped_data.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file) if len(scraped_data) == 1 else csv.DictWriter(file, fieldnames=scraped_data.keys()) 
            if isinstance(writer, csv.DictWriter):
                writer.writeheader()
            writer.writerow(scraped_data)
        print("Data exported to 'scraped_data.csv'.")

soup = content_scraper()
auto_scraper(soup)

