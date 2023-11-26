import os
import queue
import time
import heapdict

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
    def __init__(self, initial_state, goal_test, successor_function, heuristic=None):
        self.initial_state = initial_state
        self.goal_test = goal_test
        self.successor_function = successor_function
        self.heuristic = heuristic

    def BFS_solve(self):
        print("BFS")
        # create a list to store sequence of moves
        sequence = []
        # create a set to store visited states
        visited = set()
        # create a queue to store states as a frontier
        frontier = []
        # add initial state to the frontier
        frontier.append(self.initial_state)

        visit_counter = 0
        timer = time.time()
        # while frontier is not empty
        while frontier:
            # remove the first state from the frontier
            state = frontier.pop(0)
            # add state to visited
            visited.add(state)
            visit_counter += 1

            clear_console()
            print("BFS solving...")
            print("Visited: ", visit_counter)
            print("Time: ", (time.time() - timer) // 1, " seconds")
            print("Visited/Time: ", visit_counter / (time.time() - timer))
            
            # if state is the goal state
            if state.goal_test():
                # return sequence
                while (state.parent != None):
                    sequence.append(state.action)
                    state = state.parent
                sequence.reverse()
                return sequence
            # for each possible move
            for new_state in state.generate_legal_successors():
                # if new state is not in visited
                if new_state not in visited:
                    # add new state to frontier
                    frontier.append(new_state)

        clear_console()
        print("BFS solved.")
        print("Visited: ", visit_counter)
        print("Time: ", (time.time() - timer) // 1, " seconds")
        print("Visited/Time: ", visit_counter / (time.time() - timer))
        return sequence;
    
    def A_star_solve(self):
        print("A*")
        sequence = []
        visited = {}
        frontier = heapdict.heapdict()
        frontier[self.initial_state] = 0
        visited[self.initial_state] = 0
        visit_counter = 0
        timer = time.time()
        heuristics = []
        while frontier:
            state, eval = frontier.popitem()

            visit_counter += 1
            clear_console()
            print("A* solving...")
            print("Heuristic: ", state.heuristic)

            #avg heuristic
            heuristics.append(state.heuristic)
            print("Visited: ", visit_counter)
            print("Time: ", (time.time() - timer) // 1, " seconds")

            if state.goal_test():
                # might need to change logic here
                # if state is the goal state, we need to make sure we return the sequence of moves that got us to the goal state
                # but we need to make sure it is the shortest path
                # double check class notes
                while state.parent is not None:
                    sequence.append(state.action)
                    state = state.parent
                sequence.reverse()

                clear_console()
                print("A* solving...")
                print("Visited: ", visit_counter)
                print("Time final: ", (time.time() - timer) // 1, " seconds")
                print("Avg heuristic: ", sum(heuristics) / len(heuristics))
                print("Min heuristic: ", min(heuristics))
                print("Max heuristic: ", max(heuristics))

                return sequence
            for new_state in state.generate_legal_successors():
                new_priority = new_state.eval
                # Handle the case where the new state is either not visited or the evaluation is less than that of the visited state
                # This has to be different from the BFS solution because our visited set is now a dictionary with evals
                if new_state not in visited or new_priority < visited[new_state]:
                    frontier[new_state] = new_priority
                    visited[new_state] = new_priority

        clear_console()
        print("A* solving...")
        print("Visited: ", visit_counter)
        print("Time final: ", (time.time() - timer) // 1, " seconds")
        print("Visited/Time: ", visit_counter / (time.time() - timer))
        print("Avg heuristic: ", sum(heuristics) / len(heuristics))
        print("Min heuristic: ", min(heuristics))
        print("Max heuristic: ", max(heuristics))
        return sequence

    # IDA* implementation using psuedocode from https://en.wikipedia.org/wiki/Iterative_deepening_A*
    def IDA_star_solve(self):
        bound = self.initial_state.heuristic
        sequence = [] #sequence of actions
        while True:
            t = self.search(self.initial_state, bound, sequence)
            if t == "FOUND":
                return sequence
            if t == float('inf'):
                return []
            bound = t

    def search(self, state, bound, sequence):
        f = state.eval
        if f > bound:
            return f
        if state.goal_test():
            return "FOUND"
        min = float('inf')
        for new_state in state.generate_legal_successors():
            t = self.search(new_state, bound, sequence)
            if t == "FOUND":
                sequence.append(new_state.action)
                return "FOUND"
            if t < min:
                min = t
        return min

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')