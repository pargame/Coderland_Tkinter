import tkinter as tk

# 8단계: 메뉴 추가
# - 메뉴 바 생성 및 메뉴 항목 추가

def main():
    root = tk.Tk()
    root.title("8단계: 메뉴 추가")
    root.geometry("300x200")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="파일", menu=file_menu)
    file_menu.add_command(label="새 파일")
    file_menu.add_command(label="열기")
    file_menu.add_separator()
    file_menu.add_command(label="종료", command=root.quit)

    root.mainloop()

if __name__ == "__main__":
    main()
