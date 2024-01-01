''' 
    bfs.py
    Author: A.J. Ristino
    Based on code written by Professor David Musicant
    For use in CS 321.00
'''

from collections import deque
import puzzle8

def breadth_first_search(state):
    # create a deque containing the initial state
    # create empty path since first state is starting point
    path = []
    deck = deque([(path, state)])

    # create a set to keep track of visited nodes / states
    # set chosen because of its data storage properties over array
    visited = set()

    # loop over deck until it's empty

    while deck:
        # pop first element in deck in order to access current state and path of current state
        path, currState = deck.popleft()

        if currState in visited:
            continue

        if currState == puzzle8._goal: # checking if current is equivalent to our goal state

            # process path into returnable solution so it passes tests
            solution = []

            # iterate over path, converting each state into its blank square location
            for state in path:
                solution.append(puzzle8.blank_square(state))

    
            return solution 
        
        # otherwise, make sure current state is marked as visited
        visited.add(currState)
        
       

        # get location of blank in current
        blankLoc = puzzle8.blank_square(currState) 

        # use blank location to determine the set of possible moves (neighbors)
        blankNeighbors = puzzle8.neighbors(blankLoc) 

        # add neighbors of current state to the deque & prep their paths
        for neighbor_state in blankNeighbors:
            dest = puzzle8.move_blank(currState, neighbor_state)
            if dest not in visited:
                deck.append((path + [dest], dest))

    # otherwise no solution has been found :(
    return None
