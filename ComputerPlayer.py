# Load Libraries
import os
import pygame
import random

from Character import Character

class ComputerPlayer(Character):
    PATH_START = "images"
    INDEX_DOWN = 0
    INDEX_LEFT = 1
    INDEX_UP = 2
    INDEX_RIGHT = 3
    images = [None, None, None, None]

    def __init__(self, w, h):
        ranX = random.randint(0, w)
        ranY = random.randint(0, h)

        super(ComputerPlayer, self).__init__(w, h, ranX, ranY)
        self.loadResources()
        self.image = ComputerPlayer.images[ComputerPlayer.INDEX_DOWN]
        self.rect = self.image.get_rect()
        self.rect.x = ranX
        self.rect.y = ranY
        self.direction = random.randint(0, 3)

    def update(self):
        pass

    def loadResources(self):
        if ComputerPlayer.images[ComputerPlayer.INDEX_UP] == None:
            ComputerPlayer.images[ComputerPlayer.INDEX_UP] = self.loadImage("goblin_up.png")
        if ComputerPlayer.images[ComputerPlayer.INDEX_DOWN] == None:
            ComputerPlayer.images[ComputerPlayer.INDEX_DOWN] = self.loadImage("goblin_down.png")
        if ComputerPlayer.images[ComputerPlayer.INDEX_LEFT] == None:
            ComputerPlayer.images[ComputerPlayer.INDEX_LEFT] = self.loadImage("goblin_left.png")
        if ComputerPlayer.images[ComputerPlayer.INDEX_RIGHT] == None:
            ComputerPlayer.images[ComputerPlayer.INDEX_RIGHT] = self.loadImage("goblin_right.png")

    def loadImage(self, partialPath):
        return pygame.image.load(os.path.join(ComputerPlayer.PATH_START, partialPath)).convert_alpha()

    # def keyPressed(self, keyCode):
    #     if keyCode == pygame.K_UP:
    #         self.image = ComputerPlayer.images[ComputerPlayer.INDEX_UP]
    #         self.direction = ComputerPlayer.INDEX_UP
    #         self.move(0, -1)
    #     elif keyCode == pygame.K_DOWN:
    #         self.image = ComputerPlayer.images[ComputerPlayer.INDEX_DOWN]
    #         self.direction = ComputerPlayer.INDEX_DOWN
    #         self.move(0, 1)
    #     elif keyCode == pygame.K_LEFT:
    #         self.image = ComputerPlayer.images[ComputerPlayer.INDEX_LEFT]
    #         self.direction = ComputerPlayer.INDEX_LEFT
    #         self.move(-1, 0)
    #     elif keyCode == pygame.K_RIGHT:
    #         self.image = ComputerPlayer.images[ComputerPlayer.INDEX_RIGHT]
    #         self.direction = ComputerPlayer.INDEX_RIGHT
    #         self.move(1, 0)

    def getDirection(self):
        return self.direction

    def getOppositeDirection(self):
        # this only works if the indicies are defined such that the opposite
        # directions are off by 2 (every other)
        return (self.direction + 2) % 4
    
    def move(self, xDelta, yDelta):
        super(ComputerPlayer, self).move(xDelta, yDelta)
        self.checkCollisions()

    def moveRandom(self):

        if self.direction == ComputerPlayer.INDEX_UP:
            self.image = ComputerPlayer.images[ComputerPlayer.INDEX_UP]
            self.direction = ComputerPlayer.INDEX_UP
            self.move(0, -1)
        elif self.direction == ComputerPlayer.INDEX_DOWN:
            self.image = ComputerPlayer.images[ComputerPlayer.INDEX_DOWN]
            self.direction = ComputerPlayer.INDEX_DOWN
            self.move(0, 1)
        elif self.direction == ComputerPlayer.INDEX_LEFT:
            self.image = ComputerPlayer.images[ComputerPlayer.INDEX_LEFT]
            self.direction = ComputerPlayer.INDEX_LEFT
            self.move(-1, 0)
        elif self.direction == ComputerPlayer.INDEX_RIGHT:
            self.image = ComputerPlayer.images[ComputerPlayer.INDEX_RIGHT]
            self.direction = ComputerPlayer.INDEX_RIGHT
            self.move(1, 0)

    def checkCollisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = ComputerPlayer.INDEX_RIGHT
        elif self.rect.right > self.w:
            self.rect.right = self.w
            self.direction = ComputerPlayer.INDEX_LEFT
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction = ComputerPlayer.INDEX_DOWN
        elif self.rect.bottom > self.h:
            self.rect.bottom = self.h
            self.direction = ComputerPlayer.INDEX_UP

##
## REMOVE THIS BEFORE SUBMITTING
def testComputerPlayer():
    pygame.init()
    (width, height) = (700, 500)
    screen = pygame.display.set_mode((width, height))
    running = True
    sprites = pygame.sprite.Group()

    for x in range(13):
        sprites.add(ComputerPlayer(width, height))

    # for x in range(13):
        # sprites.add(ComputerPlayer(width, height,width/2,height/2)

    # p = ComputerPlayer(width, height, width / 2, height / 2)
    # sprites.add(p)

    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)

    while running:
        # handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT + 1:
                for p in sprites:
                    p.direction = random.randint(0,3)
                
        for p in sprites:
            p.moveRandom()
        sprites.update()
        screen.fill((0, 0, 0))
        sprites.draw(screen)
        pygame.display.flip()    

if __name__ == "__main__":
    testComputerPlayer()
##
## END OF CODE TO REMOVE