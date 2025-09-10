import tkinter as tk

# 10단계: 복합 위젯 및 레이아웃
# - 여러 위젯을 조합하여 간단한 폼 만들기

def main():
    root = tk.Tk()
    root.title("10단계: 복합 위젯")
    root.geometry("400x300")

    # 프레임으로 그룹화
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # 라벨과 엔트리
    tk.Label(frame, text="이름:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="나이:").grid(row=1, column=0, padx=5, pady=5)
    age_entry = tk.Entry(frame)
    age_entry.grid(row=1, column=1, padx=5, pady=5)

    # 버튼
    def submit():
        name = name_entry.get()
        age = age_entry.get()
        print(f"이름: {name}, 나이: {age}")

    submit_button = tk.Button(frame, text="제출", command=submit)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
