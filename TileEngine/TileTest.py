from Globals import Globals
from GameState import GameState
from TileEngine import TileEngine
from Camera import Camera
from math import ceil
import pygame


class TileTest(GameState):
    MAX_OFFSET_X = 150
    MAX_OFFSET_Y = 75
    FACTOR = 10
    INDEX_DOWN = 0
    INDEX_UP = 1
    INDEX_LEFT = 2
    INDEX_RIGHT = 3
    MINI_FACT = .1

    def __init__(self):
        self.tileEngine = TileEngine("test_def.txt", "test_map.txt", 1, 3)
        self.camera = Camera(self.tileEngine, pygame.Rect(
            0, 0, Globals.WIDTH, Globals.HEIGHT))
        rect = self.tileEngine.get_tile_rect()
        self.max_width = int(ceil(self.tileEngine.getMaxCols() * rect.width))
        self.max_height = int(ceil(self.tileEngine.getNumRows() * rect.height))
        self.mini_camera = Camera(self.tileEngine, pygame.Rect(0, 0, self.max_width, self.max_height))
        self.keyCode = None
        self.testPoint = [Globals.WIDTH / 2, int(Globals.HEIGHT -
                          self.camera.tileEngine.get_tile_rect().height * 3.5)]
        self.object_radius = \
            self.camera.tileEngine.get_tile_rect().height * 1.5
        self.direction = -1

    def render(self):
        self.camera.render(Globals.SCREEN)
        self.checkCollisions()
        self.drawSpecial()
        pygame.draw.circle(Globals.SCREEN, (255, 0, 0), self.testPoint, 6)
        mini_surf = pygame.Surface((self.max_width, self.max_height)).convert()
        mini_surf.set_colorkey(Camera.EMPTY_COLOR)
        self.mini_camera.render(mini_surf)
        scaled = pygame.transform.scale(mini_surf, (int(self.max_width * TileTest.MINI_FACT), int(self.max_height * TileTest.MINI_FACT)))
        Globals.SCREEN.blit(scaled, (2, 2))

    def checkCollisions(self):
        solid_tiles = \
            self.camera.get_solid_tiles(self.testPoint, self.object_radius)
        solid_rects = [pair.rect for pair in solid_tiles]
        curr_rect = \
            pygame.Rect(self.testPoint[0] - 3, self.testPoint[1] - 3, 6, 6)
        for i in curr_rect.collidelistall(solid_rects):
            wall_rect = solid_rects[i]
            if self.direction == TileTest.INDEX_UP:
                curr_rect.top = wall_rect.bottom
            elif self.direction == TileTest.INDEX_DOWN:
                curr_rect.bottom = wall_rect.top
            elif self.direction == TileTest.INDEX_LEFT:
                curr_rect.left = wall_rect.right
            elif self.direction == TileTest.INDEX_RIGHT:
                curr_rect.right = wall_rect.left

        self.testPoint[1] = curr_rect.top + 3
        self.testPoint[0] = curr_rect.left + 3
        self.checkCameraPosition()

    def checkCameraPosition(self):
        dist_x = self.camera.container.centerx - self.testPoint[0]
        dist_y = self.camera.container.centery - self.testPoint[1]
        if abs(dist_x) > TileTest.MAX_OFFSET_X:
            diff = abs(dist_x) - TileTest.MAX_OFFSET_X
            # player is to the right of center
            if dist_x < 0:
                pass
            # player is to the left of center
            else:
                diff *= -1
            self.camera.move(diff, 0)
            self.testPoint[0] -= diff
        if abs(dist_y) > TileTest.MAX_OFFSET_Y:
            diff = abs(dist_y) - TileTest.MAX_OFFSET_Y
            # player is below center
            if dist_y < 0:
                pass
            # player is above center
            else:
                diff *= -1
            self.camera.move(0, diff)
            self.testPoint[1] -= diff

    def drawSpecial(self):
        special_tiles = \
            self.camera.get_special_tiles(self.testPoint, self.object_radius)
        for tile in special_tiles:
            pygame.draw.rect(Globals.SCREEN, (0, 251, 255), tile.rect)

    def update(self, time):
        if self.keyCode is not None:
            if self.keyCode == pygame.K_UP:
                self.direction = TileTest.INDEX_UP
                # self.camera.move(0, -TileTest.FACTOR)
                self.testPoint[1] -= TileTest.FACTOR
            elif self.keyCode == pygame.K_DOWN:
                self.direction = TileTest.INDEX_DOWN
                # self.camera.move(0, TileTest.FACTOR)
                self.testPoint[1] += TileTest.FACTOR
            elif self.keyCode == pygame.K_LEFT:
                self.direction = TileTest.INDEX_LEFT
                # self.camera.move(-TileTest.FACTOR, 0)
                self.testPoint[0] -= TileTest.FACTOR
            elif self.keyCode == pygame.K_RIGHT:
                self.direction = TileTest.INDEX_RIGHT
                self.testPoint[0] += TileTest.FACTOR
                # self.camera.move(TileTest.FACTOR, 0)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Globals.RUNNING = False
            elif event.key == pygame.K_r or event.key == pygame.K_F5:
                self.reloadCamera()
            else:
                self.keyCode = event.key
        elif event.type == pygame.KEYUP and event.key == self.keyCode:
            self.keyCode = None

    def reloadCamera(self):
        try:
            self.tileEngine = TileEngine("test_def.txt", "test_map.txt", 1, 3)
            self.camera.tileEngine = self.tileEngine
            print "Reloaded Tile Engine"
        except Exception as e:
            print "Reload failed: ", e
