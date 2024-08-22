import os
import shutil
import unittest
from unittest.mock import Mock

from bot import Bot
from commands import CommandsFactory, Commands
from dbscripts import BotDatabase
from pageupd import GithubPageUpdater
from test_config import config, temp_dir


# Тест класса Bot
class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = Bot(config['bot']['telegram_token'])

    def test_initialization(self):
        application_builder = Mock()
        self.bot.application = application_builder().token().build()

        commands = CommandsFactory.create_commands(self.bot.application)

        self.assertEqual(len(commands), len(Commands.__subclasses__()))  # Проверяем, что команды создаются

    def test_run(self):
        self.bot.application.run_polling = Mock(return_value='test_response')
        result = self.bot.run()

        self.bot.application.run_polling.assert_called_once()  # Проверяем, что функция вызывалась один раз
        self.assertEqual(result, 'test_response')  # Проверяем, что возвращается ожидаемое значение


# Тест функции main
class TestMain(unittest.TestCase):
    def test_main(self):
        database = BotDatabase(config['db']['database_path'])
        database.create_tables()

        updater = GithubPageUpdater(**config['pageupd'])
        updater.htmls_creator()

        # Проверяем, что нужные файлы создались
        self.assertTrue(os.path.exists(config['db']['database_path']))
        self.assertTrue(os.path.exists(config['pageupd']['html_files']['users']))
        self.assertTrue(os.path.exists(config['pageupd']['html_files']['requests']))

    def tearDown(self):
        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()