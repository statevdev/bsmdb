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
    """
    Абстрактный класс для команд бота.

    Этот класс определяет интерфейс для всех команд, которые могут быть
    добавлены к боту. Все подклассы должны реализовать методы `setup` и `run`.
    При добавлении нового класса важно расположить его выше класса UnknownCommand,
    иначе бот не сможет посылать ответ на незнакомую команду.
    """

    @abstractmethod
    def setup(self, bot) -> None:
        """
        Настраивает команду для указанного бота.

        Этот метод должен быть реализован в подклассах для привязки
        команды к боту.

        Параметры:
        bot: Объект бота, к которому будет привязана команда.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        pass

    @abstractmethod
    async def run(self, update, context) -> None:
        """
        Выполняет команду при получении обновления.

        Этот метод должен быть реализован в подклассах для обработки
        входящих обновлений и выполнения соответствующих действий.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        pass


class CommandsFactory:
    """
    Фабрика для создания команд бота.

    Этот класс предоставляет статический метод для создания экземпляров
    всех подклассов абстрактного класса `Commands` и их настройки.
    """

    @staticmethod
    def create_commands(bot) -> list:
        """
        Создает и настраивает команды для указанного бота.

        Этот метод создает экземпляры всех подклассов `Commands`,
        вызывает метод `setup` для каждой команды и возвращает список
        настроенных команд.

        Параметры:
        bot: Объект бота, который будет передан каждой команде для настройки.

        Возвращает:
        list: Список настроенных команд.
        """
        commands = []
        for command_class in Commands.__subclasses__():
            command = command_class()
            command.setup(bot)
            commands.append(command)
        return commands


class StartCommand(Commands):
    """
    Команда для начала взаимодействия с ботом.

    Эта команда обрабатывает команду /start и отправляет пользователю
    сообщение с инструкциями по созданию заявки.
    """
    START_COMMAND_TEXT = (
        "Чтобы создать заявку, вам нужно ответить на несколько вопросов.\n\nОтправьте команду /request, "
        "чтобы начать.")

    def setup(self, bot) -> None:
        """
        Настраивает команду для указанного бота.

        Этот метод привязывает команду /start к обработчику, который
        будет вызывать метод `run`.

        Параметры:
        bot: Объект бота, к которому будет привязана команда.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        start_handler = CommandHandler('start', self.run)
        bot.add_handler(start_handler)

    async def run(self, update, context) -> None:
        """
        Обрабатывает команду /start.

        Этот метод отправляет пользователю сообщение с инструкциями
        по созданию заявки.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.START_COMMAND_TEXT)


class HelpCommand(Commands):
    """
    Команда для получения справки по использованию бота.

    Эта команда обрабатывает команду /help и отправляет пользователю
    сообщение с инструкциями по созданию заявки.
    """
    HELP_COMMAND_TEXT = (
        "Чтобы создать заявку, вам нужно ответить на несколько вопросов.\n\nОтправьте команду /request, "
        "чтобы начать."
    )

    def setup(self, bot) -> None:
        """
        Настраивает команду для указанного бота.

        Этот метод привязывает команду /help к обработчику, который
        будет вызывать метод `run`.

        Параметры:
        bot: Объект бота, к которому будет привязана команда.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        help_handler = CommandHandler('help', self.run)
        bot.add_handler(help_handler)

    async def run(self, update, context) -> None:
        """
        Обрабатывает команду /help.

        Этот метод отправляет пользователю сообщение с инструкциями
        по созданию заявки.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.HELP_COMMAND_TEXT)


class SettingsCommand(Commands):
    """
    Команда для получения информации о настройках.

    Эта команда обрабатывает команду /settings и отправляет пользователю
    сообщение с инструкциями по созданию заявки и изменению информации.
    """
    SETTINGS_COMMAND_TEXT = (
        "С моей помощью вы можете создать заявку. Изменить или дополнить информацию вы сможете "
        "когда мы с вами свяжемся."
    )

    def setup(self, bot) -> None:
        """
        Настраивает команду для указанного бота.

        Этот метод привязывает команду /settings к обработчику, который
        будет вызывать метод `run`.

        Параметры:
        bot: Объект бота, к которому будет привязана команда.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        settings_handler = CommandHandler('settings', self.run)
        bot.add_handler(settings_handler)

    async def run(self, update, context) -> None:
        """
        Обрабатывает команду /settings.

        Этот метод отправляет пользователю сообщение с информацией
        о создании заявки и изменении информации.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.SETTINGS_COMMAND_TEXT)


