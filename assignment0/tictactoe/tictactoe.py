"""
Tic Tac Toe Player
"""

import math
import copy

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
    # Initialize counts
    X_count =  0
    O_count = 0

    # Go through every square on board and update counts
    for list in board:
        for elt in list:
            if elt == X:
                X_count += 1
            elif elt == O:
                O_count += 1

    # Decide whose turn it is
    if X_count == O_count == 0:
        return X
    elif X_count > O_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Initialize actions
    actions = set()

    # go through every square on board and check if empty
    for i, row in enumerate(board):
        for j , elt in enumerate(row):
            if not elt:
                actions.add((i,j))
    return(actions)



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if board[i][j] != EMPTY:
        raise Exception("Invalid Move")
    # Create deep copy of our board
    newBoard = copy.deepcopy(board)

    # Check which player
    temp = player(board)

    # Update our copied board
    newBoard[i][j] = temp

    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    setsToCheck = []
    setsToCheck.append(board[0]) # row0
    setsToCheck.append(board[1]) # row1
    setsToCheck.append(board[2]) # row2

    setsToCheck.append([board[0][0], board[1][0], board[2][0]]) # col0
    setsToCheck.append([board[0][1], board[1][1], board[2][1]]) # col1
    setsToCheck.append([board[0][2], board[1][2], board[2][2]]) # col2

    setsToCheck.append([board[0][0], board[1][1], board[2][2]]) # diag0
    setsToCheck.append([board[0][2], board[1][1], board[2][0]]) # diag1

    for set in setsToCheck:
        if checkList(set):
            return set[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != None:
        return True

    for row in board:
        for elt in row:
            if elt == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    temp = winner(board)
    if temp == X:
        return 1
    elif temp == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    player_ = player(board)
    actions_ = actions(board)

    if player_ == X:
        optimalValue = maxValue(board)
        for action in actions_:
            if minValue(result(board, action)) == optimalValue:
                return action
    else:
        optimalValue = minValue(board)
        for action in actions_:
            if maxValue(result(board, action)) == optimalValue:
                return action

def alphaBetaPruned(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    player_ = player(board)
    actions_ = actions(board)

    if player_ == X:
        optimalValue = prunedMaxValue(board, float("-inf"), float("inf"))
        for action in actions_:
            if prunedMinValue(result(board, action), float("-inf"), float("inf")) == optimalValue:
                return action
    else:
        optimalValue = prunedMinValue(board, float("-inf"), float("inf"))
        for action in actions_:
            if prunedMaxValue(result(board, action), float("-inf"), float("inf")) == optimalValue:
                return action

def checkList(list):
    """
    Returns true if matching and not None
    """
    lastElt = list[0]
    if lastElt == None:
        return False
    for elt in list:
        if elt != lastElt:
            return False
        lastElt = elt
    return True

def maxValue(board):

    if terminal(board):
        return utility(board)

    v = float("-inf")

    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v

def minValue(board):
    if terminal(board):
        return utility(board)
    v = float("inf")
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v

def prunedMaxValue(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = float("-inf")

    for action in actions(board):
        v = max(v, prunedMinValue(result(board, action), alpha, beta))
        if (v >= beta):
            return v
        alpha = max(alpha, v)
    return v

def prunedMinValue(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = float("inf")

    for action in actions(board):
        v = min(v, prunedMaxValue(result(board, action), alpha, beta))
        if (v <= alpha):
            return v
        beta = min(beta, v)

    return v
