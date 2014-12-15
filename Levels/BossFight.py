import pygame
from Level import Level
from TileSystem.TileType import TileType
from Player import Player


class BossLevel(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'boss.txt'
    SUBTITLE_TEXT = 'Find the antidote'
    SUBTITLE_LOOPS = 3
    MUSIC_PATH = 'syringe_level.ogg'

    def __init__(self):
        super(BossLevel, self).__init__(
            BossLevel.DEF_NAME, BossLevel.MAP_NAME,
            music_path=BossLevel.MUSIC_PATH)
        self.show_subtitle(
            BossLevel.SUBTITLE_TEXT,
            BossLevel.SUBTITLE_LOOPS
        )