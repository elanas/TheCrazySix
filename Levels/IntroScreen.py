from Level import Level
from asset_loader import AssetLoader
from Globals import Globals
import Menu
import pygame


class IntroScreen(Level):
    # LOADER = None
    DEF_NAME = "map_def.txt"
    MAP_NAME = "intro_screen.txt"
    SOUND_NAME = "intro_sound.ogg"
    SECOND_SOUND_NAME = "intro_level.ogg"
    SUBTITLE_TEXT = "Climb the stairs to skip"

    def __init__(self):
        super(IntroScreen, self).__init__(IntroScreen.DEF_NAME,
                                          IntroScreen.MAP_NAME,
                                          music_path=IntroScreen.SOUND_NAME,
                                          music_loops=0,
                                          has_timer=False)
        self.first_occur = True
        self.switched_sound = False
        self.second_sound = self.loader.load_sound(IntroScreen.SECOND_SOUND_NAME)
        self.start_on_stop = True

    def got_current_state(self):
        super(IntroScreen, self).got_current_state()
        if self.first_occur:
            self.show_subtitle(IntroScreen.SUBTITLE_TEXT)
        else:
            self.stop_subtitle()

    def start_music(self):
        if self.channel or self.music_handle is None:
            return
        self.channel = self.music_handle.play(
            loops=self.music_loops, fade_ms=Level.SOUND_FADE_TIME)
        self.channel.set_endevent(Level.MUSIC_END_ID)
        self.start_on_stop = True

    def pause_music(self):
        if self.channel:
            self.channel.pause()
            self.start_on_stop = True

    def resume_music(self):
        if self.channel:
            self.channel.unpause()
            self.start_on_stop = True

    def stop_music(self):
        if self.channel:
            self.channel.fadeout(Level.SOUND_FADE_TIME)
            self.channel = None
            self.start_on_stop = False
            self.music_handle = self.second_sound
            self.music_loops = -1

    def handle_raw_event(self, event):
        if event.type == Level.MUSIC_END_ID and not self.switched_sound:
            self.switched_sound = True
            self.stop_subtitle()
            self.music_handle = self.second_sound
            self.music_loops = -1
            if self.start_on_stop:
                self.stop_music()
                self.start_music()
        else:
            super(IntroScreen, self).handle_raw_event(event)
