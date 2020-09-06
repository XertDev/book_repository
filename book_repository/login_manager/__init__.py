from flask import url_for
from flask_login import LoginManager

from ..db import db as _db
from ..models import User as _User

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
	return _db.session.query(_User).filter_by(id=user_id).first()
