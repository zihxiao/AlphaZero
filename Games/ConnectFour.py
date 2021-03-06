import numpy as np
from Games.Games import Game


class ConnectFour(Game):

    def __init__(self):
        self.board = np.zeros((6, 7), dtype=np.uint8)
        self.search_time = 8
        action_space = np.arange(0, 7)
        super().__init__(6, 7, 2, action_space, 'ConnectFour')

    def restart(self):
        super().restart()
        self.board = np.zeros((6, 7), dtype=np.uint8)

    def is_valid(self, action):
        if self.board[0, action] == 0:
            return True
        else:
            return False

    def legal_moves(self):
        return np.where(self.board[0] == 0)[0].tolist()

    def invert_board(self):
        self.board = (3 - self.board) % 3

    def step(self, action):
        """
        Args:
            action(int): a valid action
        Returns:
            reward(int) a integer which is either -1,0, or 1

        self.board    is updated in the process
        self.terminal is updated in the process
        """

        # insert
        col_index = action  # action is in range 0 - 6
        row_index = (self.board[:, col_index] != 0).argmax(
            axis=0) - 1  # subtract one from index of top filled space
        self.board[row_index][col_index] = 1

        # to check for 4 in a row horizontal
        a = 0
        for col in range(7):
            if self.board[row_index][col] == 1:
                a = a + 1
            else:
                a = 0
            if a == 4:
                self.terminal = True
                return +1

        # to check for 4 in a row vertical
        a = 0
        for row in range(6):
            if self.board[row][col_index] == 1:
                a = a + 1
            else:
                a = 0
            if a == 4:
                self.terminal = True
                return +1

        # diagonal top-left to bottom-right
        col = col_index - row_index
        a = 0
        for row in range(6):
            if col >= 0 and col < 7:
                if self.board[row][col] == 1:
                    a = a + 1
                else:
                    a = 0
                if a == 4:
                    self.terminal = True
                    return 1
            col += 1

        # diagonal bottom-left to top-right
        col = col_index + row_index
        a = 0
        for row in range(6):
            if col >= 0 and col < 7:
                if self.board[row][col] == 1:
                    a = a + 1
                else:
                    a = 0
                if a == 4:
                    self.terminal = True
                    return 1
            col -= 1

        # checks if board is filled completely
        if not np.any(self.board == 0):
            self.terminal = True

        return 0

    def render(self):
        """
        print to screen the full board nicely
        """

        for i in range(6):
            print('\n|', end="")
            for j in range(7):
                if self.board[i][j] == 1:
                    print(' X |', end="")
                elif self.board[i][j] == 0:
                    print('   |', end="")
                else:
                    print(' O |', end="")
        print('\n')
