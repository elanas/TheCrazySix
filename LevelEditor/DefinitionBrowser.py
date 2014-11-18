import pygame
from math import ceil


class DefinitionBrowser:
    NUM_COLS = 3.0
    HIDDEN_ATTR = ['switch_on']

    def __init__(self, tile_engine, container):
        self.tile_engine = tile_engine
        self.container = container
        self.tile_rect = self.tile_engine.get_tile_rect()
        self.padding = int((self.container.width - DefinitionBrowser.NUM_COLS
                            * self.tile_rect.width) /
                           (DefinitionBrowser.NUM_COLS + 1))
        self.definitions = \
            self.tile_engine.tileManager.tileDefinitions.values()
        self.definitions = sorted(
            self.definitions, key=lambda tile: tile.line_num)
        width = self.padding * (DefinitionBrowser.NUM_COLS + 1) + \
            self.tile_rect.width * DefinitionBrowser.NUM_COLS
        num_vert = ceil(len(self.definitions) / DefinitionBrowser.NUM_COLS)
        height = num_vert * (self.padding + self.tile_rect.height) + \
            self.padding
        self.surface = pygame.Surface((width, height)).convert()
        self.area = self.container.copy()
        self.area.width -= self.area.left
        self.area.height -= self.area.top
        self.area.topleft = (0, 0)
        self.selection = [-1, -1]
        self.offset = 0
        self.scroll_amount = self.tile_rect.height + self.padding * 2

    def scroll_up(self):
        self.offset += self.scroll_amount
        if self.offset > self.container.height:
            self.offset = self.container.height

    def scroll_down(self):
        self.offset = max(0, self.offset - self.scroll_amount)

    def render(self, screen):
        self.surface.fill((0, 0, 0))
        row = 0
        col = 0
        for tile in self.definitions:
            if col == DefinitionBrowser.NUM_COLS:
                row += 1
                col = 0
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
        y = self.padding + row * (self.padding + self.tile_rect.height) - self.offset
        x = self.padding + col * (self.padding + self.tile_rect.width)
        return (x, y)

    def handle_mouse_click(self, pos):
        row, col = (0, 0)
        for tile in self.definitions:
            if col == DefinitionBrowser.NUM_COLS:
                row += 1
                col = 0
            coords = self.get_coords(row, col)
            r = pygame.Rect(coords, self.tile_rect.size)
            if r.collidepoint(pos):
                self.selection = [row, col]
                break
            col += 1

    def handle_info_click(self, pos, level_editor):
        row, col = (0, 0)
        for tile in self.definitions:
            if col == DefinitionBrowser.NUM_COLS:
                row += 1
                col = 0
            coords = self.get_coords(row, col)
            r = pygame.Rect(coords, self.tile_rect.size)
            if r.collidepoint(pos):
                old_selection = self.selection
                self.selection = [row, col]
                tile = self.get_selected_tile()
                self.selection = old_selection
                level_editor.show_tile_info(tile=tile)
                break
            col += 1

    def get_selected_tile(self):
        if self.selection[0] == -1 or self.selection[1] == -1:
            return None
        else:
            row = self.selection[0]
            col = self.selection[1]
            return self.definitions[row * int(DefinitionBrowser.NUM_COLS) +
                                    col]

    def clear_selection(self):
        self.selection[0] = -1
        self.selection[1] = -1
