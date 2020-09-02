from sqlalchemy import exc, exists, and_

from ..models import BookPermission, User
from ..db import db


def get_user_book_permission_type(user_id: int, book_id: int):
	try:
		book_permission: BookPermission = db.session.query(BookPermission)\
			.filter_by(user_id=user_id, book_id=book_id)\
			.first()
		if not book_permission:
			return None
		return book_permission.type
	except exc.SQLAlchemyError:
		raise RuntimeError


def is_book_visible(user_id: int, book_id: int):
	try:
		user = User.query.filter_by(id=user_id).first()
		if not user:
			return False
		if user.is_admin():
			return True

		return db.session.query(
			exists().where(and_(BookPermission.user_id==user_id, BookPermission.book_id==book_id))).scalar()

	except exc.SQLAlchemyError:
		return False



