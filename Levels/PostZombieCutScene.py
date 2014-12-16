from Level import Level
from ZombieCutScene import ZombieCutScene
import pygame
from Globals import Globals


class PostZombieCutScene(Level):
    SUBTITLE_TEXT = 'You are disoriented'
    SUBTITLE_LOOPS = 5
    VOICE_OVER = 'transition3.ogg'
    MUSIC_PATH = 'maze.ogg'

    def __init__(self, id=0):
        super(PostZombieCutScene, self).__init__(
            ZombieCutScene.DEF_NAME,
            ZombieCutScene.MAP_NAME,
            init_music_path=PostZombieCutScene.VOICE_OVER
            music_path=PostZombieCutScene.MUSIC_PATH,
            should_fade_in=False, id=id
        )
        self.show_subtitle(PostZombieCutScene.SUBTITLE_TEXT,
                           PostZombieCutScene.SUBTITLE_LOOPS)
