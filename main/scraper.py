
import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# start chrome driver and add anti popup cookies
def setup_driver():
    # adds the ability to include options
    chrome_options = Options()
    # runs the selenium popup browser in "headless" mode which is "invisible" thus no popup/runs in the background
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    # load base site once to set cookies
    driver.get("https://millercenter.org")

    # add anti popup cookies so the site thinks we've been there before
    driver.add_cookie({"name": "has_seen_email_popup", "value": "true"})
    driver.add_cookie({"name": "newsletter_subscribed", "value": "1"})

    # reload so cookies take effect
    driver.get("https://millercenter.org")

    print("anti popup cookies added")
    return driver

# load url and then return the HTML
def download_html(driver, url):
    print(f"loading {url}")
    driver.get(url)

    html_content = driver.page_source
    return html_content

# save html as speech_1, speech_2, in a folder
def save_html_file(html_content, index):
    # makes the directory if it doesnt exist
    os.makedirs("html_pages", exist_ok=True)
    file_path = os.path.join("html_pages", f"speech_{index}.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"saved html: {file_path}")

# main function to handle url reading
def main():
    driver = setup_driver()

    # read urls from csv
    urls = []
    with open("urls.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                urls.append(row[0])

    # loop through urls and save numbered html files
    for i, url in enumerate(urls, start=1):
        html_content = download_html(driver, url)
        save_html_file(html_content, i)

    driver.quit()
    print("all html files downloaded.")

if __name__ == "__main__":
    main()
