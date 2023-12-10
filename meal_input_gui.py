import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from datetime import datetime

class MealInputFrame(ttk.Frame):
    def __init__(self, master, user_name, return_callback):
        super().__init__(master, padding="10 10 10 10")
        self.user_name = user_name
        self.return_callback = return_callback
        self.create_widgets()
        self.load_meals()

    def create_widgets(self):
        ttk.Label(self, text=f"Meal Input for {self.user_name}").pack()

        # Create a StringVar for the meal type OptionMenu
        self.meal_type_var = tk.StringVar(self)
        self.meal_type_var.set("Breakfast")  # Set default value

        # Meal options
        meal_options = ["Breakfast", "Lunch", "Dinner", "Snacks"]
        
        # Create the meal type OptionMenu and pass the StringVar
        self.meal_type_option_menu = ttk.OptionMenu(self, self.meal_type_var, "Breakfast", *meal_options)
        self.meal_type_option_menu.pack()

        ttk.Label(self, text="Enter your meal:").pack()
        self.meal_entry = ttk.Entry(self)
        self.meal_entry.pack()

        ttk.Button(self, text="Submit Meal", command=self.submit_meal).pack()
        
        ttk.Button(self, text="Done", command=self.done).pack()

        self.meal_display = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD)
        self.meal_display.pack()

    def load_meals(self):
        file_name = f"{self.user_name}_meals.txt"
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                self.meal_display.insert(tk.END, file.read())
        self.meal_display.config(state=tk.DISABLED)

    def submit_meal(self):
        meal_type = self.meal_type_var.get()
        meal = self.meal_entry.get().strip()
        current_date = datetime.now().strftime("%Y-%m-%d")

        if meal:
            file_name = f"{self.user_name}_meals.txt"
            meal_entries = self.read_meal_entries(file_name)
            # Ensure the current date is initialized in the dictionary
            if current_date not in meal_entries:
                meal_entries[current_date] = {"Breakfast": [], "Lunch": [], "Dinner": [], "Snacks": []}
            # Append the meal to the appropriate list
            meal_entries[current_date][meal_type].append(meal)
            self.write_meal_entries(file_name, meal_entries)

            self.meal_display.config(state=tk.NORMAL)
            self.meal_display.delete(1.0, tk.END)  # Clear the display
            self.meal_display.insert(tk.END, self.format_meal_entries(meal_entries))  # Insert formatted entries
            self.meal_display.config(state=tk.DISABLED)
            self.meal_entry.delete(0, 'end')
            messagebox.showinfo("Success", "Meal submitted successfully!")
        else:
            messagebox.showerror("Error", "Please enter a meal.")

    def read_meal_entries(self, file_name):
        if not os.path.exists(file_name):
            return {}
        with open(file_name, "r") as file:
            lines = file.readlines()

        meal_entries = {}
        current_date = None
        current_meal_type = None
        for line in lines:
            line = line.strip()
            if line.startswith("Date:"):
                current_date = line.split(": ")[1]
                meal_entries[current_date] = {"Breakfast": [], "Lunch": [], "Dinner": [], "Snacks": []}
                current_meal_type = None
            elif any(line.startswith(meal + ":") for meal in ["Breakfast", "Lunch", "Dinner", "Snacks"]):
                current_meal_type = line.split(":")[0]
            elif current_meal_type and current_date:
                # This line is a meal entry
                meal_entries[current_date][current_meal_type].append(line)

        return meal_entries

    def write_meal_entries(self, file_name, meal_entries):
        with open(file_name, "w") as file:
            for date, meals in meal_entries.items():
                file.write(f"Date: {date}\n")
                for meal_type, meal_list in meals.items():
                    if meal_list:  # Only write the meal type if there are meals
                        file.write(f"{meal_type}: \n")
                        for meal in meal_list:
                            file.write(f"{meal}\n")

    def format_meal_entries(self, meal_entries):
        formatted_entries = ""
        for date, meals in meal_entries.items():
            formatted_entries += f"Date: {date}\n"
            for meal_type, meal_list in meals.items():
                if meal_list:  # Only include the meal type if there are meals
                    formatted_entries += f"{meal_type}: \n" + "\n".join(meal_list) + "\n\n"
        return formatted_entries.strip()  # Remove the last newline character for clean formatting

    def update_meal_content(self, file_name, current_date, meal_type, meal):
        if not os.path.exists(file_name):
            return f"Date: {current_date}\n{meal_type}: {meal}\n", False

        with open(file_name, "r") as file:
            lines = file.readlines()

        date_line = f"Date: {current_date}\n"
        meal_line = f"{meal_type}: {meal}\n"
        updated_content = ""
        date_found = False
        entry_exists = False

        for line in lines:
            if line.startswith("Date:"):
                if date_found:
                    updated_content += date_line + meal_line
                    date_line = ""
                date_found = line.strip() == date_line.strip()

            if date_found and line.startswith(meal_type + ":"):
                entry_exists = True
                continue

            updated_content += line

        if not date_found:
            updated_content += date_line + meal_line

        return updated_content, entry_exists

    def done(self):
        self.pack_forget()
        self.return_callback()
