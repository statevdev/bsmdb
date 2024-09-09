import argparse
import sqlite3
from crypt_data import Crypt


class BotDatabase:
    """
    Класс для работы с базой данных бота.

    Этот класс предоставляет методы для создания таблиц и сохранения
    данных пользователей и их заявок в базе данных SQLite.
    """
    def __init__(self, path: str):
        """
        Инициализирует объект базы данных.

        Параметры:
        path (str): Путь к файлу базы данных.
        """
        self.path = path

    def create_tables(self):
        """
        Создает таблицы в базе данных.

        Этот метод создает таблицы для пользователей и заявок, если они
        еще не существуют.
        """
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

    async def save_user_data(self,
            user_id: str,
            user_name: str,
            request_id: str,
            problem_description: str,
            contact_info: str,
            contact_time: str
    ):
        """
        Сохраняет данные пользователя и его заявку в базе данных.

        Этот метод шифрует данные и сохраняет их в соответствующих таблицах.

        Параметры:
        user_id (str): Идентификатор пользователя.
        user_name (str): Имя пользователя.
        request_id (str): Идентификатор заявки.
        problem_description (str): Описание проблемы.
        contact_info (str): Контактная информация пользователя.
        contact_time (str): Предпочтительное время для связи.
        """
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users (user_id, user_name, contact_info)
            VALUES (?,?,?)""",
                       await Crypt.encrypt_data(user_id, user_name, contact_info))
        cursor.execute("""
            INSERT INTO requests (request_id, user_id, problem_description, contact_time)
            VALUES(?,?,?,?)""",
                       await Crypt.encrypt_data(request_id, user_id, problem_description, contact_time))
        connection.commit()
        connection.close()


if __name__ == "__main__":
    """
    Этот модуль можно запустить напрямую через терминал в формате:
    `python dbscripts.py <путь к базе данных>`, тем самым вручную создав базу данных в указанном месте.
    """
    parser = argparse.ArgumentParser(description='Create database')

    parser.add_argument('path', help='Path to database')
    args = parser.parse_args()

    BotDatabase(args.path).create_tables()



