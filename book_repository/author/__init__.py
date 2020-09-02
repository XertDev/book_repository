from flask import Blueprint, request, render_template
from flask_login import login_required

from ..services.author import get_current_user_all_authors_paginator, get_author_name
from ..services.book import get_current_user_books_per_author_paginator
from ..login_manager.permissions import view_author_permission


author = Blueprint(
	"author",
	__name__,
	template_folder="templates",
	url_prefix="/author"
)


@author.route("/")
@login_required
def all_authors():
	page = request.args.get("page", 1, type=int)
	page_size = request.args.get("page_size", 10, type=int)
	search = request.args.get("q", "", type=str)

	search = None if search == "" else search

	paginator = get_current_user_all_authors_paginator(page, page_size, search)

	extra_params = {
		"q": search
	}

	return render_template("authors_list.html", paginator=paginator, extra_params=extra_params)


@author.route("/<int:author_id>/details")
@view_author_permission.require()
def author_details(author_id):
	page = request.args.get("page", 1, type=int)
	page_size = request.args.get("page_size", 8, type=int)

	paginator = get_current_user_books_per_author_paginator(author_id, page, page_size)
	subtitle = get_author_name(author_id).title()

	extra_params = {
		"author_id": author_id,
	}

	return render_template(
		"paginated_bookshelf.html", paginator=paginator,
		selection_title=subtitle, extra_params=extra_params)
