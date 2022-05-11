from tkinter import *
from tkinter import ttk

import settings as st
from alerts import Alerts


class GuiDictionary(ttk.Frame):
    def __init__(self, parent=None, dictionary=None):
        ttk.Frame.__init__(self, parent, padding=st.MCF_PADDING)
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.create_main_widgets()
        self.dictionary = dictionary
        self.current_index = None
        self.set_default_options()
        self.alert = Alerts()

    def create_main_widgets(self):
        """Создает и виджеты и размещает их в окне программы."""
        self.table_words_labl = ttk.Label(self, text='Table of learned words ')
        self.listbox_var = StringVar()
        self.table_words = Listbox(self, height=24,
                                   listvariable=self.listbox_var)
        self.size_dictionary = ttk.Label(self)
        self.eng_entry_labl = ttk.Label(self, text='English word')
        self.eng_entry_var = StringVar()
        self.eng_entry = ttk.Entry(self, textvariable=self.eng_entry_var)
        self.rus_entry_labl = ttk.Label(self, text='Translate on Russian')
        self.rus_entry_var = StringVar()
        self.rus_entry = ttk.Entry(self, textvariable=self.rus_entry_var)
        self.btn1 = ttk.Button(self, text='Add',
                               command=self.add_to_dictionary,
                               default='normal')
        self.btn2 = ttk.Button(self, text='Delete',
                               command=self.delete_from_dictionary,
                               default='normal')
        self.btn3 = ttk.Button(self, text='Cancel',
                               command=self.set_default_options,
                               default='normal',
                               state='disabled')

        self.table_words_labl.grid(column=0, row=0, sticky=(N, W))
        self.table_words.grid(column=0, row=1, pady=(5, 5), rowspan=50,
                              sticky=(N, W, E, S))
        self.size_dictionary.grid(column=0, row=51, sticky=(N, W))
        self.eng_entry_labl.grid(column=1, row=0, padx=(20, 0), columnspan=2,
                                 sticky=(N, W))
        self.eng_entry.grid(column=1, row=1, padx=(20, 0), pady=(5, 10),
                            columnspan=2, sticky=(N, W, E))
        self.rus_entry_labl.grid(column=1, row=2, padx=(20, 0), pady=0,
                                 columnspan=2, sticky=(N, W))
        self.rus_entry.grid(column=1, row=3, padx=(20, 0), pady=(5, 10),
                            columnspan=2, sticky=(N, W, E))
        self.btn1.grid(column=1, row=4, padx=(20, 0), pady=(10, 0),
                       sticky=(N, W))
        self.btn2.grid(column=2, row=4, padx=(20, 0), pady=(10, 0),
                       sticky=(N, W))
        self.btn3.grid(column=1, row=5, padx=(20, 0), pady=(10, 0),
                       sticky=(N, W))

        self.table_words.bind('<Double-1>',
                              lambda e: self.get_word_from_listbox())

    def add_to_dictionary(self):
        """Добавляет слова введенные пользователем в базу данных."""
        user_input = self.get_from_entry()
        if user_input:
            response = self.dictionary.add_word(user_input['eng'], user_input['rus'])
            if response[0] != 'OK':
                self.alert.error(response[1])
        self.set_default_options()

    def set_default_options(self):
        """Устанавливает первоначальные настройки отображения."""
        self.table_words.delete(0, END)
        self.listbox_var.set(value=self.dictionary.words['eng'])
        self.size_dictionary['text'] = f"Words in the dictionary: {len(self.dictionary.words['eng'])}"
        self.eng_entry_var.set('')
        self.rus_entry_var.set('')
        self.btn1['text'] = 'Add'
        self.btn1['command'] = self.add_to_dictionary
        self.btn3['state'] = 'disabled'

    def delete_from_dictionary(self):
        """Удаляет слова из базы данных."""
        user_selected = self.get_from_entry()
        if user_selected and user_selected['id']:
            response = self.dictionary.delete_word(user_selected['id'])
            if response[0] != 'OK':
                self.alert.error(response[1])
        else:
            self.alert.error('Слово отсутствует в базе!')
        self.set_default_options()

    def change_words_in_dictionary(self):
        """Изменяет выбранное пользователем слово."""
        user_input = self.get_from_entry()
        if user_input:
            response = self.dictionary.change_word(
                id=self.dictionary.words['id'][self.current_index],
                eng_word=user_input['eng'],
                rus_word=user_input['rus']
            )
            if response[0] != 'OK':
                self.alert.error(response[1])
        self.set_default_options()

    def get_word_from_listbox(self):
        """Берет слово из listbox для последующего изменения.
        Изменяем функцию кнопки добавить на изменить.
        """
        self.current_index = self.table_words.curselection()[0]
        self.eng_entry_var.set(self.dictionary.words['eng'][self.current_index])
        self.rus_entry_var.set(self.dictionary.words['rus'][self.current_index])
        self.btn1['text'] = 'Save'
        self.btn1['state'] = 'active'
        self.btn1['command'] = self.change_words_in_dictionary
        self.btn3['state'] = 'active'

    def get_from_entry(self):
        """Берет из полей введенные пользователем данные."""
        words = {
            'eng': self.eng_entry_var.get(),
            'rus': self.rus_entry_var.get()
        }
        if words['eng'] and words['rus']:
            words['id'] = self.dictionary.get_id(words['eng'])
            return words
        else:
            self.alert.warning('Поля не должны быть пустыми!')
            return None
