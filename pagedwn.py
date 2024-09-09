import argparse
import requests
from bs4 import BeautifulSoup
try:
    from config import config
except ImportError:
    from test_config import test_config
    config = test_config

from crypt_data import Crypt


def github_page_downloader(table_name: str, output_file: str, decrypt: bool) -> None:
    """
    Скачивает html-страницу с указанной таблицей.

    :param table_name: Имя таблицы, которую нужно скачать.
    :param output_file: Путь к выходному файлу. Если не указан, используется имя таблицы.
    :param decrypt: Флаг, указывающий, нужно ли расшифровывать данные.
    :return: None
    """
    default_url = config['pagedwn']['tables_urls'][table_name]
    response = requests.get(default_url)
    html_data = response.text

    soup = BeautifulSoup(html_data, 'html.parser')

    for td in soup.find_all('td'):
        td.string = Crypt.decrypt_data(td.string) if decrypt else td.string

    with open(output_file if output_file else f'{table_name}.html', 'w', encoding='UTF-8') as file:
        file.write(soup.prettify())


def main() -> None:
    """
    Главная функция для обработки аргументов командной строки и вызова функции github_page_downloader.

    :return: None
    """
    parser = argparse.ArgumentParser(description='Downloading table from Github Page.')

    parser.add_argument('table_name', help='Name of the table to download')
    parser.add_argument('-o', '--output_file', help='Path to the output file')
    parser.add_argument('-d', '--decrypt', help='Decryption flag')

    args = parser.parse_args()

    decrypt_flag = True
    if args.decrypt:
        if args.decrypt.lower() == 'true':
            decrypt_flag = True
        elif args.decrypt.lower() == 'false':
            decrypt_flag = False
        else:
            print('Incorrect flag')

    github_page_downloader(args.table_name, args.output_file, decrypt=decrypt_flag)


if __name__ == '__main__':
    """
    Этот модуль можно запустить напрямую через терминал в формате:
    
    `python pagedwn.py <имя таблицы> -o <путь, по которому сохранить файл (опционально)> -d <значение флага дешифрования
    : True или False (опционально, по умолчанию стоит флаг True)>`,

    тем самым вручную скачав таблицу в эту же папку, либо в другое указанное место.
    """
    main()
