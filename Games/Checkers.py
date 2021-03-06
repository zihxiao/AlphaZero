import math
import copy
from functools import reduce
import numpy as np
from Games.Games import Game


class Checkers(Game):
    EMPTY_SPOT = 0
    P1 = 1
    P2 = 4
    P1_K = 2
    P2_K = 3
    HEIGHT = 8
    WIDTH = 4
    MAX_MOVES = 150

    Symbols = [' ', 'o', 'O', 'X', 'x']

    def __init__(self, old_spots=None):
        """
        Unless specified otherwise,
        the board will be created with a start board configuration.
        the_player_turn=True indicates turn of player P1
        """
        # initialize player and moves
        self.player_turn = True  # true for player one
        self.moves_taken = 0

        # initialize board
        if old_spots is None:
            spots = [[j, j, j, j] for j in [self.P1, self.P1, self.P1, self.EMPTY_SPOT,
                                            self.EMPTY_SPOT, self.P2, self.P2, self.P2]]
        else:
            spots = old_spots
        self.board = np.array(spots, dtype=np.uint8)

        # initialize action space
        action_space = np.zeros((32, 32, 2), dtype=np.uint8)
        for i in range(32):
            for j in range(32):
                action_space[i, j] = np.array([i, j])

        super().__init__(8, 4, 4, action_space, 'Checkers')

    def tile_to_row_col(self, tile):
        """
        Converts tile index to row col index.
        """
        row = math.floor(tile / self.WIDTH)
        col = tile % self.WIDTH
        return np.array([row, col])

    def row_col_to_tile(self, row_col):
        """
        Converts tile index to row col index.
        """
        tile = self.WIDTH * row_col[0] + row_col[1]
        return tile

    def action_to_move(self, action):
        """
        Converts an action from the action space to a 2 by 2 array representing
        a move.
        """
        return np.array([self.tile_to_row_col(action[0]),
                         self.tile_to_row_col(action[1])], dtype=np.uint8)

    def move_to_action(self, move):
        """
        Converts a 2 by 2 array move to an action.
        """
        return np.array([self.row_col_to_tile(move[0]),
                         self.row_col_to_tile(move[1])], dtype=np.uint8)

    def restart(self):
        """
        Resets the current configuration of the game board to the original
        starting position.
        """
        self.board = Checkers().board
        self.terminal = False

    def invert_board(self):
        """
        Rotate the board
        """
        self.board = np.rot90((5 - self.board) % 5, 2)

    def not_spot(self, loc):
        """
        Finds out of the spot at the given location is an actual spot on the game board.
        """
        if len(loc) == 0 or loc[0] < 0 or loc[0] > self.HEIGHT - 1 or loc[1] < 0 or \
                loc[1] > self.WIDTH - 1:
            return True
        else:
            return False

    def get_spot_info(self, loc):
        """
        Gets the information about the spot at the given location.
        """
        return self.board[loc[0]][loc[1]]

    def forward_n_locations(self, start_loc, n, backwards=False):
        """
        Gets the locations possible for moving a piece from a given location diagonally
        forward (or backwards if wanted) a given number of times(without directional change midway).
        """
        if n % 2 == 0:
            temp1 = 0
            temp2 = 0
        elif start_loc[0] % 2 == 0:
            temp1 = 0
            temp2 = 1
        else:
            temp1 = 1
            temp2 = 0

        answer = [[start_loc[0], start_loc[1] + math.floor(n / 2) + temp1],
                  [start_loc[0], start_loc[1] - math.floor(n / 2) - temp2]]

        if backwards:
            answer[0][0] = answer[0][0] - n
            answer[1][0] = answer[1][0] - n
        else:
            answer[0][0] = answer[0][0] + n
            answer[1][0] = answer[1][0] + n

        if self.not_spot(answer[0]):
            return [answer[1]]
        elif self.not_spot(answer[1]):
            return [answer[0]]
        else:
            return answer

    def get_simple_moves(self, start_loc):
        """
        Gets the possible moves a piece can make given that it does not capture any
        opponents pieces.
        """
        next_locations = self.forward_n_locations(start_loc, 1)
        if self.get_spot_info(start_loc) == self.P1_K:
            next_locations.extend(self.forward_n_locations(start_loc, 1, True))

        possible_next_locations = []

        for location in next_locations:
            if self.get_spot_info(location) == self.EMPTY_SPOT:
                possible_next_locations.append(location)

        return [[start_loc, end_spot] for end_spot in possible_next_locations]

    def get_capture_moves(self, start_loc, move_beginnings=None):
        """
        Recursively get all of the possible moves for a piece which involve capturing an
        opponent's piece.
        """
        if move_beginnings is None:
            move_beginnings = [start_loc]

        answer = []

        next1 = self.forward_n_locations(start_loc, 1)
        next2 = self.forward_n_locations(start_loc, 2)
        if self.get_spot_info(start_loc) == self.P1_K:
            # go also backwards if is a king
            next1.extend(self.forward_n_locations(start_loc, 1, True))
            next2.extend(self.forward_n_locations(start_loc, 2, True))

        for j in range(len(next1)):
            # if both spots exist
            if (not self.not_spot(next2[j])) and (not self.not_spot(next1[j])):
                # if next spot is opponent
                if self.get_spot_info(next1[j]) in [self.P2, self.P2_K]:
                    # if next next spot is empty
                    if self.get_spot_info(next2[j]) == self.EMPTY_SPOT:
                        temp_move1 = copy.deepcopy(move_beginnings)
                        temp_move1.append(next2[j])

                        answer_length = len(answer)

                        if next2[j][0] != self.HEIGHT - 1 or self.get_spot_info(start_loc) == self.P1_K:
                            temp_move2 = [start_loc, next2[j]]

                            temp_board = Checkers(copy.deepcopy(self.board))
                            temp_board.step(
                                self.move_to_action(temp_move2), True)

                            answer.extend(temp_board.get_capture_moves(
                                temp_move2[1], temp_move1))

                        if len(answer) == answer_length:
                            answer.append(temp_move1)
        return answer

    def check_win_conditions(self):
        """
        Returns true when a player wins (other player has no pieces left)
        or draw.
        """
        if not self.check_ahead():
            self.terminal = True
            return 1

        if np.any(self.board == self.P2) or np.any(self.board == self.P2_K):
            # if the other player has still pieces left
            return 0
        else:
            # if the other player has no pieces left
            self.terminal = True
            return 1

    def check_ahead(self):
        """
        Check get the legal moves one move ahead.
        """
        temp_game = Checkers(copy.deepcopy(self.board))
        temp_game.invert_board()
        return temp_game.legal_moves()

    def get_piece_locations(self):
        """
        Gets all the pieces of the current player
        """
        piece_locations = np.argwhere(self.board == self.P1).tolist(
        ) + np.argwhere(self.board == self.P1_K).tolist()
        return piece_locations

    def legal_moves(self):
        """
        Gets the possible moves that can be made from the current board configuration.
        """
        actions = []
        piece_locations = self.get_piece_locations()
        capture_moves = []
        try:
            capture_moves = list(reduce(lambda a, b: a + b, list(map(
                self.get_capture_moves, piece_locations))))
        except:
            capture_moves = []

        if len(capture_moves) != 0:
            actions = []
            for capture_move in capture_moves:
                actions.append(self.move_to_action(capture_move))
            return actions

        moves = []
        try:
            moves = list(reduce(lambda a, b: a + b,
                                list(map(self.get_simple_moves, piece_locations))))
        except:
            moves = []
        actions = np.zeros((len(moves), 2))
        for i in range(len(moves)):
            actions[i] = self.move_to_action(moves[i])
        # print(actions.tolist())
        return actions.astype(int).tolist()

    def step(self, action, is_capture_temp=False):
        """
        Makes a given move on the board, and (as long as is wanted) switches the indicator for which players turn it is.
        """
        move = self.action_to_move(action)
        if abs(int(move[0][0]) - int(move[1][0])) == 2:
            for j in range(len(move) - 1):
                if move[j][0] % 2 == 1:
                    if move[j + 1][1] < move[j][1]:
                        middle_y = move[j][1]
                    else:
                        middle_y = move[j + 1][1]
                else:
                    if move[j + 1][1] < move[j][1]:
                        middle_y = move[j + 1][1]
                    else:
                        middle_y = move[j][1]

                self.board[int((move[j][0] + move[j + 1][0]) / 2)
                           ][middle_y] = self.EMPTY_SPOT

        x_end = move[len(move) - 1][0]
        y_end = move[len(move) - 1][1]

        # move it
        if x_end == self.HEIGHT - 1:
            self.board[x_end][y_end] = self.P1_K
        else:
            self.board[x_end][y_end] = self.board[move[0][0]][move[0][1]]

        self.board[move[0][0]][move[0][1]] = self.EMPTY_SPOT

        self.moves_taken += 1
        return self.check_win_conditions()

    def render(self):
        """
        Prints a string representation of the current game board.
        """

        index_columns = "   "
        for j in range(self.WIDTH):
            index_columns += " " + str(j) + "   " + str(j) + "  "
        print(index_columns)

        norm_line = "  |---|---|---|---|---|---|---|---|"
        print(norm_line)

        for j in range(self.HEIGHT):
            temp_line = str(j) + " "
            if j % 2 == 1:
                temp_line += "|///|"
            else:
                temp_line += "|"
            for i in range(self.WIDTH):
                temp_line = temp_line + " " + \
                    self.Symbols[self.board[j, i]] + " |"
                if i != 3 or j % 2 != 1:
                    temp_line = temp_line + "///|"
            print(temp_line)
            print(norm_line)
