import pygame

from GameState import GameState
from Globals import Globals
from Menu import Menu
from BorderPlayer import BorderPlayer
from Player import Player

GAME_TITLE = "Unnamed Game"
TITLE_COLOR = pygame.color.Color("black")
TITLE_PADDING = 100
BACKGROUND_COLOR = (255, 255, 255)

class Title(GameState):
    # FADEINTIME = 5.0
    # FADEOUTTIME = 0.2
    def __init__(self):
        GameState.__init__(self)
        self.time = 0.0
        self.playerSprites = pygame.sprite.Group()
        self.playerSprites.add(BorderPlayer(Globals.WIDTH, Globals.HEIGHT, 0, 0, Player.INDEX_DOWN))
        self.playerSprites.add(BorderPlayer(Globals.WIDTH, Globals.HEIGHT, Globals.WIDTH, 0, Player.INDEX_LEFT))
        self.playerSprites.add(BorderPlayer(Globals.WIDTH, Globals.HEIGHT, 0, Globals.HEIGHT, Player.INDEX_RIGHT))
        self.playerSprites.add(BorderPlayer(Globals.WIDTH, Globals.HEIGHT, Globals.WIDTH, Globals.HEIGHT, Player.INDEX_UP))
    
    def render(self):
    	Globals.SCREEN.fill(BACKGROUND_COLOR)
        font = pygame.font.Font(None, 64)
        title_surf = font.render(GAME_TITLE, True, TITLE_COLOR)
        title_rect = title_surf.get_rect()
        title_rect.centerx = Globals.SCREEN.get_rect().centerx
        title_rect.centery = Globals.SCREEN.get_rect().centery
        # title_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(title_surf, title_rect)
        self.playerSprites.draw(Globals.SCREEN)
        for p in self.playerSprites:
        	p.onDraw()
        pygame.display.flip()
 
    def update(self, time):
        self.time += time
        self.playerSprites.update(time)
    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Globals.RUNNING = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            Globals.STATE = Menu()
