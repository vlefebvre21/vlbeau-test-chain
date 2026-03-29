import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open
import sys

# Ajout du chemin parent pour importer file_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_utils import read_file, write_file, list_files, file_exists, get_file_size

class TestFileUtils(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.txt')
        self.test_dir = os.path.join(self.temp_dir, 'subdir')
        self.nested_file = os.path.join(self.test_dir, 'nested.txt')

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.unlink(self.test_file)
        if os.path.exists(self.nested_file):
            os.unlink(self.nested_file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_read_file_success(self):
        write_file(self.test_file, 'Hello, World!')
        content = read_file(self.test_file)
        self.assertEqual(content, 'Hello, World!')

    def test_read_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_file(self.test_file)

    def test_read_file_directory(self):
        os.mkdir(self.test_dir)
        with self.assertRaises(IsADirectoryError):
            read_file(self.test_dir)

    def test_write_file_success(self):
        write_file(self.nested_file, 'Nested content')
        self.assertTrue(os.path.exists(self.nested_file))
        content = read_file(self.nested_file)
        self.assertEqual(content, 'Nested content')

    def test_list_files_success(self):
        os.mkdir(self.test_dir)
        files = list_files(self.temp_dir)
        self.assertIn('subdir', files)

    def test_list_files_not_directory(self):
        write_file(self.test_file, 'test')
        with self.assertRaises(NotADirectoryError):
            list_files(self.test_file)

    def test_file_exists(self):
        self.assertFalse(file_exists(self.test_file))
        write_file(self.test_file, 'test')
        self.assertTrue(file_exists(self.test_file))
        os.mkdir(self.test_dir)
        self.assertFalse(file_exists(self.test_dir))

    def test_get_file_size(self):
        self.assertIsNone(get_file_size(self.test_file))
        write_file(self.test_file, 'abc')
        self.assertEqual(get_file_size(self.test_file), 3)

    @patch('builtins.open', new_callable=mock_open, read_data='mocked content')
    def test_read_file_mocked(self, mock_file):
        path = '/mock/path'
        content = read_file(path)
        mock_file.assert_called_once_with(path, 'r', encoding='utf-8')
        self.assertEqual(content, 'mocked content')

if __name__ == '__main__':
    unittest.main()
