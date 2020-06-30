import random


def begin_game_seq(user_name):
    score = 0
    with open('rating.txt', 'r') as file:
        for line in file:
            if user_name in line:
                score = int(line.split(' ')[-1])
    return score


def game_options(user_list):
    comp_options = ['rock', 'paper', 'scissors']
    if user_list:
        comp_options = user_list.split(',')
    return comp_options


def winning_combos(user_list):
    options = game_options(user_list)
    i_win_if = {}
    for x in options:
        x_index = int(options.index(x))
        total_items = len(options)
        term = x_index - int(total_items / 2) - 1
        if term >= 0:
            i_win_if[x] = options[x_index - 1:term:-1]
        elif x_index == 0:
            i_win_if[x] = options[-1:term:-1]
        elif term < 0:
            i_win_if[x] = options[x_index - 1::-1]
            bonus = options[-1:term: -1]
            for i in bonus:
                i_win_if[x].append(i)

    print("Okay, let's start")
    return i_win_if


def rock_paper_scissors_game(comp_options, user_input, i_win_if):
    global rating
    comp_choice = random.choice(comp_options)
    line = False
    if user_input == '!rating':
        line = f'Your rating: {rating}'
    elif comp_choice == user_input:
        rating += 50
        line = f"There is a draw ({comp_choice})"
    elif comp_choice in i_win_if[user_input]:
        rating += 100
        line = f'Well done. Computer chose {comp_choice} and failed'
    elif user_input in i_win_if[comp_choice]:
        line = f'Sorry, but computer chose {comp_choice}'
    return line


name = input('Enter your name: ')
print(f'Hello, {name}')

rating = begin_game_seq(name)
game_list = input()
computer = game_options(game_list)
user_options = [x for x in computer]
user_options.append('!rating')
i_win = winning_combos(game_list)

user_choice = input()
while '!exit' not in user_choice:
    if user_choice in user_options:
        print(rock_paper_scissors_game(computer, user_choice, i_win))
    else:
        print('Invalid input')
    user_choice = input()
print('Bye!')
