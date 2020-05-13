from matplotlib import pyplot as plt

from maze import Maze


class MazeVisualization:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.a = None
        self.configure_plot()
        self.fill_maze()

    @staticmethod
    def show_maze():
        plt.show()

    def configure_plot(self):
        """
        Configures the plot according to the requirements to make sure visualization of maze is easier.
        :return:
        """
        fig = plt.figure(figsize=(7, 7 * self.maze.n_rows / self.maze.n_cols))
        self.a = plt.axes()
        self.a.set_aspect("equal")

        self.a.axes.get_xaxis().set_visible(False)
        self.a.axes.get_yaxis().set_visible(False)

        return fig

    def fill_maze(self):
        """
        Fills the maze with apropriate colors.
        """
        for row in self.maze.maze:
            for cell in row:
                i = cell.row
                j = cell.col
                if i == 0:
                    self.a.plot([j, (j + 1)], [i, i], color="k")
                if j == self.maze.n_cols - 1:
                    self.a.plot([(j + 1), (j + 1)], [i, (i + 1)], color="k")
                if i == self.maze.n_rows - 1:
                    self.a.plot([(j + 1), j], [(i + 1), (i + 1)], color="k")
                if j == 0:
                    self.a.plot([j, j], [(i + 1), i], color="k")
                if cell.blocked:
                    i = self.maze.n_cols - 1 - i
                    self.a.fill_between([j, j + 1], i, i + 1, color="k")
                elif cell == self.maze.start:
                    i = self.maze.n_cols - 1 - i
                    self.a.fill_between([j, j + 1], i, i + 1, color="red")
                elif cell == self.maze.goal:
                    i = self.maze.n_cols - 1 - i
                    self.a.fill_between([j, j + 1], i, i + 1, color="cyan")

    def fill_cell(self, i, j):
        i = self.maze.n_cols - 1 - i
        self.a.fill_between([j, j + 1], i, i + 1, color='yellow')

    def plot(self, i, j, label):
        i = self.maze.n_cols - 1 - i
        self.a.plot(j + 0.5, i + 0.5, "go")
        self.a.annotate(label, (j + 0.5, i + 0.5))
