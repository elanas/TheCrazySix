import pygame

class ScoreTimer():

    def __init__(self):
        self.total_time = 60000
        # self.Globals = Globals
        # print Globals.SCREEN

    def render(self, Globals):
        #Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        font = pygame.font.SysFont("hannotatesc", 64)
        COLOR = pygame.Color("white")
        time_string = pygame.time.get_ticks()
        Globals.REMAINING_TIME = self.total_time - time_string
        if Globals.REMAINING_TIME < self.total_time/4:
            COLOR = pygame.Color("red")
        if Globals.REMAINING_TIME <= 0:
             Globals.REMAINING_TIME = 00
        if Globals.REMAINING_TIME < 10000:
            Globals.REMAINING_TIME = 0 + Globals.REMAINING_TIME
        time_surf = font.render(str(Globals.REMAINING_TIME)[:2], True, COLOR)
        time_rect = time_surf.get_rect()
        time_rect.topright = Globals.SCREEN.get_rect().topright
        time_rect.width = Globals.WIDTH/4
        Globals.SCREEN.blit(time_surf, time_rect)
 

        # pygame.display.flip()

    def update(self):
        pass
