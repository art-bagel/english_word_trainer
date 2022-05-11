from tkinter import *
from tkinter import ttk

from alerts import Alerts


class GuiTrain(ttk.Frame):
    def __init__(self, parent, dictionary=None):
        ttk.Frame.__init__(self, parent)
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.parent = parent
        self.train_space = ttk.Labelframe(self)
        self.create_main_widgets(self.train_space)
        self.dictionary = dictionary
        self.alert = Alerts()
        self.word = {}
        self.set_default_settings()
        self.set_training_word()

    def create_main_widgets(self, frame):
        """Создает виджеты и размещает их в окне программы."""
        self.training_word_lable = ttk.Label(frame,
                                             text='Translate this word')
        self.training_word_var = StringVar()
        self.training_word = ttk.Label(frame,
                                       text="often",
                                       font=('Arial', 30, 'bold'),
                                       textvariable=self.training_word_var)
        self.result_translate = ttk.Label(frame,
                                          text='',
                                          font=('Arial', 15, 'bold'),
                                          )
        self.translate_lable = ttk.Label(frame, text='Enter translate')
        self.translate_var = StringVar()
        self.translate_entry = ttk.Entry(frame,
                                         textvariable=self.translate_var
                                         )
        self.btn1 = ttk.Button(frame,
                               text='Check',
                               command=self.check_user_input,
                               default='normal'
                               )
        self.btn2 = ttk.Button(frame,
                               text='Next',
                               command=self.next,
                               default='normal'
                               )
        self.train_space.pack(pady=(20, 0))
        self.training_word_lable.grid(column=0, columnspan=2, row=0)
        self.training_word.grid(column=0, row=1, columnspan=2, pady=(20, 0))
        self.result_translate.grid(column=0, row=2, columnspan=2, pady=(20, 0))
        self.translate_lable.grid(column=0, row=3, columnspan=2, pady=(20, 5))
        self.translate_entry.grid(column=0, row=4, columnspan=2)
        self.btn1.grid(column=0, row=5, pady=(20, 5))
        self.btn2.grid(column=1, row=5, pady=(20, 5))
        self.parent.update()

    def set_default_settings(self):
        """Устанавливает настройки программы по умолчанию."""
        self.result_translate['text'] = ''
        self.result_translate['foreground'] = 'green'
        self.translate_var.set('')
        self.btn1['state'] = 'active'
        self.translate_entry.bind('<Return>', lambda e: self.check_user_input())

    def set_training_word(self):
        """Выводит пользователю случайное слово из словаря."""
        self.word = self.dictionary.get_random_word()
        if self.word:
            self.training_word_var.set(self.word['eng'])

    def check_user_input(self):
        """Проверяет пользовательский ввод на корректность перевода."""
        user_input = self.translate_entry.get().lower().strip()
        if user_input:
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
            self.alert.warning('Поле не должно быть пустым')

    def next(self):
        """Выводит следующее слово для тренировки."""
        self.set_default_settings()
        self.set_training_word()
