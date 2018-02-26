import pafy
import os
import re
import urllib
import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3


def main():
    method = int(input("Type Download Method, 1 - from a txt file, 2 - from web scraping, 3 - from youtube playlist"))
    folderD = "C:/Users/User/Documents/Python/Download Youtube/Downloads"

    if method < 1 or method > 3:
        print("Select valid method")
    else:
        if method == 1:
            from_TxtFile(folderD)
        elif method == 2:
            from_Web(folderD)
        elif method == 3:
            print(folderD)

def from_TxtFile(folderD):
    lines = [line.rstrip('\n') for line in open('musicas.txt')]
    for i in range(len(lines)):
        vid = pafy.new(lines[i])
        descr = [vid.author, vid.title, vid.duration]
        print('Autor {}, Título {}, Duraçao {}\n'.format(*descr))
        chckEx = "{}/{}.mp3".format(folderD,descr[1])
        
        if  os.path.isfile(chckEx) == True:
            print("YOU ALREADY DOWNLOAD THIS FILE")
        else:
            download(vid)
            convMp3(descr[1], folderD)
            setMetD(descr[1], folderD)
            print("======DOWNLOAD COMPLETE======\n\n")
    pass


def from_Web(folderD):
    artist = input("Enter the artist")
    song = input("Enter the song")
    descr = "{} -{}".format(artist, song)
    chckEx = "{}/{}.mp3".format(folderD, descr)
    
    if  os.path.isfile(chckEx) == True:
        print("YOU ALREADY DOWNLOAD THIS FILE")
    else:
        search = "{} {}".format(artist, song)
        searchUrl = search.replace(" ", "+")
        url = 'https://youtube.com/results?search_query={}'.format(searchUrl)
        page = urllib.request.urlopen(url)
        html = page.read()
        soup = BeautifulSoup(html, "html.parser")

        urlsRes = []
        n = 0
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            urlsRes.insert(n, 'https://www.youtube.com' + vid['href'])
            print("\n{}".format(vid['title']))
            print("{}\n".format(urlsRes[n]))
            n += 1

        amountD = input("How many links do you want")
        for vid in range(int(amountD)):
            selected = input("Select the download url")
            vid = pafy.new(urlsRes[int(selected)])
            descr = [vid.author, vid.title, vid.duration]
            print('Autor {}, Título {}, Duraçao {}\n'.format(*descr))
            download(vid)
            convMp3(descr[1], folderD)
            setMetD(descr[1], folderD)
            print("======DOWNLOAD COMPLETE======\n\n")
    pass

def download(vid):
    print("\n=======STARTING DOWNLOAD======")
    audio = vid.getbestaudio("m4a")
    filename = audio.download(quiet=False)
    pass

def convMp3(descr, folderD):
    print("\n========CONVERTING TO MP3=======")
    m4a_audio = AudioSegment.from_file("{}.m4a".format(descr), format="m4a")
    m4a_audio.export("{}/{}.mp3".format(folderD, descr), format="mp3", bitrate="128k")
    os.remove("{}.m4a".format(descr))
    pass


def setMetD(descr, folderD):
    print("======SETTING THE METADATA======")
    namArq = "{}.mp3".format(descr)
    song = EasyID3("{}/{}".format(folderD, namArq))
    descSong = namArq.replace(".mp3","")
    artist, title = descSong.split(" - ")
    song["title"] = title
    song["artist"] = artist
    song.save()
    pass
    
        
if __name__ == '__main__':
    main()
