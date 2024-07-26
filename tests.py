import unittest
from unittest.mock import patch
import re
import src.data.dataReadWrite as dataReadWrite
from datetime import datetime
from src.globals import Globals

class TestGetBaseFilePath(unittest.TestCase):

    def test_get_base_file_path(self):
        #check to ensure we can successfully set base file paths with the given machine (either windows or mac/linux)
        base_path = dataReadWrite.get_base_file_path()
        windows_pattern = re.compile(r'C:\\Users\\[^\\]+\\Desktop')
        maclin_pattern = re.compile(r'/home/[^/]+/Desktop')
        self.assertTrue(bool(windows_pattern.match(base_path) or maclin_pattern.match(base_path)))

class TestGlobals(unittest.TestCase):

    def setUp(self):
        self.globals = Globals()

    def test_preferences_file_path(self):
        test_path = '/test/preferences/path'
        self.globals.preferences_file_path = test_path
        self.assertEqual(self.globals.preferences_file_path, test_path)

    def test_calorie_tracker_data_file_path(self):
        test_path = '/test/calorie/tracker/path'
        self.globals.calorie_tracker_data_file_path = test_path
        self.assertEqual(self.globals.calorie_tracker_data_file_path, test_path)

    def test_selected_date(self):
        test_date = '2024-01-01'
        self.globals.selected_date = test_date
        self.assertEqual(self.globals.selected_date, test_date)

    def test_preferences(self):
        test_preferences = {'name': 'Test User', 'daily_calorie_goal': 1500}
        self.globals.preferences = test_preferences
        self.assertEqual(self.globals.preferences, test_preferences)

    def test_calorie_tracker_data(self):
        test_data = [
            {'date': '2024-01-01', 'calories_total': 2000},
            {'date': '2024-01-02', 'calories_total': 1800}
        ]
        self.globals.calorie_tracker_data = test_data
        self.assertEqual(self.globals.calorie_tracker_data, sorted(test_data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True))

if __name__ == '__main__':
    unittest.main()
