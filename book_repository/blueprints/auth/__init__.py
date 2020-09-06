from urllib.parse import urlparse, urljoin

from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user, logout_user

from ..auth.login_form import LoginForm
from ...services.user import authenticate

auth = Blueprint(
	"auth",
	__name__,
	template_folder="templates"
)


@auth.route("/login", methods=("GET", "POST"))
def login():
	form = LoginForm(request.form)
	if form.validate_on_submit():
		data = form.data
		if authenticate(data["username"], data["password"]):
			next_page = request.args.get("next")
			if next_page:
				if is_safe_url(next_page):
					return redirect(next_page)
				else:
					return abort(400)
			return redirect(url_for("dashboard.index"))

		return render_template("login.html", msg="Invalid username or password", form=form)

	if not current_user.is_authenticated:
		return render_template("login.html", form=form)

	return redirect(url_for("dashboard.index"))


@auth.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("auth.login"))


def is_safe_url(target):
	ref_url = urlparse(request.host_url)
	test_url = urlparse(urljoin(request.host_url, target))
	return test_url.scheme in ('http', 'https') and \
		ref_url.netloc == test_url.netloc
