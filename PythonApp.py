import random 
from random import randrange
import pygame as pg
def main():
    #Day2()
    Day3()
    
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
            var1=AskInRange("Please enter the first number: ",[0,999999])
            var2=AskInRange("Please enter the second number: ",[0,999999])
            operator=AskInRange("Please enter\n1 for (+) addition\n2 for (*) multiplication\n3 for (-) subtraction\n4 for (/) division\n",[1,5])
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
                
            is_exit=AskInRange("Please enter 1 to Continue... and 0 for Exit: ",[0,1])
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
                confirmation = AskQuestion("Would you like to (C)ontinue, (F)inish the order or (E)dit it? ",{"C":"Continue","F":"Finish","E":"Edit"})
            return confirmation
        while True:
            order = AskQuestion("What would you like to order?", item_list)
            if order == "I":
                flavour = AskQuestion("What flavour for the icecream you prefer?", icecream_flavours)
                order_items.append(f"{item_list[order][0]} with {icecream_flavours[flavour]} flavour - ${item_list[order][1]}")
            elif order == "C":
                flavour = AskQuestion("What flavour for the coffee you prefer?", coffee_flavours)
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
                delete_item = AskInRange("Which item number would you like to delete (1 for first item, etc.)? ",[1,len(order_items)])
                deleted_item = order_items.pop(delete_item)
                deleted_price = float(deleted_item.split("€")[-1])
                order_sum -= deleted_price
                print(f"Deleted: {deleted_item}")
                

        print("\nFinal order:")
        for item in order_items:
            print(item)
        print(f"Total sum: €{order_sum:.2f}")
        
    def Task8_ToCelsius():
        var1=AskInRange("Please enter the Temperature° in Fahrenheit: ",[-99999,99999])
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
        minimum_balance=500.0
        balance=0.0
        min_withdraw = 5  # Minimum withdrawal amount set to €5
        #user_init = AskQuestion("Would you like to open an account?")
        #if user_init == 'n':
        #    print('Thank you for visiting our bank. Farewell')
        #    return
        user_account_type = AskQuestion("Would you like to open a (C)urrent Account or (S)avings Account?", {"C": "Current", "S": "Savings"})
        if user_account_type == 'c':
            deposit_sum = AskInRange(f"For Current Account there is a minimum deposit of €{current_opening_minimal}. Please enter the amount:", [current_opening_minimal, 99999999.0])
            balance+=deposit_sum
        else:
            deposit_sum = AskInRange(f"For Savings Account there is a minimum deposit of €{savings_opening_minimal}. Please enter the amount:", [savings_opening_minimal, 99999999.0])
            balance+=deposit_sum
        while True:
            print(f'Your balance is {style("€"+str(balance),"OKGREEN")}')

            action = AskQuestion(f"Would you like to make a {style("Deposit","OKGREEN")} or {style("Withdraw","WARNING")}?", {"D": "Deposit", "W": "Withdraw"})
            print(f"DEBUG: Value of action is {action}")
            if action == 'd':  # Deposit logic
                deposit_sum = AskInRange("Please enter the amount to deposit:", [0.01, 99999999.0])
                balance += deposit_sum
            else:  # Withdraw logic
                if balance - minimum_balance > 5:  # Ensure there's enough balance to withdraw more than €5 and maintain minimum balance
                    available_to_withdraw = balance-minimum_balance  # Calculate how much is available to withdraw after maintaining minimum balance
                    if user_account_type == 'c':  # Current Account
                        max_withdraw = min(current_withdraw_maximum, available_to_withdraw)
                    else:  # Savings Account
                        max_withdraw = min(savings_withdraw_maximum, available_to_withdraw)
                    
                    withdraw_amount = AskInRange(f"Please enter the amount to withdraw (between €{min_withdraw} and €{max_withdraw}):", [min_withdraw, max_withdraw])
                    if withdraw_amount <= max_withdraw:
                        balance -= withdraw_amount
                        print(f"Withdrawed {style("€"+str(withdraw_amount),"FAIL")} successful. New balance: {style("€"+str(balance),"OKGREEN")}")
                    else:
                        print("Withdrawal amount exceeds the allowable limit.")
                else:
                    print("Insufficient funds available for withdrawal, considering the minimum balance requirement.")
            is_continue = AskQuestion("Would you like to (C)ontinue or (E)xit?", {"C": "Continue", "E": "Exit"})
            if is_continue == 'e':
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

