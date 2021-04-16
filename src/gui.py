import tkinter
from tkinter import *
import tkinter.font as font

# creates window
r = tkinter.Tk()

# sets window size
r.geometry('650x300')

# sets background color of window
r.configure(bg='pink')

#r.place_slaves(rely=0.5, anchor=N)

# set font
myFont = font.Font(family='Courier')

# sets title
r.title('Song Lyric Comparison')

# sets labels for boxes
Label(r, text='Artist 1 Name', font=myFont, bg='pink').grid(row=0, column=0, )
Label(r, text='Artist 2 Name', font=myFont, bg='pink').grid(row=0, column=2)
Label(r, text='Song 1 Name', font=myFont, bg='pink').grid(row=1, column=0)
Label(r, text='Song 2 Name', font=myFont, bg='pink').grid(row=1, column=2)

# makes input boxes
artist1Name = Entry(r, textvariable=artist1N)
artist2Name = Entry(r)
song1Name = Entry(r)
song2Name = Entry(r)


# puts in right place
artist1Name.grid(row=0, column=1)
artist2Name.grid(row=0, column=3)
song1Name.grid(row=1, column=1)
song2Name.grid(row=1, column=3)

# button
clickGo = tkinter.Button(r, text='Compare My Songs!', bg='pink',
                         width=20, font=myFont, highlightcolor='blue', command=r.destroy)
clickGo.place(x=300, y=100, anchor=CENTER)

# runs window
r.mainloop()
