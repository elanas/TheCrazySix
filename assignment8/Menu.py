import pygame
import sys

from GameState import GameState
from Globals import Globals
from Character import Character
from BorderPlayer import BorderPlayer
from NameInput import NameInput
from Highscore import Highscore
import Title


BACKGROUND_IMG = pygame.image.load("images/background.png")


class Menu(GameState):
    # CIRCLE_COLOR = (247, 219, 59)
    # CIRCLE_COLOR = (175, 255, 143)
    CIRCLE_COLOR = pygame.color.Color("white")
    CIRCLE_PADDING = 30

    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")
        self.time = 0
        self.selection = 0

    def render(self):
        Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        Globals.SCREEN.blit(BACKGROUND_IMG, [0, 0])
        font = pygame.font.SysFont(None, 64)

        TITLE_PADDING = 160
        VERT_SPACING = 65
        HOR_SPACING = 0

        START = "Start Game"
        VOLUME = "Volume Control"
        BRIGHTNESS = "Brightness"
        SCORE = "Highscores"
        QUIT = "Quit"

        COLOR = (240, 250, 190)
        SELECT_COLOR = Menu.CIRCLE_COLOR

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
        title_rect.centerx = Globals.SCREEN.get_rect().centerx + HOR_SPACING
        title_rect.centery = Globals.SCREEN.get_rect().centery
        title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(title_surf, title_rect)

        if self.selection is 0:
            self.draw_circle(title_rect)
        op1 = font.render(BRIGHTNESS, True, BRIGHT_SELECT)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op1, title_rect)

        if self.selection is 1:
            self.draw_circle(title_rect)
        op2 = font.render(VOLUME, True, AUDIO_SELECT)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op2, title_rect)

        if self.selection is 2:
            self.draw_circle(title_rect)
        op3 = font.render(SCORE, True, SCORE_SELECT)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op3, title_rect)

        if self.selection is 3:
            self.draw_circle(title_rect)
        op4 = font.render(QUIT, True, QUIT_SELECT)
        title_rect.centery += VERT_SPACING
        Globals.SCREEN.blit(op4, title_rect)

        if self.selection is 4:
            self.draw_circle(title_rect)

        pygame.display.flip()

    def draw_circle(self, title_rect):
        pos = (title_rect.left - Menu.CIRCLE_PADDING, title_rect.centery)
        pygame.draw.circle(Globals.SCREEN, Menu.CIRCLE_COLOR, pos, 10)

    def update(self, time):
        self.time += time
        # self.playerSprites.update(time)

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
            Globals.STATE = Title.Title()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.selection == 0:
                # Globals.STATE = MainGame()
                Globals.STATE = NameInput()
            if self.selection == 3:
                Globals.STATE = Highscore()
                pass
            if self.selection == 4:
                sys.exit()

    def updateSelection(self):
        pygame.display.flip()
