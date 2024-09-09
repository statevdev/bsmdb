import git
from apscheduler.schedulers.background import BackgroundScheduler
from expdata import ExportData
try:
    from config import config
except ImportError:
    from test_config import test_config
    config = test_config


class GithubPageUpdater:
    """
    Класс для обновления страницы на GitHub с помощью автоматического экспорта данных
    и коммита изменений в репозиторий.
    """
    def __init__(self, local_repo: str, database_path: str, html_files: dict, commit_message: str):
        """
        Инициализация класса GithubPageUpdater.

        :param local_repo: Путь к локальному репозиторию Git.
        :param database_path: Путь к базе данных для экспорта данных.
        :param html_files: Словарь, где ключи - имена таблиц, а значения - пути к выходным HTML файлам.
        :param commit_message: Сообщение для коммита в Git.
        """
        self.local_repo = local_repo
        self.database_path = database_path
        self.html_files = html_files
        self.commit_message = commit_message

    def push_to_github(self) -> None:
        """
        Коммитит изменения в локальном репозитории и отправляет их на GitHub.
        """
        repo = git.Repo(self.local_repo)  # Инициализация репозитория
        repo.git.add(list(self.html_files.values()))  # Добавление HTML файлов в индекс
        repo.index.commit(self.commit_message)  # Коммит изменений

        current_branch = repo.active_branch  # Получение текущей ветки
        tracking_branch = current_branch.tracking_branch()  # Получение отслеживаемой ветки

        # Установка upstream ветки, если она не установлена
        if tracking_branch is None:
            repo.git.branch('--set-upstream-to=origin/main', current_branch.name)

        repo.remotes.origin.push()  # Отправка изменений на GitHub

    def _add_job(self, at_hour: int, at_minutes: int) -> BackgroundScheduler:
        """
        Добавляет задачу в планировщик для автоматического обновления GitHub.

        :param at_hour: Час, в который будет выполняться задача.
        :param at_minutes: Минуты, в которые будет выполняться задача.
        :return: Экземпляр планировщика.
        """
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            self.push_to_github, 'cron',
            hour=at_hour, minute=at_minutes
        )
        scheduler.start()  # Запуск планировщика
        return scheduler

    def run_on_schedule(self, hour: int, minutes: int) -> BackgroundScheduler:
        """
        Запускает создание HTML файлов и добавляет задачу в планировщик.

        :param hour: Час, в который будет выполняться задача.
        :param minutes: Минуты, в которые будет выполняться задача.
        :return: Экземпляр планировщика.
        """
        self.htmls_creator()  # Создание HTML файлов
        scheduler = self._add_job(at_hour=hour, at_minutes=minutes)  # Добавление задачи в планировщик
        return scheduler

    def run_now(self) -> None:
        """
        Выполняет создание HTML файлов и немедленно отправляет изменения на GitHub.
        """
        self.htmls_creator()  # Создание HTML файлов
        self.push_to_github()  # Отправка изменений на GitHub

    def htmls_creator(self) -> None:
        """
        Создает HTML файлы из данных базы данных.
        """
        for table_name, output_file in self.html_files.items():
            ExportData.export_to_html(self.database_path, table_name, output_file, decrypt=False)  # Экспорт данных в HTML


if __name__ == '__main__':
    """
    Этот можно запустить напрямую через терминал, тем самым обновив страницу GithubPages принудительно.
    """
    updater = GithubPageUpdater(**config['pageupd'])
    updater.run_now()

