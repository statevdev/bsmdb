import git
from apscheduler.schedulers.background import BackgroundScheduler
from expdata import ExportData


class GithubPageUpdater:
    def __init__(self, local_repo, database_path, html_files, commit_message):
        self.local_repo = local_repo
        self.database_path = database_path
        self.html_files = html_files
        self.commit_message = commit_message

    def push_to_github(self):
        repo = git.Repo(self.local_repo)
        repo.git.add(list(self.html_files.values()))
        repo.index.commit(self.commit_message)
        repo.remotes.origin_page.push()

    def add_job(self, at_hour, at_minutes):
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            self.push_to_github, 'cron',
            hour=at_hour, minute=at_minutes
        )
        scheduler.start()
        return scheduler

    def run(self, hour, minutes):
        for table_name, output_file in self.html_files.items():
            ExportData.export_to_html(self.database_path, table_name, output_file)
        scheduler = self.add_job(at_hour=hour, at_minutes=minutes)
        return scheduler

