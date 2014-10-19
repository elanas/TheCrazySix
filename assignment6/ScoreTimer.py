import pygame

class ScoreTimer():

    def __init__(self):
        self.color = pygame.color.Color("cyan")
        # self.Globals = Globals
        # print Globals.SCREEN

    def render(self, Globals):
        #Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        font = pygame.font.SysFont("hannotatesc", 64)
        COLOR = pygame.Color("green")
        time_string = pygame.time.get_ticks()
        time_surf = font.render("Timer: " + str(time_string), True, COLOR)
        time_rect = time_surf.get_rect()
        time_rect.topright = Globals.SCREEN.get_rect().topright
        time_rect.width = Globals.WIDTH/3
        #health_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(time_surf, time_rect)
 

        pygame.display.flip()

    def update(self):
        pass
