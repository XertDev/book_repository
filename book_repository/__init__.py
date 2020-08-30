from flask import Flask


def create_app(config=None):
	app = Flask(
		__name__,
		instance_relative_config=True,
		template_folder="templates"
	)

	app.config.from_mapping(
		SECRET_KEY="dev"
	)

	app.config.from_object("config")
	app.config.from_pyfile("config.py", silent=True)

	app.config["SQLALCHEMY_DATABASE_URI"] = app.config["APP_DB"]
	app.config["SQLALCHEMY_BINDS"] = {
		"calibre": app.config["CALIBRE_DB"]
	}

	from .db import db
	from . import models
	db.init_app(app)

	from .login_manager.principal import principal
	principal.init_app(app)

	from .login_manager import login_manager
	login_manager.init_app(app)

	from .file_provider import file_provider
	file_provider.init_app(app)

	from .auth import auth as auth_blueprint
	from .dashboard import dashboard as dashboard_blueprint
	from .book import book as book_blueprint
	app.register_blueprint(auth_blueprint)
	app.register_blueprint(dashboard_blueprint)
	app.register_blueprint(book_blueprint)

	return app
