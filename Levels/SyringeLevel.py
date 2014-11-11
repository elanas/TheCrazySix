import pygame
from Level import Level


class SyringeLevel(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'dodge.txt'
    SUBTITLE_TEXT = 'Watch out for syringes'

    def __init__(self):
        super(SyringeLevel, self).__init__(
            SyringeLevel.DEF_NAME, SyringeLevel.MAP_NAME)
        self.show_subtitle(SyringeLevel.SUBTITLE_TEXT)
