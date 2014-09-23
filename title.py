import sys as SYS
import glob as G
import pygame as PG
import pygame.mixer as PM
import pygame.display as PDI
import pygame.event as PE
import pygame.font as PF

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PG.init()
screen = PDI.set_mode((1024, 768))

WIDTH = screen.get_width()
HEIGHT = screen.get_height()


screen.fill(BLACK)

font = PF.Font("28-days-later.ttf", 64)
surf = font.render("Unnamed Game!", True, WHITE)
width, height = surf.get_size()
screen.blit(surf, (WIDTH / 2 - width / 2, HEIGHT / 2 - height / 2 + 64))

PDI.flip()

while True:
    for event in PE.get():
        if event.type == PG.QUIT:
            SYS.exit()
        elif event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            SYS.exit()
