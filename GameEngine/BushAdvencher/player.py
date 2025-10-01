"""
플레이어 클래스
"""
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from map_data import GameMap

class Player:
    """플레이어 엔티티"""
    def __init__(self, tile_x: int, tile_y: int, tile_size: int):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_size = tile_size
        self.color = (0, 0, 255)  # 파란색
        self.speed = 8  # 이동 속도 (픽셀/프레임)
        self.move_delay = 8  # 프레임마다 이동 (연속 이동용)
        self.move_timer = 0
        
        # 실제 픽셀 위치 (부드러운 이동용)
        self.pixel_x = float(tile_x * tile_size)
        self.pixel_y = float(tile_y * tile_size)
        
        # 목표 위치
        self.target_tile_x = tile_x
        self.target_tile_y = tile_y
        
        self.moving = False
    
    def try_move(self, dx: int, dy: int, game_map: 'GameMap'):
        """타일 단위로 이동 시도 (키 입력용)"""
        if self.moving:
            return  # 이동 중이면 새 이동 불가
        
        new_x = self.tile_x + dx
        new_y = self.tile_y + dy
        
        # 이동 가능한지 확인
        if game_map.is_walkable(new_x, new_y):
            self.target_tile_x = new_x
            self.target_tile_y = new_y
            self.moving = True
            self.move_timer = 0
    
    def update(self, keys_pressed, game_map: 'GameMap'):
        """부드러운 이동 업데이트 + 연속 키 입력 처리"""
        if self.moving:
            # 부드러운 이동 처리
            target_pixel_x = float(self.target_tile_x * self.tile_size)
            target_pixel_y = float(self.target_tile_y * self.tile_size)
            
            # X축 이동
            if self.pixel_x < target_pixel_x:
                self.pixel_x = min(self.pixel_x + self.speed, target_pixel_x)
            elif self.pixel_x > target_pixel_x:
                self.pixel_x = max(self.pixel_x - self.speed, target_pixel_x)
            
            # Y축 이동
            if self.pixel_y < target_pixel_y:
                self.pixel_y = min(self.pixel_y + self.speed, target_pixel_y)
            elif self.pixel_y > target_pixel_y:
                self.pixel_y = max(self.pixel_y - self.speed, target_pixel_y)
            
            # 목표 도달 확인
            if self.pixel_x == target_pixel_x and self.pixel_y == target_pixel_y:
                self.tile_x = self.target_tile_x
                self.tile_y = self.target_tile_y
                self.moving = False
        
        # 연속 키 입력 처리 (이동 중이 아닐 때만)
        if not self.moving:
            self.move_timer += 1
            if self.move_timer >= self.move_delay:
                dx, dy = 0, 0
                
                # 대각선 이동 규칙: 수평 우선
                if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                    dx = -1
                elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                    dx = 1
                elif keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
                    dy = -1
                elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                    dy = 1
                
                if dx != 0 or dy != 0:
                    self.try_move(dx, dy, game_map)
                    self.move_timer = 0
    
    def render(self, screen: pygame.Surface, camera_offset_x: int, camera_offset_y: int, 
               view_x: int, view_y: int):
        """플레이어 렌더링 (뷰 패널 좌표 기준)"""
        render_x = int(self.pixel_x - camera_offset_x + view_x)
        render_y = int(self.pixel_y - camera_offset_y + view_y)
        
        pygame.draw.rect(
            screen,
            self.color,
            (render_x, render_y, self.tile_size, self.tile_size)
        )
        
        # 테두리
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (render_x, render_y, self.tile_size, self.tile_size),
            2
        )
