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
        self.good_pos = None
        self.good_direction = None
        self.good_cam = None

    def update(self):
        pass

    # to be used in extending classes
    def move(self, xDelta, yDelta):
        self.rect.x += xDelta
        self.rect.y += yDelta

    def checkCollisions(self, camera, avoid_stairs=False, direct=None):
        if direct is None:
            direct = self.direction
        radius = max(self.rect.height, self.rect.width) * 2
        if not avoid_stairs:
            solid_tiles = camera.get_solid_tiles(self.rect.center, radius)
        else:
            solid_tiles = camera.get_solid_and_stair_tiles(self.rect.center, radius)
        if not avoid_stairs:
            walkable_tiles = camera.get_walkable_tiles(self.rect.center, radius,
                                                       avoid_stairs=avoid_stairs)
            walkable_rects = [pair.rect for pair in walkable_tiles]
            walkable_list = self.rect.collidelistall(walkable_rects)
        solid_rects = [pair.rect for pair in solid_tiles]
        collide_list = self.rect.collidelistall(solid_rects)
        collided = False
        for i in collide_list:
            collided = True
            curr_rect = solid_rects[i]
            if direct == Character.INDEX_UP:
                self.rect.top = curr_rect.bottom
            elif direct == Character.INDEX_DOWN:
                self.rect.bottom = curr_rect.top
            elif direct == Character.INDEX_LEFT:
                self.rect.left = curr_rect.right
            elif direct == Character.INDEX_RIGHT:
                self.rect.right = curr_rect.left
        if not avoid_stairs:
            if len(walkable_list) == 0:
                if self.good_pos:
                    camera.viewpoint.topleft = self.good_cam
                    camera.set_dirty()
                    self.rect.center = self.good_pos
                    self.direction = self.good_direction
            else:
                if len(collide_list) == 0:
                    self.good_pos = self.rect.center
                    self.good_cam = camera.viewpoint.topleft
                    self.good_direction = self.direction
        return collided

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
