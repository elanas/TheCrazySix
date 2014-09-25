# Load Libraries
import os
import pygame
import random

from Character import Character
from asset_loader import AssetLoader

class Enemy(Character):
    INDEX_DOWN = 0
    INDEX_LEFT = 1
    INDEX_UP = 2
    INDEX_RIGHT = 3
    images = [None, None, None, None]
    loader = AssetLoader("images")
    NUM_UPDATES_WALK = 500

    def __init__(self, w, h):
        ranX = random.randint(0, w)
        ranY = random.randint(0, h)

        super(Enemy, self).__init__(w, h, ranX, ranY)
        self.loadResources()
        self.direction = random.randint(0, 3)
        self.image = Enemy.images[self.direction][0]
        self.rect = self.image.get_rect()
        self.rect.x = ranX
        self.rect.y = ranY
        self.cycle = -1
        self.num_updates = Enemy.NUM_UPDATES_WALK

    def update(self):
        self.num_updates -= 1
        if self.num_updates <= 0:
            self.cycle = (self.cycle + 1) % (len(Enemy.images[self.direction]))
            self.image = Enemy.images[self.direction][self.cycle]
            old_rect = self.rect
            self.rect = self.image.get_rect()
            self.rect.center = old_rect.center
            self.num_updates = Enemy.NUM_UPDATES_WALK

    def loadResources(self):
        if Enemy.images[Enemy.INDEX_UP] is None:
            Enemy.images[Enemy.INDEX_UP] = Enemy.loader.load_spritesheet_alpha("zombie_walking_up.png", 1, 3)
        if Enemy.images[Enemy.INDEX_DOWN] is None:
            Enemy.images[Enemy.INDEX_DOWN] = Enemy.loader.load_spritesheet_alpha("zombie_walking_down.png", 1, 3)
        if Enemy.images[Enemy.INDEX_LEFT] is None:
            Enemy.images[Enemy.INDEX_LEFT] = Enemy.loader.load_spritesheet_alpha("zombie_walking_left.png", 3, 1)
        if Enemy.images[Enemy.INDEX_RIGHT] is None:
            Enemy.images[Enemy.INDEX_RIGHT] = Enemy.loader.load_spritesheet_alpha("zombie_walking_right.png", 3, 1)

    def move(self, xDelta, yDelta):
        super(Enemy, self).move(xDelta, yDelta)
        self.checkCollisions()

    def moveRandom(self):
        if self.direction == Enemy.INDEX_UP:
            self.direction = Enemy.INDEX_UP
            self.move(0, -1)
            # self.cycle = 0
            # self.num_updates = 0
            # self.update()
        elif self.direction == Enemy.INDEX_DOWN:
            self.direction = Enemy.INDEX_DOWN
            self.move(0, 1)
            # self.cycle = 0
            # self.num_updates = 0
            # self.update()
        elif self.direction == Enemy.INDEX_LEFT:
            self.direction = Enemy.INDEX_LEFT
            self.move(-1, 0)
            # self.cycle = 0
            # self.num_updates = 0
            # self.update()
        elif self.direction == Enemy.INDEX_RIGHT:
            self.direction = Enemy.INDEX_RIGHT
            self.move(1, 0)
            # self.cycle = 0
            # self.num_updates = 0
            # self.update()

    def setDirection(self, direction):
        if not self.direction == direction:
            self.num_updates = 0
            self.direction = direction
            self.update()

    def checkCollisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.setDirection(Enemy.INDEX_RIGHT)
        elif self.rect.right > self.w:
            self.rect.right = self.w
            self.setDirection(Enemy.INDEX_LEFT)
        if self.rect.top < 0:
            self.rect.top = 0
            self.setDirection(Enemy.INDEX_DOWN)
        elif self.rect.bottom > self.h:
            self.rect.bottom = self.h
            self.setDirection(Enemy.INDEX_UP)


#
# REMOVE THIS BEFORE SUBMITTING
def testEnemy():
    pygame.init()
    (width, height) = (700, 500)
    screen = pygame.display.set_mode((width, height))
    running = True
    sprites = pygame.sprite.Group()

    for x in range(13):
        sprites.add(Enemy(width, height))

    # Ideally, each computer object should have a unique timer
    # for changing direction or other movements
    # Alternative: Randomizing timer interval per object
    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)

    while running:
        # handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT + 1:
                for p in sprites:
                    p.direction = random.randint(0, 3)

        for p in sprites:
            p.moveRandom()
        sprites.update()
        screen.fill((0, 0, 0))
        sprites.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    testEnemy()
#
# END OF CODE TO REMOVE
