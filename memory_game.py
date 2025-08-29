import tkinter as tk
from random import choice

root = tk.Tk()
buttons = [[None for _ in range(3)] for _ in range(3)]

# 중앙 라벨: 시퀀스를 색으로 보여줄 영역
label1 = tk.Label(
    root,
    width=14,
    height=7,
    bg="white",
    fg="white",
    relief="flat",
    font=("Arial", 12),
)

colors = ["red", "blue", "green", "yellow", "orange", "pink", "brown", "gray"]
color_index = 0
memory_color = []
input_index = 0
is_waiting_for_input = False


def start_next_round():
    # 라운드마다 색 하나 추가 후 표시 시작
    new_color = choice(colors)
    memory_color.append(new_color)
    set_buttons_state(False)
    show_sequence(0)


def show_sequence(index=0):
    # 라벨 배경색을 번갈아 바꿔 시퀀스를 보여줌
    if index < len(memory_color):
        label1.config(bg=memory_color[index])
        root.after(
            350,
            lambda: (
                label1.config(bg="white"),
                root.after(100, lambda: show_sequence(index + 1)),
            ),
        )
    else:
        global is_waiting_for_input, input_index
        label1.config(bg="white")
        # 표시가 끝나면 입력 단계로 전환
        set_buttons_state(True)
        is_waiting_for_input = True
        input_index = 0


def reset_game():
    global memory_color, is_waiting_for_input, input_index
    memory_color = []
    is_waiting_for_input = False
    input_index = 0
    root.after(500, start_next_round)


def button_click(color):
    global input_index, is_waiting_for_input
    # 시퀀스 표시 중에는 입력 무시
    if not is_waiting_for_input:
        return
    # 현재 기대하는 색과 비교
    expected_color = memory_color[input_index]
    if color == expected_color:
        input_index += 1
        if input_index == len(memory_color):
            # 전부 맞히면 다음 라운드로 진행
            is_waiting_for_input = False
            set_buttons_state(False)
            root.after(100, start_next_round)
    else:
        # 오답이면 종료
        is_waiting_for_input = False
        root.destroy()


for row in range(3):
    for col in range(3):
        if row == 1 and col == 1:
            label1.grid(row=row, column=col)
            buttons[row][col] = label1
        else:
            current_color = colors[color_index % len(colors)]
            btn = tk.Button(
                root,
                width=14,
                height=7,
                bg=current_color,
                activebackground=current_color,
                font=("Arial", 12),
                command=lambda color=current_color: button_click(color),
            )
            btn.grid(row=row, column=col)
            btn.config(state=tk.DISABLED)
            buttons[row][col] = btn
            color_index += 1


def set_buttons_state(is_enabled: bool) -> None:
    state = tk.NORMAL if is_enabled else tk.DISABLED
    for row_widgets in buttons:
        for widget in row_widgets:
            if isinstance(widget, tk.Button):
                widget.config(state=state)


root.after(300, start_next_round)


root.mainloop()

print(
    f"""your score: {len(memory_color) - 1}
last color: {" → ".join(memory_color)}"""
)
