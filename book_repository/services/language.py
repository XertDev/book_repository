from flask_login import current_user
from sqlalchemy import func

from ..models import BookPermission, Language, Book


def get_language_name(language_id):
	lang = Language.query.with_entities(Language.lang_code).filter(Language.id == language_id).first()
	if not lang:
		return ""
	return lang.lang_code


def get_current_user_language_paginator(page: int, page_size: int):
	if current_user.is_admin():
		return get_all_language_paginator(page, page_size)
	else:
		return get_normal_user_language_paginator(current_user.id, page, page_size)


def get_all_language_paginator(page: int, page_size: int):
	return Language.query\
			.order_by(Language.lang_code.asc())\
			.paginate(page, page_size, False)


def get_normal_user_language_paginator(user_id: int, page: int, page_size: int):
	accessible = BookPermission.query \
		.with_entities(BookPermission.book_id) \
		.filter_by(user_id=user_id) \
		.all()

	accessible_id = [permission.book_id for permission in accessible]

	return Language.query\
		.join(Book, Book.languages)\
		.filter(Book.id.in_(accessible_id))\
		.group_by(Language.lang_code)\
		.having(func.count(Language.lang_code))\
		.order_by(Language.lang_code.asc())\
		.paginate(page, page_size, False)
