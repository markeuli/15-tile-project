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
    
    def shuffle_board(self):
        print("Shuffling the board...")
        num_moves = random.randint(10, 20) #test with smaller numbers
        #num_moves = random.randint(100, 200)
        for _ in range(num_moves):  # Perform between 100 and 200 random moves
            move = random.choice(self.MOVES)
            self.board.perform_action(move)
        print("Finished shuffling the board.")
        return self.board
    
    '''
    # TODO: Add a function to check if the tile puzzle is solvable
    # Not required, since we generate only solvable boards with shuffle_board()
    # https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
    def check_solvable():
        pass
    '''

class State:
    '''
    State class for the sliding tile puzzle: Needed by TreeSearch class to "understand" the
    current state of the puzzle and to generate new states by applying moves to the current state.

    Required:
    - grid: the current state of the puzzle
    - parent: the previous state of the puzzle
    - action: the move that was taken to get to the current state
    - path_cost: the cost of the path from the initial state to the current state

    Optional:
    - calc_heuristic: the estimated cost of the path from the current state to the goal state
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
        self.heuristic = 0
        self.eval = self.path_cost + self.calc_heuristic()

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
                    distance += abs(i - (self.grid[i][j] // size)) + abs(j - (self.grid[i][j] % size)) #calculate Manhattan distance for each point
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
        print("TreeSearch: Generating successors...") # REMOVE LATER
        successors = []
        for move in SlidingPuzzle.MOVES:
            new_row, new_col = self.emptyRow + move[0], self.emptyCol + move[1]
            # Check if the move is legal
            if SlidingPuzzle.check_legal_move(self, move):
                # Swap the empty tile and the adjacent tile
                self.grid[self.emptyRow][self.emptyCol], self.grid[new_row][new_col] = self.grid[new_row][new_col], self.grid[self.emptyRow][self.emptyCol]
                successors.append(State(self.size, self.grid, self, move, self.path_cost + 1))
                # Swap the empty tile and the adjacent tile back
                self.grid[self.emptyRow][self.emptyCol], self.grid[new_row][new_col] = self.grid[new_row][new_col], self.grid[self.emptyRow][self.emptyCol]
        print("TreeSearch: Number of successors: ", len(successors)) # REMOVE LATER
        return successors