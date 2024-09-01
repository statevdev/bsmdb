import asyncio
import os
import shutil
import sqlite3
import tempfile
import unittest
from unittest.mock import patch, AsyncMock, Mock

from docx import Document

from dbscripts import BotDatabase
from expdata import ExportData
from test_config import test_config


class TestExportData(unittest.TestCase):
#     def setUp(self):
#         self.update = Mock()
#         self.context = Mock()
#         self.context.user_data = {}
#
#     @patch.dict('config.config', test_config)
#     @patch("dbscripts.BotDatabase")
    def test_export_to_word(self):
        db_path = test_config['db']['database_path']
        docx_path = os.path.join(os.path.dirname(db_path), 'test.docx')

        database = BotDatabase(db_path)
        database.create_tables()

        # Запускаем метод save_user_data
        asyncio.run(database.save_user_data(
            "test_id",
            "test_user_name",
            "test_request_id",
            "test_problem_description",
            "test_contact_info",
            "test_contact_time"
        ))

        ExportData.export_to_word(db_path, 'users', output_file=docx_path)

        self.assertTrue(os.path.exists(docx_path))

        doc = Document(docx_path)
        if doc.tables:
            table = doc.tables[0]  # Получаем первую таблицу
            second_row = table.rows[1]  # Получаем вторую строку
            second_row_text = [cell.text for cell in second_row.cells]  # Получаем текст из каждой ячейки

            self.assertEqual(['test_id', 'test_user_name', 'test_contact_info'], second_row_text)

        shutil.rmtree(os.path.dirname(db_path))
