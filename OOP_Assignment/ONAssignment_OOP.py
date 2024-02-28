import tkinter as tk
import random
import sys
import subprocess
import os

class Bank_Account_App:
    def __init__(self, accounts: dict) -> None:
        self._accounts = accounts if accounts is not None else {}

    def add_account(self, account):
        self._accounts[account.account_number] = account

    def close_account(self, account_number):
        if account_number in self._accounts:
            del self._accounts[account_number]
        else:
            print("Account number does not exist.")

    @staticmethod
    def safe_cast(value, to_type, default=None):
        try:
            return to_type(value)
        except (ValueError, TypeError):
            return default

    def generate_account_number(self, account_type: str) -> str:
        while True:
            account_number = f"{'CA' if account_type == '1' else 'SA'}{random.randint(100, 999)}"
            if account_number not in self._accounts:
                return account_number
    
    def safe_cast(value, to_type, default=None):
        try:
            return to_type(value)
        except (ValueError, TypeError) as ex:
            print(f'Error during convertation {ex}')
            return default

class CLI_UI:
    def __init__(self, bank_app: Bank_Account_App) -> None:
        self.bank_app = bank_app

    def ask_a_question(self, question: str, options: dict) -> str:
        print(question)
        for key, value in options.items():
            print(f"{key}: {value}")
        answer = input().upper()
        return options.get(answer, None)
    # def main_menu(self):
    #     print('Welcome to the Banking Application.\n')
    #     account_type = self.ask_a_question_in_numbers("Would you like to open a Current Account or Savings Account?", {"1": "Current Account", "2": "Savings Account"})
    #     if account_type:
    #         account_number = self.bank_app.generate_account_number(account_type)
    #         if account_type == '1': #
    #             account = Current_Account(account_number)
    #         else:
    #             account = Savings_Account(account_number)
    #         self.bank_app.add_account(account)
    #         print(f"Account {account_number} created successfully.")
    #     else:
    #         print("Invalid option selected.")
    def main_menu(self):
        while True:
            print("Welcome to the Banking Application.\n")
            choice = self.ask_a_question_in_numbers("Please chose an operation:", {"1": "Open Account", "2": "Perform Transactions"})
            if choice == "1":
                self.account_creation_menu()
            elif choice == "2":
                self.transaction_menu()
            elif choice == "0":
                print("Thank you for using the Banking Application.")
                break
            else:
                print("Invalid choice, please try again.")

    def account_creation_menu(self):
        while True:
            account_types={"1": "Current Account", "2": "Savings Account"}
            account_type = self.ask_a_question_in_numbers("Do you want to open a Current Account or Savings Account?", account_types)
            if account_type == "0":
                break
            first_name = input("Enter the Fisrt Name for the account: ")
            last_name = input("Enter the Last Name for the account: ")
            account_number = self.bank_app.generate_account_number(account_type)
            if account_type == "1":
                account = Current_Account(account_number, first_name, last_name)
            elif account_type == "2":
                account = Savings_Account(account_number, first_name, last_name)
            else:
                print("Invalid account type selected.")
                continue
            self.bank_app.add_account(account)
            print(f"{account_types[account_type]} created successfully with account number: {account_number}")
            

    def transaction_menu(self):
        while True:
            transactions={"1": "Deposit", "2": "Withdraw", "3": "Check Balance", "3": "Calculate Interest (Savings Only)"}
            choice = self.ask_a_question_in_numbers("Please, select one of following options:", transactions)
            if choice == "0":
                break
            account_number = input("Enter your account number: ")
            account = self.bank_app._accounts.get(account_number)
            current_balance=account.get_balance()
            if not account:
                print("Account not found.")
                continue
            if choice == "1":
                amount=self.ask_in_range("Enter the amount to deposit: ",[0.01,10000.00])
                account.deposit(amount)
                print(f"Deposited {amount}. New balance is {current_balance}.")
            elif choice == "2":
                # amount = self.ask_in_range("Enter the amount to withdraw: ",[0.01,10000.00])
                min_withdraw=5
                max_withdraw=current_balance if current_balance < 1000 else 1000
                amount = self.ask_in_range(f"Please enter the amount to withdraw (between €{min_withdraw} and €{max_withdraw}):", [min_withdraw, max_withdraw])
                account.withdraw(amount)
                print(f"Withdrew {amount}. New balance is {current_balance}.")
            elif choice == "3":
                print(f"Current balance is {current_balance}.")
            elif choice == "4" and isinstance(account, Savings_Account):
                interest = account.calculate_interest()
                print(f"Calculated interest: {interest}.")
            else:
                print("Invalid choice or operation not applicable to account type.")    
    
        
    def ask_a_question_in_numbers(self,message,possible_answers={'1': 'Yes', '2': 'No'}):
        possible_answers['0'] = 'Exit'
        options_list = [f"{key}. {value}" for key, value in possible_answers.items()]
        options_str = '\n'.join(options_list)
        full_message = f"{message} [{','.join(possible_answers.keys())}]\n{options_str}"
        possible_answers_lower = {key.lower(): value for key, value in possible_answers.items()}
        while True:
            print(full_message)
            user_input = input().lower()
            if user_input in possible_answers_lower:
                if user_input == '0':
                    print("Exiting.")
                    return '0'
                else:
                    return user_input
            else:
                print(f"Incorrect input. Please enter one of the following options: [{','.join(possible_answers.keys())}]")
    
    def ask_a_question(self,message, possible_answers={'Y': 'Yes', 'N': 'No'}):
        options_str = ', '.join([f"({key}) for {value}" for key, value in possible_answers.items()])
        full_message = f"{message} Possible answers are {options_str}."
        possible_answers_lower = {key.lower(): value for key, value in possible_answers.items()}
        while True:
            print(full_message)
            user_input = input().lower() 
            possible_answers_lower = {key.lower(): value for key, value in possible_answers.items()}
            if user_input in possible_answers_lower:
                for original_key in possible_answers:
                    if original_key.lower() == user_input:
                        return original_key.lower() #return answers in the lower case always
            else:
                print(f"Incorrect input. Please enter one of the following options: {options_str}")
    @staticmethod
    def ask_in_range(text, range_limits=[1.0, 5.0], input_type=float):
        while True:
            print(text)
            var1 = input()
            try:
                if input_type == int:
                    converted = int(var1)  # Convert to integer if input_type is int
                else:
                    converted = float(var1)  # Defaults to converting to float
                    
                if converted >= min(range_limits) and converted <= max(range_limits):
                    return converted
                else:
                    print(f"Input is out of range, please enter a number between {min(range_limits)} and {max(range_limits)}.")
            except ValueError:
                print(f"Invalid input: Please enter a valid {'integer' if input_type == int else 'number'}.")

