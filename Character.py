import pygame
from TileSystem.TileType import TileType


class Character (pygame.sprite.Sprite):
    INDEX_DOWN = 0
    INDEX_LEFT = 1
    INDEX_UP = 2
    INDEX_RIGHT = 3

    def __init__(self, w, h, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.direction = -1
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def update(self):
        pass

    # to be used in extending classes
    def move(self, xDelta, yDelta):
        self.rect.x += xDelta
        self.rect.y += yDelta

    def checkCollisions(self, camera, avoid_stairs=False):
        radius = max(self.rect.height, self.rect.width) * 2
        if not avoid_stairs:
            solid_tiles = camera.get_solid_tiles(self.rect.center, radius)
        else:
            solid_tiles = camera.get_solid_and_stair_tiles(self.rect.center, radius)
        solid_rects = [pair.rect for pair in solid_tiles]
        for i in self.rect.collidelistall(solid_rects):
            curr_rect = solid_rects[i]
            if self.direction == Character.INDEX_UP:
                self.rect.top = curr_rect.bottom
            elif self.direction == Character.INDEX_DOWN:
                self.rect.bottom = curr_rect.top
            elif self.direction == Character.INDEX_LEFT:
                self.rect.left = curr_rect.right
            elif self.direction == Character.INDEX_RIGHT:
                self.rect.right = curr_rect.left

    def checkScreenCollisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity = 0
            self.playSound()
        elif self.rect.right > self.w:
            self.rect.right = self.w
            self.velocity = 0
            self.playSound()

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
            self.playSound()
        elif self.rect.bottom > self.h:
            self.rect.bottom = self.h
            self.velocity = 0
            self.playSound()
