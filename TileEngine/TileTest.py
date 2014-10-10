from Globals import Globals
from GameState import GameState
from TileEngine import TileEngine
from Camera import Camera
import pygame

class TileTest(GameState):
    FACTOR = 10

    def __init__(self):
        self.tileEngine = TileEngine("test_def.txt", "test_map.txt", 1, 3)
        self.camera = Camera(self.tileEngine, pygame.Rect(0, 0, Globals.WIDTH, Globals.HEIGHT))
        self.keyCode = None
        self.testPoint = (Globals.WIDTH / 2, int(Globals.HEIGHT - self.camera.tileEngine.get_tile_rect().height * 3.5))
        self.object_radius = self.camera.tileEngine.get_tile_rect().height * 2

    def render(self):
        self.camera.render(Globals.SCREEN)
        self.drawSolid()
        self.drawSpecial()
        pygame.draw.circle(Globals.SCREEN, (255, 0, 0), self.testPoint, 5)

    def drawSolid(self):
        solid_tiles = self.camera.getSolidObjects(self.testPoint, self.object_radius)
        for tile in solid_tiles:
            pass

    def drawSpecial(self):
        pass

    def update(self, time):
        if self.keyCode is not None:
            if self.keyCode == pygame.K_UP:
                self.camera.move(0, -TileTest.FACTOR)
            elif self.keyCode == pygame.K_DOWN:
                self.camera.move(0, TileTest.FACTOR)
            elif self.keyCode == pygame.K_LEFT:
                self.camera.move(-TileTest.FACTOR, 0)
            elif self.keyCode == pygame.K_RIGHT:
                self.camera.move(TileTest.FACTOR, 0)

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