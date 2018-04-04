# -*- coding: utf-8 -*-
from Tkinter import *
from ttk import *
import tkFileDialog as filedialog
from pydub import AudioSegment
from pytube import YouTube
import progressbar
import sys
import random
import os
import bs4 as bs
from six.moves import urllib


def vypocet():
    textovysubor = entry_txtfile.get()
    f = open(textovysubor, 'r')
    song_list = []
    name_list = []
    pocet_pesniciek = sum(1 for line in open(textovysubor))
    for x in range(0, int(pocet_pesniciek)):
        a = f.readline()
        a = a.rstrip('\n')
        if len(entry_syntax.get()) == 0:
            try:
                meno, caszaciatok, caskoniec = a.split(', ')
            except ValueError:
                meno, caszaciatok = a.split(', ')
            if len(caszaciatok) < 5:
                caszaciatok = '0' + caszaciatok
            if len(caszaciatok) < 6:
                caszaciatok = '00:' + caszaciatok
            song_list.append(caszaciatok)
            name_list.append(meno)
        else:
            try:
                poradie = entry_syntax.get()
                poradie.split(', ')
                if poradie[0] == 'm':
                    meno, caszaciatok, caskoniec = a.split(', ')
                    caskoniec = None
                elif poradie[0] == 'z':
                    caszaciatok, caskoniec, meno = a.split(', ')
                    caskoniec = None
                else:
                    sys.exit('zle zadana SYNTAX')
                if len(caszaciatok) < 5:
                    caszaciatok = '0' + caszaciatok
                if len(caszaciatok) < 6:
                    caszaciatok = '00:' + caszaciatok
                song_list.append(caszaciatok)
                name_list.append(meno)
            except ValueError:
                poradie = entry_syntax.get()
                poradie.split(', ')
                if poradie[0] == 'm':
                    meno, caszaciatok = a.split(', ')
                    caskoniec = None
                elif poradie[0] == 'z':
                    caszaciatok, meno = a.split(', ')
                    caskoniec = None
                else:
                    sys.exit('zle zadana SYNTAX')
                if len(caszaciatok) < 5:
                    caszaciatok = '0' + caszaciatok
                if len(caszaciatok) < 6:
                    caszaciatok = '00:' + caszaciatok
                song_list.append(caszaciatok)
                name_list.append(meno)

    y = 0
    progress['value'] = 0
    for x in bar(range(len(song_list))):
        try:
            caszaciatok = song_list[y]
            caskoniec = song_list[y + 1]
            meno = name_list[y]
            startH, startMin, startSec = caszaciatok.split(':')
            startH = int(startH)
            startMin = int(startMin)
            startSec = int(startSec)
            endH, endMin, endSec = caskoniec.split(':')
            endH = int(endH)
            endMin = int(endMin)
            endSec = int(endSec)
            startTime = startH * 60 * 60 * 1000 + startMin * 60 * 1000 + startSec * 1000
            endTime = endH * 60 * 60 * 1000 + endMin * 60 * 1000 + endSec * 1000

            nazov_mp3 = entry_album.get()
            song = AudioSegment.from_mp3(nazov_mp3)
            extract = song[startTime:endTime]
            extract.export(meno + '.mp3', format='mp3')

        except IndexError:

            nazov_mp3 = entry_album.get()
            song = AudioSegment.from_mp3(nazov_mp3)
            caszaciatok = random.choice(song_list[y: y + 1])
            meno = random.choice(name_list[y:y + 1])
            startH, startMin, startSec = caszaciatok.split(':')
            startH = int(startH)
            startMin = int(startMin)
            startSec = int(startSec)
            startTime = startH * 60 * 60 * 1000 + startMin * 60 * 1000 + startSec * 1000
            extract = song[startTime:]
            extract.export(meno + '.mp3', format='mp3')
        y += 1
        progress['value'] = y / len(song_list) * 100
        master.update_idletasks()


def stiahnut():
    link = entry_linkYT.get()
    meno = entry_meno.get()
    yt = YouTube(link)
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
        song.export(meno + '.mp3', format='mp3')
        os.remove(meno + '.mp4')
        os.rename(cwd + '/' + meno + '.mp3',
                  cwd + '/downloads/' + meno + '.mp3')
    else:
        sys.exit('bez mp4ky :(, neda sa stiahnut')


def linky_playlistu():
    link_album = entry_linkALBUM.get()
    nazov_albumu = entry_nazovalbumu.get()
    sauce = urllib.request.urlopen(link_album).read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    f = open('linky.txt', 'w')

    cwd = os.getcwd()
    new_path_to_album = str(cwd + '/downloads/' + nazov_albumu)
    print(new_path_to_album)

    if not os.path.exists(new_path_to_album):
        os.makedirs(new_path_to_album)

    link_text = []
    for a in soup.find_all('a', href=True):
        if a.get_text(strip=True):
            if 'watch' in str(a['href']) and 'index' in str(a['href']):
                link = 'https://www.youtube.com' + str(a['href'])
                print(link)
                link_text.append(a['href'])
                f.write(link)
                f.write('\n')
    print(len(link_text))

    f = open('linky.txt', 'r')
    pocet_pesniciek = sum(1 for line in open('linky.txt'))
    for x in bar(range(0, int(pocet_pesniciek))):
        a = f.readline()
        a = a.rstrip('\n')
        yt = YouTube(a)
        meno = yt.filename
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
            song.export(meno + '.mp3', format='mp3')
            os.remove(meno + '.mp4')
            os.rename(cwd + '/' + meno + '.mp3',
                      new_path_to_album + '/' + meno + '.mp3')
        else:
            sys.exit('bez mp4ky :(')


