import asyncio
import os
import re
import shutil

import unittest
from unittest.mock import Mock, AsyncMock, patch

from commands import StartCommand, HelpCommand, SettingsCommand, RequestCommand
from dbscripts import BotDatabase
from test_config import config, temp_dir


class TestStartCommand(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.command = StartCommand()
        self.command.setup(self.bot)

    def test_run(self):
        update = Mock()
        context = Mock()

        # Используем AsyncMock для асинхронной функции
        context.bot.send_message = AsyncMock()

        # Запускаем метод run
        asyncio.run(self.command.run(update, context))

        # Проверяем, что send_message был вызван с правильным текстом
        context.bot.send_message.assert_called_once_with(
            chat_id=update.effective_chat.id, text=StartCommand.START_COMMAND_TEXT)


class TestHelpCommand(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.command = HelpCommand()
        self.command.setup(self.bot)

    def test_run(self):
        update = Mock()
        context = Mock()

        # Используем AsyncMock для асинхронной функции
        context.bot.send_message = AsyncMock()

        # Запускаем метод run
        asyncio.run(self.command.run(update, context))

        # Проверяем, что send_message был вызван с правильным текстом
        context.bot.send_message.assert_called_once_with(
            chat_id=update.effective_chat.id, text=HelpCommand.HELP_COMMAND_TEXT)


class TestSettingsCommand(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.command = SettingsCommand()
        self.command.setup(self.bot)

    def test_run(self):
        update = Mock()
        context = Mock()

        # Используем AsyncMock для асинхронной функции
        context.bot.send_message = AsyncMock()

        # Запускаем метод run
        asyncio.run(self.command.run(update, context))

        # Проверяем, что send_message был вызван с правильным текстом
        context.bot.send_message.assert_called_once_with(
            chat_id=update.effective_chat.id, text=SettingsCommand.SETTINGS_COMMAND_TEXT)


class TestRequestCommand(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.command = RequestCommand()
        self.command.setup(self.bot)
        self.update = Mock()
        self.context = Mock()
        self.context.user_data = {}
        self.context.bot.send_message = AsyncMock()

    def test_run(self):
        asyncio.run(self.command.run(self.update, self.context))

        # Проверяем, что send_message был вызван с правильным текстом
        self.context.bot.send_message.assert_called_once_with(
            chat_id=self.update.effective_chat.id, text=RequestCommand.PROBLEM_DESCRIPTION)

    def test_step_1(self):
        # Запускаем метод _step_1
        asyncio.run(self.command._step_1(self.update, self.context))

        # Проверяем, что send_message был вызван с правильным текстом
        self.context.bot.send_message.assert_called_once_with(
            chat_id=self.update.effective_chat.id, text=RequestCommand.USER_NAME_QUESTION)

    def test_step_2(self):
        user_names = ["Test Test", "test test", "TEST TEST", "TEst1 test"]

        for user_name in user_names:
            self.update.message.text = user_name

            # Сбрасываем моки перед каждым вызовом
            self.context.bot.send_message.reset_mock()

            # Запускаем метод _step_2
            asyncio.run(self.command._step_2(self.update, self.context))

            if user_name.replace(' ', '').isalpha():
                # Проверяем, что send_message был вызван с правильным текстом
                self.context.bot.send_message.assert_called_once_with(
                    chat_id=self.update.effective_chat.id,
                    text=RequestCommand.CONTACT_INFO_QUESTION.format(user_name.title()))
            else:
                # Проверяем, что send_message был вызван с правильным текстом
                self.context.bot.send_message.assert_called_once_with(
                    chat_id=self.update.effective_chat.id, text=RequestCommand.NAME_ERROR)

    def test_step_3(self):
        numbers = ["89992348723", "933423234234", "testtest", "8999", "8999d8834023"]

        def validate_phone_number(phone_number):
            pattern = r'^(\+7|8)[0-9]{10}$'
            if re.match(pattern, phone_number):
                return True
            return False

        for number in numbers:
            self.update.message.text = number

            # Сбрасываем моки перед каждым вызовом
            self.context.bot.send_message.reset_mock()

            # Запускаем метод _step_2
            asyncio.run(self.command._step_3(self.update, self.context))

            if validate_phone_number(number):
                # Проверяем, что send_message был вызван с правильным текстом
                self.context.bot.send_message.assert_called_once_with(
                    chat_id=self.update.effective_chat.id,
                    text=RequestCommand.CONTACT_TIME_QUESTION)
            else:
                # Проверяем, что send_message был вызван с правильным текстом
                self.context.bot.send_message.assert_called_once_with(
                    chat_id=self.update.effective_chat.id, text=RequestCommand.PHONE_NUMBER_ERROR)

    @patch.dict('bsmdb.config.config', config)
    @patch("dbscripts.BotDatabase")
    def test_step_4(self, mock_bot_database):
        temp_path = config['db']['database_path']
        mock_database = mock_bot_database.return_value(path=temp_path)

        BotDatabase(temp_path).create_tables()

        # # Подменяем метод save_user_data
        # async def mock_save_user_data(user_id, user_name, request_id, problem_description, contact_info, contact_time):
        #     connection = sqlite3.connect(config['db']['database_path'])
        #     cursor = connection.cursor()
        #     cursor.execute("""
        #         INSERT OR REPLACE INTO users (user_id, user_name, contact_info)
        #         VALUES (?,?,?)""",
        #                    await Crypt.tuple_encrypter(user_id, user_name, contact_info))
        #     cursor.execute("""
        #         INSERT INTO requests (request_id, user_id, problem_description, contact_time)
        #         VALUES(?,?,?,?)""",
        #                    await Crypt.tuple_encrypter(request_id, user_id, problem_description, contact_time))
        #     connection.close()

        mock_database.save_user_data = AsyncMock(side_effect=mock_database.save_user_data)

        self.context.user_data['user_name'] = "test_user_name"
        self.context.user_data['problem_description'] = "test_problem_description"
        self.context.user_data['contact_info'] = "test_contact_info"
        self.update.message.text = "test_contact_time"

        # Запускаем метод _step_4
        asyncio.run(self.command._step_4(self.update, self.context))

        self.context.user_data['user_name'] = "test_user_name"
        self.context.user_data['problem_description'] = "test_problem_description"
        self.context.user_data['contact_info'] = "test_contact_info"
        self.update.message.text = "test_contact_time"

        # Проверяем, что send_message был вызван с правильным текстом
        self.context.bot.send_message.assert_called_once_with(
            chat_id=self.update.effective_chat.id,
            text=RequestCommand.FINAL_TEXT.format(self.context.user_data['user_name']))

        # Проверяем, что словарь user_data был очищен
        self.assertTrue(len(self.context.user_data), 0)

        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()