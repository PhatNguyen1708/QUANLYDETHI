from tkinter import *
root = Tk()
frame = Frame(root)
frame.pack()

def prep(event):
    event.widget.config(bg='light blue')
    event.widget.focus_set()  # give keyboard focus to the label
    event.widget.bind('<Key>', edit)

def edit(event):
    print(event.char)

example = Label(frame, text='Click me')
example.pack()
example.bind('<Double 1>', prep)
mainloop()