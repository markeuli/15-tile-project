import time
import matplotlib.pyplot as plt

#local imports
from games import *
from tree_search import TreeSearch

def clear_console():
    print("\033[H\033[J", end="")
    return

clear_console()

test_game = SlidingPuzzle(5)
test_board = test_game.board

print("Initial Heuristic: ", test_board.heuristic)
for row in test_board.grid:
    print(row)

#Initialize TreeSearch object
ts = TreeSearch(test_board)

#Initialize lists for data collection
bfs_times = []
a_star_times = []
ida_star_times = []

bfs_visited = []
a_star_visited = []
ida_star_visited = []

shuffles = [10, 25, 50, 100, 250]

#Run tests
for shuffle in shuffles:
    #Acquire shuffled board
    test_game.shuffle_board(shuffle)
    print("Shuffled Heuristic (Manhattan Distance): ", test_board.heuristic)

    #Solve with BFS
    bfs_sequence = ts.BFS_solve()
    bfs_time = time.time() - ts.timer
    bfs_visited = ts.visit_counter
    print("BFS Solution: ", bfs_sequence)
    print("BFS Solution Length: ", len(bfs_sequence))
    print("BFS Time: ", bfs_time)
    print("BFS Visited: ", bfs_visited)
    bfs_times.append(bfs_time)
    bfs_visited.append(bfs_visited)


    #Solve with A*
    a_star_sequence = ts.A_star_solve()
    a_star_time = time.time() - ts.timer
    a_star_visited = ts.visit_counter
    print("A* Solution: ", a_star_sequence)
    print("A* Solution Length: ", len(a_star_sequence))
    print("A* Time: ", a_star_time)
    print("A* Visited: ", a_star_visited)
    a_star_times.append(a_star_time)
    a_star_visited.append(a_star_visited)

    #Solve with IDA*
    ida_star_sequence = ts.IDA_star_solve()
    ida_star_time = time.time() - ts.timer
    ida_star_visited = ts.visit_counter
    print("IDA* Solution: ", ida_star_sequence)
    print("IDA* Solution Length: ", len(ida_star_sequence))
    print("IDA* Time: ", ida_star_time)
    print("IDA* Visited: ", ida_star_visited)
    ida_star_times.append(ida_star_time)
    ida_star_visited.append(ida_star_visited)

#Graph results




