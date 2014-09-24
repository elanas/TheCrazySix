from os import path
import pygame


class AssetLoader():
    pygame.init()  # safe to call multiple times
    loaded_images = dict()
    loaded_sounds = dict()
    color_key = (255, 0, 255)

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

    def load_spritesheet_alpha(self, img_path, num_rows, num_cols):
        images = []
        sheet = self.load_image_alpha(img_path)
        img_height = sheet.get_height() / num_rows
        img_width = sheet.get_width() / num_cols
        for curr_row in range(num_rows):
            start_y = img_height * curr_row
            for curr_col in range(num_cols):
                start_x = img_width * curr_col
                surf = pygame.Surface((img_width, img_height), pygame.SRCALPHA, 32).convert_alpha()
                surf.blit(sheet, (0, 0), (start_x, start_y, img_width, img_height))
                images.append(surf)
        return images
