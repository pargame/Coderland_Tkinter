import tkinter as tk

# 2단계: Label 위젯 추가
# - Label 생성 및 배치
# - 텍스트 표시

def main():
    root = tk.Tk()
    root.title("2단계: Label 추가")
    root.geometry("300x200")

    label = tk.Label(root, text="안녕하세요, Tkinter!")
    label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
