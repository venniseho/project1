"""
*** assignment 2 was from CSC110 was not referenced when making this wordle except for the word file.
possible_words.txt is directly taken from assignment 2
"""
import random
from game_data import Location
from typing import TextIO


def load_words(word_file: TextIO) -> list[str]:
    """
    Reads the words from possible_words.txt and converts it into a list.
    possible_words.txt contains one lowercase word per line.
    """
    word_list = []

    word = word_file.readline().strip()
    while word != '':
        word_list.append(word.upper())
        word = word_file.readline().strip()

    return word_list


def create_wordle_grid() -> list[list[str]]:
    """
    Create a blank 5x6 wordle grid (width x height).
    """

    grid = []

    for i in range(6):
        row = []
        for i in range(5):
            row.append('_')
        grid.append(row)

    return grid


def update_wordle_grid(checked_guess: list[str], turn: int, wordle_grid: list[list[str]]) -> None:
    """
    Mutates wordle_grid by turning a blank line at index 'turn' to be equal to checked_guess.

    Representation Invariants:
    - len(wordle_grid) == 6
    - all[len(row) == 5 for row in wordle_grid]
    """
    wordle_grid[turn] = checked_guess


def print_wordle_grids(wordle_grid1: list[list[str]], wordle_grid2: list[list[str]]) -> None:
    """
    Prints out the wordle grids in an aesthetically pleasing format.

    Representation Invariants:
    - len(wordle_grid) == 6
    - all[len(row) == 5 for row in wordle_grid]
    """
    for row in range(6):
        grid_row1 = f" "
        grid_row2 = f" "
        for letter in range(5):
            grid_row1 += f"{str(wordle_grid1[row][letter]) + " ": <2}"
            grid_row2 += f"{str(wordle_grid2[row][letter]) + " ": >2}"

        print(f"{grid_row1:^15} {grid_row2:^15}")


def check_guess(guess: str, answer: str) -> list:
    """
    Checks each letter in guess by wordle rules (with visual modifications for a text-based game).
    - if it's the right letter and right spot, then capitalize
    - if it's the right letter but wrong spot, then lowercase
    - if it's the wrong letter, then it shows up as a question mark
    """
    # create a dictionary that maps a letter in answer to the number of times it occurs
    answer_letter_count = {}

    for i in answer:
        if i in answer_letter_count:
            answer_letter_count[i] += 1
        else:
            answer_letter_count[i] = 1

    # compare guess to answer
    feedback = []

    for i in range(5):
        if guess[i] == answer[i] and answer_letter_count[guess[i]] > 0:
            answer_letter_count[guess[i]] -= 1
            feedback.append(guess[i])

        elif guess[i] in answer and answer_letter_count[guess[i]] > 0:
            answer_letter_count[guess[i]] -= 1
            feedback.append(guess[i].lower())

        elif guess[i] not in answer:
            feedback.append('?')

    return feedback


def play_dordle(location: Location) -> None:
    """
    Launches the game of wordle and returns True if the player won the game.
    Otherwise, returns False.
    """
    # load word_data
    word_file = open("possible_words.txt")
    word_data = load_words(word_file)
    word_file.close()

    # initialize useful variables
    answer1 = word_data[random.randint(0, len(word_data))]
    answer2 = word_data[random.randint(0, len(word_data))]

    turn = 0
    win1 = False
    win2 = False
    bypass = False

    print("This is dordle! You have 6 tries to guess two five-letter words.\n\n"
          " - a capital letter indicates the letter is in the word and in the right place.\n"
          " - a lowercase letter indicates the letter is in the word but in the wrong place.\n"
          " - a question mark indicates the letter is in not in the word.\n")

    wordle_grid1 = create_wordle_grid()
    wordle_grid2 = create_wordle_grid()
    print_wordle_grids(wordle_grid1, wordle_grid2)

    # gameplay
    # while there are turns left and both answers haven't been correctly guessed
    while turn < 6 and not (win1 and win2):
        # getting input
        guess = input("\nType in your guess here: ").upper()

        while guess not in word_data and guess != "BYPASS":
            guess = input("Invalid word. Type in another guess: ").upper()

        # bypass
        if guess == "BYPASS":
            bypass = True
            break

        # compare guess and answer
        checked_guess1 = check_guess(guess, answer1)
        checked_guess2 = check_guess(guess, answer2)

        # update and print the wordle grid
        if not win1:
            update_wordle_grid(checked_guess1, turn, wordle_grid1)

        if not win2:
            update_wordle_grid(checked_guess2, turn, wordle_grid2)

        print_wordle_grids(wordle_grid1, wordle_grid2)  # prints the wordle_grids

        # win condition
        if guess == answer1:
            win1 = True

        if guess == answer2:
            win2 = True

        turn += 1

    # post-game
    if (win1 and win2) or bypass:
        print('\nYou win!')
        location.examined = True

    else:
        print('\nYou lose :(')

    print(f"\nAnswers: {answer1}, {answer2}")

if __name__ == "__main__":
    play_dordle()
