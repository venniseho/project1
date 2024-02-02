"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Any, Optional, TextIO


class Player:
    """
    A Player in the text advanture game.
    Functions:
    - Move
    - Pick up Items
    - Use Items

    Instance Attributes:
        - x: int
        - y: int
        - inventory: list[Item]
        - points: int
        - victory: bool

    Representation Invariants:
        - 0 <= self.x <= 6
        - 0 <= self.y <= 5
        - self.points >= 0
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.inventory = []
        self.points = 0
        self.victory = False


class Item:
    """An item in our text adventure game world.

    something triggered by pick up/deposit

    Instance Attributes:
        - name: str
        - start_position: int
        - target_position: int
        - target_points: int

    Representation Invariants:
        - start_position >= -1
        - target_position >= -1
        - target_points >= 0
    """

    def __init__(self, name: str, start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = start
        self.target_position = target
        self.points = target_points


class Location:
    """A location in our text adventure game world.
    - map_position: an integer representing where the player is on the world map.
                    -1 represents inaccessible areas of the map.
                    0 represents locations the player can walk through but containing no actions.
    - name: the name of the item
    - long_desc: a long description of the location that prints if it is the player's first time visiting the location.
    - brief_desc: a brief description of the location that prints if the player has visited at least once before.
    - first_visit: True if this is the player's first time arriving at the location. False otherwise.
    - examined: False if the player has not yet examined the location. True otherwise.

    Instance Attributes:
        - map_position: int
        - name: str
        - brief_desc: str
        - long_desc: str
        - first_visit: bool
        - examined: bool

    Representation Invariants:
        - map_position >= -1
    """

    def __init__(self, map_position, name, brief_desc, long_desc) -> None:
        """Initialize a new location.
        """
        self.map_position = map_position
        self.name = name
        self.brief_desc = brief_desc
        self.long_desc = long_desc
        self.first_visit = True
        self.examined = False

    def available_items(self, item_dict: dict[Any, list[Item]]) -> Optional[list[Item]]:
        """
        Returns a list of available items from item_dict at a particular location.
        """
        if not self.examined:
            return None

        if self.map_position in item_dict:
            return item_dict[self.map_position]

        else:
            return []

class Usable_Item(Item):
    """Usable items in our game"""

    def __init__(self, name: str, start: int, target: int, target_points: int, food: bool) -> None:
        """Initialize a new usable item with the is_food attribute.
        """

        self.name = name
        self.start_position = start
        self.target_position = target
        self.points = target_points
        self.is_food = food


    def use_item(self, p: Player, l: Location) -> None:
        """Use the item by removing it form the player's inventory and modifying the player's points/location"""
        if self.is_food:
            p.points += 5
            p.inventory.remove(self)
            print("You have eaten food, 5 points added!")
        elif self.name == 'Transportation Card':
            if l.map_position == 2:
                p.x, p.y = 5, 4
                p.inventory.remove(self)
                print("You have taken the subway to the exam centre.")
            else:
                print("You must be at the Subway Station to use it, very close to your room actually....")


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - location: a nested list representation of locations their descriptions
        - items: a nested list representation of items

    Representation Invariants:
        - self.map != []
        - self.locations != []
        - self.items != []
    """

    def __init__(self, map_data: TextIO, location_data: TextIO, item_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)
        self.locations = self.load_locations(location_data)
        self.items = self.load_items(item_data)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        map = []
        line = map_data.readline().strip()
        while line != '':
            line = line.split(' ')
            row = [int(num) for num in line]
            map.append(row)
            line = map_data.readline().strip()
        return map

    def load_locations(self, location_data: TextIO) -> list[Location]:
        """Store locations from open file location_data as a nested list.
        Location list is structured such that each index corresponds to the location number. E.g. Hallway is location
        0 so can be accessed by indexing the list at 0. Null space is -1 so can be accessed by indexing list at -1.
        List is in the form [Name, Position, Short, Long]
        """
        locations = []
        line = location_data.readline().strip()

        while line != '':
            row = [line]
            for i in range(2):
                line = location_data.readline().strip()
                row.append(line)

            line = location_data.readline().strip()
            description = ''
            while line != 'END':
                description += line + ' '
                line = location_data.readline().strip()
            row.append(description)
            locations.append(Location(int(row[1]), row[0], row[2], row[3]))

            line = location_data.readline().strip()
            line = location_data.readline().strip()
        return locations

    def load_items(self, item_data: TextIO) -> dict[Any, list[Item]]:
        """Store items from open file item_data as a dictionary mapping the location number of the item to the items
        whose start position is that same location.

        Dictionary is structured as follows: {location_id1: [item1, item2], location_id2: [item3]}
        """
        items = {}

        line = item_data.readline().strip()
        while line != '':
            line = line.split(' ')
            line[3] += ' ' + line.pop(4)
            if line[3] not in ['Lucky Pen', 'Transportation Card', 'Cheat Sheet', 'T Card', 'Room Key']:
                item = Usable_Item(line[3], int(line[0]), int(line[1]), int(line[2]), True)
            elif line[3] == 'Transportation Card':
                item = Usable_Item(line[3], int(line[0]), int(line[1]), int(line[2]), False)
            else:
                item = Item(line[3], int(line[0]), int(line[1]), int(line[2]))

            if item.start_position not in items:
                items[item.start_position] = [item]

            else:
                items[item.start_position].append(item)

            line = item_data.readline().strip()

        items["Inventory"] = []

        return items

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """

        if x < len(self.map[0]) and y < len(self.map) and self.map[y][x] != -1:
            return self.locations[self.map[y][x]]

        else:
            return None
