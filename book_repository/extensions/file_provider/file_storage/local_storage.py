import errno
import os

from .file_storage import FileStorage


class LocalStorage(FileStorage):
	def __init__(self, app):
		super().__init__(app)

	def exists(self, path: str):
		return os.path.exists(self.full_path(path))

	def save(self, path: str, payload):
		path = self.full_path(path)

		dirname = os.path.dirname(path)

		if not os.path.exists(dirname):
			try:
				os.makedirs(dirname)
			except OSError as e:
				if e.errno != errno.EEXIST:
					raise

		if not os.path.isdir(dirname):
			raise IOError('Not a directory')

		try:
			file = open(path, "wb")
			file.write(payload)
			file.close()
		except IOError:
			raise RuntimeError("Failed to save file")

	def load(self, path: str):
		try:
			file = open(self.full_path(path), "rb")
			data = file.read()
		except IOError:
			raise RuntimeError("Failed to load file {}".format(path))

		return data
