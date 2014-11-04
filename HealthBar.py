import pygame


class HealthBar():

    def __init__(self):
        self.color = pygame.color.Color("cyan")
        self.health = 100

    def render(self, screen):
        # Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        font = pygame.font.SysFont(None, 64)
        COLOR = pygame.Color("green")
        if self.health < .75:
            COLOR = pygame.Color("yellow")
        elif self.health <.5:
            COLOR = pygame.Color("orange")
        else:
            COLOR = pygame.Color("red")
        health_surf = font.render("HP: " + str(self.health), True, COLOR)
        health_rect = health_surf.get_rect()
        health_rect.topleft = screen.get_rect().topleft
        health_rect.width = screen.get_rect().width / 3
        screen.blit(health_surf, health_rect)

    def changeHealth(delta):
        self.health += delta

    def printHealth(self):
        print self.health
        
    def update(self):
        pass
