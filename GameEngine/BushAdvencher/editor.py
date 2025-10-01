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
        """카메라를 타겟 중심으로 업데이트"""
        self.x = target_x - view_width // 2
        self.y = target_y - view_height // 2
        
        # 맵 경계 클램핑
        self.x = max(0, min(self.x, map_width - view_width))
        self.y = max(0, min(self.y, map_height - view_height))

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
        
        # 드래그 중인 아이템
        self.dragging_item: Optional[ItemType] = None
        self.drag_start_pos: Optional[Tuple[int, int]] = None
        
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
                if event.button == 1:  # 좌클릭
                    self.handle_mouse_down(event.pos)
                elif event.button == 3:  # 우클릭 (타일 제거)
                    self.handle_right_click(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.handle_mouse_up(event.pos)
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_item:
                    pass  # 드래그 중 처리는 render에서
    
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
        
        # 아이템 패널 클릭
        elif x < self.item_panel_width:
            self.handle_item_panel_click(x, y)
        
        # 뷰 패널 클릭 (에디트 모드만)
        elif self.mode == EditorMode.EDIT:
            self.drag_start_pos = pos
    
    def handle_item_panel_click(self, x: int, y: int):
        """아이템 패널 클릭 처리"""
        if self.mode != EditorMode.EDIT:
            return
        
        # 각 아이템은 60px 높이
        item_y = y - self.toolbar_height - self.item_scroll_offset
        item_index = item_y // 60
        
        items = list(ITEM_REGISTRY.keys())
        if 0 <= item_index < len(items):
            self.dragging_item = items[item_index]
            self.drag_start_pos = (x, y)
    
    def handle_mouse_up(self, pos: Tuple[int, int]):
        """마우스 업 처리"""
        if self.dragging_item and self.mode == EditorMode.EDIT:
            # 뷰 패널에 드롭했는지 확인
            x, y = pos
            if x >= self.view_panel_x and y >= self.view_panel_y:
                self.place_item_at_mouse(pos)
        
        self.dragging_item = None
        self.drag_start_pos = None
    
    def handle_right_click(self, pos: Tuple[int, int]):
        """우클릭으로 타일 제거"""
        if self.mode != EditorMode.EDIT:
            return
        
        x, y = pos
        if x >= self.view_panel_x and y >= self.view_panel_y:
            # 뷰 좌표를 타일 좌표로 변환
            view_x = x - self.view_panel_x + self.camera.x
            view_y = y - self.view_panel_y + self.camera.y
            tile_x = view_x // self.game_map.tile_size
            tile_y = view_y // self.game_map.tile_size
            
            self.game_map.set_tile(tile_x, tile_y, None)
    
    def place_item_at_mouse(self, pos: Tuple[int, int]):
        """마우스 위치에 아이템 배치"""
        x, y = pos
        
        # 뷰 좌표를 타일 좌표로 변환
        view_x = x - self.view_panel_x + self.camera.x
        view_y = y - self.view_panel_y + self.camera.y
        tile_x = view_x // self.game_map.tile_size
        tile_y = view_y // self.game_map.tile_size
        
        self.game_map.set_tile(tile_x, tile_y, self.dragging_item)
    
    def toggle_play_mode(self):
        """플레이 모드 토글"""
        if self.mode == EditorMode.EDIT:
            self.switch_to_play_mode()
        else:
            self.switch_to_edit_mode()
    
    def switch_to_play_mode(self):
        """플레이 모드로 전환"""
        if not self.game_map.player_start:
            print("플레이어 시작 지점이 설정되지 않았습니다!")
            return
        
        self.mode = EditorMode.PLAY
        start_x, start_y = self.game_map.player_start
        self.player = Player(start_x, start_y, self.game_map.tile_size)
    
    def switch_to_edit_mode(self):
        """에디트 모드로 전환"""
        self.mode = EditorMode.EDIT
        self.player = None
        self.camera.x = 0
        self.camera.y = 0
    
    def save_map(self):
        """맵 저장"""
        try:
            self.game_map.save_to_file("map_save.json")
            print("맵이 저장되었습니다: map_save.json")
        except Exception as e:
            print(f"맵 저장 실패: {e}")
    
    def load_map(self):
        """맵 불러오기"""
        try:
            self.game_map = GameMap.load_from_file("map_save.json")
            print("맵이 로드되었습니다: map_save.json")
        except FileNotFoundError:
            print("저장된 맵 파일이 없습니다.")
        except Exception as e:
            print(f"맵 로드 실패: {e}")
    
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
        
        # 드래그 중인 아이템 렌더링
        if self.dragging_item:
            self.render_dragging_item()
        
        pygame.display.flip()
    
    def render_toolbar(self):
        """툴바 렌더링"""
        # 배경
        pygame.draw.rect(self.screen, (60, 60, 60), 
                        (0, 0, self.screen_width, self.toolbar_height))
        
        # 플레이/정지 버튼
        button_color = (100, 200, 100) if self.mode == EditorMode.EDIT else (200, 100, 100)
        button_text = "▶ Play" if self.mode == EditorMode.EDIT else "■ Stop"
        pygame.draw.rect(self.screen, button_color, (10, 10, 100, 30))
        text = self.font.render(button_text, True, (255, 255, 255))
        self.screen.blit(text, (15, 15))
        
        # 저장 버튼
        pygame.draw.rect(self.screen, (100, 100, 200), (120, 10, 100, 30))
        save_text = self.font.render("Save", True, (255, 255, 255))
        self.screen.blit(save_text, (140, 15))
        
        # 불러오기 버튼
        pygame.draw.rect(self.screen, (100, 200, 200), (230, 10, 100, 30))
        load_text = self.font.render("Load", True, (255, 255, 255))
        self.screen.blit(load_text, (250, 15))
        
        # 모드 표시
        mode_text = f"Mode: {self.mode.upper()}"
        text = self.font.render(mode_text, True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width - 200, 15))
    
    def render_item_panel(self):
        """아이템 패널 렌더링"""
        # 배경
        pygame.draw.rect(self.screen, (50, 50, 50),
                        (0, self.toolbar_height, self.item_panel_width, 
                         self.screen_height - self.toolbar_height))
        
        # 제목
        title = self.font.render("Items", True, (255, 255, 255))
        self.screen.blit(title, (10, self.toolbar_height + 10))
        
        # 아이템 목록
        y_offset = self.toolbar_height + 40 + self.item_scroll_offset
        for item_type in ITEM_REGISTRY.keys():
            if y_offset > self.toolbar_height and y_offset < self.screen_height:
                self.render_item_in_panel(item_type, 10, y_offset)
            y_offset += 60
        
        # 구분선
        pygame.draw.line(self.screen, (100, 100, 100),
                        (self.item_panel_width, self.toolbar_height),
                        (self.item_panel_width, self.screen_height), 2)
    
    def render_item_in_panel(self, item_type: ItemType, x: int, y: int):
        """패널에 아이템 렌더링"""
        item_def = get_item_definition(item_type)
        
        # 아이템 박스
        pygame.draw.rect(self.screen, item_def.color, (x, y, 40, 40))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 40, 40), 2)
        
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
        
        # 플레이어 렌더링 (플레이 모드)
        if self.mode == EditorMode.PLAY and self.player:
            self.player.render(self.screen, self.camera.x, self.camera.y,
                             self.view_panel_x, self.view_panel_y)
    
    def render_grid(self):
        """그리드 라인 렌더링 (에디트 모드만)"""
        if self.mode != EditorMode.EDIT:
            return
        
        tile_size = self.game_map.tile_size
        
        # 수직선
        start_x = -(self.camera.x % tile_size)
        for x in range(start_x, self.view_panel_width, tile_size):
            screen_x = self.view_panel_x + x
            if self.view_panel_x <= screen_x <= self.view_panel_x + self.view_panel_width:
                pygame.draw.line(self.screen, (60, 60, 60),
                               (screen_x, self.view_panel_y),
                               (screen_x, self.view_panel_y + self.view_panel_height), 1)
        
        # 수평선
        start_y = -(self.camera.y % tile_size)
        for y in range(start_y, self.view_panel_height, tile_size):
            screen_y = self.view_panel_y + y
            if self.view_panel_y <= screen_y <= self.view_panel_y + self.view_panel_height:
                pygame.draw.line(self.screen, (60, 60, 60),
                               (self.view_panel_x, screen_y),
                               (self.view_panel_x + self.view_panel_width, screen_y), 1)
    
    def render_tiles(self):
        """배치된 타일 렌더링"""
        tile_size = self.game_map.tile_size
        
        # 보이는 타일 범위 계산
        start_tile_x = max(0, self.camera.x // tile_size)
        start_tile_y = max(0, self.camera.y // tile_size)
        end_tile_x = min(self.game_map.width, (self.camera.x + self.view_panel_width) // tile_size + 1)
        end_tile_y = min(self.game_map.height, (self.camera.y + self.view_panel_height) // tile_size + 1)
        
        for tile_x in range(start_tile_x, end_tile_x):
            for tile_y in range(start_tile_y, end_tile_y):
                tile = self.game_map.get_tile(tile_x, tile_y)
                if tile and tile.item_type:
                    # 타일의 화면상 위치 계산 (뷰 패널 좌표 기준)
                    screen_x = self.view_panel_x + (tile_x * tile_size) - self.camera.x
                    screen_y = self.view_panel_y + (tile_y * tile_size) - self.camera.y
                    
                    item_def = get_item_definition(tile.item_type)
                    pygame.draw.rect(self.screen, item_def.color,
                                   (screen_x, screen_y, tile_size, tile_size))
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                   (screen_x, screen_y, tile_size, tile_size), 1)
    
    def render_dragging_item(self):
        """드래그 중인 아이템 렌더링"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # 뷰 패널 위에 있을 때만 스냅 프리뷰
        if mouse_x >= self.view_panel_x and mouse_y >= self.view_panel_y:
            view_x = mouse_x - self.view_panel_x + self.camera.x
            view_y = mouse_y - self.view_panel_y + self.camera.y
            tile_x = view_x // self.game_map.tile_size
            tile_y = view_y // self.game_map.tile_size
            
            screen_x = self.view_panel_x + tile_x * self.game_map.tile_size - self.camera.x
            screen_y = self.view_panel_y + tile_y * self.game_map.tile_size - self.camera.y
            
            item_def = get_item_definition(self.dragging_item)
            color = list(item_def.color) + [128]  # 반투명
            
            # 반투명 사각형
            s = pygame.Surface((self.game_map.tile_size, self.game_map.tile_size))
            s.set_alpha(128)
            s.fill(item_def.color)
            self.screen.blit(s, (screen_x, screen_y))
            
            pygame.draw.rect(self.screen, (255, 255, 255),
                           (screen_x, screen_y, self.game_map.tile_size, self.game_map.tile_size), 2)
        else:
            # 마우스 커서 따라다니기
            item_def = get_item_definition(self.dragging_item)
            pygame.draw.rect(self.screen, item_def.color,
                           (mouse_x - 20, mouse_y - 20, 40, 40))
            pygame.draw.rect(self.screen, (255, 255, 255),
                           (mouse_x - 20, mouse_y - 20, 40, 40), 2)
    
    def run(self):
        """메인 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
