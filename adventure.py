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
from fight import initiate_fight
from dordle import play_dordle
from typing import Optional, Any


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


def print_long_description(curr_location: Location) -> None:
    """
    Helper function to location_description.
    Prints out the long_desc of a particular location in a (mostly) aesthetically pleasing manner.
    """
    line_count = (len(curr_location.long_desc) // 75) + 1
    for i in range(line_count):
        line = curr_location.long_desc[75 * i:75 * (i + 1)]
        print(line)
    line = curr_location.long_desc[75 * (line_count + 1):]
    print(line)


def location_description(p: Player, curr_location: Location, command: Optional[str] = None) -> None:
    """
    Prints out the location_description of a particular location
    """

    if isinstance(curr_location, BlockedOrHallway):
        if (curr_location.first_visit[(p.x, p.y)]) or (command == "look"):
            print_long_description(curr_location)
            curr_location.first_visit[(p.x, p.y)] = False
        else:
            print(curr_location.brief_desc)

    elif curr_location.first_visit or command == "look":
        print_long_description(curr_location)
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
            if location_num == -1:
                map_row.append('-')

            elif location_num == 0 and location_data[location_num].first_visit[(x, y)]:
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
    print('- - Unaccessible Square')
    for i in legend:
        print(i)


def gameplay(p: Player, l: Location, item_data: dict[Any, list[Item]]) -> None:
    """
    Initiates gameplay for our two minigames: Fight and Dordle

    Preconditions:
    - l.map_position == 3 or l.map_position == 11
    """
    # FIGHT
    if l.map_position == 11:
        print("After searching the grounds of chestnut, you see your friend with your room key.")
        print("Unfortunately for you, they're still mad about...something. You're not quite sure what you did.")
        print("All you know is you're not getting that room key without a fight!")
        fight = input("Do you run or fight? (Fighting takes time so you lose a move fyi)")
        while fight != 'run' and fight != 'fight':
            print("Invalid input.")
            fight = input("Do you run or fight? (Fighting takes time so you lose a move fyi)")
        if fight == 'run':
            print("You ran away like a coward but hey at least you're not beat up!")
        elif p.food < 3:
            print("You try to throw a punch, but unfortunately you're too weak and get pummeled instantly.")
            print("You walk away, thinking that you may have a chance if you actually had breakfast this morning....")
        else:
            initiate_fight(p, l, item_data)

    # DORDLE
    elif l.map_position == 3:
        print("After searching every floor of EJ Pratt, you realise that someone else in the library has"
              " your cheat sheet!")
        print("They challenge you to a game of dordle for the rights to the cheat sheet (even though it literally"
              "has your name on it...).")
        print("Taking the challenge will cost you one move.")

        dordle = input("Do you take the challenge? (Yes or No): ").upper()
        while dordle != 'YES' and dordle != 'NO':
            print("Invalid input.")
            dordle = input("Do you take the challenge? (Yes or No): ").upper()

        if dordle == "YES":
            play_dordle(l)

        else:
            print("You do not take the challenge. Maybe you have time to just rewrite the cheat sheet? "
                  "(you do not and you very much need that cheat sheet)")


def player_action(choice: str, p: Player, w: World, l: Location, item_data: dict[Any, list[Item]]) -> None:

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
        if isinstance(l, BlockedOrHallway):
            if not l.examined[(p.x, p.y)]:
                l.examined[(p.x, p.y)] = True
            print("No available items at this location.")

        elif l.map_position == 3 or l.map_position == 11:
            print("You have found a minigame!")
            gameplay(p, l, item_data)

        else:
            l.examined = True
            items = [item.name for item in l.available_items(item_data)]
            if items:
                print("You search the whole area and have found something!")
                print(items)
            else:
                print("No available items at this location.")

    elif choice == 'map':
        show_map(w.map, w.locations)

    elif choice == 'inventory':
        items = [item.name for item in p.inventory]
        if items:
            print(items)
        else:
            print("[Inventory Empty]")

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

                    if not isinstance(object, Usable_Item):
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
    w.locations[0].init_fv_examine(w.map)
    w.locations[-1].init_fv_examine(w.map)

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
            if (isinstance(location, BlockedOrHallway) and not location.examined[(p.x, p.y)]) or not location.examined:
                available_actions.append("examine")

        if choice == 'move':
            print("Moves left:", move_limit, "\n")
            location_description(p, location)
            print("\nWhat to do? ")
            location_description(p, location)
            # Depending on whether it's been visited before,
            # print either full description (first time visit) or brief description (every subsequent visit)
            print("What to do? \n")

        print("\n[menu]")

        for action in available_actions:
            print(action)
        choice = input("\nEnter action: ")

        while choice != "[menu]" and choice not in available_actions:
            choice = input("\nInvalid. Choose action: ")

        if choice == "[menu]":
            print("\nMenu Options: ")
            for option in menu:
                print(option)

            choice = input("\nChoose action: ")
            while choice not in menu:
                choice = input("\nInvalid. Choose action: ")

        if choice == 'quit':
            break

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
