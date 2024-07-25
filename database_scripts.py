import sqlite3
from bsmdb.crypt import Crypt


class BotDatabase:
    def __init__(self, path):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.executescript("""
                BEGIN;
                CREATE TABLE IF NOT EXISTS users (user_id PRIMARY KEY, user_name, contact_info);
                CREATE TABLE IF NOT EXISTS requests (
                request_id PRIMARY KEY,
                user_id,
                problem_description,
                contact_time,
                FOREIGN KEY(user_id) REFERENCES users(user_id));
                END;
                """)

    async def save_user_data(self, user_id, user_name, request_id, problem_description, contact_info, contact_time):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO users (user_id, user_name, contact_info)
                VALUES (?,?,?)""",
                           await Crypt.tuple_encrypter(user_id, user_name, contact_info))
            cursor.execute("""
                INSERT INTO requests (request_id, user_id, problem_description, contact_time)
                VALUES(?,?,?,?)""",
                           await Crypt.tuple_encrypter(request_id, user_id, problem_description, contact_time))



