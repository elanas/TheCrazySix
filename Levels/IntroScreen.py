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
        self.channel = None

    def got_current_state(self):
        super(IntroScreen, self).got_current_state()
        self.start_music()

    def handle_stair_up(self):
        self.stop_music()
        super(IntroScreen, self).handle_stair_up()

    def handle_pause(self):
        self.pause_music()
        super(IntroScreen, self).handle_pause()

    def handle_unpause(self):
        self.resume_music()
        super(IntroScreen, self).handle_unpause()

    def pause_music(self):
        if self.channel:
            self.channel.pause()

    def resume_music(self):
        if self.channel:
            self.channel.unpause()

    def start_music(self):
        if not Globals.INTRO_SOUND_PLAYED:
            self.played_intro = True
            Globals.INTRO_SOUND_PLAYED = True
            self.audio = IntroScreen.LOADER.load_sound(IntroScreen.SOUND_NAME)
            self.channel = self.audio.play()
            self.channel.set_endevent(pygame.USEREVENT)

    def event(self, event):
        if event.type == pygame.USEREVENT:
            self.stop_subtitle()
        else:
            super(IntroScreen, self).event(event)

    def stop_music(self):
        if self.audio is not None:
            self.audio.stop()
