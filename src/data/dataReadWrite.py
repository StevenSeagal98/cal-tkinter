import os
import json
import datetime
import src.globals as globals

file_paths = {
    'preferences': 'calorieTrackerPreferences.json',
    'calorie_tracker_data': 'calorieTrackerData.json'
}

json_indent = 4

def check_file_exists(path):
    return os.path.exists(path)

def get_base_file_path():
    if os.name == 'nt':
        return os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
    else:
        return os.path.join(os.environ.get('HOME', ''), 'Desktop')

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def init_storage():
    base_file_path = get_base_file_path()
    ensure_directory_exists(base_file_path)  # Ensure the base directory exists
    
    globals.preferences_file_path = os.path.join(base_file_path, file_paths['preferences'])
    globals.calorie_tracker_data_file_path = os.path.join(base_file_path, file_paths['calorie_tracker_data'])

    init_preferences_file()
    init_calorie_tracker_data_file()
    
    globals.preferences = read_preferences_file()
    globals.calorie_tracker_data = read_calorie_tracker_data_file()
    set_current_date()

def init_preferences_file():
    if not check_file_exists(globals.preferences_file_path):
        # Set structure of preferences file
        base_preferences = {
            'name': 'Jane Doe',
            'daily_calorie_goal': 2000
        }
        with open(globals.preferences_file_path, 'w') as preferences_file:
            json.dump(base_preferences, preferences_file, indent=json_indent)

def init_calorie_tracker_data_file():
    daily_calories_struct = {
        'date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'calories_total': 0,
        'meals': {
            'breakfast': {'calories': 0},
            'lunch': {'calories': 0},
            'dinner': {'calories': 0},
            'snacks': {'calories': 0}
        }
    }
    if not check_file_exists(globals.calorie_tracker_data_file_path):
        base_calorie_tracker_data = [daily_calories_struct]
        with open(globals.calorie_tracker_data_file_path, 'w') as calorie_tracker_data_file:
            json.dump(base_calorie_tracker_data, calorie_tracker_data_file, indent=json_indent)
    else:
        # add empty obj for current day's data
        with open(globals.calorie_tracker_data_file_path, 'r') as calorie_tracker_data_file:
            calorie_tracker_data = json.load(calorie_tracker_data_file)
            if calorie_tracker_data[-1]['date'] != datetime.datetime.now().strftime('%Y-%m-%d'):
                calorie_tracker_data.append(daily_calories_struct)
                with open(globals.calorie_tracker_data_file_path, 'w') as calorie_tracker_data_file:
                    json.dump(calorie_tracker_data, calorie_tracker_data_file, indent=json_indent)

def read_preferences_file():
    with open(globals.preferences_file_path, 'r') as preferences_file:
        return json.load(preferences_file)

def read_calorie_tracker_data_file():
    with open(globals.calorie_tracker_data_file_path, 'r') as calorie_tracker_data_file:
        return json.load(calorie_tracker_data_file)
    
def write_to_preferences(data):
    with open(globals.preferences_file_path, 'w') as preferences_file:
        json.dump(data, preferences_file, indent = json_indent)

def write_to_calorie_tracker_data(data):
    updated = False
    if not data.get('date'):
        return updated

    with open(globals.calorie_tracker_data_file_path, 'r') as calorie_tracker_data_file:
        existing_data = json.load(calorie_tracker_data_file)

    for i, day in enumerate(existing_data):
        if day['date'] == data['date']:
            existing_data[i] = data
            updated = True
            break

    if not updated:
        return False

    with open(globals.calorie_tracker_data_file_path, 'w') as calorie_tracker_data_file:
        json.dump(existing_data, calorie_tracker_data_file, indent = json_indent)

    globals.calorie_tracker_data = existing_data
    
    return updated

def set_current_date():
    globals.selected_date = datetime.datetime.now().strftime('%Y-%m-%d')

init_storage()
