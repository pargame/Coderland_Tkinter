# BushAdvencher Map Editor

Pygame 기반의 타일 맵 에디터 + 플레이 모드 엔진

## Features

- ✅ Tile-based map editor (drag and drop)
- ✅ 3 item types (Player Start, Bush, Stone)
- ✅ Play button for instant testing
- ✅ Player movement and collision detection
- ✅ Map save/load (JSON)
- ✅ **Pixel art editor** for custom item sprites
- ✅ Custom sprite save/load (JSON)
- ✅ 32x32 pixel canvas with color palette
- ✅ Real-time sprite preview in editor

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
- **'Design' button**: Enter pixel editor for selected item
- **Default mode drag**: Move view (pan camera)
- **Play button** or **P key**: Switch to play mode
- **Ctrl+S**: Save map (or sprites in design mode)

### Pixel Design Mode
- **Left click/drag on canvas**: Paint pixels with selected color
- **Color palette**: Click to select color
- **Eraser button**: Click to enable eraser mode
- **'Exit Design' button**: Return to editor mode
- **Ctrl+S**: Save custom sprites to `sprites.json`
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
├── pixel_editor.py      # Pixel art editor for custom sprites
├── map_save.json        # Saved map data
├── sprites.json         # Custom sprite pixel data
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
