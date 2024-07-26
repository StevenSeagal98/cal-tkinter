#same approach as single_day.py, but with different data
class PreferencesData:
    def __init__(self):
        self.content = {}
        self.data = None
    #get preferences data from globals
    def get_preferences_data(self):
        import src.globals as globals
        return globals.preferences
    #set content for preferences view, used for init and updates
    def set_content(self):
        import src.globals as globals
        preferences_data = self.get_preferences_data()
        self.content = {
            'title': 'Edit Preferences',
            'widgets': [
                {'type': 'label', 'text': 'Edit Preferences'},
                {'type': 'entry', 'text': 'Name', 'starting': preferences_data['name']},
                {'type': 'entry', 'text': 'Daily Calorie Goal', 'starting': str(preferences_data['daily_calorie_goal'])},
                {'type': 'button', 'text': 'Save Preferences', 'command': lambda: self.save_preferences(globals.editing_data)}
            ],
            'update': self.update
        }

    # refreshes content of instantiated obj for view updates
    def update(self):
        self.data = self.get_preferences_data()
        self.set_content()
        print('Updating preferences data')
        print('Updated content: ', self.content)

    # save preferences data to JSON file, used throughout the app
    def save_preferences(self, d):
        import src.globals as globals
        from src.data.dataReadWrite import write_to_preferences
        data = {
            'name': d['name'],
            'daily_calorie_goal': d['daily calorie goal']
        }
        passed_check = True
        passed_check_dict = {
            'title': 'Success',
            'message': 'Preferences saved successfully!',
            'color': 'green',
            'success': True
        }
        failed_check_dict = {
            'title': 'Error',
            'message': 'Preferences did not pass validation',
            'color': 'red',
            'success': False
        }
        # data validation for preferences before saving
        if not isinstance(data['name'], str) or not data['name']:
            passed_check = False

        if not data['daily_calorie_goal'].isdigit():
            passed_check = False

        if passed_check:
            #save to json file
            preferences_data = self.get_preferences_data()
            preferences_data['name'] = data['name']
            preferences_data['daily_calorie_goal'] = int(data['daily_calorie_goal'])
            write_to_preferences(preferences_data)
            globals.preferences = preferences_data
            return passed_check_dict
        else:
            return failed_check_dict

#instantiate variables for preferences data, used to pull data for front end view
preferences_data = PreferencesData()
preferences_data.update()

#update preferences data
def update_preferences_data():
    import src.globals as globals
    try:
        preferences_data.update()
    except Exception as e:
        print('Error updating preferences data: ', e)
        return None
    return globals.preferences
