from flask import Blueprint, render_template

from ..login_manager.permissions import normal_permission
from ..services.book import get_current_user_latest_books

dashboard = Blueprint(
	"dashboard",
	__name__,
	template_folder="templates"
)


@dashboard.route("/")
@normal_permission.require()
def index():
	latest_books = get_current_user_latest_books(8)
	return render_template("index.html", latest_books=latest_books)
