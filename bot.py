import logging
from telegram.ext import ApplicationBuilder
from bsmdb.commands import CommandsFactory
from bsmdb.database_scripts import BotDatabase
from bsmdb.pageupd import GithubPageUpdater
from bsmdb.config import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class Bot:
    def __init__(self, token):
        self.application = ApplicationBuilder().token(token).build()
        self.commands = CommandsFactory.create_commands(self.application)

    def run(self):
        self.application.run_polling()


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
