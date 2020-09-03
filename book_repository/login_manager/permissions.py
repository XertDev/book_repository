from flask import abort, request
from flask_principal import Permission
from sqlalchemy import and_

from .needs import admin_user, normal_user
from ..services.book_permission import get_user_book_permission_type
from ..models.app.book_permission import BookPermissionType
from ..models import Author, Language, Book, Publisher
from ..models import BookPermission as BookPermissionModel

admin_permission = Permission(admin_user)
normal_permission = Permission(admin_user, normal_user)


class BookPermission(Permission):
	"""
	Lazily loaded book edit permission
	"""
	def __init__(self, type):
		super().__init__()
		self._type = type

	def allows(self, identity):
		if identity.user.is_anonymous:
			return False

		if admin_permission.allows(identity):
			return True

		book_id = request.view_args.get("book_id")

		try:
			permission = get_user_book_permission_type(book_id=self._id, user_id=identity.id)
			return permission == self._type
		except RuntimeError:
			abort(500)


view_book_permission = BookPermission(BookPermissionType.VIEW)
edit_book_permission = BookPermission(BookPermissionType.EDIT)


class ViewAuthorPermission(Permission):
	"""
	Lazily loaded permission
	"""
	def __init__(self):
		super().__init__()

	def allows(self, identity):
		if identity.user.is_anonymous:
			return False

		if admin_permission.allows(identity):
			return True

		author_id = request.view_args.get("author_id")

		try:
			authors_books = Author.query\
				.filter(Author.id == author_id)\
				.first()\
				.books

			if not authors_books:
				abort(404)

			authors_books_id = [book.id for book in authors_books]

			accessible = BookPermissionModel.query\
				.where(and_(
					BookPermissionModel.user_id == identity.id,
					BookPermissionModel.book_id.in_(authors_books_id)
				)).count() > 0

			return accessible

		except RuntimeError:
			abort(500)


view_author_permission = ViewAuthorPermission()


class ViewLanguagePermission(Permission):
	"""
	Lazily loaded permission
	"""
	def __init__(self):
		super().__init__()

	def allows(self, identity):
		if identity.user.is_anonymous:
			return False

		if admin_permission.allows(identity):
			return True

		language_id = request.view_args.get("language_id")

		try:
			permissions = BookPermissionModel.query \
				.with_entities(BookPermissionModel.book_id) \
				.all()
			allowed_ids = [permission.book_id for permission in permissions]

			return Language.query\
				.join(Book, Book.languages)\
				.filter(
					and_(
						Language.id == language_id,
						Book.id.in_(allowed_ids)
					)
				).count() > 0

		except RuntimeError:
			abort(500)


view_language_permission = ViewLanguagePermission()


class ViewPublisherPermission(Permission):
	"""
	Lazily loaded permission
	"""
	def __init__(self):
		super().__init__()

	def allows(self, identity):
		if identity.user.is_anonymous:
			return False

		if admin_permission.allows(identity):
			return True

		publisher_id = request.view_args.get("publisher_id")

		try:

			publisher_books = Publisher.query\
				.with_entities(Publisher.id)\
				.filter(Publisher.id == publisher_id)\
				.first()

			publisher_books_ids = [book.id for book in publisher_books]

			permissions = BookPermissionModel.query \
				.with_entities(BookPermissionModel.book_id) \
				.all()
			allowed_ids = [permission.book_id for permission in permissions]

			return BookPermissionModel.query\
				.where(
					and_(
						BookPermissionModel.user_id == identity.id,
						BookPermissionModel.book_id.in_(allowed_ids)
						)
				).count() > 0

		except RuntimeError:
			abort(500)


view_publisher_permission = ViewPublisherPermission()
