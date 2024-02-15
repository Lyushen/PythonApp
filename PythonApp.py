
import random 
import pygame as pg
import ExternalFuncs #import my own library
from ExternalFuncs import ask_in_range
from ExternalFuncs import ask_a_question
from ExternalFuncs import style
from ExternalFuncs import extract_keys
from ExternalFuncs import extract_keys_with_numbers
from ExternalFuncs import Timer

import pyodbc
#import mysql connector
import contextlib

def main():
    timer = Timer(1)
    timer.start()
    #Day2()
    #Day3()
    #Day4()
    #Day5()
    Day6()
    timer.stop()
   
def Day6():
    # Assessment Scenario: Given a CSV File containing employee names, departments and daily hours worked for a week, create a programme which calculates the 
    # total workforce effort for the week by department
    # The program should generate a simple text file containing a breakdown by department showing average hours worked, total hours worked and employee with most hours.
    # OrganisationWeeklyTimesheet.csv
    # Employee, Department, Mon, Tue, Wed, Thur, Fri
    # John Doe, Management, 8, 7.5, 8, 6, 5
    # Jane Doe, Management, 7.5, 8, 6, 5, 8
    # Jack Smith, Marketing, 6, 6, 6, 6, 6
    # Mary Smith, Engineering, 7, 7,7,7,2
    # Alex Murphy, Engineering, 7.5, 6.5, 7, 8, 6
    # Organisation Department Totals.txt
    # Department Engineering
    # Total Hours Worked by Department: 65 Hours
    # Average Hours Worked by Employees: 32.5 Hours
    # Employee with Most Hours Worked: Alex Murphy
    # ...cont'd.
    file_name='SD-TA-001-A_OrganisationWeeklyTimesheet'
    work_director='IOFiles\\'
    input_csv_fpath=work_director+file_name+'.csv'
    output_csv_fpath=work_director+'output_'+file_name+'.csv'
    output_txt_fpath=work_director+file_name+'.txt'
    #print(input_csv_file_path)
    
    headers,data=read_file(input_csv_fpath)
    #display(headers,data)
    #headers,data=to_int_days(headers,data)
    
    # for row in data:
    #     if row['EmployeeName'] == 'John Smith':
    #         row['EmployeeName'] = 'John Tobin'  # Modify the John Smith's name
    
    compiled_txt=compile_the_data_optimized(headers,data)
    print(compiled_txt)
    compiled_txt=compile_the_data(headers,data)
    print(compiled_txt)
    #write_csv_file(output_csv_fpath,headers,data)

def compile_the_data(headers,data):
    print('Not Optimized version')
    timer2 = Timer(2)
    timer2.start()
    compiled_txt=''
    sum_headers = headers[2:]
    unique_departments = sorted({row['Department'] for row in data})
    for department in unique_departments:
        compiled_txt+=f'Department:\t\t\t{department}\n'
        total_hours=0
        top_hours=0
        top_name=''
        counter=0
        
        for row in data: 
            if row['Department'] == department:
                employee_total_hours=0
                for header in sum_headers:
                    temp_total = safe_cast(row[header], float, 0)
                    total_hours += temp_total
                    employee_total_hours += temp_total
                if employee_total_hours > top_hours:
                    top_hours = employee_total_hours
                    top_name = row['EmployeeName']
                counter+=1

        avg_hours = (total_hours / counter) if total_hours else 0  
        compiled_txt+=f'Total Hours Worked by Department:\t{total_hours}\n'
        compiled_txt+=f'Average Hours Worked by Employees:\t{avg_hours}\n'
        compiled_txt+=f'Employee with Most Hours Worked:\t{top_name} with {top_hours} hours\n'
    timer2.stop()
    return compiled_txt

def compile_the_data_optimized(headers, data):
    print('Optimized version')
    timer3 = Timer(3)
    timer3.start()
    compiled_txt = ''
    department_info = {}
    sum_headers = headers[2:]  # Do this once to avoid repetition

    # Single iteration to collect data
    for row in data:
        department = row['Department']
        if department not in department_info:
            department_info[department] = {'total_hours': 0, 'employee_hours': [], 'counter': 0}

        employee_total_hours = sum(safe_cast(row[header], float, 0) for header in sum_headers)
        department_info[department]['total_hours']+=employee_total_hours
        department_info[department]['employee_hours'].append((row['EmployeeName'], employee_total_hours))
        department_info[department]['counter']+=1

    # Process collected data
    for department in sorted(department_info):
        info = department_info[department]
        top_name, top_hours = max(info['employee_hours'], key=lambda x: x[1], default=("N/A", 0))
        avg_hours = info['total_hours'] / info['counter'] if info['counter'] else 0

        compiled_txt += f'Department:\t\t\t{department}\n'
        compiled_txt += f'Total Hours Worked by Department:\t{info['total_hours']}\n'
        compiled_txt += f'Average Hours Worked by Employees:\t{avg_hours}\n'
        compiled_txt += f'Employee with Most Hours Worked:\t{top_name} with {top_hours} hours\n'
    timer3.stop()
    return compiled_txt
    
