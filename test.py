import time
import matplotlib.pyplot as plt
import numpy as np

#local imports
from games import *
from tree_search import TreeSearch

def clear_console():
    print("\033[H\033[J", end="")
    return

clear_console()

test_game = SlidingPuzzle(5)
test_board = test_game.board

#Initialize TreeSearch object
ts = TreeSearch(test_board)

#Initialize lists for data collection
bfs_times = []
a_star_times = []
ida_star_times = []

bfs_visited_s = []
a_star_visited_s = []
ida_star_visited_s = []

start = 5
end = 150
num_points = 200  # Adjust this to get the desired number of points

# Generate numbers evenly spaced on a log scale (base 10)
logspace = np.logspace(np.log10(start), np.log10(end), num=num_points)

# Round the numbers to the nearest integer and remove duplicates
shuffles = sorted(set(int(round(num)) for num in logspace))
#shuffles = [5, 6, 7, 8, 9]

failures = {
        "BFS" : 0,
        "A*" : 0,
        "IDA*" : 0
    } #if all 3 fail, break to plot

#Run tests
for shuffle in shuffles:
    #Acquire shuffled board
    test_game.shuffle_board(shuffle)

    #Solve with BFS
    if not failures["BFS"]:
        bfs_sequence = ts.BFS_solve()
        if len(bfs_sequence) == 0:
            print("BFS failed")
            failures["BFS"] = 1
            bfs_time = None
            bfs_visited = None
        bfs_time = ts.timer
        bfs_visited = ts.visit_counter
        print("BFS Solution: ", bfs_sequence)
        print("BFS Solution Length: ", len(bfs_sequence))
        print("BFS Time: ", bfs_time)
        print("BFS Visited: ", bfs_visited)
        bfs_times.append(bfs_time)
        bfs_visited_s.append(bfs_visited)
    else:
        bfs_times.append(None)
        bfs_visited_s.append(None)
        print("BFS failed previously, skipping...")

    #Solve with A*
    if not failures["A*"]:
        a_star_sequence = ts.A_star_solve()
        if len(a_star_sequence) == 0:
            print("A* failed")
            failures["A*"] = 1
            a_star_time = None
            a_star_visited = None
        a_star_time = ts.timer
        a_star_visited = ts.visit_counter
        print("A* Solution: ", a_star_sequence)
        print("A* Solution Length: ", len(a_star_sequence))
        print("A* Time: ", a_star_time)
        print("A* Visited: ", a_star_visited)
        a_star_times.append(a_star_time)
        a_star_visited_s.append(a_star_visited)
    else:
        a_star_times.append(None)
        a_star_visited_s.append(None)
        print("A* failed previously, skipping...")

    #Solve with IDA*
    if not failures["IDA*"]:
        ida_star_sequence = ts.IDA_star_solve()
        ida_star_time = ts.timer
        ida_star_visited = ts.visit_counter
        if len(ida_star_sequence) == 0:
            print("IDA* failed")
            failures["IDA*"] = 1
            ida_star_time = None
            ida_star_visited = None
        print("IDA* Solution: ", ida_star_sequence)
        print("IDA* Solution Length: ", len(ida_star_sequence))
        print("IDA* Time: ", ida_star_time)
        print("IDA* Visited: ", ida_star_visited)
        ida_star_times.append(ida_star_time)
        ida_star_visited_s.append(ida_star_visited)
    else:
        ida_star_times.append(None)
        ida_star_visited_s.append(None)
        print("IDA* failed previously, skipping...")

    if failures.values() == [1, 1, 1]:
        print("All algorithms have failed. Skipping to plot.")
        break

# Graph results
plt.figure(figsize=(10, 5))  # Set the figure size

plt.subplot(1, 2, 1)  # Create the first subplot in a 1x2 grid
plt.plot(shuffles, bfs_times, label="BFS times")
plt.plot(shuffles, a_star_times, label="A* times")
plt.plot(shuffles, ida_star_times, label="IDA* times")
plt.xlabel("Number of Shuffles")
plt.ylabel("Time (s)")
plt.title("Time to Solve Puzzle vs Number of Shuffles")
plt.legend()

plt.subplot(1, 2, 2)  # Create the second subplot in a 1x2 grid
plt.plot(shuffles, bfs_visited_s, label="BFS visited")
plt.plot(shuffles, a_star_visited_s, label="A* visited")
plt.plot(shuffles, ida_star_visited_s, label="IDA* visited")
plt.xlabel("Number of Shuffles")
plt.ylabel("Visited Nodes")
plt.title("Visited Nodes vs Number of Shuffles")
plt.legend()

plt.tight_layout()  # Adjust the layout so the plots don't overlap
plt.show()


