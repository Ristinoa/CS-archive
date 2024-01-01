"""MCTS game player starter code. Fill in the methods as indicated below.

Feel free to add additional helper methods or functions.

Originally based on work by:
@author Bryce Wiedenbeck
@author Anna Rafferty
@author Dave Musicant
"""

from __future__ import annotations
import random
from game_board import GameBoard, Location
from typing import Optional
from player import Player
import math
from common_values import (EMPTY, MAX_PLAYER, MIN_PLAYER, RED, 
                           RED_MARKER, YELLOW, YELLOW_MARKER,
                           COLOR_NAMES)


class MctsPlayer(Player):
    """Uses MCTS to find the best move.

    Plays random games from the root node to a terminal state. In each playout,
    play proceeds according to UCB while all children have been expanded. The
    first node with unexpanded children has a random child expanded. After
    expansion, play proceeds by selecting uniform random moves. Upon reaching a
    terminal state, values are propagated back along the expanded portion of
    the path. After all playouts are completed, the move generating the highest
    value child of root is returned.
    """

    def __init__(self, playouts, ucb_const):
        self.playouts = playouts
        self.ucb_const = ucb_const

    def choose_move(self, board) -> Optional[Location]:
        root = MctsNode(board, None, self.ucb_const)
        return root.choose_move_via_mcts(self.playouts)


class MctsNode:
    """Node used in MCTS. It is a wrapper to contain a board/state as a node
    within a tree."""

    def __init__(self, state: GameBoard, parent: Optional[MctsNode],
                 ucb_const: float) -> None:
        """Constructor for a new node representing game state
        state. parent_node is the Node that is the parent of this
        one in the MCTS tree.
        """

        self.state = state
        self.parent = parent
        self.ucb_const = ucb_const

        # All of the known children for this node. To get to each child, a move
        # (specificed by a Location) is used.
        self.children: dict[Location, MctsNode] = {}

        self.best_ucbt_value = 0

        # Wrote this one in to solve a defaulting case, every node is initialized with
        # its best child option as None

        self.best_child_via_ucbt: MctsNode = None

        # Stats of games played out from this node, from the perspective of the
        # player at this node.
        self.wins_for_this_player = 0
        self.total_games_for_this_player = 0

        # All legal moves that can me made from this node; useful to have once
        # to avoid recalculating later. Your code will be faster if you use
        # this value rather than calculating it when you need it.
        self.legal_moves = self.state.get_legal_moves()

        # You may add additional fields if needed below.
    
    # Catch if Node is un-utilized
    # Otherwise, just calculate the win percentage with parent's bias

    def get_win_percentage_if_chosen_by_parent(self) -> float:

        # Catch for unvisited node with no stats
        if self.total_games_for_this_player == 0:
            return 0
        
        # Math to produce win percentage from parent's perspective

        parents_interest_wins = self.total_games_for_this_player - self.wins_for_this_player
        
        return (parents_interest_wins / self.total_games_for_this_player)


    def get_UCB_weight_from_parent_perspective(self) -> float:

        # catch case for root

        if self.parent == None:
            return
        
        # n = (U(n)/N(n)) + ( C * math.sqrt(math.log(N(Parent(n)) / N(n))) below

        leftSide = self.get_win_percentage_if_chosen_by_parent()

        rightSide = (self.ucb_const*math.sqrt(math.log(self.parent.total_games_for_this_player)/self.total_games_for_this_player))

        return leftSide + rightSide

    def update_play_counts(self,outcome: int,root_board: GameBoard) -> None:

        # Only way I could get this to work without breaking—couldn't sub in MAX and MIN player variables
        # Matches wins to player of interest

        self.total_games_for_this_player+=1
        if self.state.get_active_player() != root_board.get_active_player() and outcome == -1:
            self.wins_for_this_player+=1
        elif self.state.get_active_player() == root_board.get_active_player() and outcome == 1:
            self.wins_for_this_player+=1
        
 
    def get_best_ucbt(self) -> MctsNode:

        # Straightforward, iterate through node's children, pick the one with the best UCB weight

        top_node = self.best_child_via_ucbt
        top_value = self.best_ucbt_value
        
        for child in self.children:
            node = self.children[child]
            cur_value = node.get_UCB_weight_from_parent_perspective()
            if cur_value >= top_value:
                top_value = cur_value
                top_node = node
        return top_node
    
    def simulation(self, board: GameBoard) -> int:

        # Recursively check for terminal state, when found, return
        if GameBoard.is_terminal(board):
            
            if GameBoard.get_active_player(self.state) == GameBoard.value(board):
                return 1
            else:
                return -1        
        else:
            current_legal_moves = GameBoard.get_legal_moves(board)
            return self.simulation(GameBoard.make_move(board,current_legal_moves[random.randint(0,len(current_legal_moves)-1)]))

    def choose_move_via_mcts(self, playouts: int) -> Optional[Location]:
        iterations = playouts

        # Selection:
        current_node = self

        # Expansion:
        while iterations > 0:
            
            # leaf catch: 
            if len(self.legal_moves) == 0:
                return None
            
  
            # If not leaf, keep going forward:
            while len(current_node.legal_moves) > 0 and len(current_node.children) == len(current_node.legal_moves):
                next_level = current_node.get_best_ucbt()
                if next_level != None:
                    current_node = next_level
                else:
                    break
         
    
            # Impossible outcome for next step
            outcome = -2

            # Simulation:
                
            if not GameBoard.is_terminal(current_node.state):
                target = None
                for move in current_node.legal_moves:
                    if move not in current_node.children:
                        target = move
                        outcome = self.simulation(current_node.state)
                        break

                if target == None:
                    self.print_tree("")
                newNode = MctsNode(GameBoard.make_move(current_node.state,target),current_node,self.ucb_const)
                current_node.children[target] = newNode
                current_node = newNode 
                current_node.update_play_counts(outcome,self.state)
                current_node = current_node.parent
            else:
                outcome = GameBoard.value(current_node.state)
                current_node.fully_visited = True
            
           
           # Back propagation:
           
            while current_node.parent != None:
                current_node.update_play_counts(outcome,self.state)
                current_node = current_node.parent
            self.update_play_counts(outcome,self.state)

            iterations-=1

        # Make the move 

        best_move = None
        best_win_rate = 0
        for child in current_node.children:
            node = current_node.children[child]
            cur_win_rate = node.get_win_percentage_if_chosen_by_parent()
            if cur_win_rate >= best_win_rate:
                best_win_rate = cur_win_rate
                best_move = child

        return best_move