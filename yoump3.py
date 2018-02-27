import pafy
import os
import re
import urllib
import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3


folderD = "C:/Users/User/Documents/Python/Download Youtube/Downloads"

def main():
    method = int(input("Type Download Method:\n1 - from a txt file,\n2 - from web scraping,\n3 - from youtube playlist\n"))
    if method < 1 or method > 3:
        print("Select valid method")
    else:
        if method == 1:
            from_TxtFile()
        elif method == 2:
            from_Web()
        elif method == 3:
            print("3")

def from_TxtFile():
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
            download(vid, nameArq)
            convMp3(nameArq)
            setMetD(nameArq)
            print("======DOWNLOAD COMPLETE======\n\n")
    return


def from_Web():
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
            download(vid, nameArq)
            convMp3(nameArq)
            setMetD(nameArq)
            print("======DOWNLOAD COMPLETE======\n\n")
            n += 1
    return

def download(vid, nameArq):
    print("\n=======STARTING DOWNLOAD======")
    audio = vid.getbestaudio("m4a")
    filename = audio.download(filepath='{}/{}.m4a'.format(folderD, nameArq), quiet=False)
    return

def convMp3(nameArq):
    print("\n========CONVERTING TO MP3=======")
    m4a_audio = AudioSegment.from_file("{}/{}.m4a".format(folderD, nameArq), format="m4a")
    m4a_audio.export("{}/{}.mp3".format(folderD, nameArq), format="mp3", bitrate="128k")
    os.remove("{}/{}.m4a".format(folderD, nameArq))
    return

def setMetD(nameArq):
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
