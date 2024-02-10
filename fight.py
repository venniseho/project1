"""
The fight ADD DOCSTRING
"""
from typing import Any
import random
from game_data import Player, Location, Item


def initiate_fight(p: Player, location: Location, item_data: dict[Any, list[Item]]) -> None:
    """Initiate a fight. The fight should be as follows:
       - Turn based fight
       - Opponent has 40 health, you ahve 5 for every food
       - You have attack (proportional to food), heal (10HP), and special(burn the enemy, damage over time)
       - Opponent can heal 10 every tim
       - You win if opponent is 0, you lose of you are at 0"""
    health, opponent_health = p.food * 10, 40

    print_instructions()

    special, heal, opponent_heal, burned = 3, 0, 0, False

    while health > 0 and opponent_health > 0:
        attack, opponent_attack = random.randint(round(p.food * 1.5), round(p.food * 2)), random.randint(6, 8)
        print_stats(opponent_health, health, heal, special)
        available_moves = ["burn", 'attack', 'heal'] if special == 0 else ['attack', 'heal']
        if heal > 0:
            available_moves.remove('heal')
        print(available_moves)
        your_move = input("Input Move: ")
        if your_move == 'bypass win':
            opponent_health = 0
            break
        elif your_move == 'bypass lose':
            health = 0
            break

        while your_move not in available_moves:
            your_move = input("Invald. Input Move: ")

        print_move(your_move, attack)
        if your_move == 'attack':
            opponent_health -= attack
            heal -= 1 if heal > 0 else heal
            special -= 1 if special > 0 else special
        elif your_move == 'heal':
            health += 10
            health = p.food * 10 if health > p.food * 10 else health
            heal = 2
            special -= 1 if special > 0 else special
        else:
            burned, special = True, 3
            opponent_health -= 15
            heal -= 1 if heal > 0 else heal

        if opponent_health < 20 and opponent_heal == 0:
            print("Your opponent heals for 10 HP.")
            opponent_health += 10
            opponent_heal = 2
        else:
            print("Your opponent attacks you for " + str(opponent_attack) + " attack")
            health -= opponent_attack
            opponent_heal -= 1 if opponent_heal > 0 else opponent_heal

        if burned:
            burned = random.randint(3, 5)
            print("The burn causes your opponent to lose " + str(burned) + " HP")
            opponent_health -= burned

    check_fight_victory(health, opponent_health, location, item_data)


def check_fight_victory(health: int, opponent: int, location: Location, item_data: dict[Any, list[Item]]) -> None:
    """Check to see if player won fight and if so, print the desired statements
    and modify location/items appropriately"""
    if health <= 0:
        print("You have fought valiantly, but you have lost the fight")

    elif opponent <= 0:
        print("You have beaten your friend successfully, and it looks like he dropped something! ")
        location.examined = True
        items = [item.name for item in location.available_items(item_data)]
        if items != []:
            print(items)
        else:
            print("No available items at this location.")


def print_instructions() -> None:
    """Print fighting instructions"""
    print("Fight Initiated!!!")
    print("Fighting rules: ")
    print("Your opponent has 40 health and you have 5 health for every piece of food you ate today")
    print("You have three moves: attack, heal, and special. ")
    print("Your attacks scale proprotionally to the amount of food you ate")
    print("Heal grants 10 HP but can only be used once every 3 turns")
    print("Your special is a burn, thanks to your trusty pocket flamethrower. \
    You can use it after you attacks 3 times and it deals massive damage and \
    leaves your opponent burned for the remainder of the battle.")
    print("Your opponent has not special but can heal 10 HP every two turns")


def print_stats(opponent_health: int, health: int, heal: int, special: int) -> None:
    """Print the stats of the fight, including healths at the momment and
    turns neede to get to your heal and burn ability"""
    print()
    print("Your opponent health: " + str(opponent_health) + " health")
    print("Your health: " + str(health))
    print("You have " + str(special) + " moves until your special")
    print("You have " + str(heal) + " moves until your heal")


def print_move(your_move: str, attack: int) -> None:
    """Print the move you made against your opponent"""
    if your_move == 'attack':
        print("You punch your friend, dealing " + str(attack) + " damage.")
    elif your_move == 'heal':
        print("You heal 10 HP")
    else:
        print("You use your flamethrower, burning your enemy and dealing 15 damage")


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['hashlib']
    })
