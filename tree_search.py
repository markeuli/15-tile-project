import os

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
        timer = 0
        # while frontier is not empty
        while frontier:
            # remove the first state from the frontier
            state = frontier.pop(0)
            # add state to visited
            visited.add(state)
            visit_counter += 1
            print("Visited length: ", len(visited))

            # if state is the goal state
            if state.goal_test():
                # return sequence
                print("Goal state found") # REMOVE LATER
                print(state.grid)
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
        return sequence;
    '''
    #TODO: Add a function to solve the puzzle using A*
    def A_star_solve(self):
        pass

    #TODO: Add a function to solve the puzzle using IDA*
    def IDA_star_solve():
        pass
    '''