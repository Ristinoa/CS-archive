import puzzle8 as p8
from typing import List
from collections import deque

def depth_first_search(state: int, depth: int, path: List[int]) -> List[int]:
    if state == p8.solution():
        return path
    elif depth == 0:
        return []
    else:
        for square in p8.neighbors(p8.blank_square(state)):
            new_state = p8.move_blank(state, square)
            new_path = path.copy()
            new_path.append(square)
            result = depth_first_search(new_state, depth-1, new_path)
            if len(result) != 0:
                return result
        return []
        

def iterative_deepening_search(state: int) -> List[int]:
    """Finds path to solution via iterative deepening. Returns a list of
    squares that the blank moves to in order to get to solution.
    """
    depth = 1
    while(True):
        result = depth_first_search(state, depth, [])
        if (len(result) != 0):
            return result
        depth = depth + 1
    