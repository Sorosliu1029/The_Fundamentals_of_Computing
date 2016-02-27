"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []

        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        width = self.get_grid_width()
        height = self.get_grid_height()
        visited = [[EMPTY for dummy_col in range(width)]
                  for dummy_row in range(height)]
        distance_field = [[height*width for dummy_col in range(width)]
                          for dummy_row in range(height)]
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)
                visited[human[0]][human[1]] = FULL
                distance_field[human[0]][human[1]] = 0
        elif entity_type == ZOMBIE:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
                visited[zombie[0]][zombie[1]] = FULL
                distance_field[zombie[0]][zombie[1]] = 0
        while len(boundary):
            current_cell = boundary.dequeue()
            if entity_type == HUMAN:
                neighbor_cells = self.four_neighbors(current_cell[0], current_cell[1])
            elif entity_type == ZOMBIE:
                neighbor_cells = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbor_cells:
                if visited[neighbor[0]][neighbor[1]] == EMPTY and self.is_empty(neighbor[0], neighbor[1]):
                    visited[neighbor[0]][neighbor[1]] = FULL
                    boundary.enqueue(neighbor)
                    distance = distance_field[current_cell[0]][current_cell[1]] + 1
                    if distance < distance_field[neighbor[0]][neighbor[1]]:
                        distance_field[neighbor[0]][neighbor[1]] = distance
        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        move_destination = []
        for human in self._human_list:
            available_cells = self.eight_neighbors(human[0], human[1])
            available_cells += [human]
            move_to = human
            max_distance = -1
            for cell in available_cells:
                if zombie_distance_field[cell[0]][cell[1]] > max_distance and self.is_empty(cell[0], cell[1]):
                    max_distance = zombie_distance_field[cell[0]][cell[1]]
                    move_to = cell
            move_destination.append(move_to)
        self._human_list = move_destination

    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        move_destination = []
        for zombie in self._zombie_list:
            available_cells = self.four_neighbors(zombie[0], zombie[1])
            available_cells += [zombie]
            move_to = zombie
            min_distance = self.get_grid_width() * self.get_grid_height()
            for cell in available_cells:
                if human_distance_field[cell[0]][cell[1]] < min_distance and self.is_empty(cell[0], cell[1]):
                    min_distance = human_distance_field[cell[0]][cell[1]]
                    move_to = cell
            move_destination.append(move_to)
        self._zombie_list = move_destination

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
