import tkinter as tk

# 5단계: 이벤트 처리 및 상태 변경
# - Label과 Button을 연결하여 상태 변경

def main():
    root = tk.Tk()
    root.title("5단계: 이벤트 처리")
    root.geometry("300x200")

    count = 0
    label = tk.Label(root, text=f"카운트: {count}")
    label.pack()

    def increment():
        nonlocal count
        count += 1
        label.config(text=f"카운트: {count}")

    button = tk.Button(root, text="증가", command=increment)
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
