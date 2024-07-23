import logging
from telegram.ext import ApplicationBuilder
from commands import CommandsFactory
from database_scripts import BotDatabase
from pageupd import GithubPageUpdater
from config import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class Bot:
    def __init__(self, token):
        self.bot = ApplicationBuilder().token(token).build()
        self.commands = CommandsFactory.create_commands(self.bot)

    def run(self):
        self.bot.run_polling()


if __name__ == '__main__':
    # Инициализация базы данных
    database = BotDatabase(config['db']['database_path'])
    database.create_tables()

    # Инициализация и запуск UpdateGithubPage
    updater = GithubPageUpdater(**config['pageupd'])
    scheduler = updater.run(**config['update_time'])

    try:
        # Запуск бота
        bot = Bot(config['bot']['telegram_token'])
        bot.run()

        # Держим главный поток живым, чтобы позволить планировщику работать
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
