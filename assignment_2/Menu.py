import pygame

from GameState import GameState
from Globals import Globals
from MainGame import MainGame
from Highscore import Highscore


class Menu(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.color = pygame.color.Color("black")
        self.time = 0
        Globals.SCREEN.fill(pygame.color.Color("black"))
        self.selection = 0
    
    def render(self):
        font = pygame.font.SysFont("hannotatesc", 64)
        # font.
        TITLE_PADDING = 50
        VERT_SPACING = 75

        START = "Start Game"
        VOLUME = "Volume Control"
        BRIGHTNESS = "Brightness"
        SCORE = "Highscores"
        QUIT = "Quit"

        RED = pygame.color.Color("red")
        WHITE = pygame.color.Color("white")
        
        GAME_SELECT = RED
        BRIGHT_SELECT = RED
        AUDIO_SELECT = RED
        SCORE_SELECT = RED
        QUIT_SELECT = RED 

        if(self.selection is 0):
            GAME_SELECT = WHITE
        elif(self.selection is 1):
            BRIGHT_SELECT = WHITE
        elif(self.selection is 2):
            AUDIO_SELECT = WHITE
        elif(self.selection is 3):
            SCORE_SELECT = WHITE
        elif(self.selection is 4):
            QUIT_SELECT = WHITE


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

        pygame.display.flip()

    def update(self, time):
        self.time += time

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
            	Globals.STATE = MainGame()
            if self.selection == 3:
                Globals.STATE = Highscore()
                pass
            if self.selection == 4:
            	sys.exit()
    def updateSelection(self):
        pygame.display.flip()