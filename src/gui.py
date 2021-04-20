import tkinter
import tkinter.font as font
from tkinter import *

from gensim.models import LdaModel
from lyricsgenius import Genius, genius

import songComparison as sc
import API_Keys
from modelBuilder import MODEL_LOCATION

# creates window


class comparisonApp:
    def __init__(self, genius, model):
        app = Tk()

        self.genius = genius
        self.model = model

        self.myfont = font.Font(family='Courier')
        app.geometry('650x300')
        app.configure(bg='pink')
        app.title('Song Lyric Comparison')

        self.artist1 = StringVar()
        self.artist2 = StringVar()
        self.song1 = StringVar()
        self.song2 = StringVar()

        Label(app, text='Artist 1 Name', font=self.myfont,
              bg='pink').grid(row=0, column=0, )
        Label(app, text='Artist 2 Name', font=self.myfont,
              bg='pink').grid(row=0, column=2)
        Label(app, text='Song 1 Name', font=self.myfont,
              bg='pink').grid(row=1, column=0)
        Label(app, text='Song 2 Name', font=self.myfont,
              bg='pink').grid(row=1, column=2)

        artist1Box = Entry(app, textvariable=self.artist1,).grid(
            row=0, column=1)
        artist2Box = Entry(app, textvariable=self.artist2).grid(
            row=0, column=3)
        song1Box = Entry(app, textvariable=self.song1).grid(
            row=1, column=1)
        song2Box = Entry(app, textvariable=self.song2).grid(
            row=1, column=3)

        Button(app, text='Compare My Songs!', bg='pink',
               width=20, font=self.myfont, highlightcolor='blue',
               command=self.compareSongs).place(x=300, y=100, anchor=CENTER)

        app.mainloop()

    def compareSongs(self):  # TODO refactor to just call songComparison
        song1Lyrics = sc.getLyrics(
            self.song1.get(), self.artist1.get(), genius)
        song2Lyrics = sc.getLyrics(
            self.song2.get(), self.artist2.get(), genius)
        docs = [sc.tokenizeLyrics(song1Lyrics), sc.tokenizeLyrics(song2Lyrics)]
        divergence = sc.getSongSimilarity(model, docs)
        print(divergence)


# runs window
if __name__ == '__main__':
    genius = Genius(API_Keys.genius_access_token)
    genius.timeout = 15
    genius.sleep_time = 2

    model = LdaModel.load(MODEL_LOCATION)
    comparisonApp(genius, model)
    # clickGo.place(x=300, y=100, anchor=CENTER)
