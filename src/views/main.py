def get_windows():
    from .home import home_content
    from .info import info_content
    from .preferences import preferences_data
    from .single_day import single_day_data
    return {
        'main': home_content,
        'preferences': preferences_data.content,
        'info': info_content,
        'single_day': single_day_data.content
    }