"""
The fight ADD DOCSTRING
"""
from game_data import Player, Location, Item
from typing import Any
import random


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
