import sqlite3
import random


class Dictionary():
    def __init__(self):
        self._get_and_slice_data_()

    def __send_request__(self, *request):
        response = {
            'status': '',
            'massage': '',
            'data': None
        }
        try:
            db = sqlite3.connect('data_base_dictionary')
            cur = db.cursor()
            cur.execute(*request)
            db.commit()
            if 'SELECT' in request[0]:
                response['data'] = cur.fetchall()
            cur.close()
            response['status'] = 'OK'
        except:
            response['status'] = 'DROP'
            response['massage'] = 'Ошибка при обращении к базе данных!'
        return response

    def _get_and_slice_data_(self):
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
        word = word.lower().strip()
        if word in self.words['eng']:
            index = self.words['eng'].index(word)
            return self.words['id'][index]
        elif word in self.words['rus']:
            index = self.words['rus'].index(word)
            return self.words['id'][index]
        return None

    def change_weight(self, id, user_answer):
        # decrement or increment weight
        query_set = "UPDATE dict SET scoring= ? WHERE id= ?"
        index = self.words['id'].index(id)
        if user_answer:
            if self.words['weight'][index] > 1:
                self.words['weight'][index] -= 1
        else:
            self.words['weight'][index] += 1
        print(self.words['weight'])

        response = self.__send_request__(query_set, (self.words['weight'][index], id))
        return response['status'], response['massage']

    def get_random_word(self):
        random_word = random.choices(self.words['eng'], weights=self.words['weight'])[0]
        index = self.words['eng'].index(random_word)
        response = {
            'id': self.words['id'][index],
            'eng': self.words['eng'][index],
            'rus': self.words['rus'][index]
        }
        return response

    def delete_word(self, id):
        query = "DELETE FROM dict WHERE id= ?"
        value = (id,)
        response = self.__send_request__(query, value)
        if response['status'] == 'OK':
            self._get_and_slice_data_()
        return response['status'], response['massage']

    def get_all_from_db(self):
        request = "SELECT * FROM dict"
        response = self.__send_request__(request)
        return response

    def change_word(self, id, eng_word, rus_word, weight=1):
        query = "UPDATE dict " \
                "SET english_word= ?, translate_word= ?, scoring= ?  " \
                "WHERE id= ?"
        value = (eng_word.lower(), rus_word.lower(), weight, id)
        response = self.__send_request__(query, value)
        print(response)
        if response['status'] == 'OK':
            self._get_and_slice_data_()
        return response['status'], response['massage']

    def add_word(self, eng_word, rus_word):
        request = "INSERT INTO dict(english_word, translate_word, scoring)" \
                  " VALUES(?, ?, ?);"

        value = (eng_word.lower(), rus_word.lower(), 1)
        response = self.__send_request__(request, value)
        if response['status'] == 'OK':
            self._get_and_slice_data_()
        return response['status'], response['massage']

