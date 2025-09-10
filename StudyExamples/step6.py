import tkinter as tk

# 6단계: Frame 사용
# - Frame으로 위젯 그룹화
# - 레이아웃 정리

def main():
    root = tk.Tk()
    root.title("6단계: Frame 사용")
    root.geometry("300x200")

    # Frame 설명: Frame은 다른 위젯들을 그룹화하는 컨테이너 위젯
    # - Frame은 투명한 컨테이너로, 자체적으로 보이지 않지만 내부 위젯들을 묶어 관리
    # - 그룹화의 장점:
    #   1. 레이아웃 정리: 관련된 위젯들을 하나의 단위로 묶어 배치
    #   2. 스타일 적용: Frame에 배경색, 테두리 등을 설정하면 그룹 전체에 적용
    #   3. 코드 구조화: 복잡한 UI를 작은 그룹으로 나누어 관리
    #   4. 재사용성: Frame을 다른 곳에 쉽게 이동하거나 복사 가능
    #
    # 그룹화 과정:
    # 1. Frame 생성: tk.Frame(root) - root를 부모로 하는 Frame 생성
    # 2. Frame 배치: frame.pack(pady=20) - Frame을 root에 배치 (위젯 간 여백 20)
    # 3. 내부 위젯 생성: tk.Label(frame, ...) - Frame을 부모로 하는 Label 생성
    # 4. 내부 위젯 배치: label.pack() - Frame 내부에서 pack()으로 배치
    # 5. 결과: Label과 Button은 Frame에 묶여 함께 이동/관리됨
    #
    # Frame의 부모-자식 관계:
    # root (최상위 창)
    #   └── frame (Frame 위젯)
    #       ├── label (Label 위젯)
    #       └── button (Button 위젯)

    pady = 20
    frame = tk.Frame(root)
    frame.pack(pady=pady)

    label = tk.Label(frame, text="프레임 안의 라벨")
    label.pack()

    def expand_frame():
        nonlocal pady
        pady += 20
        frame.config()

    button = tk.Button(frame, text="프레임 안의 버튼", command=expand_frame)
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
