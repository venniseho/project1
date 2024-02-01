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


def location_description(curr_location: Location, command: Optional[str] = None) -> None:
    """
    Prints out the location_description of a particular location
    """
    if curr_location.first_visit or command == "look":
        print(curr_location.long_desc)
        curr_location.first_visit = False

    else:
        print(curr_location.brief_desc)


def player_action(choice: str, p: Player, w: World, l: Location, item_data: dict[Any, list[Item]]) -> Any:
    if choice == 'move':
        directions = ['N', 'S', 'E', 'W']
        print("\nValid directions: ", [d for d in directions if is_valid_move(p, d, w)])
        d = input("\nPick a direction: ")
        while d not in directions:
            d = input("\n Invalid Input. Pick a direction: ")
        move(p, d, w)

    elif choice == 'look':
        location_description(l, 'look')

    elif choice == 'examine':
        l.examined = True
        items = [item.name for item in l.available_items(item_data)]

        if items != []:
            print("You search the whole area and have found something!")
            print(items)
        else:
            print("No available items at this location.")

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
        usable = ['Granola Bar', 'Soda Can', 'Transportation Card']
        print([item.name for item in p.inventory if item.name in usable])
        item = input("\nPick an item: ")
        while item not in [object.name for object in p.inventory if object.name in usable]:
            item = input("\nInvalid item. Pick an item: ")
        for object in p.inventory:
            if item == object.name:
                item_object = object
        if item == 'Granola Bar' or item == 'Soda Can':
            p.points += 5
            p.inventory.remove(item_object)
            print("You have eaten food, 5 points added!")
        elif item == "Transportation Card":
            if l.map_position == 2:
                p.x, p.y = 5, 4
                p.inventory.remove(item_object)
                print("You have taken the subway to the exam centre.")
            else:
                print("You must be at the Subway Station to use it, very close to your room actually....")
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
    print("Insert initial plot")
    menu = ["look", "inventory", "score", "quit"]

    choice = 'move'
    move_limit = 40

    while not p.victory and move_limit > 0:
        location = w.get_location(p.x, p.y)
        available_actions = ["move"]
        if any(item.name for item in p.inventory if item.name in ['Granola Bar', 'Soda Can', 'Transportation Card']):
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
