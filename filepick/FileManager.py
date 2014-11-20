from os import listdir
from os.path import isfile, join, isdir, splitext

class FileManager(object):

	def __init__(self, path='', file_ext=None):
		if not isdir(path):
			raise IOError('The directory path given does not exist.')
		self.path = path
		self.file_ext = file_ext
		if not self.file_ext.startswith("."):
			self.file_ext = '.' + self.file_ext

	def get_files(self, strip_ext=False):
		files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
		if self.file_ext is not None:
			files = [f for f in files if f.lower().endswith(self.file_ext)]
		if strip_ext:
			files = [splitext(f)[0] for f in files]
		return files

	def file_exists(self, file_path):
		if self.file_ext is not None and not file_path.lower().endswith(self.file_ext):
			file_path += self.file_ext
		return isfile(join(self.path, file_path))
