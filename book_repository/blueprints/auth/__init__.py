from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

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
			return redirect(url_for("dashboard.index"))

		return render_template("login.html", msg="Invalid username or password", form=form)

	if not current_user.is_authenticated:
		return render_template("login.html", form=form)

	# todo: next redirecting
	return redirect(url_for("dashboard.index"))


@auth.route("/logout")
def logout():
	return "logout"
