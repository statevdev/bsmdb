import logging
import unittest
from unittest.mock import MagicMock

from bsmdb.bot import Bot
from bsmdb.commands import CommandsFactory, Commands

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class TestBot(unittest.TestCase):
    def test_initialization(self):
        application_builder = MagicMock()

        bot = Bot('test_token')
        bot.application = application_builder.token().build()

        commands = CommandsFactory.create_commands(bot.application)
        self.assertEqual(len(commands), len(Commands.__subclasses__()))  # Проверяем, что команды создаются

    def test_run(self):
        bot = Bot('test_token')
        bot.application.run_polling = MagicMock()
        bot.run()
        bot.application.run_polling.assert_called_once()  # Проверяем, что run_polling вызывается один раз
