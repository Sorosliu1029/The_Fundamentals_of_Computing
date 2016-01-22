"""
Clone of 2048 game.
"""
import random
# import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    start_idx = 0
    end_idx = 1
    dummy_line = [value for value in line if value]
    if len(dummy_line) < 2:
        return dummy_line + [0] * (len(line)-len(dummy_line))
    result = []
    while end_idx < len(dummy_line):
        if dummy_line[start_idx] == dummy_line[end_idx]:
            result.append(dummy_line[start_idx] * 2)
            start_idx = end_idx + 1
            end_idx += 1
        else:
            result.append(dummy_line[start_idx])
            start_idx = end_idx
        if end_idx == len(dummy_line)-1:
            result.append(dummy_line[end_idx])
        end_idx += 1
    return result + [0] * (len(line) - len(result))

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.__grid_height__ = grid_height
        self.__grid_width__ = grid_width
        self.__board__ = []
        self.reset()
        self.__direction_for_first__ = {}
        self.get_direction_dict()

    def get_direction_dict(self):
        """
        pre-compute the direction dictionary for further use
        :return: None
        """
        self.__direction_for_first__[UP] = [(0, dummy_j) for dummy_j in range(self.__grid_width__)]
        self.__direction_for_first__[DOWN] = [(self.__grid_height__-1, dummy_j) for dummy_j in range(self.__grid_width__)]
        self.__direction_for_first__[LEFT] = [(dummy_i, 0) for dummy_i in range(self.__grid_height__)]
        self.__direction_for_first__[RIGHT] = [(dummy_i, self.__grid_width__-1) for dummy_i in range(self.__grid_height__)]

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        for dummy_row in range(self.__grid_height__):
            self.__board__.append([0] * self.__grid_width__)
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        result = ''
        for row in self.__board__:
            result += (str(row) + '\n')
        return result

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.__grid_height__

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.__grid_width__

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        init = self.__direction_for_first__[direction]
        drc = OFFSETS[direction]
        if direction == UP or direction == DOWN:
            num_steps = self.__grid_height__
        else:
            num_steps = self.__grid_width__
        changed = False
        for tile in init:
            raw_list = []
            for step in range(num_steps):
                row = tile[0] + step * drc[0]
                col = tile[1] + step * drc[1]
                raw_list.append(self.__board__[row][col])
            merged_list = merge(raw_list)
            for step in range(num_steps):
                row = tile[0] + step * drc[0]
                col = tile[1] + step * drc[1]
                if self.__board__[row][col] != merged_list[step]:
                    self.__board__[row][col] = merged_list[step]
                    changed = True
        if changed:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        while True:
            selected_i = random.randrange(0, self.__grid_height__)
            selected_j = random.randrange(0, self.__grid_width__)
            if not self.__board__[selected_i][selected_j]:
                self.__board__[selected_i][selected_j] = 2 if random.randrange(0, 10) else 4
                break

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.__board__[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.__board__[row][col]

# poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

game = TwentyFortyEight(4, 4)
print game
game.move(UP)
print game
game.move(DOWN)
print game
game.move(LEFT)
print game
game.move(RIGHT)
print game
game.move(RIGHT)
print game
game.move(LEFT)
print game
game.move(DOWN)
print game
game.move(UP)
print game