import os
import shutil
import gc
import tempfile
import unittest
from unittest.mock import MagicMock

from bot import Bot
from commands import CommandsFactory, Commands
from database_scripts import BotDatabase
from pageupd import GithubPageUpdater


class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = Bot('test_token')

    def test_initialization(self):
        application_builder = MagicMock()
        self.bot.application = application_builder().token().build()

        commands = CommandsFactory.create_commands(self.bot.application)

        self.assertEqual(len(commands), len(Commands.__subclasses__()))  # Проверяем, что команды создаются

    def test_run(self):
        self.bot.application.run_polling = MagicMock(return_value='test_response')
        result = self.bot.run()

        self.bot.application.run_polling.assert_called_once()  # Проверяем, что функция вызывалась один раз
        self.assertEqual(result, 'test_response')  # Проверяем, что возвращается ожидаемое значение


class TestMain(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()  # Создаем временную директорию
        self.config_pageupd = {
            'local_repo': self.temp_dir,
            'database_path': os.path.join(self.temp_dir, 'test.db'),
            'html_files': {
                'users': os.path.join(self.temp_dir, 'test_users.html'),
                'requests': os.path.join(self.temp_dir, 'test_requests.html')
            },
            'commit_message': 'Test'
        }

    def test_main(self):
        database = BotDatabase(self.config_pageupd['database_path'])
        database.create_tables()

        updater = GithubPageUpdater(**self.config_pageupd)
        updater.htmls_creator()

        import psutil
        # Получаем текущий процесс
        process = psutil.Process()
        # Получаем список открытых файлов
        open_files = process.open_files()
        print("Открытые файлы:")
        for file in open_files:
            print(file.path)

        # Проверяем, что нужные файлы создались
        self.assertTrue(os.path.exists(self.config_pageupd['database_path']))
        self.assertTrue(os.path.exists(self.config_pageupd['html_files']['users']))
        self.assertTrue(os.path.exists(self.config_pageupd['html_files']['requests']))

    def tearDown(self):
        gc.collect()  # Без принудительной очистки мусора код не работает :/
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    unittest.main()