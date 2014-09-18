# IMPORT THE PYGAME
import pygame

from Player import Player

pygame.init()

BACKGROUND_IMAGE_NAME = "test.png"

background = pygame.image.load(BACKGROUND_IMAGE_NAME)
size = background.get_size()
screen = pygame.display.set_mode(size)
# frames_per_second = 24

# DIVIDE SPRITESHEET
#rows = 4
#cols = 4
#height = spriteSheet.get_height() / rows
# width = spriteSheet.get_width() / cols
# frames = []

# for row in range(rows):
#     for col in range(cols):
#         clip = pygame.Rect(col * width, row * height, width, height)
#         frame = spriteSheet.subsurface(clip)
#         frames.append(frame)

# pygame.time.set_timer(pygame.USEREVENT, int(1000 / frames_per_second))

while True:
    event = pygame.event.wait()

    if event.type == pygame.QUIT:
        break

    if event.type == pygame.USEREVENT:
        screen.fill(pygame.Color("white"))
        # frame = (frame + 1) % len(frames)
        #image = frames[frame]

        bounds = image.get_rect()
        bounds.center = pygame.mouse.get_pos()

        screen.blit(background, [0, 0])
        screen.blit(image, bounds)

        pygame.display.flip()

pygame.quit()
