import pygame
import sys

from GameState import GameState
from Globals import Globals
from Player import Player
from BorderPlayer import BorderPlayer
from TileTest import TileTest

MENU_BACKGROUND = pygame.image.load("images/menu_background.png")


class Menu(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")
        self.time = 0
        self.selection = 0
        self.playerSprites = pygame.sprite.Group()
        self.playerSprites.add(
            BorderPlayer(Globals.WIDTH, Globals.HEIGHT,
                         0, 0, Player.INDEX_DOWN))
        self.playerSprites.add(
            BorderPlayer(Globals.WIDTH, Globals.HEIGHT,
                         Globals.WIDTH, 0, Player.INDEX_LEFT))
        self.playerSprites.add(
            BorderPlayer(Globals.WIDTH, Globals.HEIGHT,
                         0, Globals.HEIGHT, Player.INDEX_RIGHT))
        self.playerSprites.add(
            BorderPlayer(Globals.WIDTH, Globals.HEIGHT,
                         Globals.WIDTH, Globals.HEIGHT, Player.INDEX_UP))

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        Globals.SCREEN.blit(MENU_BACKGROUND, [0, 0])
        font = pygame.font.SysFont("hannotatesc", 64)
        # font.
        TITLE_PADDING = 75
        VERT_SPACING = 75

        START = "Start Game"
        VOLUME = "Volume Control"
        BRIGHTNESS = "Brightness"
        SCORE = "Highscores"
        QUIT = "Quit"

        COLOR = (7, 147, 240)
        SELECT_COLOR = (11, 81, 128)

        GAME_SELECT = COLOR
        BRIGHT_SELECT = COLOR
        AUDIO_SELECT = COLOR
        SCORE_SELECT = COLOR
        QUIT_SELECT = COLOR

        if (self.selection is 0):
            GAME_SELECT = SELECT_COLOR
        elif (self.selection is 1):
            BRIGHT_SELECT = SELECT_COLOR
        elif (self.selection is 2):
            AUDIO_SELECT = SELECT_COLOR
        elif (self.selection is 3):
            SCORE_SELECT = SELECT_COLOR
        elif (self.selection is 4):
            QUIT_SELECT = SELECT_COLOR

        title_surf = font.render(START, True, GAME_SELECT)
        title_rect = title_surf.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx - 20
        title_rect.centery = Globals.SCREEN.get_rect().centery
        title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(title_surf, title_rect)

        op1 = font.render(BRIGHTNESS, True, BRIGHT_SELECT)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op1, title_rect)

        op2 = font.render(VOLUME, True, AUDIO_SELECT)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op2, title_rect)

        op3 = font.render(SCORE, True, SCORE_SELECT)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op3, title_rect)

        op4 = font.render(QUIT, True, QUIT_SELECT)
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
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if self.selection != 0:
                self.selection -= 1
                self.updateSelection()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if self.selection != 4:
                self.selection += 1
                self.updateSelection()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.selection == 0:
                # Globals.STATE = MainGame()
                Globals.STATE = TileTest()
            if self.selection == 3:
                Globals.STATE = Highscore()
                pass
            if self.selection == 4:
                sys.exit()

    def updateSelection(self):
        pygame.display.flip()


from MainGame import MainGame
from Highscore import Highscore
