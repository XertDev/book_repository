from flask import Blueprint, abort, render_template
from flask_login import current_user

from ..login_manager.permissions import admin_permission
from ..services.book import get_book_by_id
from ..services.book_permission import get_user_book_permission_type
from ..models.app.book_permission import  BookPermissionType


book = Blueprint(
	"book",
	__name__,
	template_folder="templates",
	url_prefix="/book"
)


@book.route("/<int:book_id>/details")
def book_details(book_id: int):
	if admin_permission.can():
		permission_level = BookPermissionType.EDIT
	else:
		permission_level = get_user_book_permission_type(current_user.id, book_id)

	if not permission_level:
		abort(403)

	book_data = get_book_by_id(book_id)
	return render_template(
		"book_details.html",
		book=book_data
	)

