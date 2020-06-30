from random import choice
from string import ascii_lowercase

word_list = ['python', 'java', 'kotlin', 'javascript']
choice_word = choice(word_list)
output = len(choice_word) * '-'
tries = 8
guesses = set()
acceptable_guesses = ascii_lowercase


def game_play(guess):
    global output, tries
    if guess in guesses:
        print('You already typed this letter')
    elif len(guess) != 1:
        print('You should print a single letter')
    elif guess not in acceptable_guesses:
        print('It is not an ASCII lowercase letter')
    elif guess not in choice_word:
        guesses.add(guess)
        tries -= 1
        print('No such letter in the word')
    elif choice_word.count(guess) == 1:
        position = choice_word.find(guess)
        output = output[:position] + guess + output[position + 1:]
        guesses.add(guess)
    elif choice_word.count(guess) > 1:
        position_1 = choice_word.find(guess)
        position_2 = choice_word.rfind(guess)
        output = output[:position_1] + guess + output[position_1 + 1: position_2] + guess + output[position_2 + 1:]
        guesses.add(guess)


def hangman_game():
    win_or_lose = False
    while tries > 0:
        print()
        print(output)
        this_guess = input('Input a letter: ')
        game_play(this_guess)
        if '-' not in output:
            win_or_lose = f"""

    {choice_word}
    You guessed the word!
    You survived!
            """
    if tries == 0:
        win_or_lose = 'You are hanged!'
    return win_or_lose


print('H A N G M A N')
print('Type "play" to play the game, "exit" to quit: ')
user_choice = input()
while 'exit' not in user_choice:
    print(hangman_game())
    print('Type "play" to play the game, "exit" to quit: ')
    user_choice = input()
