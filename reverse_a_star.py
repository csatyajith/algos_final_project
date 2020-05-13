from typing import Optional

from maze import Maze
from maze_visualizer import MazeVisualization
from bot import Bot
from priority_queue import PriorityQueue
from utils import Utils


class ReverseAStar:

    def __init__(self, maze=Optional[Maze], n_rows=None, n_cols=None):
        if not maze:
            self.maze = Maze(n_rows, n_cols)
        else:
            self.maze = maze
        self.bot = Bot(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.goal, self.maze)
        self.pop_counter = 0

    def compute_path(self, queue, heuristic):
        count = 1
        while 0 != len(queue):
            c = queue.pop()
            self.pop_counter += 1
            c.cell.visited = True
            valid_neighbors = self.bot.bot_maze.get_neighbors(c.cell, blocked=False, visited=False)
            if c.cell.get_co_ordinates() == self.bot.pos.get_co_ordinates():
                self.bot.bot_maze.reset_visited()
                path = Utils.get_traversal_path(c.cell, reverse_a_star=True)
                path.append(self.bot.bot_maze.goal)
                return path
            for item in valid_neighbors:
                queue.push(count, heuristic[item.row][item.col], item, c.cell)
            count = count + 1
        return None

    def run_reverse_a_star(self, show_maze = False):

        if show_maze:
            maze_vis = MazeVisualization(self.maze)
        re_compute = True
        print("Bot's destination is - row: {}, col: {}".format(self.maze.goal.row, self.maze.goal.col))
        traversed_path = list()
        while re_compute:
            manhattan_heuristic = Utils.compute_heuristic(self.maze, self.bot.pos)
            start_row = self.maze.goal.row
            start_col = self.maze.goal.col
            my_queue = PriorityQueue()
            my_queue.push(0, manhattan_heuristic[start_row][start_col],
                          self.bot.bot_maze.get_cell(start_row, start_col), None)
            path = self.compute_path(my_queue, manhattan_heuristic)
            if path is None:
                print("Path does not exist")
                return None, None
            traversed_path.extend(self.bot.traverse_path(path))
            if self.bot.pos.get_co_ordinates() == self.maze.goal.get_co_ordinates():
                re_compute = False

        if show_maze:
            Utils.print_path(traversed_path, maze_vis, "Reverse A*", self.maze.start, self.maze.goal)
            maze_vis.show_maze()
        return self.pop_counter, len(traversed_path)

    def reset_bot(self):
        self.bot = Bot(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.goal, self.maze)
