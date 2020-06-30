border = '-' * 9
row1 = ["_", "_", "_"]
row2 = ["_", "_", "_"]
row3 = ["_", "_", "_"]
game_field = [row3, row2, row1]


def print_field():
    print(f"""
    {border}
    | {" ".join(row1)} |
    | {" ".join(row2)} |
    | {" ".join(row3)} |
    {border}
    """)


def win_options():
    win_option1 = [game_field[0][0], game_field[0][1], game_field[0][2]]
    win_option2 = [game_field[0][0], game_field[1][0], game_field[2][0]]
    win_option3 = [game_field[0][0], game_field[1][1], game_field[2][2]]
    win_option4 = [game_field[0][1], game_field[1][1], game_field[2][1]]
    win_option5 = [game_field[0][2], game_field[1][2], game_field[2][2]]
    win_option6 = [game_field[0][2], game_field[1][1], game_field[2][0]]
    win_option7 = [game_field[1][0], game_field[1][1], game_field[1][2]]
    win_option8 = [game_field[2][0], game_field[2][1], game_field[2][2]]
    return [win_option1, win_option2, win_option3, win_option4, win_option5, win_option6, win_option7, win_option8]


def game_outcomes(this_game):
    """
    this returns the game state
    """
    x_wins = False
    o_wins = False
    game_result = None
    field_check = []

    for win_option in win_options():
        if win_option == ['X', 'X', 'X']:
            x_wins = True
        elif win_option == ['O', 'O', 'O']:
            o_wins = True

    for row in this_game:
        for spot in row:
            field_check.append(spot)

    if x_wins:
        game_result = 'X wins'
    elif o_wins:
        game_result = 'O wins'
    elif "_" not in field_check:
        game_result = 'Draw'
    else:
        pass

    return game_result


def player_move():
    move = 0
    game_result = None
    while game_result is None:
        print("Enter the coordinates: ")
        coordinates = input().split(" ", 1)
        try:
            bool_coordinates = [0 < int(n) < 4 for n in coordinates]
            if all(bool_coordinates) is False:
                print("Coordinates should be from 1 to 3!")
            elif all(bool_coordinates) is True:
                x = int(coordinates[0]) - 1
                y = int(coordinates[1]) - 1
                y_coordinate = game_field[y]
                target_cell = y_coordinate[x]
                if "_" not in target_cell:
                    print("This cell is occupied! Choose another one!")
                elif move == 0:
                    game_field[y][x] = 'X'
                    move += 1
                    print_field()
                    game_result = game_outcomes(game_field)
                elif move == 1:
                    game_field[y][x] = 'O'
                    move -= 1
                    print_field()
                    game_result = game_outcomes(game_field)
        except ValueError:
            print("You should enter numbers!")


print_field()

player_move()

print(game_outcomes(game_field))