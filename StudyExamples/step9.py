import tkinter as tk

# 9단계: Listbox 사용
# - Listbox로 목록 표시 및 선택

def main():
    root = tk.Tk()
    root.title("9단계: Listbox 사용")
    root.geometry("300x200")

    listbox = tk.Listbox(root)
    listbox.pack(fill=tk.BOTH, expand=True)

    # 항목 추가
    items = ["항목 1", "항목 2", "항목 3", "항목 4"]
    for item in items:
        listbox.insert(tk.END, item)

    def on_select(event):
        selected = listbox.curselection()
        if selected:
            print("선택된 항목:", listbox.get(selected[0]))

    listbox.bind("<<ListboxSelect>>", on_select)

    root.mainloop()

if __name__ == "__main__":
    main()
