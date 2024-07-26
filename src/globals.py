from datetime import datetime

class Globals:
    def __init__(self):
        self._preferences_file_path = ''
        self._calorie_tracker_data_file_path = ''
        self._selected_date = ''
        self._preferences = {}
        self._calorie_tracker_data = []

    @property
    def preferences_file_path(self):
        return self._preferences_file_path

    @preferences_file_path.setter
    def preferences_file_path(self, value):
        self._preferences_file_path = value

    @property
    def calorie_tracker_data_file_path(self):
        return self._calorie_tracker_data_file_path

    @calorie_tracker_data_file_path.setter
    def calorie_tracker_data_file_path(self, value):
        self._calorie_tracker_data_file_path = value

    @property
    def selected_date(self):
        return self._selected_date

    @selected_date.setter
    def selected_date(self, value):
        self._selected_date = value

    @property
    def preferences(self):
        return self._preferences

    @preferences.setter
    def preferences(self, value):
        self._preferences = value

    @property
    def calorie_tracker_data(self):
        return sorted(self._calorie_tracker_data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)

    @calorie_tracker_data.setter
    def calorie_tracker_data(self, value):
        self._calorie_tracker_data = value

globals = Globals()