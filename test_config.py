import os
import tempfile

temp_dir = tempfile.mkdtemp()  # Создаем временную директорию
test_config = {
    'bot': {
        'telegram_token': 'test_token',
    },
    'db': {
        'database_path': os.path.join(temp_dir, 'test.db'),
        'key': b'EGTkidMX5S8nAnTuqfGCU/FpaCzo4xs88Y3vfQsPxwM=',
    },
    'pageupd': {
        'local_repo': temp_dir,
        'database_path': os.path.join(temp_dir, 'test.db'),
        'html_files': {
            'users': os.path.join(temp_dir, 'test_users.html'),
            'requests': os.path.join(temp_dir, 'test_requests.html')
        },
        'commit_message': 'Test'
    },
    'pagedwn': {
        'tables_urls': {
            'users': 'https://statevdev.github.io/bsmdb_page/users.html',
            'requests': 'https://statevdev.github.io/bsmdb_page/requests.html'
        }
    },
    'update_time': {
        'hour': 18,
        'minutes': 0
    }
}