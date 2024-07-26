from datetime import datetime

# Holds relevant data to power the home view, derived from globals
class HomeData:
    def __init__(self):
        self.content = {}
        self.data = None
    #create cards for the last six days on home page
    def create_cards(self):
        import src.globals as globals
        tracker_data = globals.calorie_tracker_data
        last_six_days = sorted(tracker_data[-6:], key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse = True)
        calorie_tracker_cards = []
        for day in last_six_days:
            date = day['date']
            total_calories = day['calories_total']
            calorie_tracker_cards.append({
                'type': 'calorie_tracker_card',
                'date': date,
                'children': [
                    {'type': 'label', 'text': date},
                    {'type': 'label', 'text': f"Total Calories: {total_calories}"}
                ]
            })
        return calorie_tracker_cards
    # used to set content on init and in updates after switching views
    def set_content(self):
        import src.globals as globals
        calorie_tracker_data = globals.calorie_tracker_data
        home_content = {
            'title': 'Home',
            'widgets': [
                {'type': 'label', 'text': 'Welcome to CalorieTracker'},
                {'type': 'calendar'}
            ],
            'update': self.update
        }
        name = globals.preferences['name']
        home_content['widgets'][0]['text'] = f"Welcome to CalorieTracker, {name}"

        # only append cards to view if data is available
        if(len(calorie_tracker_data) > 0):
            cards = self.create_cards()
            if len(cards) > 0:
                home_content['widgets'] += cards
        self.content = home_content

    def update(self):
        self.set_content()

# instantiate HomeData and set content
home_data = HomeData()
home_data.set_content()
