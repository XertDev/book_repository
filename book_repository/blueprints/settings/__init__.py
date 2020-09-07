from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from .push_emails_forms import AddPushEmailForm, DelPushEmailForm
from ...services.email import add_push_email, del_push_email


settings = Blueprint(
	"settings",
	__name__,
	template_folder="templates",
	url_prefix="/settings"
)


SETTING_SECTIONS = {
	"Profile": "settings.profile",
	"Push emails": "settings.push_emails"
}


@settings.context_processor
def sections():
	return dict(setting_sections=SETTING_SECTIONS)


@settings.route("/")
@settings.route("/profile")
@login_required
def profile():
	return render_template("profile.html")


@settings.route("/push_emails", methods=["GET", "POST"])
@login_required
def push_emails():
	add_form = AddPushEmailForm()
	del_form = DelPushEmailForm()

	if add_form.validate_on_submit():
		add_push_email(current_user.id, add_form.data["email"], add_form.data["name"])

	if del_form.validate_on_submit():
		del_push_email(current_user.id, del_form.data["email_id"])

	return render_template("push_emails.html", add_form=add_form, del_form=del_form)



