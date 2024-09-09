import logging
from telegram.ext import ApplicationBuilder
from commands import CommandsFactory
from dbscripts import BotDatabase
from pageupd import GithubPageUpdater
try:
    from config import config
except ImportError:
    from test_config import test_config
    config = test_config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class Bot:
    def __init__(self, token: str) -> None:
        """
        Инициализация бота.

        Этот метод создает экземпляр бота и привязывает команды к приложению.

        Параметры:
        token (str): Токен для аутентификации бота в API.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        self.application = ApplicationBuilder().token(token).build()
        self.commands = CommandsFactory.create_commands(self.application)

    def run(self) -> None:
        """
        Запускает бота и начинает слушать сообщения от пользователей.

        Этот метод инициирует процесс опроса, который позволяет боту получать и обрабатывать входящие сообщения.

        Возвращает:
        None: Этот метод ничего не возвращает.
        """
        return self.application.run_polling()


def main() -> None:
    """
    Главная функция приложения.

    Эта функция инициализирует базу данных, настраивает и запускает обновление страницы на GitHub,
    а также инициализирует и запускает бота Telegram. Она удерживает главный поток живым,
    чтобы позволить планировщику работать, пока бот активен.

    Возвращает:
    None: Эта функция ничего не возвращает.
    """
    # Инициализация базы данных
    database = BotDatabase(config['db']['database_path'])
    database.create_tables()

    # Инициализация и запуск UpdateGithubPage
    updater = GithubPageUpdater(**config['pageupd'])
    scheduler = updater.run_on_schedule(**config['update_time'])

    try:
        # Запуск бота
        bot = Bot(config['bot']['telegram_token'])
        bot.run()

        # Держим главный поток живым, чтобы позволить планировщику работать
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    main()
