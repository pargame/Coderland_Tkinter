"""
BushAdvencher Map Editor
메인 실행 파일
"""
from editor import MapEditor

if __name__ == "__main__":
    print("=" * 50)
    print("BushAdvencher Map Editor")
    print("=" * 50)
    print("\nControls:")
    print("- [Default Mode]: Drag view to move map")
    print("- Left panel click: Select item (cursor changes)")
    print("- [Item Selected]: Click/drag in view to place continuously")
    print("- 'Drop Item' button: Return to default mode")
    print("- Right click (view): Remove tile")
    print("- Right click (item panel): Deselect item")
    print("- Play button or P: Toggle play mode")
    print("- Play mode: Arrow keys or WASD to move (hold)")
    print("- ESC: Exit play mode or quit program")
    print("- Ctrl+S: Save, Ctrl+O: Load")
    print("\nMap size: 50 x 50 tiles (32 pixels each)")
    print("\nItems:")
    print("- Player Start (red): Player spawn position (one per map, hidden in play)")
    print("- Bush (dark green): Walkable (future monster encounter)")
    print("- Stone (gray): Blocking")
    print("=" * 50)
    print()
    
    editor = MapEditor(1200, 800)
    editor.run()
