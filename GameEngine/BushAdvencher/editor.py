"""
맵 에디터 메인 클래스
"""
import pygame
from typing import Optional, Tuple
from map_data import GameMap
from item_types import ItemType, get_item_definition, ITEM_REGISTRY
from player import Player

class Camera:
    """카메라 (뷰 오프셋)"""
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def update(self, target_x: int, target_y: int, map_width: int, map_height: int, 
               view_width: int, view_height: int):
        """Update camera following target (with edge margin)"""
        # Edge margin (30% of viewport)
        margin_x = view_width * 0.3
        margin_y = view_height * 0.3
        
        # Move camera if target exceeds margin
        if target_x < self.x + margin_x:
            self.x = target_x - margin_x
        elif target_x > self.x + view_width - margin_x:
            self.x = target_x - view_width + margin_x
        
        if target_y < self.y + margin_y:
            self.y = target_y - margin_y
        elif target_y > self.y + view_height - margin_y:
            self.y = target_y - view_height + margin_y
        
        # Clamp to map boundaries (handle case where map is smaller than view)
        max_x = max(0, map_width - view_width)
        max_y = max(0, map_height - view_height)
        self.x = int(max(0, min(self.x, max_x)))
        self.y = int(max(0, min(self.y, max_y)))

class EditorMode:
    EDIT = "edit"
    PLAY = "play"

