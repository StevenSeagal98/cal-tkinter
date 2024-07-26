import os
import json
import datetime
import src.globals as globals

# the file paths for the preferences and calorie tracker data JSON files, crucial for data storage and app functionality
file_paths = {
    'preferences': 'calorieTrackerPreferences.json',
    'calorie_tracker_data': 'calorieTrackerData.json'
}
# the indentation for JSON files, for readability
json_indent = 4
# check if a file exists at a given path, used for preferences and calorie tracker data files
def check_file_exists(path):
    return os.path.exists(path)

# get the base file path, distinguishes between Windows and Apple/Linux
def get_base_file_path():
    if os.name == 'nt':
        return os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
    else:
        return os.path.join(os.environ.get('HOME', ''), 'Desktop')
# ensure a directory exists at a given path, used for preferences and calorie tracker data files
def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def init_storage():
    # initialize storage for the app at runtime. Create necessary files if they don't exist and populate them with necessary data
    # new object is created for each accessed date. Fill in gaps between last accessed and current run
    base_file_path = get_base_file_path()
    ensure_directory_exists(base_file_path)
    
    globals.preferences_file_path = os.path.join(base_file_path, file_paths['preferences'])
    globals.calorie_tracker_data_file_path = os.path.join(base_file_path, file_paths['calorie_tracker_data'])

    init_preferences_file()
    init_calorie_tracker_data_file()
    
    globals.preferences = read_preferences_file()
    globals.calorie_tracker_data = read_calorie_tracker_data_file()
    fill_missing_days()
    set_current_date()

def init_preferences_file():
    # initialize the preferences file and populate with placeholder data
    if not check_file_exists(globals.preferences_file_path):
        base_preferences = {
            'name': 'Jane Doe',
            'daily_calorie_goal': 2000
        }
        with open(globals.preferences_file_path, 'w') as preferences_file:
            json.dump(base_preferences, preferences_file, indent=json_indent)

def init_calorie_tracker_data_file():
    # initialize the calorie tracker data file and populate with placeholder data
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
    #create file if doesn't exist
    if not check_file_exists(globals.calorie_tracker_data_file_path):
        base_calorie_tracker_data = [daily_calories_struct]
        with open(globals.calorie_tracker_data_file_path, 'w') as calorie_tracker_data_file:
            json.dump(base_calorie_tracker_data, calorie_tracker_data_file, indent=json_indent)
    else:
        with open(globals.calorie_tracker_data_file_path, 'r') as calorie_tracker_data_file:
            calorie_tracker_data = json.load(calorie_tracker_data_file)
            if calorie_tracker_data[-1]['date'] != datetime.datetime.now().strftime('%Y-%m-%d'):
                calorie_tracker_data.append(daily_calories_struct)
                with open(globals.calorie_tracker_data_file_path, 'w') as calorie_tracker_data_file:
                    json.dump(calorie_tracker_data, calorie_tracker_data_file, indent=json_indent)

def read_preferences_file():
    # read the preferences file and return the data
    with open(globals.preferences_file_path, 'r') as preferences_file:
        return json.load(preferences_file)

def read_calorie_tracker_data_file():
    # read the calorie tracker data file and return the data
    with open(globals.calorie_tracker_data_file_path, 'r') as calorie_tracker_data_file:
        return json.load(calorie_tracker_data_file)
    
def write_to_preferences(data):
    # write data to the preferences file
    with open(globals.preferences_file_path, 'w') as preferences_file:
        json.dump(data, preferences_file, indent=json_indent)

def write_to_calorie_tracker_data(data):
    # write data to the calorie tracker data file
    updated = False
    if not data.get('date'):
        return updated

    with open(globals.calorie_tracker_data_file_path, 'r') as calorie_tracker_data_file:
        existing_data = json.load(calorie_tracker_data_file)
    # update existing data with new data in json file
    for i, day in enumerate(existing_data):
        if day['date'] == data['date']:
            existing_data[i] = data
            updated = True
            break

    if not updated:
        return False
    # write updated data to json file
    with open(globals.calorie_tracker_data_file_path, 'w') as calorie_tracker_data_file:
        json.dump(existing_data, calorie_tracker_data_file, indent=json_indent)
    # update global data to use in app after completion
    globals.calorie_tracker_data = existing_data
    return updated

def set_current_date():
    # initialize the selected date to the current date, used in views/single_day.py
    globals.selected_date = datetime.datetime.now().strftime('%Y-%m-%d')

def fill_missing_days():
    # fill in missing days between the last accessed date and the current date
    calorie_tracker_data = globals.calorie_tracker_data
    if not calorie_tracker_data:
        return
    
    start_date = datetime.datetime.strptime(calorie_tracker_data[0]['date'], '%Y-%m-%d')
    end_date = datetime.datetime.now()
    date_range = (end_date - start_date).days

    existing_dates = {day['date'] for day in calorie_tracker_data}
    for i in range(date_range + 1):
        date = (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        if date not in existing_dates:
            daily_calories_struct = {
                'date': date,
                'calories_total': 0,
                'meals': {
                    'breakfast': {'calories': 0},
                    'lunch': {'calories': 0},
                    'dinner': {'calories': 0},
                    'snacks': {'calories': 0}
                }
            }
            calorie_tracker_data.append(daily_calories_struct)
    
    calorie_tracker_data.sort(key=lambda x: x['date'])
    # update global data to use in app after completion
    globals.calorie_tracker_data = calorie_tracker_data
    
    with open(globals.calorie_tracker_data_file_path, 'w') as calorie_tracker_data_file:
        json.dump(calorie_tracker_data, calorie_tracker_data_file, indent=json_indent)

init_storage()
