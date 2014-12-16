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

    def __init__(self):
        super(SyringeLevel, self).__init__(SyringeLevel.DEF_NAME, 
                                           SyringeLevel.MAP_NAME,
                                           music_path=SyringeLevel.VOICE_OVER,
                                           music_loops=0)
        self.first_occur = True
        self.switched_sound = False
        self.second_sound = self.loader.load_sound(SyringeLevel.MUSIC_PATH)
        self.start_on_stop = True

        self.show_subtitle(
            SyringeLevel.SUBTITLE_TEXT,
            SyringeLevel.SUBTITLE_LOOPS
        )
