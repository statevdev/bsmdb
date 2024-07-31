import argparse
import sqlite3
from crypt_data import Crypt


class BotDatabase:
    def __init__(self, path):
        self.path = path

    def create_tables(self):
        connection = sqlite3.connect(self.path)
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
        connection.close()

    async def save_user_data(self, user_id, user_name, request_id, problem_description, contact_info, contact_time):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users (user_id, user_name, contact_info)
            VALUES (?,?,?)""",
                       await Crypt.tuple_encrypter(user_id, user_name, contact_info))
        cursor.execute("""
            INSERT INTO requests (request_id, user_id, problem_description, contact_time)
            VALUES(?,?,?,?)""",
                       await Crypt.tuple_encrypter(request_id, user_id, problem_description, contact_time))
        connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create database')

    parser.add_argument('path', help='Path to database')
    args = parser.parse_args()

    BotDatabase(args.path).create_tables()


