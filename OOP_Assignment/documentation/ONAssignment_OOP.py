import tkinter as tk
import random

class Bank_Account_App:
    def __init__(self, accounts:dict) -> None:
        self._accounts=accounts
    
    def add_account(self):
        pass
    
    def close_account(self):
        pass
    
    def safe_cast(value, to_type, default=None):
        try:
            return to_type(value)
        except (ValueError, TypeError) as ex:
            print(f'Error during convertation {ex}')
            return default
    
class UI(Bank_Account_App): #button to open an account and a place holder
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

    
    def generate_account_number(self,current:bool=True)-> str:
        account_number=""
        if current:
            account_number='CA'+random.randint(1,9)+random.randint(0,9)+random.randint(0,9)
        else:
            account_number='SA'+random.randint(1,9)+random.randint(0,9)+random.randint(0,9)
        return account_number
    
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
    
    
class Accounts(Bank_Account_App):
    def __init__(self,account_nubmer:str,first_name:str,last_name:str) -> None:
        self.account_nubmer=account_nubmer
        self.deposit_fee=0.00
        self.withdraw_fee=0.00
        self.first_name=first_name
        self.last_name=last_name
        pass

    def _get_balance(self) -> float:
        return self._balance
    
    def _set_balance(self,amount:float):
        self._balance=amount
    
    def deposit(self,amount:float):
        self._balance+=amount #logic of the calculation?

    def withdraw(self,amount:float):
        self._balance-=amount

class Current_Account(Accounts):
    def __init__(self,account_nubmer:str) -> None:
        super().__init__(account_nubmer)
        self._balance=0
        
        
class Savings_Account(Accounts):
    def __init__(self, account_nubmer:str) -> None:
        super().__init__(account_nubmer)
        self._balance=0.00
        
    def get_balance(self) -> float:
        return self._balance
    
    def set_balance(self,value:float):
        self.balance=value
        
def main():
    root=tk.Tk()
    app=UI(root,{})
    root.mainloop()
    
main()