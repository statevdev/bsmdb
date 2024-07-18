import argparse
import sqlite3
import pandas
from docx import Document


class ExportData():
    @staticmethod
    def export_to_word(database_path, table_name, output_file):
        with sqlite3.connect(database_path) as connection:
            dataframe = pandas.read_sql_query(f"SELECT * FROM {table_name}", connection)
            doc = Document()
            table = doc.add_table(rows=dataframe.shape[0] + 1, cols=dataframe.shape[1])
            table.style = 'Table Grid'

            for i, column_name in enumerate(dataframe.columns):
                table.cell(0, i).text = column_name

            for i, row in enumerate(dataframe.itertuples(), 1):
                for j, value in enumerate(row[1:]):
                    table.cell(i, j).text = str(value)

            doc.save(output_file if output_file else f'{table_name}.docx')

    @staticmethod
    def export_to_excel(database_path, table_name, output_file):
        with sqlite3.connect(database_path) as connection:
            dataframe = pandas.read_sql_query(f"SELECT * FROM {table_name}", connection)
            dataframe.to_excel(output_file if output_file else f'{table_name}.xlsx', index=False, engine='openpyxl')

    @staticmethod
    def export_to_csv(database_path, table_name, output_file):
        with sqlite3.connect(database_path) as connection:
            dataframe = pandas.read_sql_query(f"SELECT * FROM {table_name}", connection)
            dataframe.to_csv(output_file if output_file else f'{table_name}.csv', index=False, encoding='UTF-8')

    @staticmethod
    def export_to_html(database_path, table_name, output_file):
        with sqlite3.connect(database_path) as connection:
            dataframe = pandas.read_sql_query(f"SELECT * FROM {table_name}", connection)
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


def main():
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
    main()
