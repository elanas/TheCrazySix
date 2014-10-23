import pygame
from math import ceil

class DefinitionBrowser:
    NUM_COLS = 3.0
    
    def __init__(self, tile_engine, container):
        self.tile_engine = tile_engine
        self.container = container
        self.tile_rect = self.tile_engine.get_tile_rect()
        self.padding = int((self.container.width - DefinitionBrowser.NUM_COLS \
                            * self.tile_rect.width) / (DefinitionBrowser.NUM_COLS + 1))
        self.definitions = self.tile_engine.tileManager.tileDefinitions.copy()
        width = self.padding * (DefinitionBrowser.NUM_COLS + 1) + self.tile_rect.width * DefinitionBrowser.NUM_COLS
        num_vert = ceil(len(self.definitions) / DefinitionBrowser.NUM_COLS)
        height = num_vert * (self.padding + self.tile_rect.height) + self.padding
        self.surface = pygame.Surface((width, height)).convert()
        # self.surface.fill((255, 255, 255))
        self.area = self.container.copy()
        self.area.width -= self.area.left
        self.area.height -= self.area.top
        self.area.topleft = (0, 0)
        self.selection = (-1, -1)

    def render(self, screen):
        row = 0
        col = 0
        for key in self.definitions:
            if col == DefinitionBrowser.NUM_COLS:
                row += 1
                col = 0
            tile = self.definitions[key]
            pos = self.get_coords(row, col)
            self.surface.blit(tile.image, pos)
            r = self.tile_rect.copy()
            r.inflate_ip(1, 1)
            r.centerx = pos[0] + self.tile_rect.width / 2
            r.centery = pos[1] + self.tile_rect.height / 2
            color = (255, 255, 255)
            if self.selection[0] == row and self.selection[1] == col:
                color = (255, 0, 0)
            pygame.draw.rect(self.surface, color, r, 2)
            col += 1
        screen.blit(self.surface, self.container, self.area)

    def get_coords(self, row, col):
        y = self.padding + row * (self.padding + self.tile_rect.height)
        x = self.padding + col * (self.padding + self.tile_rect.width)
        return (x, y)
