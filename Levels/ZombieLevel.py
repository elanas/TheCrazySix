import pygame
from Level import Level


class ZombieLevel(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'zombie_level.txt'
    SUBTITLE_TEXT = 'Use the attack key to defeat the other participants'
    SUBTITLE_LOOPS = 3
    VOICE_OVER = "transition2.ogg"
    MUSIC_PATH = 'zombie_level.ogg'

    def __init__(self, mid=0):
        super(ZombieLevel, self).__init__(
            ZombieLevel.DEF_NAME,
            ZombieLevel.MAP_NAME,
            init_music_path=ZombieLevel.VOICE_OVER,
            music_path=ZombieLevel.MUSIC_PATH, mid=mid)

        self.show_subtitle(
            ZombieLevel.SUBTITLE_TEXT,
            ZombieLevel.SUBTITLE_LOOPS
        )
