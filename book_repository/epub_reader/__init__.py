from flask import Blueprint, render_template

from ..login_manager.permissions import view_book_permission
from ..services.book import get_book_by_id


epub_reader = Blueprint(
	"epub_reader",
	__name__,
	template_folder="templates",
	url_prefix="/epub_reader"
)


@epub_reader.route("/<int:book_id>")
@view_book_permission.require()
def read(book_id):
	book = get_book_by_id(book_id)
	return render_template("reader.html", book=book)
