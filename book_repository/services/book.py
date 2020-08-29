from sqlalchemy import exc

from ..models import BookPermission, Book, User
from ..login_manager.permissions import admin_permission


def get_book_by_id(id: int):
	try:
		return Book.query\
			.filter_by(id=id)\
			.first()
	except exc.SQLAlchemyError:
		return None


def get_latest_user_visible(user_id, limit: int = 4):
	try:
		user = User.query.filter_by(id=user_id).first()
		if not user:
			return []
		if user.is_admin():
			return Book.query\
				.order_by(Book.last_modified.desc())\
				.limit(limit)\
				.all()
		else:
			# todo: optimalization
			accessible = BookPermission.query\
				.with_entities(BookPermission.book_id)\
				.filter_by(user_id=user_id)\
				.all()

			accessible_id = [permission.book_id for permission in accessible]

			return Book.query\
				.where(Book.id.in_(accessible_id))\
				.order_by(Book.last_modified.desc())\
				.limit(limit)\
				.all()
	except exc.SQLAlchemyError as e:
		return []
