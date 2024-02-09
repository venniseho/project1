"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""

# Note: You may add in other import statements here as needed
from game_data import BlockedOrHallway, World, Item, Location, Player, Usable_Item
from typing import Optional, Any
import random


# Note: You may add helper functions, classes, etc. here as needed

def move(p: Player, d: str, w: World) -> None:
    """Given a direction (N, S, W, E), update the player's location in that direction given the move is valid
    """
    direction = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}
    new_x = p.x + direction[d][0]
    new_y = p.y + direction[d][1]
    if not is_valid_move(p, d, w):
        print("Invalid, this square is unaccessible")
        return

    elif new_x == 0 and new_y == 0 and "Room Key" not in {item.name for item in p.inventory}:
        print("Your room is locked. Your room key is not on you but you remember you left it at chestnut somewhere....")
        return

    else:
        p.x = new_x
        p.y = new_y
        print("You have moved to" + "(" + str(p.x) + ", " + str(p.y) + ")")
        return


def is_valid_move(p: Player, d: str, w: World) -> bool:
    """Given a direction verify if the move is valid"""
    direction = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}
    new_x = p.x + direction[d][0]
    new_y = p.y + direction[d][1]
    return 0 <= new_x <= 5 and 0 <= new_y <= 4 and w.map[new_y][new_x] != -1


def initiate_fight(p: Player, l: Location, item_data: dict[Any, list[Item]]) -> None:
    """Initiate a fight"""
    health = p.food * 10
    opponent_health = 40
    print("Fight Initiated!!!")
    print("Fighting rules: ")
    print("Your opponent has 50 health and you have 5 health for every piece of food you ate today")
    print("You have three moves: attack, heal, and special")
    print("Your attacks scale proprotionally to the amount of food you ate")
    print("Heal grants 10 HP but can only be used once every 3 turns")
    print("Your special is a burn, thanks to your trusty pocket flamethrower. You can use it after you attacks 3 times "
          "and it deals massive damage and leaves your opponent burned for the remainder of the battle.")
    print("Your opponent has not special but can heal 10 HP every two turns")
    special = 3
    heal = 0
    opponent_heal = 0
    burned = False

    while health > 0 and opponent_health > 0:
        attack = random.randint(round(p.food * 1.5), round(p.food * 2))
        opponent_attack = random.randint(6, 8)
        print("Your opponent has " + str(opponent_health) + " health")
        print("Your health: " + str(health))
        print("You have " + str(special) + " moves until your special")
        print("You have " + str(heal) + " moves until your heal")
        available_moves = ["burn", 'attack', 'heal'] if special == 0 else ['attack', 'heal']
        if heal > 0:
            available_moves.remove('heal')
        print(available_moves)
        your_move = input("Input Move: ")

        while your_move not in available_moves:
            your_move = input("Invald. Input Move: ")

        if your_move == 'attack':
            print("You punch your friend, dealing " + str(attack) + " damage.")
            opponent_health -= attack
            heal -= 1 if heal > 0 else heal
            special -= 1 if special > 0 else special
        elif your_move == 'heal':
            print("You heal 10 HP")
            health += 10
            health = p.food * 8 if health > p.food * 8 else health
            heal = 2
            special -= 1 if special > 0 else special
        else:
            print("You use your flamethrower, burning your enemy and dealing 15 damage")
            burned = True
            special = 3
            opponent_health -= 15
            heal -=1 if heal > 0 else heal

        print()

        if opponent_health < 20 and opponent_heal == 0:
            print("Your opponent heals for 10 HP.")
            opponent_health += 10
            opponent_heal = 2
        else:
            print("Your opponent attacks you for " + str(opponent_attack) + " attack")
            health -= opponent_attack
            opponent_heal -= 1 if opponent_heal > 0 else opponent_heal

        if burned:
            burned = random.randint(3,5)
            print("The burn causes your opponent to lose " + str(burned) + " HP")
            opponent_health -= burned

    if health <= 0:
        print("You have fought valiantly, but you have lost the fight")

    elif opponent_health <= 0:
        print("You have beaten your friend successfully, and it looks like he dropped something! ")
        l.examined = True
        items = [item.name for item in l.available_items(item_data)]
        if items != []:
            print(items)
        else:
            print("No available items at this location.")


def location_description(p: Player, curr_location: Location, command: Optional[str] = None) -> None:
    """
    Prints out the location_description of a particular location
    """
    if isinstance(curr_location, BlockedOrHallway):
        if curr_location.first_visit[(p.x, p.y)] or command == "look":
            print(curr_location.long_desc)
            curr_location.first_visit[(p.x, p.y)] = False

    elif curr_location.first_visit or command == "look":
        print(curr_location.long_desc)
        curr_location.first_visit = False

    else:
        print(curr_location.brief_desc)


def show_map(map_data: list[list[int]], location_data: list[Location]) -> None:
    """
    Prints the map_data as a grid in the console with a corresponding legend.
    If the player has not visited a location before, the location will show up as '?'.
    Otherwise, the location will show up as an integer.
    """
    new_map = []
    known_locations = set()

    # iterate through the map rows
    for y in range(len(map_data)):
        map_row = []

        # iterate through each item in the row
        for x in range(len(map_data[0])):
            location_num = map_data[y][x]

            # if it's a hallway or blocked area, check the first_visit attribute
            # (True if the player has not visited before)
            if (location_num == 0 or location_num == -1) and location_data[location_num].first_visit[(x, y)]:
                map_row.append('?')

            # otherwise, just check the first_visit attribute
            elif location_data[location_num].first_visit is True:
                map_row.append('?')

            else:
                map_row.append(location_num)
                known_locations.add(location_num)

        new_map.append(map_row)

    # print the map grid in a visually pleasing manner
    for row in new_map:
        grid_row = f"   "
        for item in row:
            grid_row += f"{str(item) + " ": ^3}"

        print(grid_row)

    # print the legend for the map location names
    legend = [f"{location_data[i].map_position} - {location_data[i].name}" for i in known_locations]
    print()
    for i in legend:
        print(i)


