import random

import numpy as np

from utils import Utils


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.blocked = False
        self.visited = False
        self.parent = None
        self.children = []

    def get_co_ordinates(self):
        return self.row, self.col


class Maze:

    def __init__(self, n_rows, n_cols, bot=False):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.p_block = 0.3
        self.maze = [[Cell(r, c) for c in range(n_cols)] for r in range(n_rows)]
        if not bot:
            self._create_blockers()
        self.start = self.random_cell()
        self.goal = self.random_cell()

    def _create_blockers(self):
        traversal_stack = []
        while not self.all_cells_visited():
            if len(traversal_stack) == 0:
                traversal_stack.append(self.get_random_unvisited_cell())
                self.maze[traversal_stack[-1].row][traversal_stack[-1].col].visited = True
            valid_neighbors = self.get_neighbors(traversal_stack[-1], blocked=False, visited=False)

            if len(valid_neighbors) == 0:
                traversal_stack.pop()
                continue

            next_step = random.choice(valid_neighbors)
            self.maze[next_step.row][next_step.col].visited = True
            if np.random.random() <= self.p_block:
                self.maze[next_step.row][next_step.col].blocked = True
            else:
                traversal_stack.append(next_step)
        self.reset_visited()

    def get_neighbors(self, cell: Cell, blocked=None, visited=None):
        """
        Gets neighbors that satisfy the conditions listed in the parameters.
        :param cell: The cell for which we need to compute the neighbors
        :param blocked: Whether the neighbor should be blocked or not
        :param visited: Whether the neighbor should be visited or not
        :return:
        """
        blocked_arr = [blocked] if blocked is not None else [True, False]
        visited_arr = [visited] if visited is not None else [True, False]
        r_neigh, c_neigh = Utils.get_neighbor_range(cell, self.n_rows, self.n_cols)
        neighbors = list()
        for i in r_neigh:
            n1 = self.maze[cell.row + i][cell.col]
            if n1.blocked in blocked_arr and n1.visited in visited_arr:
                neighbors.append(n1)

        for j in c_neigh:
            n2 = self.maze[cell.row][cell.col + j]
            if n2.blocked in blocked_arr and n2.visited in visited_arr:
                neighbors.append(n2)

        return neighbors

    def get_random_unvisited_cell(self):
        """
        Gives one random unvisited cell from the maze
        """
        unvisited = list()
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if not self.maze[i][j].visited:
                    unvisited.append(self.maze[i][j])
        return random.choice(unvisited)

    def all_cells_visited(self):
        """
        :return: True if all cells in the maze are marked as visited. Otherwise, False is returned
        """
        for r in self.maze:
            for c in r:
                if not c.visited:
                    return False
        return True

    def random_cell(self):
        while True:
            x = np.random.randint(0, self.n_rows - 1)
            y = np.random.randint(0, self.n_cols - 1)
            if not self.maze[x][y].blocked:
                return self.maze[x][y]

    def get_cell(self, row, col):
        """
        Function to get a particular cell.
        :param row: row number
        :param col: column number
        :return: The cell with the row number and column number
        """
        return self.maze[row][col]

    def reset_visited(self):
        """
        Marks all the cells in the maze as unvisited.
        """
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                self.maze[r][c].visited = False
