"""
Gomoku AI Engine
Author(s): Samantha Chang and Hasnain Heryani
"""

# is_empty():
# Paraneters:
# board: The game board
# Check if the entire board is empty meaning no 'w' or 'b' in the board
# Returns True if the baord is empty
# Otherwise returns False
def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != ' ':
                return False
    return True
    
# is_bounded():
# Parameters:
# board: The game board
# y_end: The end y coordinate of the sequence
# x_end: The end x coodrinate of the sequence
# length: The length of the sequence
# (d_y, d_x): The Direction of the sequence
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    # Gets the side length of the baord
    board_size = len(board)-1
    x_start = (x_end - (length-1)) * d_x
    y_start = (y_end - (length-1)) * d_y
    # Case  1: Sequence is horizontal
    if (x_end != length - 1 and board[y_start - d_y][x_start - d_x] == ' '):
        return "SEMIOPEN"
    elif (x_end != length - 1 and board[y_start - d_y][x_start - d_x]) == ' ' and (x_end != board_size and board[y_end + d_y][x_end + d_x] == ' '):
        return "OPEN"
    elif (x_end != length - 1 and board[y_start - d_y][x_start - d_x] == ' ') or (x_end != board_size and board[y_end + d_y][x_end + d_x] == ' '):
        return "SEMIOPEN"
    else:
        return "CLOSED"
    # if d_y == 0 and d_x == 1:
    #     if (x_end != length - 1 and board[y_end][x_end - length - 1] == ' '):
    #         return "SEMIOPEN"
    #     elif (x_end != length - 1 and board[y_end][x_end - length - 1]) == ' ' and (x_end != board_size and board[y_end][x_end + 1] == ' '):
    #         return "OPEN"
    #     elif (x_end != length - 1 and board[y_end][x_end - length - 1] == ' ') or (x_end != board_size and board[y_end][x_end + 1] == ' '):
    #         return "SEMIOPEN"
    #     else:
    #         return "CLOSED"
    # elif d_y == 1 and d_x == 0:
    #     if (y_end != length - 1 and board[y_end - length - 1][x_end] == ' '):
    #         return "SEMIOPEN"
    #     elif (y_end != length - 1 and board[y_end - length - 1][x_end]) == ' ' and (y_end != board_size and board[y_end + 1][x_end] == ' '):
    #         return "OPEN"
    #     elif (y_end != length - 1 and board[y_end - length - 1][x_end] == ' ') or (y_end != board_size and board[y_end + 1][x_end] == ' '):
    #         return "SEMIOPEN"
    #     else:
    #         return "CLOSED"
    # elif d_y == 1 and (d_x == 1 or d_x == -1):
    #     if (y_end != length - 1 and x_end != length - 1 and board[y_end - length - 1][x_end - length - 1] == ' '):
    #         return "SEMIOPEN"
    #     elif (y_end != length - 1 and x_end != length - 1 and board[y_end - length - 1][x_end - length - 1] == ' ') and (y_end != board_size and x_end != board_size and board[y_end + 1][x_end + 1] == ' '):
    #         return "OPEN"
    #     elif (y_end != length - 1 and x_end != length - 1 and  board[y_end - length - 1][x_end - length - 1] == ' ') or (y_end != board_size and x_end != board_size and board[y_end + 1][x_end + 1] == ' '):
    #         return "SEMIOPEN"
    #     else:
    #         return "CLOSED"
        
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    count = 0
    open_seq_count = 0
    semi_open_seq_count = 0
    i = y_start
    j = x_start
    x_anti_diagonal_bound_multiplier = 1
    if d_x == -1:
        x_anti_diagonal_bound_multiplier = 0
    while (d_x == 0 and i < len(board)-1) or (d_y == 0 and j < len(board)-1) or (d_x > 0 and d_y > 0 and j < len(board)-1 and i < len(board)-1) or (d_y > 0 and d_x < 0 and j >= 0 and i < len(board)-1):
        if board[i][j] == col:
            count += 1
        else:
            count = 0
        if count == length and (i != (len(board)-1)*d_y or j != ((len(board)-1)*x_anti_diagonal_bound_multiplier) and board[i+d_y][j+d_x] == ' '):
            bound = is_bounded(board, i, j, length, d_y, d_x)
            if bound == "OPEN":
                open_seq_count += 1
            elif bound == "SEMIOPEN":
                semi_open_seq_count += 1
            count = 0
        elif count == length and (i == (len(board)-1) or j == (len(board)-1)*x_anti_diagonal_bound_multiplier):
            bound = is_bounded(board, i, j, length, d_y, d_x)
            if bound == "SEMIOPEN":
                semi_open_seq_count += 1
            count = 0
        if count > length:
            count = 0
        i += d_y
        j += d_x
    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    ####CHANGE ME
    open_seq_count, semi_open_seq_count = 0, 0
    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    move_y = 0
    move_x = 0
    
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)      
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])
    
def is_win(board):
    who_won = is_seq_complete(board, "w", 1, 1, 1, 5)
    if who_won:
        return "White won"

def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s) 

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        print("open sequences and semi open sequences:", detect_row(board, 'w', 0, 0, 3, 0, 1))
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res        
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

def is_seq_complete(board, col, y_start, x_start, d_y, d_x):
    count = 0
    for i in range(y_start, y_start + d_y + 1):
        count = 0
        for j in range(x_start, x_start + d_x + 1):
            if board[i][j] == col:
                count += 1
            if count == 5:
                return True
    return False

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


  
            
if __name__ == '__main__':
    print(play_gomoku(8))