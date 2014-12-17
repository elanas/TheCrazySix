from os import listdir, makedirs
from os.path import isfile, join, isdir, splitext
import re


class FileManager(object):

    def __init__(self, path='', file_ext=None, create_dir=True):
        if not isdir(path):
            if create_dir:
                makedirs(path)
            else:
                raise Exception('The path "' + path + '" does not exist.')
        self.path = path
        self.file_ext = file_ext
        if file_ext is not None and not self.file_ext.startswith("."):
            self.file_ext = '.' + self.file_ext

    def get_files(self, strip_ext=False, sort=True, prefix_path=None):
        files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        if self.file_ext is not None:
            files = [f for f in files if f.lower().endswith(self.file_ext)]
        if strip_ext:
            files = [splitext(f)[0] for f in files]
        if sort:
            files.sort(key=FileManager.natural_key)
        if prefix_path is not None:
            files = [join(prefix_path, f) for f in files]
        return files

    @staticmethod
    def natural_key(text):
        # method from http://stackoverflow.com/a/5967539
        return [FileManager.atoi(c) for c in re.split('(\d+)', text)]

    @staticmethod
    def atoi(text):
        return int(text) if text.isdigit() else text

    def file_exists(self, file_path):
        if self.file_ext is not None and \
                not file_path.lower().endswith(self.file_ext):
            file_path += self.file_ext
        return isfile(join(self.path, file_path))

    def fix_ext(self, file_path, file_ext=None):
        if file_ext is None:
            if self.file_ext is None:
                raise Exception('You must provide or set a file extension.')
            file_ext = self.file_ext
        return file_path if file_path.endswith(file_ext) else \
            file_path + file_ext
