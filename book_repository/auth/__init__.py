from flask import Blueprint, render_template

from book_repository.auth.login_form import LoginForm

auth = Blueprint(
	"auth",
	__name__,
	template_folder="templates"
)


@auth.route("/login")
def login():
	form = LoginForm()
	return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
	return "logout"
