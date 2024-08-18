import asyncio
import unittest
from unittest.mock import Mock, AsyncMock
from commands import StartCommand, send_message


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
        context.bot.send_message.assert_called_once_with(chat_id=update.effective_chat.id, text=StartCommand.START_COMMAND_TEXT)


if __name__ == '__main__':
    unittest.main()