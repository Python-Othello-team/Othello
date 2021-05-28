import random

#0 빈칸, 1 하양, 2 검정
def color_check(color):
    if color == 1 or color == 2:
        return True
    else:
        return False

def make_base():
    board = []
    return board

def available_check(color, board):
    if not color_check(color): return []
    return

def get_score(color, board):
    if not color_check(color): return 0
    return