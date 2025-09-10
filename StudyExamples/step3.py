import tkinter as tk

# 3단계: Button 위젯 추가
# - Button 생성 및 배치
# - 클릭 이벤트 처리

def main():
    root = tk.Tk()
    root.title("3단계: Button 추가")
    root.geometry("300x200")

    def on_click():
        print("버튼이 클릭되었습니다!")

    button = tk.Button(root, text="클릭하세요", command=on_click)
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
