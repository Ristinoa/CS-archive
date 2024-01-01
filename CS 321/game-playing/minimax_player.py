"""Minimax game player. You should modify the choose_move code for the
MinimaxPlayer class. You should also modify the heuristic function, which
should return a number indicating the value of that board position.

Feel free to add additional helper methods or functions.
"""

from __future__ import annotations
from game_board import GameBoard, Location
from typing import Optional, Callable, List
from player import Player
from collections import namedtuple
import common_values
import sys
from common_values import (
    EMPTY, MAX_PLAYER, MIN_PLAYER, RED, RED_MARKER, YELLOW, YELLOW_MARKER,
    COLOR_NAMES)


# Helper function for use in heuristic
def get_neighbors(board: GameBoard, row: int, col: int) -> List[Location]:
    neighbors = []
    for x in range(row-1, row+2):
        for y in range(col-1, col+2):
            if 0 <= x < board.size and 0 <= y < board.size and (x, y) != (row, col):
                neighbors.append(Location(x, y))
    return neighbors


def heuristic(board: GameBoard) -> float:
    """Measure the value of the game board, where a high number means that is
    good for the max player, and a low number means that it is good for the min
    player. The maximum possible value should be 1, which is the value that
    should be returned if the board supplied is a guaranteed win for the max
    player. Likewise, the minimum possible value should be a -1, which is a
    guaranteed win for the min player.

    (The textbook indicates at some point in passing that this heuristic should
    range from 0 to 1, but there's no theoretical reason for 0 as opposed to -1
    for the bottom end, and the asymmetry just makes everything more
    complicated. What does matter is that the heuristic value for a
    non-terminal state should never be bigger in magnitude than that for an
    terminal state, because that would suggest that it the non-terminal state
    is more conclusive than a terminal state (which it can't be).
    """

    # Heuristic is sum of neighboring values / 8 (the maximum number of neighbors)

    sum = 0
    max_neighbors = 8
    legal_moves = GameBoard.get_legal_moves(board)
    for move in legal_moves:
        neighbors = get_neighbors(board, move.row, move.column)
        for neighbor in neighbors:
            sum += board.grid[neighbor.row][neighbor.column]    
    return sum/max_neighbors


    #Another idea for a heuristic 
    # player_legal_moves = board.get_legal_moves()
    # if player == MAX_PLAYER:
    #     final_heu = ((1 - (len(player_legal_moves)/((board.size+2)**2))) - (1 - (len(enemy_legal_moves)/((board.size+2)**2))))
    # else:
    #     final_heu = ((1 - (len(enemy_legal_moves)/((board.size+2)**2))) - (1 - (len(player_legal_moves)/((board.size+2)**2))))


class MinimaxPlayer(Player):
    """Minimax player: uses minimax to find the best move."""

    def __init__(self,
                 heuristic: Callable[[GameBoard], float],
                 plies: int) -> None:
        self.heuristic = heuristic
        self.plies = plies
        self.Board_Node = namedtuple("Board_Node", ["heuristic", "parent_move"])
        self.alpha = sys.maxsize
        self.beta = -sys.maxsize

    
    def choose_move(self, board: GameBoard) -> Optional[Location]:
        '''
        Function that chooses a move by calling minimax helper function
        '''
        player = board.get_active_player()
        minimax_result = self.minimax(self.alpha, self.beta, board, self.plies, player)

        return minimax_result.parent_move
        
        
    def minimax(self, alpha, beta, board: GameBoard, depth, player):
        '''The minimax helper function that compares heuristic values and returns the best move found
        for max player and min player respectively '''

        #Check if game is over for player or max depth has been reached 
        if board.is_terminal() or depth == 0:
            return self.Board_Node(heuristic(board), None)

        #Return best move for current board for a max player
        if player == 1:
            max_value = -sys.maxsize
            child_locations = board.get_legal_moves()
            move = Location(1,1)
    
            for child_location in child_locations:
                child_board = board.make_move(child_location)
                minimax_result = self.minimax(alpha, beta, child_board, depth - 1, -1 if player == 1 else 1)
                value = minimax_result.heuristic

                if value > max_value:
                    max_value = value
                    move = child_location
                
                alpha = max_value
                
                if alpha <= beta:
                    break

            return self.Board_Node(max_value, move)

        #Return best move for current board for a min player
        else:
            min_value = sys.maxsize
            child_locations = board.get_legal_moves()
            move = Location(1,1)
            for child_location in child_locations:
                child_board = board.make_move(child_location)

                minimax_result = self.minimax(alpha, beta, child_board, depth - 1, -1 if player == 1 else 1)
                value = minimax_result.heuristic

                if value <  min_value:
                    min_value = value
                    move = child_location
                beta = min_value
                
                if alpha <= beta:
                    break
                    

            return self.Board_Node(min_value, move)