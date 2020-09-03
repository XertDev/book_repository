from flask_login import current_user
from sqlalchemy import exc, and_
from flask import abort
from werkzeug.security import safe_join

from ..models import BookPermission, Book, Data, Author, Language
from ..models.calibre.books_authors_link import books_authors_link
from ..models.calibre.books_languages_link import books_languages_link
from ..models.calibre.books_publishers_link import books_publishers_link


def get_book_cover_path(book_id: int):
	try:
		book = Book.query\
			.with_entities(Book.path, Book.has_cover)\
			.filter_by(id=book_id)\
			.first()

		if not book or not book.has_cover:
			return None

		return safe_join(book.path, "cover.jpg")
	except Exception as e:
		abort(500)


def get_book_file_path(book_id: int, file_format: str):
	try:
		data = Data.query\
			.filter_by(book=book_id, format=file_format)\
			.first()
	except exc.SQLAlchemyError:
		abort(500)

	if not data or not data.linked_book:
		return None

	filename = data.name
	extension = file_format.lower()
	base_path = data.linked_book.path

	return safe_join(base_path, "{}.{}".format(filename, extension))


def get_book_by_id(book_id: int):
	try:
		return Book.query\
			.filter_by(id=book_id)\
			.first()
	except exc.SQLAlchemyError:
		abort(500)


def get_current_user_latest_books(limit: int = 4):
	if current_user.is_admin():
		return get_latest_books(limit)
	else:
		return get_normal_user_latest_books(current_user.id, limit)


def get_latest_books(limit: int):
	return Book.query \
		.order_by(Book.last_modified.desc()) \
		.limit(limit) \
		.all()


def get_normal_user_latest_books(user_id, limit: int = 4):
	try:
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
	except exc.SQLAlchemyError:
		abort(500)


def get_current_user_books_per_author_paginator(author_id, page, page_size):
	if current_user.is_admin():
		return get_books_per_author_paginator(author_id, page, page_size)
	else:
		return get_normal_user_books_per_author_paginator(current_user.id, author_id, page, page_size)


def get_books_per_author_paginator(author_id, page, page_size):
	try:
		books = Book.query\
			.join(Author, Book.authors)\
			.filter(Author.id == author_id)\
			.paginate(page, page_size, False)

		return books

	except exc.SQLAlchemyError:
		abort(500)


def get_normal_user_books_per_author_paginator(user_id, author_id, page, page_size):
	try:
		books = Book.query\
			.with_entities(Book.id)\
			.join(books_authors_link)\
			.filter(books_authors_link.c.author == author_id)

		books_id = [book.id for book in books]

		permissions = BookPermission.query\
			.with_entities(BookPermission.book_id)\
			.where(
				and_(
					BookPermission.book_id.in_(books_id),
					BookPermission.user_id == user_id
				)
			)\
			.all()

		permissions_id = [permission.book_id for permission in permissions]

		return Book.query\
			.filter(Book.id.in_(permissions_id))\
			.paginate(page, page_size, False)

	except exc.SQLAlchemyError:
		abort(500)


def get_current_user_book_per_language_paginator(language_id: int, page: int, page_size: int):
	if current_user.is_admin():
		return get_books_per_language_paginator(language_id, page, page_size)
	else:
		return get_normal_user_book_per_language_paginator(current_user.id, language_id, page, page_size)


def get_normal_user_book_per_language_paginator(user_id: int, language_id: int, page: int, page_size: int):
	try:
		permissions = BookPermission.query\
			.with_entities(BookPermission.book_id)\
			.filter(BookPermission.user_id == user_id)\
			.all()

		allowed_books_ids = [permission.book_id for permission in permissions]

		return Book.query\
			.join(Language, Book.languages)\
			.filter(
				and_(
					Book.id.in_(allowed_books_ids),
					Language.id == language_id
				)
			).order_by(Book.title.asc())\
			.paginate(page, page_size, False)

	except exc.SQLAlchemyError:
		abort(500)


def get_books_per_language_paginator(language_id: int, page: int, page_size: int):
	return Book.query \
		.join(books_languages_link) \
		.filter(books_languages_link.c.lang_code == language_id) \
		.paginate(page, page_size)


def get_current_user_book_per_publisher_paginator(publisher_id: int, page: int, page_size: int):
	if current_user.is_admin():
		return get_books_per_publisher_paginator(publisher_id, page, page_size)
	else:
		return get_normal_user_book_per_language_paginator(current_user.id, publisher_id, page, page_size)


def get_normal_user_books_per_publisher_paginator(user_id, publisher_id, page, page_size):
	try:
		books = Book.query\
			.with_entities(Book.id)\
			.join(books_publishers_link)\
			.filter(books_publishers_link.c.publisher == publisher_id)

		books_id = [book.id for book in books]

		permissions = BookPermission.query\
			.with_entities(BookPermission.book_id)\
			.where(
				and_(
					BookPermission.book_id.in_(books_id),
					BookPermission.user_id == user_id
				)
			)\
			.all()

		permissions_id = [permission.book_id for permission in permissions]

		return Book.query\
			.filter(Book.id.in_(permissions_id))\
			.paginate(page, page_size, False)

	except exc.SQLAlchemyError:
		abort(500)


def get_books_per_publisher_paginator(publisher_id: int, page: int, page_size: int):
	return Book.query \
		.join(books_publishers_link) \
		.filter(books_publishers_link.c.publisher == publisher_id) \
		.paginate(page, page_size)
