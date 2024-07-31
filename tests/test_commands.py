import unittest
from unittest.mock import Mock
from commands import StartCommand, send_message


class TestStartCommand(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.command = StartCommand()
        self.command.setup(self.bot)

    def test_run(self):
        update = Mock()
        context = Mock()
        self.command.run(update, context)
        self.send_message.assert_called_once_with(chat_id=update.effective_chat.id,
                                                      text=self.command.START_COMMAND_TEXT)