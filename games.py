import random

class SlidingPuzzle:

    MOVES = [
    (1, 0),  # Down
    (-1, 0),  # Up
    (0, 1),  # Right
    (0, -1),  # Left
    ]

    def __init__(self, size=4):
        self.size = size
        self.board = State(size=size)

    @staticmethod
    def check_legal_move(state, move):
        new_row, new_col = state.emptyRow + move[0], state.emptyCol + move[1]
        # Check if the move is legal
        if 0 <= new_row < state.size and 0 <= new_col < state.size and abs(new_row - state.emptyRow) + abs(new_col - state.emptyCol) == 1:
          return True
        return False
    
    def shuffle_board(self, num_moves=100):
        print("Shuffling the board...")
        moves = self.MOVES.copy()
        prev_move = (1, 0) # down
        for _ in range(num_moves):  # Perform between 100 and 200 random moves
            # Choose a random move, and perform it. If the move is not legal, choose another move.
            move = random.choice(moves)
            # Make sure the same move is not repeated twice in a row, and attempt to perform the move
            # Note: This is not a perfect way to ensure the move won't be undone, it just won't happen immediately (short num_moves)
            while move == prev_move or not self.board.perform_action(move):
                move = random.choice(moves)
            prev_move = move
        return self.board

class State:
    '''
    State class for the sliding tile puzzle: Needed by TreeSearch class to "understand" the
    current state of the puzzle and to generate new states by applying moves to the current state.

    Required arguments:
    - size: the size of the puzzle
    Optional
    - grid: the current state of the puzzle
    - parent: the previous state of the puzzle
    - action: the move that was taken to get to the current state
    - path_cost: the cost of the path from the initial state to the current state

    attributes:
    - size: the size of the puzzle
    - grid: the current state of the puzzle
    - emptyRow: the row of the empty tile
    - emptyCol: the column of the empty tile
    - path_cost: the cost of the path from the initial state to the current state
    - parent: the previous state of the puzzle
    - action: the move that was taken to get to the current state
    - heuristic: the estimated cost of the path from the current state to the goal state
    - eval: the evaluation function for A* and IDA*

    methods:
    - findEmpty: finds the empty tile in the grid
    - __hash__: hashes the grid as a tuple of tuples
    - __eq__: checks if two states are equal
    - __lt__: checks if the evaluation function of the current state is less than the evaluation function of another state
    - __gt__: checks if the evaluation function of the current state is greater than the evaluation function of another state
    - calc_heuristic: calculates the heuristic of the current state
    - goal_test: checks if the current state is the goal state
    - perform_action: performs a move on the current state
    - generate_legal_successors: generates all possible moves from the current state

    NOTE: These methods are required by the TreeSearch class, but they can be modified to suit the needs of the game.
    To use the TreeSearch class with a different game, you will need to implement a similar State class with the same methods for your game.
    '''
    def __init__(self, size, grid=None, parent=None, action=None, path_cost=0):
        self.size = size
        if grid is None:
            self.grid = self.grid = [[i + j * size + 1 for i in range(size)] for j in range(size)]
            self.emptyRow, self.emptyCol = size - 1, size - 1
            self.grid[self.emptyRow][self.emptyCol] = 0
        else:
            self.grid = grid
            self.emptyRow, self.emptyCol = self.findEmpty()

        self.path_cost = path_cost
        self.parent = parent
        self.action = action
        self.heuristic = self.calc_heuristic()
        self.eval = self.path_cost + self.heuristic

    def findEmpty(self):
        size = len(self.grid)
        for i in range(size):
            for j in range(size):
                if self.grid[i][j] == 0:
                    return i, j

    #need to make hashable type
    def __hash__(self):
        #hashing the grid as a tuple of tuples
        #Link to example: https://stackoverflow.com/questions/17585730/what-does-hash-do-in-python
        # https://python-forum.io/thread-22933.html
        return hash(tuple(tuple(row) for row in self.grid))

    def __eq__(self, other):
        if isinstance(other, State):
            return self.grid == other.grid
        return False
    
    def __lt__(self, other):
        return self.eval < other.eval

    def __gt__(self, other):
        return self.eval > other.eval
    
    def calc_heuristic(self):
        # Manhattan distance
        distance = 0

        size = len(self.grid)
        for i in range(size):
            for j in range(size):
                if self.grid[i][j] != 0:
                    distance += abs(i - ((self.grid[i][j]  - 1) // size)) + abs(j - (self.grid[i][j] - 1) % size) #calculate Manhattan distance for each point
        self.heuristic = distance
        return distance
    
    def goal_test(self):
        # This will serve as the goal test function to be passed to the TreeSearch class, can check any state for the goal
        size = len(self.grid)
        for row in range(size):
            for col in range(size):
                if self.grid[row][col] != row * size + col + 1 and (row != size - 1 or col != size - 1):
                    return False
        return True
    
    def perform_action(self, move):
        new_row, new_col = self.emptyRow + move[0], self.emptyCol + move[1]
        # Check if the move is legal
        if SlidingPuzzle.check_legal_move(self, move):
            # Swap the empty tile and the adjacent tile
            self.grid[self.emptyRow][self.emptyCol], self.grid[new_row][new_col] = self.grid[new_row][new_col], self.grid[self.emptyRow][self.emptyCol]
            self.emptyRow, self.emptyCol = new_row, new_col
            return True
        return False
    
    def generate_legal_successors(self):
        successors = []
        for move in SlidingPuzzle.MOVES:
            new_row, new_col = self.emptyRow + move[0], self.emptyCol + move[1]
            # Check if the move is legal
            if SlidingPuzzle.check_legal_move(self, move):
                # Create a copy of the grid
                new_grid = [row.copy() for row in self.grid]
                # Swap the empty tile and the adjacent tile
                new_grid[self.emptyRow][self.emptyCol], new_grid[new_row][new_col] = new_grid[new_row][new_col], new_grid[self.emptyRow][self.emptyCol]
                successors.append(State(self.size, new_grid, self, move, self.path_cost + 1))
        return successors