def pridat_mp4():
    master.filename = filedialog.askopenfilename(filetypes=(('MP3 file', '*.mp3'),
                                                            ('All files', '*.*')))
    entry_album.insert(0, master.filename)
    print(master.filename)


def pridat_txtfile():
    master.filename = filedialog.askopenfilename(filetypes=(('Txt file', '*.txt'),
                                                            ('All files', '*.*')))
    entry_txtfile.insert(0, master.filename)
    print(master.filename)


master = Tk()
note = Notebook(master)
bar = progressbar.ProgressBar()

cwd = os.getcwd()
downloads = str(cwd + '/downloads')
print(downloads)

if not os.path.exists(downloads):
    os.makedirs(downloads)


tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)

# upper panel
button_quit = Button(master, text='Quit', command=master.quit)
button_quit.grid(row=0, column=0, sticky=W, pady=4)
progress = Progressbar(master, orient=HORIZONTAL, length=200, mode='determinate')
progress.grid(row=1, column=0, sticky=W, pady=4)

# download
nazov_meno = Label(tab1, text='Meno: ')
nazov_meno.grid(row=1, column=0, sticky=W, pady=4)
entry_meno = Entry(tab1)
entry_meno.grid(row=1, column=1, sticky=W, pady=4)
nazov_linkYT = Label(tab1, text='Link: ')
nazov_linkYT.grid(row=2, column=0, sticky=W, pady=4)
entry_linkYT = Entry(tab1)
entry_linkYT.grid(row=2, column=1, sticky=W, pady=4)
button_linkYT = Button(tab1, text='Stiahnut', command=stiahnut)
button_linkYT.grid(row=2, column=2, sticky=W, pady=4)
nazov_miesto_ulozenia = Label(tab1, text='Miesto ulozenia: ')
nazov_miesto_ulozenia.grid(row=3, column=0, sticky=W, pady=4)

cwd = os.getcwd()

nazov_miesto_ulozenia = Label(tab1, text=cwd)
nazov_miesto_ulozenia.grid(row=3, column=1, sticky=W, pady=4)

# cut

nazov_album = Label(tab2, text='Album: ')
nazov_album.grid(row=1, column=0, sticky=W, pady=4)
entry_album = Entry(tab2)
entry_album.grid(row=1, column=1, sticky=W, pady=4)
button_album = Button(tab2, text='Album', command=pridat_mp4)
button_album.grid(row=1, column=2, sticky=W, pady=4)
nazov_txtfile = Label(tab2, text='Txtfile: ')
nazov_txtfile.grid(row=2, column=0, sticky=W, pady=4)
entry_txtfile = Entry(tab2)
entry_txtfile.grid(row=2, column=1, sticky=W, pady=4)
button_txtfile = Button(tab2, text='Textfile', command=pridat_txtfile)
button_txtfile.grid(row=2, column=2, sticky=W, pady=4)
nazov1_syntax = Label(tab2, text='Zadaj vlstnu syntax')
nazov1_syntax.grid(row=3, column=0, sticky=W, pady=4)
entry_syntax = Entry(tab2)
entry_syntax.grid(row=3, column=1, sticky=W, pady=4)
button_syntax = Button(tab2, text='Vypocet', command=vypocet)
button_syntax.grid(row=3, column=2, sticky=W, pady=4)
nazov1_syntax = Label(tab2, text='Povodna syntax: meno, zaciatok pesnicky, koniec pesnicky')
nazov1_syntax.grid(row=4, column=0, columnspan=2, sticky=W, pady=4)

# download playlist

nazov_linkALBUM = Label(tab3, text='Link: ')
nazov_linkALBUM.grid(row=0, column=0, sticky=W, pady=4)
entry_linkALBUM = Entry(tab3)
entry_linkALBUM.grid(row=0, column=1, sticky=W, pady=4)
nazov_album = Label(tab3, text='Nazov Albumu: ')
nazov_album.grid(row=1, column=0, sticky=W, pady=4)
entry_nazovalbumu = Entry(tab3)
entry_nazovalbumu.grid(row=1, column=1, sticky=W, pady=4)
nazov_interpret = Label(tab3, text='Meno Interpreta: ')
nazov_interpret.grid(row=2, column=0, sticky=W, pady=4)
entry_interpret = Entry(tab3)
entry_interpret.grid(row=2, column=1, sticky=W, pady=4)
button_download = Button(tab3, text='Download', command=linky_playlistu)
button_download.grid(row=3, column=1, sticky=W, pady=4)

note.add(tab1, text="Download Song", compound=TOP)
note.add(tab2, text="Song to Album")
note.add(tab3, text="Download Playlist")
note.grid()
master.mainloop()
exit()
