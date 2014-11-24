import pygame
from Globals import Globals


class ScoreTimer():
    SCREEN_OFFSET = 10
    COLOR = pygame.Color("white")
    TEXT_SIZE = 50

    def __init__(self):
        self.total_time = 0
        self.font = pygame.font.SysFont(None, ScoreTimer.TEXT_SIZE)
        self.offset = pygame.time.get_ticks()
        self.paused = False

    def pause(self):
        if self.paused:
            return
        self.pause_time = pygame.time.get_ticks()
        self.paused = True

    def unpause(self):
        if not self.paused:
            return
        self.paused = False
        self.offset += pygame.time.get_ticks() - self.pause_time

    def render(self, screen):
        self.total_time = pygame.time.get_ticks() - self.offset
        time_surf = self.font.render(
            str(self.total_time / 1000),
            True,
            ScoreTimer.COLOR
        )
        time_rect = time_surf.get_rect()
        time_rect.top = ScoreTimer.SCREEN_OFFSET
        time_rect.right = Globals.WIDTH - ScoreTimer.SCREEN_OFFSET
        screen.blit(time_surf, time_rect)

    def update(self):
        pass
