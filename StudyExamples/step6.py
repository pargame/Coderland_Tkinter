import tkinter as tk

# 6단계: Frame 사용
# - Frame으로 위젯 그룹화
# - 레이아웃 정리

def main():
    root = tk.Tk()
    root.title("6단계: Frame 사용")
    root.geometry("300x200")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    label = tk.Label(frame, text="프레임 안의 라벨")
    label.pack()

    button = tk.Button(frame, text="프레임 안의 버튼")
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
