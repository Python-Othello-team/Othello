import random

#0 빈칸, 1 하양, 2 검정

#유효한 색상인지 확인 //작업 끝
def color_check(color):
    if color == 1 or color == 2:
        return True
    else:
        return False

#board 생성 //작업 끝
def make_base():
    board = [[0 for _ in range(8)] for _ in range(8)]
    board[3][3] = 1
    board[4][4] = 1
    board[3][4] = 2
    board[4][3] = 2
    return board

#board 출력 //현 상태에서는 작업 끝. 추후 수정이 필요하면 수정 예정
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

def print_board_debug(board):
    C_GREEN  = "\033[32m"
    C_BLACK  = "\033[30m"
    C_WHITE  = "\033[37m"
    C_BGGREEN  = "\033[42m"
    C_BGBLACK  = "\033[40m"
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                print(" ", i,".",j," ", end = "", sep="")
            if board[i][j] == 1:
                print(" ", i,".",j,"W", end = "", sep="")
            if board[i][j] == 2:
                print(" ", i,".",j,"B", end = "", sep="")
        print()
        """
            if board[i][j] == 0:
                print(C_BGBLACK + C_WHITE + " ", i,".",j," ", end = "", sep="")
            if board[i][j] == 1:
                print(C_BGGREEN + C_WHITE + " ", i,".",j," ", end = "", sep="")
            if board[i][j] == 2:
                print(C_BGGREEN + C_BLACK + " ", i,".",j," ", end = "", sep="")
        print(C_BGBLACK + C_WHITE)
        """
    return

#color 돌을 놓을 수 있는 위치 반환 //작업 끝. 테스트 필요
def available_list(color, board):
    if not color_check(color): return [] #유효하지 않은 색상 체크
    dx = [0, 0, -1, 1, -1, -1, 1, 1]
    dy = [-1, 1, 0, 0, -1, 1, -1, 1]
    l = list()
    for i in range(8): #모든 좌표에 대해 반복문
        for j in range(8):
            if board[i][j] != color: continue #색 체크
            for k in range(8): #상하좌우 대각선에 대한 체크
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
                            l.append([[i,j],[x, y]]) #시작 좌표, 놓는 돌의 좌표
                            break
                    else: cnt += 1 #사이에 다른색 돌 개수 + 1
    return l

#color 색의 돌 개수 반환 //작업 끝
def get_score(color, board):
    if not color_check(color): return 0
    cnt = 0
    for i in board:
        for j in i:
            if j == color: cnt += 1
    return cnt

#(x,y)위치에 color색 돌을 놓을 수 있는지 확인 //작업 끝. 테스트 필요
def check_place(color, board, x, y):
    if not color_check(color): return False #유효한 색인지 확인
    if x >= 8 or x < 0 or y >= 8 or y < 0: return False #위치가 범위를 벗어나는지 확인
    if board[x][y] != 0: return False #칸이 비어있는지 확인
    dx = [0, 0, -1, 1, -1, -1, 1, 1]
    dy = [-1, 1, 0, 0, -1, 1, -1, 1]
    for i in range(8):
        ddx, ddy = x, y
        cnt = 0
        while True:
            if ddx + dx[i] >= 8 or ddx + dx[i] < 0 or ddy + dy[i] >= 8 or ddy + dy[i] < 0: break #범위를 벗어나는지 확인
            ddx += dx[i]
            ddy += dy[i]
            if board[ddx][ddy] == 0: break
            elif board[ddx][ddy] != color: cnt += 1
            else:
                if cnt == 0: break
                else: return True
    return False

#(x, y) 위치에 color색 돌을 놓음. 놓을 수 없는 경우 놓지 않음 //작업끝, 버그있음
def let_stone(color, board, x, y):
    if not check_place(color, board, x, y):
        print("ASD")
        return board
    dx = [0, 0, -1, 1, -1, -1, 1, 1]
    dy = [-1, 1, 0, 0, -1, 1, -1, 1]
    board[x][y] = color
    print("Put ", x,".",y, " -> ", color, sep="")
    for i in range(8):
        ddx, ddy = x, y
        cnt = 0
        while True:
            if ddx + dx[i] >= 8 or ddx + dx[i] < 0 or ddy + dy[i] >= 8 or ddy + dy[i] < 0: break #범위를 벗어나는지 확인
            ddx += dx[i]
            ddy += dy[i]
            if board[ddx][ddy] == 0: break
            elif board[ddx][ddy] == color:
                dddx, dddy = x, y
                for _ in range(cnt):
                    dddx += dx[i]
                    dddy += dy[i]
                    board[dddx][dddy] = color
                    print(dddx,".",dddy, " -> ", color, sep="")
            elif board[ddx][ddy] != color: cnt += 1
    return board

#게임 종료 확인 //작업끝, 테스트 필요
def is_end(board):
    black_list = available_list(1, board)
    white_list = available_list(2, board)
    if len(black_list) == 0 and len(white_list) == 0: return True
    else: return False

#오델로 게임 //테스트용
def inGame():
    user_input = "" #사용자 입력 저장용
    black_list = list() #검은색이 놓을 수 있는 경우의 수
    white_list = list() #하얀색이 놓을 수 있는 경우의 수
    board = make_base()
    while not is_end(board):
        black_list = available_list(2, board)
        if len(black_list) != 0:
            choose = black_list[random.randint(0, len(black_list) - 1)]
            choose = choose[1]
            board = let_stone(2, board, choose[0], choose[1])
        print_board_debug(board)
        print()
        white_list = available_list(1, board)
        if len(white_list) != 0:
            choose = white_list[random.randint(0, len(white_list) - 1)]
            choose = choose[1]
            board = let_stone(1, board, choose[0], choose[1])
        print_board_debug(board)
        print()
    black_score = get_score(2, board)
    white_score = get_score(1, board)
    print(black_score, white_score)
    if black_score == white_score: print("DRAW!")
    elif black_score < white_score: print("WHITE WIN")
    else: print("BLACK WIN")

inGame()