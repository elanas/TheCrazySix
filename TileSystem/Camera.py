import pygame
from Globals import Globals
from collections import namedtuple
from TileType import TileType


class Camera(object):
    BOTTOM_PADDING = 0
    EMPTY_COLOR = (0, 0, 0)
    TileRectPair = namedtuple('TileRectPair', 'tile rect coords')

    def __init__(self, tileEngine, container):
        self.tileEngine = tileEngine
        self.container = container
        self.viewpoint = container.copy()
        self.initView()
        self.surface = pygame.Surface(self.viewpoint.size).convert()
        self.surface_ready = False

    def set_dirty(self):
        self.surface_ready = False

    def initView(self):
        tileRect = self.tileEngine.get_tile_rect()
        numRows = self.tileEngine.getNumRows()
        tile_map = self.tileEngine.tileMap
        start_pos = [-1, -1]
        for row_num in range(0, len(tile_map)):
            for col_num in range(0, len(tile_map[row_num])):
                if tile_map[
                    row_num
                ][col_num] is None:
                    continue
                if TileType.START_ATTR in \
                        tile_map[row_num][col_num].special_attr:
                    if start_pos[0] != -1:
                        raise Exception(
                            "There can only be one starting tile in the map"
                        )
                    start_pos[0] = row_num
                    start_pos[1] = col_num
        if start_pos[0] != -1:
            self.viewpoint.centery = tileRect.height * start_pos[0]
            self.viewpoint.centerx = tileRect.width * start_pos[1]
            tile_map[start_pos[0]][start_pos[1]] = \
                self.tileEngine.get_tile_from_attr(TileType.BASE_ATTR)
        else:
            self.viewpoint.bottom = tileRect.height * numRows + \
                Camera.BOTTOM_PADDING
            self.viewpoint.centerx = (tileRect.width *
                                      self.tileEngine.getMaxCols()) / 2

    def render(self, screen):
        screen.fill(Camera.EMPTY_COLOR, self.container)
        if self.surface_ready:
            screen.blit(self.surface, self.container)
        else:
            self.build_surface()
            self.render(screen)

    def build_surface(self):
        self.surface.fill(Camera.EMPTY_COLOR)
        curr_y = self.viewpoint.top
        while curr_y - self.viewpoint.top < self.container.height:
            curr_x = self.viewpoint.left
            while curr_x - self.viewpoint.left < self.container.right:
                curr_tile_img, curr_rect = \
                    self.tileEngine.get_tile_image(curr_x, curr_y)
                curr_rect.left = \
                    (curr_x - self.viewpoint.left)
                curr_rect.top = \
                    (curr_y - self.viewpoint.top)
                if curr_tile_img is not None:
                    img_area = curr_tile_img.get_rect()
                    if curr_rect.bottom > self.container.height:
                        img_area.height -= \
                            curr_rect.bottom - self.container.height
                    if curr_rect.right > self.container.width:
                        img_area.width -= \
                            curr_rect.right - self.container.width
                    self.surface.blit(curr_tile_img, curr_rect, img_area)
                curr_x += curr_rect.width
            curr_y += curr_rect.height
        self.surface_ready = True

    def move(self, xDelta, yDelta):
        self.surface_ready = False
        self.viewpoint.x += xDelta
        self.viewpoint.y += yDelta

    def get_nearby_tiles(self, center, radius):
        tiles = list()
        curr_y = center[1] - radius
        max_x = center[0] + radius
        max_y = center[1] + radius
        while curr_y < max_y:
            curr_x = center[0] - radius
            trans_y = curr_y + self.viewpoint.top
            while curr_x < max_x:
                trans_x = curr_x + self.viewpoint.left
                curr_tile, curr_rect = \
                    self.tileEngine.get_tile(trans_x, trans_y)
                curr_rect.x = \
                    (curr_rect.x - self.viewpoint.left) + self.container.left
                curr_rect.y = \
                    (curr_rect.y - self.viewpoint.top) + self.container.top
                if curr_rect.bottom > max_y:
                    curr_rect.height -= curr_rect.bottom - max_y
                if curr_rect.right > max_x:
                    curr_rect.width -= curr_rect.right - max_x
                tiles.append(
                    Camera.TileRectPair(
                        tile=curr_tile,
                        rect=curr_rect,
                        coords=(trans_x, trans_y)
                    ))
                curr_x += curr_rect.width
                if curr_rect.width == 0:
                    break
            curr_y += curr_rect.height
            if curr_rect.height == 0:
                break
        return tiles

    def get_solid_tiles(self, center, radius):
        nearby_tiles = self.get_nearby_tiles(center, radius)
        return [pair for pair in nearby_tiles if pair.tile.is_solid]

    def get_special_tiles(self, center, radius):
        nearby_tiles = self.get_nearby_tiles(center, radius)
        return [pair for pair in nearby_tiles if pair.tile.is_special]
