from Globals import Globals
from GameState import GameState
from TileEngine import TileEngine
from Camera import Camera
import pygame

class TileTest(GameState):
    FACTOR = 10

    def __init__(self):
        self.tileEngine = TileEngine("test_def.txt", "test_map.txt", "tiles.png", 1, 3, 0.5)
        self.camera = Camera(self.tileEngine, pygame.Rect(0, 0, Globals.WIDTH, Globals.HEIGHT))
        self.keyCode = None

    def render(self):
        self.camera.render(Globals.SCREEN)

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
            self.keyCode = event.key
        elif event.type == pygame.KEYUP and event.key == self.keyCode:
            self.keyCode = None