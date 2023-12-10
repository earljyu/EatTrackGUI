import tkinter as tk
from tkinter import ttk, simpledialog
import os
from new_or_existing_user_gui import UserNameEntryFrame
from meal_input_gui import MealInputFrame
from create_files_gui import CreateFiles

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style_application()
        self.create_files_instance = CreateFiles()
        self.show_user_selection()

    def style_application(self):
        self.title("EatTrack Meal Tracker")
        self.geometry("400x300")
        # Set a theme
        style = ttk.Style(self)
        style.theme_use('clam')  # 'clam' is a theme that supports more customization

        # Custom colors
        background_color = '#f5f5dc'  # Sets the color to cream
        button_color = '#dcdcdc'
        entry_color = '#ffffff'

        # Configure styles
        style.configure('TButton', background=button_color, borderwidth=0)
        style.configure('TLabel', background=background_color)
        style.configure('TEntry', background=entry_color)

        # Set the background color of the root window
        self.configure(background=background_color)

    def show_user_selection(self):
        existing_users = self.create_files_instance.get_existing_users()
        self.user_selection_frame = ttk.Frame(self)
        self.user_selection_frame.pack(padx=10, pady=10, fill='both', expand=True)

        ttk.Label(self.user_selection_frame, text="Select a user or enter a new name:").pack()

        # List existing users as selectable buttons
        for user in existing_users:
            user_button = ttk.Button(self.user_selection_frame, text=user, 
                                     command=lambda u=user: self.user_login(u))
            user_button.pack(fill='x', padx=5, pady=5)

        # New user entry
        new_user_label = ttk.Label(self.user_selection_frame, text="New user name:")
        new_user_label.pack(pady=(10, 0))
        self.new_user_entry = ttk.Entry(self.user_selection_frame)
        self.new_user_entry.pack(pady=(0, 10))
        new_user_button = ttk.Button(self.user_selection_frame, text="Add New User",
                                     command=self.add_new_user)
        new_user_button.pack()

    def add_quit_button(self):
        quit_button = ttk.Button(self, text="Quit", command=self.quit_application)
        quit_button.pack(pady=(10, 0))

    def quit_application(self):
        self.destroy()  # This will close the application window and terminate the program


    def add_new_user(self):
        new_user_name = self.new_user_entry.get().strip().capitalize()
        if new_user_name:
            self.user_login(new_user_name)
        else:
            # Display an error message
            pass

    def user_login(self, user_name):
        self.create_files_instance.create_new_files(user_name)
        self.create_files_instance.create_account(user_name)
        self.user_selection_frame.pack_forget()
        self.meal_input_frame = MealInputFrame(self, user_name, self.show_user_selection)
        self.meal_input_frame.pack()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()