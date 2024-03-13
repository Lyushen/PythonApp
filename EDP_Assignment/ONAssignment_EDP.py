import tkinter as tk
from tkinter import ttk,messagebox,filedialog
import os

def safe_cast(value, to_type, default=None):
    """This function ensures that we won't get an error during the converting
    Args:
        value (str): String representation of the value that we need to convert
        to_type (type): To what type should we convert (int, float, etc)
        default (any, optional): Any value that the user wants to return if the converting failed. Defaults to None.
    Returns:
        type: converted value to required type    """
    try:
        return to_type(value)
    except (ValueError, TypeError) as ex:
        print(f"DEBUG: Convertation error - {ex}. Returning defaul value '{default}'.")
        return default

class Database_IO:
    """A separate Database class is made to create some private functions that aim to interact with database files."""

    def __init__(self, el_manager):
        self.database_dir:str = os.path.dirname(os.path.abspath(__file__)) + '\\database' #get current path of the .py file and locate database directory
        os.makedirs(self.database_dir, exist_ok=True) # Ensure the directory exists, otherwise create it without an error
        self.file_type='.csv' # just incase we want to change the default extention to txt for example
        self.db_file_name:str='db_todo' # database file name
        self.db_file_path:str=os.path.join(self.database_dir,self.db_file_name+self.file_type) # building database file path with os.path.join function built-in the os library
        """Database_IO class initialisation. We receive as an argument the referance to our external Element_Manager instance.

        Args:
            el_manager (Element_Manager): The received reference is to ensure that we use only one list
        """
        self.el_manager = el_manager

    def db_save_file(self,file_path:str=None):
        """This is a public function to save the todo list to the file

        Args:
            file_path (str, optional): Defaults (if none) to self.db_file_path. The path to our file that we're going to write. Parameter is optional because if we able to pass parameter which to which file we want to save, we use predefined database directory, from relative path that has been built in db_file_path
        """
        if file_path is None:
            file_path = self.db_file_path
        if self.__write_file(file_path):
            self.is_modified=False

    def db_read_file(self,update_callback:callable,file_path:str=None):
        """The public function inside our Database_IO class is intended to read our database file. We also redefine db_filepath received from the user in case of usage of the Open File function

        Args:
            update_callback (callable): As parameter we receive reference to update the interface function and we call it on succesfull complition of private __read_file function
            file_path (str, optional): Defaults (if none) to self.db_file_path. The path to our file. Parameter is optional because if we don't use this function to open file, we use predefined database directory, from relative path that has been built in db_file_path
        """
        if file_path is None:
            file_path = self.db_file_path
        if self.__read_file(file_path):
            if file_path != self.db_file_path:
                self.db_file_path = file_path # redefine the file path 
            update_callback()

    def __read_file(self,file_path:str) -> bool:
        """Private function to read a database file

        Args:
            file_path (str): Path to the file that we want to read

        Returns:
            bool: We return succsessful or not was the function, if not, we don't call an update_interface callback function
        """
        try:
            self.el_manager.todo_list=[] # clear list before we refill it with the new read data
            with open(file_path, 'r', encoding="utf-8") as csvfile:
                content = csvfile.read()  # Read the entire file content at once
                lines = content.strip().split('\n')  # Split content into lines
                for line in lines:
                    splitted_data = line.strip().split(',') #strip() cuts the non-printable characters like \n on beginning and end of the string
                    self.el_manager.todo_list.append(Element(splitted_data[0],splitted_data[1],splitted_data[2],safe_cast(splitted_data[3],int,0)))
                return True
        except Exception as ex:
            print(f"Error in reading the file '{file_path}'\n{ex}")
            return False
    
    def __write_file(self, file_path:str, append:bool=False) -> bool:
        """Private function to write the database file

        Args:
            file_path (str): Path to the file that we want to write
            append (bool, optional): Defaults to False. if we want to add data to existing list, we can set parameter to True and we will use Appent instead of Write 

        Returns:
            bool: Rerurn Success of the function
        """
        try:
            content = ''
            for el in self.el_manager.todo_list:
                content += f"{el.title},{el.details},{el.alarm_target_time},{0 if el.completed==False else 1}\n"
            with open(file_path, 'a' if append else 'w', encoding="utf-8") as csvfile: # Optional parameter Append if we passed True or Write if we passed False or used defaul value
                csvfile.write(content) # Write the file in one go
            print(f'Successfully wrote the file {file_path}')  # Corrected
            # Assuming you have a method to update the is_modified flag or directly accessing the attribute
            self.el_manager.is_modified = False  # Directly setting the attribute, adjust according to your implementation
            return True
        except Exception as ex:
            print(f"Error in writing the file '{file_path}'\n{ex}")
            return False

