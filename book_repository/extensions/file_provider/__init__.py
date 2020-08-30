from importlib import import_module

from flask import current_app

from .file_storage.file_storage import FileStorage

KNOWN_STORAGES = {
	"LOCAL": "local_storage"
}


class _FileProviderState:
	def __init__(self, provider):
		self.provider = provider


class FileProvider:
	_storage = None

	def __init__(self, app=None):
		self.app = app
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		app.config.setdefault("FILE_PROVIDER_TYPE", "LOCAL")
		app.config.setdefault("FILE_PROVIDER_PREFIX", "library")

		app.extensions["file_provider"] = _FileProviderState(self)

		if not self._storage:
			self._init_storage(app)

	@staticmethod
	def check_storage_config(app, storage):
		if hasattr(storage, "REQUIRED_CONFIG"):
			for name in storage.REQUIRED_CONFIG:
				if not app.config.get(name):
					raise RuntimeError("{} must be set".format(name))

	def _init_storage(self, app):
		provider_type = app.config["FILE_PROVIDER_TYPE"]

		if provider_type not in KNOWN_STORAGES:
			raise ValueError("Unknown file provider {}".format(provider_type))

		module_path = ".file_storage.{}".format(KNOWN_STORAGES[provider_type])
		class_name = KNOWN_STORAGES[provider_type]\
			.replace("_", " ")\
			.title()\
			.replace(" ", "")

		module = import_module(module_path, package=__name__)
		if not hasattr(module, class_name):
			raise ImportError("Failed to load storage {}. No implementation found.".format(provider_type))

		storage_class = getattr(module, class_name)

		self.check_storage_config(app, storage_class)
		self._storage = storage_class(app)

	def _get_app(self):
		if current_app:
			return current_app._get_current_object()

		if self.app:
			return self.app

		raise RuntimeError(
			"No application found."
			"Either work inside a view function or push an application context"
		)

	@staticmethod
	def _get_state(app):
		assert "file_provider" in app.extensions, (
			"The File provider extension was not registered to the current application."
			"Please make sure to call init_app() first."
		)
		return app.extensions["file_provider"]

	def get_current_storage(self):
		return self._storage

	def get_storage(self) -> FileStorage:
		app = self._get_app()
		state = self._get_state(app)
		return state.provider.get_current_storage()

	def save(self, path: str, payload):
		self.get_storage().save()

	def load(self, path: str):
		return self.get_storage().load(path)

	def exists(self, path: str):
		return self.get_storage().exists(path)
