import pygame

from GameState import GameState
from Globals import Globals
from Player import Player
from BorderPlayer import BorderPlayer


class Highscore(GameState):

    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")
        self.time = 0.0
        self.playerSprites = pygame.sprite.Group()
        self.playerSprites.add(BorderPlayer(
            Globals.WIDTH, Globals.HEIGHT, 0, 0, Player.INDEX_DOWN))
        self.playerSprites.add(BorderPlayer(
            Globals.WIDTH, Globals.HEIGHT,
            Globals.WIDTH, 0, Player.INDEX_LEFT))
        self.playerSprites.add(BorderPlayer(
            Globals.WIDTH, Globals.HEIGHT, 0,
            Globals.HEIGHT, Player.INDEX_RIGHT))
        self.playerSprites.add(BorderPlayer(
            Globals.WIDTH, Globals.HEIGHT,
            Globals.WIDTH, Globals.HEIGHT, Player.INDEX_UP))

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        font = pygame.font.SysFont("hannotatesc", 64)
        # font.
        TITLE_PADDING = 75
        VERT_SPACING = 75

        COLOR = (7, 147, 240)

        title_surf = font.render("Highscores", True, (0, 0, 0))
        title_rect = title_surf.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx - 120
        title_rect.centery = Globals.SCREEN.get_rect().centery
        title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(title_surf, title_rect)

        op1 = font.render("Mlbvsnba - 521 pts", True, COLOR)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op1, title_rect)

        op2 = font.render("Gogoprincess - 448 pts", True, COLOR)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op2, title_rect)

        op3 = font.render("Tutu451 - 334 pts", True, COLOR)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op3, title_rect)

        op4 = font.render("phf - 3 pts", True, COLOR)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op4, title_rect)

        self.playerSprites.draw(Globals.SCREEN)
        for p in self.playerSprites:
            p.onDraw()

        pygame.display.flip()

    def update(self, time):
        self.time += time
        self.playerSprites.update(time)

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Globals.STATE = Menu()

