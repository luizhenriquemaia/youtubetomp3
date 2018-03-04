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
    method = int(input("Type Download Method, 1 - from a txt file, 2 - from web scraping, 3 - from youtube playlist "))

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
    fileTxt = input("Type the Name of File ")
    fileTxt = str(fileTxt) + ".txt"
    lines = [line.rstrip('\n') for line in open(fileTxt)]
    for i in range(len(lines)):
        vid = pafy.new(lines[i])
        descr = [vid.author, vid.title, vid.duration]
        title = re.sub(r'([^\s\w]|)_+', '', descr[1])
        title = title.replace("  ", " - ")
        print('Autor {}, Título {}, Duraçao {}\n'.format(*descr))
        chckEx = "{}/{}.mp3".format(folderD, title)
        
        if  os.path.isfile(chckEx) == True:
            print("YOU ALREADY DOWNLOAD THIS FILE")
        else:
            download(vid, title)
            convMp3(title)
            setMetD(title)
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

        while True:
            if n > 1:
                showAvVid(soup, urlsRes)
            else:
                pass
                
            selected = input("Select the download: ")
            vid = pafy.new(urlsRes[int(selected)])
            descr = [vid.author, vid.title, vid.duration]
            title = re.sub(r'([^\s\w]|_)+', '', descr[1])
            title = title.replace("  ", " - ")
            download(vid, title)
            convMp3(title)
            setMetD(title)
            print("======DOWNLOAD COMPLETE======\n\n")
            n += 1
    return

def showAvVid(soup, urlsRes):
    n = 0
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        urlsRes.insert(n, 'https://www.youtube.com' + vid['href'])
        print("{} - {}".format(n, vid['title']))
        n += 1
    return(urlsRes)

def download(vid, title):
    print("\n=======STARTING DOWNLOAD======")
    audio = vid.getbestaudio("m4a")
    filename = audio.download(filepath='{}/{}.m4a'.format(folderD, title), quiet=False)
    return

def convMp3(title):
    print("\n========CONVERTING TO MP3=======")
    m4a_audio = AudioSegment.from_file("{}/{}.m4a".format(folderD, title), format="m4a")
    m4a_audio.export("{}/{}.mp3".format(folderD, title), format="mp3", bitrate="128k")
    os.remove("{}/{}.m4a".format(folderD, title))
    return


def setMetD(title):
    print("======SETTING THE METADATA======")
    song = EasyID3("{}/{}.mp3".format(folderD, title))
    try:
        artist, title = title.split(" - ")
        song["title"] = title
        song["artist"] = artist
        song.save()
    except:
        print("Wasn't possible to set metadata!")
    return
    
        
if __name__ == '__main__':
    main()
