from flask_login import current_user
from sqlalchemy import exc, func
from flask import abort

from ..models import Author, BookPermission, Book


def get_author_name(author_id):
	return Author.query.with_entities(Author.name).filter_by(id=author_id).first().name


def get_current_user_all_authors_paginator(page: int, page_size: int, search=None):
	if current_user.is_admin():
		return get_all_authors_paginator(page, page_size, search)
	else:
		return get_normal_user_authors_paginator(current_user.id, page, page_size, search)


def get_all_authors_paginator(page: int, page_size: int, search=None):
	try:
		query = Author.query

		if search:
			query = query.filter(Author.name.like("%{}%".format(search)))

		return query\
			.order_by(Author.name.asc())\
			.paginate(page, page_size, False)
	except exc.SQLAlchemyError:
		abort(500)


def get_normal_user_authors_paginator(user_id: int, page: int, page_size: int, search=None):
	try:
		query = Author.query

		accessible = BookPermission.query \
			.with_entities(BookPermission.book_id) \
			.filter_by(user_id=user_id) \
			.all()

		accessible_id = [permission.book_id for permission in accessible]

		query = query.join(Book, Author.books).filter(Book.id.in_(accessible_id))

		if search:
			query = query.filter(Author.name.like("%{}%".format(search)))

		return query.\
			group_by(Author.name)\
			.having(func.count(Author.name) > 0)\
			.order_by(Author.name.asc())\
			.paginate(page, page_size, False)

	except exc.SQLAlchemyError as e:
		abort(500)


