import urllib
import time

urls = ["https://www.lyricsfreak.com/f/frank+sinatra/",
        "https://www.lyricsfreak.com/n/nirvana/",
        "https://www.lyricsfreak.com/t/taylor+swift/"]

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

for i in range(len(urls)):
    try:
        name = urls[i].split('/')[-2]
        request = urllib.request.Request( urls[i], None, headers )
        response = urllib.request.urlopen( request )
        with open(name+".html", 'w',encoding="utf-8") as f:
            f.write(str(response.read().decode('utf-8')))
        time.sleep(1)
    except urllib.error.HTTPError as e:
        print(e)

        