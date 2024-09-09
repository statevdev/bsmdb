import argparse
import sqlite3
import pandas
from docx import Document
from crypt_data import Crypt


class ExportData:
    """
    Класс для экспорта данных из SQLite базы данных в различные форматы.
    """
    @staticmethod
    def export_to_word(database_path: str, table_name: str, output_file: str = None) -> None:
        """
        Экспортирует данные из указанной таблицы базы данных в формат Word (.docx).

        :param database_path: Путь к файлу базы данных SQLite.
        :param table_name: Имя таблицы, данные из которой нужно экспортировать.
        :param output_file: Путь к выходному файлу. Если не указан, используется имя таблицы.
        :return: None
        """
        connection = sqlite3.connect(database_path)
        try:
            dataframe = pandas.read_sql_query(f"SELECT * FROM {table_name}", connection)
            doc = Document()
            table = doc.add_table(rows=dataframe.shape[0] + 1, cols=dataframe.shape[1])
            table.style = 'Table Grid'

            for i, column_name in enumerate(dataframe.columns):
                table.cell(0, i).text = column_name

            for i, row in enumerate(dataframe.itertuples(), 1):
                for j, value in enumerate(row[1:]):
                    table.cell(i, j).text = Crypt.decrypt_data(value)

            doc.save(output_file if output_file else f'{table_name}.docx')
        except Exception as e:
            print(f"Ошибка при экспорте в Word: {e}")
        finally:
            connection.close()

    @staticmethod
    def export_to_excel(database_path: str, table_name: str, output_file: str = None) -> None:
        """
        Экспортирует данные из указанной таблицы базы данных в формат Excel (.xlsx).

        :param database_path: Путь к файлу базы данных SQLite.
        :param table_name: Имя таблицы, данные из которой нужно экспортировать.
        :param output_file: Путь к выходному файлу. Если не указан, используется имя таблицы.
        :return: None
        """
        connection = sqlite3.connect(database_path)
        try:
            dataframe = pandas.read_sql_query(f"SELECT * FROM {table_name}", connection)
            dataframe = dataframe.applymap(Crypt.decrypt_data)
            dataframe.to_excel(output_file if output_file else f'{table_name}.xlsx', index=False, engine='openpyxl')
        except Exception as e:
            print(f"Ошибка при экспорте в Excel: {e}")
        finally:
            connection.close()

    @staticmethod
    def export_to_csv(database_path: str, table_name: str, output_file: str = None) -> None:
        """
        Экспортирует данные из указанной таблицы базы данных в формат CSV (.csv).

        :param database_path: Путь к файлу базы данных SQLite.
        :param table_name: Имя таблицы, данные из которой нужно экспортировать.
        :param output_file: Путь к выходному файлу. Если не указан, используется имя таблицы.
        :return: None
        """
        connection = sqlite3.connect(database_path)
        try:
            dataframe = pandas.read_sql_query(f"SELECT * FROM {table_name}", connection)
            dataframe = dataframe.applymap(Crypt.decrypt_data)
            dataframe.to_csv(output_file if output_file else f'{table_name}.csv', index=False, encoding='UTF-8')
        except Exception as e:
            print(f"Ошибка при экспорте в CSV: {e}")
        finally:
            connection.close()

    @staticmethod
    def export_to_html(database_path: str, table_name: str, output_file: str = None, decrypt: bool = True) -> None:
        """
        Экспортирует данные из указанной таблицы базы данных в формат HTML (.html).

        :param database_path: Путь к файлу базы данных SQLite.
        :param table_name: Имя таблицы, данные из которой нужно экспортировать.
        :param output_file: Путь к выходному файлу. Если не указан, используется имя таблицы.
        :param decrypt: Флаг, указывающий, нужно ли расшифровывать данные.
        :return: None
        """
        connection = sqlite3.connect(database_path)
        try:
            dataframe = pandas.read_sql_query(f"SELECT * FROM {table_name}", connection)
            dataframe = dataframe.applymap(Crypt.decrypt_data) if decrypt else dataframe
            html_content = dataframe.to_html(index=False, border=1)

            # Добавляем мета-тег кодировки
            html_file = f"""
              <!DOCTYPE html>
              <html lang="en">
              <head>
                  <meta charset="UTF-8">
                  <title>{table_name}</title>
              </head>
              <body>
                  {html_content}
              </body>
              </html>
              """
            with open(output_file if output_file else f'{table_name}.html', 'w', encoding='UTF-8') as file:
                file.write(html_file)
        except Exception as e:
            print(f"Ошибка при экспорте в HTML: {e}")
        finally:
            connection.close()


def main() -> None:
    """
    Главная функция для обработки аргументов командной строки и вызова методов экспорта.

    :return: None
    """
    parser = argparse.ArgumentParser(description='Export data from SQLite database to various formats.')

    parser.add_argument('method', choices=['word', 'excel', 'csv', 'html'], help='Export method')
    parser.add_argument('database_path', help='Path to the SQLite database file')
    parser.add_argument('table_name', help='Name of the table to export')
    parser.add_argument('-o', '--output_file', help='Path to the output file')

    args = parser.parse_args()

    export_methods = {
        'word': ExportData.export_to_word,
        'excel': ExportData.export_to_excel,
        'csv': ExportData.export_to_csv,
        'html': ExportData.export_to_html
    }

    if args.method in export_methods:
        export_methods[args.method](args.database_path, args.table_name, args.output_file)


if __name__ == '__main__':
    """
    Этот модуль можно запустить напрямую через терминал в формате:
    `python expdata.py <формат файла (word, excel, csv, html)> <путь к базе данных> <имя таблицы> <путь, по которому сохранить файл (опционально)>`,
    тем самым вручную экспортировав данные в эту же папку, либо в другое указанное место.
    """
    main()
