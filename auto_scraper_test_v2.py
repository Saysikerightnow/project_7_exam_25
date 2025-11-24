
import requests
from bs4 import BeautifulSoup
import csv
import os

# First we want to fetch and parse the desired page for future use
def content_scraper():
    # Fetch and parse the page for future use
    url = input("Insert url for desired content \n")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Return "soup" i.e. our parsed content for use in subsequent functions
    return soup

def auto_scraper(soup):
    # Create an empty list to hold the fetched content
    scraped_data = {}
    transcript_content = ""
    # Define a set of variables in a dictionary for the tool to search for
    variables = {
    "president_name": "president-name",
        # in div class= about this episode on the sidebar
    "speech_title": "presidential-speeches--title",
        # Contains both date and title of the speech. must be spliced before appending
    "speech_date": "episode-date",
        # In the sidebar div class= "about-this-episode--inner"
    "speech_duration": "duration",
        # in div class="audio-player-wrapper"
    "transcript": "view-transcript",
        # Transcript in view-transcript
    }

    # Now fetch only the desired content from the page
    # for loop. for every key (variable) and class in variable. do the following
    for key, class_name in variables.items():
        # fetch the content. create a grabable container (content_fetch)
        content_fetch = soup.find(class_=class_name)
        # Start the arguements for handling the content
        if content_fetch:
            # If the content key is = "transcript", then 
            if key == "transcript":
                # remove all spaces and html tags. keeps only the text inside content_fetch
                transcript_content = content_fetch.text.strip()
            elif key == "speech_title":
                # remove all spaces and html tags. keeps only the text inside content_fetch
                full_text = content_fetch.text.strip()
                # Removes everything before the ":" sign in the speech title as the line always includes date as well as title
                # strips the undesired part of the title
                if ": " in full_text:
                    # splits the text at the first occurrence of : and only the first. i.e. "1"
                    parts = full_text.split(": ", 1)
                    # if it happened, keep the second part of the split text. if not. keep the entire text
                    title_part = parts[1].strip() if len(parts) > 1 else full_text
                    # store the extracted text in a specific key (title_part)
                    scraped_data[key] = title_part
                else:
                    scraped_data[key] = full_text
            else:
                scraped_data[key] = content_fetch.text.strip()
    if scraped_data:
        # Formats and prints keys with capital first letter and removes underscore and space
        for key, item in scraped_data.items():
            print(f"{key.capitalize().replace("_", " ")}: {item} \n")
            if transcript_content:
                print("Transcript saved to a .txt file")
    else:
        print("No content found.")
    
    # Now that we have fetched, parsed and handled the data, we want to write the content into a csv and txt file

    # Use CSV write and define title based on variables
    # Prepare Folder Names
    president_name_cleaned = scraped_data["president_name"].replace(" ", "_").replace(",", "").replace(":", "").replace("/", "")
    # takes the scraped data then assigns a file name for president_name_cleaned based on scraped data info
    speech_title_cleaned = scraped_data["speech_title"].replace(" ", "_").replace(",", "").replace(":", "").replace("/", "")
    # the same for title and date
    speech_date_cleaned = scraped_data["speech_date"].replace(" ", "_").replace(",", "").replace(":", "").replace("/", "")

    # Now we want to create a folder for each president name and a subfolder for each speech
    # Top level folder for the President
    president_folder = president_name_cleaned

    # Subfolder for the specific speech. This name will also be used for the CSV file.
    speech_subfolder_name = f"{speech_title_cleaned}_{speech_date_cleaned}"

    # Combine them to get the full path for the speech's folder
    full_speech_folder_path = os.path.join(president_folder, speech_subfolder_name)

    # using the os import we are going to create folders for each speech
    try:
        os.makedirs(full_speech_folder_path, exist_ok=True)
        print(f"Created folder structure: '{full_speech_folder_path}'")
    except Exception as e:
        print(f"Error creating folders '{full_speech_folder_path}': {e}")
        return
    
    if scraped_data:
        csv_internal_filename = f"{speech_subfolder_name}.csv"
        csv_full_path = os.path.join(full_speech_folder_path, csv_internal_filename)

        with open(csv_full_path, "w", newline="", encoding="utf-8") as file:
            fieldnames = scraped_data.keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(scraped_data)
        print(f"Metadata exported to '{csv_full_path}'.")
    else:
        print("No metadata to export to CSV.")

    if transcript_content:
        txt_internal_filename = "transcript.txt"
        txt_full_path = os.path.join(full_speech_folder_path, txt_internal_filename)

        with open(txt_full_path, "w", encoding="utf-8") as file:
            file.write(transcript_content)
        print(f"Transcript exported to '{txt_full_path}'.")
    else:
        print("No transcript to export to .txt file.")

soup = content_scraper()
auto_scraper(soup)

