import tkinter as tk

# 4단계: Entry 위젯 추가
# - Entry 생성 및 배치
# - 텍스트 입력 받기

def main():
    root = tk.Tk()
    root.title("4단계: Entry 추가")
    root.geometry("300x200")

    entry = tk.Entry(root)
    entry.pack()

    def get_text():
        label.config(text=f'input entry text: {entry.get()}')

    button = tk.Button(root, text="fetch text", command=get_text)
    button.pack()

    label = tk.Label(root, text="input text:")
    label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