def AskInRange(message, range_limits=[1.0, 5.0]):
    while True:
        var1 = input(message + "\n")
        try:
            converted = float(var1)
            if converted >= min(range_limits) and converted <= max(range_limits):
                return converted
            else:
                # Explicitly converting float to str for safe concatenation
                print("Input is out of range, please enter a number between " + str(min(range_limits)) + " and " + str(max(range_limits)) + ".")
        except ValueError:
            print("Invalid input: Please enter a valid number.")

def AskQuestion(message, possible_answers={'Y': 'Yes', 'N': 'No'}):
    options_str = ', '.join([f"({key}) for {value}" for key, value in possible_answers.items()])
    full_message = f"{message} Possible answers are {options_str}."
    possible_answers_lower = {key.lower(): value for key, value in possible_answers.items()}
    while True:
        print(full_message) 
        user_input = input().lower() 
        possible_answers_lower = {key.lower(): value for key, value in possible_answers.items()}
        if user_input in possible_answers_lower:
            for original_key in possible_answers:
                if original_key.lower() == user_input:
                    return original_key.lower()
        else:
            print(f"Incorrect input. Please enter one of the following options: {options_str}")

def style(message, style):
    style_name = style.upper()
    style_attribute = getattr(bcolors, style_name, None)
    str_message=str(message)
    if style_attribute is None:
        return  str_message # Return the original message if the style is not found
    return style_attribute + str_message + bcolors.ENDC

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Day2():
    #RugbyScore()
    #CardGame()
    #CardGame2()
    #Task3()
    #SnakeGame()
    SnakeTwoPlayers()
    
def SnakeGame(): # One Player Snake
    tile_size = 25
    window_width = 800
    window_height = 600
    x_range = (tile_size // 2, window_width - tile_size // 2)
    y_range = (tile_size // 2, window_height - tile_size // 2)
    def get_random_position():
        x_position = randrange(x_range[0], x_range[1], tile_size)
        y_position = randrange(y_range[0], y_range[1], tile_size)
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

def SnakeTwoPlayers():
    tile_size = 25
    window_width = 800
    window_height = 600
    x_range = (tile_size // 2, window_width - tile_size // 2)
    y_range = (tile_size // 2, window_height - tile_size // 2)

    def get_random_position():
        x_position = randrange(x_range[0], x_range[1], tile_size)
        y_position = randrange(y_range[0], y_range[1], tile_size)
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
   
def CardGame():
    cards_not_used = [0]*52
    minumum_cards = 10
    while (len(cards_not_used)-minumum_cards):
        answer = AskHL("Do you think next card will be higher or lower?").lower()
        unused_indexes = [index for index, value in enumerate(cards_not_used) if value == 0]
        if unused_indexes>minumum_cards:
            break
        chosen_index = random.choice(unused_indexes)
        cards_not_used[chosen_index] = 1

        if answer == "h":
            print()

def CardGame2():
    while True:
        deck = generate_deck()
        round_wins = 0
        for _ in range(3):  # Three rounds
            card1 = pick_unused_card(deck)
            print(f"We drawn {card1['card']}")

            answer = AskHL("Do you think the next card will be higher or lower?", ["h", "l"])
            card2 = pick_unused_card(deck)

            print(f"We drawn {card2['card']}")
            guess_correct = (answer == "h" and card1["rank"] < card2["rank"]) or (answer == "l" and card1["rank"] > card2["rank"])

            if guess_correct:
                print("Correct guess!")
                round_wins += 1
            else:
                print("Wrong guess.")

        if round_wins >= 2:
            print("You won the round!")
        else:
            print("You lost the round.")

        play_again = AskHL("Do you want to play another round? (Y)es or (N)o", ["y", "n"])
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

def AskHL(text, possible_answers):
    print(text)
    while True:
        answer = input().lower()
        if answer in possible_answers:
            return answer
        else:
            print("Invalid input. Please try again.")

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