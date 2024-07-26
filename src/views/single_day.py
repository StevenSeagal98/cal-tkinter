# This file contains the SingleDayData class which is used to display the data for a single day in the calorie tracker
class SingleDayData:
    def __init__(self):
        self.content = {}
        self.data = None

    def get_single_day_data(self, data):
        try:
            selected_date = data.selected_date
            for day in data.calorie_tracker_data:
                if day['date'] == selected_date:
                    return day
        except Exception as e:
            print('Error getting single day data: ', e)
            return None
        return data.calorie_tracker_data[0]

    def set_content(self):
        import src.globals as globals
        day_calorie_data = self.get_single_day_data(globals)
        #content for single day view, including total calories and meal calories
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
    #refreshes content of instantiated obj for view updates
    def update(self):
        import src.globals as globals
        self.data = self.get_single_day_data(globals)
        self.set_content()

    #save calories data to JSON file, used throughout the app
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
        #data validation for calories before saving
        for key, value in data.items():
            if not value.isdigit():
                passed_check = False
        
        if passed_check:
            total_cals = 0
            day_calorie_data = self.get_single_day_data(globals)
            #update calories for each meal, increment total
            for key, value in data.items():
                total_cals += int(value)
                day_calorie_data['meals'][key]['calories'] = value
            day_calorie_data['calories_total'] = total_cals
            #save to json file
            write_to_calorie_tracker_data(day_calorie_data)
            return passed_check_dict
        else:
            return failed_check_dict

#instantiate SingleDayData and set content
single_day_data = SingleDayData()
single_day_data.update()

def update_single_day_data():
    import src.globals as globals
    return globals.selected_date