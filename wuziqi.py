import tkinter as tk
import math

BOARD_SIZE = 15
GRID_SIZE = 40
EMPTY = 0
BLACK = 1
WHITE = 2

SEARCH_DEPTH = 3   # 👉 改成4会更变态（但更慢）

class Gomoku:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋（变态AI版）")

        self.canvas = tk.Canvas(root, width=GRID_SIZE*BOARD_SIZE, height=GRID_SIZE*BOARD_SIZE, bg="#DDB88C")
        self.canvas.pack()

        self.board = [[EMPTY]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.canvas.bind("<Button-1>", self.click)

        self.draw_board()

    def draw_board(self):
        for i in range(BOARD_SIZE):
            self.canvas.create_line(GRID_SIZE/2, GRID_SIZE/2 + i*GRID_SIZE,
                                    GRID_SIZE/2 + (BOARD_SIZE-1)*GRID_SIZE, GRID_SIZE/2 + i*GRID_SIZE)
            self.canvas.create_line(GRID_SIZE/2 + i*GRID_SIZE, GRID_SIZE/2,
                                    GRID_SIZE/2 + i*GRID_SIZE, GRID_SIZE/2 + (BOARD_SIZE-1)*GRID_SIZE)

    def click(self, event):
        x = round((event.y - GRID_SIZE/2) / GRID_SIZE)
        y = round((event.x - GRID_SIZE/2) / GRID_SIZE)

        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            return
        if self.board[x][y] != EMPTY:
            return

        self.place(x, y, BLACK)

        if self.win(x, y, BLACK):
            self.show("你赢了（不太可能）")
            return

        self.root.after(100, self.ai_move)

    def place(self, x, y, player):
        self.board[x][y] = player
        color = "black" if player == BLACK else "white"
        self.canvas.create_oval(
            y*GRID_SIZE+8, x*GRID_SIZE+8,
            y*GRID_SIZE+GRID_SIZE-8, x*GRID_SIZE+GRID_SIZE-8,
            fill=color
        )

    def ai_move(self):
        _, move = self.minimax(SEARCH_DEPTH, -math.inf, math.inf, True)
        if move:
            x, y = move
            self.place(x, y, WHITE)
            if self.win(x, y, WHITE):
                self.show("AI：结束了")

    # ================= AI核心 =================

    def evaluate(self):
        return self.score_player(WHITE) - self.score_player(BLACK)*1.2

    def score_player(self, player):
        score = 0
        patterns = {
            (5,0):100000,
            (4,2):10000,
            (4,1):5000,
            (3,2):1000,
            (3,1):200,
            (2,2):50
        }

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == player:
                    for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:
                        count, open_ends = self.count(i,j,dx,dy,player)
                        score += patterns.get((count,open_ends),0)
        return score

    def count(self, x, y, dx, dy, player):
        count = 1
        open_ends = 0

        for d in [1,-1]:
            nx, ny = x, y
            while True:
                nx += dx*d
                ny += dy*d
                if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE:
                    if self.board[nx][ny] == player:
                        count += 1
                    elif self.board[nx][ny] == EMPTY:
                        open_ends += 1
                        break
                    else:
                        break
                else:
                    break
        return count, open_ends

    def get_moves(self):
        moves = set()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] != EMPTY:
                    for dx in range(-2,3):
                        for dy in range(-2,3):
                            nx, ny = i+dx, j+dy
                            if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE:
                                if self.board[nx][ny] == EMPTY:
                                    moves.add((nx,ny))
        if not moves:
            return [(7,7)]

        # ⭐ 排序（关键优化）
        return sorted(moves, key=lambda m: self.move_score(m[0], m[1]), reverse=True)[:10]

    def move_score(self, x, y):
        self.board[x][y] = WHITE
        score = self.evaluate()
        self.board[x][y] = EMPTY
        return score

    def minimax(self, depth, alpha, beta, maximizing):
        if depth == 0:
            return self.evaluate(), None

        moves = self.get_moves()
        best_move = None

        if maximizing:
            max_eval = -math.inf
            for x,y in moves:
                self.board[x][y] = WHITE

                if self.win(x,y,WHITE):
                    self.board[x][y] = EMPTY
                    return 100000, (x,y)

                eval,_ = self.minimax(depth-1, alpha, beta, False)
                self.board[x][y] = EMPTY

                if eval > max_eval:
                    max_eval = eval
                    best_move = (x,y)

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = math.inf
            for x,y in moves:
                self.board[x][y] = BLACK

                if self.win(x,y,BLACK):
                    self.board[x][y] = EMPTY
                    return -100000, (x,y)

                eval,_ = self.minimax(depth-1, alpha, beta, True)
                self.board[x][y] = EMPTY

                if eval < min_eval:
                    min_eval = eval
                    best_move = (x,y)

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move

    # =========================================

    def win(self, x, y, player):
        for dx,dy in [(1,0),(0,1),(1,1),(1,-1)]:
            count = 1
            for d in [1,-1]:
                nx,ny = x,y
                while True:
                    nx+=dx*d
                    ny+=dy*d
                    if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and self.board[nx][ny]==player:
                        count+=1
                    else:
                        break
            if count>=5:
                return True
        return False

    def show(self, text):
        self.canvas.create_text(300,300,text=text,fill="red",font=("Arial",28))


if __name__ == "__main__":
    root = tk.Tk()
    game = Gomoku(root)
    root.mainloop()