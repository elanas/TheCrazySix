import pygame
from Globals import Globals
from asset_loader import AssetLoader


class Syringe (pygame.sprite.Sprite):
    NEGATIVE_MARGIN = 2

    def __init__(self, x, y, left, left_img_path, right_img_path):
        super(Syringe, self).__init__()
        self.x = x
        self.y = y
        self.left = left
        self.loader = AssetLoader("images")
        self.is_dead = False
        if left:
            self.image = self.loader.load_image_alpha(left_img_path)
        else:
            self.image = self.loader.load_image_alpha(right_img_path)
        self.init_rect(self.image.get_rect())

    def init_rect(self, rect):
        self.rect = rect
        if self.left:
            self.rect.right = self.x + Syringe.NEGATIVE_MARGIN
        else:
            self.rect.left = self.x - Syringe.NEGATIVE_MARGIN
        self.rect.centery = self.y

    def move(self, x_delta, y_delta):
        self.x += x_delta
        self.y += y_delta

    def get_health_effect(self):
        return 0

    def kill(self):
        self.is_dead = True

    def update(self, time, camera):
        pass


class NormalSyringe(Syringe):
    LEFT_PATH = "normal_syringe_left.png"
    RIGHT_PATH = "normal_syringe_right.png"

    def __init__(self, x, y, left):
        super(NormalSyringe, self).__init__(x, y, left,
                                            NormalSyringe.LEFT_PATH,
                                            NormalSyringe.RIGHT_PATH)        
