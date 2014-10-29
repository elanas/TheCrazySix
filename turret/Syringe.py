import pygame
from Globals import Globals
from asset_loader import AssetLoader


class Syringe (pygame.sprite.Sprite):
    NEGATIVE_MARGIN = 2
    VELOCITY = 200

    def __init__(self, x, y, left, left_img_path, right_img_path):
        super(Syringe, self).__init__()
        self.left = left
        self.velocity = Syringe.VELOCITY
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
        self.x += x_delta
        self.y += y_delta

    def get_health_effect(self):
        return 0

    def kill(self):
        self.is_dead = True

    def update(self, time, camera):
        self.rect.x += time * self.velocity
        radius = max(self.rect.size) * 1.5
        solid_tiles = camera.get_solid_tiles(self.rect.center, radius)
        solid_rects = [pair.rect for pair in solid_tiles]
        collide_rects = self.rect.collidelistall(solid_rects)
        if len(collide_rects) > 0:
            self.is_dead = True


class NormalSyringe(Syringe):
    LEFT_PATH = "normal_syringe_left.png"
    RIGHT_PATH = "normal_syringe_right.png"

    def __init__(self, x, y, left):
        super(NormalSyringe, self).__init__(x, y, left,
                                            NormalSyringe.LEFT_PATH,
                                            NormalSyringe.RIGHT_PATH)        
