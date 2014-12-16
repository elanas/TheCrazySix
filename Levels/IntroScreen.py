from Level import Level
from asset_loader import AssetLoader
from Globals import Globals
import Menu
import pygame


class IntroScreen(Level):
    # LOADER = None
    DEF_NAME = "map_def.txt"
    MAP_NAME = "intro_screen.txt"
    INIT_SOUND_PATH = "intro_sound.ogg"
    BACKGROUND_SOUND_PATH = "intro_level.ogg"
    SUBTITLE_TEXT = "Climb the stairs to skip"

    def __init__(self, mid=0):
        super(IntroScreen, self).__init__(
            IntroScreen.DEF_NAME,
            IntroScreen.MAP_NAME,
            init_music_path=IntroScreen.INIT_SOUND_PATH,
            music_path=IntroScreen.BACKGROUND_SOUND_PATH,
            music_loops=0,
            has_timer=False,
            mid=mid)

        # self.second_sound = self.loader.load_sound(IntroScreen.SECOND_SOUND_NAME)
        self.show_subtitle(IntroScreen.SUBTITLE_TEXT)

    # def got_current_state(self):
    #     super(IntroScreen, self).got_current_state()
    #     if self.first_occur:

    #     else:
    #         self.stop_subtitle()

    # def start_music(self):
    #     if self.first_occur:
    #         self.show_subtitle(IntroScreen.SUBTITLE_TEXT)
    #     else:
    #         self.stop_subtitle()
    #     super(IntroScreen, self).start_music()

    # def pause_music(self):
    #     if self.channel:
    #         self.channel.pause()
    #         self.start_on_stop = True

    # def resume_music(self):
    #     if self.channel:
    #         self.channel.unpause()
    #         self.start_on_stop = True

    # def stop_music(self):
    #     if self.channel:
    #         self.channel.fadeout(Level.SOUND_FADE_TIME)
    #         self.channel = None
    #         self.start_on_stop = False
    #         self.music_handle = self.second_sound
    #         self.music_loops = -1
