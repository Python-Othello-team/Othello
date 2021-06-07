import random
import pygame
import sys

#0 빈칸, 1 하양, 2 검정

#유효한 색상인지 확인 //작업 끝
def color_check(color):
    if color == 1 or color == 2:
        return True
    else:
        return False

#다른 색상 받기
def other_color(color):
    if color_check(color):
        if color == 1: return 2
        else: return 1

#board 생성 //작업 끝
def make_base():
    board = [[0 for _ in range(8)] for _ in range(8)]
    board[3][3] = 1
    board[4][4] = 1
    board[3][4] = 2
    board[4][3] = 2
    return board

#color 돌을 놓을 수 있는 위치 반환 //작업 끝.
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
                            if not [x,y] in l:
                                l.append([x, y]) #놓는 돌의 좌표
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

#(x,y)위치에 color색 돌을 놓을 수 있는지 확인 //작업 끝.
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

#(x, y) 위치에 color색 돌을 놓음. 놓을 수 없는 경우 놓지 않음 //작업끝
def let_stone(color, board, x, y):
    if not check_place(color, board, x, y): return board
    dx = [0, 0, -1, 1, -1, -1, 1, 1]
    dy = [-1, 1, 0, 0, -1, 1, -1, 1]
    board[x][y] = color
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
            elif board[ddx][ddy] != color: cnt += 1
    return board

#게임 종료 확인 //작업끝
def is_end(board):
    black_list = available_list(1, board)
    white_list = available_list(2, board)
    if len(black_list) == 0 and len(white_list) == 0: return True
    else: return False

#오셀로 판 그리기 -> pygame
def draw_base(screen):
    COLOR1 = (139,79,18)
    COLOR2 = (240,183,127)
    #COLOR2 = (246,198,151)
    pygame.draw.rect(screen, COLOR2, [0, 0, 512, 512])
    for i in range(8):
        if i % 2 == 0:
            for j in range(1, 8, 2):
                pygame.draw.rect(screen, COLOR1, [i * 64, j * 64, 64, 64])
        else:
            for j in range(0, 8, 2):
                pygame.draw.rect(screen, COLOR1, [i * 64, j * 64, 64, 64])

#돌 그리기 -> pygame
def draw_checker(screen, board):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                pygame.draw.circle(screen, WHITE, [32 + i * 64, 32 + j * 64], 25)
            elif board[i][j] == 2:
                pygame.draw.circle(screen, BLACK, [32 + i * 64, 32 + j * 64], 25)

#돌을 놓을 수 있는 위치 표시 -> pygame
def draw_let_place(screen, place_list):
    COLOR = (127,240,142)
    for i in place_list:
        pygame.draw.circle(screen, COLOR, [32 + i[0] * 64, 32 + i[1] * 64], 4)

#마우스 클릭 위치를 격자의 몇번째 칸인지 변환 -> pygame
def click_position(x, y):
    return x // 64, y // 64

#검은돌, 흰돌 선택 -> pygame
def select_player_turn(screen):
    while True:
        screen.fill((255,255,255))
        draw_base(screen)
        event = pygame.event.poll()
        COLOR = (100, 100, 100)
        pygame.draw.rect(screen, COLOR, [50, 300, 150, 50])
        pygame.draw.rect(screen, COLOR, [316, 300, 150, 50])
        font = pygame.font.Font('D2Codingl.ttc', 30)
        text1 = font.render("흑돌", True, (255,255,255))
        text2 = font.render("백돌", True, (255,255,255))
        screen.blit(text1, (95, 308))
        screen.blit(text2, (361, 308))

        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos[0], event.pos[1] #마우스 클릭 좌표 받기
                if 50 <= x <= 200 and 300 <= y <= 350:
                    return 2
                elif 316 <= x <= 456 and 300 <= y <= 350:
                    return 1
        pygame.display.flip() 

#승자 표시 -> pygame
def draw_winner(screen, board):
    white_score = get_score(1, board) #흰돌 개수
    black_score = get_score(2, board) #검은돌 개수

    text = ""
    if white_score == black_score: #이긴사람 판정
        print("DRAW")
        text = "무승부"
    elif white_score > black_score:
        print("WHITE WIN")
        text = "흰색 승리"
    else:
        print("BLACK WIN")
        text = "검은색 승리"

    font = pygame.font.Font('D2Codingl.ttc', 50) #글씨 그리기
    text = font.render(text, True, (150,150,150))
    text_Rect = text.get_rect()
    text_Rect.centerx = 256
    text_Rect.y = 200

    while True:
        draw_base(screen)
        draw_checker(screen, board)
        screen.blit(text, text_Rect)
        pygame.display.flip() 
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: #마우스 클릭했을때
            if event.button == 1:
                sys.exit()

#플레이어 차례 -> pygame
def player_turn(screen, board, color):
    place = available_list(color, board)
    while True:
        #기본적인거 그리는 부분
        screen.fill((255,255,255))
        draw_base(screen)
        draw_checker(screen, board)
        draw_let_place(screen, place)
        pygame.display.flip()

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: #마우스 클릭했을때
            if event.button == 1:
                x, y = click_position(event.pos[0], event.pos[1]) #어느칸 클릭했는지 확인
                if [x, y] in place: #돌을 놓을 수 있는 위치 확인
                    board = let_stone(color, board, x, y)  #돌 놓고 반복문 탈출
                    break
                elif len(place) == 0: #돌을 놓을 수 없다면 반복문 탈출
                    break
    return board

#ai 차례 -> pygame
def ai_turn(screen, board, color):
    place = available_list(color, board)
    #기본적인거 그리는 부분
    screen.fill((255,255,255))
    draw_base(screen)
    draw_checker(screen, board)
    pygame.display.flip()

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        sys.exit()

    if len(place) != 0:
        choose = place[random.randint(0, len(place) - 1)] #돌을 놓을 수 있는 위치 중에서 무작위로 1개 선택
        board = let_stone(color, board, choose[0], choose[1]) #돌 놓음
        return board
    else: #돌을 놓을 수 없다면 board 그대로 반환
        return board

#Log.txt 초기화
def reset_log():
    f = open("Log.txt", 'w')
    f.close()
    return

#Log.txt에 현재 턴 저장
def save_turn(board):
    f = open("Log.txt", 'a')
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                f.write(" " + str(i) + "." + str(j) + " ")
            if board[i][j] == 1:
                f.write(" " + str(i) + "." + str(j) + "W")
            if board[i][j] == 2:
                f.write(" " + str(i) + "." + str(j) + "B")
        f.write('\n')
    f.write('\n')
    f.write('\n')
    f.close()
    return

#게임
def inGame():
    board = make_base()
    pygame.init()
    MainScreen = pygame.display.set_mode([512, 512])
    pygame.display.set_caption("오델로")
    player_color = select_player_turn(MainScreen)
    ai_color = other_color(player_color)
    turn = 1
    reset_log()
    save_turn(board)
    while not is_end(board):
        if turn == player_color:
            board = player_turn(MainScreen, board, player_color)
            turn = ai_color
        else:
            board = ai_turn(MainScreen, board, ai_color)
            turn = player_color
        save_turn(board)
    draw_winner(MainScreen, board)

inGame()