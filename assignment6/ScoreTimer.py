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
        health_surf = font.render("Time: ", True, COLOR)
        health_rect = health_surf.get_rect()
        health_rect.topright = Globals.SCREEN.get_rect().topright
        health_rect.width = Globals.WIDTH/3
        #health_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(health_surf, health_rect)
 

        pygame.display.flip()

    def update(self):
        pass
