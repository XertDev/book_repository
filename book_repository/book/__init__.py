from flask import Blueprint, abort, render_template, make_response, redirect
from flask_login import current_user, login_required
import os
import mimetypes

from ..login_manager.permissions import admin_permission, view_book_permission
from ..services.book import get_book_by_id, get_book_file_path, get_book_cover_path
from ..services.book_permission import get_user_book_permission_type
from ..models.app.book_permission import BookPermissionType
from ..file_provider import file_provider


book = Blueprint(
	"book",
	__name__,
	template_folder="templates",
	url_prefix="/book"
)


@book.route("/<int:book_id>/details")
@login_required
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


@book.route("/<int:book_id>/cover")
@view_book_permission.require()
def book_cover(book_id):
	path = get_book_cover_path(book_id)

	if not path:
		return redirect("https://bulma.io/images/placeholders/256x256.png")

	file = file_provider.load(path)

	response = make_response(file)
	response.headers.set("Content-Type", "image/jpeg")
	response.headers.set("Content-Disposition", "inline")
	return response


@book.route("/<int:book_id>/version/<string:version>")
@view_book_permission.require()
def book_file(book_id: int, version: str):
	path = get_book_file_path(book_id, version)

	if not path:
		abort(404)

	file = file_provider.load(path)
	mimetype = mimetypes.types_map.get(".{}".format(version.lower()), "application/octet-stream")

	response = make_response(file)
	response.headers.set("Content-Type", mimetype)
	response.headers.set("Content-Disposition", "attachment", filename=os.path.basename(path))
	return response
