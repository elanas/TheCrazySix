# Load Libraries
import os
import pygame

from Character import Character

class Player(Character):
    PATH_START = "images"
    SOUND_PATH = os.path.join("sounds", "hitSound.wav")
    INDEX_DOWN = 0
    INDEX_LEFT = 1
    INDEX_UP = 2
    INDEX_RIGHT = 3
    images = [None, None, None, None]
    hitSound = None

    def __init__(self, w, h, x, y):
        super(Player, self).__init__(w, h, x, y)
        self.loadResources()
        self.image = Player.images[Player.INDEX_DOWN]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = Player.INDEX_DOWN

    def update(self):
        pass

    def loadResources(self):
        if Player.images[Player.INDEX_UP] == None:
            Player.images[Player.INDEX_UP] = self.loadImage("businessman_up.png")
        if Player.images[Player.INDEX_DOWN] == None:
            Player.images[Player.INDEX_DOWN] = self.loadImage("businessman_down.png")
        if Player.images[Player.INDEX_LEFT] == None:
            Player.images[Player.INDEX_LEFT] = self.loadImage("businessman_left.png")
        if Player.images[Player.INDEX_RIGHT] == None:
            Player.images[Player.INDEX_RIGHT] = self.loadImage("businessman_right.png")
        if Player.hitSound == None:
            Player.hitSound = pygame.mixer.Sound(Player.SOUND_PATH)

    def loadImage(self, partialPath):
        return pygame.image.load(os.path.join(Player.PATH_START, partialPath)).convert_alpha()

    def keyPressed(self, keyCode):
        if keyCode == pygame.K_UP:
            self.image = Player.images[Player.INDEX_UP]
            self.direction = Player.INDEX_UP
            self.move(0, -1)
        elif keyCode == pygame.K_DOWN:
            self.image = Player.images[Player.INDEX_DOWN]
            self.direction = Player.INDEX_DOWN
            self.move(0, 1)
        elif keyCode == pygame.K_LEFT:
            self.image = Player.images[Player.INDEX_LEFT]
            self.direction = Player.INDEX_LEFT
            self.move(-1, 0)
        elif keyCode == pygame.K_RIGHT:
            self.image = Player.images[Player.INDEX_RIGHT]
            self.direction = Player.INDEX_RIGHT
            self.move(1, 0)

    def getDirection(self):
        return self.direction

    def getOppositeDirection(self):
        # this only works if the indicies are defined such that the opposite
        # directions are off by 2 (every other)
        return (self.direction + 2) % 4
    
    def move(self, xDelta, yDelta):
        super(Player, self).move(xDelta, yDelta)
        self.checkCollisions()

    def checkCollisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.playSound()
        elif self.rect.right > self.w:
            self.rect.right = self.w
            self.playSound()

        if self.rect.top < 0:
            self.rect.top = 0
            self.playSound()
        elif self.rect.bottom > self.h:
            self.rect.bottom = self.h
            self.playSound()

    def playSound(self):
        Player.hitSound.play()

def testPlayer():
    pygame.init()
    (width, height) = (700, 500)
    screen = pygame.display.set_mode((width, height))
    running = True
    sprites = pygame.sprite.Group()
    p = Player(width, height, width / 2, height / 2)
    sprites.add(p)
    last_key = None
    while running:
        # handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                last_key = event.key
            elif event.type == pygame.KEYUP:
                last_key = None
        if not last_key == None:
            p.keyPressed(last_key)
        sprites.update()
        screen.fill((0, 0, 0))
        sprites.draw(screen)
        pygame.display.flip()    

if __name__ == "__main__":
    testPlayer()
