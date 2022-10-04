"""
Tic Tac Toe Player
"""

from curses.ascii import EM
from hashlib import new
import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X

    X_count = 0
    O_count = 0
    for row in board:
        X_count += row.count(X)
        O_count += row.count(O)
    
    if X_count > O_count:
        return O
    elif X_count == O_count:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.append((i,j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    print(action)

    if new_board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid action: not EMPTY")
    else:
        new_board[action[0]][action[1]] =player(new_board)
    print(new_board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) ==3:
            return X
        if row.count(O) ==3:
            return 0

    columns = []
    for j in range(3):
        column = [row[j] for row in board]
        columns.append(column)
    
    for j in columns:
        if j.count(X) == 3:
            return X
        elif j.count(O) == 3:
            return O
    
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    
    # Tie or game in progress
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
      # If winner found
    if winner(board) != None:
        return True
    
    # If board is fully filled
    EMPTY_count = 0
    for row in board:
        EMPTY_count += row.count(EMPTY)
    if EMPTY_count == 0:
        return True

    # Else
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #if terminal(board) == True:
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
        # Terminal board
    if terminal(board):
        return None
    
    # Return best action
    current_player = player(board)
    best_action = None

    if current_player == X:
        v = -math.inf
        for action in actions(board):
            k = min_value(result(board, action), -math.inf, math.inf)
            if k > v:
                v = k
                best_action = action

    if current_player == O:
        v = math.inf
        for action in actions(board):
            k = max_value(result(board, action), -math.inf, math.inf)
            if k < v:
                v = k
                best_action = action
    return best_action
    

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    
    v = -math.inf
    
    for action in actions(board):
        #v = max(v, min_value(result(board, action), alpha, beta))
        t = min_value(result(board, action), alpha, beta)
        v = max(v, t)
        alpha = max(alpha, t)
        if alpha > beta:
            break
    return v


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        #v = min(v, max_value(result(board, action), alpha, beta))
        t = max_value(result(board, action), alpha, beta)
        v = min(v, t)
        beta = min(alpha, t)
        if alpha > beta:
            break
    return v
