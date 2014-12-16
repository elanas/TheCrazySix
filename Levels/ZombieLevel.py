import pygame
from Level import Level


class ZombieLevel(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'zombie_level.txt'
    MUSIC_PATH = 'zombie_level.ogg'

    def __init__(self, id=0):
        super(ZombieLevel, self).__init__(
            ZombieLevel.DEF_NAME, ZombieLevel.MAP_NAME,
            music_path=ZombieLevel.MUSIC_PATH, id=id)