class RequestCommand(Commands):
    """
    Команда для обработки заявок от пользователей.

    Эта команда обрабатывает команду /request и ведет пользователя через
    процесс создания заявки, задавая последовательные вопросы.
    """
    PROBLEM_DESCRIPTION = "Чтобы оставить заявку, опишите как можно подробнее вашу проблему."
    USER_NAME_QUESTION = "Понял вас! Как я могу к вам обращаться?"
    CONTACT_INFO_QUESTION = "Хорошо, {}! Укажите свой номер телефона, чтобы мы могли с вами связаться."
    CONTACT_TIME_QUESTION = "Отлично, почти все готово! Пожалуйста, укажите предпочтительное время для связи."
    FINAL_TEXT = "{}, заявка принята! Мы свяжемся с вами в указанное время."

    NAME_ERROR = "В имени могут быть только буквы!"
    PHONE_NUMBER_ERROR = "Некорректный номер телефона! Номер должен состоять из 10 цифр, начинающихся с +7 или 8"

    def setup(self, bot) -> None:
        """
        Настраивает команду для указанного бота.

        Этот метод привязывает команду /request к обработчику, который
        будет вызывать метод `run`, а также добавляет обработчик для
        текстовых сообщений, чтобы вести пользователя через процесс
        создания заявки.

        Параметры:
        bot: Объект бота, к которому будет привязана команда.
        """
        request_handler = CommandHandler('request', self.run)
        script_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self._next_step)
        bot.add_handler(request_handler)
        bot.add_handler(script_handler)

    async def run(self, update, context) -> None:
        """
        Запускает процесс создания заявки.

        Этот метод отправляет пользователю сообщение с просьбой описать
        проблему. Если пользователь уже начал процесс, состояние сбрасывается
        и процесс начинается заново.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        if not context.user_data:
            context.user_data['problem_description'] = None  # Начальное состояние
            await context.bot.send_message(chat_id=update.effective_chat.id, text=self.PROBLEM_DESCRIPTION)
        else:
            context.user_data.clear()  # Сброс состояния
            await self.run(update, context)

    async def _step_1(self, update, context) -> None:
        """
        Обрабатывает первый шаг процесса создания заявки.

        Этот метод сохраняет описание проблемы и запрашивает имя пользователя.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        context.user_data['user_name'] = None
        context.user_data['problem_description'] = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.USER_NAME_QUESTION)

    async def _step_2(self, update, context) -> None:
        """
        Обрабатывает второй шаг процесса создания заявки.

        Этот метод проверяет имя пользователя и запрашивает номер телефона.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        user_name = update.message.text
        if user_name.replace(' ', '').isalpha():
            context.user_data['contact_info'] = None
            context.user_data['user_name'] = user_name.title()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=self.CONTACT_INFO_QUESTION.format(user_name.title()))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=self.NAME_ERROR)

    async def _step_3(self, update, context) -> None:
        """
        Обрабатывает третий шаг процесса создания заявки.

        Этот метод проверяет номер телефона и запрашивает предпочтительное время для связи.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """

        async def validate_phone_number(phone_number: str) -> bool:
            """
            Проверяет, является ли номер телефона корректным.

            Номер телефона должен начинаться с +7 или 8 и состоять из 10 цифр.

            Параметры:
            phone_number (str): Номер телефона для проверки.

            Возвращает:
            bool: True, если номер телефона корректен, иначе False.
            """
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

    async def _step_4(self, update, context) -> None:
        """
        Обрабатывает четвертый шаг процесса создания заявки.

        Этот метод сохраняет данные пользователя в базе данных и отправляет
        сообщение о том, что заявка принята.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        context.user_data['contact_time'] = update.message.text
        database = BotDatabase(config['db']['database_path'])

        await database.save_user_data(
            user_id=update.effective_user.id,
            request_id=update.update_id,
            **context.user_data)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=self.FINAL_TEXT.format(context.user_data['user_name']))
        context.user_data.clear()  # Сброс состояния

    async def _next_step(self, update, context) -> None:
        """
        Переходит к следующему шагу в процессе создания заявки.

        Этот метод вызывает соответствующий метод шага в зависимости от
        текущего состояния пользователя.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        if context.user_data:
            await getattr(self, f'_step_{len(context.user_data)}')(update, context)


class UnknownCommand(Commands):
    """
    Команда для обработки неизвестных команд.

    Эта команда обрабатывает любые команды, которые не были распознаны
    ботом, и отправляет пользователю сообщение с информацией о том,
    как оставить заявку.
    """
    UNKNOWN_COMMAND_TEXT = "Извините, я не понял вашу команду. Чтобы оставить заявку, отправьте /request."

    def setup(self, bot) -> None:
        """
        Настраивает команду для указанного бота.

        Этот метод добавляет обработчик для всех команд, которые не были
        распознаны, и вызывает метод `run`.

        Параметры:
        bot: Объект бота, к которому будет привязана команда.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        unknown_handler = MessageHandler(filters.COMMAND, self.run)
        bot.add_handler(unknown_handler)

    async def run(self, update, context):
        """
        Обрабатывает неизвестные команды.

        Этот метод отправляет пользователю сообщение о том, что команда
        не распознана, и предоставляет информацию о том, как оставить заявку.

        Параметры:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Контекст, содержащий информацию о состоянии бота.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.UNKNOWN_COMMAND_TEXT)






