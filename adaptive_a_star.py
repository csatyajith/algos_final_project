from typing import Optional, List

from bot import Bot
from maze import Maze, Cell
from maze_visualizer import MazeVisualization
from priority_queue import PriorityQueue
from utils import Utils
import time

class AdaptiveAStar:

    def __init__(self, maze=Optional[Maze], n_rows=None, n_cols=None):
        if not maze:
            self.maze = Maze(n_rows, n_cols)
        else:
            self.maze = maze
        self.bot = Bot(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.goal, self.maze)
        self.heuristics = Utils.compute_heuristic(self.maze, self.maze.goal)
        self.pop_counter = 0
        self.time_end = None

    def update_heuristics(self, traversal_path: List[Cell]):
        count = 0
        traversal_path.reverse()
        print("\n")
        for path_cell in traversal_path[1:]:
            for i in path_cell.children:
                self.heuristics[i.row][i.col] = count
                print("New heuristic for ({}, {}) is {}".format(i.row, i.col, count))
            count += 1
        print("Adaptive A star moves", count, "\n")

    def find_path(self, queue):
        """
        Finds the path using the queue as the input. Queue is a priority queue.
        :param queue:
        :return: Returns a sample path.
        """
        moves = 1
        while 0 != len(queue):
            curr = queue.pop()
            self.pop_counter += 1
            if curr.cell.parent is not None:
                if curr.cell not in curr.cell.parent.children:
                    curr.cell.parent.children.append(curr.cell)
            curr.cell.visited = True
            valid_neighbors = self.bot.bot_maze.get_neighbors(curr.cell, blocked=False, visited=False)
            if curr.cell.get_co_ordinates() == self.bot.bot_maze.goal.get_co_ordinates():
                self.bot.bot_maze.reset_visited()
                return Utils.get_traversal_path(curr.cell)
            for item in valid_neighbors:
                queue.push(moves, self.heuristics[item.row][item.col], item, curr.cell)
            moves = moves + 1
        return None

    def execute_algorithm(self, show_maze=False):
        if show_maze:
            maze_vis = MazeVisualization(self.maze)
        traversed_path = [self.bot.pos]
        re_compute = True
        print("Bot's destination is - row: {}, col: {}".format(self.maze.goal.row, self.maze.goal.col))
        while re_compute:
            start_row = self.bot.pos.row
            start_col = self.bot.pos.col
            my_queue = PriorityQueue()
            my_queue.push(0, self.heuristics[start_row][start_col],
                          self.bot.bot_maze.get_cell(start_row, start_col),
                          None)
            path = self.find_path(my_queue)
            if path is None:
                print("Path does not exists\n")
                return None, None
            traversed_path.extend(self.bot.traverse_path(path))
            if self.bot.pos.get_co_ordinates() == self.maze.goal.get_co_ordinates():
                re_compute = False
        self.time_end = time.time()
        print("Adaptive * path exists\n")
        self.update_heuristics(traversed_path)
        if show_maze:
            Utils.print_path(traversed_path, maze_vis, "Adaptive A*", self.maze.start, self.maze.goal)
            maze_vis.show_maze()
        return self.pop_counter, len(traversed_path) - 1

    def reset_bot(self):
        self.bot = Bot(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.goal, self.maze)

    def demo_adaptive_a_star(self, n_times=10):
        for i in range(n_times):
            self.reset_bot()
            if (i + 1) % 400 == 0:
                self.execute_algorithm(show_maze=True)
            else:
                self.execute_algorithm()