class TK_UI(Bank_Account_App): #button to open an account and a place holder
    def __init__(self,root: tk.Tk, accounts: dict) -> tk.Tk:
        super().__init__(accounts)
        self.root = root
        self.root.title("Banking Application")
        self.root.geometry("1000x600+450+250")  # Set the window geometry
        self.first_name=''
        self.last_name=''
        self.generate_general_grid()
        self.create_status_bar()
        self.create_initial_controls()

    def generate_general_grid(self):
        # Configure the root grid to have a single column that expands
        self.root.grid_columnconfigure(0, weight=1)
        
        # Label for the title
        self.dice_label = tk.Label(self.root, text=f'Banking Application GUI', font=('Arial', 12,'bold'))
        self.dice_label.grid(row=0, columnspan=7, padx=5, pady=5, sticky='ew')  # 'ew' = east+west
        
        # Create two frames
        self.left_frame = tk.Frame(self.root)  # Left frame 
        self.right_frame = tk.Frame(self.root)  # Right frame
        
        # Place the frames in the grid
        self.left_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.right_frame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        
        # Configure the root grid to split space equally between the two frames
        self.root.grid_columnconfigure(1, weight=1)
        
        # Configure rows and columns within the frames if necessary
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)
        
        # Add titles or any other widgets to each frame
        self.left_title = tk.Label(self.left_frame, text="Current Account", font=('Arial', 12))
        self.left_title.grid(row=0, columnspan=5, sticky='new')
        
        self.right_title = tk.Label(self.right_frame, text="Savings Account", font=('Arial', 12))
        self.right_title.grid(row=0, columnspan=5, sticky='new')
        
        self.left_frame.grid_columnconfigure(0, weight=1)  # Make the first column grow, pushing content to the center
        self.left_frame.grid_columnconfigure(1, weight=0)  # Fixed size for labels
        self.left_frame.grid_columnconfigure(2, weight=0)  # Fixed size for entry fields
        self.left_frame.grid_columnconfigure(3, weight=1)  # Make the last column grow, pushing content to the center
        self.right_frame.grid_columnconfigure(0, weight=1)  # Make the first column grow, pushing content to the center
        self.right_frame.grid_columnconfigure(1, weight=0)  # Fixed size for labels
        self.right_frame.grid_columnconfigure(2, weight=0)  # Fixed size for entry fields
        self.right_frame.grid_columnconfigure(3, weight=1)  # Make the last column grow, pushing content to the center
    
    def create_status_bar(self): # 
        """Create the Status Bar and its Frame"""
        self.status_bar_frame = tk.Frame(self.root, height=25)
        self.status_bar_frame.pack_propagate(False)
        self.status_bar_frame.grid(row=3, column=0, columnspan=7, sticky='ew')
        self.root.grid_rowconfigure(3, weight=0)

        self.status_label = tk.Label(self.status_bar_frame, text='Status: Ready', anchor='w', font=('Arial', 9))
        self.status_label.pack(fill='x', side='left')

        # Exit Button in the Status Bar
        self.exit_button = tk.Button(self.status_bar_frame, text='Exit', padx=5,pady=5, command=self.close_application)
        self.exit_button.pack(side='right', padx=10)

    def close_application(self):
        """Close the application."""
        self.root.destroy()

    def update_status(self, message:str, color:str='black'):
        """Update the status bar message."""
        self.status_label.config(text='Status: '+message, fg=color)

    def create_initial_controls(self): #c_ for current, s_ for savings        
        ## Current Account Field
        frame_var=self.left_frame
        self.left_frame_bg = self.left_frame.cget('bg')
        # First Name Label and Entry
        self.c_first_name_label = tk.Label(frame_var, text="First Name:", font=('Arial', 12))
        self.c_first_name_label.grid(row=1, column=1, sticky='ew')
        self.c_first_name_entry = tk.Entry(frame_var, font=('Arial', 12, 'normal'))
        self.c_first_name_entry.grid(row=1, column=2, padx=5, pady=5, sticky='ew')
        self.c_first_name_error_label = tk.Label(frame_var, text="Please enter first name",fg=self.left_frame_bg, bg=self.left_frame_bg)
        self.c_first_name_error_label.grid(row=2, column=1, sticky='ew', padx=5, pady=0, columnspan=2)
        # Last Name Label and Entry
        self.c_last_name_label = tk.Label(frame_var, text="Last Name:", font=('Arial', 12))
        self.c_last_name_label.grid(row=3, column=1, sticky='ew')
        self.c_last_name_entry = tk.Entry(frame_var, font=('Arial', 12, 'normal'))
        self.c_last_name_entry.grid(row=3, column=2, padx=5, pady=5, sticky='ew')
        self.c_last_name_error_label = tk.Label(frame_var, text="Please enter last name",fg=self.left_frame_bg, bg=self.left_frame_bg)
        self.c_last_name_error_label.grid(row=4, column=1, sticky='ew', padx=5, pady=0, columnspan=2)
        # Confirmation Button
        self.c_create_account_button = tk.Button(frame_var, text="Open Current Account", command=self.creating_current_account, font=('Arial', 12))
        self.c_create_account_button.grid(row=5, column=1, padx=5, pady=5, sticky='ew', columnspan=2)
        
        ## Savings Account Field
        frame_var=self.right_frame
        self.righ_frame_bg = self.right_frame.cget('bg')
        # First Name Label and Entry
        self.s_first_name_label = tk.Label(frame_var, text="First Name:", font=('Arial', 12))
        self.s_first_name_label.grid(row=1, column=1, sticky='ew')
        self.s_first_name_entry = tk.Entry(frame_var, font=('Arial', 12, 'normal'))
        self.s_first_name_entry.grid(row=1, column=2, padx=5, pady=5, sticky='ew')
        self.s_first_name_error_label = tk.Label(frame_var, text="Please enter first name",fg=self.righ_frame_bg, bg=self.righ_frame_bg)
        self.s_first_name_error_label.grid(row=2, column=1, sticky='ew', padx=5, pady=0, columnspan=2)
        # Last Name Label and Entry
        self.s_last_name_label = tk.Label(frame_var, text="Last Name:", font=('Arial', 12))
        self.s_last_name_label.grid(row=3, column=1, sticky='ew')
        self.s_last_name_entry = tk.Entry(frame_var, font=('Arial', 12, 'normal'))
        self.s_last_name_entry.grid(row=3, column=2, padx=5, pady=5, sticky='ew')
        self.s_last_name_error_label = tk.Label(frame_var, text="Please enter last name",fg=self.righ_frame_bg, bg=self.righ_frame_bg)
        self.s_last_name_error_label.grid(row=4, column=1, sticky='ew', padx=5, pady=0, columnspan=2)
        # Confirmation Button
        self.s_create_account_button = tk.Button(frame_var, text="Open Savings Account", command=self.creating_savings_account, font=('Arial', 12))
        self.s_create_account_button.grid(row=5, column=1, padx=5, pady=5, sticky='ew', columnspan=2)
    
    def destroy_initial_controls(self,is_ca:bool=True):
        try:
            self.s_first_name_label.destroy()
            self.s_first_name_entry.destroy()
            self.s_first_name_error_label.destroy()
            self.s_last_name_label.destroy()
            self.s_last_name_entry.destroy()
            self.s_last_name_error_label.destroy()
            self.c_first_name_label.destroy()
            self.c_first_name_entry.destroy()
            self.c_first_name_error_label.destroy()
            self.c_last_name_label.destroy()
            self.c_last_name_entry.destroy()
            self.c_last_name_error_label.destroy()
            if is_ca:
                self.c_create_account_button.destroy()
            else:
                self.s_create_account_button.destroy()
        except:
            pass
    
    def creating_current_account(self):
        # Accounts.first_name
        if self.first_name=='' or self.last_name=='':
            self.first_name=self.c_first_name_entry.get()
            self.last_name=self.c_last_name_entry.get()
        if self.first_name!='' and self.last_name!='':
            self.update_status(f"Current Account for '{self.first_name} {self.last_name}' has been created")
            self.left_title.config(text=f'Current Account for {self.first_name} {self.last_name}')
            print(f'Debug: {self.first_name} {self.last_name}')
            self.destroy_initial_controls()
            return

        self.first_name=self.c_first_name_entry.get()
        self.last_name=self.c_last_name_entry.get()

        if self.first_name=="":
            self.c_first_name_error_label.config(fg='red')
            self.update_status("We couldn't register Current Account for you, please enter the First and Last names correctly",'red')
        else:
            self.c_first_name_error_label.config(fg=self.left_frame_bg)
        
        if self.last_name=="":
            self.update_status("We couldn't register Current Account for you, please enter the First and Last names correctly",'red')
            self.c_last_name_error_label.config(fg='red')
        else:
            self.c_last_name_error_label.config(fg=self.left_frame_bg)
        

    def creating_savings_account(self):
        # Accounts.first_name
        if self.first_name=='' or self.last_name=='':
            self.first_name=self.s_first_name_entry.get()
            self.last_name=self.s_last_name_entry.get()
        if self.first_name!='' and self.last_name!='':
            self.update_status(f"Savings Account for '{self.first_name} {self.last_name}' has been created")
            self.right_title.config(text=f"Savings Account for {self.first_name} {self.last_name}")
            print(f'Debug: {self.first_name} {self.last_name}')
            self.destroy_initial_controls(False)
            return
        
        if self.first_name=="":
            self.s_first_name_error_label.config(fg='red')
            self.update_status("We couldn't register Savings Account for you, please enter the First and Last names correctly",'red')
        else:
            self.s_first_name_error_label.config(fg=self.left_frame_bg)
        
        if self.last_name=="":
            self.update_status("We couldn't register Savings Account for you, please enter the First and Last names correctly",'red')
            self.s_last_name_error_label.config(fg='red')
        else:
            self.s_last_name_error_label.config(fg=self.left_frame_bg)

    

    
    def create_current_account_controls():
        
        #generate new one
        pass
    
    def create_savings_account_controls():
        
        #generate new one
        pass
     
    def update_balance_ui(self,account_id,value):
        pass
    
    def update_deposit_ui(self,account_id,value):
        pass
    
    def update_withdraw_ui(self,account_id,value):
        pass
    
    def get_deposit_input_box(self) -> float:
        return 'float value of the deposit'
    
    def get_withdraw_input_box(self) -> float:
        return 'float value of the widthraw'

