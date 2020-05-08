from typing import Optional, List

from maze import Maze, Agent, Cell, MazeVisualizer
from priority_queue import PriorityQueue
from utils import Utils


class AdaptiveAStarWithAgent:

    def __init__(self, maze=Optional[Maze], n_rows=None, n_cols=None):
        if not maze:
            self.maze = Maze(n_rows, n_cols)
        else:
            self.maze = maze
        self.agent = Agent(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.end, self.maze)
        self.heuristics = Utils.compute_heuristic(self.maze, self.maze.end)
        self.pop_counter = 0

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

    def compute_path(self, queue):
        moves = 1
        while 0 != len(queue):
            c = queue.pop()
            self.pop_counter += 1
            if c.cell.parent is not None:
                if c.cell not in c.cell.parent.children:
                    c.cell.parent.children.append(c.cell)
            c.cell.visited = True
            valid_neighbors = self.agent.agent_maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell.get_co_ordinates() == self.agent.agent_maze.end.get_co_ordinates():
                self.agent.agent_maze.reset_visited()
                return Utils.get_traversal_path(c.cell)
            for item in valid_neighbors:
                queue.push(moves, self.heuristics[item.row][item.col], item, c.cell)
            moves = moves + 1
        return None

    def run_adaptive_a_star(self):
        maze_vis = MazeVisualizer(self.maze)
        traversed_path = [self.agent.current_loc]
        re_compute = True
        print("Agent's destination is - row: {}, col: {}".format(self.maze.end.row, self.maze.end.col))
        while re_compute:
            start_row = self.agent.current_loc.row
            start_col = self.agent.current_loc.col
            my_queue = PriorityQueue()
            my_queue.push(0, self.heuristics[start_row][start_col],
                          self.agent.agent_maze.get_cell(start_row, start_col),
                          None)
            path = self.compute_path(my_queue)
            if path is None:
                print("Path does not exists\n")
                return None, None
            traversed_path.extend(self.agent.traverse_path(path))
            if self.agent.current_loc.get_co_ordinates() == self.maze.end.get_co_ordinates():
                re_compute = False

        print("Adaptive * path exists\n")
        self.update_heuristics(traversed_path)
        Utils.print_path(traversed_path, maze_vis, "Adaptive A*", self.maze.start, self.maze.end)
        maze_vis.show_maze()
        return self.pop_counter, len(traversed_path)

    def reset_agent(self):
        self.agent = Agent(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.end, self.maze)

    def demo_adaptive_a_star(self, n_times=10):
        self.maze.start = self.maze.get_random_cell()
        for _ in range(n_times):
            if self.maze.start == self.maze.end:
                continue
            self.reset_agent()
            self.run_adaptive_a_star()