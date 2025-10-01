"""
BushAdvencher Map Editor
메인 실행 파일
"""
from editor import MapEditor

if __name__ == "__main__":
    print("=" * 50)
    print("BushAdvencher Map Editor")
    print("=" * 50)
    print("\n조작법:")
    print("- 좌측 패널에서 아이템을 클릭하고 맵으로 드래그")
    print("- 우클릭: 타일 제거")
    print("- Play 버튼 또는 P: 플레이 모드 토글")
    print("- 플레이 모드: 화살표 키 또는 WASD로 이동")
    print("- ESC: 플레이 모드 종료 또는 프로그램 종료")
    print("- Ctrl+S: 저장, Ctrl+O: 불러오기")
    print("\n아이템:")
    print("- Player Start (녹색): 플레이어 시작 위치 (맵에 하나만)")
    print("- Bush (어두운 녹색): 지나갈 수 있음 (추후 몬스터 조우)")
    print("- Stone (회색): 지나갈 수 없음")
    print("=" * 50)
    print()
    
    editor = MapEditor(1200, 800)
    editor.run()
