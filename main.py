#0 빈칸, 1 하양, 2 검정
def color_check(color):
    if color == 1 or color == 2:
        return True
    else:
        return False

def make_base():
    board = [[0 for _ in range(8)] for _ in range(8)]
    board[3][3] = 1
    board[4][4] = 1
    board[3][4] = 2
    board[4][3] = 2
    return board

def print_board(board):
    C_GREEN  = "\033[32m"
    C_BLACK  = "\033[30m"
    C_WHITE  = "\033[37m"
    C_BGGREEN  = "\033[42m"
    C_BGBLACK  = "\033[40m"
    for i in board:
        for j in i:
            if j == 0:
                print(C_BGGREEN + C_BLACK + " . ", end = "")
            if j == 1:
                print(C_BGGREEN + C_WHITE + " ● ", end = "")
            if j == 2:
                print(C_BGGREEN + C_BLACK + " ● ", end = "")
        print(C_BGBLACK + C_WHITE)
    return

def available_list(color, board):
    if not color_check(color): return [] #유효하지 않은 색상 체크
    dx = [0, 0, -1, 1, -1, -1, 1, 1]
    dy = [-1, 1, 0, 0, -1, 1, -1, 1]
    l = list()
    for i in range(8): #모든 좌표에 대해 반복문
        for j in range(8):
            if board[i][j] != color: continue #색 체크
            for k in range(8):
                x, y = i, j
                cnt = 0
                while True:
                    if x + dx[k] >= 8 or x + dx[k] < 0 or y + dy[k] >= 8 or y + dy[k] < 0: break #범위 밖을 나가는지 체크
                    x += dx[k]
                    y += dy[k]
                    if board[x][y] == color: break #같은색인지 체크
                    elif board[x][y] == 0: #빈칸인지 체크
                        if cnt == 0: break #사이에 다른색 돌이 없으면 추가 x
                        else: #있으면 빈칸의 좌표 추가
                            l.append([x, y, cnt])
                            break
                    else: cnt += 1 #사이에 다른색 돌 개수 + 1
    return l

def get_score(color, board):
    if not color_check(color): return 0
    cnt = 0
    for i in board:
        for j in i:
            if j == color: cnt += 1
    return cnt

b = make_base()
print_board(b)
print(available_list(1, b))