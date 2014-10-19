import pygame

class HealthBar():

    def __init__(self):
        self.color = pygame.color.Color("cyan")
        # self.Globals = Globals
        # print Globals.SCREEN

    def render(self, Globals):
        #Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        font = pygame.font.SysFont("hannotatesc", 64)
        COLOR = pygame.color("green")
        health_string = Globals.PLAYER_HEALTH
        if (Globals.PLAYER_HEALTH < 50):
            COLOR = pygame.Color("yellow")
        if (Globals.PLAYER_HEALTH < 25):
            COLOR = pygame.color("red")
        health_surf = font.render(health_string, True, COLOR)
        health_rect = health_surf.get_rect()
        health_rect.topleft = Globals.SCREEN.get_rect().topleft
        health_rect.width = Globals.WIDTH/3
        #health_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(health_surf, health_rect)
 

        pygame.display.flip()

    def update(self):
    	pass

