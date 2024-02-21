import os

def main():
    """Within the scope of our main function, we will call all our procedures from here."""
    main_directory:str = os.path.dirname(os.path.abspath(__file__)) # Receiving the path of .py file to create relative path to Database directory
    directory_path:str=main_directory+'\\database\\'
    is_generate_data=True # Assuming that the clinet requested the data generation
    if is_generate_data: generate_data(directory_path)
# Reading the data
    table_headers={}
    table_headers,modules_data=read_csv_data(directory_path,'modules',table_headers) # Passing the empty list to follow function's structure
    table_headers,tutors_data=read_csv_data(directory_path,'tutors',table_headers)
    table_headers,completed_courses_data=read_csv_data(directory_path,'completed_courses',table_headers)
# Process the data
    try:
        tutors_data=calculation_tutor_earnings(modules_data,tutors_data,completed_courses_data)
        table_headers['tutors'].append('tutor_total_earnings')
    except Exception as ex:
        print(f'Error in Tutors calculation: {ex}')
    try:
        modules_data=calculation_profit_per_module(modules_data,tutors_data,completed_courses_data)
        table_headers['modules'].append('module_total_profit')
    except Exception as ex:
        print(f'Error in Modules calculation: {ex}')
# Display updated tables
    compiled_tutor_string=display_tutor_table(tutors_data)
    compiled_module_string=display_modules_table(modules_data)
# Write the information to documentation directory
    documentation_dir=main_directory+'\\documentation\\'
    write_txt_file(documentation_dir,'compiled_tutor_stats.txt',compiled_tutor_string)
    write_txt_file(documentation_dir,'compiled_module_stats.txt',compiled_module_string)
# Update the tables with new data
    mapped_data = {
        "modules.csv": modules_data,
        "tutors.csv": tutors_data,
        "completed_courses.csv": completed_courses_data}
    write_csv_file(table_headers,mapped_data,directory_path)

def write_txt_file(documentation_dir:str,filename:str,compiled_stats):
    """ This function is used to write a text file with displayed statistics into the documentation_dir folder
        We also do extra checking of the directory, if it doesn't exist, we create the whole path
    Args:
        documentation_dir (str): folder, where text files will be stored
        filename (str): the name of the file with the .txt extension
        compiled_stats (str): string representation of calculated data that we will write in one go
    """
    stats_path=documentation_dir+filename
    try:
        os.makedirs(documentation_dir, exist_ok=True) # Ensure the directory exists, otherwise create it without an error
        with open(stats_path,'w',encoding='utf-8') as file:
            file.write(compiled_stats)
    except Exception as ex:
        print(f'Error in writing txt file {ex}')

def display_tutor_table(tutors_data:list):
    """ The function with specific use of the building and displaying the table of tutors

    Args:
        tutors_data (list): we pass updated tutor_data list to build the table with pre-defined column names

    Returns:
        str: Returning a long string, that contains new line characters in a table format
    """
    compiled_string = '\n'
    header=f"{'Tutor ID':<10} {'Tutor Name':<20} {'Daily Rate':<15} {'Rate P/P':<15} {'Total Ernings':<15}"
    compiled_string+=header+'\n'
    compiled_string+=('-' * len(header))+'\n'
    for line in tutors_data:
        compiled_string += f"{line[0]:<10} {line[1]:<20} €{safe_cast(line[2],float,0.0):<15.2f} x{safe_cast(line[3],float,0.0):<15.2f} €{safe_cast(line[4],float,0.0):<15.2f}\n"
    print(compiled_string)
    return compiled_string

