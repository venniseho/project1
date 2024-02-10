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
from typing import Optional, Any
from game_data import BlockedOrHallway, World, Item, Location, Player, UsableItem
from fight import initiate_fight
from dordle import play_dordle


def move(p: Player, d: str, w: World) -> None:
    """
    Given a direction (N, S, W, E), update the player's location in that direction given the move is valid
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
    Prints out the location_description of a particular location.
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
        grid_row = "   "
        for item in row:
            grid_row += f"{str(item) + " ": ^3}"

        print(grid_row)

    # print the legend for the map location names
    legend = [f"{location_data[index].map_position} - {location_data[index].name}" for index in known_locations]
    print()
    print('- - Unaccessible Square')
    for i in legend:
        print(i)


def gameplay(p: Player, curr_location: Location, item_data: dict[Any, list[Item]]) -> None:
    """
    Initiates gameplay for our two minigames: Fight and Dordle

    Preconditions:
    - location.map_position == 3 or location.map_position == 11
    """
    # FIGHT
    if curr_location.map_position == 11:
        print("After searching the grounds of chestnut, you see your friend with your room key.")
        print("Unfortunately for you, they're still mad about...something. You're not quite sure what you did.")
        print("All you know is you're not getting that room key without a fight!")
        fight = input("Do you run or fight? (Fighting takes time so you lose a move fyi)")
        while fight not in ['run', 'fight']:
            print("Invalid input.")
            fight = input("Do you run or fight? (Fighting takes time so you lose a move fyi)")
        if fight == 'run':
            print("You ran away like a coward but hey at least you're not beat up!")
        elif p.food < 3:
            print("You try to throw a punch, but unfortunately you're too weak and get pummeled instantly.")
            print("You walk away, thinking that you may have a chance if you actually had breakfast this morning....")
        else:
            initiate_fight(p, curr_location, item_data)

    # DORDLE
    elif curr_location.map_position == 3:
        print("After searching every floor of EJ Pratt, you realise that someone else in the library has"
              " your cheat sheet!")
        print("They challenge you to a game of dordle for the rights to the cheat sheet (even though it literally"
              "has your name on it...).")
        print("Taking the challenge will cost you one move.")

        dordle = input("Do you take the challenge? (Yes or No): ").upper()
        while dordle not in ['YES', 'NO']:
            print("Invalid input.")
            dordle = input("Do you take the challenge? (Yes or No): ").upper()

        if dordle == "YES":
            play_dordle(curr_location)

        else:
            print("You do not take the challenge. Maybe you have time to just rewrite the cheat sheet? "
                  "(you do not and you very much need that cheat sheet)")


def pick_up(p: Player, w: World, curr_location: Location) -> None:
    """Allows player to pick up item"""
    if curr_location.examined:
        print([location_item.name for location_item in w.items[curr_location.map_position]])

        item = input("\nPick an item: ")
        while item not in [location_item.name for location_item in w.items[curr_location.map_position]]:
            item = input("\nInvalid item. Pick an item: ")

        for picked_object in w.items[curr_location.map_position]:
            if picked_object.name == item:
                p.inventory.append(picked_object)

                p.points = p.points + picked_object.points if not isinstance(picked_object, UsableItem) else p.points

                w.items[curr_location.map_position].remove(picked_object)
                print("You have picked up " + item)

    else:
        print("You don't know what items are available because you have not examined this room yet.")


def examine(p: Player, curr_location: Location, item_data: dict[int, list[Item]]) -> None:
    """
    Allow player to examine the location to find possible items

    >>> granola = Item('granola', 1, 2, 5)
    >>> player1 = Player(0, 1)
    >>> curr_location1 = Location(1, 'location', 'brief', 'long')
    >>> item_dict1 = {2: [granola]}
    >>> examine(player1, curr_location1, item_dict1)
    No available items at this location.

    >>> granola = Item('granola', 1, 2, 5)
    >>> player2 = Player(0, 1)
    >>> curr_location2 = Location(1, 'location', 'brief', 'long')
    >>> item_dict2 = {1: [granola]}
    >>> examine(player2, curr_location2, item_dict2)
    You search the whole area and have found something!
    ['granola']
    """
    if isinstance(curr_location, BlockedOrHallway):
        if not curr_location.examined[(p.x, p.y)]:
            curr_location.examined[(p.x, p.y)] = True
        print("No available items at this location.")

    elif curr_location.map_position in [3, 11]:
        print("You have found a minigame!")
        gameplay(p, curr_location, item_data)

    else:
        curr_location.examined = True
        items = [location_item.name for location_item in curr_location.available_items(item_data)]
        if items:
            print("You search the whole area and have found something!")
            print(items)
        else:
            print("No available items at this location.")


def use(p: Player, curr_location: Location) -> None:
    """Allow player to use a usable item"""
    print([player_item.name for player_item in p.inventory if isinstance(player_item, UsableItem)])
    item = input("\nPick an item: ")
    while item not in [player_item.name for player_item in p.inventory if isinstance(player_item, UsableItem)]:
        item = input("\nInvalid item. Pick an item: ")
    for player_object in p.inventory:
        if item == player_object.name:
            item_object = player_object
    item_object.use_item(p, curr_location)


def player_action(player_choice: str, p: Player, w: World,
                  curr_location: Location, item_data: dict[Any, list[Item]]) -> None:
    """Takes a player's choice and based on it, performs a specific action (e.g. move input will mutate player
    and move them)."""
    if player_choice == 'move':
        directions = ['N', 'S', 'E', 'W']
        print("\nValid directions: ", [direction for direction in directions if is_valid_move(p, direction, w)])
        d = input("\nPick a direction: ")

        while d not in directions:
            d = input("\n Invalid Input. Pick a direction: ")
        move(p, d, w)

    elif player_choice == 'look':
        location_description(p, curr_location, 'look')

    elif player_choice == 'examine':
        examine(p, curr_location, item_data)

    elif player_choice == 'map':
        show_map(w.map, w.locations)

    elif player_choice == 'inventory':
        items = [player_item.name for player_item in p.inventory]
        if items:
            print(items)
        else:
            print("[Inventory Empty]")

    elif player_choice == 'score':
        print("You have " + str(p.points) + " points.")

    elif player_choice == 'pick up':
        pick_up(p, w, curr_location)

    elif player_choice == 'use':
        use(p, curr_location)


def check_victory(p: Player) -> None:
    """Checks to see if the player won the game"""
    items = {item.name for item in p.inventory}
    if "Cheat Sheet" in items and "Lucky Pen" in items and "T Card" in items and p.x == 5 and p.y == 4:
        p.victory = True


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    world = World(open("map.txt"), open("locations.txt"), open("items.txt"))

    player = Player(0, 1)  # set starting location of player; you may change the x, y coordinates here as appropriate

    # setting first_visit attribute for blocked/hallway locations
    world.locations[0].init_fv_examine(world.map)
    world.locations[-1].init_fv_examine(world.map)

    menu = ["look", "map", "inventory", "score", "quit"]

    choice = 'move'
    move_limit = 40

    while not player.victory and move_limit > 0:

        location = world.get_location(player.x, player.y)
        available_actions = ["move"]

        if any(item.name for item in player.inventory if isinstance(item, UsableItem)):
            available_actions.append("use")

        if location.examined and (location.map_position in world.items and world.items[location.map_position] != []):
            available_actions.append("pick up")
        else:
            if ((isinstance(location, BlockedOrHallway)
                 and not location.examined[(player.x, player.y)])
                    or not location.examined):
                available_actions.append("examine")

        if choice == 'move':
            print("Moves left:", move_limit, "\n")
            location_description(player, location)
            print("\nWhat to do? ")
            location_description(player, location)
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

        player_action(choice, player, world, location, world.items)

        if choice in ["examine", "move"]:
            move_limit -= 1

        check_victory(player)

    if player.victory:
        print("You have successfully brought everything to the exam centre, and just in the nick of time too!")
        print("Points: " + str(player.points))
        print("You win!")

    elif move_limit <= 0:
        print("Unfortunately, time is up. Your exam has started and you have not reached the exam centre. You lost.")

    elif choice == 'quit':
        print("You have successfuly quit the game. Nothing was saved sorry.")

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['hashlib']
    })
