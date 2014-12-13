import pygame


class LightSource(object):
    LIGHT_SURF = None
    TILE_SIZE = None
    RADIUS = None
    COLOR = (50, 50, 50)

    def __init__(self, x_center, y_center, tile_size=TILE_SIZE):
        LightSource.TILE_SIZE = tile_size
        if LightSource.LIGHT_SURF is None:
            self.init_light_surf()
        self.rect = LightSource.LIGHT_SURF.get_rect()
        self.rect.topleft = (x_center,
                             y_center)

    def init_light_surf(self):
        surf_size = LightSource.TILE_SIZE * 3
        surf_size = LightSource.TILE_SIZE * 3
        LightSource.RADIUS = surf_size / 2
        LightSource.LIGHT_SURF = pygame.Surface((surf_size, surf_size),
                                         pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.circle(
            LightSource.LIGHT_SURF, LightSource.COLOR,
            (LightSource.RADIUS, LightSource.RADIUS),
            LightSource.RADIUS)

    def move(self, x_delta, y_delta):
        self.rect.x += x_delta
        self.rect.y += y_delta

    def render(self, surface):
        surface.blit(LightSource.LIGHT_SURF, self.rect,
                     special_flags=pygame.BLEND_ADD)
