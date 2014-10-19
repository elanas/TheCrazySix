import pygame

class HealthBar():

    def __init__(self, Globals):
        self.color = pygame.color.Color("green")
        self.Globals = Globals

    def render(self):
        #Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        font = pygame.font.SysFont("hannotatesc", 64)
        COLOR = (7, 147, 240)

        health_surf = font.render("Health", True, (255, 255, 255))
        health_rect = health_surf.get_rect()
        health_rect.topleft = self.Globals.SCREEN.get_rect().topleft
        health_rect.width = self.Globals.WIDTH/3
        #health_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        self.Globals.SCREEN.blit(health_surf, health_rect)

 

        pygame.display.flip()

    def update(self):
    	pass

