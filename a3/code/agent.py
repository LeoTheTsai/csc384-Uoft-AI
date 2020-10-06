"""
An AI player for Othello.
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move
mini_dict = {}
albe_dict = {}



def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute utility value of terminal state
def compute_utility(board, color):
    score = get_score(board)
    if color == 1:
        return score[0] - score[1]
    else:
        return score[1] - score[0]

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    board_len = len(board)
    total_cell = board_len * board_len
    score = get_score(board)

    final = 0
    #beginning state of the game
    # at least flip one more than the opponent, use compute_utility
    final += compute_utility(board, color)

    # control the corner, since corner cannot be flipped
    if board[0][0] == color:
        final += 1
    if board[0][board_len - 1] == color:
        final += 1
    if board[board_len - 1][0] == color:
        final += 1
    if board[board_len - 1][board_len - 1] == color:
        final += 1

    # more disc on the center, control of center
    for i in range(1, board_len):
        for j in range(1, board_len):
            if board[i][j] == color:
                final += 1

    # minimize opponent possible moves
    opponent_possible_moves = get_possible_moves(board, change_color(color))
    final = total_cell - len(opponent_possible_moves)

    return final

def change_color(color):
    if color == 1:
        return 2
    return 1

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    #same as the max strategy but change the util comparison

    if caching:
        if board in mini_dict:
            return mini_dict[board]

    all_move = get_possible_moves(board, change_color(color))
    if len(all_move) == 0 or limit == 0:
        value = (None, compute_utility(board, color))
        if caching:
            mini_dict[board] = value
        return value

    init_utility = float("inf")
    init_move = all_move[0]
    for move in all_move:
        #DFS implementation
        new_play_board = play_move(board, change_color(color), move[0], move[1])
        #since after play_move, its min turn and return coord and util
        utility = minimax_max_node(new_play_board, color, limit - 1, caching)[1]
        #update utility if its > init_utility and update init_move as the new move
        if utility < init_utility:
            init_utility = utility
            init_move = move
    if caching:
        mini_dict[board] = (init_move, init_utility)

    return (init_move, init_utility)





def minimax_max_node(board, color, limit, caching = 0):
    #returns highest possible utility
    #need to return the best move and util for select move

    if caching:
        if board in mini_dict:
            return mini_dict[board]

    all_move = get_possible_moves(board, color)
    if len(all_move) == 0 or limit == 0:
        value = (None, compute_utility(board, color))
        if caching:
            mini_dict[board] = value
        return value



    init_utility = float("-inf")
    init_move = all_move[0]
    for move in all_move:
        #DFS implementation
        new_play_board = play_move(board, color, move[0], move[1])
        #since after play_move, its min turn and return coord and util
        utility = minimax_min_node(new_play_board, color, limit - 1, caching)[1]
        #update utility if its > init_utility and update init_move as the new move
        if utility > init_utility:
            init_utility = utility
            init_move = move

    if caching:
        mini_dict[board] = (init_move, init_utility)

    return (init_move, init_utility)






def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    ##need to return coord instead of utility
    return minimax_max_node(board, color, limit, caching)[0] #change this!


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):

    if caching:
        if board in albe_dict:
            return albe_dict[board]


    all_move = get_possible_moves(board, change_color(color))
    if len(all_move) == 0 or limit == 0:
        value = (None, compute_utility(board, color))
        if caching:
            albe_dict[board] = value
        return value


    board_to_move = {}
    all_board = []
    for move in all_move:
        new_board = play_move(board, change_color(color), move[0], move[1])
        board_to_move[new_board] = move
        all_board.append(new_board)

    if ordering:
        all_board = sorted(all_board,
                           key=lambda x: compute_utility(x, change_color(color)),
                           reverse=True)


    init_move = all_board[0]
    for b in all_board:
        new_beta = alphabeta_max_node(b, color, alpha, beta, limit - 1,
                           caching, ordering)[1]
        if new_beta < beta:
            beta = new_beta
            init_move = board_to_move[b]
        if beta <= alpha:
            break
    if caching:
        albe_dict[board] = (init_move, beta)

    return (init_move, beta) #change this!

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT
    if caching:
        if board in albe_dict:
            return albe_dict[board]

    all_move = get_possible_moves(board, color)
    if len(all_move) == 0 or limit == 0:
        value = (None, compute_utility(board, color))
        if caching:
            albe_dict[board] = value
        return value

    #compute all board utility and sort and put in a dictionary to access move in future!!!!!!
    board_to_move = {}
    all_board = []
    for move in all_move:
        new_board = play_move(board, color, move[0], move[1])
        board_to_move[new_board] = move
        all_board.append(new_board)

    if ordering:
        all_board = sorted(all_board,
                           key=lambda x: compute_utility(x, color),
                           reverse=True)


    init_move = all_board[0]
    for b in all_board:
        new_alpha = alphabeta_min_node(b, color, alpha, beta, limit - 1,
                           caching, ordering)[1]
        if new_alpha > alpha:
            alpha = new_alpha
            init_move = board_to_move[b]

        if beta <= alpha:
            break

    if caching:
        albe_dict[board] = (init_move, alpha)

    return (init_move, alpha) #change this!

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    #IMPLEMENT
    return alphabeta_max_node(board, color, float("-inf"), float("inf"), limit, caching, ordering)[0] #change this!

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
