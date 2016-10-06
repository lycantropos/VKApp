import os
import unittest
from datetime import datetime

from vk_app.utils import get_year_month_date, find_file, check_dir, get_valid_dirs


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.date_time = datetime(2016, 9, 30, 23, 55, 8)
        self.year_month_date_str = "2016-09"
        self.file_path = __file__
        self.file_name = os.path.basename(self.file_path)
        self.file_dir = os.path.dirname(self.file_path)
        self.dirs = ['dir', 'subdir', None, 'subsubdir']
        self.valid_dirs = ['dir', 'subdir', 'subsubdir']

    def test_get_year_month_date(self):
        self.assertEqual(get_year_month_date(self.date_time, sep='-'), self.year_month_date_str)

    def test_find_file(self):
        self.assertEqual(find_file(self.file_name, self.file_dir), self.file_path)

    def test_get_valid_dirs(self):
        valid_dirs = get_valid_dirs(*self.dirs)
        self.assertEqual(self.valid_dirs, valid_dirs)

    def test_check_dir(self):
        check_dir(self.file_dir, *self.valid_dirs)
        test_dir = os.path.join(self.file_dir, *self.valid_dirs)
        self.assertTrue(os.path.exists(test_dir))
        for ind in range(len(self.valid_dirs)):
            test_dir = os.path.join(self.file_dir, *self.valid_dirs[:len(self.valid_dirs) - ind])
            os.rmdir(test_dir)


if __name__ == '__main__':
    test = TestUtils()
    test.run()
