from sqlalchemy import exc
from flask import abort
from werkzeug.security import safe_join

from ..models import BookPermission, Book, User, Data


def get_book_cover_path(id: int):
	try:
		book = Book.query\
			.filter_by(id=id)\
			.first()

		if not book or not book.has_cover:
			return None

		return safe_join(book.path, "cover.jpg")
	except exc.SQLAlchemyError:
		abort(500)

def get_book_file_path(id: int, type: str):
	try:
		data = Data.query\
			.filter_by(book=id, format=type)\
			.first()
	except exc.SQLAlchemyError:
		abort(500)

	if not data or not data.linked_book:
		return None

	filename = data.name
	extension = type.lower()
	base_path = data.linked_book.path

	return safe_join(base_path, "{}.{}".format(filename, extension))


def get_book_by_id(id: int):
	try:
		return Book.query\
			.filter_by(id=id)\
			.first()
	except exc.SQLAlchemyError:
		abort(500)


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
		abort(500)
