import pygame
from Level import Level


class ZombieLevel(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'zombie_level.txt'

    def __init__(self):
        super(ZombieLevel, self).__init__(
            ZombieLevel.DEF_NAME, ZombieLevel.MAP_NAME)
