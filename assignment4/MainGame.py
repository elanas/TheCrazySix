import pygame
from GameState import GameState
from Globals import Globals
from Player import Player
from Enemy import Enemy
from Wall import Wall


class MainGame(GameState):
    NUM_ENEMY = 13

    def __init__(self):
        self.enemySprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()
        self.wallSprites = pygame.sprite.Group()
        for x in range(MainGame.NUM_ENEMY):
            self.enemySprites.add(Enemy(Globals.WIDTH, Globals.HEIGHT))
        self.playerSprites.add(Player(Globals.WIDTH, Globals.HEIGHT,
                                      Globals.WIDTH / 2, Globals.HEIGHT / 2))
        # creates walls where we want them...
        self.wallSprites.add(Wall(200, 20, 100, 300))


    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        self.enemySprites.draw(Globals.SCREEN)
        self.playerSprites.draw(Globals.SCREEN)
        self.wallSprites.draw(Globals.SCREEN)

    def update(self, time):
        self.playerSprites.update(time)
        self.enemySprites.update(time)
        # for p in self.playerSprites:
        #     pygame.sprite.spritecollide(p, self.enemySprites, True)

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Globals.STATE = Menu()
        elif event.type == pygame.KEYDOWN:
            for p in self.playerSprites:
                p.keyPressed(event.key)
        elif event.type == pygame.KEYUP:
            for p in self.playerSprites:
                p.keyReleased(event.key)

from Menu import Menu
