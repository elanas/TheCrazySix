import pygame

class Character (pygame.sprite.Sprite):

    def __init__(self, w, h, x, y):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def update(self):
        pass

    # to be used in extending classes
    def move(self, xDelta, yDelta):
        self.x += xDelta
        self.y += yDelta



    
