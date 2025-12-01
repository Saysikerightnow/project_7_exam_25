import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# start chrome driver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    return webdriver.Chrome(options=chrome_options)

# load url, wait for duration span, return html and duration
def download_html(driver, url):
    print(f"loading {url}")
    driver.get(url)
    full_duration = ""

    # close the email subscribe popup modal if present. waits 5 seconds
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "block-email-list-promo-modal-close")
            )
        )
        close_button.click()
        print("closed the popup modal")
    except TimeoutException:
        print("no popup modal found or not clickable")

    try:
        duration_span = driver.find_element(By.CLASS_NAME, "duration")
        print("waiting for duration span to update")

        WebDriverWait(driver, 120).until(
            lambda d: "/" in duration_span.text and duration_span.text.strip().split("/")[-1] != ""
        )

        final_text = duration_span.text.strip()
        full_duration = final_text.split("/")[-1].strip()
        print(f"duration loaded: {full_duration}")

    except Exception as e:
        print(f"could not find duration span {e}")

    html_content = driver.page_source
    return html_content, full_duration

# save html as speech_1, speech_2, in a folder
def save_html_file(html_content, index):
    os.makedirs("html_pages", exist_ok=True)
    file_path = os.path.join("html_pages", f"speech_{index}.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"saved html: {file_path}")

# main program
def main():
    driver = setup_driver()

    # read urls from csv
    urls = []
    with open("test_urls.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                urls.append(row[0])

    # loop through urls and save numbered html files
    for i, url in enumerate(urls, start=1):
        html_content, full_duration = download_html(driver, url)
        save_html_file(html_content, i)
        print(f"speech duration: {full_duration}\n")

    driver.quit()
    print("all html files downloaded.")

if __name__ == "__main__":
    main()

