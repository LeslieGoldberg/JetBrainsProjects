from random import randint
from math import inf

border = '-' * 9


def start_game():
    game_parameters = False
    player_options = ['user', 'easy', 'medium', 'hard']
    while game_parameters is False:
        game_parameters = input('Input command: ').split(" ")
        if game_parameters[0] == 'exit':
            exit()
        elif game_parameters[0] != 'start':
            print('Bad parameters!')
            game_parameters = False
        elif len(game_parameters) != 3:
            print('Bad parameters!')
            game_parameters = False
        elif game_parameters[1] and game_parameters[2] not in player_options:
            print('Bad parameters!')
            game_parameters = False
    player_x = game_parameters[1]
    player_o = game_parameters[2]
    return player_x, player_o


def game_field_coordinate(*coordinates_list):
    coordinate_list = [num for num in coordinates_list]
    if coordinate_list == ['1', '1']:
        return 6
    elif coordinate_list == ['1', '2']:
        return 3
    elif coordinate_list == ['1', '3']:
        return 0
    elif coordinate_list == ['2', '1']:
        return 7
    elif coordinate_list == ['2', '2']:
        return 4
    elif coordinate_list == ['2', '3']:
        return 1
    elif coordinate_list == ['3', '1']:
        return 8
    elif coordinate_list == ['3', '2']:
        return 5
    elif coordinate_list == ['3', '3']:
        return 2


def win_options(game_field):
    win_option0 = [game_field[0], game_field[1], game_field[2]]
    win_option1 = [game_field[3], game_field[4], game_field[5]]
    win_option2 = [game_field[6], game_field[7], game_field[8]]
    win_option3 = [game_field[0], game_field[3], game_field[6]]
    win_option4 = [game_field[1], game_field[4], game_field[7]]
    win_option5 = [game_field[2], game_field[5], game_field[8]]
    win_option6 = [game_field[0], game_field[4], game_field[8]]
    win_option7 = [game_field[2], game_field[4], game_field[6]]
    return [win_option0, win_option1, win_option2, win_option3, win_option4, win_option5, win_option6, win_option7]


def print_field(field):
    print(f"""
    {border}
    | {" ".join(field[0:3])} |
    | {" ".join(field[3:6])} |
    | {" ".join(field[6:])} |
    {border}
    """)


class TicTacToe:
    def __init__(self, player1, player2):
        self.game_field = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.player1 = player1
        self.player2 = player2

    def __repr__(self):
        return "TicTacToe({}, {})".format(self.player1, self.player2)

    def game_outcomes(self):
        """
        this returns the game state
        """
        game_result = None
        field_check = []

        for spot in self.game_field:
            field_check.append(spot)

        for win_option in win_options(self.game_field):
            if win_option == ['X', 'X', 'X']:
                game_result = 'X wins'
            elif win_option == ['O', 'O', 'O']:
                game_result = 'O wins'
        if " " not in field_check:
            game_result = 'Draw'

        return game_result

    def player_move(self, x_or_o):
        make_move = False
        while make_move is False:
            print("Enter the coordinates: ")
            coordinates = input().split(" ", 1)
            try:
                bool_coordinates = [0 < int(n) < 4 for n in coordinates]
                if all(bool_coordinates) is False:
                    print("Coordinates should be from 1 to 3!")
                elif all(bool_coordinates) is True:
                    target_cell = game_field_coordinate(*coordinates)
                    if " " not in self.game_field[target_cell]:
                        print("This cell is occupied! Choose another one!")
                    else:
                        self.game_field[target_cell] = x_or_o
                        make_move = True
            except ValueError:
                print("You should enter numbers!")

    def game_play(self):
        print_field(self.game_field)
        game_result = None
        move = 0
        while game_result is None:
            if move == 0:
                if self.player1 == 'user':
                    self.player_move(x_or_o='X')
                else:
                    pass
                print_field(self.game_field)
                move += 1
                game_result = self.game_outcomes()
            elif move == 1:
                if self.player2 == 'user':
                    self.player_move(x_or_o='O')
                else:
                    pass
                print_field(self.game_field)
                move -= 1
                game_result = self.game_outcomes()

        return game_result


class EasyComp(TicTacToe):
    def comp_easy_move(self, x_or_o):
        print('Making move level "easy"')
        coordinate = randint(0, 8)
        target_cell = self.game_field[coordinate]
        while " " not in target_cell:
            coordinate = randint(0, 8)
            target_cell = self.game_field[coordinate]
        self.game_field[coordinate] = x_or_o

    def game_play(self):
        print_field(self.game_field)
        game_result = None
        move = 0
        while game_result is None:
            if move == 0:
                if self.player1 == 'user':
                    self.player_move(x_or_o='X')
                elif self.player1 == 'easy':
                    self.comp_easy_move(x_or_o='X')
                print_field(self.game_field)
                move += 1
                game_result = self.game_outcomes()
            elif move == 1:
                if self.player2 == 'user':
                    self.player_move(x_or_o='O')
                elif self.player2 == 'easy':
                    self.comp_easy_move(x_or_o='O')
                print_field(self.game_field)
                move -= 1
                game_result = self.game_outcomes()

        return game_result


