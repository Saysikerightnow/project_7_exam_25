
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

def link_scraper():
# This script uses selenium to auto scroll the url and then parses the conten. at the end it writes every link to a csv file with a row for each link

# Initialize WebDriver
    driver = webdriver.Chrome() 
    url = "https://millercenter.org/the-presidency/presidential-speeches"
    driver.get(url)

    # Automatically scroll the page
    scroll_pause_time = 3  
    # Pause between each scroll
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1
    while True:
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)
        # Check if reaching the end of the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break

    # Fetch the data using BeautifulSoup after all data is loaded
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Process and save the data as needed

    # Close the WebDriver session
    driver.quit()

    content_fetch = soup.find("div", class_="views-infinite-scroll-content-wrapper clearfix")
    links = []

    # For loop to fetch the desired HTML element inside the fetched content
    if content_fetch:
        for a in content_fetch.find_all("a", href=True):
            if "/the-presidency/presidential-speeches/" in a["href"]:
                link = a["href"]
            
                if link not in links:
                    links.append(link)
            # find the desired element and adds it to the empty scraped_data list. also removes spaces
        if links:
            # Loops through the content and prints each paragraf in the original format
            for i, link in enumerate(links, 1):
                print (f"{link} \n")
    else:
        # Loop break in case of no content found within the parametres
        print("No content found.")   

    if links:
        with open("links.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file) 
            
            for link in links:
                writer.writerow([link])
        
        print("Data exported to 'links.csv'.")

link_scraper()


