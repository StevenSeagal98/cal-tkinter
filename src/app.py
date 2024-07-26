from tkinter import *
from tkinter import scrolledtext
from tkcalendar import Calendar
from .data.dataReadWrite import *
from datetime import datetime
import customtkinter
import src.globals as globals
import os
from PIL import Image

# Main function to run the app
def main():
    customtkinter.set_appearance_mode('System')
    customtkinter.set_default_color_theme('blue')
    # set initial window to main
    current_window = 'main'
    # create the root for the app, all widgets append to this ultimately
    root = Tk()
    root.geometry('800x600')
    icon_dir = os.path.dirname(__file__)  # Get the directory of the current script
    icon_path = os.path.join(icon_dir, 'assets', 'ct-icon.ico')
    root.iconbitmap(icon_path)

    # create a container to hold the navbar and main content
    container = customtkinter.CTkFrame(root)
    container.pack(fill = 'both', expand = True)

    # create side navbar
    navbar = customtkinter.CTkFrame(container, width = 250)
    navbar.pack(side = 'left', fill = 'y')

    main_content = customtkinter.CTkFrame(container)
    main_content.pack(side = 'right', fill = 'both', expand = True)

    # # Load the logo image
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script
    logo_path = os.path.join(script_dir, 'assets', 'cal_tracker_logo.png')

    nav_logo = customtkinter.CTkImage(dark_image = Image.open(logo_path), light_image = Image.open(logo_path), size = (150, 150))
    nav_logo_label = customtkinter.CTkLabel(navbar, text = '', image = nav_logo)
    nav_logo_label.pack(pady = 10, padx = 10)

    def show_toast(title, message, color):
        toast = Toplevel()
        toast.title(title)
        
        toast.geometry('250x100+1000+500')
        toast.overrideredirect(True)
        
        label = customtkinter.CTkLabel(toast, text = message, padx = 20, pady = 10, bg = color)
        label.pack()

        def close_toast():
            toast.destroy()

        toast.after(2000, close_toast)

    def clear_window():
        for widget in main_content.winfo_children():
            widget.destroy()

    def set_preferences():
        from .views.main import get_windows
        windows = get_windows()
        windows['preferences']['update']()
        set_current_window('preferences')

    def set_single_day(date_str = None, needs_formatting = False):
        from .views.main import get_windows
        windows = get_windows()
        if date_str is None:
            length = len(globals.calorie_tracker_data)
            globals.selected_date = globals.calorie_tracker_data[length - 1]['date']
            print('Setting single day to today')
        else:
            print('Setting single day to: ', date_str)
            try:
                d = date_str
                if needs_formatting:
                    converted_date_obj = datetime.strptime(date_str, '%m/%d/%y') if needs_formatting else datetime.strptime(date_str, '%Y-%m-%d')
                    d = converted_date_obj.strftime('%Y-%m-%d')
                globals.selected_date = d
            except Exception as e:
                print('Error setting single day: ', e)
                return
        windows['single_day']['update']()
        set_current_window('single_day')

    def render_widgets(window):
        from .views.main import get_windows
        windows = get_windows()
        root.title('Calorie Counter App | ' + windows[window]['title'])
        clear_window()
        if windows[window].get('update') is not None:
            windows[window]['update']()
        print('Window: ', windows[window])

        card_frame = customtkinter.CTkFrame(main_content)
        card_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        calendar_frame = customtkinter.CTkFrame(main_content)
        calendar_frame.pack(side='right', fill='y', expand=False, padx=10, pady=10)

        widget_frame = customtkinter.CTkFrame(card_frame)
        widget_frame.pack(fill='both', expand = True)

        # Render the widgets for the window
        # fun little view structure, allows for dynamic view creation. Widgets specified in the ./views files are brought to life here.
        # loop through widgets for view, mount them to the frame and apply any necessary logic

        for widget in windows[window]['widgets']:
            if widget['type'] == 'label':
                customtkinter.CTkLabel(widget_frame, text = widget['text']).pack(pady = 5)
            elif widget['type'] == 'button':
                # Handle the submit button in different views
                def handle_submit_success(cm):
                    from .data.dataReadWrite import init_storage
                    cm_data = cm()
                    if(cm_data == None):
                        print('Setting success to true')
                        cm_data = { 'success' : True }
                    
                    print('Data submitted successfully: ', cm_data)
                    # if the button click came from a "form" view, check for a success key
                    if len(cm_data.keys()) > 1:
                        print('Got it')
                        if not cm_data['title']:
                            return
                        init_storage()
                        set_current_window('main')
                        #show_toast(cm_data['title'], cm_data['message'], cm_data['color'])
                # Create the button and bind the command to the handle_submit_success function
                customtkinter.CTkButton(widget_frame, text = widget['text'], command = lambda cm = widget['command']: handle_submit_success(cm)).pack(pady = 5)
            elif widget['type'] == 'entry':
                # Create an entry widget and bind the KeyRelease event to update the editing data
                customtkinter.CTkLabel(widget_frame, text = widget['text']).pack(pady = 5)
                entry = customtkinter.CTkEntry(widget_frame)
                starting = StringVar(root, value = widget['starting'])
                entry.insert(END, starting.get())
                entry.pack(pady = 5)
                print('widget: ', widget)
                if not hasattr(globals, 'editing_data'):
                    globals.editing_data = {}
                key = widget['text'].lower()
                if key not in globals.editing_data:
                    globals.editing_data[key] = starting.get()

                def update_editing_data(event, key=key, entry=entry):
                    # Update the editing data with the current value of the entry
                    current_value = entry.get()
                    globals.editing_data[key] = current_value
                
                # Bind the KeyRelease event to the update function
                entry.bind('<KeyRelease>', lambda event, key = key, entry = entry: update_editing_data(event, key, entry))
            
            #for scrolled text widget on info view
            elif widget['type'] == 'scrolledtext':
                scroll_text = scrolledtext.ScrolledText(widget_frame, wrap = WORD, width = 50, height = 15)
                scroll_text.pack(padx = 10, pady = 10)
                scroll_text.tag_config('header')
                lines = widget['text'].strip().split('\n')
                for line in lines:
                    #insert each line of text after a new line, check views/info.py for the text
                    scroll_text.insert(INSERT, line + '\n')
                # disable the widget so it can't be edited
                scroll_text.config(state = DISABLED)
            elif widget['type'] == 'calorie_tracker_card':
                # Create a card for the calorie tracker data, one of these are applied for each day in the last six days if available
                card = customtkinter.CTkFrame(widget_frame)
                card.pack(fill = 'x', padx = 10, pady = 10)
                # Loop through the children of the card and create a label for each
                for child in widget['children']:
                    customtkinter.CTkLabel(card, text=child['text']).pack(side = 'left', fill = 'x', padx = 10, pady = 10)
                # Create a button to view the day in more detail
                customtkinter.CTkButton(card, text = 'View', command = lambda d = widget['date']: set_single_day(d)).pack(side='right')
            elif widget['type'] == 'calendar':
                # Create a calendar widget to select a day
                now = datetime.now()
                cal = Calendar(calendar_frame, selectmode = 'day', year = now.year, month = now.month, day = now.day)
                cal.pack(pady = 10)
                # Create a button to select the day, fire set_single_day function on click
                customtkinter.CTkButton(calendar_frame, text='Select', command = lambda: set_single_day(cal.get_date(), True)).pack(pady=10)
    # Set the current window to the specified window
    def set_current_window(window):
        current_window = window
        render_widgets(current_window)

    def create_navbar_buttons():
        # Create the buttons for the navbar dynamically
        nav_buttons = [
            {'text': 'Home', 'command': lambda: set_current_window('main')},
            {'text': 'Today\'s Calories', 'command': lambda: set_single_day()},
            {'text': 'Preferences', 'command': lambda: set_preferences()},
            {'text': 'Info', 'command': lambda: set_current_window('info')}
        ]
        
        for btn in nav_buttons:
            customtkinter.CTkButton(navbar, text = btn['text'], command = btn['command']).pack(fill = 'x', padx = 10, pady = 10)
        
    create_navbar_buttons()

    # Set the initial window to main
    set_current_window(current_window)
    # Run the main loop
    root.mainloop()
