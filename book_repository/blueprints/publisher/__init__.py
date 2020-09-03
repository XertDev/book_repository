from flask import Blueprint, request, render_template
from flask_login import login_required

from ...services.publisher import get_current_user_publisher_paginator, get_publisher_name
from ...login_manager.permissions import view_publisher_permission
from ...services.book import get_current_user_book_per_publisher_paginator

publisher = Blueprint(
	"publisher",
	__name__,
	template_folder="templates",
	url_prefix="/publisher"
)


@publisher.route("/")
@login_required
def all_publishers():
	page = request.args.get("page", 1, type=int)
	page_size = request.args.get("page_size", 10, type=int)

	paginator = get_current_user_publisher_paginator(page, page_size)
	return render_template("publishers_list.html", paginator=paginator)


@publisher.route("/<int:publisher_id>/details")
@view_publisher_permission.require()
def publisher_details(publisher_id):
	page = request.args.get("page", 1, type=int)
	page_size = request.args.get("page_size", 8, type=int)

	paginator = get_current_user_book_per_publisher_paginator(publisher_id, page, page_size)
	subtitle = get_publisher_name(publisher_id).title()

	extra_params = {
		"publisher_id": publisher_id,
	}

	return render_template(
		"paginated_bookshelf.html", paginator=paginator,
		selection_title=subtitle, extra_params=extra_params)
