import os

class CreateFiles:
    def create_new_files(self, user_name):
        file_name = f"{user_name}_meals.txt"
        if not os.path.exists(file_name):
            open(file_name, 'w').close()

    def create_account(self, user_name):
        account_file = "accounts.txt"
        with open(account_file, "a+") as file:
            file.seek(0)
            if user_name not in file.read():
                file.write(f"{user_name}\n")

    def get_existing_users(self):
        return [file.replace('_meals.txt', '') for file in os.listdir('.') if file.endswith('_meals.txt')]
