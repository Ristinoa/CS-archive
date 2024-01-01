import puzzle8 as p8
import heapq
from typing import List


def num_wrong_tiles(state) -> int:

    # pretty simple, count # of differences between current state layout and goal state layout
    # structure should be in for loop style

    sum = 0
    for i in range(9):
        numTile = p8.get_tile(state, i)
        if numTile != 0 and numTile != p8.get_tile(p8._goal,i):
            sum+=1
    return sum
    

def manhattan_distance(state) -> int:

    # do comparisons on what goal state order should look like vs
    # order of current state to determine manhattan distance

    goal_state = [1,2,3,8,0,4,7,6,5]

    manhattan_dist = 0

    for i in range(len(goal_state)):
        tile = p8.get_tile(state,i)

        if tile != 0 and tile != goal_state[i]:
            goalX, goalY, = p8.xy_location(goal_state.index(tile))
            currentX, currentY = p8.xy_location(i)
            dist = abs(goalX-currentX) + abs(goalY-currentY)
            manhattan_dist += dist

    return manhattan_dist
    


def astar_search(state: int, heuristic) -> List[int]:

    # using heap property (and heappop) navigate to the goal state
  
    heap = []
    cost = 0
    currState = state
    path = []
    heapq.heappush(heap,(cost,currState,path))
    while heap:

        cost, currState, path = heapq.heappop(heap)

        # setup for processing + solution catch

        blank_square = p8.blank_square(currState)
        blanksNeighbors = p8.neighbors(blank_square)

        # solution catch

        if currState == p8._goal:
            solution = []
            for state in path[:-1]:
                solution.append(p8.blank_square(state))
            solution.append(blank_square)
            return solution

        # neighbor processing

        for neighbors in blanksNeighbors:
            dest = p8.move_blank(currState,neighbors)
            total_cost = cost + 1
            pathCost = total_cost + heuristic(dest)
            new_path = path + [dest]
            heapq.heappush(heap,(pathCost,dest,new_path))
        
    return None
