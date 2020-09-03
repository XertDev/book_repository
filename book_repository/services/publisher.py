from flask_login import current_user
from sqlalchemy import func

from ..models import Publisher, Book
from .book_permission import get_user_accessible_books_ids


def get_publisher_name(publisher_id):
	publisher = Publisher.query\
		.with_entities(Publisher.name)\
		.filter(Publisher.id == publisher_id)\
		.first()
	if not publisher:
		return ""

	return publisher.name


def get_current_user_publisher_paginator(page: int, page_size: int):
	if current_user.is_admin():
		return get_all_publishers_paginator(page, page_size)
	else:
		return get_normal_user_publisher_paginator(current_user.id, page, page_size)


def get_all_publishers_paginator(page: int, page_size: int):
	return Publisher.query\
			.order_by(Publisher.name.asc())\
			.paginate(page, page_size, False)


def get_normal_user_publisher_paginator(user_id: int, page: int, page_size: int):
	accessible_ids = get_user_accessible_books_ids(user_id)

	return Publisher.query\
		.join(Book, Book.publishers)\
		.filter(Book.id.in_(accessible_ids))\
		.group_by(Publisher.name)\
		.having(func.count(Publisher.name))\
		.order_by(Publisher.name.asc())\
		.paginate(page, page_size, False)
