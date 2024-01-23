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
from game_data import World, Item, Location, Player
from typing import Optional, Any


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


def location_description(curr_location: Location, command: Optional[str] = None) -> None:
    """
    Prints out the location_description of a particular location
    """
    if curr_location.first_visit or command == "look":
        print(curr_location.long_desc)
        curr_location.first_visit = False

    else:
        print(curr_location.brief_desc)


def available_actions(curr_location: Location, item_data: dict[Any, list[Item]], player_inventory: list, p: Player,
                      w: World) \
        -> dict[str, list[str]]:
    """
    Returns a list of available actions at a specific location.
    """
    directions = ['N', 'S', 'E', 'W']
    actions = {"move": [d for d in directions if is_valid_move(p, d, w)],
               "pick up": [item.name for item in curr_location.available_items(item_data)],
               "use": [item.name for item in player_inventory if item.target_position == curr_location]}
    actions = {action: actions[action] for action in actions if actions[action] != []}

    return actions


def player_action(choice: str, p: Player, w: World, l: Location) -> Any:
    if choice == 'move':
        d = input("\nPick a direction: ")
        while d not in ['N', 'S', 'E', 'W']:
            d = input("\n Invalid Input. Pick a direction: ")
        move(p, d, w)

    elif choice == 'look':
        location_description(l, 'look')

    elif choice == 'inventory':
        print([item.name for item in p.inventory])

    elif choice == 'score':
        print("You have " + str(p.points) + " points.")

    elif choice == 'pick up':
        print([object.name for object in w.items[l.map_position]])
        item = input("\nPick an item: ")
        while item not in [object.name for object in w.items[l.map_position]]:
            item = input("\nInvalid item. Pick an item: ")
        for object in w.items[l.map_position]:
            if object.name == item:
                p.inventory.append(object)
                w.items[l.map_position].remove(object)
            print("You have picked up " + item)

    elif choice == 'use':
        # TODO: Add parameters for using items
        item = input("\nPick an item: ")
        while item not in [item.name for item in p.inventory if item.target_position == l]:
            item = input("\nInvalid item. Pick an item: ")
        for object in w.items[l]:
            if object.name == item: p.inventory.remove(object)
            print("You have used " + item)

    return


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(0, 0)  # set starting location of player; you may change the x, y coordinates here as appropriate
    print("Insert initial plot")
    menu = ["look", "inventory", "score", "quit"]
    choice = 'move'

    while not p.victory:
        location = w.get_location(p.x, p.y)
        if choice == 'move':
            print(location_description(location))
            # Depending on whether it's been visited before,
            # print either full description (first time visit) or brief description (every subsequent visit)
            print("What to do? \n")
        print("[menu]")
        for action in available_actions(location, w.items, p.inventory, p, w):
            print(action, available_actions(location, w.items, p.inventory, p, w)[action])
        choice = input("\nEnter action: ")

        while choice != "[menu]" and choice not in available_actions(location, w.items, p.inventory, p, w):
            choice = input("\nInvalid. Choose action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")
            while choice not in menu:
                choice = input("\nInvalid. Choose action: ")
            player_action(choice, p, w, location)

        elif choice == 'quit':
            break

        else:
            player_action(choice, p, w, location)

    if p.victory:
        print("You win!")
    else:
        print("Bye")

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