def find_empty_space(*coordinates):
    coordinate_list = "".join([str(num) for num in coordinates])
    empty_cell0 = ['00', '30', '60']
    empty_cell1 = ['01', '40']
    empty_cell2 = ['02', '50', '70']
    empty_cell3 = ['10', '31']
    empty_cell4 = ['11', '41', '61', '71']
    empty_cell5 = ['12', '51']
    empty_cell6 = ['20', '32', '72']
    empty_cell7 = ['21', '42']
    empty_cell8 = ['22', '52', '62']
    empty_cell = None
    if coordinate_list in empty_cell0:
        empty_cell = 0
    elif coordinate_list in empty_cell1:
        empty_cell = 1
    elif coordinate_list in empty_cell2:
        empty_cell = 2
    elif coordinate_list in empty_cell3:
        empty_cell = 3
    elif coordinate_list in empty_cell4:
        empty_cell = 4
    elif coordinate_list in empty_cell5:
        empty_cell = 5
    elif coordinate_list in empty_cell6:
        empty_cell = 6
    elif coordinate_list in empty_cell7:
        empty_cell = 7
    elif coordinate_list in empty_cell8:
        empty_cell = 8
    return empty_cell


class MediumGame(TicTacToe):
    def find_winning_space(self, x_or_o):
        option_number = 0
        total_options = len(win_options(self.game_field))
        empty_spot = None
        make_a_move = False
        while make_a_move is False:
            for option in win_options(self.game_field):
                my_count = 0
                space_count = 0
                for space in option:
                    if space == ' ':
                        empty_spot = space_count
                    elif space == x_or_o:
                        my_count += 1
                        space_count += 1
                if my_count == 2 and space_count == 1:
                    make_a_move = True
                    break
                option_number += 1
            if option_number == total_options:
                break
        if make_a_move is True:
            coordinates = [option_number, empty_spot]
            target_cell = find_empty_space(*coordinates)
            self.game_field[target_cell] = x_or_o
        return make_a_move

    def find_blocking_space(self, x_or_o):
        option_number = 0
        empty_spot = None
        total_options = len(win_options(self.game_field))
        make_a_move = False
        while make_a_move is False:
            for option in win_options(self.game_field):
                opponent_count = 0
                space_count = 0
                for space in option:
                    if space == ' ':
                        empty_spot = space_count
                    elif space != x_or_o:
                        opponent_count += 1
                        space_count += 1
                if opponent_count == 2 and space_count == 1:
                    make_a_move = True
                    break
                option_number += 1
            if option_number == total_options:
                break
        if make_a_move is True:
            coordinates = [option_number, empty_spot]
            target_cell = find_empty_space(*coordinates)
            self.game_field[target_cell] = x_or_o
        return make_a_move

    def comp_medium_move(self, x_or_o):
        move_made = False
        while move_made is False:
            if self.find_winning_space(x_or_o) is True:
                move_made = True
            elif self.find_blocking_space(x_or_o) is True:
                move_made = True
            else:
                coordinate = randint(0, 8)
                target_cell = self.game_field[coordinate]
                while " " not in target_cell:
                    coordinate = randint(0, 8)
                    target_cell = self.game_field[coordinate]
                self.game_field[coordinate] = x_or_o
                move_made = True
        print('Making move level "medium"')

    def game_play(self):
        print_field(self.game_field)
        game_result = None
        move = 0
        while game_result is None:
            if move == 0:
                if self.player1 == 'user':
                    self.player_move(x_or_o='X')
                elif self.player1 == 'medium':
                    self.comp_medium_move(x_or_o='X')
                print_field(self.game_field)
                move += 1
                game_result = self.game_outcomes()
            elif move == 1:
                if self.player2 == 'user':
                    self.player_move(x_or_o='O')
                elif self.player2 == 'medium':
                    self.comp_medium_move(x_or_o='O')
                print_field(self.game_field)
                move -= 1
                game_result = self.game_outcomes()

        return game_result


def wins(state, player):
    win_state = win_options(state)
    if [player, player, player] in win_state:
        return True
    else:
        return False


def available_spots(game_field):
    available_spots = []
    counter = 0
    for spot in game_field:
        if spot == ' ':
            available_spots.append(counter)
        counter += 1
    return available_spots


