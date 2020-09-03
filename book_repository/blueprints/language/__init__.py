from flask import Blueprint, request, render_template
from flask_login import login_required

from ...services.language import get_current_user_language_paginator, get_language_name
from ...login_manager.permissions import view_language_permission
from ...services.book import get_current_user_book_per_language_paginator

language = Blueprint(
	"language",
	__name__,
	template_folder="templates",
	url_prefix="/lang"
)


@language.route("/")
@login_required
def all_languages():
	page = request.args.get("page", 1, type=int)
	page_size = request.args.get("page_size", 10, type=int)

	paginator = get_current_user_language_paginator(page, page_size)
	return render_template("languages_list.html", paginator=paginator)


@language.route("/<int:language_id>/details")
@view_language_permission.require()
def language_details(language_id):
	page = request.args.get("page", 1, type=int)
	page_size = request.args.get("page_size", 8, type=int)

	paginator = get_current_user_book_per_language_paginator(language_id, page, page_size)
	subtitle = get_language_name(language_id).upper()

	extra_params = {
		"language_id": language_id,
	}

	return render_template(
		"paginated_bookshelf.html", paginator=paginator,
		selection_title=subtitle, extra_params=extra_params)
