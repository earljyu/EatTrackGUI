import tkinter as tk
from tkinter import ttk, messagebox

class UserNameEntryFrame(ttk.Frame):
    def __init__(self, master, login_callback):
        super().__init__(master, padding="10 10 10 10")
        self.login_callback = login_callback
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Enter your first name:").pack(pady=(0, 10))
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=(0, 10))
        ttk.Button(self, text="Submit", command=self.submit_name).pack()

    def submit_name(self):
        user_name = self.name_entry.get().strip().capitalize()
        if user_name:
            self.login_callback(user_name)
        else:
            messagebox.showerror("Error", "Please enter a valid name.")
