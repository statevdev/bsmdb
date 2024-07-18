import git
from apscheduler.schedulers.background import BackgroundScheduler
from expdata import ExportData
from bot_settings import pageupdconfig


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

        current_branch = repo.active_branch
        tracking_branch = current_branch.tracking_branch()

        if tracking_branch is None:
            repo.git.branch('--set-upstream-to=origin/main', current_branch.name)

        repo.remotes.origin.push()

    def _add_job(self, at_hour, at_minutes):
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            self.push_to_github, 'cron',
            hour=at_hour, minute=at_minutes
        )
        scheduler.start()
        return scheduler

    def run(self, hour, minutes):
        self.htmls_creator()
        scheduler = self._add_job(at_hour=hour, at_minutes=minutes)
        return scheduler

    def htmls_creator(self):
        for table_name, output_file in self.html_files.items():
            ExportData.export_to_html(self.database_path, table_name, output_file)


if __name__ == '__main__':
    updater = GithubPageUpdater(**pageupdconfig)
    updater.htmls_creator()
    updater.push_to_github()
