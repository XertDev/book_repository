from sqlalchemy import exc, and_
from flask import abort

from ..models import PushEmail
from ..db import db


def add_push_email(user_id: int, email: str):
	try:
		push_email = PushEmail(email=email, user_id=user_id)
		db.session.add(push_email)
		db.session.commit()

	except exc.SQLAlchemyError:
		abort(500)


def del_push_email(user_id, email_id):
	try:
		email = PushEmail.query.filter(
			and_(
				PushEmail.id == email_id,
				PushEmail.user_id == user_id
			)
		).first()

		if not email:
			abort(403)

		db.session.delete(email)
		db.session.commit()

	except exc.SQLAlchemyError:
		abort(500)
