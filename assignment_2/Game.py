# IMPORT THE PYGAME
import pygame
import random

from Player import Player
from Enemy import Enemy
from Globals import Globals

class GameState(object):
    def __init__(self):
        pass
    def render(self):
        pass
    def update(self, time):
        pass
    def event(self, event):
        pass

class Title(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.color = PC.Color("black")
        self.time = 0.0
        Globals.SCREEN.fill(PC.Color("black"))
    def render(self):
        font = PF.Font(None, 64)
        surf = font.render("Unnamed Game!", True, WHITE)
        width, height = surf.get_size()
        screen.blit(surf, (Globals.WIDTH / 2 - width / 2, Globals.HEIGHT / 2 - height / 2 + 64))

        PDI.flip()
 
    def update(self, time):
        self.time += time
    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.RUNNING = False
        elif event.type == PG.KEYDOWN and event.key == PG.K_SPACE:
            Globals.STATE = Menu()

class Menu(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.color = PC.Color("black")
        Globals.SCREEN.fill(PC.Color("black"))
        selection = 0
    
    def render(self):
        font = PF.Font(None, 64)
        surf = font.render("MENU", True, WHITE)
        width, height = surf.get_size()
        screen.blit(surf, (WIDTH / 2 - width / 2, HEIGHT / 2 - height / 2 + 164))


        surf = font.render("Start Game", True, WHITE)
        screen.blit(surf, (WIDTH / 2 - width / 2, HEIGHT / 2 - height / 2 + 64))

        surf = font.render("adjust visual brightness", True, WHITE)
        screen.blit(surf, (WIDTH / 2 - width / 2, HEIGHT / 2 - height / 2 - 36))

        surf = font.render("adjust visual brightness", True, WHITE)
        screen.blit(surf, (WIDTH / 2 - width / 2, HEIGHT / 2 - height / 2 - 136))

        surf = font.render("display high-scores", True, WHITE)
        screen.blit(surf, (WIDTH / 2 - width / 2, HEIGHT / 2 - height / 2 - 236))

        surf = font.render("quit", True, WHITE)
        screen.blit(surf, (WIDTH / 2 - width / 2, HEIGHT / 2 - height / 2 - 336))
        PDI.flip()

    def update(self, time):
        self.time += time

    def event(self, event):
        if event.type == PG.QUIT:
            SYS.exit()
        elif event.type == PG.KEYDOWN and event.key == PG.K_UP:
            if selection != 0:
            	selection -= 1
        elif event.type == PG.KEYDOWN and event.key == PG.K_DOWN:
            if selection != 4:
            	selection += 1
        elif event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            SYS.exit()
        elif event.type == PG.KEYDOWN and event.key == PG.K_SPACE:
            if selection == 0:
            	Globals.STATE = Game()
            if selection == 3:
                Globals.STATE = Score()
            if selection == 4:
            	SYS.exit()

def initialize():
    pygame.init()
    Globals.WIDTH = 700
    Globals.HEIGHT = 500
    Globals.SCREEN = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))
    # Globals.STATE = Title()

def loadGame():
    (width, height) = (Globals.WIDTH, Globals.HEIGHT)
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
                    p.direction = random.randint(0, 3)
            elif event.type == pygame.USEREVENT + 2:
                for p in enemySprites:
                    p.moveRandom()
                if last_key is not None:
                    for p in playerSprites:
                        p.keyPressed(last_key)
            elif event.type == pygame.KEYDOWN:
                last_key = event.key
            elif event.type == pygame.KEYUP:
                last_key = None

        enemySprites.update()
        playerSprites.update()
        Globals.SCREEN.fill((0, 0, 0))
        enemySprites.draw(Globals.SCREEN)
        playerSprites.draw(Globals.SCREEN)
        
        pygame.display.flip()

def main():
    initialize()
    loadGame()
    # pygame.init()
    # (width, height) = (700, 500)
    # screen = pygame.display.set_mode((width, height))
    # running = True
    # enemySprites = pygame.sprite.Group()
    # playerSprites = pygame.sprite.Group()

    # for x in range(13):
    #     enemySprites.add(Enemy(width, height))

    # playerSprites.add(Player(width, height, width / 2, height / 2))

    # # Ideally, each computer object should have a unique timer
    # # for changing direction or other movements
    # # Alternative: Randomizing timer interval per object
    # pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
    # pygame.time.set_timer(pygame.USEREVENT + 2, 20)

    # last_key = None

    # while running:
    #     # handle pygame events
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
    #             running = False
    #         elif event.type == pygame.USEREVENT + 1:
    #             for p in enemySprites:
    #                 p.direction = random.randint(0, 3)
    #         elif event.type == pygame.USEREVENT + 2:
    #             for p in enemySprites:
    #                 p.moveRandom()
    #             if last_key is not None:
    #                 for p in playerSprites:
    #                     p.keyPressed(last_key)
    #         elif event.type == pygame.KEYDOWN:
    #             last_key = event.key
    #         elif event.type == pygame.KEYUP:
    #             last_key = None

    #     enemySprites.update()
    #     playerSprites.update()
    #     screen.fill((0, 0, 0))
    #     enemySprites.draw(screen)
    #     playerSprites.draw(screen)
    #     pygame.display.flip()

if __name__ == '__main__':
    main()


# pygame.init()

# BACKGROUND_IMAGE_NAME = "test.png"

# background = pygame.image.load(BACKGROUND_IMAGE_NAME)
# size = background.get_size()
# screen = pygame.display.set_mode(size)
# # frames_per_second = 24

# # DIVIDE SPRITESHEET
# #rows = 4
# #cols = 4
# #height = spriteSheet.get_height() / rows
# # width = spriteSheet.get_width() / cols
# # frames = []

# # for row in range(rows):
# #     for col in range(cols):
# #         clip = pygame.Rect(col * width, row * height, width, height)
# #         frame = spriteSheet.subsurface(clip)
# #         frames.append(frame)

# # pygame.time.set_timer(pygame.USEREVENT, int(1000 / frames_per_second))

# while True:
#     event = pygame.event.wait()

#     if event.type == pygame.QUIT:
#         break

#     if event.type == pygame.USEREVENT:
#         screen.fill(pygame.Color("white"))
#         # frame = (frame + 1) % len(frames)
#         #image = frames[frame]

#         bounds = image.get_rect()
#         bounds.center = pygame.mouse.get_pos()

#         screen.blit(background, [0, 0])
#         screen.blit(image, bounds)

#         pygame.display.flip()

# pygame.quit()
