import os
import pygame
import math
import random

from Character import Character
from asset_loader import AssetLoader
from Globals import Globals


class Enemy(Character):
    HEALTH_EFFECT = -1
    MOVE_VELOCITY = 75
    INDEX_DOWN = 0
    INDEX_LEFT = 1
    INDEX_UP = 2
    INDEX_RIGHT = 3
    images = [None, None, None, None]
    loader = AssetLoader("images")
    WALK_ANIM_TIME = .25

    def __init__(self, w=0, h=0, camera=None, x=None, y=None):
        super(Enemy, self).__init__(w, h, 0, 0)
        self.loadResources()
        self.direction = random.randint(0, 3)
        self.image = Enemy.images[self.direction][0]
        self.rect = self.image.get_rect()
        self.cycle = -1
        self.time_to_change_direction = (random.random() * 1.5) + .5
        self.time_elapsed_anim = 0
        self.time_elapsed_direction = 0
        if camera is not None:
            self.setInitialPosition(camera)
        if x is not None and y is not None:
            self.rect.topleft = (x, y)
        self.moving = True
        self.velocity = Enemy.MOVE_VELOCITY
        self.is_alive = True

    def setInitialPosition(self, camera):
        tile_rect = camera.tileEngine.get_tile_rect()
        max_x = camera.tileEngine.getMaxCols() * tile_rect.width -\
            self.rect.width
        min_y = -(
            camera.tileEngine.getNumRows() * tile_rect.height
        ) + Globals.HEIGHT
        max_y = camera.tileEngine.getNumRows() * tile_rect.height -\
            self.rect.height
        keep_looking = True
        radius = max(self.rect.height, self.rect.width) * 2
        while keep_looking:
            self.rect.x = random.randint(0, max_x)
            self.rect.y = random.randint(min_y, Globals.HEIGHT)
            solid_tiles = camera.get_solid_tiles(self.rect.center, radius)
            solid_rects = [pair.rect for pair in solid_tiles]
            num_collided = len(self.rect.collidelistall(solid_rects))
            keep_looking = num_collided > 0

    def update(self, time, camera=None, player=None, change_direction=True):
        if not self.moving:
            return
        self.time_elapsed_anim += time
        self.time_elapsed_direction += time
        if change_direction and \
                self.time_elapsed_direction >= self.time_to_change_direction:
            self.direction = random.randint(0, 3)
            self.time_elapsed_anim = Enemy.WALK_ANIM_TIME
            self.cycle = -1
            self.time_elapsed_direction = 0
        if self.time_elapsed_anim >= Enemy.WALK_ANIM_TIME:
            self.cycle = (self.cycle + 1) % (len(Enemy.images[self.direction]))
            self.image = Enemy.images[self.direction][self.cycle]
            old_rect = self.rect
            self.rect = self.image.get_rect()
            self.rect.center = old_rect.center
            self.time_elapsed_anim = 0
        self.moveRandom(time)
        if camera is not None:
            self.checkCollisions(camera)
        else:
            self.checkScreenCollisions()

    def loadResources(self):
        if Enemy.images[Enemy.INDEX_UP] is None:
            Enemy.images[Enemy.INDEX_UP] = \
                Enemy.loader.load_spritesheet_alpha(
                    "zombie_walking_up.png", 1, 3)
        if Enemy.images[Enemy.INDEX_DOWN] is None:
            Enemy.images[Enemy.INDEX_DOWN] = \
                Enemy.loader.load_spritesheet_alpha(
                    "zombie_walking_down.png", 1, 3)
        if Enemy.images[Enemy.INDEX_LEFT] is None:
            Enemy.images[Enemy.INDEX_LEFT] = \
                Enemy.loader.load_spritesheet_alpha(
                    "zombie_walking_left.png", 3, 1)
        if Enemy.images[Enemy.INDEX_RIGHT] is None:
            Enemy.images[Enemy.INDEX_RIGHT] = \
                Enemy.loader.load_spritesheet_alpha(
                    "zombie_walking_right.png", 3, 1)

    def move(self, xDelta, yDelta):
        super(Enemy, self).move(xDelta, yDelta)

    def moveRandom(self, time):
        norm_delta = self.getMoveNormalized()
        dist_delta = [x * time * self.velocity for x in norm_delta]
        self.move(dist_delta[0], dist_delta[1])

    def getMoveNormalized(self):
        if self.direction == Enemy.INDEX_UP:
            return 0, -1
        elif self.direction == Enemy.INDEX_DOWN:
            return 0, 1
        elif self.direction == Enemy.INDEX_LEFT:
            return -1, 0
        elif self.direction == Enemy.INDEX_RIGHT:
            return 1, 0

    def setDirection(self, direction):
        if not self.direction == direction:
            self.direction = direction
            self.time_elapsed_anim = Enemy.WALK_ANIM_TIME

    def handle_hit(self):
        self.is_alive = False
