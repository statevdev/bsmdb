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
    def __init__(self, token):
        self.application = ApplicationBuilder().token(token).build()
        self.commands = CommandsFactory.create_commands(self.application)

    def run(self):
        return self.application.run_polling()


def main():
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
