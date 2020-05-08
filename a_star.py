from typing import Optional

from maze import Maze, Agent, MazeVisualizer
from priority_queue import PriorityQueue
from utils import Utils


class AStarWithAgent:

    def __init__(self, maze=Optional[Maze], n_rows=None, n_cols=None):
        if not maze:
            self.maze = Maze(n_rows, n_cols)
        else:
            self.maze = maze
        self.agent = Agent(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.end, self.maze)
        self.pop_counter = 0

    def compute_path(self, queue, heuristic):
        count = 1
        while 0 != len(queue):
            c = queue.pop()
            self.pop_counter += 1
            c.cell.visited = True
            valid_neighbors = self.agent.agent_maze.get_unblocked_unvisited_neighbors(c.cell)
            if c.cell.get_co_ordinates() == self.agent.agent_maze.end.get_co_ordinates():
                self.agent.agent_maze.reset_visited()
                return Utils.get_traversal_path(c.cell)
            for item in valid_neighbors:
                queue.push(count, heuristic[item.row][item.col], item, c.cell)
            count = count + 1
        return None

    def reset_agent(self):
        self.agent = Agent(self.maze.n_rows, self.maze.n_cols, self.maze.start, self.maze.end, self.maze)

    def run_a_star_with_agent(self):
        maze_vis = MazeVisualizer(self.maze)
        re_compute = True
        traversed_path = list()
        manhattan_heuristic = Utils.compute_heuristic(self.maze, self.maze.end)
        while re_compute:
            start_row = self.agent.current_loc.row
            start_col = self.agent.current_loc.col
            my_queue = PriorityQueue()
            my_queue.push(0, manhattan_heuristic[start_row][start_col],
                          self.agent.agent_maze.get_cell(start_row, start_col), None)
            path = self.compute_path(my_queue, manhattan_heuristic)
            if path is None:
                print("Path does not exist")
                return None, None
            traversed_path.extend(self.agent.traverse_path(path))
            if self.agent.current_loc.get_co_ordinates() == self.maze.end.get_co_ordinates():
                re_compute = False
        Utils.print_path(traversed_path, maze_vis, "A*", self.maze.start, self.maze.end)
        print("\nTotal popped nodes are: ", self.pop_counter)
        maze_vis.show_maze()
        return self.pop_counter, len(traversed_path)