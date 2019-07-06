from copy import deepcopy
from datetime import datetime

SIZE = 6  # problem size

# result
MAX_QUEEN = None
RESULT = None


def count_queen(board):
    count = 0
    for row in range(0, SIZE):
        count += board[row].count(1)
    return count


def print_board(board):
    for row in range(0, SIZE):
        print(board[row])


def analyze_board(board):
    global MAX_QUEEN
    global RESULT

    for row in range(0, SIZE):
        for col in range(0, SIZE):
            if board[row][col] == 1:
                # horizontal check
                for pos in range(col + 1, SIZE):
                    if board[row][pos] == 1:
                        return
                # vertical check
                for pos in range(row + 1, SIZE):
                    if board[pos][col] == 1:
                        return
                # south-east check
                for pos in range(1, min(SIZE - col, SIZE - row)):
                    if board[row + pos][col + pos] == 1:
                        return
                # south-west check
                for pos in range(1, min(SIZE - row, col + 1)):
                    if board[row + pos][col - pos] == 1:
                        return

    count = count_queen(board)
    if MAX_QUEEN is None or MAX_QUEEN < count:
        MAX_QUEEN = count
        RESULT = deepcopy(board)


def enum_variants(board_row, board_col, board, queen_row=None, queen_col=None):
    for val in range(0, 2):
        if queen_row == board_row and val == 1:
            continue
        if queen_col == board_col and val == 1:
            continue
        board[board_row][board_col] = val
        if val == 1:
            queen_row = board_row
            queen_col = board_col
        if board_col + 1 < SIZE:
            enum_variants(board_row, board_col + 1, board, queen_row, queen_col)
        elif board_row + 1 < SIZE:
            enum_variants(board_row + 1, 0, board, queen_row, queen_col)
        if board_row + 1 == SIZE and board_col + 1 == SIZE:
            analyze_board(board)


def solve_nqueen():
    board = [[0 for _ in range(0, SIZE)] for _ in range(0, SIZE)]
    enum_variants(0, 0, board)


def solve_nqueen2(board, row=0, col=0):
    global MAX_QUEEN
    global RESULT

    if row + 1 == SIZE and col + 1 == SIZE:
        # check
        queen_count = count_queen(board)
        if MAX_QUEEN is None or MAX_QUEEN < queen_count:
            MAX_QUEEN = queen_count
            RESULT = deepcopy(board)

        # stop
        return

    # check if we can put queen in this cell
    allowed_cell = True

    for pos in range(1, row + 1):
        if board[row - pos][col] == 1:
            allowed_cell = False
            break
        if col + pos < SIZE and board[row - pos][col + pos] == 1:
            allowed_cell = False
            break

    if allowed_cell:
        for pos in range(1, col + 1):
            if board[row][col - pos] == 1:
                allowed_cell = False
                break
            if row - pos >= 0 and board[row - pos][col - pos] == 1:
                allowed_cell = False
                break

    if allowed_cell:
        # can put
        board[row][col] = 1
        if col + 1 < SIZE:
            solve_nqueen2(board=board, row=row, col=col + 1)
        elif row + 1 < SIZE:
            solve_nqueen2(board=board, row=row + 1, col=0)

    board[row][col] = 0
    if col + 1 < SIZE:
        solve_nqueen2(board=board, row=row, col=col + 1)
    elif row + 1 < SIZE:
        solve_nqueen2(board=board, row=row + 1, col=0)

print("Start time: {}".format(datetime.now()))
solve_nqueen2(board=[[0 for _ in range(0, SIZE)] for _ in range(0, SIZE)])
print("Max queen number: {}".format(MAX_QUEEN))
print("Result board:")
print_board(RESULT)
print("End time: {}".format(datetime.now()))

