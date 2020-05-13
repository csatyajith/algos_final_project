import pickle
import random


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def load_mazes():
        with open("mazes", "rb") as mazes_file:
            return pickle.load(mazes_file)

    @staticmethod
    def load_random_maze():
        with open("mazes", "rb") as mazes_file:
            mazes = pickle.load(mazes_file)
        return random.choice(mazes)

    @staticmethod
    def compute_heuristic(maze, target):
        rows, cols = (maze.n_rows, maze.n_cols)
        goal = target
        heuristic_arr = [[(abs(goal.col - i) + abs(goal.row - j)) for i in range(cols)] for j in range(rows)]
        return heuristic_arr

    @staticmethod
    def print_path(path, mazevis, algo_name, start, end):
        count = 0
        for cell in path[:-1]:
            if cell.get_co_ordinates() not in [start.get_co_ordinates(), end.get_co_ordinates()]:
                mazevis.fill_cell(cell.row, cell.col)
                count += 1
        print("Total {} moves are: {} \n".format(algo_name, count))

    @staticmethod
    def get_traversal_path(target, reverse_a_star=False):
        path = list()
        path_cell = target
        while path_cell.parent is not None:
            path.append(path_cell)
            path_cell = path_cell.parent
        if not reverse_a_star:
            path.reverse()
        return path

    @staticmethod
    def get_neighbor_range(cell, n_rows, n_cols):
        accepted_rows = [-1, 1]
        accepted_cols = [-1, 1]
        if cell.row == n_rows - 1:
            accepted_rows = [-1]
        elif cell.row == 0:
            accepted_rows = [1]
        if cell.col == n_cols - 1:
            accepted_cols = [-1]
        elif cell.col == 0:
            accepted_cols = [1]

        return accepted_rows, accepted_cols
