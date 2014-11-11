from Level import Level
from SyringeLevel import SyringeLevel
from asset_loader import AssetLoader
from Globals import Globals
import Menu
import pygame


class IntroScreen(Level):
    LOADER = None
    DEF_NAME = "map_def.txt"
    MAP_NAME = "intro_screen.txt"
    SOUND_NAME = "intro_sound.ogg"
    SUBTITLE_TEXT = "Climb the stairs to skip"

    def __init__(self):
        super(IntroScreen, self).__init__(IntroScreen.DEF_NAME,
                                          IntroScreen.MAP_NAME,
                                          has_timer=False)
        self.audio = None
        if IntroScreen.LOADER is None:
            IntroScreen.LOADER = AssetLoader("images", "sounds")
        self.played_intro = False
        if not Globals.INTRO_SOUND_PLAYED:
            self.show_subtitle(IntroScreen.SUBTITLE_TEXT)

    def got_current_state(self):
        super(IntroScreen, self).got_current_state()
        self.start_music()

    def handle_stair_up(self):
        self.stop_music()
        super(IntroScreen, self).handle_stair_up()

    def handle_escape(self):
        self.stop_music()
        super(IntroScreen, self).handle_escape()

    def start_music(self):
        if not Globals.INTRO_SOUND_PLAYED:
            self.played_intro = True
            Globals.INTRO_SOUND_PLAYED = True
            self.audio = IntroScreen.LOADER.load_sound(IntroScreen.SOUND_NAME)
            self.audio.play()

    def stop_music(self):
        if self.audio is not None:
            self.audio.stop()
