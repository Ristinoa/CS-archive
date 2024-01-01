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

        self.expand_id = 0


        self.best_child_via_ucbt: MctsNode = None
        self.best_ucbt_value = 0

        self.times_visited = 0
        self.fully_visited = False

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

        return float(self.total_games_for_this_player-self.wins_for_this_player)/float(self.total_games_for_this_player)

    def get_UCB_weight_from_parent_perspective(self) -> float:
        """Weight from the UCB formula for this node, when used by its parent
        to select a node proportionally to its weight. The win percentage
        aspect of this formula must be from the parent's perspective, since
        that is the node making the decision.

        You will need to use this as part of the selection phase when doing
        playouts.
        """
        if self.parent == None:
            return
        return self.get_win_percentage_if_chosen_by_parent()+(self.ucb_const*math.sqrt(math.log(self.parent.total_games_for_this_player)/self.total_games_for_this_player))

    def update_play_counts(self,outcome: int,root_board: GameBoard) -> None:
        """Updates the total games played from this node, as well as the number
        of wins from this node for the current player.

        You will need this for backpropagating wins/losses back up the tree.

        outcome: +1 for 1st player win, -1 for 2nd player win.
        """

        self.total_games_for_this_player+=1
        if self.state.get_active_player() == root_board.get_active_player() and outcome == 1:
            self.wins_for_this_player+=1
        elif self.state.get_active_player() != root_board.get_active_player() and outcome == -1:
            self.wins_for_this_player+=1


    def simulation(self, board: GameBoard) -> int:
        if GameBoard.is_terminal(board):
            # return GameBoard.value(board)
            if GameBoard.get_active_player(self.state) == GameBoard.value(board):
                return 1
            else:
                return -1

        current_legal_moves = GameBoard.get_legal_moves(board)
        return self.simulation(GameBoard.make_move(board,current_legal_moves[random.randint(0,len(current_legal_moves)-1)]))
    

 
    def get_best_ucbt(self) -> MctsNode:
        best_value = self.best_ucbt_value
        best_node = self.best_child_via_ucbt
        for child in self.children:
            node = self.children[child]
            cur_value = node.get_UCB_weight_from_parent_perspective()
            if cur_value >= best_value:
                best_value = cur_value
                best_node = node
        return best_node

    def print_tree(self,tab_str):
        print(tab_str+"ID: "+str(self.expand_id)+", WR: "+str(self.wins_for_this_player)+"/"+str(self.total_games_for_this_player)+" ("+str(float(self.wins_for_this_player)/float(self.total_games_for_this_player))+"), WR PAR: "+str(self.get_win_percentage_if_chosen_by_parent())+", UCB: "+str(self.get_UCB_weight_from_parent_perspective()))
        for child in self.children:
            self.children[child].print_tree(tab_str+"---:")


    def first_move(self,board: GameBoard):
        count = 0
        for row in range(1,board.size+1):
            for col in range(1,board.size+1):
                if board.grid[row][col] != 0:
                    return False
        return True
    
    def check_if_children_fully_visited(self):
        if len(self.children) != len(self.legal_moves):
            False
        for child in self.children:
            if self.children[child].fully_visited == False:
                return False
        return True

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
        # if self.first_move(self.state):
        #     return GameBoard.get_random_legal_move(self.state)

        iterations = playouts
        current_node = self
        id = 0
        while iterations > 0:
            #Selection via UBCT-1 Criterion
            #print("Iteration: "+str(iterations))
            # print(current_node)
            if len(self.legal_moves) == 0:
                return None
            
            #print("SELECTION VIA UCBT:")
            #level = 0
            while len(current_node.legal_moves) > 0 and len(current_node.children) == len(current_node.legal_moves):
                next_level = current_node.get_best_ucbt()
                if next_level != None:
                    current_node = next_level
                else:
                    break
                #print("LEVEL: "+str(level)+". UCB VALUE: "+str(current_node.get_UCB_weight_from_parent_perspective))
                #level += 1
            
            

            #Simulation
            outcome = -2
                
            if not GameBoard.is_terminal(current_node.state):
                loc = None
                for location in current_node.legal_moves:
                    if location not in current_node.children:
                        loc = location
                        outcome = self.simulation(current_node.state)
                        break

                if loc == None:
                    self.print_tree("")
                newNode = MctsNode(GameBoard.make_move(current_node.state,loc),current_node,self.ucb_const)
                current_node.children[loc] = newNode
                current_node = newNode 
                current_node.update_play_counts(outcome,self.state)
                current_node.expand_id = id
                id += 1
                current_node = current_node.parent
            else:
                outcome = GameBoard.value(current_node.state)
                current_node.fully_visited = True
            
            #print("OUTCOME:"+str(outcome))
            while current_node.parent != None:
                current_node.update_play_counts(outcome,self.state)
                current_node = current_node.parent
            self.update_play_counts(outcome,self.state)

            iterations-=1

            #print("\n\n")
            
            
            #print("Playouts left: "+str(iterations))
            #print("\n\n")
 
        best_move = None
        best_win_rate = 0
        for child in current_node.children:
            node = current_node.children[child]
            cur_win_rate = node.get_win_percentage_if_chosen_by_parent()
            if cur_win_rate >= best_win_rate:
                best_win_rate = cur_win_rate
                best_move = child
        #print("Best Move: row="+str(best_move.row))

        if best_move == None:
            self.print_tree("")
        return best_move