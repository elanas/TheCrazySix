import pygame


class Border (pygame.sprite.Sprite):

    def __init__(self, w, h, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def update(self):
        pass
