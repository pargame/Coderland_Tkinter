import tkinter as tk

# 7단계: Canvas 그리기
# - Canvas 위젯으로 도형 그리기

def main():
    root = tk.Tk()
    root.title("7단계: Canvas 그리기")
    root.geometry("400x300")

    canvas = tk.Canvas(root, bg="white")
    canvas.pack(fill="both", expand=True)

    # 사각형 그리기
    canvas.create_rectangle(50, 50, 150, 150, fill="blue")

    # 원 그리기
    canvas.create_oval(200, 50, 300, 150, fill="red")

    root.mainloop()

if __name__ == "__main__":
    main()
