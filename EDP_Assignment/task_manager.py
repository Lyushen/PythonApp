class Task:
    def __init__(self,title,details='',alarm_target_time=None,completed=False) -> None:
        self.title=title
        self.details=details
        self.alarm_target_time=alarm_target_time
        self.completed=completed

class Task_Manager:
    def __init__(self) -> None:
        self.todo_list=[]
        self.history = []
        self.is_modified=False
        # self.add_dummies() # debug fill
      
    def add_dummies(self):
        for i in range(1,21):
            self.add_element(f'Dummy{i}',f'Deets{i}',None,False)
    
    def add_element_by_index(self,index:int, title:str, details:str='', alarm_target_time=None,completed:bool=False):
        new_element = Task(title, details, alarm_target_time, completed)
        self.todo_list.insert(index, new_element)
        self.history.append(('add', index, new_element)) # Store the action, index, and element object in history
        self.is_modified=True
    
    def add_element(self, title, details='', alarm_target_time=None,completed=False):
        new_element = Task(title, details, alarm_target_time, completed)
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