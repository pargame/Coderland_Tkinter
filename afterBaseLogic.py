import tkinter as tk

# 함수: 라벨의 텍스트를 업데이트하고 1초 후에 다시 실행
# 전역 변수 counter를 증가시키고, 라벨의 텍스트를 업데이트
# root.after를 사용하여 주기적으로 이 함수를 호출
def update_label():
    global counter  # 전역 변수 counter를 수정하기 위해 global 선언
    counter += 1  # counter 값을 1 증가
    label.config(text=f"카운트: {counter}")  # 라벨의 텍스트를 업데이트
    root.after(1000, update_label)  # 1초 후에 update_label 함수를 다시 호출

# Tk 객체 생성: GUI 애플리케이션의 메인 윈도우 생성
root = tk.Tk()

# 초기 변수 설정: 카운터 초기값을 0으로 설정
counter = 0

# 라벨 위젯 생성: 텍스트를 표시하는 라벨 생성
label = tk.Label(root, text="안녕하세요, Tkinter!")
label.pack()  # 라벨을 윈도우에 배치

# 버튼 위젯 생성: 클릭 시 애플리케이션을 종료하는 버튼 생성
button = tk.Button(root, text="종료", command=root.destroy)
button.pack()  # 버튼을 윈도우에 배치

# 주기적인 작업 시작: 1초 후에 update_label 함수 호출 시작
root.after(1000, update_label)

# 메인 루프 실행: GUI 애플리케이션 실행 및 사용자 입력 대기
root.mainloop()