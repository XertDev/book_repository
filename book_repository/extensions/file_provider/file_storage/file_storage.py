import abc
from werkzeug.security import safe_join


class FileStorage(abc.ABC):
	@abc.abstractmethod
	def __init__(self, app):
		self._prefix = app.config["FILE_PROVIDER_PREFIX"]

	@abc.abstractmethod
	def exists(self, path: str):
		pass

	@abc.abstractmethod
	def save(self, path: str, payload):
		pass

	@abc.abstractmethod
	def load(self, path: str):
		pass

	def full_path(self, path):
		return safe_join(self._prefix, path)
