from tkinter import *
from tkinter import ttk

import settings as st
import dictionary_base as db
from gui_dictionary import GuiDictionary as GuiDict
from gui_train import GuiTrain

if __name__ == '__main__':
    # Create main window
    dictionary = db.Dictionary()
    root = Tk()
    root.geometry(f"+{st.INDENT_LEFT}+{st.INDENT_TOP}")
    root.title('English word trainer')
    root.resizable(st.RESIZE_W, st.RESIZE_H)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    note_book = ttk.Notebook(root)
    note_book.grid(column=0, row=0, sticky=(N, W, E, S))
    train = GuiTrain(note_book, dictionary=dictionary)
    dictionary = GuiDict(note_book, dictionary=dictionary)
    note_book.add(train, text='Train')
    note_book.add(dictionary, text='Dictionary')

    root.mainloop()
