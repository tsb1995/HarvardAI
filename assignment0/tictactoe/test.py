import tictactoe as ttt

X = "X"
O = "O"
EMPTY = None

board = [[EMPTY, O, O],
        [X, X, O],
        [O, X, X]]

empty_board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

full_board = [[X, O, X],
            [O, X, O],
            [X, O, X]]

X_win_board = [[O, X, O],
            [EMPTY, X, O],
            [EMPTY, X, X]]

O_win_board = [[O, O, O],
            [X, X, O],
            [EMPTY, X, X]]

print(ttt.maxValue(board))
