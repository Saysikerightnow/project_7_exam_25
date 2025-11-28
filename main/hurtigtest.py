
import csv
import os
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Initialize and return a chrome webdriver instance. This lets us reuse the driver later on
def setup_driver():
    chrome_options = Options()
    # Run Chrome in headless mode so it doesnt pop op
    # chrome_options.add_argument("--headless=new")
    return webdriver.Chrome(options=chrome_options)


# Load the url, wait for duration info, and return parsed HTML (soup) and duration
def content_scraper(driver, url):
    try:
        print(f"Loading: {url}")

        driver.get(url)
        full_duration = ""

        try:
            duration_span = driver.find_element(By.CLASS_NAME, "duration")
            print("Waiting for duration span to update...")

            # Wait until duration text matches ".../MM:SS" or ".../HH:MM"
            WebDriverWait(driver, 120).until(
                lambda d: re.search(
                    r"/\s*\d+:\d+$",
                    duration_span.text.strip()
                )
            )

            # Extract updated duration
            final_text = duration_span.text.strip()
            full_duration = final_text.split("/")[-1].strip()

            print(f"Duration loaded: {full_duration}")

        except Exception as e:
            print(f"Could not find duration span: {e}")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            return soup, ""

        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup, full_duration

    except Exception as e:
        print(f"Error: {e}")
        return None, ""


# Extract metadata and transcript from parsed HTML
def auto_scraper(soup, full_duration):
    scraped_data = {}
    transcript_content = ""

    scraped_data["speech_duration"] = full_duration if full_duration else ""

    variables = {
        "president_name": "president-name",
        "speech_title": "presidential-speeches--title",
        "speech_date": "episode-date",
        "transcript": "view-transcript",
    }

    # Look for the keys "transcript" and "speech_title" and handle them differently i.e. transcript only gets inner p tag scraped and speech title only gets the title scraped. and not the date before it
    for key, class_name in variables.items():
        content_fetch = soup.find(class_=class_name)
        if content_fetch:
            if key == "transcript":
                transcript_content = ""
                for p in content_fetch.find_all("p"):
                    transcript_content += p.text.strip() + "\n"
                transcript_content = transcript_content.strip()
            elif key == "speech_title":
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
            print(f"{key.capitalize().replace('_', ' ')}: {item}\n")

    if transcript_content:
        print("Transcript saved to a .txt file")
    else:
        print("No content found.")

    return scraped_data, transcript_content

# Save scraped metadata to csv and transcript to .txt organized in folders
def save_data(scraped_data, transcript_content):
    # Main folder for all scraped data
    main_folder = "scraped_data"
    os.makedirs(main_folder, exist_ok=True)
    # Makes a folder based on the presidents name, the speech title and the date og the speech
    president_name_cleaned = scraped_data["president_name"].replace(" ", "_").replace(",", "").replace(":", "").replace("/", "")
    speech_title_cleaned = scraped_data["speech_title"].replace(" ", "_").replace(",", "").replace(":", "").replace("/", "")
    speech_date_cleaned = scraped_data["speech_date"].replace(" ", "_").replace(",", "").replace(":", "").replace("/", "")
    # writes the data into a subfolder for the president based on the specific speech title 
    president_folder = os.path.join(main_folder, president_name_cleaned)
    speech_subfolder_name = f"{speech_title_cleaned}_{speech_date_cleaned}"
    full_speech_folder_path = os.path.join(president_folder, speech_subfolder_name)


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

# Function: Main loop to scrape URLs from a CSV file and save data
def main():
    # create driver once and reuse
    driver = setup_driver()  

    # Read URLs from CSV file
    urls = []
    with open("test_urls.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:  
            if row:
                # assuming each URL is in the first column
                urls.append(row[0])  

    for url in urls:
        soup, full_duration = content_scraper(driver, url)

        if soup == "NO_DURATION":
            print("No duration found, writing placeholder data.")
            # placeholder names should the data be missing. Although redundant
            scraped_data = {               
                "president_name": "Unknown",                
                "speech_title": "No Recording",                
                "speech_date": "Unknown",                
                "speech_duration": "",                
                "status": "No recording available"}
            transcript_content = ""
            save_data(scraped_data, transcript_content)

        elif soup:
            scraped_data, transcript_content = auto_scraper(soup, full_duration)
            save_data(scraped_data, transcript_content)

        else:
            print(f"Skipping {url} - page did not load properly")
    # quit driver once at the end
    driver.quit()  
    print("Done!")

# content_scraper to accept driver and url argument

if __name__ == "__main__":
    main()
