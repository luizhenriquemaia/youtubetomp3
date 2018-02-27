import pafy
import os
import re
import urllib
import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3


def main():
    method = int(input("Type Download Method, 1 - from a txt file, 2 - from web scraping, 3 - from youtube playlist "))
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
        nameArq = re.sub(r'([^\s\w]|)_+', '', descr[1])
        nameArq = nameArq.replace("  ", " - ")
        print('Autor {}, Título {}, Duraçao {}\n'.format(*descr))
        chckEx = "{}/{}.mp3".format(folderD, nameArq)
        
        if  os.path.isfile(chckEx) == True:
            print("YOU ALREADY DOWNLOAD THIS FILE")
        else:
            download(vid, folderD, nameArq)
            convMp3(nameArq, folderD)
            setMetD(nameArq, folderD)
            print("======DOWNLOAD COMPLETE======\n\n")
    return


def from_Web(folderD):
    artist = input("Enter the artist: ")
    song = input("Enter the song: ")
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
        showAvVid(soup, urlsRes)
        n = 1

        amountD = input("How many links do you want: ")
        for vid in range(int(amountD)):
            if n > 1:
                showAvVid(soup, urlsRes)
            else:
                pass
                
            selected = input("Select the download: ")
            vid = pafy.new(urlsRes[int(selected)])
            descr = [vid.author, vid.title, vid.duration]
            nameArq = re.sub(r'([^\s\w]|_)+', '', descr[1])
            nameArq = nameArq.replace("  ", " - ")
            download(vid, folderD, title)
            convMp3(nameArq, folderD)
            setMetD(nameArq, folderD)
            print("======DOWNLOAD COMPLETE======\n\n")
            n += 1
    return

def download(vid, folderD, nameArq):
    print("\n=======STARTING DOWNLOAD======")
    audio = vid.getbestaudio("m4a")
    filename = audio.download(filepath='{}/{}.m4a'.format(folderD, nameArq), quiet=False)
    return

def convMp3(nameArq, folderD):
    print("\n========CONVERTING TO MP3=======")
    m4a_audio = AudioSegment.from_file("{}/{}.m4a".format(folderD, nameArq), format="m4a")
    m4a_audio.export("{}/{}.mp3".format(folderD, nameArq), format="mp3", bitrate="128k")
    os.remove("{}/{}.m4a".format(folderD, nameArq))
    return


def setMetD(nameArq, folderD):
    print("======SETTING THE METADATA======")
    song = EasyID3("{}/{}.mp3".format(folderD, nameArq))
    artist, title = nameArq.split(" - ")
    song["title"] = title
    song["artist"] = artist
    song.save()
    return

def showAvVid(soup, urlsRes):
    n = 0
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        urlsRes.insert(n, 'https://www.youtube.com' + vid['href'])
        print("{} - {}".format(n, vid['title']))
        n += 1
    return(urlsRes)
    
        
if __name__ == '__main__':
    main()
