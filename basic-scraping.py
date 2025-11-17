
import urllib

urls = ["https://www.lyricsfreak.com/f/frank+sinatra/",
        "https://www.lyricsfreak.com/n/nirvana/",
        "https://www.lyricsfreak.com/t/taylor+swift/"]

for i in range(len(urls)):
    name = urls[i].split('/')[-2]
    urllib.request.urlretrieve(urls[i],name+".html")
