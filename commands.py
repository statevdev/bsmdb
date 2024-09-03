import re
from abc import ABC, abstractmethod
from telegram.ext import CommandHandler, MessageHandler, filters

try:
    from config import config
except ImportError:
    from test_config import test_config
    config = test_config

from dbscripts import BotDatabase


class Commands(ABC):
    @abstractmethod
    def setup(self, bot):
        pass

    @abstractmethod
    async def run(self, update, context):
        pass


class CommandsFactory:
    @staticmethod
    def create_commands(bot):
        commands = []
        for command_class in Commands.__subclasses__():
            command = command_class()
            command.setup(bot)
            commands.append(command)
        return commands


class StartCommand(Commands):
    START_COMMAND_TEXT = (
        "Чтобы создать заявку, вам нужно ответить на несколько вопросов.\n\nОтправьте команду /request, "
        "чтобы начать.")

    def setup(self, bot):
        start_handler = CommandHandler('start', self.run)
        bot.add_handler(start_handler)

    async def run(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.START_COMMAND_TEXT)


class HelpCommand(Commands):
    HELP_COMMAND_TEXT = (
        "Чтобы создать заявку, вам нужно ответить на несколько вопросов.\n\nОтправьте команду /request, "
        "чтобы начать.")

    def setup(self, bot):
        help_handler = CommandHandler('help', self.run)
        bot.add_handler(help_handler)

    async def run(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.HELP_COMMAND_TEXT)


class SettingsCommand(Commands):
    SETTINGS_COMMAND_TEXT = (
        "С моей помощью вы можете создать заявку. Изменить или дополнить информацию вы сможете "
        "когда мы с вами свяжемся.")

    def setup(self, bot):
        settings_handler = CommandHandler('settings', self.run)
        bot.add_handler(settings_handler)

    async def run(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.SETTINGS_COMMAND_TEXT)


class RequestCommand(Commands):
    PROBLEM_DESCRIPTION = "Чтобы оставить заявку, опишите как можно подробнее вашу проблему."
    USER_NAME_QUESTION = "Понял вас! Как я могу к вам обращаться?"
    CONTACT_INFO_QUESTION = "Хорошо, {}! Укажите свой номер телефона, чтобы мы могли с вами связаться."
    CONTACT_TIME_QUESTION = "Отлично, почти все готово! Пожалуйста, укажите предпочтительное время для связи."
    FINAL_TEXT = "{}, заявка принята! Мы свяжемся с вами в указанное время."

    NAME_ERROR = "В имени могут быть только буквы!"
    PHONE_NUMBER_ERROR = "Некорректный номер телефона! Номер должен состоять из 10 цифр, начинающихся с +7 или 8"

    def setup(self, bot):
        request_handler = CommandHandler('request', self.run)
        script_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self._next_step)
        bot.add_handler(request_handler)
        bot.add_handler(script_handler)

    async def run(self, update, context):
        if not context.user_data:
            context.user_data['problem_description'] = None  # Начальное состояние
            await context.bot.send_message(chat_id=update.effective_chat.id, text=self.PROBLEM_DESCRIPTION)
        else:
            context.user_data.clear()  # Сброс состояния
            await self.run(update, context)

    async def _step_1(self, update, context):
        context.user_data['user_name'] = None
        context.user_data['problem_description'] = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.USER_NAME_QUESTION)

    async def _step_2(self, update, context):
        user_name = update.message.text
        if user_name.replace(' ', '').isalpha():
            context.user_data['contact_info'] = None
            context.user_data['user_name'] = user_name.title()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=self.CONTACT_INFO_QUESTION.format(user_name.title()))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=self.NAME_ERROR)

    async def _step_3(self, update, context):
        async def validate_phone_number(phone_number):
            pattern = r'^(\+7|8)[0-9]{10}$'
            if re.match(pattern, phone_number):
                return True
            return False

        if await validate_phone_number(update.message.text):
            context.user_data['contact_time'] = None
            context.user_data['contact_info'] = update.message.text
            await context.bot.send_message(chat_id=update.effective_chat.id, text=self.CONTACT_TIME_QUESTION)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=self.PHONE_NUMBER_ERROR)

    async def _step_4(self, update, context):
        context.user_data['contact_time'] = update.message.text
        database = BotDatabase(config['db']['database_path'])

        await database.save_user_data(
            user_id=update.effective_user.id,
            request_id=update.update_id,
            **context.user_data)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=self.FINAL_TEXT.format(context.user_data['user_name']))
        context.user_data.clear()  # Сброс состояния

    async def _next_step(self, update, context):
        if context.user_data:
            await getattr(self, f'_step_{len(context.user_data)}')(update, context)


class UnknownCommand(Commands):
    UNKNOWN_COMMAND_TEXT = "Извините, я не понял вашу команду. Чтобы оставить заявку, отправьте /request."

    def setup(self, bot):
        unknown_handler = MessageHandler(filters.COMMAND, self.run)
        bot.add_handler(unknown_handler)

    async def run(self, update, context):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.UNKNOWN_COMMAND_TEXT)





