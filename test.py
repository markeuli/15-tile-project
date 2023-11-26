import time

#local imports
from games import *
from tree_search import TreeSearch

test_game = SlidingPuzzle(5)
test_board = test_game.board

print("Initial Heuristic: ", test_board.heuristic)
for row in test_board.grid:
    print(row)