def player_action(choice: str, p: Player, w: World, l: Location, item_data: dict[Any, list[Item]]) -> Any:

    if choice == 'move':
        directions = ['N', 'S', 'E', 'W']
        print("\nValid directions: ", [d for d in directions if is_valid_move(p, d, w)])
        d = input("\nPick a direction: ")

        while d not in directions:
            d = input("\n Invalid Input. Pick a direction: ")
        move(p, d, w)

    elif choice == 'look':
        location_description(p, l, 'look')

    elif choice == 'examine':
        if l.map_position != 11:
            l.examined = True
            items = [item.name for item in l.available_items(item_data)]
            if items != []:
                print("You search the whole area and have found something!")
                print(items)
            else:
                print("No available items at this location.")
        else:
            print("After searching the grounds of chestnut, you see your friend with your room key.")
            print(
                "Unfortunately for you, their still mad about...something, you're actually not quite sure what you did.")
            print("All you know is you're not getting that room key without a fight!")
            fight = input("Do you run or fight? (Fighting takes time so you lose a move fyi)")
            while fight != 'run' and fight != 'fight':
                print("Invalid input.")
                fight = input("Do you run or fight? (Fighting takes time so you lose a move fyi)")
            if fight == 'run':
                print("You ran away like a coward but hey at least you're not beat up!")
            elif p.food < 3:
                print("You try to throw a punch, but unfortunately you're too weak and get pummeled instantly.")
                print(
                    "You walk away, thinking that you may have a chance if you actually had breakfast this morning....")
            else:
                initiate_fight(p, l, item_data)



    elif choice == 'map':
        show_map(w.map, w.locations)

    elif choice == 'inventory':
        print([item.name for item in p.inventory])

    elif choice == 'score':
        print("You have " + str(p.points) + " points.")

    elif choice == 'pick up':

        if l.examined:
            print([object.name for object in w.items[l.map_position]])

            item = input("\nPick an item: ")
            while item not in [object.name for object in w.items[l.map_position]]:
                item = input("\nInvalid item. Pick an item: ")

            for object in w.items[l.map_position]:
                if object.name == item:
                    p.inventory.append(object)
                    p.points += object.points
                    w.items[l.map_position].remove(object)
                    print("You have picked up " + item)

        else:
            print("You don't know what items are available because you have not examined this room yet. ")

    elif choice == 'use':
        print([item.name for item in p.inventory if isinstance(item, Usable_Item)])
        item = input("\nPick an item: ")
        while item not in [item.name for item in p.inventory if isinstance(item, Usable_Item)]:
            item = input("\nInvalid item. Pick an item: ")
        for object in p.inventory:
            if item == object.name: item_object = object
        item_object.use_item(p, l)
    return


def check_victory(p: Player, w: World, l: Location) -> None:
    """Checks to see if the player won the game"""
    items = {item.name for item in p.inventory}
    if "Cheat Sheet" in items and "Lucky Pen" in items and "T Card" in items and p.x == 5 and p.y == 4:
        p.victory = True


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(0, 1)  # set starting location of player; you may change the x, y coordinates here as appropriate

    # setting first_visit attribute for blocked/hallway locations
    w.locations[0].first_visit_dict(w.map)
    w.locations[-1].first_visit_dict(w.map)

    print("Insert initial plot")
    menu = ["look", "map", "inventory", "score", "quit"]

    choice = 'move'
    move_limit = 40

    while not p.victory and move_limit > 0:

        location = w.get_location(p.x, p.y)
        available_actions = ["move"]

        if any(item.name for item in p.inventory if isinstance(item, Usable_Item)):
            available_actions.append("use")

        if location.examined and (location.map_position in w.items and w.items[location.map_position] != []):
            available_actions.append("pick up")
        else:
            if not location.examined: available_actions.append("examine")

        if choice == 'move':
            print(location_description(location))
            # Depending on whether it's been visited before,
            # print either full description (first time visit) or brief description (every subsequent visit)
            print("What to do? \n")

        print("Moves left:", move_limit)
        print("[menu]")

        for action in available_actions:
            print(action)
        choice = input("\nEnter action: ")

        while choice != "[menu]" and choice not in available_actions:
            choice = input("\nInvalid. Choose action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)

            choice = input("\nChoose action: ")
            while choice not in menu:
                choice = input("\nInvalid. Choose action: ")

            player_action(choice, p, w, location, w.items)

        elif choice == 'quit':
            break

        else:
            player_action(choice, p, w, location, w.items)

        if choice == "examine" or choice == "move":
            move_limit -= 1

        check_victory(p, w, location)

    if p.victory:
        print("You have successfully brought everything to the exam centre, and just in the nick of time too!")
        print("Points: " + str(p.points))
        print("You win!")

    elif move_limit <= 0:
        print("Unfortunately, time is up. Your exam has started and you have not reached the exam centre. You lost.")

    elif choice == 'quit':
        print("You have successfuly quit the game. Nothing was saved sorry.")

        # TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
