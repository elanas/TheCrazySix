from Globals import Globals
from GameState import GameState
from TileEngine import TileEngine
from Camera import Camera
import pygame

from Player import Player
from Enemy import Enemy
# from Menu import Menu



class TileTest(GameState):
    FACTOR = 10
    INDEX_DOWN = 0
    INDEX_UP = 1
    INDEX_LEFT = 2
    INDEX_RIGHT = 3

    NUM_ENEMY = 13
    WALL_WIDTH = 50

    def __init__(self):
        self.tileEngine = TileEngine("test_def.txt", "test_map.txt", 1, 3)
        self.camera = Camera(self.tileEngine, pygame.Rect(
            0, 0, Globals.WIDTH, Globals.HEIGHT))
        self.keyCode = None
        self.testPoint = [Globals.WIDTH / 2, int(Globals.HEIGHT -
                          self.camera.tileEngine.get_tile_rect().height * 3.5)]
        self.object_radius = \
            self.camera.tileEngine.get_tile_rect().height * 1.5
        self.direction = -1
        self.has_collided = False
        self.enemySprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()
        
        # for x in range(MainGame.NUM_ENEMY):
        #     self.enemySprites.add(Enemy(Globals.WIDTH, Globals.HEIGHT))
        self.playerSprites.add(Player(Globals.WIDTH, Globals.HEIGHT,
                                      self.testPoint[0], self.testPoint[1]))

    def render(self):
        self.camera.render(Globals.SCREEN)
        self.checkCollisions()
        self.drawSpecial()
        # pygame.draw.circle(Globals.SCREEN, (255, 0, 0), self.testPoint, 6)

        # Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        # self.enemySprites.draw(Globals.SCREEN)
        self.playerSprites.draw(Globals.SCREEN)
        # self.wallSprites.draw(Globals.SCREEN)

    def checkCollisions(self):
        solid_tiles = \
            self.camera.get_solid_tiles(self.testPoint, self.object_radius)
        solid_rects = [pair.rect for pair in solid_tiles]
        # # curr_rect = \
        # #     pygame.Rect(self.testPoint[0] - 3, self.testPoint[1] - 3, 6, 6)
        # curr_rect = self.playerSprites.get
        # for i in curr_rect.collidelistall(solid_rects):

        for p in self.playerSprites:
            curr_rect = p.rect
            for i in curr_rect.collidelistall(solid_rects):

                wall_rect = solid_rects[i]
                if self.direction == TileTest.INDEX_UP:
                    curr_rect.top = wall_rect.bottom
                    self.has_collided = True
                elif self.direction == TileTest.INDEX_DOWN:
                    curr_rect.bottom = wall_rect.top
                    self.has_collided = True
                elif self.direction == TileTest.INDEX_LEFT:
                    curr_rect.left = wall_rect.right
                    self.has_collided = True
                elif self.direction == TileTest.INDEX_RIGHT:
                    curr_rect.right = wall_rect.left
                    self.has_collided = True
                else:
                    self.has_collided = False

        self.testPoint[1] = curr_rect.top + 3
        self.testPoint[0] = curr_rect.left + 3

    def drawSpecial(self):
        special_tiles = \
            self.camera.get_special_tiles(self.testPoint, self.object_radius)
        for tile in special_tiles:
            print tile.is_special
            pygame.draw.rect(Globals.SCREEN, (0, 251, 255), tile.rect)

    def update(self, time):
        if self.keyCode is not None:
            if self.keyCode == pygame.K_UP:
                self.direction = TileTest.INDEX_UP
                if self.has_collided:
                    self.camera.move(0, 0)
                else:
                    self.camera.move(0, -TileTest.FACTOR)
            elif self.keyCode == pygame.K_DOWN:
                self.direction = TileTest.INDEX_DOWN
                if self.has_collided:
                    self.camera.move(0, 0)
                else:
                    self.camera.move(0, TileTest.FACTOR)
            elif self.keyCode == pygame.K_LEFT:
                self.direction = TileTest.INDEX_LEFT
                if self.has_collided:
                    self.camera.move(0, 0)
                else:
                    self.camera.move(-TileTest.FACTOR, 0)
            elif self.keyCode == pygame.K_RIGHT:
                self.direction = TileTest.INDEX_RIGHT
                if self.has_collided:
                    self.camera.move(0, 0)
                else:
                    self.camera.move(TileTest.FACTOR, 0)
        self.playerSprites.update(time)
        self.has_collided = False
        # self.enemySprites.update(time)

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


        if event.type == pygame.KEYDOWN:
            for p in self.playerSprites:
                p.keyPressed(event.key)
        if event.type == pygame.KEYUP:
            for p in self.playerSprites:
                p.keyReleased(event.key)

    def reloadCamera(self):
        try:
            self.tileEngine = TileEngine("test_def.txt", "test_map.txt", 1, 3)
            self.camera.tileEngine = self.tileEngine
            print "Reloaded Tile Engine"
        except Exception as e:
            print "Reload failed: ", e


