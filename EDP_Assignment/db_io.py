import os
from task_manager import Task

RELATIVE_PY_PATH=os.path.dirname(os.path.abspath(__file__)) # Constant to get current path of the .py file to build relative path

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
        """Database_IO class initialisation. We receive as an argument the referance to our external Element_Manager instance.
        Args:
            el_manager (Element_Manager): The received reference is to ensure that we use only one list        """
        self.database_dir:str = RELATIVE_PY_PATH + '/database' # relative directory + database work directory
        os.makedirs(self.database_dir, exist_ok=True) # Ensure the directory exists, otherwise create it without an error
        self.file_type='.csv' # just incase we want to change the default extention to txt for example
        self.db_file_name:str='db_todo' # database file name
        self.db_file_path:str=os.path.join(self.database_dir,self.db_file_name+self.file_type) # Building database file path with os.path.join function built-in the os library

        self.el_manager = el_manager

    def db_save_file(self,file_path:str=None):
        """This is a public function to save the todo list to the file

        Args:
            file_path (str, optional): Defaults (if none) to self.db_file_path. The path to our file that we're going to write. Parameter is optional because if we able to pass parameter which to which file we want to save, we use predefined database directory, from relative path that has been built in db_file_path        """
        if file_path is None:
            file_path = self.db_file_path
        if self.__write_file(file_path):
            self.is_modified=False

    def db_read_file(self,update_callback:callable,file_path:str=None):
        """The public function inside our Database_IO class is intended to read our database file. We also redefine db_filepath received from the user in case of usage of the Open File function

        Args:
            update_callback (callable): As parameter we receive reference to update the interface function and we call it on succesfull complition of private __read_file function
            file_path (str, optional): Defaults (if none) to self.db_file_path. The path to our file. Parameter is optional because if we don't use this function to open file, we use predefined database directory, from relative path that has been built in db_file_path        """
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
            bool: We return succsessful or not was the function, if not, we don't call an update_interface callback function        """
        try:
            self.el_manager.todo_list=[] # clear list before we refill it with the new read data
            with open(file_path, 'r', encoding="utf-8") as csvfile:
                content = csvfile.read()  # Read the entire file content at once
                lines = content.strip().split('\n')  # Split content into lines
                for line in lines:
                    splitted_data = line.strip().split(',') #strip() cuts the non-printable characters like \n on beginning and end of the string
                    self.el_manager.todo_list.append(Task(splitted_data[0],splitted_data[1],splitted_data[2],safe_cast(splitted_data[3],int,0)))
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
            bool: Rerurn Success of the function        """
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