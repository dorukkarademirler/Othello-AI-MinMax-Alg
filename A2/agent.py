"""
An AI player for Othello. 
Explanation for the heuristic: 
I used the logic given in point 2, "Consider the number of moves you and your opponent can make, given the current board configuration".
Having more available moves on player's side has more value on determining the outcome of the game. Therefore, if the heuristic function returns a high value
that means the position is valuable since it indicates the player has variety of options. Conversely, if the function returns a low value, that indicates limited number of moves
which is bad for the player.
"""
 
import random
import sys
import time
 
# You can use the functions from othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move
 
cache = {} # Use this for state caching
 
def eprint(*args, **kwargs): #use this for debugging, to print to sterr
    print(*args, file=sys.stderr, **kwargs)
    
def compute_utility(board, color):
    # IMPLEMENT!
    """
    Method to compute the utility value of board.
    INPUT: a game state and the player that is in control
    OUTPUT: an integer that represents utility
    """
    dark, light = get_score(board)
    if color == 1:
        return dark - light
    return light - dark
 
def compute_heuristic(board, color):
    # IMPLEMENT! Optional though!
    """
    Method to heuristic value of board, to be used if we are at a depth limit.
    INPUT: a game state and the player that is in control
    OUTPUT: an integer that represents heuristic value
    """
    player_move = get_possible_moves(board, color)
    opponent_move = get_possible_moves(board, 3 - color)
    return len(player_move) - len(opponent_move)
 
############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    A helper function for minimax that finds the lowest possible utility
    """
    # HINT:
    # 1. Get the allowed moves
    # 2. Check if w are at terminal state
    # 3. If not, for each possible move, get the max utiltiy
    # 4. After checking every move, you can find the minimum utility
    # ...
    if board in cache and caching:
        return cache[board]
    player = 3 - color
    moves = get_possible_moves(board, player)
    if limit == 0 or moves == []:
        return None, compute_utility(board, color)
    min_utility, best = len(board) * len(board[0]), None
    for move in moves:
        new_board = play_move(board, player, move[0], move[1])
        utility = minimax_max_node(new_board, color, limit - 1, caching)[1]
        if utility < min_utility:
            min_utility = utility
            best = move
        if caching:
            cache[new_board] = (best, min_utility)
    return best, min_utility
 
 
 
def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    # IMPLEMENT!
    """
    A helper function for minimax that finds the highest possible utility
    """
    # HINT:
    # 1. Get the allowed moves
    # 2. Check if w are at terminal state
    # 3. If not, for each possible move, get the min utiltiy
    # 4. After checking every move, you can find the maximum utility
    # ...
    if board in cache and caching:
        return cache[board]
    moves = get_possible_moves(board, color)
    if limit == 0 or moves == []:
        return None, compute_utility(board, color)
    max_utility, best = -10 * (len(board) * len(board[0])), None
    for move in moves:
        new_board = play_move(board, color, move[0], move[1])
        util = minimax_min_node(new_board, color, limit - 1, caching)[1]
        if util > max_utility:
            max_utility = util
            best = move
        if caching:
            cache[new_board] = (best, max_utility)
 
    return best, max_utility
 
    
def select_move_minimax(board, color, limit, caching = 0):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using Minimax algorithm. 
    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    INPUT: a game state, the player that is in control, the depth limit for the search, and a flag determining whether state caching is on or not
    OUTPUT: a tuple of integers (i,j) representing a move, where i is the column and j is the row on the board.
    """
    best= minimax_max_node(board, color, limit, caching)[0]
    cache.clear()
    return best
 
 
############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    A helper function for alpha-beta that finds the lowest possible utility (don't forget to utilize and update alpha and beta!)
    """
    if board in cache and caching:
        return cache[board]
    player = 3 - color
 
    moves = get_possible_moves(board, player)
    if limit == 0 or moves == []:
        return None, compute_utility(board, color)
    min_utility, best = 10 * len(board) * len(board[0]), None
    i = 0
    flag = True
    while i < len(moves) and flag:
        move = moves[i]
        new_board = play_move(board, player, move[0], move[1])
        utility = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching, ordering)[1]
        if utility < min_utility:
            best = move
            min_utility = utility
        if min_utility < beta:
            beta = min_utility
        if caching:
            cache[new_board] = (move, utility)
        if alpha >= beta:
            flag = False
 
        i += 1
 
    return best, min_utility
    
 
def alphabeta_max_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    if board in cache and caching:
        return cache[board]
 
    moves = get_possible_moves(board, color)
 
 
    utilities_list = []
    if ordering:
        for move in moves:
            new_board = play_move(board, color, move[0], move[1])
            utility_next = compute_utility(new_board, color)  #to get the next move utility
            temp_tuple = (move, utility_next)
            utilities_list.append(temp_tuple)
 
        utilities_list.sort(key=lambda util: util[1], reverse=True) #we need to get the higher valued moves fist
        sorted_moves = []
        for elem in utilities_list:
            sorted_moves.append(elem[0])
 
    if limit == 0 or moves == []:
        return None, compute_utility(board, color)
    max_utility, best = -(len(board) * len(board[0])), None
    i = 0
    flag = True
    while i < len(moves) and flag:
        if ordering:
            move = sorted_moves[i]
        else:
            move = moves[i]
        new_board = play_move(board, color, move[0], move[1])
        utility = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)[1]
        if utility > max_utility:
            best = move
            max_utility = utility
        if utility > alpha:
            alpha = utility
        if caching:
            cache[new_board] = (move, utility)
        if alpha >= beta:
            flag = False
        i += 1
    return best, max_utility
 
 
 
 
def select_move_alphabeta(board, color, limit = -1, caching = 0, ordering = 0):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using Alpha-Beta algorithm. 
    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    INPUT: a game state, the player that is in control, the depth limit for the search, a flag determining whether state caching is on or not, a flag determining whether node ordering is on or not
    OUTPUT: a tuple of integers (i,j) representing a move, where i is the column and j is the row on the board.
    """
    cache.clear()
    size = len(board) * len(board[0]) * 100
    best= alphabeta_max_node(board, color, -size, size, limit, caching, ordering)[0]
    
    return best
 
####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) # Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) # Depth limit
    minimax = int(arguments[2]) # Minimax or alpha beta
    caching = int(arguments[3]) # Caching 
    ordering = int(arguments[4]) # Node-ordering (for alpha-beta only)
 
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