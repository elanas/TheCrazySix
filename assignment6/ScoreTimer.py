import pygame

class ScoreTimer():

    def __init__(self):
        self.timer = 60

        self.total_time = 60
        self.time_start = pygame.time.get_ticks()

    def render(self, Globals):
        #Globals.SCREEN.fill(Globals.BACKGROUND_COLOR)
        font = pygame.font.SysFont("hannotatesc", 64)
        COLOR = pygame.Color("white")
        time_string = pygame.time.get_ticks()
        if (Globals.PLAYER_HEALTH < self.total_time/4):
            COLOR = pygame.Color("red")
        time_surf = font.render("Time: " + str(time_string), True, COLOR)
        time_rect = time_surf.get_rect()
        time_rect.topleft = Globals.SCREEN.get_rect().topright
        time_rect.width = Globals.WIDTH/3
        #health_rect.top = Globals.SCREEN.get_rect().top + TITLE_PADDING
        Globals.SCREEN.blit(health_surf, health_rect)
 

        pygame.display.flip()

    def update(self):
    	pass
