from __future__ import division
import pygame
from asset_loader import AssetLoader
from math import fabs


class SettingsSlider(object):
    BASE_HEIGHT_PERCENT = .5
    BASE_COLOR = (0, 229, 255)
    BASE_HIGHLIGHT_COLOR = pygame.color.Color('yellow')
    BASE_BORDER_COLOR = pygame.color.Color('black')
    BASE_BORDER_WIDTH = 4
    INDICATOR_WIDTH_PERCENT = .4
    INDICATOR_BORDER_PERCENT = .6
    INDICATOR_BORDER_COLOR = pygame.color.Color('black')
    INDICATOR_INNER_COLOR = pygame.color.Color('gray')
    ARROW_MARGIN = 15
    VELOCITY = 300

    def __init__(self, container, max_value=100, value=None):
        self.container = container
        self.max_value = max_value
        self.value = value if value is not None else self.max_value
        self.loader = AssetLoader('images')
        self.init_slider()
        self.init_arrows()
        self.selected = False

    def init_slider(self):
        self.init_indicator()
        self.init_base()

    def init_indicator(self):
        indicator_height = self.container.height
        indicator_width = indicator_height * \
            SettingsSlider.INDICATOR_WIDTH_PERCENT
        self.indicator_surf = pygame.Surface(
            (indicator_width, indicator_height)).convert()
        self.indicator_surf.fill(SettingsSlider.INDICATOR_INNER_COLOR)
        self.indicator_rect = self.indicator_surf.get_rect()
        pygame.draw.rect(
            self.indicator_surf,
            SettingsSlider.INDICATOR_BORDER_COLOR, self.indicator_rect,
            int(indicator_width * SettingsSlider.INDICATOR_BORDER_PERCENT))
        self.indicator_rect.top = self.container.top
        self.target_x = self.container.left + \
            self.container.width * self.get_percentage()
        self.indicator_rect.centerx = self.target_x

    def init_arrows(self):
        self.arrow_left_surf = self.loader.load_image_alpha('arrow_left.png')
        self.arrow_right_surf = self.loader.load_image_alpha('arrow_right.png')
        self.arrow_left_rect = self.arrow_left_surf.get_rect()
        self.arrow_right_rect = self.arrow_right_surf.get_rect()
        self.arrow_left_rect.centery = self.container.centery
        self.arrow_right_rect.centery = self.container.centery
        self.arrow_left_rect.right = self.container.left - \
            SettingsSlider.ARROW_MARGIN
        self.arrow_right_rect.left = self.container.right + \
            SettingsSlider.ARROW_MARGIN

    def init_base(self):
        base_height = self.container.height * \
            SettingsSlider.BASE_HEIGHT_PERCENT
        self.base_surf = pygame.Surface(
            (self.container.width, base_height)).convert()
        self.base_rect = self.base_surf.get_rect()
        self.base_rect.topleft = self.container.topleft
        self.base_rect.top += (self.container.height - base_height) / 2
        self.fill_base()

    def fill_base(self, base_color=BASE_COLOR):
        self.base_surf.fill(base_color)
        area = self.base_surf.get_rect()
        pygame.draw.rect(
            self.base_surf,
            SettingsSlider.BASE_BORDER_COLOR, area,
            SettingsSlider.BASE_BORDER_WIDTH)

    def select(self):
        self.fill_base(SettingsSlider.BASE_HIGHLIGHT_COLOR)
        self.selected = True

    def deselect(self):
        self.fill_base()
        self.selected = False

    def change_value(self, delta):
        self.set_value(self.value + delta)

    def set_value(self, value):
        self.value = value
        if self.value < 0:
            self.value = 0
        elif self.value > self.max_value:
            self.value = self.max_value
        self.target_x = self.container.left + \
            self.container.width * self.get_percentage()

    def get_percentage(self):
        return self.value / self.max_value

    def render(self, screen):
        screen.blit(self.base_surf, self.base_rect)
        screen.blit(self.indicator_surf, self.indicator_rect)
        if self.selected:
            if self.value > 0:
                screen.blit(self.arrow_left_surf, self.arrow_left_rect)
            if self.value < self.max_value:
                screen.blit(self.arrow_right_surf, self.arrow_right_rect)

    def update(self, time):
        if self.indicator_rect.centerx < self.target_x:
            self.indicator_rect.centerx = min(
                self.indicator_rect.centerx + SettingsSlider.VELOCITY * time,
                self.target_x)
        elif self.indicator_rect.centerx > self.target_x:
            self.indicator_rect.centerx = max(
                self.indicator_rect.centerx - SettingsSlider.VELOCITY * time,
                self.target_x)
