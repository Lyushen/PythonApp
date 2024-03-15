import tkinter as tk
from tkinter import ttk,messagebox,filedialog,Entry,Scrollbar,Button,Menu
import os,ctypes
from task_manager import Task_Manager
from db_io import Database_IO,RELATIVE_PY_PATH,safe_cast

class UI(tk.Tk):
    def __init__(self) -> None:
        """The initialisation of our GUI interface, as we inherit from tk.Tk parent, we can refer to self as to the root. It simplifies interaction with root. Instead of using self.root. all the time, we refer to self."""
        super().__init__() # Inherits of the root
        self.el_manager=Task_Manager() # IInitialisation of the instance of Element_Manager, that will be storing and responsible for interaction with our database list
        self.db_ref = Database_IO(self.el_manager) #  The passage of the reference to ensure that we use only one Element_Manager.todo_list
        self.title("To-Do List")
        self.geometry("700x370+700+200")
        self.resizable(width=False, height=False) # Do not allow a user to change the main window size
        self.font=('Tahoma',12) # Default font
        self.entry_box_def_message="Enter your todo here..." # Message for enter_box Entry, as we use it multiple times, we better store it once
        self.entry_var = tk.StringVar() # Setup a string variable that will be attached to the entry box to track changes and disable or enable the add button
        if os.name == 'nt': ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID() # Apply icon to current app_id. Usable to apply an icon to Windows' Taskbar using ctypes library. To avoid issues we check if that is Windows to use Windll library. May not work as intended as it's not compiled exe version.
        self.iconbitmap(default=RELATIVE_PY_PATH + '/database/ico/to-do-list.ico')
        self.on_start() # Initialization stage where we create controls and read our db file
        self.protocol("WM_DELETE_WINDOW", self.on_exit_app) # creating tracks for the even when we close the app with X
        self.last_sort_col = None # Sorting variables. Remember the last sorted column.
        self.sort_reverse = False 
        self.dragged_item = None
        self.scroll_enabled=False
    
    # Initialisation
    def on_start(self):
        """ Initialization stage where we create controls and read our db file."""
        self.create_controls()
        self.ui_read_file()

    def create_controls(self):
        """The function is responsible to create GUI interface and assign multiple events."""
        # Applying styling to Treeview and main form background
        style = ttk.Style(self) # style.theme_use("calm")
        style.configure("Treeview", background="#FDE8B4", fieldbackground="#FEEFCD")
        self.configure(background='#FEEFCD')
        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.columnconfigure(1, weight=3)
        # Entry Box lable used to add elements to the list
        self.entry_box = Entry(self, font=self.font, fg='grey', textvariable=self.entry_var)
        self.entry_box.grid(column=0, row=0, sticky='we', pady=10, padx=(10,140), columnspan=3)
        self.entry_box.insert(0, self.entry_box_def_message) # Preset default holder message into our enry_box on creation stage
        self.entry_box.bind("<FocusIn>", lambda event, m=self.entry_box_def_message, e=self.entry_box: self.clear_placeholder(e, m, event))
        self.entry_box.bind("<FocusOut>", lambda event, m=self.entry_box_def_message, e=self.entry_box: self.restore_placeholder(e, m, event))
        self.entry_box.bind('<Return>', self.add_task) # Event-driven example on Enter press
        self.entry_box.bind('<Escape>', self.deselect_widget) # Deselect the Entry Box on Escape button
        # Setup tracking system for the entry_box input variable that will call an event each time the value is changing
        self.entry_var.trace_add("write", self.on_entry_change)
        # Add button creation
        self.add_btn = tk.Button(self, text='Add', font=self.font, command=self.add_task, width=10)
        self.add_btn.grid(column=2, row=0, sticky='e', pady=10, padx=10)
        self.add_btn.config(state='disabled') # By default, it will be disabled, as no elements are selected in a Treeview filed
        self.add_btn.bind('<Button-1>', self.on_disabled_add_btn) # Even if the button is disabled, we still can track pressing, in our case we use it to focus on the Entry Box
        # Treeview widget used from tkinter.ttk library to display our todo_list
        self.tree = ttk.Treeview(self, columns=('ID', 'Title', 'Description', 'Alarm', 'Done'), show='headings', selectmode='extended')
        self.tree.heading('ID', text='ID', command=lambda: self.tree_sort_column('ID')) # Assigning sorting events
        self.tree.heading('Title', text='Title', command=lambda: self.tree_sort_column('Title'))
        self.tree.heading('Description', text='Description', command=lambda: self.tree_sort_column('Description'))
        self.tree.heading('Alarm', text='Alarm', command=lambda: self.tree_sort_column('Alarm'))
        self.tree.heading('Done', text='Done', command=lambda: self.tree_sort_column('Done'))
        # Adjusting column widths for the Treeview
        self.tree.column('ID', width=50, minwidth=50, stretch=tk.NO)
        self.tree.column('Title', width=200)
        self.tree.column('Description', width=250)
        self.tree.column('Alarm', width=100)
        self.tree.column('Done', width=63,stretch=tk.NO)
        self.tree.bind('<<TreeviewSelect>>', self.on_list_select) # Event that triggers on selecting any element
        self.tree.bind('<Escape>', self.deselect_widget) # Escape button to deselect our choices
        self.tree.bind('<Delete>', self.delete_task) # Escape button to deselect our choices
        self.tree.bind('<Double-1>', self.complete_task) # Bind double-click event
        self.tree.grid(column=0, row=1, sticky='nsew', pady=10,padx=(10,0), columnspan=3)
        # Adding the scrollbar to our Treeview
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(column=3, row=1, sticky='ns', padx=0)
        # Adding Delete button
        self.delete_btn = Button(self, text='Delete', font=self.font, width=10, command=self.delete_task)
        self.delete_btn.grid(column=1, row=2, sticky='e', pady=10,padx=10)
        self.delete_btn.config(state='disabled') # Disable state by default
        # Adding Done button
        self.done_btn = Button(self, text='Complete', font=self.font, width=10, command=self.complete_task)
        self.done_btn.grid(column=0, row=2, sticky='w', pady=10,padx=10,)
        self.done_btn.config(state='disabled') # Disable state by default
        # Adding Duplicate button
        self.duplicate_btn = Button(self, text='Duplicate', font=self.font, width=10, command=self.duplicate_task)
        self.duplicate_btn.grid(column=1, row=2, sticky='w', pady=10,padx=10)
        self.duplicate_btn.config(state='disabled') # Disable state by default
        # Adding Undo button
        self.undo_btn = Button(self, text='Undo', font=self.font, width=10, command=self.undo)
        self.undo_btn.grid(column=2, row=2, sticky='e', pady=10, padx=10)
        self.undo_btn.config(state='disabled') # Disable state by default
        # Setup menu
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)
        # File menu
        self.file_menu = Menu(self.menu_bar, tearoff=0, bg="#FEEFCD")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.on_open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.ui_save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Reload", command=self.ui_read_file, accelerator="Ctrl+R")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_exit_app, accelerator="Ctrl+Q")
        # Bind hotkeys
        self.bind('<Control-o>', self.on_open_file)
        self.bind('<Control-s>', self.ui_save_file)
        self.bind('<Control-r>', self.ui_read_file)
        self.bind('<Control-q>', self.on_exit_app)
        self.bind('<Control-d>', self.duplicate_task)
        self.bind('<Control-z>', self.undo)
        self.bind('<Control-c>', self.complete_task)
        self.tree.bind('<Control-a>', self.select_all)
        # Create a context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Complete", command=self.complete_task, accelerator="Ctrl+C")
        self.context_menu.add_command(label="Duplicate", command=self.duplicate_task, accelerator="Ctrl+D")
        self.context_menu.add_command(label="Delete", command=self.delete_task, accelerator="Delete")
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        # Bind the right-click context menu
        self.tree.bind("<Button-3>", self.show_context_menu)

    # DB file interaction
    def on_open_file(self,*_): # Extra function to ensure to save changes if there are some and call 
        """This is the event that triggers when we have unsaved changes before opening a new file.
        If there were any changes, the flag self.el_manager.is_modified will be True, in this case, we call function on_unsaved_changes and pass our ui_open_file callback function when we're done asking to save changes. Otherwise, we just call ui_open_file to the open file."""
        if self.el_manager.is_modified: 
            self.on_unsaved_changes(self.ui_open_file)
        else:
            self.ui_open_file()
    
    def ui_open_file(self):
        """This UI function asks a user to select a database file, and if we have a new path, we redefine the default path and will be working with that file from now on."""
        file_path = filedialog.askopenfilename(
            initialdir=self.db_ref.database_dir,  # Starting directory for the open_file dialog
            title="Select file",
            filetypes=(("Text or CSV database file", "*.txt *.csv"), ("all files", "*.*"))  # File filters
        )
        if file_path: # If a file was selected (not cancelled)
            if self.db_ref.db_read_file(self.update_ui_tree,file_path): # If we read the file and pass a new file path, also pass our update UI function to update the tree with new information
                self.el_manager.is_modified = False # We read fresh new data, and set is_modified to false to reflect the fresh stage for the on_unsaved_changes question

    def ui_save_file(self,*_):
        """An internal function-event intends to call the external db_save_file function from the DB class."""
        self.db_ref.db_save_file()
    
    def ui_read_file(self,*_):
        """An internal function-event intends to call the external db_read_file function from the DB class."""
        self.db_ref.db_read_file(self.update_ui_tree)

    def on_exit_app(self,*_):
        """A function-event intends to call the on_unsaved_changes function-question and as a callback, we pass root.quit() if we finish successfully, otherwise if changes have not been detected, we exit the application."""
        if self.el_manager.is_modified:
            self.on_unsaved_changes(self.quit)
        else:
            self.quit()
    
    def on_unsaved_changes(self,callback:callable):
        """Function Event if changes have been detected we call save and callback optional function.

        Args:
            callback (callable): This callable variable we use to pass execution in succesfull cases.

        Returns: If user_choice is None, it means Cancel was selected, so we do nothing and return from the function."""
        user_choice = messagebox.askyesnocancel("You have unsaved changes", "Do you want to save changes?")
        if user_choice is True:  # Save
            self.db_ref.db_save_file()
            if callback: callback()
        elif user_choice is False:  # Don't Save
            if callback: callback()
        return # If user_choice is None, it means Cancel was selected, so we do nothing and return from the function
    
    # Actual functionality
    def update_ui_tree(self):
        """Updated our Tree in a way to recreate it, it's a more efficient way to interact with the Tree instead of iterating through the tree values to delete some index."""
        self.undo_button_state_check()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for inx,el in enumerate(self.el_manager.todo_list):
            done_status = '「✔」' if el.completed==1 else '「    」'
            self.tree.insert('', 'end', values=(inx+1, el.title, el.details, el.alarm_target_time, done_status))

    def add_task(self,*_):
        """The function adds task elements to the to-do storage list. Also, we update the tree, clears previous entries and out-focus the entry_box.
        This function also has an additional optional parameter to make it callable as an event."""
        title = self.entry_box.get().strip()
        if title != self.entry_box_def_message and title != "":
            self.el_manager.add_element(title)
            self.update_ui_tree()
            self.entry_box.delete(0, tk.END)
            self.focus()

    def delete_task(self,*_):
        """Deletion number of tasks, possible multiple selections and delete multiple. And updates the tree. Has DELETE hotkey.
        This function also has an additional optional parameter to make it callable as an event."""
        selected_indices = [self.tree.index(item) for item in self.tree.selection()] # Retrieve the correct index
        self.el_manager.delete_elements_by_ids(selected_indices) # delete elements by indexes
        self.update_ui_tree()
    
    def complete_task(self,*_):
        """Completing tasks with multiple selections. And updates the tree.
        This function also has an additional optional parameter to make it callable as an event."""
        indexes_to_toggle = [self.tree.index(item) for item in self.tree.selection()]  # Retrieve the correct index
        self.el_manager.complete_element(indexes_to_toggle) # call the complete method with the list of indexes
        self.update_ui_tree()

    def undo(self,*_):
        """Undo added, deleted or completed tasks one action by the time. And updates the tree. Has CTRL+Z hotkey.
        This function also has an additional optional parameter to make it callable as an event."""
        self.el_manager.undo()
        self.update_ui_tree()
        
    def undo_button_state_check(self):
        """In each update tree call, we check if there is history for UNDO action, if there is, we enable the button, otherwise history has no stored actions. The same is for context menu option."""
        if len(self.el_manager.history)>0:
            self.undo_btn.config(state='normal')
            self.context_menu.entryconfig("Undo", state="normal")
        else:
            self.undo_btn.config(state='disabled')
            self.context_menu.entryconfig("Undo", state="disabled")
        
    def duplicate_task(self, *_):
        """Duplication of the task, it supports multiple selections and places duplications after each currently selected task (by index in the list).
        This function also has an additional optional parameter to make it callable as an event."""
        selected_items = self.tree.selection()  # Get the selected item(s)
        for item in reversed(selected_items):
            item_values = self.tree.item(item, 'values')
            index_to_insert = safe_cast(item_values[0], int, 0) # Duplicate at the calculated index
            self.el_manager.add_element_by_index(index_to_insert, *item_values[1:-1]) # *item_values[1:-1] correctly represents the additional parameters your method expects
        self.update_ui_tree()
    
    def select_all(self,*_):
        """Select All function when the tree is focused. Has CTRL+A hotkey.
        This function also has an additional optional parameter to make it callable as an event."""
        self.tree.selection_set(self.tree.get_children())
        
    # Events    
    def show_context_menu(self, event):
        """Displays context menu on Right Mouse Button press without altering selection. Operates on already selected items.
        If no items are selected, it disables certain actions."""
        try:
            if self.tree.selection():
                # Enable actions if items are selected
                self.context_menu.entryconfig("Complete", state="normal")
                self.context_menu.entryconfig("Duplicate", state="normal")
                self.context_menu.entryconfig("Delete", state="normal")
            else:
                # Disable actions if no items are selected
                self.context_menu.entryconfig("Complete", state="disabled")
                self.context_menu.entryconfig("Duplicate", state="disabled")
                self.context_menu.entryconfig("Delete", state="disabled")
            # Show the context menu at the cursor's location in any case
            self.context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            print(f'Error in context menu:{e}')

    def tree_sort_column(self, col:str):
        """Sorting tree by clicking on a column header. Prioritizing Ascending sorting. Only if you already selected column press the second time - Descending order will apply.

        Args:
            col (str): Column name
        """
        if self.last_sort_col != col: # Ensure that we always switch to ascending sorting when we switch to a new column
            self.sort_reverse = False
        else:
            self.sort_reverse = not self.sort_reverse
        if col == 'ID':
            l = [(safe_cast((self.tree.set(k, col)),int,0), k) for k in self.tree.get_children('')]
        else:
            l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=self.sort_reverse)
        for index, (val, k) in enumerate(l): # Rearrange items in sorted positions (Descending sorting)
            self.tree.move(k, '', index)
        self.last_sort_col = col # Reverse sort next time
        self.tree.heading(col, command=lambda: self.tree_sort_column(col))
    
    def on_entry_change(self,*_):
        """This function-event triggers when entry_var gets changed to enable/disable add button"""
        content = self.entry_var.get()
        if content.strip() and content != self.entry_box_def_message:
            self.add_btn.config(state='normal')
        else:
            self.add_btn.config(state='disabled')

    def on_disabled_add_btn(self,*_):
        """Simple function to focus on the entry box"""
        self.entry_box.focus()
        
    def deselect_widget(self,*_):
        """If we have selection inside the tree, we deselect it, otherwise we focus on the root window"""
        if self.tree.selection():
            for item in self.tree.selection():
                self.tree.selection_remove(item)
        else:
            self.focus()

    def on_list_select(self,*_):
        """Disable/Enable Done and Delete buttons and their context menus if we have selected at least one task."""
        selected_items=self.tree.selection()
        if len(selected_items)<=0:
            self.delete_btn.config(state='disabled')
            self.done_btn.config(state='disabled')
            self.duplicate_btn.config(state='disabled')
        else:
            self.delete_btn.config(state='normal')
            self.done_btn.config(state='normal')
            self.duplicate_btn.config(state='normal')

    def clear_placeholder(self,entry_box, default_message:str,*_):
        """Function-event that clear placeholder massage when focused."""
        if entry_box.get() == default_message:
            entry_box.delete(0, tk.END)
            entry_box.config(fg='black')

    def restore_placeholder(self,entry_box, default_message:str,*_):
        """Function-event that restores the placeholder message when unfocused."""
        if entry_box.get() == "":
            entry_box.config(fg='grey')
            entry_box.insert(0, default_message)

def main():
    app = UI()
    app.mainloop()

if __name__ == '__main__':
    main()