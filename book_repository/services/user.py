from flask import abort, current_app
from flask_login import login_user
from flask_principal import identity_changed, Identity
from sqlalchemy import exc

from ..db import db
from ..models import User


def authenticate(username: str, password: str) ->bool:
	try:
		user = db.session.query(User)\
			.filter_by(username=username)\
			.first()
		if not user:
			return False
		if not user.check_password(password):
			return False
		login_user(user)
		# access to private - official tutorial info
		identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
		return True
	except exc.SQLAlchemyError:
		abort(500)


