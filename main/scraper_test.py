import os
import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

# start the chrome driver
def setup_driver():
    chrome_options = Options()
    # run in background
    # chrome_options.add_argument("--headless=new")  
    return webdriver.Chrome(options=chrome_options)

# load url, wait for duration span, return html and duration
def download_html(driver, url):
    print(f"Loading: {url}")
    driver.get(url)
    full_duration = ""

    # wait for the duration span if it exists
    try:
        duration_span = driver.find_element(By.CLASS_NAME, "duration")
        print("Waiting for duration span to update...")

        WebDriverWait(driver, 120).until(
            lambda d: re.search(r"/\s*\d+:\d+$", duration_span.text.strip())
        )

        final_text = duration_span.text.strip()
        full_duration = final_text.split("/")[-1].strip()
        print(f"Duration loaded: {full_duration}")

    except Exception as e:
        print(f"Could not find duration span: {e}")

    html_content = driver.page_source
    return html_content, full_duration

# clean text for safe folder/file names
def clean_text(text):
    return "".join(c for c in text if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")

# extract metadata for folder organization
def extract_metadata(soup):
    president_tag = soup.find(class_="president-name")
    title_tag = soup.find(class_="presidential-speeches--title")
    date_tag = soup.find(class_="episode-date")

    president_name = president_tag.text.strip() if president_tag else "Unknown_President"

    if title_tag:
        full_text = title_tag.text.strip()
        speech_title = full_text.split(": ", 1)[1].strip() if ": " in full_text else full_text
    else:
        speech_title = "Unknown_Speech"

    speech_date = date_tag.text.strip() if date_tag else "Unknown_Date"

    return president_name, speech_title, speech_date

# save html in structured folders
def save_html_file(html_content, president_name, speech_title, speech_date):
    president_clean = clean_text(president_name)
    title_clean = clean_text(speech_title)
    date_clean = clean_text(speech_date)

    folder_path = os.path.join("html_pages", president_clean, f"{title_clean}_{date_clean}")
    os.makedirs(folder_path, exist_ok=True)

    html_file = os.path.join(folder_path, "page.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Saved HTML: {html_file}")

# main function
def main():
    driver = setup_driver()

    # read urls from CSV
    urls = []
    with open("test_urls.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                urls.append(row[0])

    # loop through urls
    for url in urls:
        html_content, full_duration = download_html(driver, url)
        soup = BeautifulSoup(html_content, "html.parser")
        president_name, speech_title, speech_date = extract_metadata(soup)
        save_html_file(html_content, president_name, speech_title, speech_date)
        print(f"Speech duration: {full_duration}\n")

    driver.quit()
    print("All HTML pages downloaded!")

if __name__ == "__main__":
    main()