def display_modules_table(modules_data:list):
    """ The function with specific use of building and displaying the table of modules

    Args:
        modules_data (list): we pass updated modules_data list to build the table with pre-defined column names

    Returns:
        str: Returning a long string, that contains new line characters in a table format
    """
    compiled_string = '\n'
    header=f"{'Module ID':<10} {'Module Name':<35} {'Duration Days':<15} {'Price P/P':<15} {'Total Profit':<15}"
    compiled_string+=header+'\n'
    compiled_string+=('-' * len(header))+'\n'
    for line in modules_data:
        compiled_string += f"{line[0]:<10} {line[1]:<35} {safe_cast(line[2],int,0):<15} €{safe_cast(line[3],float,0.0):<15.2f} €{safe_cast(line[4],float,0.0):<15.2f}\n"
    print(compiled_string)
    return compiled_string

def calculation_tutor_earnings(modules_data:list,tutors_data:list,completed_courses_data:list):
    """ With this function, we calculate total earnings per tutor and append the data into related list, in this case it's tutor_data
        Calling this function recommended to add a header name for the extra column.
        To avoid adding the header if an error appears in the function, call the function in try:except block

    Args:
        modules_data (list): list of available modules from the database
        tutors_data (list): list of active tutors from the database
        completed_courses_data (list): list of completed courses from the database

    Returns:
        list: we return the updated tutors_data list as we appended the data into this list
    """
    for tutor in tutors_data:
        tutor_basic_daily_rate=safe_cast(tutor[2],float,0.0)
        tutor_bonus_per_student=safe_cast(tutor[3],float,0.0)
        tutor_total_earnings=0
        for course in completed_courses_data:
            if tutor[0] == course[1]:
                number_of_students = safe_cast(course[3], int,0)
                for module in modules_data:
                    if module[0] == course[2]:
                        duration_days = safe_cast(module[2], int,0)
                        tutor_total_earnings += (duration_days * tutor_basic_daily_rate) + (number_of_students * tutor_bonus_per_student * duration_days)
                        break
        tutor.append(round(tutor_total_earnings,2))
    return tutors_data

def calculation_profit_per_module(modules_data,tutors_data,completed_courses_data):
    """ With this function, we calculate profit per module for the company and append the data into related list, in this case it's tutor_data
        Calling this function recommended to add a header name for the extra column.
        To avoid adding the header if an error appears in the function, call the function in try:except block

    Args:
        modules_data (list): list of available modules from the database
        tutors_data (list): list of active tutors from the database
        completed_courses_data (list): list of completed courses from the database

    Returns:
        list: we return the updated modules_data list as we appended the data into this list
    """
    for module in modules_data:
        module_id = module[0]
        module_price_per_person = safe_cast(module[3],float,0.0)
        module_total_profit = 0
        for course in completed_courses_data:
            if course[2] == module_id:
                tutor_id = course[1]
                number_of_students = safe_cast(course[3],int,0)
                for tutor in tutors_data:
                    if tutor[0] == tutor_id:
                        tutor_daily_rate = safe_cast(tutor[2],float,0.0)
                        tutor_bonus_per_student = safe_cast(tutor[3],float,0.0)
                        total_revenue = module_price_per_person * number_of_students
                        total_cost = tutor_daily_rate * safe_cast(module[2],int,0) + tutor_bonus_per_student * number_of_students
                        module_total_profit += total_revenue - total_cost
                        break
        module.append(round(module_total_profit,2))
    return modules_data

