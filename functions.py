import sqlite3
from config import admin

connection = sqlite3.connect('data.db')
q = connection.cursor()


def join(chat_id):
    q.execute(f"SELECT * FROM users WHERE user_id = {chat_id}")
    result = q.fetchall()
    if len(result) == 0:
        sql = 'INSERT INTO users (user_id) VALUES ({})'.format(chat_id)
        q.execute(sql)
        connection.commit()