def render(state, c_choice, h_choice):
    chars = {-10: h_choice, 10: c_choice, ' ': ' '}
    field = []
    for cell in state:
        symbol = chars[cell]
        field.append(symbol)
    print_field(field)


class HardGame(TicTacToe):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.HUMAN = -10
        self.COMP = 10

    def evaluate(self, state):
        if wins(state, self.COMP):
            score = 10
        elif wins(state, self.HUMAN):
            score = -10
        else:
            score = 0
        return score

    def game_over(self, state):
        return wins(state, self.HUMAN) or wins(state, self.COMP)

    def valid_move(self, move):
        if move in available_spots(self.game_field):
            return True
        else:
            return False

    def set_move(self, move, player):
        if self.valid_move(move):
            self.game_field[move] = player
            return True
        else:
            return False

    def hard_game_outcomes(self, c_choice, h_choice):
        """
        this returns the game state
        """
        x_wins = False
        o_wins = False
        game_result = None

        chars = {-10: h_choice, 10: c_choice, ' ': ' '}
        field = []
        for cell in self.game_field:
            symbol = chars[cell]
            field.append(symbol)

        for win_option in win_options(field):
            if win_option == ['X', 'X', 'X']:
                x_wins = True
            elif win_option == ['O', 'O', 'O']:
                o_wins = True

        if x_wins is True:
            game_result = 'X wins'
        elif o_wins is True:
            game_result = 'O wins'
        elif ' ' not in field:
            game_result = 'Draw'

        return game_result

    def mini_max(self, state, depth, player):
        if player == self.COMP:
            best = [-1, -inf]
        else:
            best = [-1, inf]

        if depth == 0 or self.game_over(state):
            score = self.evaluate(state)
            return [-1, score]

        for spot in available_spots(state):
            index = spot
            state[index] = player
            score = self.mini_max(state, depth - 1, -player)
            state[index] = ' '
            score[0] = index

            if player == self.COMP:
                if score[1] > best[1]:
                    best = score
            else:
                if score[1] < best[1]:
                    best = score

        return best

    def ai_turn(self, c_choice, h_choice):
        depth = len(available_spots(self.game_field))
        if depth == 0 or wins(self.game_field, self.COMP):
            return

        if depth == 9:
            spot = randint(0, 8)
        else:
            move = self.mini_max(self.game_field, depth, self.COMP)
            spot = move[0]

        self.set_move(spot, self.COMP)
        print('Making move level "hard"')
        render(self.game_field, c_choice, h_choice)

    def human_turn(self, c_choice, h_choice):
        make_move = False
        while make_move is False:
            print("Enter the coordinates: ")
            coordinates = input().split(" ", 1)
            try:
                bool_coordinates = [0 < int(n) < 4 for n in coordinates]
                if all(bool_coordinates) is False:
                    print("Coordinates should be from 1 to 3!")
                elif all(bool_coordinates) is True:
                    target_cell = game_field_coordinate(*coordinates)
                    if self.valid_move(target_cell) is False:
                        print("This cell is occupied! Choose another one!")
                    else:
                        self.set_move(target_cell, self.HUMAN)
                        make_move = True
            except ValueError:
                print("You should enter numbers!")
        render(self.game_field, c_choice, h_choice)

    def game_play(self):
        h_choice = ''
        c_choice = ''
        choice = 0

        if self.player1 == 'user':
            h_choice = 'X'
        elif self.player2 == 'user':
            h_choice = 'O'

        if self.player1 == 'hard':
            c_choice = 'X'
        elif self.player2 == 'hard':
            c_choice = 'O'

        while len(available_spots(self.game_field)) > 0 and self.game_over(self.game_field) is False:
            if c_choice == 'X' and choice == 0:
                self.ai_turn(c_choice, h_choice)
                choice = 1
            elif choice == 0:
                self.human_turn(c_choice, h_choice)
                choice += 1
            elif choice == 1:
                self.ai_turn(c_choice, h_choice)
                choice -= 1

        if self.game_over(self.game_field) or len(available_spots(self.game_field)) == 0:
            return self.hard_game_outcomes(c_choice, h_choice)


#    def players(self):
# WHAT IF BOTH PLAYERS ARE AI?
#        if self.player1 == self.player2:
#            self.ai_player_1 = 'X'
#            self.ai_player_2 = 'O'


players = start_game()
if 'easy' in players:
    game = EasyComp(players[0], players[1])
elif 'medium' in players:
    game = MediumGame(players[0], players[1])
elif 'hard' in players:
    game = HardGame(players[0], players[1])
else:
    game = TicTacToe(players[0], players[1])
end_of_play = game.game_play()
print(end_of_play)