def generate_data(directory_path:str):
    """Based on our assumptions we build pre-defined data before with optional flag in the main function

    Args:
        directory_path (str): Parameter receives a path in a string format of the database directory
    """
    table_headers={
        "modules":['module_id','module_name','duration_days','price_per_person'],
        "tutors":['tutor_id','tutor_name','basic_daily_rate','bonus_per_student'],
        "completed_courses":['course_id','tutor_id','module_id','number_of_students']}
    modules_data = [
        [1, 'Customer Support Provision', 19, 409.48],
        [2, 'Software Development and Design', 8, 247.35],
        [3, 'Web Development', 10, 184.33],
        [4, 'Data and Cyber Security', 13, 495.57],
        [5, 'Software Development Using SQL', 12, 251.41]]
    tutors_data = [
        [1, 'Alex Johnson', 113.5, 1.8],
        [2, 'Chris Lee', 143, 1.3],
        [3, 'Jordan Smith', 149, 1.3],
        [4, 'Taylor Brown', 144.1, 1.9],
        [5, 'Morgan Davis', 84, 2.9]]
    completed_courses_data = [
        [1, 1, 3, 11],
        [2, 1, 1, 15],
        [3, 4, 3, 6],
        [4, 3, 5, 8],
        [5, 5, 4, 17],
        [6, 2, 2, 14],
        [7, 1, 3, 19],
        [8, 5, 1, 9],
        [9, 4, 4, 17],
        [10, 3, 3, 12]]
    mapped_data = {
        "modules.csv": modules_data,
        "tutors.csv": tutors_data,
        "completed_courses.csv": completed_courses_data
        }
    write_csv_file(table_headers,mapped_data,directory_path)

def read_csv_data(directory_path:str,filename:str,table_headers:dict):
    """Reading data from CSV database files, in case if the customer wants to change CSV values manually.

    Args:
        directory_path (str): Parameter receives a path in a string format of the database directory
        filename (str): File name without extension
        table_headers (dict): Receive dictionary for further update if the headers are not the same as pre-defined

    Returns:
        dict: One of parameters we return read headers from each CSV file
        list: List of data to build our data in memory in list representation
    """
    try:
        full_file_path=directory_path+filename+'.csv'
        with open(full_file_path, 'r', encoding="utf-8-sig") as file: # Use UTF-8-Signateure encoding fow reading highly recommended when working with CSV files
            table_headers[filename]=file.readline().strip().split(',')
            data = []
            for line in file:
                splitted_data = line.strip().split(',') #strip() helps get helps cut the non-printable characters like \n on beginning and end of strings
                data.append(splitted_data)
        print(f'Successfully read the file {filename+'.csv'}')
        return table_headers,data
    except Exception as e:
        print(f"Error in reading file: {e}")

def write_csv_file(table_headers:dict,mapped_data:dict,directory_path:str):
    """ Write a CSV file with passed all mapped data, where key the file name.csv and value is a list of data, that we use to write 3 separate files

    Args:
        table_headers (dict): Passing dictionary of headers
        mapped_data (dict): all data, where the key is the file name.csv and value is a list of data
        directory_path (str): a path string to the database directory
    """
    for filename, headers in table_headers.items():
        try: # Even we use the WITH function, write in the try function helps us to catch file errors
            os.makedirs(directory_path, exist_ok=True) # Ensure the directory exists, otherwise create it without an error
            content = ','.join(headers) + '\n' # Starting with the header row
            data_rows = mapped_data[f"{filename}.csv"] # Compile data rows into a single string for each file
            for row in data_rows:
                content += ','.join([str(item) for item in row]) + '\n' # Convert each item to string, join with commas, and add a newline at the end
            file_path = f"{directory_path}{filename}.csv" # Now write the compiled content to the file in one go
            with open(file_path, 'w', encoding='utf-8') as csvfile: # Use UTF-8 encoding is highly recommended when working with CSV files, as differen enviroments have different default encoding parameter.
                csvfile.write(content)
            print(f'Successfully wrote the file {filename+'.csv'}')
        except Exception as e:
            print(f"Error in writing the file: {e}")

def safe_cast(value:str, to_type:type, default=None):
    """This function ensures that we won't get an error during the converting

    Args:
        value (str): String representation of the value that we need to convert
        to_type (type): To what type should we convert (int, float, etc)
        default (any, optional): Any value that the user wants to return if the converting failed. Defaults to None.

    Returns:
        type: converted value to required type
    """
    try:
        return to_type(value)
    except (ValueError, TypeError) as ex:
        print(f"DEBUG: Convertation error - {ex}. Returning defaul value '{default}'.")
        return default

main()