class MapEditor:
    """맵 에디터"""
    def __init__(self, screen_width: int = 1200, screen_height: int = 800):
        pygame.init()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("BushAdvencher Map Editor")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.mode = EditorMode.EDIT
        
        # UI 레이아웃
        self.item_panel_width = 200
        self.toolbar_height = 50
        self.view_panel_x = self.item_panel_width
        self.view_panel_y = self.toolbar_height
        self.view_panel_width = screen_width - self.item_panel_width
        self.view_panel_height = screen_height - self.toolbar_height
        
        # 맵
        self.game_map = GameMap(50, 50, 32)
        
        # 선택된 아이템 (브러시 모드)
        self.selected_item: Optional[ItemType] = None
        
        # 뷰에서 드래그 중인지 여부
        self.is_painting = False
        self.is_erasing = False  # 우클릭 드래그로 지우기
        
        # 뷰 패널 드래그 (카메라 이동)
        self.is_dragging_view = False
        self.drag_start_camera_pos: Optional[Tuple[int, int]] = None
        self.drag_start_mouse_pos: Optional[Tuple[int, int]] = None
        
        # 카메라
        self.camera = Camera()
        
        # 플레이어 (플레이 모드용)
        self.player: Optional[Player] = None
        
        # 폰트
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # 아이템 패널 스크롤
        self.item_scroll_offset = 0
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.mode == EditorMode.PLAY:
                        self.switch_to_edit_mode()
                    else:
                        self.running = False
                
                elif event.key == pygame.K_p:
                    self.toggle_play_mode()
                
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.save_map()
                
                elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.load_map()
                
                # 플레이 모드는 update에서 연속 키 입력 처리
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_down(event.pos)
                elif event.button == 3:  # Right click
                    self.handle_right_mouse_down(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_painting = False
                    self.is_dragging_view = False
                    self.drag_start_camera_pos = None
                    self.drag_start_mouse_pos = None
                elif event.button == 3:
                    self.is_erasing = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.mode == EditorMode.EDIT:
                    # View drag (camera movement)
                    if self.is_dragging_view:
                        self.handle_view_drag(event.pos)
                    # Item painting
                    elif self.is_painting and self.selected_item:
                        self.paint_at_mouse(event.pos)
                    # Erasing tiles
                    elif self.is_erasing:
                        self.erase_at_mouse(event.pos)
    
    def handle_mouse_down(self, pos: Tuple[int, int]):
        """마우스 다운 처리"""
        x, y = pos
        
        # 툴바 클릭 (플레이 버튼)
        if y < self.toolbar_height:
            # 플레이 버튼 영역: 10~110
            if 10 <= x <= 110:
                self.toggle_play_mode()
            # 저장 버튼
            elif 120 <= x <= 220:
                self.save_map()
            # 불러오기 버튼
            elif 230 <= x <= 330:
                self.load_map()
        
        # 아이템 패널 클릭 (아이템 선택 또는 "놓기" 버튼)
        elif x < self.item_panel_width:
            self.handle_item_panel_click(x, y)
        
        # 뷰 패널 클릭 (에디트 모드만)
        elif self.mode == EditorMode.EDIT and x >= self.view_panel_x and y >= self.view_panel_y:
            if self.selected_item:
                # 아이템 선택 시 페인팅
                self.is_painting = True
                self.paint_at_mouse(pos)
            else:
                # 아이템 미선택 시 뷰 드래그 (카메라 이동)
                self.is_dragging_view = True
                self.drag_start_camera_pos = (self.camera.x, self.camera.y)
                self.drag_start_mouse_pos = pos
    
    def handle_item_panel_click(self, x: int, y: int):
        """Handle item panel click - select or drop item"""
        if self.mode != EditorMode.EDIT:
            return
        
        # Check "Drop" button area (above item list)
        drop_button_y = self.toolbar_height + 10
        drop_button_height = 30
        
        if drop_button_y <= y <= drop_button_y + drop_button_height:
            # Drop button clicked
            if self.selected_item:
                print("Item dropped")
            self.selected_item = None
            return
        
        # Item list area (each item is 60px height)
        item_list_start_y = drop_button_y + drop_button_height + 10
        item_y = y - item_list_start_y - self.item_scroll_offset
        
        if item_y >= 0:
            item_index = item_y // 60
            
            items = list(ITEM_REGISTRY.keys())
            if 0 <= item_index < len(items):
                self.selected_item = items[item_index]
                print(f"Selected item: {get_item_definition(self.selected_item).name}")
    
    def handle_right_mouse_down(self, pos: Tuple[int, int]):
        """Handle right mouse down - start erasing"""
        if self.mode != EditorMode.EDIT:
            return
        
        x, y = pos
        
        # Right click on view panel - start erasing
        if x >= self.view_panel_x and y >= self.view_panel_y:
            self.is_erasing = True
            self.erase_at_mouse(pos)
    
    def erase_at_mouse(self, pos: Tuple[int, int]):
        """Erase tile at mouse position (drag erasing)"""
        x, y = pos
        
        # Ignore if outside view panel
        if x < self.view_panel_x or y < self.view_panel_y:
            return
        
        # Convert view coordinates to tile coordinates
        view_x = x - self.view_panel_x + self.camera.x
        view_y = y - self.view_panel_y + self.camera.y
        tile_x = view_x // self.game_map.tile_size
        tile_y = view_y // self.game_map.tile_size
        
        self.game_map.set_tile(tile_x, tile_y, None)
    
    def paint_at_mouse(self, pos: Tuple[int, int]):
        """마우스 위치에 선택된 아이템 배치 (브러시)"""
        x, y = pos
        
        # 뷰 패널 밖이면 무시
        if x < self.view_panel_x or y < self.view_panel_y:
            return
        
        # 뷰 좌표를 타일 좌표로 변환
        view_x = x - self.view_panel_x + self.camera.x
        view_y = y - self.view_panel_y + self.camera.y
        tile_x = view_x // self.game_map.tile_size
        tile_y = view_y // self.game_map.tile_size
        
        self.game_map.set_tile(tile_x, tile_y, self.selected_item)
    
    def handle_view_drag(self, pos: Tuple[int, int]):
        """View drag for camera movement"""
        if not self.drag_start_mouse_pos or not self.drag_start_camera_pos:
            return
        
        # Calculate mouse movement
        dx = pos[0] - self.drag_start_mouse_pos[0]
        dy = pos[1] - self.drag_start_mouse_pos[1]
        
        # Move camera in opposite direction (map moves with drag)
        new_camera_x = self.drag_start_camera_pos[0] - dx
        new_camera_y = self.drag_start_camera_pos[1] - dy
        
        # Map boundaries with padding
        map_pixel_width = self.game_map.width * self.game_map.tile_size
        map_pixel_height = self.game_map.height * self.game_map.tile_size
        
        padding = 200  # Padding beyond map edge
        
        min_x = -padding
        min_y = -padding
        max_x = map_pixel_width - self.view_panel_width + padding
        max_y = map_pixel_height - self.view_panel_height + padding
        
        self.camera.x = max(min_x, min(new_camera_x, max_x))
        self.camera.y = max(min_y, min(new_camera_y, max_y))
    
    def toggle_play_mode(self):
        """플레이 모드 토글"""
        if self.mode == EditorMode.EDIT:
            self.switch_to_play_mode()
        else:
            self.switch_to_edit_mode()
    
    def switch_to_play_mode(self):
        """Switch to play mode"""
        if not self.game_map.player_start:
            print("Player start position not set!")
            return
        
        self.mode = EditorMode.PLAY
        start_x, start_y = self.game_map.player_start
        self.player = Player(start_x, start_y, self.game_map.tile_size)
    
    def switch_to_edit_mode(self):
        """Switch to edit mode"""
        self.mode = EditorMode.EDIT
        self.player = None
        self.camera.x = 0
        self.camera.y = 0
    
    def save_map(self):
        """Save map"""
        try:
            self.game_map.save_to_file("map_save.json")
            print("Map saved: map_save.json")
        except Exception as e:
            print(f"Failed to save map: {e}")
    
    def load_map(self):
        """Load map"""
        try:
            self.game_map = GameMap.load_from_file("map_save.json")
            print("Map loaded: map_save.json")
        except FileNotFoundError:
            print("No saved map file found.")
        except Exception as e:
            print(f"Failed to load map: {e}")
    
    def update(self):
        """게임 로직 업데이트"""
        if self.mode == EditorMode.PLAY and self.player:
            # 키 입력 상태 가져오기
            keys = pygame.key.get_pressed()
            self.player.update(keys, self.game_map)
            
            # 카메라를 플레이어 중심으로
            map_pixel_width = self.game_map.width * self.game_map.tile_size
            map_pixel_height = self.game_map.height * self.game_map.tile_size
            self.camera.update(
                int(self.player.pixel_x + self.game_map.tile_size // 2),
                int(self.player.pixel_y + self.game_map.tile_size // 2),
                map_pixel_width,
                map_pixel_height,
                self.view_panel_width,
                self.view_panel_height
            )
    
    def render(self):
        """화면 렌더링"""
        self.screen.fill((40, 40, 40))
        
        # 툴바 렌더링
        self.render_toolbar()
        
        # 아이템 패널 렌더링
        self.render_item_panel()
        
        # 뷰 패널 렌더링
        self.render_view_panel()
        
        # 선택된 아이템 커서 프리뷰
        self.render_cursor_preview()
        
        pygame.display.flip()
    
    def render_toolbar(self):
        """툴바 렌더링"""
        # 배경
        pygame.draw.rect(self.screen, (60, 60, 60), 
                        (0, 0, self.screen_width, self.toolbar_height))
        
        # Play/Stop button
        button_color = (100, 200, 100) if self.mode == EditorMode.EDIT else (200, 100, 100)
        button_text = "Play" if self.mode == EditorMode.EDIT else "Stop"
        pygame.draw.rect(self.screen, button_color, (10, 10, 100, 30))
        text = self.font.render(button_text, True, (255, 255, 255))
        self.screen.blit(text, (35, 15))
        
        # Save button
        pygame.draw.rect(self.screen, (100, 100, 200), (120, 10, 100, 30))
        save_text = self.font.render("Save", True, (255, 255, 255))
        self.screen.blit(save_text, (140, 15))
        
        # Load button
        pygame.draw.rect(self.screen, (100, 200, 200), (230, 10, 100, 30))
        load_text = self.font.render("Load", True, (255, 255, 255))
        self.screen.blit(load_text, (250, 15))
        
        # Player position display (play mode only)
        if self.mode == EditorMode.PLAY and self.player:
            pos_text = f"Player: ({self.player.tile_x}, {self.player.tile_y})"
            text = self.font.render(pos_text, True, (255, 255, 0))
            self.screen.blit(text, (self.screen_width - 400, 15))
        
        # Mode display
        mode_text = f"Mode: {self.mode.upper()}"
        text = self.font.render(mode_text, True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width - 200, 15))
    
    def render_item_panel(self):
        """Render item panel"""
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50),
                        (0, self.toolbar_height, self.item_panel_width, 
                         self.screen_height - self.toolbar_height))
        
        # "Drop" button
        drop_button_y = self.toolbar_height + 10
        drop_button_height = 30
        button_color = (80, 80, 80) if not self.selected_item else (150, 80, 80)
        
        pygame.draw.rect(self.screen, button_color,
                        (10, drop_button_y, self.item_panel_width - 20, drop_button_height))
        pygame.draw.rect(self.screen, (200, 200, 200),
                        (10, drop_button_y, self.item_panel_width - 20, drop_button_height), 2)
        
        drop_text = "Drop Item" if self.selected_item else "Default Mode"
        text_surface = self.small_font.render(drop_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.item_panel_width // 2, drop_button_y + 15))
        self.screen.blit(text_surface, text_rect)
        
        # Item list
        item_list_start_y = drop_button_y + drop_button_height + 10
        y_offset = item_list_start_y + self.item_scroll_offset
        
        for item_type in ITEM_REGISTRY.keys():
            if y_offset > self.toolbar_height and y_offset < self.screen_height:
                self.render_item_in_panel(item_type, 10, y_offset)
            y_offset += 60
        
        # Divider line
        pygame.draw.line(self.screen, (100, 100, 100),
                        (self.item_panel_width, self.toolbar_height),
                        (self.item_panel_width, self.screen_height), 2)
    
    def render_item_in_panel(self, item_type: ItemType, x: int, y: int):
        """패널에 아이템 렌더링"""
        item_def = get_item_definition(item_type)
        
        # 선택된 아이템이면 하이라이트
        is_selected = (self.selected_item == item_type)
        border_color = (255, 255, 0) if is_selected else (255, 255, 255)
        border_width = 3 if is_selected else 2
        
        # 아이템 박스
        pygame.draw.rect(self.screen, item_def.color, (x, y, 40, 40))
        pygame.draw.rect(self.screen, border_color, (x, y, 40, 40), border_width)
        
        # 이름
        name_text = self.small_font.render(item_def.name, True, (255, 255, 255))
        self.screen.blit(name_text, (x + 45, y + 5))
        
        # 속성
        props = []
        if item_def.walkable:
            props.append("Walkable")
        else:
            props.append("Blocking")
        if item_def.unique:
            props.append("Unique")
        
        prop_text = self.small_font.render(", ".join(props), True, (180, 180, 180))
        self.screen.blit(prop_text, (x + 45, y + 22))
    
    def render_view_panel(self):
        """뷰 패널 렌더링"""
        # 배경
        pygame.draw.rect(self.screen, (30, 30, 30),
                        (self.view_panel_x, self.view_panel_y,
                         self.view_panel_width, self.view_panel_height))
        
        # 그리드 렌더링
        self.render_grid()
        
        # 타일 렌더링
        self.render_tiles()
        
        # Render player (play mode)
        if self.mode == EditorMode.PLAY and self.player:
            # Clip to view panel
            clip_rect = pygame.Rect(self.view_panel_x, self.view_panel_y,
                                   self.view_panel_width, self.view_panel_height)
            self.screen.set_clip(clip_rect)
            
            self.player.render(self.screen, self.camera.x, self.camera.y,
                             self.view_panel_x, self.view_panel_y)
            
            self.screen.set_clip(None)
    
    def render_grid(self):
        """Render grid lines (only within map bounds)"""
        tile_size = self.game_map.tile_size
        map_pixel_width = self.game_map.width * tile_size
        map_pixel_height = self.game_map.height * tile_size
        
        # Calculate visible tile range
        start_tile_x = max(0, self.camera.x // tile_size)
        start_tile_y = max(0, self.camera.y // tile_size)
        end_tile_x = min(self.game_map.width, (self.camera.x + self.view_panel_width) // tile_size + 1)
        end_tile_y = min(self.game_map.height, (self.camera.y + self.view_panel_height) // tile_size + 1)
        
        # Vertical lines
        for tile_x in range(start_tile_x, end_tile_x + 1):
            world_x = tile_x * tile_size
            screen_x = self.view_panel_x + world_x - self.camera.x
            
            if self.view_panel_x <= screen_x <= self.view_panel_x + self.view_panel_width:
                pygame.draw.line(self.screen, (60, 60, 60),
                               (screen_x, self.view_panel_y),
                               (screen_x, self.view_panel_y + self.view_panel_height), 1)
        
        # Horizontal lines
        for tile_y in range(start_tile_y, end_tile_y + 1):
            world_y = tile_y * tile_size
            screen_y = self.view_panel_y + world_y - self.camera.y
            
            if self.view_panel_y <= screen_y <= self.view_panel_y + self.view_panel_height:
                pygame.draw.line(self.screen, (60, 60, 60),
                               (self.view_panel_x, screen_y),
                               (self.view_panel_x + self.view_panel_width, screen_y), 1)
    
    def render_tiles(self):
        """Render placed tiles (only within view panel bounds)"""
        tile_size = self.game_map.tile_size
        
        # Calculate visible tile range
        start_tile_x = max(0, self.camera.x // tile_size)
        start_tile_y = max(0, self.camera.y // tile_size)
        end_tile_x = min(self.game_map.width, (self.camera.x + self.view_panel_width) // tile_size + 1)
        end_tile_y = min(self.game_map.height, (self.camera.y + self.view_panel_height) // tile_size + 1)
        
        for tile_x in range(start_tile_x, end_tile_x):
            for tile_y in range(start_tile_y, end_tile_y):
                tile = self.game_map.get_tile(tile_x, tile_y)
                if tile and tile.item_type:
                    # Hide player start in play mode
                    if self.mode == EditorMode.PLAY and tile.item_type == ItemType.PLAYER_START:
                        continue
                    
                    # Calculate tile screen position
                    screen_x = self.view_panel_x + (tile_x * tile_size) - self.camera.x
                    screen_y = self.view_panel_y + (tile_y * tile_size) - self.camera.y
                    
                    # Only render if within view panel bounds
                    if (screen_x + tile_size > self.view_panel_x and 
                        screen_x < self.view_panel_x + self.view_panel_width and
                        screen_y + tile_size > self.view_panel_y and
                        screen_y < self.view_panel_y + self.view_panel_height):
                        
                        # Clip to view panel boundaries
                        clip_rect = pygame.Rect(self.view_panel_x, self.view_panel_y,
                                              self.view_panel_width, self.view_panel_height)
                        self.screen.set_clip(clip_rect)
                        
                        item_def = get_item_definition(tile.item_type)
                        pygame.draw.rect(self.screen, item_def.color,
                                       (screen_x, screen_y, tile_size, tile_size))
                        pygame.draw.rect(self.screen, (255, 255, 255),
                                       (screen_x, screen_y, tile_size, tile_size), 1)
                        
                        self.screen.set_clip(None)
    
    def render_cursor_preview(self):
        """Render selected item cursor preview"""
        if not self.selected_item or self.mode != EditorMode.EDIT:
            return
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Show snap preview when over view panel
        if mouse_x >= self.view_panel_x and mouse_y >= self.view_panel_y:
            view_x = mouse_x - self.view_panel_x + self.camera.x
            view_y = mouse_y - self.view_panel_y + self.camera.y
            tile_x = view_x // self.game_map.tile_size
            tile_y = view_y // self.game_map.tile_size
            
            screen_x = self.view_panel_x + tile_x * self.game_map.tile_size - self.camera.x
            screen_y = self.view_panel_y + tile_y * self.game_map.tile_size - self.camera.y
            
            item_def = get_item_definition(self.selected_item)
            
            # Semi-transparent rectangle
            s = pygame.Surface((self.game_map.tile_size, self.game_map.tile_size))
            s.set_alpha(128)
            s.fill(item_def.color)
            self.screen.blit(s, (screen_x, screen_y))
            
            pygame.draw.rect(self.screen, (255, 255, 0),
                           (screen_x, screen_y, self.game_map.tile_size, self.game_map.tile_size), 2)
        else:
            # Follow mouse cursor
            item_def = get_item_definition(self.selected_item)
            pygame.draw.rect(self.screen, item_def.color,
                           (mouse_x - 15, mouse_y - 15, 30, 30))
            pygame.draw.rect(self.screen, (255, 255, 0),
                           (mouse_x - 15, mouse_y - 15, 30, 30), 2)
    
    def run(self):
        """메인 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
