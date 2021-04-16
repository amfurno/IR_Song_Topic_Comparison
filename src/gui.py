import tkinter
import tkinter.font as font
from tkinter import *

import songComparison

# creates window


class comparisonApp:
    def __init__(self):
        app = Tk()

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

    def compareSongs(self):
        print(self.artist1.get())


# runs window
if __name__ == '__main__':

    comparisonApp()
    # clickGo.place(x=300, y=100, anchor=CENTER)
