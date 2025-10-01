# BushAdvencher Map Editor

Pygame 기반의 타일 맵 에디터 + 플레이 모드 엔진

## 기능

- ✅ 타일 기반 맵 에디터 (드래그앤드롭)
- ✅ 3가지 아이템 타입 (Player Start, Bush, Stone)
- ✅ 플레이 버튼으로 즉시 테스트
- ✅ 플레이어 이동 및 충돌 처리
- ✅ 맵 저장/불러오기 (JSON)

## 실행 방법

```bash
python main.py
```

## 필요 패키지

```bash
pip install pygame
```

## Controls

### Editor Mode
- **Left panel click**: Select item (cursor changes to item)
- **Left click/drag in view**: Place selected item continuously
- **Right click/drag (view)**: Erase tiles continuously
- **'Drop Item' button**: Deselect item (return to default mode)
- **Default mode drag**: Move view (pan camera)
- **Play button** or **P key**: Switch to play mode
- **Ctrl + S**: 맵 저장 (`map_save.json`)
- **Ctrl + O**: 맵 불러오기
- **ESC**: 프로그램 종료

### Play Mode
- **Arrow keys** or **WASD**: Move player (hold to move continuously)
- **ESC** or **Stop button**: Return to editor mode
- **Player position**: Displayed in top bar (yellow text)

## Item Types

1. **Player Start (red)**: Player spawn position
   - Only one can be placed per map
   - Required to start play mode
   - Hidden during play mode

2. **Bush (dark green)**: Walkable grass
   - Player can pass through
   - Future: Random monster encounter

3. **Stone (gray)**: Blocking obstacle
   - Player cannot pass through (collision)

## File Structure

```
BushAdvencher/
├── main.py              # Main entry point
├── editor.py            # Editor main logic
├── map_data.py          # Map data structure and save/load
├── item_types.py        # Item type definitions
├── player.py            # Player class
├── 기획안.md            # Project design document (Korean)
└── README.md            # This file
```

## Future Development

- [ ] Random monster encounter system in Bush tiles
- [ ] Battle screen transition
- [ ] More tile/item types
- [ ] Undo/Redo functionality
- [ ] Tile animations
- [ ] Minimap
- [ ] Extended layer system

## License

MIT License