class UI(tk.Tk):
        def __init__(self) -> None:
            """The initialisation of our GUI interface, as we inherit from tk.Tk parent, we can refer to self as to root. It simplifies interaction with root. Instead of using self.root. all the time, we refer to self.
            """
            super().__init__() # Inherits of the root
            self.el_manager=Element_Manager() # Initialisation of the instance of Element_Manager, that will be stroing and responsible for interaction our database list
            self.db_ref = Database_IO(self.el_manager) #  The passsage of the reference to ensure that we use only one Element_Manager.todo_list
            self.title("To-Do List")
            self.geometry("700x370+700+200")
            self.resizable(width=False, height=False) # Do not allow user to change the main window size
            self.font=('Tahoma',12) # Default font
            self.entry_box_def_message="Enter your todo here..." # Message for enter_box Entry, as we use it multiple times, we better to store it once
            self.entry_var = tk.StringVar() # Setup a string variable that will be attached to entry box to track changes and disable or enable add button
            self.on_start() # Initialization stage where we create controls and read our db file
            self.protocol("WM_DELETE_WINDOW", self.on_exit_app) # creating track for the even when we close the app with X
        
        # Initialisation
        def on_start(self):
            """ Initialization stage where we create controls and read our db file."""
            self.create_controls()
            self.ui_read_file()

        def create_controls(self):
            """The function is responsible to create GUI interface and assign multiple events"""
            # Grid configuration
            self.grid_columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=3)
            # Entry Box lable used to add elements to the list
            self.entry_box = tk.Entry(self, font=self.font, fg='grey', textvariable=self.entry_var)
            self.entry_box.grid(column=0, row=0, sticky='ew', pady=10,padx=10, columnspan=2)
            self.entry_box.insert(0, self.entry_box_def_message) # Preset default holder message into our enry_box on creation stage
            self.entry_box.bind("<FocusIn>", lambda event, m=self.entry_box_def_message, e=self.entry_box: self.clear_placeholder(e, m, event))
            self.entry_box.bind("<FocusOut>", lambda event, m=self.entry_box_def_message, e=self.entry_box: self.restore_placeholder(e, m, event))
            self.entry_box.bind('<Return>', self.adding_element) # Event-driven example on Enter press
            self.entry_box.bind('<Escape>', self.deselect_widget) # Deselect the Entry Box on Escape button
            # Add button creation
            self.add_btn = tk.Button(self, text='Add', font=self.font, command=self.adding_element)
            self.add_btn.grid(column=2, row=0, sticky='ew', pady=10,padx=10)
            self.add_btn.config(state='disabled') # By default, it will be disabled, as no elements selected in a Treeview filed
            self.add_btn.bind('<Button-1>', self.on_disabled_add_b_press) # Even if the button disabled, we still are able to track pressing, in our case we use it to focus on the Enry Box
            # Treeview widget used from tkinter.ttk library to display our todo_list
            self.tree = ttk.Treeview(self, columns=('ID', 'Title', 'Description', 'Alarm', 'Done'), show='headings', selectmode='extended')
            self.tree.heading('ID', text='ID')
            self.tree.heading('Title', text='Title')
            self.tree.heading('Description', text='Description')
            self.tree.heading('Alarm', text='Alarm')
            self.tree.heading('Done', text='Done')
            # Adjusting column widths for the Treeview
            self.tree.column('ID', width=50, minwidth=50, stretch=tk.NO)
            self.tree.column('Title', width=200)
            self.tree.column('Description', width=250)
            self.tree.column('Alarm', width=100)
            self.tree.column('Done', width=50,stretch=tk.NO)
            # Adding the scrollbar to our Treeview
            scrollbar = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.grid(column=3, row=1, sticky='ns', padx=0)
            self.tree.bind('<<TreeviewSelect>>', self.on_list_select) # Event that triggers on selecting any element
            self.tree.bind('<Escape>', self.deselect_widget) # Escape button to deselect our choices
            self.tree.grid(column=0, row=1, sticky='nsew', pady=10,padx=(10,0), columnspan=5)
            # Adding Delete button
            self.delete_btn = tk.Button(self, text='Delete', font=self.font, width=10, command=self.delete_element)
            self.delete_btn.grid(column=2, row=2, sticky='e', pady=10,padx=10,)
            self.delete_btn.config(state='disabled') # Disable state by default
            # Adding Done button
            self.done_btn = tk.Button(self, text='Mark Done', font=self.font, width=10, command=self.done_element)
            self.done_btn.grid(column=0, row=2, sticky='w', pady=10,padx=10,)
            self.done_btn.config(state='disabled') # Disable state by default
            # Adding Undo button
            self.undo_btn = tk.Button(self, text='Undo', font=self.font, width=10, command=self.undo)
            self.undo_btn.grid(column=1, row=2, sticky='e', pady=10, padx=10)
    
            # Setup tracking system for variable that will call an event each time the value of that variable has been changed
            self.entry_var.trace_add("write", self.on_entry_change)
            
            # Setup menu
            self.menu_bar = tk.Menu(self)
            self.config(menu=self.menu_bar)
            # File menu
            self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="File", menu=self.file_menu)
            self.file_menu.add_command(label="Open", command=self.on_open_file, accelerator="Ctrl+O")
            self.file_menu.add_command(label="Save", command=self.ui_save_file, accelerator="Ctrl+S")
            self.file_menu.add_command(label="Reload", command=self.ui_read_file, accelerator="Ctrl+R")
            self.file_menu.add_separator()
            self.file_menu.add_command(label="Exit", command=self.on_exit_app, accelerator="Ctrl+Q")
            # Bind shortcuts
            self.bind('<Control-o>', self.on_open_file)
            self.bind('<Control-s>', self.ui_save_file)
            self.bind('<Control-r>', self.ui_read_file)
            self.bind('<Control-q>', self.on_exit_app)

        # DB file interaction
        def on_open_file(self,*_): # Extra function to ensure to save changes if there are some and call 
            """This is the event that trigers when we have unsaved changes before we open a new file
            If there was any changes, the flag self.el_manager.is_modified will be True, in this case we call function on_unsaved_changes and passing our ui_open_file callback function when we done asking to save changes. Otherwise we just call ui_open_file to open file"""
            if self.el_manager.is_modified: 
                self.on_unsaved_changes(self.ui_open_file)
            else:
                self.ui_open_file()
        
        def ui_open_file(self):
            """This UI function-event asks a user to select a database file, and if we have a new path, we redefine the default path and will be working with that file from now on"""
            file_path = filedialog.askopenfilename(
                initialdir=self.db_ref.database_dir,  # Starting directory for the open_file dialog
                title="Select file",
                filetypes=(("Text or CSV database file", "*.txt *.csv"), ("all files", "*.*"))  # File filters
            )
            if file_path: # If a file was selected (not cancelled)
                if self.db_ref.db_read_file(self.update_the_list,file_path): # If we read the file and pass new file path, also pass our update ui function to update the tree with new information
                    self.el_manager.is_modified = False # We read fresh new data, and set is_modified to false to reflect the fresh stage for the on_unsaved_changes question
                    
        
        def ui_save_file(self,*_):
            """An internal function-event intends to call the external db_save_file function from the DB class"""
            self.db_ref.db_save_file()
        
        def ui_read_file(self,*_):
            """An internal function-event intends to call the external db_read_file function from the DB class"""
            self.db_ref.db_read_file(self.update_the_list)

        def on_exit_app(self,*_):
            """A function-event intends to call the on_unsaved_changes function-question and as callback, we pass root.quit() if we finish successfully, otherwise if changes have not been detected, we exit the application"""
            if self.el_manager.is_modified:
                self.on_unsaved_changes(self.quit)
            else:
                self.quit()
        
        def on_unsaved_changes(self,callback:callable):
            """Function Event if there changes have been detected we call save and callback optional function

            Args:
                callback (callable): This callable variable we use to pass execution in succesfull cases

            Returns: If user_choice is None, it means Cancel was selected, so we do nothing and return from the function
            """
            user_choice = messagebox.askyesnocancel("You have unsaved changes", "Do you want to save changes?")
            if user_choice is True:  # Save
                self.db_ref.db_save_file()
                if callback: callback()
            elif user_choice is False:  # Don't Save
                if callback: callback()
            return # If user_choice is None, it means Cancel was selected, so we do nothing and return from the function
        
        # Actual functionality
        def update_the_list(self):
            """Updated our Tree in a way to recreate it, it's a more efficient way to interact with the Tree instead of iterating trough the tree values to delete some index """
            for item in self.tree.get_children():
                self.tree.delete(item)
            for inx,el in enumerate(self.el_manager.todo_list):
                done_status = '「✔」' if el.completed==1 else '「    」'
                self.tree.insert('', 'end', values=(inx+1, el.title, el.details, el.alarm_target_time, done_status))

        def adding_element(self,*_):
            """_summary_
            """
            title = self.entry_box.get().strip()
            if title != self.entry_box_def_message and title != "":
                self.el_manager.add_element(title, '')
                self.update_the_list()
                self.entry_box.delete(0, tk.END)
                self.focus()

        def delete_element(self):
            selected_indices = [self.tree.index(item) for item in self.tree.selection()] 
            self.el_manager.delete_elements_by_ids(selected_indices)
            self.update_the_list()
        
        def done_element(self):
            selected_items = self.tree.selection()
            indexes_to_toggle = [self.tree.index(item) for item in selected_items]  # Retrieve the correct index
            self.el_manager.complete_element(indexes_to_toggle) # call the complete method with the list of indexes
            self.update_the_list()

        def undo(self):
            self.el_manager.undo()
            self.update_the_list()
            
        # Events
        def on_entry_change(self,*_):
            content = self.entry_var.get()
            if content.strip() and content != self.entry_box_def_message:
                self.add_btn.config(state='normal')
            else:
                self.add_btn.config(state='disabled')

        def on_disabled_add_b_press(self,*_):
            self.entry_box.focus()
            
        def deselect_widget(self,*_):
            if self.tree.selection():
                for item in self.tree.selection():
                    self.tree.selection_remove(item)
            else:
                self.focus()

        def on_list_select(self,*_):
            selected_items=self.tree.selection()
            if len(selected_items)<=0:
                self.delete_btn.config(state='disabled')
                self.done_btn.config(state='disabled')
            else:
                self.delete_btn.config(state='normal')
                self.done_btn.config(state='normal')

        def clear_placeholder(self,entry_box, default_message:str,*_):
            if entry_box.get() == default_message:
                entry_box.delete(0, tk.END)
                entry_box.config(fg='black')

        def restore_placeholder(self,entry_box, default_message:str,*_):
            if entry_box.get() == "":
                entry_box.config(fg='grey')
                entry_box.insert(0, default_message)



