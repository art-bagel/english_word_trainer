import sqlite3


class Db():
    def __send_request__(self, *request):
        response = None

        db = sqlite3.connect('dictionary')
        cur = db.cursor()
        cur.execute(*request)
        db.commit()
        if 'SELECT' in request[0]:
            response = cur.fetchall()
        cur.close()
        return response

    def change_scoring(self, id, decrement = False):
        #decrement or increment scoring
        query_get = "SELECT scoring FROM dict WHERE id= ?"
        scoring = self.__send_request__(query_get, (id, ))[0][0]
        if decrement:
            scoring -= 1
        else:
            scoring += 1
        query_set = "UPDATE dict SET scoring= ? WHERE id= ?"
        self.__send_request__(query_set, (scoring, id))

    def delete_word(self, id):
        query = "DELETE FROM dict WHERE id= ?"
        value = (id, )
        self.__send_request__(query, value)

    def get_words(self):
        request = "SELECT * FROM dict"
        response = self.__send_request__(request)
        return response

    def change_word(self, id, eng_word, rus_word,):
        query = "UPDATE dict " \
                "SET english_word= ?, translate_word= ?  " \
                "WHERE id= ?"
        value = (eng_word.lower(), rus_word.lower(), id)
        self.__send_request__(query, value)

    def add_word(self, eng_word, rus_word):
        request = "INSERT INTO dict(english_word, translate_word, scoring)" \
                  " VALUES(?, ?, ?);"
        value = (eng_word.lower(), rus_word.lower(), 0)
        self.__send_request__(request, value)
