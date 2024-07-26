#create all dicts for windows, call function in app.py to get all windows
#refreshed with each window change to ensure data consistency

def get_windows():
    from .home import home_data
    from .info import info_content
    from .preferences import preferences_data
    from .single_day import single_day_data
    return {
        'main': home_data.content,
        'preferences': preferences_data.content,
        'info': info_content,
        'single_day': single_day_data.content
    }