import urllib
from bs4 import BeautifulSoup
import os
import time

os.mkdir("nirvana")

page = open('nirvana.html','r',encoding='utf-8').read()
soup = BeautifulSoup(page,features="lxml")

songs = soup.findAll('div',attrs={'class':'js-sort-table-content-item'})

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

for song in songs:
    link = song.find('a')
    name = link.text.strip().replace(' Lyrics','')
    try:
        print("Getting lyrics for:",name)
        url = 'https://www.lyricsfreak.com'+link['href']
        request = urllib.request.Request( url, None, headers )
        response = urllib.request.urlopen( request )
        with open("nirvana/"+name.replace('/','-')+".html", 'w',encoding="utf-8") as f:
            f.write(str(response.read().decode('utf-8')))
        time.sleep(1)
    except KeyError:
        print("No lyrics available for:",name)
    except urllib.error.HTTPError as e:
        print(e)        
        
        
        