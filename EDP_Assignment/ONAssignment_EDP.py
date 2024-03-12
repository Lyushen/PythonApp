import tkinter as tk
from tkinter import ttk #,messagebox
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
    database_dir:str = os.path.dirname(os.path.abspath(__file__)) + '\\database' #get current path of the .py file and locate database directory
    os.makedirs(database_dir, exist_ok=True) # Ensure the directory exists, otherwise create it without an error
    file_type='.csv'
    db_file_name:str='db_todo'
    db_file_path:str=os.path.join(database_dir,db_file_name+file_type)

    def __init__(self):
        self.el_manager = Element_Manager()
        
    def read_file(self,file_path) -> list:
        try:
            data=[]
            with open(file_path, 'r', encoding="utf-8-sig") as csvfile:
                for line in csvfile:
                    splitted_data = line.strip().split(',') #strip() helps get helps cut the non-printable characters like \n on beginning and end of strings
                    data.append(Element(splitted_data[0],splitted_data[1],splitted_data[2],splitted_data[3]))
                return data
        except Exception as ex:
            print(f"Error in reading the file '{file_path}'\n{ex}")
    
    def write_file(self,file_path,append=False) -> int:
        try:
            content = ''
            for row in self.el_manager.todo_list: # Compile data rows into a single string for each file
                content += ','.join([str(item) for item in row]) + '\n' # Convert each item to string, join with commas, and add a newline at the end
            with open(file_path, 'a' if append else 'w', encoding="utf-8-sig") as csvfile: # Checking if we are appending
                csvfile.write(content) # write built content in one go
            print(f'Successfully wrote the file {file_path+'.csv'}')
            return len(csvfile)
        except Exception as ex:
            print(f"Error in writing the file '{file_path}'\n{ex}")
            return 0

