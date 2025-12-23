import os
import csv
from bs4 import BeautifulSoup

# extract metadata and transcript from parsed html
def auto_parser(soup):
    scraped_data = {}
    transcript_content = ""
    variables = {
        "president_name": "president-name",
        "speech_title": "presidential-speeches--title",
        "speech_date": "episode-date",
        "transcript": "view-transcript",
    }
    # find the desired keys, i.e. our variables, in the soup content from the html file
    for key, class_name in variables.items():
        content_fetch = soup.find(class_=class_name)
        if content_fetch:
            # for the transcript, find the html container and extract only the content from the "p" tags
            if key == "transcript":
                transcript_content = ""
                for p in content_fetch.find_all("p"):
                    transcript_content += p.text.strip() + "\n"
                transcript_content = transcript_content.strip()
            # for the speech title, do the same as above, but this time strip everything before the colon ":" as the format is the same for every single page
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

    if transcript_content:
        print("transcript saved to txt file")
    else:
        print("no content found")

    return scraped_data, transcript_content

# clean text for safe folder/file names
def clean_text(text):
    return "".join(c for c in text if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")

# save scraped metadata to csv and transcript to txt
def save_data(scraped_data, transcript_content):
    if not scraped_data:
        print("Skipping save_data(): empty scraped_data")
        return
    # create the main folder if it doesnt exist.
    main_folder = "scraped_data"
    os.makedirs(main_folder, exist_ok=True)
    # find metadata for folder naming further on
    president_name_cleaned = clean_text(scraped_data.get("president_name", "unknown"))
    speech_title_cleaned = clean_text(scraped_data.get("speech_title", "unknown"))
    speech_date_cleaned = clean_text(scraped_data.get("speech_date", "unknown"))

    # find and join the structure for each president, the speech subfolder and the full speech folder path
    president_folder = os.path.join(main_folder, president_name_cleaned)
    speech_subfolder_name = f"{speech_title_cleaned}_{speech_date_cleaned}"
    full_speech_folder_path = os.path.join(president_folder, speech_subfolder_name)

    # make the folder structure if it doesnt exist
    try:
        os.makedirs(full_speech_folder_path, exist_ok=True)
        print(f"created folder structure {full_speech_folder_path}")
    except Exception as e:
        print(f"error creating folders {full_speech_folder_path} {e}")
        return

    # csv export
    csv_metadata_path = os.path.join(main_folder, "metadata.csv")
    file_exists = os.path.isfile(csv_metadata_path)
    # write the extracted metadata to the csv file based on the keys from our variables
    with open(csv_metadata_path, "a", newline="", encoding="utf-8") as file:
        # create the keys "id"s from our variables
        fieldnames = scraped_data.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(scraped_data)
        print(f"metadata exported to {csv_metadata_path}")

    # txt export
    if transcript_content:
        txt_internal_filename = "transcript.txt"
        txt_full_path = os.path.join(full_speech_folder_path, txt_internal_filename)
        with open(txt_full_path, "w", encoding="utf-8") as file:
            file.write(transcript_content)
        print(f"transcript exported to {txt_full_path}")
    else:
        print("no transcript to export to txt file")

# count words from transcript
def wordcounter(transcript_content):
    num_words = 0
    for line in transcript_content.splitlines():
        words = line.split()
        num_words += len(words)
    return num_words

# main parser loop
def main():
    folder = "html_pages"
    html_files = [f for f in os.listdir(folder) if f.endswith(".html")]

    # iterate over each html file in the file folder
    for html_file in html_files:
        file_path = os.path.join(folder, html_file)
        print(f"\n processing file {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")
        scraped_data, transcript_content = auto_parser(soup)

        # do the word count from transcript
        if transcript_content and scraped_data:
            num_words = wordcounter(transcript_content)
            scraped_data["speech_duration"] = num_words
            print(f"speech word count: {num_words}")
        elif scraped_data:
            scraped_data["speech_duration"] = 0

        save_data(scraped_data, transcript_content)

    print("\n done parsing all html files")

if __name__ == "__main__":
    main()
