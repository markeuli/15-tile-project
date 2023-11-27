import os
import queue
import time
import heapdict

# Constants
TIME_LIMIT = 10 * 60 # seconds

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class TreeSearch:
    '''
    TreeSearch class for the sliding tile puzzle: Needed to solve the puzzle using BFS, A*, and IDA*.
    Required:
    - initial_state: the initial state of the puzzle
    - goal_test: a function that returns True if the current state is the goal state
    - successor_function: a function that returns a list of possible moves from the current state
    - heuristic: a function that returns the estimated cost of the path from the current state to the goal state (if applicable)
    '''

    

    #To initialize the class, you need to pass the initial state of the puzzle, the goal test function, the successor function, and the heuristic function (if applicable)
    def __init__(self, initial_state):
        # initialize state object implemented in game
        self.initial_state = initial_state
        
        # initialize metric variables
        self.timer = 0
        self.visit_counter = 0
        self.bound = 0

    def BFS_solve(self):
        sequence = []
        visited = set()
        frontier = []
        frontier.append(self.initial_state)

        self.visit_counter = 0
        self.timer = time.time()

        while frontier:
            state = frontier.pop(0)
            visited.add(state)
            self.visit_counter += 1

            #termination condition: time limit exceeded
            if (time.time() - self.timer) // 1 > TIME_LIMIT: # 5 minute time limit
                print("BFS ERROR: Time limit exceeded.")
                self.timer = None
                return sequence

            '''
            Console output for debugging
            clear_console()
            print("BFS solving...")
            print("Visited: ", visit_counter)
            print("Time: ", (time.time() - timer) // 1, " seconds")
            print("Visited/Time: ", visit_counter / (time.time() - timer))
            '''
            if state.goal_test():
                self.timer = time.time() - self.timer
                while (state.parent != None):
                    sequence.append(state.action)
                    state = state.parent
                sequence.reverse()
                return sequence
            for new_state in state.generate_legal_successors():
                if new_state not in visited:
                    frontier.append(new_state)
        return sequence;
    
    def A_star_solve(self):
        sequence = []
        visited = {}
        frontier = heapdict.heapdict()
        frontier[self.initial_state] = 0
        visited[self.initial_state] = 0
        self.visit_counter = 0
        self.timer = time.time()

        while frontier:
            state, eval = frontier.popitem()
            self.visit_counter += 1

            if state.goal_test():
                self.timer = time.time() - self.timer
                while state.parent is not None:
                    sequence.append(state.action)
                    state = state.parent
                sequence.reverse()
                return sequence

            #termination condition: time limit exceeded
            if (time.time() - self.timer) // 1 > TIME_LIMIT: 
                print("A* ERROR: Time limit exceeded.")
                self.timer = None
                return sequence

            '''
            Console output for debugging
            clear_console()
            print("A* solving...")
            print("Visited: ", visit_counter)
            print("Time final: ", (time.time() - timer) // 1, " seconds")
            print("Avg heuristic: ", sum(heuristics) / len(heuristics))
            print("Min heuristic: ", min(heuristics))
            print("Max heuristic: ", max(heuristics))
            '''
                
            for new_state in state.generate_legal_successors():
                new_priority = new_state.eval
                # Handle the case where the new state is either not visited or the evaluation is less than that of the visited state
                # This has to be different from the BFS solution because our visited set is now a dictionary with evals
                if new_state not in visited or new_priority < visited[new_state]:
                    frontier[new_state] = new_priority
                    visited[new_state] = new_priority
        return sequence

    # IDA* implementation using psuedocode from https://en.wikipedia.org/wiki/Iterative_deepening_A*
    def IDA_star_solve(self):
        
        bound = self.initial_state.heuristic
        sequence = [] #sequence of actions

        # reset relevant metric variables
        self.timer = time.time()
        self.visit_counter = 0
        self.bound = 0

        while True:
            t = self.search(self.initial_state, self.bound, sequence)
            if t == "FOUND":
                sequence.reverse()
                return sequence
            
            #termination condition: time limit exceeded
            if t == "ERROR":
                return sequence
            
            if t == float('inf'):
                return []
            self.bound = t

    def search(self, state, bound, sequence):
        f = state.eval
        if f > bound:
            return f
        
        if state.goal_test():
            self.timer = time.time() - self.timer
            return "FOUND"
        
        min = float('inf')

        #termination condition: time limit exceeded
        if (time.time() - self.timer) // 1 > TIME_LIMIT: # 5 minute time limit
            print("IDA* ERROR: Time limit exceeded.")
            self.timer = None
            return "ERROR"

        self.visit_counter += 1
        '''
        clear_console()
        print("IDA* solving...")
        print("Visited: ", self.visit_counter)
        print("Time final: ", (time.time() - self.timer) // 1, " seconds")
        print("Visited/Time: ", self.visit_counter / (time.time() - self.timer))
        print("Bound: ", bound)
        '''
        for new_state in state.generate_legal_successors():
            t = self.search(new_state, bound, sequence)
            if t == "ERROR":
                return "ERROR"
            if t == "FOUND":
                sequence.append(new_state.action)
                return "FOUND"
            if t < min:
                min = t
        return min

