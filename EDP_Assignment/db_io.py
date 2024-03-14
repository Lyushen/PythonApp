import os
from task_manager import Task

RELATIVE_PY_PATH=os.path.dirname(os.path.abspath(__file__)) # Constant to get the current path of the .py file to build relative path

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
        print(f"DEBUG: Convertation error - {ex}. Returning default value '{default}'.")
        return default

class Database_IO:
    """A separate Database class is made to create some private functions that aim to interact with database files."""
    def __init__(self, el_manager):
        """Database_IO class initialisation. We receive as an argument the reference to our external Element_Manager instance.
        Args:
            el_manager (Element_Manager): The received reference is to ensure that we use only one list        """
        self.database_dir:str = RELATIVE_PY_PATH + '/database' # relative directory + database work directory
        os.makedirs(self.database_dir, exist_ok=True) # Ensure the directory exists, otherwise create it without an error
        self.file_type='.csv' # just in case we want to change the default extension to txt for example
        self.db_file_name:str='db_todo' # database file name
        self.db_file_path:str=os.path.join(self.database_dir,self.db_file_name+self.file_type) # Building database file path with os.path.join function built-in the os library

        self.el_manager = el_manager

    def db_save_file(self,file_path:str=None):
        """This is a public function to save the to-do list to the file

        Args:
            file_path (str, optional): Defaults (if none) to self.db_file_path. The path to our file that we're going to write. The parameter is optional because if we are able to pass the parameter to which file we want to save, we use a predefined database directory, from the relative path that has been built in db_file_path"""
        if file_path is None:
            file_path = self.db_file_path
        if self.__write_file(file_path):
            self.is_modified=False

    def db_read_file(self,update_callback:callable,file_path:str=None):
        """The public function inside our Database_IO class is intended to read our database file. We also redefine db_filepath received from the user in case of usage of the Open File function

        Args:
            update_callback (callable): As a parameter, we receive a reference to update the interface function and we call it on successful completion of the private __read_file function
            file_path (str, optional): Defaults (if none) to self.db_file_path. The path to our file. The parameter is optional because if we don't use this function to open the file, we use a predefined database directory, from the relative path that has been built in db_file_path        """
        if file_path is None:
            file_path = self.db_file_path
        if self.__read_file(file_path):
            if file_path != self.db_file_path:
                self.db_file_path = file_path # redefine the file path 
            update_callback()

    def __read_file(self, file_path: str) -> bool:
        """Private function to read a database file. It skips empty lines, validates 4 data fields in the database CSV file and uses the safe_cast function to safely convert the completed status to an integer

        Args:
            file_path (str): Path to the file that we want to read

        Returns:
            bool: True if the file was successfully read and processed, False otherwise.
        """
        try:
            self.el_manager.todo_list = []  # Clear the list before refilling it with the new read data
            with open(file_path, 'r', encoding="utf-8") as csvfile:
                content = csvfile.read()
                lines = content.strip().split('\n')

                for line_number, line in enumerate(lines, start=1):
                    if not line.strip():  # Skip empty lines
                        continue

                    splitted_data = line.strip().split(',')
                    if len(splitted_data) != 4:  # Validate expected data fields
                        print(f"Skipping line {line_number}: Expected 4 fields, got {len(splitted_data)}")
                        continue

                    try: # Extract and cast data safely
                        title, description, alarm, completed = splitted_data
                        completed = safe_cast(completed, int, 0)  # Ensure priority is an integer, default to 0 if not
                        self.el_manager.todo_list.append(Task(title, description, alarm, completed))
                    except ValueError as ve:
                        print(f"Error processing line {line_number}: {ve}")
                        continue
            return True
        except Exception as ex:
            print(f"Error in reading the file '{file_path}'\n{ex}")
            return False
    
    def __write_file(self, file_path: str, append: bool = False) -> bool:
        """Private function to write to the database file

        Args:
            file_path (str): Path to the file that we want to write to.
            append (bool, optional): Defaults to False. If we want to add data to an existing list, this parameter can be set to True to use append mode instead of write mode.

        Returns:
            bool: True if the file was successfully written, False otherwise.
        """
        try:
            if not self.el_manager.todo_list: # Check for empty list
                print("Warning: Attempting to write an empty to-do list.")
                return False
            content = ''  # Constructing the content string from the todo list
            for el in self.el_manager.todo_list:
                if not hasattr(el, 'title') or not hasattr(el, 'details') or not hasattr(el, 'alarm_target_time') or not hasattr(el, 'completed'): #hasattr function is used to check if an object has an attribute with a specified name. It returns True if the object has the specified attribute
                    print(f"Error: Task object missing required attributes. Skipping task: {el}")
                    continue
                content += f"{el.title},{el.details},{el.alarm_target_time},{0 if el.completed == False else 1}\n" #Store True or False in digits
            if not content.strip():  # If content is empty after processing the list
                print("Error: No valid content to write after processing the todo list.")
                return False
            # Writing the file
            write_or_append_mode = 'a' if append else 'w' 
            with open(file_path, write_or_append_mode, encoding="utf-8") as csvfile:
                csvfile.write(content)
            print(f'Successfully wrote to the file {file_path}')
            self.el_manager.is_modified = False # Reset the modification flag after a successful write
            return True
        except IOError as io_ex:
            print(f"IOError in writing the file '{file_path}': {io_ex}")
            return False
        except Exception as ex:
            print(f"Unexpected error in writing the file '{file_path}': {ex}")
            return False