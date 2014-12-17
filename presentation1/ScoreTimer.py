import pygame

class ScoreTimer():

    def __init__(self):

        self.total_time = 90000
        self.font = pygame.font.SysFont(None, 64)
        self.offset = pygame.time.get_ticks()

    def render(self, Globals):
        COLOR = pygame.Color("white")
        time_string = pygame.time.get_ticks() - self.offset
        Globals.REMAINING_TIME = self.total_time - time_string
        time_surf = self.font.render(str(Globals.REMAINING_TIME)[:2], True, COLOR)
        if Globals.REMAINING_TIME < self.total_time / 4:
            COLOR = pygame.Color("red")
        time_rect = time_surf.get_rect()
        time_rect.topright = Globals.SCREEN.get_rect().topright
        time_rect.width = Globals.WIDTH/4
        Globals.SCREEN.blit(time_surf, time_rect)
 
    def update(self):
        pass
