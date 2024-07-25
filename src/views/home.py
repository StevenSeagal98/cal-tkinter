from datetime import datetime

home_content = {
    'title': 'Home',
    'widgets': [
        {'type': 'label', 'text': 'Welcome to CalorieTracker'},
        {'type': 'calendar'}
    ]
}

def create_cards(tracker_data):
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

def init():
    import src.globals as globals
    calorie_tracker_data = globals.calorie_tracker_data
    name = globals.preferences['name']
    home_content['widgets'][0]['text'] = f"Welcome to CalorieTracker, {name}"
    if(len(calorie_tracker_data) > 0):
        calorie_tracker_cards = create_cards(calorie_tracker_data)
        home_content['widgets'] += calorie_tracker_cards

def update():
    home_content['widgets'] = home_content['widgets'][:2]
    init()

home_content['update'] = update
