def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != " ":
                return False
    return True
    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    # booleans to check each side of the sequence
    frontOpen = True
    backOpen = True
    # different protocals for each direction
    if d_y == 0 and d_x == 1:
        x_start = x_end - length
        if (x_end == 7):
            backOpen = False
        elif (board[y_end][x_end + 1] != " "):
            backOpen = False
        if (x_start == 0):
            frontOpen = False
        elif (board[y_end][x_start - 1] != " "):
            frontOpen = False 
    elif d_y == 1 and d_x == 0:
        y_start = y_end - length
        if (y_end == 7):
            backOpen = False
        elif (board[y_end+1][x_end] != " "):
            backOpen = False
        if (y_start == 0):
            frontOpen = False
        elif (board[y_end-1][x_end] != " "):
            frontOpen = False 
    elif d_y == 1 and d_x == 1:
        y_start = y_end - length
        x_start = x_end - length
        if (y_end == 7) or (x_end == 7):
            backOpen = False
        elif (board[y_end+1][x_end+1] != " "):
            backOpen = False
        if (y_start == 0) or (x_start == 0):
            frontOpen = False
        elif (board[y_end-1][x_start-1] != " "):
            frontOpen = False 
    else:
        y_start = y_end - length
        x_start = x_end + length
        if (y_end == 7) or (x_end == 0):
            backOpen = False
        elif (board[y_end+1][x_end-1] != " "):
            backOpen = False
        if (y_start == 0) or (x_start == 7):
            frontOpen = False
        elif (board[y_start-1][x_start+1] != " "):
            frontOpen = False
    if (frontOpen and backOpen):
        return "OPEN"
    elif (frontOpen or backOpen):
        return "SEMIOPEN"
    else:
        return "CLOSED"


    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    # possible (dy,dx): (0,1), (1,0), (1,1), (1,-1)
    # length >= 2
    # assume start y,x on edges - assume to be top and left edges
    open_seq_count = 0
    semi_open_seq_count = 0
    cur_len = 0
    cur_y = y_start
    cur_x = x_start
    #count = 0
    while cur_y<len(board) and cur_x<len(board[0]):

        if board[cur_y][cur_x] == col:
            cur_len+=1
        else:
            if cur_len == length:
                y_end = cur_y-d_y
                x_end = cur_x-d_x
                seq_type = is_bounded(board, y_end, x_end, length, d_y, d_x)
                if seq_type == "OPEN":
                    open_seq_count+=1
                if seq_type == "SEMIOPEN":
                    semi_open_seq_count+=1
            cur_len=0

        #count+=1
        cur_y+=d_y
        cur_x+=d_x

    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    # direction: (dy, dx)
    # left-right: (0, 1)
    # top-bottom: (1, 0)
    # upL-lowR: (1, 1)
    # upR-lowL: (1, -1)
    # top-left corner - check left-right, top-bottom, upL-lowR
    # horizontal - check top-bottom, upL-lowR, upR-lowL
    # vertical - check left-right, upL-lowR, upR-lowL

    #top-left corner
    y_start = 0
    x_start = 0
    # left-right
    open_temp, semi_temp = detect_row(board, col, y_start, x_start, length, 0, 1)
    open_seq_count += open_temp
    semi_open_seq_count += semi_temp
    # top-bottom
    open_temp, semi_temp = detect_row(board, col, y_start, x_start, length, 1, 0)
    open_seq_count += open_temp
    semi_open_seq_count += semi_temp
    # upL-lowR
    open_temp, semi_temp = detect_row(board, col, y_start, x_start, length, 1, 1)
    open_seq_count += open_temp
    semi_open_seq_count += semi_temp

    # horizontal - move along x - board[0][x]
    # y_start = 0
    for i in range(1,len(board[0])):
        x_start = i
        # top-bottom
        open_temp, semi_temp = detect_row(board, col, y_start, x_start, length, 1, 0)
        open_seq_count += open_temp
        semi_open_seq_count += semi_temp
        # upL-lowR
        open_temp, semi_temp = detect_row(board, col, y_start, x_start, length, 1, 1)
        open_seq_count += open_temp
        semi_open_seq_count += semi_temp
        # upR-lowL
        open_temp, semi_temp = detect_row(board, col, y_start, x_start, length, 1, -1)
        open_seq_count += open_temp
        semi_open_seq_count += semi_temp
    
    # vertical - move along y - board[y][0]
    x_start = 0
    for i in range(1, len(board)):
        # left-right
        open_temp, semi_temp = detect_row(board, col, y_start, x_start, length, 0, 1)
        open_seq_count += open_temp
        semi_open_seq_count += semi_temp
        # upL-lowR
        open_temp, semi_temp = detect_row(board, col, y_start, x_start, length, 1, 1)
        open_seq_count += open_temp
        semi_open_seq_count += semi_temp
        # upR-lowL
        open_temp, semi_temp = detect_row(board, col, y_start, x_start, length, 1, -1)
        open_seq_count += open_temp
        semi_open_seq_count += semi_temp
        
    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    # evaluates score for every position, returns move with highest score
    max_score = -1
    move_y = 0
    move_x = 0
    for y in range(len(board)):
        for x in range(len(board)):
            # if not occupied:
            if board[y][x] == " ":
                # create new deep copy of current board
                # aka virtual board
                future = []
                for sub in board:
                    future.append(sub[:])
                # place piece in virtual board and evaluate
                future[y][x] = 'b'
                temp_score = score(future)
                # if winning immediately return
                if temp_score == 100000:
                    return y, x
                # compares this move to best known move
                if temp_score > max_score:
                    max_score = temp_score
                    move_y = y
                    move_x = x
    return move_y, move_x
    
#don't change
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
    if (detect_rows(board, "w", 5) [0] > 0) or (detect_rows(board, "w", 5) [1] > 0):
        return "White won"
    elif (detect_rows(board, "b", 5) [0] > 0) or (detect_rows(board, "b", 5) [1] > 0):
        return "Black won"
    else:
        for x in board:
            for y in x:
                if y == " ":
                    return "Continue playing"
        return "Draw"

#don't change
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
                

#don't change
def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i)
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

#don't change
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
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
#don't change        
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x




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
    play_gomoku(8)
    