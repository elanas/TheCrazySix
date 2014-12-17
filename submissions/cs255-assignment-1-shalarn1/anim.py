# Team: The Crazy Six
# Sarika Halarnakar - shalarn1@jhu.ed
# Assignment 1
#!/usr/bin/python

import pygame
import random


background_colour = (255,255,255)
(width, height) = (600, 400)

pygame.init()
x_prev = 0
y_prev = 0

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Assignment 1 - shalarn1')
screen.fill(background_colour)

running = True
while running:
  red = random.randint(0, 255)
  blue = random.randint(0, 255)
  green = random.randint(0, 255)
  x2 = random.randint(0, width)
  y2 = random.randint(0, height)
  pygame.draw.lines(screen,(red, blue, green) , False, [(x_prev, y_prev), (x2,y2)], 1)
  pygame.display.update()
  x_prev = x2
  y_prev = y2
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False