class Accounts:
    def __init__(self, account_number: str, first_name: str, last_name: str) -> None:
        self.account_number = account_number
        self.first_name = first_name
        self.last_name = last_name
        self._balance = 0.00
    
    def deposit(self, amount: float):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount: float):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            return True
        return False

    def get_balance(self) -> float:
        return self._balance

class Current_Account(Accounts):
    transaction_fee = 1.50

    def __init__(self, account_number: str, first_name: str = "", last_name: str = "") -> None:
        super().__init__(account_number, first_name, last_name)

    def withdraw(self, amount: float):
        if super().withdraw(amount + Current_Account.transaction_fee):
            print(f"Withdrawal successful. Transaction fee of €{Current_Account.transaction_fee} applied.")
            return True
        return False

class Savings_Account(Accounts):
    interest_rate = 0.025

    def __init__(self, account_number: str, first_name: str = "", last_name: str = "") -> None:
        super().__init__(account_number, first_name, last_name)

    def calculate_interest(self):
        return self._balance * Savings_Account.interest_rate

        
def main():
    if __name__ == "__main__":
        main_directory:str = os.path.dirname(os.path.abspath(__file__))
        if len(sys.argv) > 1:
            mode = sys.argv[1]
            launch_interface(mode)
        else:
            subprocess.call(["python", os.path.join(main_directory, "launcher.py")])
            
def launch_interface(mode):
    accounts = {}
    if mode == 'cli':
        bank_app = Bank_Account_App(accounts)
        cli_ui = CLI_UI(bank_app)
        cli_ui.main_menu()
    elif mode == 'gui':
        root=tk.Tk()
        app=TK_UI(root,accounts)
        app.root.mainloop()

main()