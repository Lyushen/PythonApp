import tkinter as tk
from tkinter import ttk,messagebox

def safe_cast(value, to_type, default=None):
    try:
        return to_type(value)
    except (ValueError, TypeError) as ex:
        print(f'Error during convertation {ex}')
        return default

class UI(tk.Tk):
        def __init__(self) -> None:
            super().__init__()
            self.el_manager=Element_Manager()
            self.title("To-Do List")
            self.geometry("700x370+700+200")
            self.resizable(width=False, height=False)
            self.font=('Tahoma',12)
            self.entry_box_def_message="Enter your todo here..."
            self.create_controls()

        def create_controls(self):
            self.grid_columnconfigure(0, weight=1) # Grid configuration for Treeview
            self.columnconfigure(1, weight=3)
            self.entry_box = tk.Entry(self, font=self.font)
            self.entry_box.grid(column=0, row=0, sticky='ew', pady=10,padx=10, columnspan=2)
            self.entry_box.insert(0, self.entry_box_def_message)
            self.entry_box.config(fg='grey')
            self.entry_box.bind("<FocusIn>", lambda event, m=self.entry_box_def_message, e=self.entry_box: self.clear_placeholder(event, e, m))
            self.entry_box.bind("<FocusOut>", lambda event, m=self.entry_box_def_message, e=self.entry_box: self.restore_placeholder(event, e, m))
            self.entry_box.bind('<Return>', self.adding_element) # event driven example on Enter press

            self.add_btn = tk.Button(self, text='Add', font=self.font, command=self.adding_element)
            self.add_btn.grid(column=2, row=0, sticky='ew', pady=10,padx=10)
            self.add_btn.config(state='disabled')
            
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
            
            self.tree.grid(column=0, row=1, sticky='nsew', pady=10,padx=(10,0), columnspan=3)
            self.grid_columnconfigure(3, weight=0)
            self.update_the_list() # Update with preset data

            self.delete_btn = tk.Button(self, text='Delete', font=self.font, width=10, command=self.delete_element)
            self.delete_btn.grid(column=2, row=2, sticky='e', pady=10,padx=10,)
            self.delete_btn.config(state='disabled')
        
            self.done_btn = tk.Button(self, text='Mark Done', font=self.font, width=10, command=self.done_element)
            self.done_btn.grid(column=0, row=2, sticky='w', pady=10,padx=10,)
            self.done_btn.config(state='disabled')

            self.undo_btn = tk.Button(self, text='Undo', font=self.font, width=10, command=self.undo)
            self.undo_btn.grid(column=1, row=2, sticky='ew', pady=10,padx=10,)


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
            self.add_btn.config(state='normal')

        def restore_placeholder(self, event, entry_box, default_message:str):
            if entry_box.get() == "":
                entry_box.config(fg='grey')
                entry_box.insert(0, default_message)
            self.add_btn.config(state='disabled')

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
            selected_items = self.tree.selection()
            ids_to_delete = [self.tree.item(item, 'values')[0] for item in selected_items]
            self.el_manager.delete_elements_by_ids(ids_to_delete)
            self.update_the_list()
        
        def done_element(self):
            selected_items = self.tree.selection()
            for item in selected_items:
                item_values = self.tree.item(item, 'values')
                el_id = item_values[0]
                self.el_manager.complete_element(safe_cast(el_id,int,0))
            self.update_the_list()

        def undo(self):
            self.el_manager.undo()
            self.update_the_list()

class Element:
    _last_id = 0
    def __init__(self,title,details='',alarm_target_time=None) -> None:
        Element._last_id += 1
        self.id = Element._last_id
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
            self.todo_list.append(Element(f'Dummy{i}',f'Deets{i}',None))
    
    def add_element(self, title, details='', alarm_target_time=None):
        new_element = Element(title, details, alarm_target_time)
        self.todo_list.append(new_element)
        self.history.append(('add', new_element.id))

    def complete_element(self, el_id):
        for el in self.todo_list:
            if el.id == el_id:
                el.completed = not el.completed
                self.history.append(('complete', [el_id])) # Recording the action for undo
                break
    
    def delete_elements_by_ids(self, ids_to_delete):
        ids_to_delete = set(map(int, ids_to_delete))
        deleted_items = [(el.id, el) for el in self.todo_list if el.id in ids_to_delete]
        self.todo_list = [el for el in self.todo_list if el.id not in ids_to_delete]
        if deleted_items:
            self.history.append(('delete', deleted_items))
        
    def undo(self):
        if not self.history:
            return
        action, details = self.history.pop()
        if action == 'delete':
            for el_id, el in reversed(details):
                self.todo_list.insert(el_id - 1, el)
        elif action == 'add':
            self.todo_list = [el for el in self.todo_list if el.id != details]
    
    def set_alarm(self):
        pass
    
    def edit_alarm(self):
        pass
    
    def delete_alarm(self):
        pass
    

if __name__ == '__main__':
    app = UI()
    app.mainloop()