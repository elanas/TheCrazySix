import pygame


class ScoreTimer():

    def __init__(self):

        self.total_time = 0
        self.font = pygame.font.SysFont(None, 64)
        self.offset = pygame.time.get_ticks()

    def render(self, screen):
        COLOR = pygame.Color("white")
        total_time = pygame.time.get_ticks() - self.offset
        time_surf = self.font.render(
            str(sel)[:2],
            True,
            COLOR
        )
        time_rect = time_surf.get_rect()
        time_rect.topright = screen.get_rect().topright
        time_rect.width = screen.get_rect().width / 4
        screen.blit(time_surf, time_rect)

    def update(self):
        pass
