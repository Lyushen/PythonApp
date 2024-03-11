import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class Element:
    def __init__(self, id, title, details='', completed=False, priority=0, due_date=None):
        self.id = id
        self.title = title
        self.details = details
        self.completed = completed
        self.priority = priority
        self.due_date = due_date

class Observer:
    def update(self, *args, **kwargs):
        pass

class ElementManager:
    def __init__(self):
        self.elements = []
        self.next_id = 1
        self.observers = []
        self.history = []

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(*args, **kwargs)

    def add_element(self, title, details='', priority=0, due_date=None):
        element = Element(self.next_id, title, details, completed=False, priority=priority, due_date=due_date)
        self.elements.append(element)
        self.next_id += 1
        self.history.append(('add', element.id))
        self.notify_observers()

    def delete_element(self, id, undo=False):
        element = self.find_element(id)
        if element:
            self.elements.remove(element)
            if not undo:
                self.history.append(('delete', element))
            self.notify_observers()

    def find_element(self, id):
        for el in self.elements:
            if el.id == id:
                return el
        return None

    def toggle_completed(self, id):
        element = self.find_element(id)
        if element:
            element.completed = not element.completed
            self.notify_observers()

    def undo(self):
        if not self.history:
            return
        action, element_id = self.history.pop()
        if action == 'add':
            self.delete_element(element_id, undo=True)
        elif action == 'delete':
            self.elements.append(element_id)
            self.next_id = max(el.id for el in self.elements) + 1
        self.notify_observers()

    def sort_elements(self):
        self.elements.sort(key=lambda x: (x.priority, x.due_date or datetime.date.max))
        self.notify_observers()

class TodoListGUI(tk.Tk, Observer):
    def __init__(self, element_manager):
        super().__init__()
        self.element_manager = element_manager
        self.element_manager.add_observer(self)
        self.title("To-Do List")
        self.geometry("800x600")

        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="Title:").pack(side=tk.LEFT)
        self.title_entry = tk.Entry(frame)
        self.title_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        tk.Label(frame, text="Details:").pack(side=tk.LEFT)
        self.details_entry = tk.Entry(frame)
        self.details_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        tk.Label(frame, text="Priority:").pack(side=tk.LEFT)
        self.priority_entry = tk.Spinbox(frame, from_=0, to=5, width=5)
        self.priority_entry.pack(side=tk.LEFT)

        tk.Label(frame, text="Due Date (YYYY-MM-DD):").pack(side=tk.LEFT)
        self.due_date_entry = tk.Entry(frame)
        self.due_date_entry.pack(side=tk.LEFT)

        add_button = tk.Button(frame, text="Add Task", command=self.add_element)
        add_button.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Details", "Completed", "Priority", "Due Date"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Details", text="Details")
        self.tree.heading("Completed", text="Completed")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        control_frame = tk.Frame(self)
        control_frame.pack(fill=tk.X)

        delete_button = tk.Button(control_frame, text="Delete", command=self.delete_element)
        delete_button.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        toggle_button = tk.Button(control_frame, text="Toggle Completed", command=self.toggle_completed)
        toggle_button.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        undo_button = tk.Button(control_frame, text="Undo", command=self.undo_action)
        undo_button.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        sort_button = tk.Button(control_frame, text="Sort", command=self.sort_elements)
        sort_button.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

        self.refresh_treeview()

    def add_element(self):
        title = self.title_entry.get()
        details = self.details_entry.get()
        priority = int(self.priority_entry.get())
        due_date_str = self.due_date_entry.get()
        due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

        if not title:
            messagebox.showerror("Error", "Title cannot be empty.")
            return

        self.element_manager.add_element(title, details, priority, due_date)
        self.title_entry.delete(0, tk.END)
        self.details_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)

    def delete_element(self):
        selected_item = self.tree.selection()
        if selected_item:
            id = int(self.tree.item(selected_item, 'values')[0])
            self.element_manager.delete_element(id)

    def toggle_completed(self):
        selected_item = self.tree.selection()
        if selected_item:
            id = int(self.tree.item(selected_item, 'values')[0])
            self.element_manager.toggle_completed(id)

    def undo_action(self):
        self.element_manager.undo()

    def sort_elements(self):
        self.element_manager.sort_elements()

    def update(self):
        self.refresh_treeview()

    def refresh_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for el in self.element_manager.elements:
            completed_text = "Yes" if el.completed else "No"
            due_date = el.due_date.strftime('%Y-%m-%d') if el.due_date else ''
            self.tree.insert('', 'end', values=(el.id, el.title, el.details, completed_text, el.priority, due_date))

if __name__ == "__main__":
    element_manager = ElementManager()
    app = TodoListGUI(element_manager)
    app.mainloop()