# Load Libraries
import os
import pygame
import math

from Border import Border
from asset_loader import AssetLoader
from Globals import Globals


class Wall(Border):
    SOUND_PATH = "collision_sound.ogg"
    image = [None, None, None, None]
    hitSound = None
    loader = AssetLoader("images", "sounds")

    def __init__(self, w, h, x, y):
        super(Wall, self).__init__(w, h, x, y)
        self.loadResources()
        self.image = pygame.Surface((w, h)).convert()
        self.fillSurface()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def fillSurface(self):
        img = self.getScaledImage()
        if self.isVertical():
            curr_height = 0
            while curr_height < self.h:
                height = min(img.get_rect().height, self.h - curr_height)
                area = pygame.Rect(0, curr_height, self.w, height)
                self.image.blit(img, area)
                curr_height += height
        else:
            curr_with = 0
            while curr_with < self.w:
                width = min(img.get_rect().width, self.w - curr_with)
                area = pygame.Rect(curr_with, 0, width, self.h)
                self.image.blit(img, area)
                curr_with += width

    def getScaledImage(self):
        img = self.loader.load_image("gray_tile_brick.png")
        old_w = img.get_rect().width
        old_h = img.get_rect().height
        new_w = 0
        new_h = 0
        if self.isVertical():
            img = pygame.transform.rotate(img, 90)
            if old_w >= self.w:
                return img
            new_w = self.w
            new_h = old_h * self.w / old_w
        else:
            if old_h >= self.h:
                return img
            new_h = self.h
            new_w = old_w * self.h / old_h
        return pygame.transform.scale(img, (new_w, new_h))

    def isVertical(self):
        return self.h > self.w

    def update(self, time):
        pass

    def loadResources(self):
        pass

    def checkCollisions(self):
        pass

    def playSound(self):
        pass
