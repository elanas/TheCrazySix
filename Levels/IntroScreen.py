from Level import Level
from SyringeLevel import SyringeLevel
from asset_loader import AssetLoader
from Globals import Globals
import Menu
import pygame


class IntroScreen(Level):
    # LOADER = None
    DEF_NAME = "map_def.txt"
    MAP_NAME = "intro_screen.txt"
    SOUND_NAME = "intro_sound.ogg"
    SUBTITLE_TEXT = "Climb the stairs to skip"

    def __init__(self):
        super(IntroScreen, self).__init__(IntroScreen.DEF_NAME,
                                          IntroScreen.MAP_NAME,
                                          music_path=IntroScreen.SOUND_NAME,
                                          music_loops=0,
                                          has_timer=False)
        self.first_occur = True

    def got_current_state(self):
        super(IntroScreen, self).got_current_state()
        if self.first_occur:
            self.show_subtitle(IntroScreen.SUBTITLE_TEXT)
        else:
            self.stop_subtitle()

    def start_music(self):
        if not Globals.INTRO_SOUND_PLAYED:
            super(IntroScreen, self).start_music()
            Globals.INTRO_SOUND_PLAYED = True

    def handle_raw_event(self, event):
        if event.type == Level.MUSIC_END_ID:
            self.stop_subtitle()
        else:
            super(IntroScreen, self).handle_raw_event(event)
