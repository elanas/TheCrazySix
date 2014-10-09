import pygame
from Globals import Globals


class Camera(object):
    BOTTOM_PADDING = 0
    EMPTY_COLOR = (0, 0, 0)

    def __init__(self, tileEngine, container):
        self.tileEngine = tileEngine
        self.container = container
        self.viewpoint = container.copy()
        self.initView()

    def initView(self):
        tileRect = self.tileEngine.get_tile_rect()
        numRows = self.tileEngine.getNumRows()
        self.viewpoint.bottom = tileRect.height * numRows + Camera.BOTTOM_PADDING
        self.viewpoint.centerx =  (tileRect.width * self.tileEngine.getMaxCols()) / 2

    def render(self, screen):        
        screen.fill(Camera.EMPTY_COLOR, self.container)
        curr_y = self.viewpoint.top
        while curr_y - self.viewpoint.top + self.container.top < self.container.bottom:
            curr_x = self.viewpoint.left
            while curr_x - self.viewpoint.left + self.container.left < self.container.right:
                curr_tile_img, curr_rect = self.tileEngine.get_tile_image(curr_x, curr_y)
                curr_rect.left = (curr_x - self.viewpoint.left) + self.container.left
                curr_rect.top = (curr_y - self.viewpoint.top) + self.container.top
                if curr_tile_img is not None:
                    img_area = curr_tile_img.get_rect()
                    if curr_rect.bottom > self.container.bottom:
                        img_area.height -= curr_rect.bottom - self.container.bottom
                    if curr_rect.right > self.container.right:
                        img_area.width -= curr_rect.right - self.container.right
                    
                    screen.blit(curr_tile_img, curr_rect, img_area)
                curr_x += curr_rect.width
            curr_y += curr_rect.height

    def move(self, xDelta, yDelta):
        self.viewpoint.x += xDelta
        self.viewpoint.y += yDelta

    def getSolidObjects(self, center, radius):
        pass

    def getSpecialObjects(self, center, radius):
        pass
