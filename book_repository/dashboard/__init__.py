from flask import Blueprint, render_template
from flask_login import current_user

from ..login_manager.permissions import normal_permission
from ..services.book import get_latest_user_visible

dashboard = Blueprint(
	"dashboard",
	__name__,
	template_folder="templates"
)


@dashboard.route("/")
@normal_permission.require()
def index():
	latest_books = get_latest_user_visible(current_user)
	return render_template("index.html", latest_books=latest_books)
