import argparse
import requests
from bs4 import BeautifulSoup
from config import config

from crypt_data import Crypt


def github_page_downloader(table_name, output_file, decrypt):
    default_url = config['pagedwn']['tables_urls'][table_name]
    response = requests.get(default_url)
    html_data = response.text

    soup = BeautifulSoup(html_data, 'html.parser')

    for td in soup.find_all('td'):
        td.string = Crypt.decrypt_data(td.string) if decrypt else td.string

    with open(output_file if output_file else f'{table_name}.html', 'w', encoding='UTF-8') as file:
        file.write(soup.prettify())


def main():
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
    main()