class Element:
    def __init__(self,title,details='',alarm_target_time=None,completed=False) -> None:
        self.title=title
        self.details=details
        self.alarm_target_time=alarm_target_time
        self.completed=completed

class Element_Manager:
    def __init__(self) -> None:
        self.todo_list=[]
        self.history = []
        self.is_modified=False
        # self.add_dummies() # debug fill
      
    def add_dummies(self):
        for i in range(1,21):
            self.add_element(f'Dummy{i}',f'Deets{i}',None)
    
    def add_element(self, title, details='', alarm_target_time=None,completed=False):
        new_element = Element(title, details, alarm_target_time, completed)
        self.todo_list.append(new_element)
        self.history.append(('add', len(self.todo_list) - 1, new_element)) # Store the action, index, and element object in history
        self.is_modified=True

    def complete_element(self, indexes):
        unique_indexes = set(indexes)
        for index in unique_indexes:
            if 0 <= index < len(self.todo_list):
                element = self.todo_list[index]
                element.completed = not element.completed  # Toggle the completion status
                # Record this action for undo
                self.history.append(('complete', index, element.completed))
        self.is_modified=True

    def delete_elements_by_ids(self, ids_to_delete):
        indexes_to_delete_sorted = sorted(ids_to_delete, reverse=True)
        for index in indexes_to_delete_sorted:
            if index < len(self.todo_list) and index >= 0:
                deleted_element = self.todo_list.pop(index)  # pop by index
                # Store the action, index, and element object before deletion
                self.history.append(('delete', index, deleted_element))
        self.is_modified=True
        
    def undo(self):
        if not self.history:
            return
        action, index, data = self.history.pop()
        if action == 'delete':
            # Insert the element back at its original position
            self.todo_list.insert(index, data)
        elif action == 'add':
            # Remove the element that was last added
            self.todo_list.pop(index)
        elif action == 'complete':
            # Revert the completion status
            self.todo_list[index].completed = not self.todo_list[index].completed # Switch (Flip) a task status
        self.is_modified=True
    
    def set_alarm(self):
        pass
    
    def edit_alarm(self):
        pass
    
    def delete_alarm(self):
        pass
    

if __name__ == '__main__':
    app = UI()
    app.mainloop()