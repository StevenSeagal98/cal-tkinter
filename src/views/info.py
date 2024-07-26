
#simple text box component for "info" view

body_text = """
How to edit and save calories

1. Select your date from the "Home" window with either the calendar widget or clicking "View" on the calorie tracker cards

2. Edit the calories for each meal

3. Click "Save Calories" to save your changes

4. You will be redirected to the "Home" window if your changes were successful


How to view your daily calories

Option 1. Click "Today's Calories" in the navigation bar

Option 2. Select your date from the "Home" window with either the calendar widget or clicking "View" on the calorie tracker cards


How to view and edit your preferences

1. Click "Preferences" in the navigation bar

2. Edit your preferences

    a. Name: Accepts alpha characters only (a-z, A-Z)

    b. Daily Calorie Goal: Accepts numeric characters only (0-9)

3. Click "Save Preferences" to save your changes

4. You will be redirected to the "Home" window if your changes were successful


Where to find the source code

The source code is publicly available on Github at https://github.com/StevenSeagal98/cal-tkinter


Is my data safe?

Your data is only stored on your local machine utilizing the JSON file format. No data is stored on any external servers or databases and is totally private for each user.


What operating systems does this app run on?

CalorieTracker is built with Python and Tkinter, which means it can run on any operating system that supports Python and Tkinter. This includes Windows, MacOS, and Linux. The executable file is only available for Windows at this time, but you can run the app on any operating system by running the Python script.
"""

#init content/widgets for info view
info_content = {
    'title': 'Info',
    'widgets': [
        {'type': 'label', 'text': 'Info'},
        {'type': 'scrolledtext', 'text': body_text}
    ]
}