import pygame
from Player import Player


class BorderPlayer(Player):

    def __init__(self, w, h, init_x, init_y, init_direction):
        super(BorderPlayer, self).__init__(w, h, init_x, init_y)
        # self.is_moving = True
        self.direction = init_direction
        # self.move_velocity = 100

    def onDraw(self):
        if self.direction == Player.INDEX_UP:
            self.keyPressed(pygame.K_UP)
        elif self.direction == Player.INDEX_DOWN:
            self.keyPressed(pygame.K_DOWN)
        elif self.direction == Player.INDEX_LEFT:
            self.keyPressed(pygame.K_LEFT)
        elif self.direction == Player.INDEX_RIGHT:
            self.keyPressed(pygame.K_RIGHT)

    def checkCollisions(self):
        if self.rect.left < 0:
            # self.rect.top = self.rect.left
            self.rect.left = 0
            self.direction = Player.INDEX_DOWN
        elif self.rect.right > self.w:
            # self.rect.top -= self.rect.right - self.w
            self.rect.right = self.w
            self.direction = Player.INDEX_UP
        elif self.rect.top < 0:
            # self.rect.x -= self.rect.top
            self.rect.top = 0
            self.direction = Player.INDEX_LEFT
        elif self.rect.bottom > self.h:
            # self.rect.x = self.rect.bottom - self.h
            self.rect.bottom = self.h
            self.direction = Player.INDEX_RIGHT
