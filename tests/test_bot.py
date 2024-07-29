import os
import shutil
import tempfile
import time
import unittest
from unittest.mock import MagicMock, patch, Mock

from bsmdb.bot import Bot
from bsmdb.commands import CommandsFactory, Commands
from bsmdb.database_scripts import BotDatabase
from bsmdb.pageupd import GithubPageUpdater


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


# class TestMain(unittest.TestCase):
#     def test_main(self):
#         config_pageupd = {
#             'local_repo': 'test',
#             'database_path': 'test.db',
#             'html_files': {
#                 'users': 'test_users.html',
#                 'requests': 'test_requests.html'
#             },
#             'commit_message': 'Test'
#         }
#
#         # config_update_time = {
#         #     'hour': 0,
#         #     'minutes': 0
#         # }
#
#         database = BotDatabase('test.db')
#         database.create_tables()
#
#         updater = GithubPageUpdater(**config_pageupd)
#         updater.htmls_creator()
#
#         self.assertTrue(os.path.exists('test.db'))
#         self.assertTrue(os.path.exists('test_users.html'))
#         self.assertTrue(os.path.exists('test_requests.html'))
#
#     def tearDown(self):
#         os.remove('test.db')
#         os.remove('test_users.html')
#         os.remove('test_requests.html')

class TestMain(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
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

        self.assertTrue(os.path.exists(self.config_pageupd['database_path']))
        self.assertTrue(os.path.exists(self.config_pageupd['html_files']['users']))
        self.assertTrue(os.path.exists(self.config_pageupd['html_files']['requests']))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    unittest.main()