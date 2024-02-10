"""
*** assignment 2 was from CSC110 was not referenced when making this wordle except for the word file.
possible_words.txt is directly taken from assignment 2
"""
import random
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
    FIXDOCSTRINGFIXDOCSTRINGFIXDOCSTRINGFIXDOCSTRINGFIXDOCSTRINGFIXDOCSTRINGFIXDOCSTRINGFIXDOCSTRING
    Mutates wordle_grid by turning a blank line at index 'turn' to be equal to checked_guess.
    """
    wordle_grid[turn] = checked_guess
    print(wordle_grid)


def print_wordle_grid(wordle_grid: list[list[str]]) -> None:
    """
    prints out the wordle grid in an aesthetically pleasing format.
    """
    for row in wordle_grid:
        grid_row = f" "

        for item in row:
            grid_row += f"{str(item) + " ": ^2}"

        print(grid_row)


def check_guess(guess: str, answer: str) -> list:
    """
    Check guess
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


def play_wordle() -> None:
    """
    Play wordle.
    """
    # load word_data
    word_file = open("possible_words.txt")
    word_data = load_words(word_file)
    word_file.close()

    # initialize useful variables
    answer = word_data[random.randint(0, len(word_data))]
    print(answer)
    turn = 0
    win_condition = False

    print("This is wordle! You have 6 tries to guess a five-letter word.\n\n"
          " - a capital letter indicates the letter is in the right place.\n"
          " - a question mark indicates the letter is in the wrong place.\n"
          " - a lowercase letter indicates the letter is in the word but in wrong place.\n")

    wordle_grid = create_wordle_grid()
    print_wordle_grid(wordle_grid)

    # gameplay
    while turn < 6 and not win_condition:
        # getting input
        guess = input("\nType in your guess here: ")

        while guess.upper() not in word_data:
            guess = input("Invalid word. Type in another guess: ")

        # compare guess and answer
        checked_guess = check_guess(guess, answer)

        # update and print the wordle grid
        update_wordle_grid(checked_guess, turn, wordle_grid)
        print(wordle_grid)
        print_wordle_grid(wordle_grid)  # prints the wordle_grid

        # check win
        if answer == guess:
            win_condition = True

    # post-game
    if win_condition:
        print('You win!')

    else:
        print('You lose :(')


if __name__ == "__main__":
    play_wordle()
