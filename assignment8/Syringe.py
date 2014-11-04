import pygame
from Globals import Globals
from asset_loader import AssetLoader
import random


class Syringe (pygame.sprite.Sprite):
    NEGATIVE_MARGIN = 10
    VELOCITY = 200
    BURST_VELOCITY = 300
    BURST_PROB = .2

    def __init__(self, x, y, left, left_img_path, right_img_path):
        super(Syringe, self).__init__()
        self.health_effect = 0
        self.left = left
        self.velocity = Syringe.VELOCITY
        if random.random() <= Syringe.BURST_PROB:
            self.velocity = Syringe.BURST_VELOCITY
        if self.left:
            self.velocity *= -1
        self.loader = AssetLoader("images")
        self.is_dead = False
        if left:
            self.image = self.loader.load_image_alpha(left_img_path)
        else:
            self.image = self.loader.load_image_alpha(right_img_path)
        self.init_rect(self.image.get_rect(), x, y)

    def init_rect(self, rect, x, y):
        self.rect = rect
        if self.left:
            self.rect.right = x + Syringe.NEGATIVE_MARGIN
        else:
            self.rect.left = x - Syringe.NEGATIVE_MARGIN
        self.rect.centery = y

    def move(self, x_delta, y_delta):
        self.rect.x += x_delta
        self.rect.y += y_delta

    def kill(self):
        self.is_dead = True

    def update(self, time, camera):
        self.rect.x += time * self.velocity
        radius = max(self.rect.size) * 1.5
        solid_tiles = camera.get_solid_tiles(self.rect.center, radius)
        solid_rects = [pair.rect for pair in solid_tiles]
        collide_rects = self.rect.collidelistall(solid_rects)
        if len(collide_rects) > 0:
            self.kill()


class NormalSyringe(Syringe):
    LEFT_PATH = "blue_syringe_left.png"
    RIGHT_PATH = "blue_syringe_right.png"
    HEALTH_EFFECT = -2

    def __init__(self, x, y, left):
        super(NormalSyringe, self).__init__(x, y, left,
                                            NormalSyringe.LEFT_PATH,
                                            NormalSyringe.RIGHT_PATH)
        self.health_effect = NormalSyringe.HEALTH_EFFECT

class HealthSyringe(Syringe):
    LEFT_PATH = "pink_syringe_left.png"
    RIGHT_PATH = "pink_syringe_right.png"
    HEALTH_EFFECT = 15

    def __init__(self, x, y, left):
        super(HealthSyringe, self).__init__(x, y, left,
                                            HealthSyringe.LEFT_PATH,
                                            HealthSyringe.RIGHT_PATH)
        self.health_effect = NormalSyringe.HEALTH_EFFECT
        
class DeathSyringe(Syringe):
    LEFT_PATH = "green_syringe_left.png"
    RIGHT_PATH = "green_syringe_right.png"
    HEALTH_EFFECT = -10

    def __init__(self, x, y, left):
        super(DeathSyringe, self).__init__(x, y, left,
                                            DeathSyringe.LEFT_PATH,
                                            DeathSyringe.RIGHT_PATH)
        self.health_effect = DeathSyringe.HEALTH_EFFECT
