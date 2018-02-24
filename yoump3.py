import pafy
import os
import re
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3


lines = [line.rstrip('\n') for line in open('musicas.txt')]
folderD = "C:/Users/User/Documents/Python/Download Youtube/Downloads"

for i in range(len(lines)):
    vid = pafy.new(lines[i])
    descr = [vid.author, vid.title, vid.duration]
    print('Autor {}, Título {}, Duraçao {}\n'.format(*descr)) 
    chckEx = "{}/{}.mp3".format(folderD,descr[1])

    if  os.path.isfile(chckEx) == True:
        print("YOU ALREADY DOWNLOAD THIS FILE")
    else:
        audio = vid.getbestaudio("m4a")
        filename = audio.download(quiet=False)
        
        print("\n========CONVERTING TO MP3=======")
        m4a_audio = AudioSegment.from_file("{}.m4a".format(descr[1]), format="m4a")
        m4a_audio.export("{}/{}.mp3".format(folderD, descr[1]), format="mp3", bitrate="128k")

        os.remove("{}.m4a".format(descr[1]))

        print("======SETTING THE METADATA======")
        namArq = "{}.mp3".format(descr[1])
        song = EasyID3("{}/{}".format(folderD, namArq))
        descSong = namArq.replace(".mp3","")
        artist, title = descSong.split(" - ")
        song["title"] = title
        song["artist"] = artist
        song.save()
        print("======DOWNLOAD COMPLETE======\n\n")




