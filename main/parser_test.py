import os
import csv
from bs4 import BeautifulSoup

# extract metadata and transcript from parsed html
def auto_parser(soup, full_duration=""):
    scraped_data = {}
    transcript_content = ""
    scraped_data["speech_duration"] = full_duration if full_duration else ""
    variables = {
        "president_name": "president-name",
        "speech_title": "presidential-speeches--title",
        "speech_date": "episode-date",
        "transcript": "view-transcript",
    }

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
            print(f"{key.replace('_', ' ')} {item}")

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
    main_folder = "scraped_data"
    os.makedirs(main_folder, exist_ok=True)

    president_name_cleaned = clean_text(scraped_data.get("president_name", "unknown"))
    speech_title_cleaned = clean_text(scraped_data.get("speech_title", "unknown"))
    speech_date_cleaned = clean_text(scraped_data.get("speech_date", "unknown"))

    president_folder = os.path.join(main_folder, president_name_cleaned)
    speech_subfolder_name = f"{speech_title_cleaned}_{speech_date_cleaned}"
    full_speech_folder_path = os.path.join(president_folder, speech_subfolder_name)

    try:
        os.makedirs(full_speech_folder_path, exist_ok=True)
        print(f"created folder structure {full_speech_folder_path}")
    except Exception as e:
        print(f"error creating folders {full_speech_folder_path} {e}")
        return

    if scraped_data:
        csv_internal_filename = f"{speech_subfolder_name}.csv"
        csv_full_path = os.path.join(full_speech_folder_path, csv_internal_filename)
        with open(csv_full_path, "w", newline="", encoding="utf-8") as file:
            fieldnames = scraped_data.keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(scraped_data)
        print(f"metadata exported to {csv_full_path}")
    else:
        print("no metadata to export to csv")

    if transcript_content:
        txt_internal_filename = "transcript.txt"
        txt_full_path = os.path.join(full_speech_folder_path, txt_internal_filename)
        with open(txt_full_path, "w", encoding="utf-8") as file:
            file.write(transcript_content)
        print(f"transcript exported to {txt_full_path}")
    else:
        print("no transcript to export to txt file")

# main parser loop
def main():
    folder = "html_pages"
    html_files = [f for f in os.listdir(folder) if f.endswith(".html")]

    for html_file in html_files:
        file_path = os.path.join(folder, html_file)
        print(f"processing file {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # extract duration if available in html
        duration_span = soup.find(class_="duration")
        full_duration = duration_span.text.strip().split("/")[-1] if duration_span else ""

        scraped_data, transcript_content = auto_parser(soup, full_duration)
        save_data(scraped_data, transcript_content)

    print("done parsing all html files")

if __name__ == "__main__":
    main()
