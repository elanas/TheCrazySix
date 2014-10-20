import pygame

from Globals import Globals
from GameState import GameState
from TileEngine import TileEngine
from TileType import TileType
from Camera import Camera
from HealthBar import HealthBar
from ScoreTimer import ScoreTimer

# from Highscore import Highscore
# importing Highscore isn't working for me

from Player import Player
from Enemy import Enemy


class TileTest(GameState):
    MAX_OFFSET_X = 150
    MAX_OFFSET_Y = 75
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
        self.testPoint = []
        self.object_radius = \
            self.camera.tileEngine.get_tile_rect().height * 1.5
        self.direction = -1
        self.has_collided = False
        self.enemySprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()
        self.health = HealthBar()
        self.score_timer = ScoreTimer()
        for x in range(TileTest.NUM_ENEMY):
            # fix the positions they are added in and everything else
            # should work
            self.enemySprites.add(Enemy(Globals.WIDTH, Globals.HEIGHT,
                                        self.camera))
        player_x = Globals.WIDTH / 2
        player_y = int(Globals.HEIGHT -
                       self.camera.tileEngine.get_tile_rect().height * 3.5)
        self.player = Player(Globals.WIDTH, Globals.HEIGHT, player_x, player_y)
        self.playerSprites.add(self.player)

    def render(self):
        self.camera.render(Globals.SCREEN)
        self.enemySprites.draw(Globals.SCREEN)
        self.playerSprites.draw(Globals.SCREEN)
        self.health.render(Globals)
        self.score_timer.render(Globals)

    def update(self, time):
        self.player.update(time, self.camera, self.enemySprites)
        self.enemySprites.update(time, self.camera)
        self.checkCameraPosition()
        if pygame.sprite.spritecollideany(self.player, self.enemySprites):
            Globals.PLAYER_HEALTH -= .5
        if ScoreTimer.remaining_time <= 0

    def checkCameraPosition(self):
        dist_x = self.camera.container.centerx - self.player.rect.centerx
        dist_y = self.camera.container.centery - self.player.rect.centery
        if abs(dist_x) > TileTest.MAX_OFFSET_X:
            diff = abs(dist_x) - TileTest.MAX_OFFSET_X
            # player is to the right of center
            if dist_x < 0:
                pass
            # player is to the left of center
            else:
                diff *= -1
            self.camera.move(diff, 0)
            self.player.rect.centerx -= diff
            for enemy in self.enemySprites:
                enemy.rect.centerx -= diff
        if abs(dist_y) > TileTest.MAX_OFFSET_Y:
            diff = abs(dist_y) - TileTest.MAX_OFFSET_Y
            # player is below center
            if dist_y < 0:
                pass
            # player is above center
            else:
                diff *= -1
            self.camera.move(0, diff)
            self.player.rect.centery -= diff
            for enemy in self.enemySprites:
                enemy.rect.centery -= diff

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
