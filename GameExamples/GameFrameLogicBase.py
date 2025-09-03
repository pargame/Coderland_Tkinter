import tkinter as tk

# 프레임 속도 설정 (초당 60 프레임)
FPS = 60
FRAME_DELAY = int(1000 / FPS)  # 한 프레임당 지연 시간 (밀리초)

# Tk 객체 생성
root = tk.Tk()
root.title("Simple Game Loop")

# 캔버스 생성 (게임 화면)
canvas = tk.Canvas(root, width=1280, height=720, bg="black")
canvas.pack()

# 게임 상태 변수
x, y = 200, 150  # 공의 초기 위치
dx, dy = 15, 15    # 공의 이동 속도

# 게임 업데이트 함수
def update_game():
    global x, y, dx, dy

    # 공 이동
    x += dx
    y += dy

    # 벽 충돌 처리
    if x <= 0 or x >= 1280:
        dx = -dx
    if y <= 0 or y >= 720:
        dy = -dy

    # 화면 갱신
    canvas.delete("all")  # 이전 프레임 지우기
    canvas.create_oval(x-10, y-10, x+10, y+10, fill="white")  # 공 그리기

    # 다음 프레임 예약
    root.after(FRAME_DELAY, update_game)

# 게임 루프 시작
update_game()

# 메인 루프 실행
root.mainloop()