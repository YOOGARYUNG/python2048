import tkinter as tk
import random

class Game2048:
    def __init__(self):
        # Tkinter 창 생성
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.window.geometry("400x400")

        # 4x4 크기의 보드
        self.board = [[0] * 4 for _ in range(4)]
        # 점수 초기화
        self.score = 0

        # UI 초기화
        self.initUI()
        # 초기 타일 생성
        self.spawn_tile()
        # UI 업데이트
        self.update_ui()

        # Tkinter 이벤트 루프 시작
        self.window.mainloop()

    def initUI(self):
        # Tkinter 캔버스 생성
        self.canvas = tk.Canvas(self.window, bg="white", width=400, height=400)
        self.canvas.pack()

        # 키 이벤트 바인딩
        self.window.bind("<Key>", self.on_key_press)

    def draw_board(self):
        # 캔버스의 타일 영역 지우기
        self.canvas.delete("tiles")
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                x, y = j * 100, i * 100 # 100*100크기의 타일
                # 각 타일 그리기
                self.canvas.create_rectangle(x, y, x + 100, y + 100, fill="#FFE5C2", tags="tiles")
                if value != 0:
                    self.canvas.create_text(x + 50, y + 50, text=str(value), font=("Arial", 20, "bold"), tags="tiles")

    def update_ui(self):
        # 보드 업데이트 및 점수 표시
        self.draw_board()
        self.window.title(f"2048 Game - Score: {self.score}")

    def spawn_tile(self):
        # 빈 셀 중에서 무작위로 타일 생성
        # 16칸 중에 임의의 하나가 0이면 = empty_cells
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        # 이동 방향에 따라 적절한 메소드 호출
        if direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        elif direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()

    def move_left(self):
        # 왼쪽키으로 이동하는 메소드
        for i in range(4):
            # self.board[i][::-1]: i번째 행을 뒤집는다.
            # 뒤집은 행을 slide_and_combine 메소드에 전달
            # [::-1]slide_and_combine 메소드의 결과를 다시 뒤집어서 원래의 순서로 되돌립니다.
            self.board[i] = self.slide_and_combine(self.board[i][::-1])[::-1]


    def move_right(self):
        # 오른쪽으로 이동하는 메소드
        for i in range(4):
            self.board[i] = self.slide_and_combine(self.board[i])

    def move_up(self):
        # 위로 이동하는 메소드
        transposed_board = [list(row) for row in zip(*self.board)]
        for i in range(4):
            transposed_board[i] = self.slide_and_combine(transposed_board[i][::-1])[::-1]
        self.board = [list(row) for row in zip(*transposed_board)]

    def move_down(self):
        # 아래로 이동하는 메소드
        transposed_board = [list(row) for row in zip(*self.board)]
        for i in range(4):
            transposed_board[i] = self.slide_and_combine(transposed_board[i])
        self.board = [list(row) for row in zip(*transposed_board)]


    def slide_and_combine(self, row):
        # 타일을 슬라이드하고 합치는 메소드
        non_zero_tiles = [tile for tile in row if tile != 0] # 만약 타일이 0이 아니라면
        new_row = [0] * (4 - len(non_zero_tiles)) + non_zero_tiles

        for i in range(3, 0, -1):
            if new_row[i] == new_row[i - 1]: # 만약 현재위치와 그전위치의 값이 같다면
                new_row[i] *= 2              # 원래값의 2배증가
                self.score += new_row[i]     # 합친 점수만큼 스코어 증가
                new_row[i - 1] = 0           # 2개의 타일이 하나로 합쳐져 -1을 하면 0이 됨

        non_zero_tiles = [tile for tile in new_row if tile != 0] # 비어있는 타일 = non_zero_tiles
        # 0으로 이루어진 리스트를 생성 길이는 4 - len(non_zero_tiles)
        return [0] * (4 - len(non_zero_tiles)) + non_zero_tiles  # 0이 아닌 값들은 원래의 순서를 유지하고, 나머지는 0으로 채워진 리스트가 반환된다.

    def on_key_press(self, event):  # on_key_press메소드
        # 키 이벤트 처리
        key = event.keysym.lower()
        if key in ("left", "right", "up", "down"): # 왼,오,위.아래 키를 누르면
            self.move(key)          # move메소드 실행되며 타일 이동
            self.spawn_tile()       # 랜덤으로  빈공간중 타일 생성
            self.update_ui()        # 점수 업데이트

if __name__ == "__main__":
    # 게임 시작
    game = Game2048()
