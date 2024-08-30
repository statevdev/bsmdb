import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from pagedwn import github_page_downloader
from test_config import test_config


class TestGithubPageDownloader(unittest.TestCase):
    @patch('config.config', test_config)
    def test_github_page_downloader(self):
        temp_dir_with_html = tempfile.mkdtemp()
        test_path = os.path.join(temp_dir_with_html, 'test.html')
        github_page_downloader('users', output_file=test_path, decrypt=True)

        self.assertTrue(os.path.exists(test_path))

        shutil.rmtree(temp_dir_with_html)


if __name__ == '__main__':
    unittest.main()