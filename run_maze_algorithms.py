import json

from a_star import AStarWithAgent
from adaptive_a_star import AdaptiveAStarWithAgent
from reverse_a_star import ReverseAStar
from utils import Utils

if __name__ == '__main__':
    def_mazes = Utils.load_mazes()

    # A star algorithm
    my_a_star = AStarWithAgent(def_mazes[0])
    my_a_star.run_a_star_with_agent()

    # Reverse A star algorithm
    my_reverse = ReverseAStar(def_mazes[0])
    my_reverse.run_reverse_a_star()

    # Adaptive A star algorithm
    my_agent_a_star = AdaptiveAStarWithAgent(def_mazes[0])
    my_agent_a_star.run_adaptive_a_star()


def aws_function():
    differences = list()
    n_times = 500
    adaptive = AdaptiveAStarWithAgent(maze=def_mazes[0])
    a_star = AStarWithAgent(maze=def_mazes[0])
    all_a_star_moves = []
    all_adaptive_moves = []
    for _ in range(n_times):
        new_start = a_star.maze.get_random_cell()
        a_star.maze.start = new_start

        a_star.reset_agent()
        a_star_pops, a_star_moves = a_star.run_a_star_with_agent()
        all_a_star_moves.append({"start": a_star.maze.start.get_co_ordinates(),
                                 "end": a_star.maze.end.get_co_ordinates(),
                                 "moves": a_star_moves,
                                 })

        adaptive.maze.start = adaptive.maze.maze[new_start.row][new_start.col]
        adaptive.reset_agent()
        adaptive_pops, adaptive_moves = adaptive.run_adaptive_a_star()
        all_adaptive_moves.append({"start": a_star.maze.start.get_co_ordinates(),
                                   "end": a_star.maze.end.get_co_ordinates(),
                                   "moves": adaptive_moves,
                                   })
        if adaptive_pops is not None and a_star_pops is not None:
            differences.append({"start": a_star.maze.start.get_co_ordinates(),
                                "end": a_star.maze.end.get_co_ordinates(),
                                "difference": adaptive_pops - a_star_pops,
                                })

    moves_obj = {
        "adaptive_moves": all_adaptive_moves,
        "a_star_moves": all_a_star_moves
    }
    with open("differences_adaptive.json", "w") as diff_file:
        json.dump(differences, diff_file)

    with open("moves.json", "w") as moves_file:
        json.dump(moves_obj, moves_file)

    print("The differences array is: ", differences)
    print("Average difference is: ", (sum(differences) / len(differences)))
