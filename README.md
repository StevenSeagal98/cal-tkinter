# Calorie Tracker

## Starting The Application

### Option 1: Download Executable (Windows Only)
This is the simplest way to get Calorie Tracker up and running, but there are some issues involved with the download due to our build process and it is currently only available for Windows machines.
1) Visit [our website](https://stevenseagal98.github.io/calorie-tracker-site/) and click 'Download'
2) Find and click on your newly downloaded CalorieTracker.exe file to get started

*You will most likely encounter security alerts from Windows during this process, you can safely disregard this behavior as executables built with our bundler (PyInstaller) are often flagged as potential Trojans.*

### Option 2: Build Locally (Recommended)
This method is a little more involved, but negates the security warning issues involved with the executable.
1) Clone this repository
2) Find your newly cloned directory on your machine and cd in
3) Install dependencies
4) Run with `python run.py`

## User Walkthrough
There are four windows available in Calorie Tracker which you're able to traverse with our navigation bar to the left of the main content, available on all views:
- Home
    - This is the entry point of the application.

    - View the calorie counts for the last 6 days
        - Click one to view/edit

    - Use the calendar widget to select a day to view/edit
        - Click your desired date and then click the *Select* button below the calendar

- Single Day View / Edit
    - This view populates your selected date's data
    - Available via side navigation bar (current day), cards on home page, or calendar widget
    - Your previously saved input will populate the entry boxes, change these and click *Save* to save your changes. The app will automatically pull your new data and refresh the widgets

- Preferences
    - This is where you can store your name and calorie goal
    - Similar to the Single Day View functionality, this entry boxes will populate with your previously saved data. Change them and click *Save* to change your preferences

- Info
    - This is a scrollable view which contains all the information pertinent to using the application for a user, as well as a contact email.

## For Developers

### Dependencies
- Python
- Tkinter
- customtkinter
- tkcalendar

### Directories & Files
- **src**
    - Contains all source files for the application. Bundled separately to work with build software (PyInstaller)

    - **Data**
        - Responsible for reading and writing data to locally created and hosted JSON files.
        - Responsible for loading data to be used throughout the application
        - Automatically creates files required for application functionality (preferences and calorieTrackerData)
        - OS Independent functionality

    - **Views**
        - Works with an abstraction layer on top of the standard Tkinter window functionality in order to more easily create and destroy widgets depending on application state instead.
            - Feeds into *create_widgets* function in *app.py*
        - Contains all data and view logic for each respective view

- **Globals**
    - Used to hold app state and other variables needed to run the application

- **app.py**
    - Contains our *main* module
    - Holds core view/widget mounting and refresh logic
    - Creates main window and global widgets, such as the side navigation bar