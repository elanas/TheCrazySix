import os
import pygame
import math

from Character import Character
from asset_loader import AssetLoader
from Globals import Globals
from FileManager import FileManager


class Player(Character):
    COIN_FACTOR = 10000
    STAIR_OFFSET = 20
    ACTION_OFFSET = 30
    MOVE_VELOCITY = 200
    SECONDS_TO_FULL_SPEED = .5
    ACCELERATION = MOVE_VELOCITY / SECONDS_TO_FULL_SPEED
    SOUND_PATH = "collision_sound.ogg"
    ATTACK_SOUND_PATH = "attack.ogg"
    INDEX_DOWN = 0
    INDEX_LEFT = 1
    INDEX_UP = 2
    INDEX_RIGHT = 3
    still_images = [None, None, None, None]
    walking_images = [None, None, None, None]
    punching_images = [None, None, None, None]
    hitSound = None
    attackSound = None
    loader = AssetLoader("images", "sounds")
    WALK_ANIM_TIME = .05
    ACCEL_ANIM_TIME = .2
    STILL_ANIM_TIME = .5
    PUNCH_ANIM_TIME = .05
    BLINK_SPEED = .1
    TOTAL_BLINK_TIME = .5
    WALKING_PATH = os.path.join('images', 'main_character')
    PREFIX_PATH = os.path.join('main_character')
    WALKING_DOWN_PATH = 'walking_down'
    WALKING_UP_PATH = 'walking_up'
    WALKING_LEFT_PATH = 'walking_left'
    WALKING_RIGHT_PATH = 'walking_right'
    PUNCHING_DOWN_PATH = 'punching_down'
    PUNCHING_UP_PATH = 'punching_up'
    PUNCHING_LEFT_PATH = 'punching_left'
    PUNCHING_RIGHT_PATH = 'punching_right'
    PUNCH_INTERVAL = .5
    PUNCH_RECT_PERCENT = .7

    def __init__(self, w, h, x, y):
        super(Player, self).__init__(w, h, x, y)
        self.empty_image = pygame.Surface((1, 1)).convert()
        self.loadResources()
        self.image = Player.still_images[Player.INDEX_UP][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = Player.INDEX_UP
        self.is_moving = False
        self.velocity = 0
        self.cycle = -1
        self.time_elapsed = 0
        self.anim_time = Player.STILL_ANIM_TIME
        self.proper_image = None
        self.blinking = False
        self.blinking_time = 0
        self.total_blinking_time = 0
        self.last_sound_time = 0.0
        self.punching = False
        self.pre_attack_rect = self.rect
        self.since_punch = 0
        self.last_d = self.direction

    def stop_and_set_direction(self, direction):
        self.velocity = 0
        self.direction = direction
        self.anim_time = Player.STILL_ANIM_TIME
        self.time_elapsed = Player.STILL_ANIM_TIME
        self.cycle = 0
        self.is_moving = False
        self.image = Player.still_images[self.direction][self.cycle]

    def update(self, time, camera=None):
        self.updateVelocity(time)
        self.time_elapsed += time
        self.since_punch += time
        if self.time_elapsed >= self.anim_time:
            if self.punching:
                self.update_punch()
            elif self.velocity == 0:
                self.cycle = (self.cycle + 1) % \
                             (len(Player.still_images[self.direction]))
                self.image = Player.still_images[self.direction][self.cycle]
                old_rect = self.rect
                self.rect = self.image.get_rect()
                self.rect.center = old_rect.center
            else:
                self.cycle = (self.cycle + 1) % \
                             (len(Player.walking_images[self.direction]))
                self.image = Player.walking_images[self.direction][self.cycle]
                old_rect = self.rect
                self.rect = self.image.get_rect()
                self.rect.center = old_rect.center
            self.time_elapsed = 0
        if self.velocity > 0:
            self.move(time)
        self.update_blinking(time)
        if not self.punching:
            self.checkCollisions(camera, self.last_d)
        self.last_d = self.direction

    def update_punch(self):
        self.cycle += 1
        if self.cycle >= len(Player.punching_images[self.direction]):
            self.end_punch()
            return
        self.image = Player.punching_images[self.direction][self.cycle]
        old_rect = self.rect
        self.rect = self.image.get_rect()
        self.rect.center = old_rect.center
        if self.direction == Player.INDEX_DOWN:
            self.rect.top = old_rect.top
        elif self.direction == Player.INDEX_UP:
            self.rect.bottom = old_rect.bottom
        elif self.direction == Player.INDEX_LEFT:
            self.rect.right = old_rect.right
        elif self.direction == Player.INDEX_RIGHT:
            self.rect.left = old_rect.left

    def handle_attack(self):
        if self.punching or self.since_punch < Player.PUNCH_INTERVAL:
            return
        Player.attackSound.play()
        self.since_punch = 0
        self.anim_time = Player.PUNCH_ANIM_TIME
        self.time_elapsed = self.anim_time
        self.cycle = 0
        self.is_moving = False
        self.velocity = 0
        self.image = Player.punching_images[self.direction][self.cycle]
        self.pre_attack_rect = self.rect
        self.rect = self.image.get_rect()
        self.rect.center = self.pre_attack_rect.center
        self.punching = True

    def end_punch(self):
        self.cycle = 0
        self.time_elapsed = 0
        if self.velocity == 0:
            self.anim_time = Player.STILL_ANIM_TIME
            self.image = Player.still_images[self.direction][self.cycle]
        else:
            self.anim_time = Player.WALK_ANIM_TIME
            self.image = Player.walking_images[self.direction][self.cycle]
        self.rect = self.image.get_rect()
        self.rect.center = self.pre_attack_rect.center
        self.punching = False

    def update_blinking(self, time):
        if not self.blinking:
            return
        if self.image is not self.empty_image:
            self.proper_image = self.image
        self.total_blinking_time += time
        self.blinking_time += time
        if self.blinking_time >= Player.BLINK_SPEED:
            self.blinking_time = 0
            if self.image is self.empty_image:
                self.image = self.proper_image
            else:
                self.image = self.empty_image
        if self.total_blinking_time >= Player.TOTAL_BLINK_TIME:
            self.total_blinking_time = 0
            self.blinking_time = 0
            self.blinking = False

    def updateVelocity(self, time):
        if self.velocity == Player.MOVE_VELOCITY:
            self.anim_time = Player.WALK_ANIM_TIME
        if self.is_moving and self.velocity < Player.MOVE_VELOCITY:
            self.velocity = min(self.velocity + Player.ACCELERATION
                                * time, Player.MOVE_VELOCITY)
            if self.velocity == Player.MOVE_VELOCITY:
                self.anim_time = Player.WALK_ANIM_TIME
                self.time_elapsed = Player.WALK_ANIM_TIME
        elif not self.is_moving and self.velocity > 0:
            self.velocity = max(self.velocity - Player.ACCELERATION * time, 0)
            if self.velocity == 0:
                self.anim_time = Player.STILL_ANIM_TIME
                self.time_elapsed = Player.STILL_ANIM_TIME

    def loadResources(self):
        if Player.still_images[Player.INDEX_UP] is None:
            Player.still_images[Player.INDEX_UP] = \
                Player.loader.load_spritesheet_alpha("main_still_up.png", 1, 2)
        if Player.still_images[Player.INDEX_DOWN] is None:
            Player.still_images[Player.INDEX_DOWN] = \
                Player.loader.load_spritesheet_alpha(
                    "main_still_down.png", 1, 2)
        if Player.still_images[Player.INDEX_LEFT] is None:
            Player.still_images[Player.INDEX_LEFT] = \
                Player.loader.load_spritesheet_alpha(
                    "main_still_left.png", 2, 1)
        if Player.still_images[Player.INDEX_RIGHT] is None:
            Player.still_images[Player.INDEX_RIGHT] = \
                Player.loader.load_spritesheet_alpha(
                    "main_still_right.png", 2, 1)

        if Player.walking_images[Player.INDEX_DOWN] is None:
            path = os.path.join(Player.WALKING_PATH, Player.WALKING_DOWN_PATH)
            prefix_path = os.path.join(Player.PREFIX_PATH, Player.WALKING_DOWN_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            Player.walking_images[Player.INDEX_DOWN] = \
                Player.loader.load_images(fM.get_files(prefix_path=prefix_path))
        if Player.walking_images[Player.INDEX_UP] is None:
            path = os.path.join(Player.WALKING_PATH, Player.WALKING_UP_PATH)
            prefix_path = os.path.join(Player.PREFIX_PATH, Player.WALKING_UP_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            Player.walking_images[Player.INDEX_UP] = \
                Player.loader.load_images(fM.get_files(prefix_path=prefix_path))
        if Player.walking_images[Player.INDEX_LEFT] is None:
            path = os.path.join(Player.WALKING_PATH, Player.WALKING_LEFT_PATH)
            prefix_path = os.path.join(Player.PREFIX_PATH, Player.WALKING_LEFT_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            Player.walking_images[Player.INDEX_LEFT] = \
                Player.loader.load_images(fM.get_files(prefix_path=prefix_path))
        if Player.walking_images[Player.INDEX_RIGHT] is None:
            path = os.path.join(Player.WALKING_PATH, Player.WALKING_RIGHT_PATH)
            prefix_path = os.path.join(Player.PREFIX_PATH, Player.WALKING_RIGHT_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            Player.walking_images[Player.INDEX_RIGHT] = \
                Player.loader.load_images(fM.get_files(prefix_path=prefix_path))

        if Player.punching_images[Player.INDEX_DOWN] is None:
            path = os.path.join(Player.WALKING_PATH, Player.PUNCHING_DOWN_PATH)
            prefix_path = os.path.join(Player.PREFIX_PATH, Player.PUNCHING_DOWN_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            Player.punching_images[Player.INDEX_DOWN] = \
                Player.loader.load_images(fM.get_files(prefix_path=prefix_path))
        if Player.punching_images[Player.INDEX_UP] is None:
            path = os.path.join(Player.WALKING_PATH, Player.PUNCHING_UP_PATH)
            prefix_path = os.path.join(Player.PREFIX_PATH, Player.PUNCHING_UP_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            Player.punching_images[Player.INDEX_UP] = \
                Player.loader.load_images(fM.get_files(prefix_path=prefix_path))
        if Player.punching_images[Player.INDEX_LEFT] is None:
            path = os.path.join(Player.WALKING_PATH, Player.PUNCHING_LEFT_PATH)
            prefix_path = os.path.join(Player.PREFIX_PATH, Player.PUNCHING_LEFT_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            Player.punching_images[Player.INDEX_LEFT] = \
                Player.loader.load_images(fM.get_files(prefix_path=prefix_path))
        if Player.punching_images[Player.INDEX_RIGHT] is None:
            path = os.path.join(Player.WALKING_PATH, Player.PUNCHING_RIGHT_PATH)
            prefix_path = os.path.join(Player.PREFIX_PATH, Player.PUNCHING_RIGHT_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            Player.punching_images[Player.INDEX_RIGHT] = \
                Player.loader.load_images(fM.get_files(prefix_path=prefix_path))
        if Player.hitSound is None:
            Player.hitSound = Player.loader.load_sound(Player.SOUND_PATH)
        if Player.attackSound is None:
            Player.attackSound = Player.loader.load_sound(Player.ATTACK_SOUND_PATH)

    def keyPressed(self, keyCode):
        if keyCode == pygame.K_UP:
            self.last_d = self.direction
            self.direction = Player.INDEX_UP
            if not self.is_moving:
                self.anim_time = Player.ACCEL_ANIM_TIME
                self.time_elapsed = Player.ACCEL_ANIM_TIME
            self.is_moving = True
        elif keyCode == pygame.K_DOWN:
            self.last_d = self.direction
            self.direction = Player.INDEX_DOWN
            if not self.is_moving:
                self.anim_time = Player.ACCEL_ANIM_TIME
                self.time_elapsed = Player.ACCEL_ANIM_TIME
            self.is_moving = True
        elif keyCode == pygame.K_LEFT:
            self.last_d = self.direction
            self.direction = Player.INDEX_LEFT
            if not self.is_moving:
                self.anim_time = Player.ACCEL_ANIM_TIME
                self.time_elapsed = Player.ACCEL_ANIM_TIME
            self.is_moving = True
        elif keyCode == pygame.K_RIGHT:
            self.last_d = self.direction
            self.direction = Player.INDEX_RIGHT
            if not self.is_moving:
                self.anim_time = Player.ACCEL_ANIM_TIME
                self.time_elapsed = Player.ACCEL_ANIM_TIME
            self.is_moving = True

    def keyReleased(self, keyCode):
        if keyCode == pygame.K_UP and self.direction == Player.INDEX_UP:
            self.is_moving = False
            self.anim_time = Player.ACCEL_ANIM_TIME
            self.time_elapsed = Player.ACCEL_ANIM_TIME
        elif keyCode == pygame.K_DOWN and self.direction == Player.INDEX_DOWN:
            self.is_moving = False
            self.anim_time = Player.ACCEL_ANIM_TIME
            self.time_elapsed = Player.ACCEL_ANIM_TIME
        elif keyCode == pygame.K_LEFT and self.direction == Player.INDEX_LEFT:
            self.is_moving = False
            self.anim_time = Player.ACCEL_ANIM_TIME
            self.time_elapsed = Player.ACCEL_ANIM_TIME
        elif keyCode == pygame.K_RIGHT \
                and self.direction == Player.INDEX_RIGHT:
            self.is_moving = False
            self.anim_time = Player.ACCEL_ANIM_TIME
            self.time_elapsed = Player.ACCEL_ANIM_TIME

    def getDirection(self):
        return self.direction

    def getMoveNormalized(self):
        if self.direction == Player.INDEX_UP:
            return 0, -1
        elif self.direction == Player.INDEX_DOWN:
            return 0, 1
        elif self.direction == Player.INDEX_LEFT:
            return -1, 0
        elif self.direction == Player.INDEX_RIGHT:
            return 1, 0

    def move(self, time):
        norm_delta = self.getMoveNormalized()
        dist_delta = [x * time * self.velocity for x in norm_delta]
        super(Player, self).move(dist_delta[0], dist_delta[1])

    def play_sound(self):
        current_time = pygame.time.get_ticks() / 1000
        if self.last_sound_time == 0.0 or \
                current_time - Player.hitSound.get_length() >= \
                self.last_sound_time:
            self.last_sound_time = current_time
            Player.hitSound.play()

    def show_damage(self):
        self.blinking = True
        self.play_sound()

    def get_punching_rect(self):
        r = None
        if self.direction == Player.INDEX_DOWN:
            r = self.rect.inflate(
                -self.rect.width * Player.PUNCH_RECT_PERCENT, 0)
            r.move_ip(0, int(self.rect.height / 2) + 10)
        elif self.direction == Player.INDEX_UP:
            r = self.rect.inflate(
                -self.rect.width * Player.PUNCH_RECT_PERCENT, 0)
            r.move_ip(0, -int(self.rect.height / 2) - 10)
        elif self.direction == Player.INDEX_RIGHT:
            r = self.rect.inflate(
                0, -self.rect.height * Player.PUNCH_RECT_PERCENT)
            r.move_ip(int(self.rect.width / 2) + 10, 0)
        elif self.direction == Player.INDEX_LEFT:
            r = self.rect.inflate(
                0, -self.rect.height * Player.PUNCH_RECT_PERCENT)
            r.move_ip(-int(self.rect.width / 2) - 10, 0)
        return r
