from flask import abort, request
from flask_principal import Permission

from .needs import admin_user, normal_user
from ..services.book_permission import get_user_book_permission_type
from ..models.app.book_permission import BookPermissionType

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
