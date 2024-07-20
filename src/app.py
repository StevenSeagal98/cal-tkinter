from math import fabs
from tkinter import *
from tkinter import scrolledtext
from tkcalendar import Calendar
from .data.dataReadWrite import *
from datetime import datetime
import customtkinter
import src.globals as globals

def main():
    customtkinter.set_appearance_mode('System')
    customtkinter.set_default_color_theme('blue')

    current_window = 'main'

    root = Tk()
    root.geometry('800x600')

    container = customtkinter.CTkFrame(root)
    container.pack(fill = 'both', expand = True)

    navbar = customtkinter.CTkFrame(container, width = 250)
    navbar.pack(side = 'left', fill = 'y')

    main_content = customtkinter.CTkFrame(container)
    main_content.pack(side = 'right', fill = 'both', expand = True)

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

    def set_single_day(date_str = None):
        from .views.main import get_windows
        windows = get_windows()
        if date_str is None:
            length = len(globals.calorie_tracker_data)
            globals.selected_date = globals.calorie_tracker_data[length - 1]['date']
            print('Setting single day to today')
        else:
            print('Setting single day to: ', date_str)
            try:
                converted_date_obj = datetime.strptime(date_str, '%m/%d/%y')
                formatted_date_str = converted_date_obj.strftime('%Y-%m-%d')
                globals.selected_date = formatted_date_str
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

        card_frame = customtkinter.CTkFrame(main_content)
        card_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        calendar_frame = customtkinter.CTkFrame(main_content)
        calendar_frame.pack(side='right', fill='y', expand=False, padx=10, pady=10)

        widget_frame = customtkinter.CTkFrame(card_frame)
        widget_frame.pack(fill='both', expand=True)

        for widget in windows[window]['widgets']:
            if widget['type'] == 'label':
                customtkinter.CTkLabel(widget_frame, text=widget['text']).pack(pady=5)
            elif widget['type'] == 'button':
                def handle_submit_success(cm):
                    from .data.dataReadWrite import init_storage
                    cm_data = cm()
                    print('CM Data: ', cm_data)
                    if(cm_data == None):
                        print('Setting success to true')
                        cm_data = { 'success' : True }
                    print('Data submitted successfully: ', cm_data)
                    if len(cm_data.keys()) > 1:
                        print('Got it')
                        if not cm_data['title']:
                            return
                        init_storage()
                        set_current_window('main')
                        #show_toast(cm_data['title'], cm_data['message'], cm_data['color'])
                customtkinter.CTkButton(widget_frame, text = widget['text'], command = lambda cm = widget['command']: handle_submit_success(cm)).pack(pady = 5)
            elif widget['type'] == 'entry':
                customtkinter.CTkLabel(widget_frame, text = widget['text']).pack(pady=5)
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
                    current_value = entry.get()
                    globals.editing_data[key] = current_value
                
                # Bind the KeyRelease event to the update function
                entry.bind('<KeyRelease>', lambda event, key = key, entry = entry: update_editing_data(event, key, entry))
            elif widget['type'] == 'scrolledtext':
                scroll_text = scrolledtext.ScrolledText(widget_frame, wrap = WORD, width = 50, height = 15)
                scroll_text.pack(padx=10, pady=10)
                scroll_text.tag_config('header')
                lines = widget['text'].strip().split('\n')
                for line in lines:
                    if line.startswith('Header'):
                        scroll_text.insert(INSERT, line + '\n', 'header')
                    else:
                        scroll_text.insert(INSERT, line + '\n')
                scroll_text.config(state=DISABLED)
            elif widget['type'] == 'calorie_tracker_card':
                card = customtkinter.CTkFrame(widget_frame)
                card.pack(fill = 'x', padx = 10, pady = 10)
                for child in widget['children']:
                    customtkinter.CTkLabel(card, text=child['text']).pack(side='left', fill='x', padx=10, pady=10)
                customtkinter.CTkButton(card, text='View', command=lambda: print('Searching for: ', widget['date'])).pack(side='right')
            elif widget['type'] == 'calendar':
                now = datetime.now()
                cal = Calendar(calendar_frame, selectmode='day', year=now.year, month=now.month, day=now.day)
                cal.pack(pady=10)
                customtkinter.CTkButton(calendar_frame, text='Select', command=lambda: set_single_day(cal.get_date())).pack(pady=10)

    def set_current_window(window):
        current_window = window
        render_widgets(current_window)

    def create_navbar_buttons():
        nav_buttons = [
            {'text': 'Home', 'command': lambda: set_current_window('main')},
            {'text': 'Today\'s Calories', 'command': lambda: set_single_day()},
            {'text': 'Preferences', 'command': lambda: set_preferences()},
            {'text': 'Info', 'command': lambda: set_current_window('info')}
        ]
        
        for btn in nav_buttons:
            customtkinter.CTkButton(navbar, text = btn['text'], command = btn['command']).pack(fill = 'x', padx = 10, pady = 10)
        
    create_navbar_buttons()
    set_current_window(current_window)

    root.mainloop()
