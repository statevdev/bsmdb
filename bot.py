import logging
from telegram.ext import ApplicationBuilder
from commands import CommandsFactory
from database_scripts import BotDatabase
from pageupd import GithubPageUpdater
from bot_settings import bot_config, pageupdconfig

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
    database = BotDatabase(bot_config['database_path'])
    database.create_tables()

    # Инициализация и запуск UpdateGithubPage
    updater = GithubPageUpdater(**pageupdconfig)
    scheduler = updater.run(3, 5)

    try:
        # Запуск бота
        bot = Bot(bot_config['telegram_token'])
        bot.run()

        # Держим главный поток живым, чтобы позволить планировщику работать
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
