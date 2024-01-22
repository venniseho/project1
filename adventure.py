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

def pick_up(p: Player, item: Item) -> str:
    """Picks up an item and adds it to the player's inventory and prints out the successful pick up"""
    p.inventory.append(item)
    return "You have successfully picked up " + item.name


def move(p: Player, d: str, world_map: World) -> str:
    """Given a direction (N, S, W, E), update the player's location in that direction given the move is valid
    """
    direction = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}
    new_x = p.x + direction[d][0]
    new_y = p.x + direction[d][1]
    if world_map.map[new_x, new_y] == -1:
        return "Invalid, this square is unaccessible"
    else:
        p.x = new_x
        p.y = new_y
        return "TODO - Replace this with something"


def location_description(curr_location: Location, command: Optional[str] = None) -> None:
    """
    Prints out the location_description of a particular location
    """
    if curr_location.first_visit or command == "look":
        print(curr_location.long_desc)
        curr_location.first_visit = False

    else:
        print(curr_location.brief_desc)


def available_actions(curr_location: Location, item_data: dict[Any, list[Item]], player_inventory: list) \
        -> dict[str, list[str]]:
    """
    Returns a list of available actions at a specific location.
    """
    actions = {"move": ['N', 'S', 'E', 'W'], "pick up": [curr_location.available_items(item_data)],
               "use": [item.name for item in player_inventory if item.target_position == curr_location]}

    return actions


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(0, 0)  # set starting location of player; you may change the x, y coordinates here as appropriate
    print("Insert initial plot")
    menu = ["look", "inventory", "score", "quit", "back"]

    while not p.victory:
        location = w.get_location(p.x, p.y)

        # Depending on whether it's been visited before,
        # print either full description (first time visit) or brief description (every subsequent visit)

        print("What to do? \n")
        print("[menu]")
        for action in location.available_actions():
            print(action)
        choice = input("\nEnter action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")

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
