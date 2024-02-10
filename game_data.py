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
    name: str
    start_position: int
    target_position: int
    points: int

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
    - first_visit: True if the player has not yet visited the location. False otherwise.
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
    map_position: int
    name: str
    brief_desc: str
    long_desc: str
    first_visit: bool
    examined: bool

    def __init__(self, map_position: int, name: str, brief_desc: str, long_desc: str) -> None:
        """Initialize a new location.
        """
        self.map_position = map_position
        self.name = name
        self.brief_desc = brief_desc
        self.long_desc = long_desc
        self.first_visit = True
        self.examined = False

    def available_items(self, item_dict: dict[int, list[Item]]) -> Optional[list[Item]]:
        """
        Returns a list of available items from item_dict at a particular location only if the player has
        examined the location before.

        >>> granola = Item('granola', 1, 2, 5)
        >>> items = {1: [granola]}
        >>> curr_location = Location(1, 'name', 'brief_desc', 'long_desc')
        >>> curr_location.available_items(items) is None
        True

        >>> curr_location.examined = True
        >>> items_at_location = curr_location.available_items(items)
        >>> [item.name for item in items_at_location] == ['granola']
        True

        >>> items = {2: [granola]}
        >>> curr_location.available_items(items)
        []
        """
        if not self.examined:
            return None

        if self.map_position in item_dict:
            return item_dict[self.map_position]

        else:
            return []


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
    - food: int

    Representation Invariants:
    - 0 <= self.x <= 6
    - 0 <= self.y <= 5
    - self.points >= 0
    - food >= 0
    """
    x: int
    y: int
    inventory: list[Item]
    points: int
    victory: bool
    food: int

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
        self.food = 0


class BlockedOrHallway(Location):
    """
    'Blocked' and 'Hallway' are special Locations that the player can encounter.
    Unlike named Locations, there can be multiple instances of 'Blocked' and 'Hallway' in the world map.

    It has the following updated attributes:
    - map_position: always equal to 0 or -1
    - first_visit: a dictionary mapping (x, y) coordinates to whether or not the location has been visited before (bool)
    - examined: a dictionary mapping (x, y) coordinates to whether or not the location has been examined before (bool)

    Instance Attributes:
    - map_position: int
    - first_visit: dict[tuple, bool]
    - examined: dict[tuple, bool]

    Representation invariants:
    - self.map_position == 0 or self.map_position == -1
    """
    map_position: int
    first_visit: dict[tuple, bool]
    examined: dict[tuple, bool]

    def __init__(self, map_position: int, name: str, brief_desc: str, long_desc: str) -> None:
        """Initialize a new hallway or blocked area.
        """
        super().__init__(map_position, name, brief_desc, long_desc)
        self.first_visit = {}
        self.examined = {}

    def init_fv_examine(self, map_data: list[list[int]]) -> None:
        """
        For the first_visit attribute and the examined attribute:
        Sets the (x, y) coordinates of blocked or hallway areas and sets first_visit to True (because the player has
        not yet visited the location) and sets examined to Fales (because the player has not examined the location yet).

        >>> map_list = [[-1, 0, -1], [4, -1, 0]]
        >>> hallway = BlockedOrHallway(0, 'hallway', 'brief', 'longggggg')
        >>> hallway.init_fv_examine(map_list)
        >>> hallway.first_visit == {(1, 0): True, (2, 1): True}
        True
        >>> hallway.examined == {(1, 0): False, (2, 1): False}
        True

        >>> blocked = BlockedOrHallway(-1, 'blocked', 'brief', 'longggggg')
        >>> blocked.init_fv_examine(map_list)
        >>> blocked.first_visit == {(0, 0): True, (2, 0): True, (1, 1): True}
        True
        >>> blocked.examined == {(0, 0): False, (2, 0): False, (1, 1): False}
        True
        """
        for y in range(len(map_data)):
            for x in range(len(map_data[0])):
                if map_data[y][x] == self.map_position:
                    self.first_visit[(x, y)] = True
                    self.examined[(x, y)] = False


class UsableItem(Item):
    """
    Usable items in our game.
    Unlike regular items, usable items can be consumed or used by the player.

    It has the additional attribute:
    - is_food: True if an item can be eaten by the player. False otherwise.
    - target_points: always equal to 5
    """
    is_food: bool

    def __init__(self, name: str, start: int, target: int, food: bool) -> None:
        """
        Initialize a new usable item with the is_food attribute.
        """
        super().__init__(name, start, target, 5)
        self.is_food = food

    def use_item(self, p: Player, location: Location) -> None:
        """
        Use the item by removing it form the player's inventory and modifying the player's points/location.
        An item will either be food or it will be the Transportation Card

        Preconditions:
        - (self.name == 'Transportation Card') and (self.is_food is False)
        - (self.name != 'Transportation Card') and (self.is_food is True)
        - any([self.name == item.name for item in p.inventory])

        >>> granola = UsableItem('granola', 1, 2, True)
        >>> location1 = Location(1, 'name', 'brief_desc', 'long_desc')
        >>> player1 = Player(0, 1)
        >>> player1.inventory.append(granola)

        >>> granola.use_item(player1, location1)
        You have eaten food, 5 points added!
        >>> player1.points == 5
        True
        >>> player1.food == 1
        True
        >>> player1.inventory == []
        True

        >>> subway_card = UsableItem('Transportation Card', 1, 2, False)
        >>> location2 = Location(2, 'Subway Station', 'brief_desc', 'long_desc')
        >>> player2 = Player(0, 2)
        >>> player2.inventory.append(subway_card)

        >>> subway_card.use_item(player2, location2)
        You have taken the subway to the exam centre.
        >>> player2.inventory == []
        True

        >>> subway_card = UsableItem('Transportation Card', 1, 2, False)
        >>> location2 = Location(4, 'Not the Subway Station', 'brief_desc', 'long_desc')
        >>> player2 = Player(0, 5)
        >>> player2.inventory.append(subway_card)

        >>> subway_card.use_item(player2, location2)
        You must be at the Subway Station to use it, very close to your room actually....
        >>> player2.inventory == [subway_card]
        True
        """

        if self.is_food:
            p.points += 5
            p.food += 1
            p.inventory.remove(self)
            print("You have eaten food, 5 points added!")

        elif self.name == 'Transportation Card':
            if location.map_position == 2:
                p.x, p.y = 5, 4
                p.inventory.remove(self)
                print("You have taken the subway to the exam centre.")
            else:
                print("You must be at the Subway Station to use it, very close to your room actually....")


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
    - map: a nested list representation of this world's map
    - location: a list of Location objects
    - items: a list Item objects

    Representation Invariants:
    - self.map != []
    - self.locations != []
    - self.items != []
    """
    map: list[list[int]]
    locations: list[Location]
    items: dict[int, list[Item]]

    def __init__(self, map_data: TextIO, location_data: TextIO, item_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """
        self.map = self.load_map(map_data)
        self.locations = self.load_locations(location_data)
        self.items = self.load_items(item_data)

    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        map_list = []
        line = map_data.readline().strip()
        while line != '':
            line = line.split(' ')
            row = [int(num) for num in line]
            map_list.append(row)
            line = map_data.readline().strip()
        return map_list

    def load_locations(self, location_data: TextIO) -> list[Location]:
        """
        Store locations from open file location_data as a list of Location class items.
        The list is structured such that each index corresponds to the location number.
        E.g. Hallway is location 0 so can be accessed by indexing the list at 0.
             Null space is -1 so can be accessed by indexing list at -1.
        """
        locations = []
        line = location_data.readline().strip()

        while line != '':
            row = [line]

            line = location_data.readline().strip()
            row.append(line)
            line = location_data.readline().strip()
            row.append(line)

            line = location_data.readline().strip()
            description = ''
            while line != 'END':
                description += line + ' '
                line = location_data.readline().strip()
            row.append(description)

            if int(row[1]) == 0 or int(row[1]) == -1:
                locations.append(BlockedOrHallway(int(row[1]), row[0], row[2], row[3]))
            else:
                locations.append(Location(int(row[1]), row[0], row[2], row[3]))

            location_data.readline().strip()
            line = location_data.readline().strip()
        return locations

    def load_items(self, item_data: TextIO) -> dict[Any, list[Item]]:
        """
        Store items from open file item_data as a dictionary mapping the location number of the item to the items
        whose start position is that same location.

        Dictionary is structured as follows: {location_id1: [item1, item2], location_id2: [item3]}
        """
        items = {}

        line = item_data.readline().strip()
        while line != '':
            line = line.split(' ')
            line[3] += ' ' + line.pop(4)
            if line[3] not in ['Lucky Pen', 'Transportation Card', 'Cheat Sheet', 'T Card', 'Room Key']:
                item = UsableItem(line[3], int(line[0]), int(line[1]), True)
            elif line[3] == 'Transportation Card':
                item = UsableItem(line[3], int(line[0]), int(line[1]), False)
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
        """
        Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
        that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
        return None.)
        """

        if x < len(self.map[0]) and y < len(self.map) and self.map[y][x] != -1:
            return self.locations[self.map[y][x]]

        else:
            return None


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120
    })
