from tkinter import *
from tkinter import filedialog
from pygame import *
import pygame
import threading
import os
import tkinter.ttk as ttk

class MusicPlayer:
    def __init__(self, window):
        window.geometry('420x280');
        window.title('Music Player');
        window.resizable(0, 0)
        self.lst = Listbox(window, height=10, width=60)
        self.start=0
        self.lst.grid(row=0, column=0)
        self.scrollbar = Scrollbar(Frame(self.lst), orient=VERTICAL, command=self.lst.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.lst['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.grid(row=20, column=2, sticky=(N, S))
        self.lst.pack()
        self.lst.pack()
        LoadFie = Button(window, text='Open Fie', width=10, font=('Times', 10), command=self.loadfie)
        LoadFolder = Button(window, text='Open Dir', width=10, font=('Times', 10), command=self.loadfolder)
        self.pb = ttk.Progressbar(window, orient=HORIZONTAL, length=100, mode='determinate')
        self.pb.pack()
        LoadFie.place(x=5, y=20);
        LoadFolder.place(x=110, y=20);
        self.lst.place(x=5, y=60);
        self.pb.place(x=20, y=230)
        self.music_file = False
        self.playing_state = False
        self.lst_pos = 1
        self.musicdirs = []
        mixer.init()

    def autoPlay(self, pb):
        if self.playing_state == False:
            return
        self.pb['value'] = mixer.music.get_pos() / mixer.music.get_length() * 100
        time.sleep(1)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(5)
        if self.musicdirs[0]:
            self.musicdirs.append(self.musicdirs[0])
            self.musicdirs = self.musicdirs[1:]
            mixer.music.queue(self.musicdirs[0])
            mixer.music.load(self.musicdirs[0])
            mixer.music.play()

    def loadfie(self):
        self.lst.insert(self.lst_pos, filedialog.askopenfilename())

    def loadfolder(self):
        sourcePath = filedialog.askdirectory()
        self.dirs = os.listdir(sourcePath)
        self.lst_pos = self.lst.size()
        for file in self.dirs:
            if file:
                if file.endswith('.mp3'):
                    self.lst.insert(self.lst_pos, sourcePath + '/' + file)
                    self.musicdirs.append(sourcePath + '/' + file)
                    self.lst_pos = self.lst_pos + 1
        self.scrollbar.config(command=self.lst.yview)

    def playAll(self):
        print("Playing file:")
        self.lst_pos = 0
        for file in self.lst.get(0, END):
            print("Playing file:")
            if file.endswith('.mp3'):
                print("Playing file:", file)
                self.lst.selection_clear(0, END)
                self.lst.selection_set(first=self.lst_pos)
                self.lst.activate(self.lst_pos)
                mixer.music.load(file)
                mixer.music.play()
                self.playing_state = True
                # Wait for the music to play before exiting
                self.lst_pos = self.lst_pos + 1
                if self.lst_pos > self.lst.size() - 1:
                    self.lst_pos = 0
                while mixer.music.get_busy():
                    pygame.time.Clock().tick(500)

    def play(self):
        if self.lst.curselection():
            if self.lst.get(self.lst.curselection()):
                self.lst_pos = self.lst.curselection()
                self.music_file = self.lst.get(self.lst.curselection())
                mixer.music.load(self.music_file)
                mixer.music.play()
                self.playing_state = True
                print('hello')

    def prevSong(self):
        if self.lst.curselection() and self.playing_state == True:
            if self.lst.get(self.lst.curselection()[0]):
                self.lst_pos = self.lst.curselection()[0] - 1
                if self.lst_pos < 0:
                    self.lst_pos = self.lst.size() - 1
                print(self.lst_pos)
                self.lst.selection_clear(0, END)
                self.lst.selection_set(first=self.lst_pos)
                self.lst.activate(self.lst_pos)
                self.lst.index(self.lst_pos)
                self.music_file = self.lst.get(self.lst.curselection())
                mixer.music.load(self.music_file)
                mixer.music.play()
                self.playing_state = True

    def nextSong(self):
        if self.lst.curselection():
            if self.lst.get(self.lst.curselection()[0]) and self.playing_state == True:
                self.lst_pos = self.lst.curselection()[0] + 1
                if self.lst_pos > self.lst.size() - 1:
                    self.lst_pos = 0
                print(self.lst_pos)
                self.lst.selection_clear(0, END)
                self.lst.selection_set(first=self.lst_pos)
                self.lst.activate(self.lst_pos)
                self.lst.index(self.lst_pos)
                self.music_file = self.lst.get(self.lst.curselection())
                mixer.music.load(self.music_file)
                mixer.music.play()
                self.playing_state = True  # else:

    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state = True
        else:
            mixer.music.unpause()
            self.playing_state = False

    def volup(self):
        mixer.music.set_volume(min(1.0, mixer.music.get_volume() + 0.1))
        # mixer.music.play()

    def voldown(self):
        mixer.music.set_volume(max(0.0, mixer.music.get_volume() - 0.1))
        # mixer.music.play()

    def stop(self):
        mixer.music.stop()
        self.playing_state = False

    def function(self,root):
        barThread = threading.Thread(target=1, args=(1,))
        # set thread as daemon (thread will die if parent is killed)
        barThread.daemon = True
        # Start thread, could also use root.after(50, barThread.start()) if desired
        barThread.start()
        root.mainloop()
