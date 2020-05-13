import json
import time

from a_star import AStar
from adaptive_a_star import AdaptiveAStar
from reverse_a_star import ReverseAStar
from utils import Utils


def performance_computation():
    n_times = 100
    adaptive = AdaptiveAStar(maze=def_mazes[1])
    a_star = AStar(maze=def_mazes[1])
    reverse_a_star = ReverseAStar(maze=def_mazes[1])
    all_a_star_moves = []
    all_adaptive_moves = []
    all_reverse_moves = []

    adaptive_a_star_times = []
    a_star_times = []
    reverse_a_star_times = []

    for _ in range(n_times):
        new_start = a_star.maze.random_cell()
        a_star.maze.start = new_start

        a_star.reset_bot()
        a_star_time_start = time.time()
        a_star_pops, a_star_moves = a_star.run_a_star_with_bot()
        a_star.pop_counter = 0
        all_a_star_moves.append(a_star_moves)
        a_star_times.append(round(time.time() - a_star_time_start, 4))

        reverse_a_star_time_start = time.time()
        reverse_a_star.reset_bot()
        reverse_a_star.maze.start = new_start
        reverse_pops, reverse_moves = reverse_a_star.run_reverse_a_star()
        all_reverse_moves.append(reverse_moves)
        reverse_a_star_times.append(round(time.time() - reverse_a_star_time_start, 4))

        adaptive_time_start = time.time()
        adaptive.maze.start = adaptive.maze.maze[a_star.maze.start.row][a_star.maze.start.col]
        adaptive.reset_bot()
        adaptive_pops, adaptive_moves = adaptive.execute_algorithm()
        adaptive.pop_counter = 0
        all_adaptive_moves.append(adaptive_moves)
        adaptive_a_star_times.append(round(time.time() - adaptive_time_start, 4))

    moves_obj = {
        "adaptive_moves": all_adaptive_moves,
        "a_star_moves": all_a_star_moves,
        "reverse_moves": all_reverse_moves
    }

    times_obj = {

        "adaptive_times": adaptive_a_star_times,
        "a_star_times": a_star_times,
        "reverse_times": reverse_a_star_times
    }

    with open("moves_new.json", "w") as moves_file:
        json.dump(moves_obj, moves_file)

    with open("times_new.json", "w") as times_file:
        json.dump(times_obj, times_file)


if __name__ == '__main__':
    """
    In the following lines, uncomment the the part you want to run and run it.
    
    """

    def_mazes = Utils.load_mazes()
    # maze_vis = MazeVisualization(def_mazes[0])
    # maze_vis.show_maze()

    # A star algorithm
    my_a_star = AStar(def_mazes[0])
    my_a_star.run_a_star_with_bot(show_maze=True)

    # Reverse A star algorithm
    my_reverse = ReverseAStar(def_mazes[0])
    my_reverse.run_reverse_a_star(show_maze=True)

    # Adaptive A star algorithm
    my_bot_a_star = AdaptiveAStar(def_mazes[0])
    my_bot_a_star.demo_adaptive_a_star(n_times=400)
    # performance_computation()
