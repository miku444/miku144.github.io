import pygame
import sys
import random

pygame.init()
BOARD_SIZE = 15
CELL = 40
W = BOARD_SIZE * CELL
H = BOARD_SIZE * CELL

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG = (210, 180, 130)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("五子棋 - 人类几乎不可能赢版")

# 0空 1玩家黑 2AI白
board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
player_turn = True
game_over = False

dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]

SCORE = {
    'FIVE': 1000000,
    'FOUR_LIVE': 500000,
    'FOUR_DEAD': 50000,
    'THREE_LIVE': 10000,
    'THREE_DEAD': 1000,
    'TWO_LIVE': 500,
    'TWO_DEAD': 50,
    'ONE': 1
}

def draw_board():
    screen.fill(BG)
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (CELL//2, CELL//2+i*CELL), (W-CELL//2, CELL//2+i*CELL), 1)
        pygame.draw.line(screen, BLACK, (CELL//2+i*CELL, CELL//2), (CELL//2+i*CELL, H-CELL//2), 1)

def draw_pieces():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != 0:
                x = c * CELL + CELL//2
                y = r * CELL + CELL//2
                color = BLACK if board[r][c] == 1 else WHITE
                pygame.draw.circle(screen, color, (x, y), CELL//2 - 3)

def get_click(pos):
    x, y = pos
    c = x // CELL
    r = y // CELL
    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
        return r, c
    return None

def check_win(r, c, role):
    for dr, dc in dirs:
        cnt = 1
        tr, tc = r+dr, c+dc
        while 0 <= tr < BOARD_SIZE and 0 <= tc < BOARD_SIZE and board[tr][tc] == role:
            cnt += 1
            tr += dr
            tc += dc
        tr, tc = r-dr, c-dc
        while 0 <= tr < BOARD_SIZE and 0 <= tc < BOARD_SIZE and board[tr][tc] == role:
            cnt += 1
            tr -= dr
            tc -= dc
        if cnt >= 5:
            return True
    return False

def eval_dir(r, c, dr, dc, role):
    me = str(role)
    op = str(3 - role)
    line = []
    for i in range(-4, 5):
        nr, nc = r + dr*i, c + dc*i
        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
            line.append(str(board[nr][nc]))
        else:
            line.append(op)
    s = ''.join(line)

    if me*5 in s: return SCORE['FIVE']
    if f'0{me*4}0' in s: return SCORE['FOUR_LIVE']
    if me*4+'0' in s or '0'+me*4 in s: return SCORE['FOUR_DEAD']
    if f'0{me*3}0' in s: return SCORE['THREE_LIVE']
    if me*3+'00' in s or '00'+me*3 in s or f'0{me}0{me*2}0' in s: return SCORE['THREE_DEAD']
    if f'0{me*2}0' in s: return SCORE['TWO_LIVE']
    if me*2+'00' in s or '00'+me*2 in s: return SCORE['TWO_DEAD']
    if f'0{me}0' in s: return SCORE['ONE']
    return 0

def point_score(r, c, role):
    if board[r][c] != 0:
        return -1
    sc = 0
    for dr, dc in dirs:
        sc += eval_dir(r, c, dr, dc, role)
    return sc

def evaluate():
    ai = 0
    player = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == 1:
                player += point_score(r, c, 1)
            elif board[r][c] == 2:
                ai += point_score(r, c, 2)
    return ai - player

def gen_candidates():
    res = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == 0:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] != 0:
                            res.append((r, c))
                            break
                    else:
                        continue
                    break
    if not res:
        return [(7, 7)]
    return list(set(res))

def minimax(depth, alpha, beta, is_max):
    if depth == 0:
        return evaluate()
    candidates = gen_candidates()
    if is_max:
        max_sc = -float('inf')
        for r, c in candidates:
            if board[r][c] != 0:
                continue
            board[r][c] = 2
            sc = minimax(depth-1, alpha, beta, False)
            board[r][c] = 0
            max_sc = max(max_sc, sc)
            alpha = max(alpha, sc)
            if beta <= alpha:
                break
        return max_sc
    else:
        min_sc = float('inf')
        for r, c in candidates:
            if board[r][c] != 0:
                continue
            board[r][c] = 1
            sc = minimax(depth-1, alpha, beta, True)
            board[r][c] = 0
            min_sc = min(min_sc, sc)
            beta = min(beta, sc)
            if beta <= alpha:
                break
        return min_sc

def ai_best():
    best = -float('inf')
    moves = []
    # 先看有没有一步杀
    for r, c in gen_candidates():
        board[r][c] = 2
        if check_win(r, c, 2):
            board[r][c] = 0
            return (r, c)
        board[r][c] = 0
    # 再看要不要堵对方一步杀
    for r, c in gen_candidates():
        board[r][c] = 1
        if check_win(r, c, 1):
            board[r][c] = 0
            return (r, c)
        board[r][c] = 0
    # 深度4层搜索
    for r, c in gen_candidates():
        if board[r][c] != 0:
            continue
        board[r][c] = 2
        sc = minimax(4, -float('inf'), float('inf'), False)
        board[r][c] = 0
        if sc > best:
            best = sc
            moves = [(r, c)]
        elif sc == best:
            moves.append((r, c))
    return random.choice(moves)

# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player_turn:
            pos = get_click(event.pos)
            if pos:
                r, c = pos
                if board[r][c] == 0:
                    board[r][c] = 1
                    if check_win(r, c, 1):
                        print("你赢了！（不可思议）")
                        game_over = True
                    player_turn = False

    if not player_turn and not game_over:
        r, c = ai_best()
        board[r][c] = 2
        if check_win(r, c, 2):
            print("AI赢了！")
            game_over = True
        player_turn = True

    draw_board()
    draw_pieces()
    pygame.display.flip()