import pygame


class HealthBar():
    width = 200
    height = 30
    base_color = (175,175,175)
    border_color = (255, 255, 255)
    normal_color = (0,255,240)
    HURT_COLOR = (255, 0, 0)
    GOOD_COLOR = (0, 255, 0)
    border_width = 3
    position = (20, 20)
    CHANGE_TIME = .3

    def __init__(self):
        self.color = pygame.color.Color("cyan")
        self.health = 100
        self.makeHealthBar()
        self.color_change = False
        self.time_change = 0

    def update(self, time):
        if self.color_change:
            self.time_change += time
            if self.time_change >= HealthBar.CHANGE_TIME:
                self.color_change = False
                self.time_change = 0
                self.health_surf.fill(HealthBar.normal_color)

    def render(self, screen):
        screen.blit(self.base_surf, self.base_rect)
        screen.blit(self.health_surf, self.health_rect, self.health_area)

    def changeHealth(self, delta):
        self.health += delta
        if self.health > 100:
            self.health = 100
        elif self.health < 0:
            self.health = 0
        self.health_area.width = int(self.max_width * (self.health / 100.0))
        if delta < 0:
            self.time_change = 0
            self.color_change = True
            self.health_surf.fill(HealthBar.HURT_COLOR)
        elif delta > 0:
            self.time_change = 0
            self.color_change = True
            self.health_surf.fill(HealthBar.GOOD_COLOR)

    def makeHealthBar(self):
        self.base_surf = pygame.Surface((HealthBar.width,HealthBar.height)).convert()
        self.base_surf.fill(HealthBar.base_color)
        self.base_rect = self.base_surf.get_rect()
        pygame.draw.rect(self.base_surf, HealthBar.border_color, self.base_rect, HealthBar.border_width)
        self.base_rect.topleft = HealthBar.position

        self.health_surf = pygame.Surface((HealthBar.width - 2*HealthBar.border_width, HealthBar.height - 2*HealthBar.border_width)).convert()
        self.health_rect = self.health_surf.get_rect()
        self.health_area = self.health_surf.get_rect()
        self.health_rect.topleft = self.base_rect.topleft
        self.health_rect.left += HealthBar.border_width
        self.health_rect.top += HealthBar.border_width
        self.max_width = self.health_rect.width
        self.health_surf.fill(HealthBar.normal_color)
