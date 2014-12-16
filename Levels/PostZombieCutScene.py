from Level import Level
from ZombieCutScene import ZombieCutScene
import pygame
from Globals import Globals


class PostZombieCutScene(Level):
    SUBTITLE_TEXT = 'You are disoriented'
    SUBTITLE_LOOPS = 5
    MUSIC_PATH = 'maze.mp3'

    def __init__(self):
        super(PostZombieCutScene, self).__init__(
            ZombieCutScene.DEF_NAME,
            ZombieCutScene.MAP_NAME, music_path=PostZombieCutScene.MUSIC_PATH,
            should_fade_in=False
        )
        self.show_subtitle(PostZombieCutScene.SUBTITLE_TEXT,
                           PostZombieCutScene.SUBTITLE_LOOPS)