class UI(tk.Tk):
        def __init__(self) -> None:
            super().__init__()
            self.el_manager=Element_Manager()
            self.title("To-Do List")
            self.geometry("700x370+700+200")
            self.resizable(width=False, height=False)
            self.font=('Tahoma',12)
            self.entry_box_def_message="Enter your todo here..."
            self.entry_var = tk.StringVar() # setup a string variable that will be attached to entry box to track changes and disable or enable add button
            self.create_controls()

        def create_controls(self):
            self.grid_columnconfigure(0, weight=1) # Grid configuration for Treeview
            self.columnconfigure(1, weight=3)
            self.entry_box = tk.Entry(self, font=self.font, textvariable=self.entry_var)
            self.entry_box.grid(column=0, row=0, sticky='ew', pady=10,padx=10, columnspan=2)
            self.entry_box.insert(0, self.entry_box_def_message)
            self.entry_box.config(fg='grey')
            self.entry_box.bind("<FocusIn>", lambda event, m=self.entry_box_def_message, e=self.entry_box: self.clear_placeholder(event, e, m))
            self.entry_box.bind("<FocusOut>", lambda event, m=self.entry_box_def_message, e=self.entry_box: self.restore_placeholder(event, e, m))
            self.entry_box.bind('<Return>', self.adding_element) # event driven example on Enter press
            
            self.add_btn = tk.Button(self, text='Add', font=self.font, command=self.adding_element)
            self.add_btn.grid(column=2, row=0, sticky='ew', pady=10,padx=10)
            self.add_btn.config(state='disabled')
            self.add_btn.bind('<Button-1>', self.on_disabled_add_b_press)
            
            self.tree = ttk.Treeview(self, columns=('ID', 'Title', 'Description', 'Alarm', 'Done'), show='headings', selectmode='extended')
            self.tree.heading('ID', text='ID')
            self.tree.heading('Title', text='Title')
            self.tree.heading('Description', text='Description')
            self.tree.heading('Alarm', text='Alarm')
            self.tree.heading('Done', text='Done')
            # Adjusting column widths
            self.tree.column('ID', width=50, minwidth=50, stretch=tk.NO)
            self.tree.column('Title', width=200)
            self.tree.column('Description', width=250)
            self.tree.column('Alarm', width=100)
            self.tree.column('Done', width=50,stretch=tk.NO)
            # Adding the scrollbar
            scrollbar = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.grid(column=3, row=1, sticky='ns', padx=0)
            self.tree.bind('<<TreeviewSelect>>', self.on_list_select) #Event for Listbox that triggers on selection
            self.tree.bind('<Escape>', self.deselect_treeview)
            
            self.tree.grid(column=0, row=1, sticky='nsew', pady=10,padx=(10,0), columnspan=5)
            self.grid_columnconfigure(3, weight=0)
            self.update_the_list() # Update with preset data

            self.delete_btn = tk.Button(self, text='Delete', font=self.font, width=10, command=self.delete_element)
            self.delete_btn.grid(column=2, row=2, sticky='e', pady=10,padx=10,)
            self.delete_btn.config(state='disabled')
        
            self.done_btn = tk.Button(self, text='Mark Done', font=self.font, width=10, command=self.done_element)
            self.done_btn.grid(column=0, row=2, sticky='w', pady=10,padx=10,)
            self.done_btn.config(state='disabled')

            self.undo_btn = tk.Button(self, text='Undo', font=self.font, width=10, command=self.undo)
            self.undo_btn.grid(column=1, row=2, sticky='e', pady=10, padx=10)
            
            self.entry_var.trace_add("write", self.on_entry_change)

        def on_entry_change(self,*args):
            content = self.entry_var.get()
            if content.strip() and content != self.entry_box_def_message:
                self.add_btn.config(state='normal')
            else:
                self.add_btn.config(state='disabled')

        def on_disabled_add_b_press(self,event=''):
            self.entry_box.focus()
            
        def deselect_treeview(self,event):
            for item in self.tree.selection():
                self.tree.selection_remove(item)

        def on_list_select(self,event=''):
            selected_items=self.tree.selection()
            if len(selected_items)<=0:
                self.delete_btn.config(state='disabled')
                self.done_btn.config(state='disabled')
            else:
                self.delete_btn.config(state='normal')
                self.done_btn.config(state='normal')

        def clear_placeholder(self,event, entry_box, default_message:str):
            if entry_box.get() == default_message:
                entry_box.delete(0, tk.END)
                entry_box.config(fg='black')

        def restore_placeholder(self, event, entry_box, default_message:str):
            if entry_box.get() == "":
                entry_box.config(fg='grey')
                entry_box.insert(0, default_message)

        def update_the_list(self):
            for item in self.tree.get_children():
                self.tree.delete(item)
            for inx,el in enumerate(self.el_manager.todo_list):
                done_status = '「✔」' if el.completed else '「    」'
                self.tree.insert('', 'end', values=(inx+1, el.title, el.details, el.alarm_target_time, done_status))

        def adding_element(self, event=None):
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

class Element:
    def __init__(self,title,details='',alarm_target_time=None) -> None:
        self.title=title
        self.details=details
        self.completed=False
        self.alarm_target_time=alarm_target_time

class Element_Manager:
    def __init__(self) -> None:
        self.todo_list=[]
        self.history = []
        self.add_dummy_els() # debug fill

    # def get_element(self,title):
    #     return 
    def add_dummy_els(self):
        for i in range(1,21):
            self.add_element(f'Dummy{i}',f'Deets{i}',None)
    
    def add_element(self, title, details='', alarm_target_time=None):
        new_element = Element(title, details, alarm_target_time)
        self.todo_list.append(new_element)
        self.history.append(('add', len(self.todo_list) - 1, new_element)) # Store the action, index, and element object in history

    def complete_element(self, indexes):
        unique_indexes = set(indexes)

        for index in unique_indexes:
            if 0 <= index < len(self.todo_list):
                element = self.todo_list[index]
                element.completed = not element.completed  # Toggle the completion status
                # Record this action for undo
                self.history.append(('complete', index, element.completed))
    
    def delete_elements_by_ids(self, ids_to_delete):
        indexes_to_delete_sorted = sorted(ids_to_delete, reverse=True)
        for index in indexes_to_delete_sorted:
            if index < len(self.todo_list) and index >= 0:
                deleted_element = self.todo_list.pop(index)  # pop by index
                # Store the action, index, and element object before deletion
                self.history.append(('delete', index, deleted_element))
        
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
            self.todo_list[index].completed = not self.todo_list[index].completed
    
    def set_alarm(self):
        pass
    
    def edit_alarm(self):
        pass
    
    def delete_alarm(self):
        pass
    

if __name__ == '__main__':
    app = UI()
    app.mainloop()