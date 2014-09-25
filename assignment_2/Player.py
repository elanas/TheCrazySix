# Load Libraries
import os
import pygame

from Character import Character
from asset_loader import AssetLoader


class Player(Character):
    MOVE_FACTOR = 3
    SOUND_PATH = "hitSound.ogg"
    INDEX_DOWN = 0
    INDEX_LEFT = 1
    INDEX_UP = 2
    INDEX_RIGHT = 3
    still_images = [None, None, None, None]
    walking_images = [None, None, None, None]
    hitSound = None
    loader = AssetLoader("images", "sounds")
    NUM_UPDATES_STILL = 400
    NUM_UPDATES_WALK = 200

    def __init__(self, w, h, x, y):
        super(Player, self).__init__(w, h, x, y)
        self.loadResources()
        self.image = Player.still_images[Player.INDEX_DOWN][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = Player.INDEX_DOWN
        self.is_moving = False
        self.cycle = -1
        self.num_updates = Player.NUM_UPDATES_STILL

    def update(self):
        self.num_updates -= 1
        if self.num_updates <= 0:
            if not self.is_moving:
                self.cycle = (self.cycle + 1) % (len(Player.still_images[self.direction]))
                self.image = Player.still_images[self.direction][self.cycle]
                old_rect = self.rect
                self.rect = self.image.get_rect()
                self.rect.center = old_rect.center
                self.num_updates = Player.NUM_UPDATES_STILL
            else:
                self.cycle = (self.cycle + 1) % (len(Player.walking_images[self.direction]))
                self.image = Player.walking_images[self.direction][self.cycle]
                old_rect = self.rect
                self.rect = self.image.get_rect()
                self.rect.center = old_rect.center
                self.num_updates = Player.NUM_UPDATES_WALK

    def loadResources(self):
        if Player.still_images[Player.INDEX_UP] is None:
           Player.still_images[Player.INDEX_UP] = Player.loader.load_spritesheet_alpha("zombie_walking_up.png", 1, 2)
        if Player.still_images[Player.INDEX_DOWN] is None:
           Player.still_images[Player.INDEX_DOWN] = Player.loader.load_spritesheet_alpha("zombie_walking_down.png", 1, 2)
        if Player.still_images[Player.INDEX_LEFT] is None:
           Player.still_images[Player.INDEX_LEFT] = Player.loader.load_spritesheet_alpha("zombie_walking_left.png", 2, 1)
        if Player.still_images[Player.INDEX_RIGHT] is None:
           Player.still_images[Player.INDEX_RIGHT] = Player.loader.load_spritesheet_alpha("zombie_walking_right.png", 2, 1)
        if Player.walking_images[Player.INDEX_UP] is None:
           Player.walking_images[Player.INDEX_UP] = Player.loader.load_spritesheet_alpha("main_walking_up.png", 8, 1)
           Player.walking_images[Player.INDEX_UP].reverse()
        if Player.walking_images[Player.INDEX_DOWN] is None:
           Player.walking_images[Player.INDEX_DOWN] = Player.loader.load_spritesheet_alpha("main_walking_down.png", 8, 1)
        if Player.walking_images[Player.INDEX_LEFT] is None:
           Player.walking_images[Player.INDEX_LEFT] = Player.loader.load_spritesheet_alpha("main_walking_left.png", 1, 8)
           Player.walking_images[Player.INDEX_LEFT].reverse()
        if Player.walking_images[Player.INDEX_RIGHT] is None:
           Player.walking_images[Player.INDEX_RIGHT] = Player.loader.load_spritesheet_alpha("main_walking_right.png", 1, 8)
        if Player.hitSound is None:
           Player.hitSound = Player.loader.load_sound(Player.SOUND_PATH)

    # Returns True if the sprite moves, False otherwise
    def keyPressed(self, keyCode):
        if keyCode == pygame.K_UP:
            self.direction = Player.INDEX_UP
            self.move(0, -Player.MOVE_FACTOR)
            if not self.is_moving:
                self.num_updates = 0
            self.is_moving = True
            self.update()
        elif keyCode == pygame.K_DOWN:
            self.direction = Player.INDEX_DOWN
            self.move(0, Player.MOVE_FACTOR)
            if not self.is_moving:
                self.num_updates = 0
            self.is_moving = True
            self.update()
        elif keyCode == pygame.K_LEFT:
            self.direction = Player.INDEX_LEFT
            self.move(-Player.MOVE_FACTOR, 0)
            if not self.is_moving:
                self.num_updates = 0
            self.is_moving = True
            self.update()
        elif keyCode == pygame.K_RIGHT:
            self.direction = Player.INDEX_RIGHT
            self.move(Player.MOVE_FACTOR, 0)
            if not self.is_moving:
                self.num_updates = 0
            self.is_moving = True
            self.update()
        else:
            return False
        return True

    def keyReleased(self, keyCode):
        if keyCode == pygame.K_UP:
            self.is_moving = False
            self.num_updates = 0
            self.update()
        elif keyCode == pygame.K_DOWN:
            self.is_moving = False
            self.num_updates = 0
            self.update()
        elif keyCode == pygame.K_LEFT:
            self.is_moving = False
            self.num_updates = 0
            self.update()
        elif keyCode == pygame.K_RIGHT:
            self.is_moving = False
            self.num_updates = 0
            self.update()

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


#
# REMOVE THIS BEFORE SUBMITTING
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
        if last_key is not None:
            p.keyPressed(last_key)
        sprites.update()
        screen.fill((0, 0, 0))
        sprites.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    testPlayer()
#
# END OF CODE TO REMOVE
