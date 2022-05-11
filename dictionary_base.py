import os
import sqlite3
import random

from alerts import Alerts


class Dictionary():
    DATA_BASE_NAME = 'dictionary_db'

    def __init__(self):
        self._get_and_slice_data_()
        self.alert = Alerts()
        if not os.path.exists(self.DATA_BASE_NAME):
            self.create_db()

    def create_db(self):
        """Создает базу данных."""
        connect = sqlite3.connect(self.DATA_BASE_NAME)
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE dict (id INTEGER PRIMARY KEY, 
                                             english_word TEXT, 
                                             russian_word TEXT,
                                             weight INTEGER)
                       """)

    def _send_request(self, *request):
        """Отправляет запрос в базу данных."""
        response = {
            'status': '',
            'massage': '',
            'data': None
        }
        try:
            db = sqlite3.connect(self.DATA_BASE_NAME)
            cur = db.cursor()
            cur.execute(*request)
            db.commit()
            if 'SELECT' in request[0]:
                response['data'] = cur.fetchall()
            cur.close()
            db.close()
            response['status'] = 'OK'
        except Exception as error:
            print(error)
            response['status'] = 'DROP'
            response['massage'] = 'Ошибка при обращении к базе данных!'
        return response

    def _get_and_slice_data_(self):
        """Получает данные из базы и сохраняем в словарь."""
        self.words = {
            'id': [],
            'eng': [],
            'rus': [],
            'weight': []
        }
        response = self.get_all_from_db()
        if response['status'] == 'OK':
            for row in response['data']:
                self.words['id'].append(row[0])
                self.words['eng'].append(row[1])
                self.words['rus'].append(row[2])
                self.words['weight'].append(row[3])

    def get_id(self, word):
        """Получает id слова."""
        word = word.lower().strip()
        if word in self.words['eng']:
            index = self.words['eng'].index(word)
            return self.words['id'][index]
        return None

    def change_weight(self, id, user_answer):
        """Изменяет вес слова."""
        query = "UPDATE dict SET weight= ? WHERE id= ?"
        index = self.words['id'].index(id)
        if user_answer:
            if self.words['weight'][index] > 1:
                self.words['weight'][index] -= 1
        else:
            self.words['weight'][index] += 1

        response = self._send_request(query, (self.words['weight'][index], id))
        return response['status'], response['massage']

    def get_random_word(self):
        """Получает случаное слово из словаря."""
        if not self.words['eng']:
            self.alert.warning("Словарь пуст! Для тренеровки наполните словарь!")
            return None
        random_word = random.choices(self.words['eng'], weights=self.words['weight'])[0]
        index = self.words['eng'].index(random_word)
        response = {
            'id': self.words['id'][index],
            'eng': self.words['eng'][index],
            'rus': self.words['rus'][index]
        }
        return response

    def delete_word(self, id):
        """Удаляет слова из базы данных."""
        query = "DELETE FROM dict WHERE id= ?"
        value = (id,)
        response = self._send_request(query, value)
        if response['status'] == 'OK':
            self._get_and_slice_data_()
        return response['status'], response['massage']

    def get_all_from_db(self):
        """Получает все слова из базы данных."""
        request = "SELECT * FROM dict"
        response = self._send_request(request)
        return response

    def change_word(self, id, eng_word, rus_word, weight=1):
        """Изменяет слово в базе данных."""
        query = ("UPDATE dict "
                 "SET english_word= ?, russian_word= ?, weight= ?  "
                 "WHERE id= ?")
        value = (eng_word.lower(), rus_word.lower(), weight, id)
        response = self._send_request(query, value)
        if response['status'] == 'OK':
            self._get_and_slice_data_()
        return response['status'], response['massage']

    def add_word(self, eng_word, rus_word):
        """Добавляет новое слово в базу данных."""
        request = ("INSERT INTO dict(english_word, russian_word, weight)"
                  " VALUES(?, ?, ?);")

        value = (eng_word.lower(), rus_word.lower(), 1)
        response = self._send_request(request, value)
        if response['status'] == 'OK':
            self._get_and_slice_data_()
        return response['status'], response['massage']
