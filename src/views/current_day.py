from datetime import datetime

def get_current_day_calorie_data():
    import src.globals as globals
    data = None
    try:
        current_date = datetime.now().strftime('%Y-%m-%d')
        for item in globals.calorie_tracker_data:
            if item['date'] == current_date:
                data = item
                break
    except Exception as e:
        print('Error initializing current day content: ', e)
    return data

def init_current_day_content(content_obj):
    if(len(content_obj['widgets']) > 1):
        content_obj['widgets'] = content_obj['widgets'][:1]
    try:
        data = get_current_day_calorie_data()
        if data:
            content_obj['widgets'].append({
                'type': 'label',
                'text': f"Total for today: {data['calories_total']}"
            })
            for meal in data['meals']:
                content_obj['widgets'].append({
                    'type': 'label',
                    'text': f"{meal.capitalize()}: {data['meals'][meal]['calories']}"
                })
        else:
            content_obj['widgets'].append({
                'type': 'label',
                'text': 'Error, no data found for today.'
            })
    except Exception as e:
        print('Error initializing current day content: ', e)

current_day_content = {
    'title': 'Today\'s Calories',
    'widgets': [
        {
            'type': 'label',
            'text': 'Today\'s Calories'
        },
        {
            'type': 'form',
            'children': []
        }
    ]
}

current_day_content['update'] = lambda: init_current_day_content(current_day_content)

init_current_day_content(current_day_content)