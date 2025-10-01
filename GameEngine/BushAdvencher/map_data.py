"""
맵 데이터 구조 및 저장/불러오기
"""
import json
from typing import List, Dict, Any, Optional, Tuple
from item_types import ItemType

class MapTile:
    """맵의 한 타일"""
    def __init__(self, x: int, y: int, item_type: Optional[ItemType] = None):
        self.x = x
        self.y = y
        self.item_type = item_type
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "item_type": self.item_type.value if self.item_type else None
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'MapTile':
        item_type = ItemType(data["item_type"]) if data["item_type"] else None
        return MapTile(data["x"], data["y"], item_type)

class GameMap:
    """게임 맵 데이터"""
    def __init__(self, width: int, height: int, tile_size: int = 32):
        self.width = width  # 타일 개수
        self.height = height
        self.tile_size = tile_size  # 픽셀 단위
        self.tiles: Dict[Tuple[int, int], MapTile] = {}
        self.player_start: Optional[Tuple[int, int]] = None
    
    def set_tile(self, x: int, y: int, item_type: Optional[ItemType]) -> bool:
        """타일에 아이템 배치"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        # 플레이어 스타트는 하나만 배치 가능
        if item_type == ItemType.PLAYER_START:
            # 기존 플레이어 스타트 제거
            if self.player_start:
                old_x, old_y = self.player_start
                if (old_x, old_y) in self.tiles:
                    del self.tiles[(old_x, old_y)]
            self.player_start = (x, y)
        
        if item_type is None:
            # 타일 제거
            if (x, y) in self.tiles:
                # 플레이어 스타트였다면 초기화
                if self.tiles[(x, y)].item_type == ItemType.PLAYER_START:
                    self.player_start = None
                del self.tiles[(x, y)]
        else:
            self.tiles[(x, y)] = MapTile(x, y, item_type)
        
        return True
    
    def get_tile(self, x: int, y: int) -> Optional[MapTile]:
        """타일 가져오기"""
        return self.tiles.get((x, y))
    
    def is_walkable(self, x: int, y: int) -> bool:
        """해당 위치로 이동 가능한지 확인"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        tile = self.get_tile(x, y)
        if tile is None:
            return True  # 빈 타일은 이동 가능
        
        from item_types import get_item_definition
        item_def = get_item_definition(tile.item_type)
        return item_def.walkable
    
    def to_dict(self) -> Dict[str, Any]:
        """맵을 딕셔너리로 변환 (저장용)"""
        return {
            "width": self.width,
            "height": self.height,
            "tile_size": self.tile_size,
            "tiles": [tile.to_dict() for tile in self.tiles.values()],
            "player_start": list(self.player_start) if self.player_start else None
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GameMap':
        """딕셔너리에서 맵 로드"""
        game_map = GameMap(data["width"], data["height"], data["tile_size"])
        for tile_data in data["tiles"]:
            tile = MapTile.from_dict(tile_data)
            game_map.tiles[(tile.x, tile.y)] = tile
        
        if data.get("player_start"):
            game_map.player_start = tuple(data["player_start"])
        
        return game_map
    
    def save_to_file(self, filepath: str):
        """맵을 JSON 파일로 저장"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_from_file(filepath: str) -> 'GameMap':
        """JSON 파일에서 맵 로드"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return GameMap.from_dict(data)
