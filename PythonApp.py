import random 
from random import randrange
import pygame as pg
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

Day2()