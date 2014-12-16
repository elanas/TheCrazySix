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
                                           music_path=SyringeLevel.VOICE_OVER)
        self.first_occur = True
        self.switched_sound = False
        self.second_sound = self.loader.load_sound(SyringeLevel.MUSIC_PATH)
        self.start_on_stop = True

        self.show_subtitle(
            SyringeLevel.SUBTITLE_TEXT,
            SyringeLevel.SUBTITLE_LOOPS
        )

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
            super(SyringeLevel, self).handle_raw_event(event)
