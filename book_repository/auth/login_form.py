from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
	"""Login to user account"""

	username = StringField(
		"Username",
		[
			DataRequired()
		]
	)

	password = PasswordField(
		"Password",
		[
			DataRequired("Please enter a password")
		]
	)
