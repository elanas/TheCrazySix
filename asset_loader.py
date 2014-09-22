from os import path
import pygame


class AssetLoader():
    pygame.init()  # safe to call multiple times
    loaded_images = dict()
    loaded_sounds = dict()

    def __init__(self, image_path_start="", sound_path_start=""):
        self.image_path_start = image_path_start
        self.sound_path_start = sound_path_start

    def load_image(self, img_path):
        img_path = path.abspath(path.join(self.image_path_start, img_path))
        try:
            return AssetLoader.loaded_images[img_path]
        except KeyError:
            img = pygame.image.load(img_path).convert()
            AssetLoader.loaded_images[img_path] = img
            return img

    def load_image_alpha(self, img_path):
        img_path = path.abspath(path.join(self.image_path_start, img_path))
        try:
            return AssetLoader.loaded_images[img_path]
        except KeyError:
            img = pygame.image.load(img_path).convert_alpha()
            AssetLoader.loaded_images[img_path] = img
            return img

    def unload_image(self, img_path):
        img_path = path.abspath(path.join(self.image_path_start, img_path))
        try:
            del AssetLoader.loaded_images[img_path]
        except KeyError:
            pass

    def load_sound(self, sound_path):
        sound_path = path.abspath(path.join(self.sound_path_start, sound_path))
        try:
            return AssetLoader.loaded_sounds[sound_path]
        except KeyError:
            sound = pygame.mixer.Sound(sound_path)
            AssetLoader.loaded_sounds[sound_path] = sound
            return sound

    def unload_sound(self, sound_path):
        sound_path = path.abspath(path.join(self.sound_path_start, sound_path))
        try:
            del AssetLoader.loaded_sounds[sound_path]
        except KeyError:
            pass
