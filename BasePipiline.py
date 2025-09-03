import tkinter as tk

def __main__():
    # 1. Tk 객체 생성
    root = tk.Tk()

    # 2. 위젯 생성
    label = tk.Label(root, text="안녕하세요, Tkinter!")

    # 3. 위젯 배치
    label.pack()

    # 4. 이벤트 처리 (예: 버튼 클릭)
    button = tk.Button(root, text="클릭", command=lambda: print("버튼 클릭됨"))
    button.pack()

    # 5. 메인 루프 실행
    root.mainloop()

if __name__ == "__main__":
    __main__()