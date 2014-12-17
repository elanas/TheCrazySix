import pygame
from Level import Level
from TileSystem.TileType import TileType
from Player import Player


class SyringeLevel(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'dodge.txt'
    SUBTITLE_TEXT = 'Watch out for syringes'
    SUBTITLE_LOOPS = 3
    VOICE_OVER = 'transition1.ogg'
    MUSIC_PATH = 'syringe_level.ogg'

    def __init__(self, mid=0):
        super(SyringeLevel, self).__init__(
            SyringeLevel.DEF_NAME,
            SyringeLevel.MAP_NAME,
            init_music_path=SyringeLevel.VOICE_OVER,
            music_path=SyringeLevel.MUSIC_PATH, mid=mid)

        self.show_subtitle(
            SyringeLevel.SUBTITLE_TEXT,
            SyringeLevel.SUBTITLE_LOOPS
        )
