"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        assert target_row > 1, 'target_row invalid'
        result = True
        if self._grid[target_row][target_col] != 0:
            result = False
        for row in range(target_row+1, self._height):
            for col in range(self._width):
                solved_value = (col + self._width * row)
                if solved_value != self._grid[row][col]:
                    result = False
        for col in range(target_col+1, self._width):
            solved_value = (col + self._width * target_row)
            if solved_value != self._grid[target_row][col]:
                result = False
        return result

    def position_tile(self, target_row, target_col, cur_row, cur_col, need_ld=True):
        """
        helper function for solve_interior_tile and solve_col0_tile
        """
        move_str = ''
        if cur_row == target_row:
            if cur_col < target_col:
                move_str += 'l' * (target_col - cur_col)
                if target_col - cur_col > 1:
                    move_str += 'ur'
                    move_str += 'druldru' * (target_col - cur_col - 1)
                else:
                    move_str += 'ur' if not need_ld else ''
                    need_ld = False
            else:
                move_str += 'r' * (cur_col - target_col)
                if cur_col - target_col > 1:
                    move_str += 'ul'
                    move_str += 'dlurdlu' * (cur_col - target_col - 1)
                else:
                    need_ld = False
        else:
            move_str += 'u' * (target_row - cur_row)
            if cur_col < target_col:
                move_str += ('l' * (target_col - cur_col) + 'dru')
                move_str += 'druldru' * (target_col - cur_col - 1)
                move_str += 'lddru' * (target_row - cur_row - 1)
            elif cur_col > target_col:
                move_str += ('r' * (cur_col - target_col) + 'dlu')
                move_str += 'dlurdlu' * (cur_col - target_col - 1)
                move_str += 'lddru' * (target_row - cur_row - 1)
            else:
                move_str += 'lddru' * (target_row - cur_row - 1)
        if need_ld:
            move_str += 'ld'
        return move_str

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        cur_row, cur_col = self.current_position(target_row, target_col)
        move_str = self.position_tile(target_row, target_col, cur_row, cur_col)
        self.update_puzzle(move_str)
        return move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_str = 'ur'
        self.update_puzzle(move_str)
        cur_row, cur_col = self.current_position(target_row, 0)
        if cur_row == target_row and cur_col == 0:
            move_str += 'r' * (self._width - 2)
        else:
            move_str += self.position_tile(target_row-1, 1, cur_row, cur_col)
            move_str += 'ruldrdlurdluurddlur'
            move_str += 'r' * (self._width - 2)
        self.update_puzzle(move_str[2:])
        return move_str

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        result = True
        if self._grid[0][target_col] != 0:
            result = False
        if self._grid[1][target_col] != (target_col + self._width * 1):
            result = False
        for row in range(2, self._height):
            for col in range(self._width):
                solved_value = (col + self._width * row)
                if solved_value != self._grid[row][col]:
                    result = False
        for row in (0, 1):
            for col in range(target_col+1, self._width):
                solved_value = (col + self._width * row)
                if solved_value != self._grid[row][col]:
                    result = False
        return result

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        result = True
        if self._grid[1][target_col] != 0:
            result = False
        for row in range(2, self._height):
            for col in range(self._width):
                solved_value = (col + self._width * row)
                if solved_value != self._grid[row][col]:
                    result = False
        for row in (0, 1):
            for col in range(target_col+1, self._width):
                solved_value = (col + self._width * row)
                if solved_value != self._grid[row][col]:
                    result = False
        return result

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move_str = 'ld'
        self.update_puzzle(move_str)
        cur_row, cur_col = self.current_position(0, target_col)
        if cur_row == 0 and cur_col == target_col:
            return move_str
        else:
            move_str += self.position_tile(1, target_col-1, cur_row, cur_col)
            move_str += 'urdlurrdluldrruld'
        self.update_puzzle(move_str[2:])
        return move_str

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        cur_row, cur_col = self.current_position(1, target_col)
        move_str = self.position_tile(1, target_col, cur_row, cur_col, need_ld=False)
        self.update_puzzle(move_str)
        return move_str

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        cur_row, cur_col = self.current_position(0, 0)
        move_str = 'u' * cur_row + 'l' * cur_col
        self.update_puzzle(move_str)
        if self.check_2x2_solved():
            return move_str
        else:
            while not self.check_2x2_solved():
                move_str += 'rdlu'
                self.update_puzzle('rdlu')
        return move_str

    def check_2x2_solved(self):
        """
        check if the top left 2*2 puzzle is solved
        """
        return self._grid[0][0] == 0 and self._grid[0][1] == 1 \
               and self._grid[1][0] == self._width*1 and self._grid[1][1] == (1 + self._width * 1)

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        cur0_row, cur0_col = self.current_position(0, 0)
        move_str = 'd' * (self._height - cur0_row - 1) + 'r' * (self._width - cur0_col - 1)
        self.update_puzzle(move_str)
        for row in range(self._height-1, 1, -1):
            for col in range(self._width-1, -1, -1):
                assert self.lower_row_invariant(row, col)
                if col != 0:
                    move_str += self.solve_interior_tile(row, col)
                else:
                    move_str += self.solve_col0_tile(row)
        for col in range(self._width-1, 1, -1):
            assert self.row1_invariant(col)
            move_str += self.solve_row1_tile(col)
            assert self.row0_invariant(col)
            move_str += self.solve_row0_tile(col)
        move_str += self.solve_2x2()
        return move_str

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]))
