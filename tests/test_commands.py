import asyncio
import unittest
from unittest.mock import Mock, AsyncMock
from commands import StartCommand, HelpCommand, SettingsCommand, RequestCommand


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
        self.context.user_data['user_name'] = None
        self.context.user_data['problem_description'] = "test problem description"

        # Запускаем метод _step_1
        asyncio.run(self.command._step_1(self.update, self.context))

        # Проверяем, что send_message был вызван с правильным текстом
        self.context.bot.send_message.assert_called_once_with(
            chat_id=self.update.effective_chat.id, text=RequestCommand.USER_NAME_QUESTION)

    # def test_step_2(self):
    #     user_name =
    #     if user_name.replace(' ', '').isalpha():
    #         self.context.user_data['contact_info'] = None
    #         self.context.user_data['user_name'] = user_name.title()
    #
    #         # Проверяем, что send_message был вызван с правильным текстом
    #         self.context.bot.send_message.assert_called_once_with(
    #             chat_id=self.update.effective_chat.id,
    #             text=RequestCommand.CONTACT_INFO_QUESTION.format(user_name.title()))
    #     else:
    #         # Проверяем, что send_message был вызван с правильным текстом
    #         self.context.bot.send_message.assert_called_once_with(
    #             chat_id=self.update.effective_chat.id, text=RequestCommand.NAME_ERROR)


if __name__ == '__main__':
    unittest.main()