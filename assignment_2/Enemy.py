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
    NUM_UPDATES_WALK = 200

    def __init__(self, w, h):
        ranX = random.randint(0, w)
        ranY = random.randint(0, h)

        super(Enemy, self).__init__(w, h, ranX, ranY)
        self.loadResources()
        self.image = Enemy.images[Enemy.INDEX_DOWN][0]
        self.rect = self.image.get_rect()
        self.rect.x = ranX
        self.rect.y = ranY
        self.direction = random.randint(0, 3)
        self.cycle = -1
        self.num_updates = Player.NUM_UPDATES_WALK

    def update(self):
        pass

    def loadResources(self):
        if Enemy.images[Enemy.INDEX_UP] is None:
            Enemy.images[Enemy.INDEX_UP] = Player.loader.load_spritesheet_alpha("zombie_walking_up.png", 1, 2)
        if Enemy.images[Enemy.INDEX_DOWN] is None:
            Enemy.images[Enemy.INDEX_DOWN] = Player.loader.load_spritesheet_alpha("zombie_walking_down.png", 1, 2)
        if Enemy.images[Enemy.INDEX_LEFT] is None:
            Enemy.images[Enemy.INDEX_LEFT] = Player.loader.load_spritesheet_alpha("zombie_walking_left.png", 2, 1)
        if Enemy.images[Enemy.INDEX_RIGHT] is None:
            Enemy.images[Enemy.INDEX_RIGHT] = Player.loader.load_spritesheet_alpha("zombie_walking_right.png", 2, 1)

    def loadImage(self, partialPath):
        return pygame.image.load(os.path.join(
            Enemy.PATH_START, partialPath)).convert_alpha()

    def getDirection(self):
        return self.direction

    def getOppositeDirection(self):
        # this only works if the indicies are defined such that the opposite
        # directions are off by 2 (every other)
        return (self.direction + 2) % 4

    def move(self, xDelta, yDelta):
        super(Enemy, self).move(xDelta, yDelta)
        self.checkCollisions()

    def moveRandom(self):

        if self.direction == Enemy.INDEX_UP:
            self.image = Enemy.images[Enemy.INDEX_UP]
            self.direction = Enemy.INDEX_UP
            self.move(0, -1)
        elif self.direction == Enemy.INDEX_DOWN:
            self.image = Enemy.images[Enemy.INDEX_DOWN]
            self.direction = Enemy.INDEX_DOWN
            self.move(0, 1)
        elif self.direction == Enemy.INDEX_LEFT:
            self.image = Enemy.images[Enemy.INDEX_LEFT]
            self.direction = Enemy.INDEX_LEFT
            self.move(-1, 0)
        elif self.direction == Enemy.INDEX_RIGHT:
            self.image = Enemy.images[Enemy.INDEX_RIGHT]
            self.direction = Enemy.INDEX_RIGHT
            self.move(1, 0)

    def checkCollisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = Enemy.INDEX_RIGHT
        elif self.rect.right > self.w:
            self.rect.right = self.w
            self.direction = Enemy.INDEX_LEFT
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction = Enemy.INDEX_DOWN
        elif self.rect.bottom > self.h:
            self.rect.bottom = self.h
            self.direction = Enemy.INDEX_UP


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
