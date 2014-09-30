# Load Libraries
import os
import pygame
import math

from Border import Border
from asset_loader import AssetLoader
from Globals import Globals


class Wall(Border):
    SOUND_PATH = "hitSound.ogg"
    image = [None, None, None, None]
    hitSound = None
    loader = AssetLoader("images", "sounds")
  
    def __init__(self, w, h, x, y):
        super(Wall, self).__init__(w, h, x, y)
        self.loadResources()
        self.image = pygame.Surface((w, h))

        # self.image = Player.still_images[Player.INDEX_DOWN][0]
        # self.rect = self.image.get_rect()
        self.rect = pygame.draw.rect(self.image, (0, 0, 255), (x, y, w, h))
        self.rect.x = x
        self.rect.y = y

    def update(self, time):
        pass

    def loadResources(self):
        #load image
        # if Player.hitSound is None:
        #     Player.hitSound = Player.loader.load_sound(Player.SOUND_PATH)
        pass

    def checkCollisions(self):
        # if self.rect.left < 0:
        #     self.rect.left = 0
        #     self.playSound()
        # elif self.rect.right > self.w:
        #     self.rect.right = self.w
        #     self.playSound()

        # if self.rect.top < 0:
        #     self.rect.top = 0
        #     self.playSound()
        # elif self.rect.bottom > self.h:
        #     self.rect.bottom = self.h
        #     self.playSound()
        pass

    def playSound(self):
        # Player.hitSound.play()
        pass
