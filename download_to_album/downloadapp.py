from pydub import AudioSegment
from pytube import YouTube
import os
import progressbar
import sys


bar = progressbar.ProgressBar()

f = open('linky.txt', 'r')
song_list = []
name_list = []
pocet_pesniciek = sum(1 for line in open('linky.txt'))
for x in bar(range(0, int(pocet_pesniciek))):
    a = f.readline()
    a = a.rstrip('\n')
    yt = YouTube(a)
    meno = yt.filename[14:]
    yt.set_filename(meno)
    typy_videa = str(yt.videos)
    if '.mp4' in typy_videa:
        list_kvality = ['144p', '240p', '360p', '720p', '1080p']
        y = 0
        for x in range(0, len(list_kvality)):
            try:
                video = yt.get('mp4', list_kvality[y])
                break
            except:
                y += 1
        try:
            print(video)
        except NameError:
            sys.exit('NENASLO VHODNU VERZIU')
        cwd = os.getcwd()
        video.download(cwd)
        song = AudioSegment.from_file(meno + '.mp4', 'mp4')
        song.export(meno + '.mp3', format='mp3', tags={'artist': 'Jozef Holly', 'album': 'Best of Jozef Holly'})
        os.remove(meno + '.mp4')
    else:
        sys.exit('bez mp4ky :(')
