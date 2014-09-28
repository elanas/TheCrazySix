# IMPORT THE PYGAME
import pygame
import random

from Player import Player
from Enemy import Enemy


def main():
    pygame.init()
    (width, height) = (700, 500)
    screen = pygame.display.set_mode((width, height))
    running = True
    enemySprites = pygame.sprite.Group()
    playerSprites = pygame.sprite.Group()

    for x in range(13):
        enemySprites.add(Enemy(width, height))

    playerSprites.add(Player(width, height, width / 2, height / 2))

    # Ideally, each computer object should have a unique timer
    # for changing direction or other movements
    # Alternative: Randomizing timer interval per object
    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 20)

    last_key = None

    while running:
        # handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.USEREVENT + 1:
                for p in enemySprites:
                    p.setDirection(random.randint(0, 3))
                    # p.direction = random.randint(0, 3)
            elif event.type == pygame.USEREVENT + 2:
                for p in enemySprites:
                    p.moveRandom()
                if last_key is not None:
                    for p in playerSprites:
                        p.keyPressed(last_key)
            elif event.type == pygame.KEYDOWN and last_key is None:
                last_key = event.key
            elif event.type == pygame.KEYUP and event.key == last_key:
                for p in playerSprites:
                    p.keyReleased(event.key)
                last_key = None

        enemySprites.update()
        playerSprites.update()
        screen.fill((255, 255, 255))
        enemySprites.draw(screen)
        playerSprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()


# pygame.init()

# BACKGROUND_IMAGE_NAME = "test.png"

# background = pygame.image.load(BACKGROUND_IMAGE_NAME)
# size = background.get_size()
# screen = pygame.display.set_mode(size)
# frames_per_second = 24

# DIVIDE SPRITESHEET
# rows = 4
# cols = 4
# height = spriteSheet.get_height() / rows
# width = spriteSheet.get_width() / cols
# frames = []

# for row in range(rows):
# for col in range(cols):
# clip = pygame.Rect(col * width, row * height, width, height)
# frame = spriteSheet.subsurface(clip)
# frames.append(frame)

# pygame.time.set_timer(pygame.USEREVENT, int(1000 / frames_per_second))

# while True:
#     event = pygame.event.wait()

#     if event.type == pygame.QUIT:
#         break

#     if event.type == pygame.USEREVENT:
#         screen.fill(pygame.Color("white"))
# frame = (frame + 1) % len(frames)
# image = frames[frame]

#         bounds = image.get_rect()
#         bounds.center = pygame.mouse.get_pos()

#         screen.blit(background, [0, 0])
#         screen.blit(image, bounds)

#         pygame.display.flip()

# pygame.quit()
