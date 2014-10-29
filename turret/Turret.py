import pygame
import random
import Syringe


class Turret(object):
    MIN_WAIT = 3
    PROB_NORMAL = .05

    def __init__(self, x, y, left):
        self.x = x
        self.y = y
        self.left = left
        self.lastshot = Turret.MIN_WAIT
        self.syringeSprites = pygame.sprite.Group()

    def render(self, screen):
        self.syringeSprites.draw(screen)

    def update(self, time, camera):
        self.lastshot += time
        if self.lastshot >= Turret.MIN_WAIT:
	        self.fire()
        self.syringeSprites.update(time, camera)
        dead = [syringe for syringe in self.syringeSprites if syringe.is_dead]
        self.syringeSprites.remove(dead)

    def fire(self):
        if random.random() <= Turret.PROB_NORMAL:
            self.syringeSprites.add(Syringe.NormalSyringe(self.x,self.y, self.left))
            self.lastshot = 0

    def move(self, x_delta, y_delta):
    	self.x += x_delta
    	self.y += y_delta
        for syringe in self.syringeSprites:
            syringe.move(x_delta, y_delta)