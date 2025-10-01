"""
아이템 타입 정의
"""
from enum import Enum
from typing import Dict, Any

class ItemType(Enum):
    PLAYER_START = "player_start"
    BUSH = "bush"
    STONE = "stone"

class ItemDefinition:
    """아이템의 정의(타입, 색상, 충돌 가능 여부 등)"""
    def __init__(self, item_type: ItemType, name: str, color: tuple, walkable: bool, unique: bool = False):
        self.item_type = item_type
        self.name = name
        self.color = color  # RGB
        self.walkable = walkable  # 플레이어가 지나갈 수 있는지
        self.unique = unique  # 맵에 하나만 배치 가능한지
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.item_type.value,
            "name": self.name,
            "walkable": self.walkable,
            "unique": self.unique
        }

# 아이템 정의 레지스트리
ITEM_REGISTRY = {
    ItemType.PLAYER_START: ItemDefinition(
        ItemType.PLAYER_START,
        "Player Start",
        (255, 0, 0),  # 빨간색
        True,
        unique=True  # 맵에 하나만 배치 가능
    ),
    ItemType.BUSH: ItemDefinition(
        ItemType.BUSH,
        "Bush",
        (34, 139, 34),  # 어두운 녹색
        True  # 지나갈 수 있음
    ),
    ItemType.STONE: ItemDefinition(
        ItemType.STONE,
        "Stone",
        (128, 128, 128),  # 회색
        False  # 지나갈 수 없음
    )
}

def get_item_definition(item_type: ItemType) -> ItemDefinition:
    """아이템 타입으로 정의 가져오기"""
    return ITEM_REGISTRY[item_type]