def to_int_days(headers,data):
    day_to_int = {day: index for index, day in enumerate(headers, start=3)}
    converted_data = []
    for row in data:
        converted_row = {key: (day_to_int[value] if key in day_to_int else value) for key, value in row.items()}
        converted_data.append(converted_row)
    return converted_data

def display(headers,data):
    print(headers)
    for row in data:
        print(row)
            
def read_file(file_path):
    data = []
    headers = []
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()  # Read the entire file content at once
            lines = content.strip().split('\n')  # Split content into lines
            headers = lines[0].split(',')  # Extract headers
            for line in lines[1:]:
                values = line.split(',')
                row_dict = dict(zip(headers, values))
                data.append(row_dict)
    except Exception as e:
        print(f"Error in reading the file: {e}")
    return headers, data

def write_csv_file(output_csv_file_path, headers, data):
    try:
        compiled_string = ','.join(headers) + '\n'
        for row_dict in data:
            row_values = [str(row_dict.get(header, "")) for header in headers]  # Get values in header order, safely handling missing keys
            compiled_string += ','.join(row_values) + '\n'
        with open(output_csv_file_path, 'w') as file:
            file.write(compiled_string)
    except Exception as e:
        print(f"Error in writing the file: {e}")
 
def Day5():
    # Create an application for ABC company, database ABC_Company and a table Employee 
    # Name, Address, Email, Salary, Department
    # in the company there are HR, Finance, IT, Sales and each department has 5 employees
    # 1. Show a List of Employees working in IT department
    # 2. Show the Name, Address and Email of employee from Dublin
    # 3. Show the Name, Department and Salary in the 25-50k range
    # 4. Update the department name of employee from Sales to Finance
    # 5. Delete 1 Employee from the Sales departments
    driver='{SQL Server}'
    server='localhost/localdb'
    server3='localhost'
    server2='localdb'
    database='ONAssignmentB'
    connection_string=f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={database}" #;Uid={username};Pwd={password}
    #db_con = pyodbc.connect(driver=driver, server=server, database=database,trusted_connection='yes')
    #cursor = db_con.cursor()
    execute_code="SELECT * FROM Customer"
    
    @contextlib.contextmanager
    def use_connection():
        try:
            connection = pyodbc.connect(connection_string)
            yield connection
        except Exception as e:
            print(f"Error connecting to LocalDB: {e}")
        finally:
            if connection:
                connection.close()
    # Example usage
    with use_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(execute_code)
        rows = cursor.fetchall()
        print(rows)
    print()
    
