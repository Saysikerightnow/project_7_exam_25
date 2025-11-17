import urllib
from bs4 import BeautifulSoup
import os

os.mkdir("nirvana")

page = open('nirvana.html','r',encoding='utf-8').read()
soup = BeautifulSoup(page,features="lxml")
songs = soup.findAll('div',attrs={'class':'js-sort-table-content-item'})

for song in songs:
    link = song.find('a')
    name = link.text.strip().replace(' Lyrics','')
    try:
        print("Getting lyrics for:",name)
        url = 'https://www.lyricsfreak.com'+link['href']
        urllib.request.urlretrieve(url,"nirvana/"+name.replace('/','-')+".html")
    except KeyError:
        print("No lyrics available for:",name)
        
        
        
        