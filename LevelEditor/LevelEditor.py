import pygame
from GameState import GameState
from Globals import Globals
from TileEngine import TileEngine
from TileType import TileType
from Camera import Camera
from asset_loader import AssetLoader
from os.path import join

class LevelEditor(GameState):
    PADDING = 20
    RIGHT_PADDING = 120
    HIGHLIGHT_COLOR = (255, 0, 255)
    HIGHLIGHT_ALPHA = 100

    def __init__(self, definition_path, map_path):
        loader = AssetLoader(join("images", "tiles"))
        self.base_image = loader.load_image("transparent.png")
        self.base_rect = self.base_image.get_rect()
        self.definition_path = definition_path
        self.map_path = map_path
        self.tile_engine = TileEngine(self.definition_path, self.map_path)
        self.tile_rect = self.tile_engine.get_tile_rect()
        self.shift_factor = self.tile_rect.width
        self.camera_dest = pygame.Rect(LevelEditor.PADDING, 0, Globals.WIDTH - LevelEditor.RIGHT_PADDING - LevelEditor.PADDING, Globals.HEIGHT)# - LevelEditor.PADDING * 2)
        self.camera = Camera(self.tile_engine, self.camera_dest)
        extra_y = self.camera_dest.height % self.tile_rect.height
        extra_x = self.camera_dest.width % self.tile_rect.width
        if extra_y > 0:
            self.camera_dest.height -= extra_y
        if extra_x > 0:
            self.camera_dest.width -= extra_x
        self.camera_dest.centery = Globals.HEIGHT / 2
        self.key_code = None
        self.highlight_surf = pygame.Surface(self.tile_rect.size).convert()
        self.highlight_surf.fill(LevelEditor.HIGHLIGHT_COLOR)
        self.highlight_surf.set_alpha(LevelEditor.HIGHLIGHT_ALPHA)

    def render(self):
        self.clear_camera_surf()
        self.camera.render(Globals.SCREEN, False)
        self.handle_mouse()
    
    def clear_camera_surf(self):
        num_horiz = int(self.camera_dest.width / self.base_rect.width)
        num_vert = int(self.camera_dest.height / self.base_rect.height)
        for y in range(0, num_vert):
            y_coord = y * self.base_rect.height + self.camera_dest.top
            for x in range(0, num_horiz):
                x_coord = x * self.base_rect.width + self.camera_dest.left
                Globals.SCREEN.blit(self.base_image, (x_coord, y_coord))

    def update(self, time):
        if self.key_code is not None:
            if self.key_code == pygame.K_UP:
                self.camera.move(0, -self.shift_factor)
            elif self.key_code == pygame.K_DOWN:
                self.camera.move(0, self.shift_factor)
            elif self.key_code == pygame.K_LEFT:
                self.camera.move(-self.shift_factor, 0)
            elif self.key_code == pygame.K_RIGHT:
                self.camera.move(self.shift_factor, 0)

    def handle_mouse(self):
        pos = pygame.mouse.get_pos()
        if self.camera_dest.collidepoint(pos):
            temp = (pos[0] - self.camera_dest.left, pos[1] - self.camera_dest.top)
            rect = self.tile_rect.copy()
            x = pos[0] - temp[0] % self.tile_rect.width
            y = pos[1] - temp[1] % self.tile_rect.height
            rect.topleft = (x, y)
            Globals.SCREEN.blit(self.highlight_surf, rect)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Globals.RUNNING = False
            elif self.key_code is None:
                self.key_code = event.key
        if event.type == pygame.KEYUP:
            if event.key == self.key_code:
                self.key_code = None
