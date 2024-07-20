class SingleDayData:
    def __init__(self):
        self.content = {}
        self.data = None

    def get_single_day_data(self, data):
        try:
            selected_date = data.selected_date
            for day in data.calorie_tracker_data:
                print('Comparing: ', day['date'], selected_date)
                if day['date'] == selected_date:
                    print('Found day: ', day)
                    return day
        except Exception as e:
            print('Error getting single day data: ', e)
            return None
        return data.calorie_tracker_data[0]

    def set_content(self):
        import src.globals as globals
        day_calorie_data = self.get_single_day_data(globals)
        self.content = {
            'title': 'Edit Calories',
            'widgets': [
                {'type': 'label', 'text': f"Edit Calories For {globals.selected_date}"},
                {'type': 'label', 'text': f"Total Calories: {day_calorie_data['calories_total']}"},
                {'type': 'entry', 'text': 'Breakfast', 'starting': day_calorie_data['meals']['breakfast']['calories']},
                {'type': 'entry', 'text': 'Lunch', 'starting': day_calorie_data['meals']['lunch']['calories']},
                {'type': 'entry', 'text': 'Dinner', 'starting': day_calorie_data['meals']['dinner']['calories']},
                {'type': 'entry', 'text': 'Snacks', 'starting': day_calorie_data['meals']['snacks']['calories']},
                {'type': 'button', 'text': 'Save Calories', 'command': lambda: self.save_calories(globals.editing_data)}
            ],
            'update': self.update
        }
        
    def update(self):
        import src.globals as globals
        self.data = self.get_single_day_data(globals)
        self.set_content()


    def save_calories(self, data):
        import src.globals as globals
        from src.data.dataReadWrite import write_to_calorie_tracker_data

        passed_check = True
        passed_check_dict = {
            'title': 'Success',
            'message': 'Data saved successfully!',
            'color': 'green',
            'success': True
        }
        failed_check_dict = {
            'title': 'Error',
            'message': 'Data did not pass validation',
            'color': 'red',
            'success': False
        }
        for key, value in data.items():
            print(f'Key: {key}, Value: {value}')
            if not value.isdigit():
                passed_check = False
        
        if passed_check:
            print('Data passed validation')
            # Format and save to file
            print('Data saved successfully: ', data)
            total_cals = 0
            day_calorie_data = self.get_single_day_data(globals)
            for key, value in data.items():
                total_cals += int(value)
                day_calorie_data['meals'][key]['calories'] = value
            day_calorie_data['calories_total'] = total_cals
            print('Day Calorie Data: ', day_calorie_data)
            write_to_calorie_tracker_data(day_calorie_data)
            return passed_check_dict
        else:
            print('Data did not pass validation')
            return failed_check_dict

single_day_data = SingleDayData()
single_day_data.update()

def update_single_day_data():
    import src.globals as globals
    try:
        selected_date = globals.selected_date
        print('Updating single day data for: ')
        print('Globals.selected_date in single_day: ', selected_date)
    except Exception as e:
        print('Error getting single day data: ', e)
        return None
    return globals.selected_date