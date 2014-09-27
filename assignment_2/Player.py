# Load Libraries
import os
import pygame
import math

from Character import Character
from asset_loader import AssetLoader


class Player(Character):
    MOVE_VELOCITY = 2
    SOUND_PATH = "hitSound.ogg"
    INDEX_DOWN = 0
    INDEX_LEFT = 1
    INDEX_UP = 2
    INDEX_RIGHT = 3
    still_images = [None, None, None, None]
    walking_images = [None, None, None, None]
    hitSound = None
    loader = AssetLoader("images", "sounds")
    WALK_ANIM_TIME = .02
    STILL_ANIM_TIME = .5

    def __init__(self, w, h, x, y):
        super(Player, self).__init__(w, h, x, y)
        self.loadResources()
        self.image = Player.still_images[Player.INDEX_DOWN][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = Player.INDEX_DOWN
        self.is_moving = False
        self.cycle = -1
        self.time_elapsed = 0
        self.anim_time = Player.STILL_ANIM_TIME

    def update(self, time):
        self.time_elapsed += time
        if self.time_elapsed >= self.anim_time:
            if not self.is_moving:
                self.cycle = (self.cycle + 1) % (len(Player.still_images[self.direction]))
                self.image = Player.still_images[self.direction][self.cycle]
                old_rect = self.rect
                self.rect = self.image.get_rect()
                self.rect.center = old_rect.center
            else:
                self.cycle = (self.cycle + 1) % (len(Player.walking_images[self.direction]))
                self.image = Player.walking_images[self.direction][self.cycle]
                old_rect = self.rect
                self.rect = self.image.get_rect()
                self.rect.center = old_rect.center
            self.time_elapsed = 0

        if self.is_moving:
            self.move(time)

    def loadResources(self):
        if Player.still_images[Player.INDEX_UP] is None:
           Player.still_images[Player.INDEX_UP] = Player.loader.load_spritesheet_alpha("main_still_up.png", 1, 2)
        if Player.still_images[Player.INDEX_DOWN] is None:
           Player.still_images[Player.INDEX_DOWN] = Player.loader.load_spritesheet_alpha("main_still_down.png", 1, 2)
        if Player.still_images[Player.INDEX_LEFT] is None:
           Player.still_images[Player.INDEX_LEFT] = Player.loader.load_spritesheet_alpha("main_still_left.png", 2, 1)
        if Player.still_images[Player.INDEX_RIGHT] is None:
           Player.still_images[Player.INDEX_RIGHT] = Player.loader.load_spritesheet_alpha("main_still_right.png", 2, 1)
        if Player.walking_images[Player.INDEX_UP] is None:
           Player.walking_images[Player.INDEX_UP] = Player.loader.load_spritesheet_alpha("main_walking_up.png", 8, 1)
           Player.walking_images[Player.INDEX_UP].reverse()
        if Player.walking_images[Player.INDEX_DOWN] is None:
           Player.walking_images[Player.INDEX_DOWN] = Player.loader.load_spritesheet_alpha("main_walking_down.png", 8, 1)
        if Player.walking_images[Player.INDEX_LEFT] is None:
           Player.walking_images[Player.INDEX_LEFT] = Player.loader.load_spritesheet_alpha("main_walking_left.png", 1, 8)
           Player.walking_images[Player.INDEX_LEFT].reverse()
        if Player.walking_images[Player.INDEX_RIGHT] is None:
           Player.walking_images[Player.INDEX_RIGHT] = Player.loader.load_spritesheet_alpha("main_walking_right.png", 1, 8)
        if Player.hitSound is None:
           Player.hitSound = Player.loader.load_sound(Player.SOUND_PATH)

    def keyPressed(self, keyCode):
        if keyCode == pygame.K_UP:
            self.direction = Player.INDEX_UP
            if not self.is_moving:
                self.anim_time = Player.WALK_ANIM_TIME
                self.time_elapsed = Player.WALK_ANIM_TIME
            self.is_moving = True
        elif keyCode == pygame.K_DOWN:
            self.direction = Player.INDEX_DOWN
            if not self.is_moving:
                self.anim_time = Player.WALK_ANIM_TIME
                self.time_elapsed = Player.WALK_ANIM_TIME
            self.is_moving = True
        elif keyCode == pygame.K_LEFT:
            self.direction = Player.INDEX_LEFT
            if not self.is_moving:
                self.anim_time = Player.WALK_ANIM_TIME
                self.time_elapsed = Player.WALK_ANIM_TIME
            self.is_moving = True
        elif keyCode == pygame.K_RIGHT:
            self.direction = Player.INDEX_RIGHT
            if not self.is_moving:
                self.anim_time = Player.WALK_ANIM_TIME
                self.time_elapsed = Player.WALK_ANIM_TIME
            self.is_moving = True

    def keyReleased(self, keyCode):
        if keyCode == pygame.K_UP and self.direction == Player.INDEX_UP:
            self.is_moving = False
            self.anim_time = Player.STILL_ANIM_TIME
            self.time_elapsed = Player.STILL_ANIM_TIME
        elif keyCode == pygame.K_DOWN and self.direction == Player.INDEX_DOWN:
            self.is_moving = False
            self.anim_time = Player.STILL_ANIM_TIME
            self.time_elapsed = Player.STILL_ANIM_TIME
        elif keyCode == pygame.K_LEFT and self.direction == Player.INDEX_LEFT:
            self.is_moving = False
            self.anim_time = Player.STILL_ANIM_TIME
            self.time_elapsed = Player.STILL_ANIM_TIME
        elif keyCode == pygame.K_RIGHT and self.direction == Player.INDEX_RIGHT:
            self.is_moving = False
            self.anim_time = Player.STILL_ANIM_TIME
            self.time_elapsed = Player.STILL_ANIM_TIME

    def getDirection(self):
        return self.direction

    def getOppositeDirection(self):
        # this only works if the indicies are defined such that the opposite
        # directions are off by 2 (every other)
        return (self.direction + 2) % 4

    def getMoveNormalized(self):
        if not self.is_moving:
            return 0, 0
        elif self.direction == Player.INDEX_UP:
            return 0, -1
        elif self.direction == Player.INDEX_DOWN:
            return 0, 1
        elif self.direction == Player.INDEX_LEFT:
            return -1, 0
        elif self.direction == Player.INDEX_RIGHT:
            return 1, 0

    def move(self, time):
        norm_delta = self.getMoveNormalized()
        dist_delta = [math.ceil(abs(x) * time * Player.MOVE_VELOCITY) for x in norm_delta]
        if norm_delta[0] < 0:
            dist_delta[0] *= -1
        if norm_delta[1] < 0:
            dist_delta[1] *= -1
        super(Player, self).move(dist_delta[0], dist_delta[1])
        self.checkCollisions()

    def checkCollisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.playSound()
        elif self.rect.right > self.w:
            self.rect.right = self.w
            self.playSound()

        if self.rect.top < 0:
            self.rect.top = 0
            self.playSound()
        elif self.rect.bottom > self.h:
            self.rect.bottom = self.h
            self.playSound()

    def playSound(self):
        Player.hitSound.play()
