from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb
import settings as st
import dictionary_base as db


class GuiTrain(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.parent = parent

        # Create the different widgets
        self.train_space = ttk.Frame(self)
        self.training_word_lable = ttk.Label(self.train_space, text='Translate this word')
        self.training_word_var = StringVar()
        self.training_word = ttk.Label(self.train_space,
                                       text="often",
                                       font=('Arial', 30, 'bold'),
                                       textvariable=self.training_word_var)
        self.result_translate = ttk.Label(self.train_space,
                                          text='',
                                          font=('Arial', 15, 'bold'),
                                          )
        self.translate_lable = ttk.Label(self.train_space, text='Enter translate')
        self.translate_var = StringVar()
        self.translate_entry = ttk.Entry(self.train_space, textvariable=self.translate_var)
        self.btn1 = ttk.Button(self.train_space, text='Check', command=self.check_user_input, default='normal')
        self.btn2 = ttk.Button(self.train_space, text='Next', command=self.next, default='normal')

        # Grid all the widgets
        self.train_space.pack(pady=(20, 0))
        self.training_word_lable.grid(column=0, columnspan=2, row=0)
        self.training_word.grid(column=0, row=1, columnspan=2, pady=(20, 0))
        self.result_translate.grid(column=0, row=2, columnspan=2, pady=(20, 0))
        self.translate_lable.grid(column=0, row=3, columnspan=2, pady=(20, 5))
        self.translate_entry.grid(column=0, row=4, columnspan=2)
        self.btn1.grid(column=0, row=5, pady=(20, 5))
        self.btn2.grid(column=1, row=5, pady=(20, 5))
        self.parent.update()

        # Create other variable
        self.dictionary = db.Dictionary()
        self.word = {}

        self.set_default_settings()
        self.set_training_word()

    def set_default_settings(self):
        self.result_translate['text'] = ''
        self.result_translate['foreground'] = 'green'
        self.translate_var.set('')
        self.btn1['state'] = 'active'
        self.translate_entry.bind('<Return>', lambda e: self.check_user_input())

    def set_training_word(self):
        self.word = self.dictionary.get_random_word()
        self.training_word_var.set(self.word['eng'])

    def check_user_input(self):
        user_input = self.translate_entry.get().lower().split()
        if user_input:
            user_input = user_input[0]
            message = "Правильно!"
            answer = True

            if user_input != self.word['rus']:
                message = f'Правильный ответ: {self.word["rus"]}'
                self.result_translate['foreground'] = 'red'
                answer = False

            self.dictionary.change_weight(id=self.word['id'], user_answer=answer)
            self.result_translate['text'] = message
            self.btn1['state'] = 'disabled'
            self.translate_entry.bind('<Return>', lambda e: self.next())
        else:
            self.__show_warning__('Поле не должно быть пустым')

    def next(self):
        self.set_default_settings()
        self.set_training_word()

    def __show_warning__(self, msg):
        mb.showwarning("Предупреждение", msg)



