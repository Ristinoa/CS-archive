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
from common_values import (
    EMPTY, MAX_PLAYER, MIN_PLAYER, RED, RED_MARKER, YELLOW, YELLOW_MARKER,
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

        # Stats of games played out from this node, from the perspective of the
        # player at this node.
        self.wins_for_this_player = 0
        self.total_games_for_this_player = 0

        # All legal moves that can me made from this node; useful to have once
        # to avoid recalculating later. Your code will be faster if you use
        # this value rather than calculating it when you need it.
        self.legal_moves = self.state.get_legal_moves()

        # You may add additional fields if needed below.

    def get_win_percentage_if_chosen_by_parent(self) -> float:
        """Gets the win percentage for the current node, from the perspective
        of the parent node that is trying to decide whether or not to select
        this node.

        You will need this for computing the UCB weight when doing playouts,
        and also for making the final choice on which move to make.
        """

        # we never encounter a case where the parent has never played a game
        # since that's where we're coming from

        # do we multiply by 100
        if self.total_games_for_this_player == 0:
            return 0

        parents_interest_wins = self.total_games_for_this_player - self.wins_for_this_player
        return (parents_interest_wins / self.total_games_for_this_player)

        # return  100 * (self.wins_for_this_player / self.total_games_for_this_player)


    def get_total_games_for_parent(self) -> int:
        total_parent_games = 0
        for child in self.children.values():
            total_parent_games += child.total_games_for_this_player
        return total_parent_games


    # TODO: ask dave to see what happens if i do
    #       self.parent.children.values()
    #  


    def get_UCB_weight_from_parent_perspective(self) -> float:
        """Weight from the UCB formula for this node, when used by its parent
        to select a node proportionally to its weight. The win percentage
        aspect of this formula must be from the parent's perspective, since
        that is the node making the decision.

        You will need to use this as part of the selection phase when doing
        playouts.
        """
        
        # n = (U(n)/N(n)) + ( C * math.sqrt(math.log(N(Parent(n)) / N(n))) 
        leftSide = self.get_win_percentage_if_chosen_by_parent()

        #how do i do N(parent(n)) / N(n)
        # N(n) is the total games for this player, but how to get parent. cause self in UCB is the parent, so N(n) is child then?
        rightSide = self.ucb_const * math.sqrt(math.log(self.get_total_games_for_parent)/ self.total_games_for_this_player)

        if self.parent == None:
            return
        return leftSide + rightSide

    def update_play_counts(self, outcome: int) -> None:
        """Updates the total games played from this node, as well as the number
        of wins from this node for the current player.

        You will need this for backpropagating wins/losses back up the tree.

        outcome: +1 for 1st player win, -1 for 2nd player win.
        """

        self.total_games_for_this_player+=1
        if self.state.get_active_player() == MAX_PLAYER and outcome == 1:
            self.wins_for_this_player+=1
        elif self.state.get_active_player() == MIN_PLAYER  and outcome == -1:
            self.wins_for_this_player+=1

        # if not self.parent:
        #     # can the game ever end in a tie? 

        #     # update total games for player
        #     self.total_games_for_this_player += 1

        #     # update the wins for the player depending on the outcome
        #     self.wins_for_this_player += (outcome + 1)  // 2

        #     """Line 131 is the same as doing

        #         if  outcome == 1:
        #             self.wins_for_this_player +=1
        #         else
        #             self.wins_for_this_player -= 1
        #     """
        
        # else: self.parent.update_play_counts(outcome)


    # It selects a child node of the current node that has the 
    # highest UCB  weight value.
    def mcts_selection(self):
        bestWeight = 0
        new_child = MctsNode
        weight = MctsNode.get_UCB_weight_from_parent_perspective

        #iterate through children of currNode, calculate their UCB
        for child in self.children.values():
            # if UCB weight val of curr node is better than our best weight
            # curr child is the new child with highest UCB

            if weight > bestWeight:
                new_child = child
                bestWeight = weight

            #return highest UCB child
        return new_child

    # # repeatedly selects the next child node to explore based of UCB val of children of currNode
    # # using our selection() method. 
    # # stops when we reach a terminal staet, or we reached the number of games played
    # def mcts_selection(self, board: GameBoard,node:MctsNode):
    #     while board.is_terminal == False and self.total_games_for_this_player >= 1:
    #         node = MctsNode.selection
    #     return node

    def choose_move_via_mcts(self, playouts: int) -> Optional[Location]:
        """Select a move by Monte Carlo tree search. Plays playouts random
        games from the root node to a terminal state. In each playout, play
        proceeds according to UCB while all children have been expanded. The
        first node with unexpanded children has a random child expanded. After
        expansion, play proceeds by selecting uniform random moves. Upon
        reaching a terminal state, values are propagated back along the
        expanded portion of the path. After all playouts are completed, the
        move generating the highest value child of root is returned.

        Returns None if no legal moves are available. If playouts is 0, returns
        a random choice from the legal moves.

        You will undoubtedly want to use helper functions when writing this,
        both some that I've provided, as well as helper functions of your own.
        """


        for i in range(1,playouts):
            node = self

            #selection 

            if node.legal_moves == None:
                return None


            if playouts == 0:
                return random.choice(node.legal_moves)

            # if legal move is empty and dictionary of children is not empty,
            # then all posible moves have already been explored, so we cant
            # make any more moves

            #TLDR: checks if curr node has no legal moves and has already
            #explored some chil nodes. If true, we at terminal node
            while self.legal_moves == None and self.children != {}:
                node = self.mcts_selection
                return None
                # ^^ required to call mcts selection when we've explored everything
            
            if node.legal_moves != None:
                # expand a random child
                # expansion

                # can use node.get_random_legal_move 
                move = random.choice(node.legal_moves)
                

                # add the child to the childrens dictionary of the parents node
                # the child takes in the new game state from the resulting move (legal???),
                # the parent node, and a ucb const C
                node.children[move] = MctsNode(node.state.make_move(move), node, node.ucb_const)
                
                # update curr node to be child nove corresponding to the move state
                node = node.children[move]

                # simulation
                copied_state = node.state.copy()
                while not copied_state.is_terminal:
                    move = random.choice(copied_state.get_legal_moves)
                    outcome = copied_state.make_move(move)
                    
                outcome = copied_state

                #backpropogation
                node.update_play_counts(outcome)

        # filler to eventually turn the best move
        return node
