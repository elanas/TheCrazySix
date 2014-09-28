import pygame
from GameState import GameState
from Globals import Globals
from Player import Player
from Enemy import Enemy
from Game import Title


class MainGame(GameState):
    NUM_ENEMY = 13
    BACKGROUND_COLOR = (255, 255, 255)

    def __init__(self):
        self.enemySprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()
        for x in range(MainGame.NUM_ENEMY):
            self.enemySprites.add(Enemy(Globals.WIDTH, Globals.HEIGHT))
        self.playerSprites.add(Player(Globals.WIDTH, Globals.HEIGHT, Globals.WIDTH / 2, Globals.HEIGHT / 2))

    def render(self):
        Globals.SCREEN.fill(MainGame.BACKGROUND_COLOR)
        self.enemySprites.draw(Globals.SCREEN)
        self.playerSprites.draw(Globals.SCREEN)

    def update(self, time):
        self.playerSprites.update(time)
        self.enemySprites.update(time)

    def event(self, event):
        print "hello"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Globals.STATE = Highscore()
        elif event.type == pygame.KEYDOWN:
            for p in self.playerSprites:
                p.keyPressed(event.key)
        elif event.type == pygame.KEYUP:
            for p in self.playerSprites:
                p.keyReleased(event.key)


