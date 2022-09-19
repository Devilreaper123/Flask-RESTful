import sqlite3


class User:
    def __init__(self , _id, username , password):
        self.id = _id
        self.username = username
        self.password = password



    def find_by_username(self,username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"

        result = cursor.execute(query,(username,))

