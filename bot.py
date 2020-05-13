from typing import List

from maze import Cell, Maze


class Bot:
    def __init__(self, n_rows, n_cols, start: Cell, target: Cell, original_maze: Maze):
        self.bot_maze = Maze(n_rows, n_cols, bot=True)
        # bot_maze is the maze from the perspective of the bot.
        self.bot_maze.start = start
        self.pos = self.bot_maze.maze[start.row][start.col]
        print("Bot starts at - row: {}, col: {}".format(start.row, start.col))
        self.original_maze = original_maze
        self.mark_blocked_neighbors()
        self.bot_maze.goal = target

    def mark_blocked_neighbors(self):
        for n in self.original_maze.get_neighbors(self.pos, blocked=True):
            self.bot_maze.maze[n.row][n.col].blocked = True

    def traverse_path(self, cells: List[Cell]):
        traversed_path = []
        for cell in cells:
            if self.bot_maze.maze[cell.row][cell.col].blocked:
                print(
                    "Bot hit blocked cell at row: {}, col: {}".format(cell.row, cell.col))
                return traversed_path
            else:
                self.pos = self.bot_maze.maze[cell.row][cell.col]
                print("Bot moved to row: {}, column: {}".format(cell.row, cell.col))
                traversed_path.append(cell)
            self.mark_blocked_neighbors()
        return traversed_path