def Day4():
    def Task1():
        my_list=[1,2,3,4,5]
        print("Print element 2nd element from my_list[2]"+my_list[2])
        print("Print element on -1 index from my_list[-1]"+my_list[-1])
        print("Print len() of my_list"+len(my_list))
    
    def Task2():
        user_list=[]
        itterations = 10
        var=0   
        for i in range(itterations):
            var = ask_in_range(f"Please input the {i+1} value: ", [-99999, 99999])
            if var % 2 != 0:
                value_to_append = var + 1
            else:
                value_to_append = var
            user_list.append(value_to_append)
        user_list.sort()
        print(user_list)
        
    def Task3():
        user_list=[]
        itterations = 10
        for i in range(itterations):
            user_list.append(ask_in_range(f"Please input the {i+1} value", [-99999, 99999],int))
        #user_list.sort()
        user_list2,user_list3=user_list,user_list
        for x,i in enumerate(user_list):
            for y,j in enumerate(user_list):
                if i<j:
                    user_list[x],user_list[y]=user_list[y],user_list[x] #without temp var
        for x,i in enumerate(user_list2): #my version
            for y,j in enumerate(user_list2):
                if i<j:
                    temp_value=user_list2[x]
                    user_list2[x]=user_list2[y]
                    user_list2[y]=temp_value
        for i in range(len(user_list3)): #teacher's version
           for j in range(len(user_list3)):
               if user_list3[i]<user_list3[j]:
                   temp_value=user_list3[i]
                   user_list3[i]=user_list3[j]
                   user_list3[j]=temp_value
        print(str(user_list)+"\n"+str(user_list2)+"\n"+str(user_list3))
    
    def Task4(): #Sum and average
        user_list=[]
        itterations = 10
        for i in range(itterations):
            user_list.append(ask_in_range(f"Please input the {i+1} value", [-99999, 99999],int))
        sum=0
        for i in user_list:
            sum+=i
        # sum=sum(user_list)
        # average=avr
        average=sum/len(user_list)
        print(f"User_list: {user_list}\nAverage: {str(average)}\nSum: {str(sum)}")
        
    def Task5(): #Dictionary Practice
        dict_one={
            "name":"abc",
            "course":"oop"
        }
        print(dict_one)
        dict_one["course"]="OOP"
        print(dict_one)
        dict_one["email"]="abc@abc.com"
        print(dict_one.keys())
        new_name={"name":"def"}
        dict_one.update(new_name)
        print(dict_one)
        
    def Task6(): #sale tax
        # Write a program wich would calculate the sales tax on two products by the name of Toothpaste and Shampoo.
        # First the user would be asked for the product type.
        # Once the user selects the product then ask them about the price of the product.
        # For the product, if the price is less than 50, clculate 3% sales tax, more than 50 and less than 100 then calculate 5% sales tax on the product.
        # If price is more than 100, calculate 10% sale tax.
        # Then display the sales tax to the user and total amount including sale tax
        ## give user an option if user wants to buy an other product
        
        tax_low_rate=3
        tax_mid_rate=5
        tax_high_rate=10
        CUR="€"
        products={
            "Toothpaste":55.25,
            "Shampoo":43.11,
            "Toilet Paper":150
        }
        order_list={}
        total_sum=0.00
        while True:
            order_list.update(order_a_product("Please select the product",products))
            print("\nYour current order includes:")
            for order in order_list:
                for key in order:
                    print(order[key]['Formatted'])
            continue_finish_or_edit=ask_a_question("Would you like to (C)ontinue, (F)inish the order or (E)dit it? ",{"C":"Continue","F":"Finish","E":"Edit"})
            if continue_finish_or_edit=="f":
                print("\nFinal order:")
                for order in order_list:
                    for key in order:
                        print(order[key]['Formatted'])
                        total_sum += order[key]['Price']
                print(f"Total sum: €{total_sum:.2f}")
                return
            elif continue_finish_or_edit=="e":
                order_list=edit_order(order_list)
            else:
                break

        def edit_order(user_orders):
            print("Current order:")
            for order in user_orders:
                for key in order:
                    print(order[key]['Formatted'])
            position_to_remove = ask_in_range("Enter the position number of the product you want to delete: ",[1,len(user_orders)+1])
            del user_orders[position_to_remove - 1]
            return user_orders
                    
        def order_a_product(message, products):
            # Generate a list of formatted product strings for display
            options_list = [f"{idx + 1}. {name} - {price}" for idx, (name, price) in enumerate(products.items())]
            options_str = '\n'.join(options_list)
            full_message = f"{message}\nPossible options are:\n{options_str}"

            while True:
                print(full_message)
                user_input = input("Enter the number of your choice: ")
                try:
                    selected_index = int(user_input) - 1  # Convert to zero-based index
                    if 0 <= selected_index < len(products):
                        selected_product = list(products.items())[selected_index]
                        return {
                            str(selected_index + 1): {
                                "Name": selected_product[0],
                                "Price": selected_product[1],
                                "Formatted": f"{selected_index + 1}. {selected_product[0]} - {selected_product[1]}"
                            }
                        }
                    else:
                        print("Selection out of range. Please enter a valid option number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
    
    def Task7():
        # write a program in which a father wants to know the grate of his two sons. Ask the user for the marks.
        # 95-100 - A+
        # 90-94 - A
        # 85-89 - A-
        sons_grades={}
        amount_of_sons=ask_in_range("How many sons do you have?",[1,99],int)
        for i in range(amount_of_sons):
            sons_grades.update({f"Son {i}":ask_in_range(f"Please enther the grade for the Son {i}:",[0,100],int)})
        print(sons_grades)
        for name, grade in sons_grades.items():
            print(f"For {name}, the grade is {grade}.")
                

        print()
    def get_grade_category(score):
        grades=["A+","A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F+", "F", "F-","F--"]
        scale=100
        index = (score / (scale / len(grades)))
        index = min(index, len(grades) - 1)
        return grades[index]
    #Task1()
    #Task2()
    #Task3()
    #Task4()
    #Task5()
    #Task6()
    Task7()
    
def Day3():   
    def Task1():
        for i in range(1,5):
            for j in range (i):
                print("*",end="")
            print("")
    
    def Task2():
        fruits=["Apple","Orange","Mango"]
        for fruit in fruits:
            print(fruit)    
    
    def Task3():
        ocount,ecount=0,0
        for i in range(1,5):
            if 1%2==0:
                ecount+=1
            else:
                ccount+=1
        print("Even Numbers are: ",ecount)
        print("Odd Numbers are:",ocount)
        
    def Task4():
        number = input("Enter the number: ")
        int_input = safe_cast(number,int,0)
        for i in range (1,int_input+1):
            print(f"{int_input}*{i}={int_input*i}")
    
    def Task4Teacher():
        var=input("Enter the number: ")
        for i in range(1,int(var)+1):
            print(f"{var} * {i} = {int(var)*i}")
    
    def Task5():
        var1=input("Enter the number: ")
        var2=input("Enter until what you want to multiply: ")
        int_var1=safe_cast(var1,int,0)
        int_var2=safe_cast(var2,int,0)
        for i in range(1,int_var2+1):
            print(f"{int_var1}*{i}={int_var1*i}")
    
    def Task6_SimpleCalc():
        while True:
            var1=ask_in_range("Please enter the first number: ",[0,999999])
            var2=ask_in_range("Please enter the second number: ",[0,999999])
            operator=ask_in_range("Please enter\n1 for (+) addition\n2 for (*) multiplication\n3 for (-) subtraction\n4 for (/) division\n",[1,5])
            operators={
                1:"+",
                2:"*",
                3:"-",
                4:"/"
            }
            operation_str = f"{var1} {operators[operator]} {var2}"
            try:
                result = eval(operation_str)
                print(f"Calculation of {operation_str} = {result}")
            except ZeroDivisionError:
                print("Error: Division by zero is not allowed.")
            except Exception as e:  # Catches other exceptions including NameError, SyntaxError, etc.
                print(f"An error occurred: {e}")
                
            is_exit=ask_in_range("Please enter 1 to Continue... and 0 for Exit: ",[0,1])
            if (is_exit==0):
                break
            
    def Task7_Cafe():
        item_list={         "I":["Icecream",5.25],
                            "C":["Coffee",2.25],
                            "S":["Shake",3.25]}
        icecream_flavours={ "S":"Strawberry",
                            "C":"Chocolate",
                            "V":"Vanilla"}
        coffee_flavours={   "S":"Strawberry",
                            "C":"Chocolate",
                            "V":"Vanilla"}
        order_sum=0.0
        order_items = []  
        def ConfirmOrder(order_items,prnt='no'):
            print("\nYour current order includes:")
            for idx, item in enumerate(order_items, start=1):
                print(f"{idx}. {item}")
            if prnt=='no':
                confirmation = ask_a_question("Would you like to (C)ontinue, (F)inish the order or (E)dit it? ",{"C":"Continue","F":"Finish","E":"Edit"})
            return confirmation
        while True:
            order = ask_a_question("What would you like to order?", item_list)
            if order == "I":
                flavour = ask_a_question("What flavour for the icecream you prefer?", icecream_flavours)
                order_items.append(f"{item_list[order][0]} with {icecream_flavours[flavour]} flavour - ${item_list[order][1]}")
            elif order == "C":
                flavour = ask_a_question("What flavour for the coffee you prefer?", coffee_flavours)
                order_items.append(f"{item_list[order][0]} with {coffee_flavours[flavour]} flavour - ${item_list[order][1]}")
            else:
                flavour = "None"
                order_items.append(f"{item_list[order][0]} - ${item_list[order][1]}")
            order_sum += item_list[order][1]
            confirmation = ConfirmOrder(order_items)
            if confirmation == 'c':
                break
            elif confirmation == "e":
                ConfirmOrder(order_items,'yes')
                delete_item = ask_in_range("Which item number would you like to delete (1 for first item, etc.)? ",[1,len(order_items)])
                deleted_item = order_items.pop(delete_item)
                deleted_price = float(deleted_item.split("€")[-1])
                order_sum -= deleted_price
                print(f"Deleted: {deleted_item}")
                

        print("\nFinal order:")
        for item in order_items:
            print(item)
        print(f"Total sum: €{order_sum:.2f}")
        
    def Task8_ToCelsius():
        var1=ask_in_range("Please enter the Temperature° in Fahrenheit: ",[-99999,99999])
        try:
            celcius= (var1 - 32) * 5 / 9
            print(f"{round(var1,1)}° Fahrenheit is {round(celcius,1)}°")
        except Exception as e:
            print(f"An error occurred: {e}")
               
    def Task9_Banking():
        current_opening_minimal=100.0
        savings_opening_minimal=500.0
        current_withdraw_maximum=1000.0
        savings_withdraw_maximum=2500.0
        min_withdraw = 5  # Minimum withdrawal amount €5
        minimum_balance=500.0
        balance=0.00
        #if AskQuestion("Would you like to open a Bank Account?") == 'n':
        #    print('Thank you for visiting our bank. Farewell')
        #    return
        current_or_savings_account = ask_a_question("Would you like to open a (C)urrent Account or (S)avings Account?", {"C": "Current", "S": "Savings"})
        if current_or_savings_account == 'c':
            balance+= ask_in_range(f"For Current Account there is a minimum deposit of €{current_opening_minimal}. Please enter the amount:", [current_opening_minimal, 99999999.0])
        else:
            balance+= ask_in_range(f"For Savings Account there is a minimum deposit of €{savings_opening_minimal}. Please enter the amount:", [savings_opening_minimal, 99999999.0])
        while True:
            print(f'Your balance is {style("€"+str(balance),"OKGREEN")}')
            deposit_or_withdraw = ask_a_question(f"Would you like to make a {style("Deposit","OKGREEN")} or {style("Withdraw","WARNING")}?", {"D": "Deposit", "W": "Withdraw"})
            #print(f"DEBUG: Value of action is {action}")
            if deposit_or_withdraw == 'd':  # Deposit logic
                deposit_sum = ask_in_range("Please enter the amount to deposit:", [0.01, 99999999.0])
                balance += deposit_sum
            else:  # Withdraw logic
                if balance - minimum_balance > 5:  # Ensure there's enough balance to withdraw more than €5 and maintain minimum balance
                    available_to_withdraw = balance-minimum_balance  # Calculate how much is available to withdraw after maintaining minimum balance
                    if current_or_savings_account == 'c':  # Current Account
                        max_withdraw = min(current_withdraw_maximum, available_to_withdraw)
                    else:  # Savings Account
                        max_withdraw = min(savings_withdraw_maximum, available_to_withdraw)
                    
                    withdraw_amount = ask_in_range(f"Please enter the amount to withdraw (between €{min_withdraw} and €{max_withdraw}):", [min_withdraw, max_withdraw])
                    if withdraw_amount <= max_withdraw:
                        balance -= withdraw_amount
                        print(f"{style("Withdrawed €-"+str(withdraw_amount)+" successfully","OKGREEN")}. New balance: {style("€"+str(balance),"OKGREEN")}")
                    else:
                        print(style("Withdrawal amount exceeds the allowable limit.","FAIL"))
                else:
                    if current_or_savings_account == 'c':
                        print(style(f"Insufficient funds available for withdrawal, considering the minimum balance for Current Account is €{minimum_balance}. Your balance: {style("€"+str(balance),"OKGREEN")}","FAIL"))
                    else:
                        print(style(f"Insufficient funds available for withdrawal, considering the minimum balance for Savings Account is €{minimum_balance}. Your balance: {style("€"+str(balance),"OKGREEN")}","FAIL"))
            if ask_a_question("Would you like to (C)ontinue or (E)xit?", {"C": "Continue", "E": "Exit"}) == 'e':
                print(f"Final balance: {style("€"+str(balance),"OKGREEN")}")
                break

    #Task1()
    #Task2()
    #Task3()
    #Task4()
    #Task4Teacher()
    #Task5()
    #Task6_SimpleCalc()
    #Task7_Cafe()
    #Task8_ToCelsius()
    Task9_Banking()

def Day2():
    #RugbyScore()
    #CardGame()
    #CardGame2()
    #Task3()
    #SnakeGame()
    snake_for_two_players()
    
def snake_game(): # One Player Snake
    tile_size = 25
    window_width = 800
    window_height = 600
    x_range = (tile_size // 2, window_width - tile_size // 2)
    y_range = (tile_size // 2, window_height - tile_size // 2)
    def get_random_position():
        x_position = random.randrange(x_range[0], x_range[1], tile_size)
        y_position = random.randrange(y_range[0], y_range[1], tile_size)
        return [x_position, y_position]
    snake = pg.rect.Rect([0,0,tile_size-2,tile_size-2])
    snake.center=get_random_position()
    length = 1
    snake_dir=(0,0)
    time,time_step=0,110
    segments = [snake.copy()]
    food=snake.copy()
    food.center=get_random_position()
    pg.init()
    screen = pg.display.set_mode((window_width,window_height))
    clock = pg.time.Clock()
    running = True
    prev_cords_print=None
    dirs={pg.K_w:1,pg.K_s:1,pg.K_a:1,pg.K_d:1}

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_w and dirs[pg.K_w]:
                    snake_dir=(0,-tile_size)
                    dirs={pg.K_w:1,pg.K_s:0,pg.K_a:1,pg.K_d:1}
                if event.key==pg.K_s and dirs[pg.K_s]:
                    snake_dir=(0,tile_size)
                    dirs={pg.K_w:0,pg.K_s:1,pg.K_a:1,pg.K_d:1}
                if event.key==pg.K_a and dirs[pg.K_a]:
                    snake_dir=(-tile_size,0)
                    dirs={pg.K_w:1,pg.K_s:1,pg.K_a:1,pg.K_d:0}
                if event.key==pg.K_d and dirs[pg.K_d]:
                    snake_dir=(tile_size,0)
                    dirs={pg.K_w:1,pg.K_s:1,pg.K_a:0,pg.K_d:1}
                    
        screen.fill('black')
        # selfcollision
        self_eating = pg.Rect.collidelist(snake,segments[:-1])!=-1
        # border checking and restart the game if hit -> changed the restart only on selfcollision
        if self_eating:
            snake.center, food.center = get_random_position(),get_random_position()
            length,snake_dir=1,(0,0)
            segments = [snake.copy()]
        # eat food
        if snake.colliderect(food):
            food.center = get_random_position()  # Ensure this is aligned with the grid
            length += 1
        pg.draw.rect(screen,'red',food) #draw food
        [pg.draw.rect(screen,'green',segment) for segment in segments] #draw snake
        time_now=pg.time.get_ticks()
        # Action Tick
        if time_now-time>time_step:
            time=time_now
            snake.move_ip(snake_dir)
            # Wrapping logic
            if snake.left < 0:
                snake.right = window_width
            elif snake.right > window_width:
                snake.left = 0
            if snake.top < 0:
                snake.bottom = window_height
            elif snake.bottom > window_height:
                snake.top = 0
            # After updating the snake's position, add the new position to segments
            segments.append(snake.copy())
            segments = segments[-length:]
            # Print coords of the snake and , if they were changed
            cords=f"Snake: {snake.center} Food: {food.center}"
            if (prev_cords_print!=cords):
                print(cords)
                prev_cords_print=cords
        
        pg.display.flip()
        clock.tick(60) # Consistent 60 fps

def snake_for_two_players():
    tile_size = 25
    window_width = 800
    window_height = 600
    x_range = (tile_size // 2, window_width - tile_size // 2)
    y_range = (tile_size // 2, window_height - tile_size // 2)

    def get_random_position():
        x_position = random.randrange(x_range[0], x_range[1], tile_size)
        y_position = random.randrange(y_range[0], y_range[1], tile_size)
        return [x_position, y_position]

    # Initialize the first snake
    snake = pg.Rect([0, 0, tile_size - 2, tile_size - 2])
    snake.center = get_random_position()
    length = 1
    snake_dir = (0, 0)
    segments = [snake.copy()]

    # Initialize the second snake
    snake2 = pg.Rect([0, 0, tile_size - 2, tile_size - 2])
    snake2.center = get_random_position()
    length2 = 1
    snake_dir2 = (0, 0)
    segments2 = [snake2.copy()]

    # Initial settings
    food = snake.copy()
    food.center = get_random_position()
    pg.init()
    screen = pg.display.set_mode((window_width, window_height))
    font = pg.font.SysFont('Arial', 24)  # Choose a font and size
    clock = pg.time.Clock()
    running = True
    time_step = 110  # in milliseconds
    last_move_time = pg.time.get_ticks()  # Initialize the last move time
    prev_cords_print=None
    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
    dirs2 = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
    

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                # Controls for the snake 1
                if event.key == pg.K_w and dirs[pg.K_w]:
                    snake_dir = (0, -tile_size)
                    dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_s and dirs[pg.K_s]:
                    snake_dir = (0, tile_size)
                    dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_a and dirs[pg.K_a]:
                    snake_dir = (-tile_size, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
                if event.key == pg.K_d and dirs[pg.K_d]:
                    snake_dir = (tile_size, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
                # Controls for the snake 2
                if event.key == pg.K_UP and dirs2[pg.K_UP]:
                    snake_dir2 = (0, -tile_size)
                    dirs2 = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
                if event.key == pg.K_DOWN and dirs2[pg.K_DOWN]:
                    snake_dir2 = (0, tile_size)
                    dirs2 = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
                if event.key == pg.K_LEFT and dirs2[pg.K_LEFT]:
                    snake_dir2 = (-tile_size, 0)
                    dirs2 = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
                if event.key == pg.K_RIGHT and dirs2[pg.K_RIGHT]:
                    snake_dir2 = (tile_size, 0)
                    dirs2 = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}

        screen.fill('black')
        restart,collision_snake,collision_snake2 = False,False,False
        # Collision and game logic for both snakes
        self_eating = (pg.Rect.collidelist(snake, segments[:-1]) != -1 or pg.Rect.collidelist(snake2, segments2[:-1]) != -1 or snake.colliderect(snake2) or snake2.colliderect(snake))
        if self_eating: restart=True
        # Players collision
        for segment in segments2[1:]:  # Skip the head of the second snake to prevent head-on collisions counting as a loss for both
            if snake.colliderect(segment):
                restart, collision_snake2 = True, True  # If snake 1 hits snake 2, snake 2 wins
        for segment in segments[1:]:  # Skip the head of the first snake for the same reason
            if snake2.colliderect(segment):
                restart, collision_snake = True, True  # If snake 2 hits snake 1, snake 1 wins
        message_to_display = None
        if collision_snake and not collision_snake2:  # Only snake 1 wins
            message_to_display = "Player Two (Blue) Wins!"
        elif collision_snake2 and not collision_snake:  # Only snake 2 wins
            message_to_display = "Player One (Green) Wins!"
        elif collision_snake and collision_snake2:  # If both collide with each other simultaneously
            message_to_display = "It's a Draw!"  # Or handle according to your game's rules
        if message_to_display:
            print(message_to_display)
        if (restart):
            snake.center, snake2.center, food.center = get_random_position(), get_random_position(), get_random_position()
            length, length2 = 1, 1
            snake_dir, snake_dir2 = (0, 0), (0, 0)
            segments, segments2 = [snake.copy()], [snake2.copy()]
        # Food eating logic for both snakes
        if snake.colliderect(food):
            food.center = get_random_position()
            length += 1
        if snake2.colliderect(food):
            food.center = get_random_position()
            length2 += 1

        time_now = pg.time.get_ticks()
        time_step = 110
        # Action tick for the first snake
        if time_now - last_move_time > time_step:
            last_move_time = time_now
            snake.move_ip(snake_dir)
            snake2.move_ip(snake_dir2)
            # Wrapping logic for both snakes
            for s in [snake, snake2]:
                if s.left < 0: s.right = window_width
                elif s.right > window_width: s.left = 0
                if s.top < 0: s.bottom = window_height
                elif s.bottom > window_height: s.top = 0
            segments.append(snake.copy())
            segments = segments[-length:]
            segments2.append(snake2.copy())
            segments2 = segments2[-length2:]
             # Print coords of the snake and , if they were changed
            cords=f"P1: {snake.center} P2:{snake2.center} F:{food.center}"
            if (prev_cords_print!=cords):
                print(cords)
                prev_cords_print=cords
            
            
        pg.draw.rect(screen, 'red', food)  # Draw food
        [pg.draw.rect(screen, 'green', segment) for segment in segments]  # Draw first snake
        [pg.draw.rect(screen, 'blue', segment) for segment in segments2]  # Draw second snake

        pg.display.flip()
        clock.tick(60)  # Consistent 60 fps
    
def Task3(): #ListWork
    my_list = [0,1,2,3,4,5,6,7,8,9]
    print(f"Pure my_list is\n\t{my_list}")
    print(f"\tmy_list[:]\n\t\t{my_list[:]}")
    print(f"\tmy_list[2:6]\n\t\t{my_list[2:6]}")
    print(f"\tmy_list[:4]\n\t\t{my_list[:4]}")
    print(f"\tmy_list[5:]\n\t\t{my_list[5:]}")
    print("negative list range")
    print(f"\tmy_list[-3:]\n\t\t{my_list[-3:]}")
    print(f"\tmy_list[-3:] Returns last 3\n\t\t{my_list[:-2]}")
    print("stepping in my_list")
    print(f"\tmy_list[::2]\n\t\t{my_list[::2]}")
    print(f"\tmy_list[::-1]\n\t\t{my_list[::-1]}")
    my_string="Hello Python"
    print(f"reverse the string '{my_string}'")
    print(f"\tmy_string[::-1]\n\t\t{my_string[::-1]}")
   
def card_game():
    cards_not_used = [0]*52
    minumum_cards = 10
    while (len(cards_not_used)-minumum_cards):
        higher_or_lower = ask_a_question("Do you think next card will be higher or lower?",{'H':'Higher','L':'Lower'})
        unused_indexes = [index for index, value in enumerate(cards_not_used) if value == 0]
        if unused_indexes>minumum_cards:
            break
        chosen_index = random.choice(unused_indexes)
        cards_not_used[chosen_index] = 1

        if higher_or_lower == "h":
            print()

def card_game_v2():
    while True:
        deck = generate_deck()
        round_wins = 0
        for _ in range(3):  # Three rounds
            card1 = pick_unused_card(deck)
            print(f"We drawn {card1['card']}")

            higher_or_lower = ask_a_question("Do you think next card will be higher or lower?",{'H':'Higher','L':'Lower'})
            card2 = pick_unused_card(deck)

            print(f"We drawn {card2['card']}")
            guess_correct = (higher_or_lower == "h" and card1["rank"] < card2["rank"]) or (higher_or_lower == "l" and card1["rank"] > card2["rank"])

            if guess_correct:
                print("Correct guess!")
                round_wins += 1
            else:
                print("Wrong guess.")

        if round_wins >= 2:
            print("You won the round!")
        else:
            print("You lost the round.")

        play_again = ask_a_question("Do you want to play another round? (Y)es or (N)o", {'H':'Higher','L':'Lower'})
        if play_again == "n":
            break

def generate_deck():
    suits = ['♥', '♦', '♠', '♣']  # Hearts, Diamonds, Spades, Clubs
    ranks = {
        '2': 2, '3': 3, '4': 4, '5': 5,
        '6': 6, '7': 7, '8': 8, '9': 9,
        '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    deck = [
        {"card": rank + suit, "used": 0, "rank": ranks[rank]} 
        for suit in suits
        for rank in ranks
    ]
    return deck

def pick_unused_card(deck):
    unused_indexes = [index for index, card in enumerate(deck) if card["used"] == 0]
    if len(unused_indexes) < 10:
        print("There are less than 10 cards left! Regenerating deck.")
        return generate_deck()
    chosen_index = random.choice(unused_indexes)
    deck[chosen_index]["used"] = 1
    return deck[chosen_index]

def RugbyScore():
    file_name= "rugby_tournament_scores"
    file_path = file_name+".csv"
    file_to_write = file_name+".txt"
    data=ReadFile(file_path)
    compiledString = ProcessData(data) #skip the header
    print(compiledString)
    WriteFile(file_to_write,compiledString)

def ProcessData(data):
    headers=data[0]
    dataList=data[1:]
    #countries = set(country for _, country, _ in dataList) # instead of hardcoding contruies, we create unique list from read contry Data column
    countries = ["England","France","Ireland","Italy","Scotland","Wales"]
    country_totals = [0] * 6
    highest_scores = [0] * 6
    players = [""] * 6
    compiledString = ""

    for i in range(len(dataList)):
        data_fields = dataList[i].split(",")
        total_score = 0
        country_index = countries.index(data_fields[2])
        for j in range(3, 8):
            total_score += safe_cast(data_fields[j], int, 0)
        country_totals[country_index] += total_score
        if total_score > highest_scores[country_index]:
            highest_scores[country_index] = total_score
            players[country_index] = f"{data_fields[0]} {data_fields[1]}" 
            
    for i in range(len(countries)):
        compiledString += f"### {countries[i]}: ###\n\tTotal Score: {country_totals[i]}\n\tHighest Score: {players[i]} scored {highest_scores[i]}\n"
    return compiledString

def ReadFile(path):
    try:
        with open(path, 'r') as f:
            data = f.readlines()
        return data
    except (ValueError, TypeError):
        return []

def WriteFile(path, text):
    try:
        with open(path, "w") as f:
            f.write(text)
    except (ValueError, TypeError):
        return []

def safe_cast(value, to_type, default=None):
    try:
        return to_type(value)
    except (ValueError, TypeError):
        return default

main()