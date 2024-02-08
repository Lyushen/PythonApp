import random 
import pygame as pg
def Day2():
    #RugbyScore()
    #CardGame()
    #CardGame2()
    #Task3()
    SnakeGame()
    
def SnakeGame():
    window=800
    tile_size=50
    range=1
    pg.init()
    screen = pg.display.set_mode((window,window*0.75))
    clock = pg.time.Clock()
    running = True
    player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    while running:
        for event in pg.event.get():
            print(event)
            if event.type == pg.QUIT:
                running = False
        screen.fill('black')
        pg.display.flip()
        pg.draw.rect(screen, "red", pg.Rect(30,30,60,60))

    
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