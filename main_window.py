from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb
import settings as st
import dictionary_base as db
from gui_dictionary import GuiDictionary as GuiDict
from gui_train import GuiTrain

if __name__ == '__main__':
    # Create main window
    root = Tk()
    root.geometry(f"+{st.INDENT_LEFT}+{st.INDENT_TOP}")
    root.title('English word trainer')
    root.resizable(st.RESIZE_W, st.RESIZE_H)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    note_book = ttk.Notebook(root)
    note_book.grid(column=0, row=0, sticky=(N, W, E, S))
    train = GuiTrain(note_book)  # first page, which would get widgets gridded into it
    dictionary = GuiDict(note_book)  # second page
    note_book.add(train, text='Train')
    note_book.add(dictionary, text='Dictionary')

    root.mainloop()
# TODO сделать версию на каждй странице приложения
# TODO сделать поиск по с листбоксу
# TODO открытие окна приложения по центру экрана
# TODO сделать обратную тренеровку