# Monty Python Game & Simulator
# A Probability Project created by Jack Tobia

import random
import time

games = 0
wins = 0

#  Prints a graphic of a goat
def print_goat():
    print("(_(")
    print("/_/'_____/)")
    print("\"  |      |")
    print("   |\"\"\"\"\"\"|")

#  Prints a graphic of a car
def print_car():
    print("        _______")
    print("       //  ||\\ \\")
    print(" _____//___||_\\ \\___")
    print(" )  _          _    \\")
    print(" |_/ \\________/ \\___|")
    print("   \\_/        \\_/")

#  Ensures that an inputted message is an integer
def validate_int(message):
    try:
        return int(input(message))
    except ValueError:
        print("Pick a positive integer, please.")
        return validate_int(message)

#  The user's final decision in the game, which determines if they win or not
def final_choice(select, car):
    print("Time for your final decision...")
    time.sleep(1)
    switch = input(
        f"Do you want to switch from door {select}? (yes/no): ").lower()
    while switch not in ["yes", "no"]:
        switch = input("Please enter 'yes' or 'no': ").lower()
    win = False
    if switch == "yes" and select != car:
            win = True
    elif switch == "no" and select == car:
            win = True
    print("Okay...")
    time.sleep(0.5)
    seconds = 3
    while seconds > 0:
        print(seconds)
        time.sleep(1)  # Wait for 1 second
        seconds -= 1
    if win:
        print_car()
        print("Congratulations! You've won the car!")
        return 1
    print_goat()
    print("Sorry, it's a goat.")
    time.sleep(1)
    print(f"The car was behind door {car}!")
    return 0

#  Simulates a Monty Hall Problem game recursively using a given strategy
def sim_game(select, doors, behind_door, car, switch, strat):
    reveal = random.randint(1, doors)
    while behind_door[reveal] != 0 or reveal == select:
        reveal = random.randint(1, doors)
    behind_door[reveal] = 2
    if strat == 4:
        switch = random.choice([True, False])
    if behind_door.count(0) == 1:
        if strat == 2 or strat == 3:
            switch = True
        if switch and select != car:
            return 1
        elif not switch and select == car:
            return 1
        return 0
    if strat == 2:
        switch = True
    if switch:
        available = []
        for i in range(1, doors + 1):
            if behind_door[i] == 0 or i == car:
                available.append(i)
        select = random.randint(1, doors)
        while select not in available:
            select = random.randint(1, doors)
        return sim_game(select, doors, behind_door, car, switch, strat)
    else:
        return sim_game(select, doors, behind_door, car, switch, strat)

#  Recursively makes the play mode function, allows the user to choose doors
def picking_doors(select, doors, behind_door, car):
    reveal = random.randint(1, doors)
    while behind_door[reveal] != 0 or reveal == select:
        reveal = random.randint(1, doors)
    behind_door[reveal] = 2
    print(f"Okay, show us what's behind door number {str(reveal)}!")
    time.sleep(1.2)
    print_goat()
    print("It's a GOAT!")
    time.sleep(1)
    if behind_door.count(0) == 1:
        return final_choice(select, car)
    switch = input("Do you want to switch doors? (yes/no): ").lower()
    while switch not in ["yes", "no"]:
        switch = input("Please enter 'yes' or 'no': ").lower()
    if switch == "yes":
        available = ""
        for i in range(1, doors + 1):
            if behind_door[i] == 0 or i == car:
                available += str(i) + ", "
        available = available[:-2]
        available += ": "
        select = validate_int(
            f"Which door? The doors you can select are {available}")
        while str(select) not in available:
            select = validate_int("Select a valid door number: ")
        return picking_doors(select, doors, behind_door, car)
    else:
        return picking_doors(select, doors, behind_door, car)

#  Starts the game's processes
def play(sim):
    if sim:
        print("WARNING: This simulation can handle a maximum of 996 doors "
              "without crashing.")
    doors = validate_int("How many doors should the game have? ")
    while doors <= 2:
        if doors == 0:
            print("Zero doors?!")
        elif doors == 1:
            print("One door? What fun is that?")
        elif doors == 2:
            print("Go flip a coin!")
        else:
            print("You cannot have negative doors.")
        doors = validate_int("How many doors should the game have? ")
    car = random.randint(1, doors)
    behind_door = [7]  # Add filler at the front so the index == # of door
    for i in range(1, doors + 1):
        if i == car:
            behind_door.append(1)
        else:
            behind_door.append(0)
    if sim:  # Simulation mode
        num_games = validate_int("How many games would you like to simulate? ")
        while num_games <= 0:
            print("Pick a positive integer, please.")
            num_games = validate_int(
                "How many games would you like to simulate? ")
        temp_doors = doors
        temp_bd = behind_door
        temp_car = car
        strats = ["Always Stay", "Always Switch", "Stay but Switch Last",
                  "Random Switching"]
        print("")
        for i in range(4):
            strat_wins = 0
            for j in range(num_games):
                select = random.randint(1, doors)
                strat_wins += sim_game(select, temp_doors, temp_bd, temp_car,
                                       False, i + 1)
                temp_doors = doors
                temp_car = random.randint(1, doors)
                temp_bd = [7]
                for k in range(1, doors + 1):
                    if k == car:
                        temp_bd.append(1)
                    else:
                        temp_bd.append(0)
            print(f"Strategy \"{strats[i]}\" won {strat_wins} out of "
                  f"{num_games} games, which is about "
                  f"{round(float(strat_wins / num_games * 100))}% of games.")
        print("")
    else:  # Play mode
        select = 0
        while select < 1 or select > doors:
            select = validate_int(
                "Pick one door, 1-" + str(doors) + ": ")
        return picking_doors(select, doors, behind_door, car)
    return 0

if __name__ == '__main__':
    print("Welcome to the Monty Hall Game & Simulator!")
    invalid_game = True
    user_played = False
    game_type = input(
        "Enter 'p' to play, 's' to simulate, or 'q' to quit: ").lower()
    while game_type not in ['p', 's', 'q']:
        game_type = input(
            "Enter 'p' to play, 's' to simulate, or 'q' to quit: ").lower()
    while invalid_game:
        play_again = 'u'
        if game_type in ['p', 's', 'q']:
            if game_type == 'q':
                exit(0)
            elif game_type == 'p':
                user_played = True
                games += 1
                wins += play(False)
            else:
                games += 1
                wins += play(True)
            while play_again not in ["yes", "no"]:
                play_again = input("Play again? (yes/no): ").lower()
            if play_again == "yes":
                invalid_game = True
            else:
                invalid_game = False
                if user_played:
                    print(f"You won {wins} out of {games} games!")
