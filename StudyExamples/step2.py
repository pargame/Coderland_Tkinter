import tkinter as tk

# 2단계: Label 위젯 추가
# - Label 생성 및 배치
# - 텍스트 표시

def main():
    root = tk.Tk()
    root.title("2단계: Label 추가")
    root.geometry("300x200")

    # 배치 방법 설명 (Geometry Managers)
    # Tkinter에서 위젯을 배치하는 방법은 크게 3가지: pack(), grid(), place()
    #
    # 1. pack() - 가장 간단한 방법, 위젯을 부모 컨테이너에 순서대로 쌓아 배치
    #    - 옵션: side (TOP, BOTTOM, LEFT, RIGHT), fill (X, Y, BOTH), expand (True/False), padx/pady (여백)
    #    - 장점: 자동으로 크기 조절, 간단한 레이아웃에 적합
    #    - 단점: 복잡한 레이아웃에서는 제한적
    #
    # 2. grid() - 테이블 형태로 배치, 행과 열로 위치 지정
    #    - 옵션: row, column (행/열 번호), rowspan/colspan (병합), sticky (N, S, E, W, NW 등), padx/pady
    #    - 장점: 복잡한 레이아웃에 유용, 상대적 위치 조절 가능
    #    - 단점: pack()과 혼용 불가
    #
    # 3. place() - 절대적 위치 지정 (픽셀 단위)
    #    - 옵션: x, y (좌표), width, height, relx/rely (상대 좌표), anchor (위치 기준점)
    #    - 장점: 정밀한 위치 제어
    #    - 단점: 창 크기 변경 시 재조정 필요, 복잡한 레이아웃에 부적합
    #
    # 파이프라인: 위젯 생성 -> 속성 설정 -> 배치 방법 선택 -> pack/grid/place() 호출 -> 부모 컨테이너에 추가

    label = tk.Label(root, text="안녕하세요, Tkinter!")
    label.pack()  # pack() 사용: 위젯을 세로로 쌓아 중앙 배치

    root.mainloop()

if __name__ == "__main__":
    main()
